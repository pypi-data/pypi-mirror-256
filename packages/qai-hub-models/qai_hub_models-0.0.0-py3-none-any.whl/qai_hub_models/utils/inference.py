from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from typing import List, Tuple

import numpy as np
import qai_hub as hub
import torch
from qai_hub.public_rest_api import DatasetEntries

from qai_hub_models.utils.base_model import BaseModel, SourceModelFormat, TargetRuntime
from qai_hub_models.utils.input_spec import InputSpec

try:
    from qai_hub_models.utils.quantization_aimet import AIMETQuantizableMixin
except NotImplementedError:
    AIMETQuantizableMixin = None  # type: ignore


def prepare_compile_zoo_model_to_hub(
    model: BaseModel,
    source_model_format: SourceModelFormat,
    target_runtime: TargetRuntime,
    output_path: str = "",
    input_spec: InputSpec | None = None,
    check_trace: bool = True,
    prepare_compile_options_only: bool = False,
) -> Tuple[str | None, str]:
    """
    Args:

    - (source_model_format, target_runtime):  One of the followings

        (1) (ONNX, QNN)

            (a) For fp32 model, torch -> onnx -> qnn.

            (b) For AIMET, torch -> onnx + aimet encodings -> qnn

        (2) (ONNX, TFLITE)

            (a) For fp32, torch (fp32) -> onnx -> tflite,

            (b) For quantized, torch(AIMET) -> onnx + aimet .encodings -> tflite
            (via qnn-onnx-converter).

        (3) (TORCHSCRIPT, TFLITE)

            (a) Fp32: Invalid option for model not subclass of AIMETQuantizableMixin

            (b) For AIMETQuantizableMixin subclass, torch(AIMET) ->
            torchscript with embedded quantizer -> tflite

        (4) (TORCHSCRIPT, QNN)

            (a) For fp32, torch -> qnn (via qnn-torch-converter, aka
                    --use_qnn_pytorch_converter flag in Hub)

            (b) For AIMETQuantizableMixin subclass, torch(AIMET) ->
            torchscript with embedded quantizer -> qnn (via
                    qnn-pytorch-converter)

    Returns:

    Path to source model that can be used directly with hub.upload_model or
    hub.submit_compile_job.
    """
    is_aimet = AIMETQuantizableMixin is not None and isinstance(
        model, AIMETQuantizableMixin
    )

    model_name = model.__class__.__name__

    compilation_options = ""
    if target_runtime == TargetRuntime.QNN:
        compilation_options = "--target_runtime qnn_lib_aarch64_android"
    # Default compilation uses tflite already

    if is_aimet:
        if source_model_format == SourceModelFormat.ONNX:

            def export_model_func():
                return model.convert_to_onnx_and_aimet_encodings(
                    output_path, model_name=model_name
                )

        elif (
            source_model_format == SourceModelFormat.TORCHSCRIPT
            and target_runtime == TargetRuntime.TFLITE
        ):

            def export_model_func():
                traced_model = model.convert_to_quantized_torchscript(
                    input_spec=input_spec, check_trace=check_trace
                )
                model_path = os.path.join(output_path, model_name + ".pt")
                os.makedirs(output_path, exist_ok=True)
                torch.jit.save(traced_model, model_path)
                return model_path

        else:  # Torchscript and QNN

            def export_model_func():
                exported_model = model.convert_to_torchscript_and_aimet_encodings(  # type: ignore
                    output_path,
                    model_name=model_name,
                    input_spec=input_spec,
                )
                return exported_model

    else:  # fp32

        def export_model_func():
            traced_model = model.convert_to_torchscript(
                input_spec=input_spec, check_trace=check_trace
            )
            model_path = os.path.join(output_path, model_name + ".pt")
            os.makedirs(output_path, exist_ok=True)
            torch.jit.save(traced_model, model_path)
            return model_path

        if (
            target_runtime == TargetRuntime.TFLITE
            and source_model_format == SourceModelFormat.ONNX
        ):
            pass  # default is good

    if prepare_compile_options_only:
        return None, compilation_options
    else:
        return export_model_func(), compilation_options


def compile_zoo_model_to_hub(
    model: BaseModel,
    device: hub.Device,
    source_model_format: SourceModelFormat,
    target_runtime: TargetRuntime,
    calibration_data: DatasetEntries | None = None,
    input_spec: InputSpec | None = None,
    check_trace: bool = True,
) -> HubModel:
    """
    Similar to `prepare_compile_zoo_model_to_hub`, but also performs the
    compilation on AI Hub and construct a HubModel object.
    """
    is_aimet = AIMETQuantizableMixin is not None and isinstance(
        model, AIMETQuantizableMixin
    )

    if is_aimet:
        # Generally need a tempdir to export to
        context = tempfile.TemporaryDirectory()
    else:

        @contextmanager
        def no_op_context():
            yield None

        context = no_op_context()  # type: ignore

    if input_spec is None:
        input_spec = model.get_input_spec()

    model_name = model.__class__.__name__

    with context as tmp_dir:
        assert tmp_dir is not None
        source_model, compilation_options = prepare_compile_zoo_model_to_hub(
            model=model,
            source_model_format=source_model_format,
            target_runtime=target_runtime,
            output_path=tmp_dir,
            check_trace=check_trace,
        )

        compile_job = hub.submit_compile_job(
            model=source_model,
            input_specs=input_spec,
            device=device,
            name=f"{model_name}_{source_model_format.name}_{target_runtime.name}",
            options=compilation_options,
            calibration_data=calibration_data,
        )
    assert isinstance(compile_job, hub.CompileJob)
    if not compile_job.wait().success:
        job_msg = compile_job.get_status().message or "(no job failure message)"
        raise ValueError(f"Compile job {compile_job} failed: {job_msg}")

    hub_model = compile_job.get_target_model()
    assert hub_model is not None
    input_names = list(model.get_input_spec().keys())
    return HubModel(hub_model, input_names, device)


class HubModel:
    """
    Class that behaves like a pytorch model except when called, it runs an
        inference job on hub and returns a torch output.

    Intended to be passed as in input to app.py to run an app on-device.

    Parameters:
        input_names: List of input names to the model.
        device: Device on which to execute inference.
        hub_model_id: ID of Model stored in hub that will be used to run inference.
        model: If hub_model_id is absent, this model is compiled and used for inference.

    Returns:
        Callable that mimics the I/O of a torch model and evaluates inference on device.
    """

    def __init__(
        self,
        model: hub.Model,
        input_names: List[str],
        device: hub.Device,
    ):
        self.model = model
        self.input_names = input_names
        self.device = device

    def __call__(
        self, *input_tensors: torch.Tensor | List[torch.Tensor] | hub.Dataset
    ) -> torch.Tensor | Tuple[torch.Tensor, ...]:
        if len(input_tensors) == 1 and isinstance(input_tensors[0], hub.Dataset):
            inputs: hub.Dataset = input_tensors[0]
        else:
            # Upload dataset
            inputs = {}  # type: ignore
            for name, tensor in zip(self.input_names, input_tensors):
                if isinstance(tensor, (list, tuple)):
                    inputs[name] = [t.detach().numpy() for t in tensor]  # type: ignore
                else:
                    inputs[name] = [tensor.detach().numpy()]  # type: ignore
        inference_job = hub.submit_inference_job(
            model=self.model,
            inputs=inputs,
            device=self.device,
            name="zoo_inference_job",
        )
        assert isinstance(inference_job, hub.InferenceJob)
        if not inference_job.wait().success:
            job_msg = inference_job.get_status().message or "(no job failure message)"
            raise ValueError(f"Inference job {inference_job} failed: {job_msg}")

        output_ds_handle = inference_job.get_output_dataset()
        assert output_ds_handle is not None
        output_dataset = output_ds_handle.download()

        output_torch = [
            torch.from_numpy(np.concatenate(outputs, axis=0))
            for outputs in output_dataset.values()  # type: ignore
        ]
        if len(output_torch) == 1:
            return output_torch[0]
        return tuple(output_torch)
