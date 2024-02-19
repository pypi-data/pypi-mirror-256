import argparse
import os
import subprocess
import tempfile

import qai_hub as hub
import yaml
from huggingface_hub import create_repo, delete_repo, upload_file

from qai_hub_models.utils.asset_loaders import (
    ASSET_BASES_DEFAULT_PATH,
    ASSET_CONFIG,
    QAIHM_WEB_ASSET,
    ModelZooAssetConfig,
)
from qai_hub_models.utils.config_loaders import (
    MODEL_IDS,
    MODEL_STATUS,
    QNN_PATH,
    QAIHMModelInfo,
    QAIHMModelPerf,
)

ORG_NAME = "qualcomm"

MODEL_CARD_TEMPLATE = open(
    os.path.join(os.path.dirname(__file__), "templates", "hf_model_card_template.md")
).read()

NOASSSETS_MODEL_CARD_TEMPLATE = open(
    os.path.join(
        os.path.dirname(__file__), "templates", "hf_noassets_model_card_template.md"
    )
).read()

PACKAGE_INSTALL_INSTRUCTIONS_WITH_EXTRAS = """
Install the package via pip:
```bash
pip install \"qai-hub-models[{model_id}]\"
```
"""
PACKAGE_INSTALL_INSTRUCTIONS = """
Install the package via pip:
```bash
pip install qai-hub-models
```
"""

HEADER_FOR_PERF_TABLE = """
| Device | Chipset | Target Runtime | Inference Time (ms) | Peak Memory Range (MB) | Precision | Primary Compute Unit | Target Model
| ---|---|---|---|---|---|---|---|
"""

NO_LICENSE = "This model's original implementation does not provide a LICENSE."


def main():
    """Generate a hugging face model card for each model, and save it in <model_dir>/HF_MODEL_CARD.md."""
    args = parse_args()

    # Login using HuggingFace CLI
    subprocess.run(["huggingface-cli", "login", "--token", args.huggingface_token])

    # Verify correct environment variables are set.
    ModelZooAssetConfig.load_asset_cfg(
        ASSET_BASES_DEFAULT_PATH, verify_env_has_all_variables=True
    )

    # Make a list of models, we wish to upload to HuggingFace
    assert args.all or args.models
    if args.models:
        model_list = args.models.split(",")
    else:
        model_list = MODEL_IDS

    for model_id in model_list:
        model_info = QAIHMModelInfo.from_model(model_id)
        model_perf = QAIHMModelPerf(
            perf_yaml_path=model_info.get_perf_yaml_path(), model_name=model_info.name
        )
        model_code_gen = {}
        model_code_gen_path = model_info.get_code_gen_yaml_path()
        if os.path.exists(model_code_gen_path):
            with open(model_code_gen_path, "r") as f:
                model_code_gen = yaml.safe_load(f)

        repo_id = ORG_NAME + "/" + model_info.name
        private = True if not args.public else False

        # Generate Proprietary model card for
        # models with no code or model asset to share
        # but want to show perf data.
        if model_code_gen.get("no_assets", False):
            model_card_path = model_info.get_hf_model_card_path()
            model_card = generate_hf_model_card(
                model_info,
                model_perf,
                model_code_gen,
                model_info.has_model_requirements(),
                NOASSSETS_MODEL_CARD_TEMPLATE,
                add_export_out=False,
            )
            if os.path.exists(model_card_path):
                os.remove(model_card_path)
            with open(model_card_path, "w") as model_card_file:
                model_card_file.write(model_card)

            create_repo(repo_id=repo_id, exist_ok=True, private=private)
            upload_file(
                path_or_fileobj=model_card_path,
                path_in_repo="README.md",
                repo_id=f"qualcomm/{model_info.name}",
            )
        elif (
            model_info.status == MODEL_STATUS.PUBLIC
            and os.path.exists(model_info.get_perf_yaml_path())
            and not model_perf.skip_overall
        ):
            print(f"Creating hugging face model card for {model_id}")

            # pass the name to be added to perf table
            model_card = generate_hf_model_card(
                model_info,
                model_perf,
                model_code_gen,
                model_info.has_model_requirements(),
            )
            model_card_path = model_info.get_hf_model_card_path()
            if os.path.exists(model_card_path):
                os.remove(model_card_path)
            with open(model_card_path, "w") as model_card_file:
                model_card_file.write(model_card)

            # Create repository.
            create_repo(repo_id=repo_id, exist_ok=True, private=private)

            upload_file(
                path_or_fileobj=model_card_path,
                path_in_repo="README.md",
                repo_id=f"qualcomm/{model_info.name}",
            )

            # Some models can be split into many modules
            names, tflite_ids, qnn_ids = model_perf.get_submodel_names_and_ids()

            # Upload the assets as well
            if not args.skip_upload_assets:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    for i in range(len(names)):

                        if not model_perf.skip_tflite:
                            # Download tflite asset in temp directory and upload to repo
                            tflite_model_path = os.path.join(
                                tmp_dir, f"{names[i]}.tflite"
                            )
                            hub.get_job(
                                tflite_ids[i]
                            ).model.producer.download_target_model(tflite_model_path)
                            upload_file(
                                path_or_fileobj=tflite_model_path,
                                path_in_repo=f"{names[i]}.tflite",
                                repo_id=f"qualcomm/{model_info.name}",
                            )

                        # Download qnn asset in temp directory and upload to repo
                        if not model_perf.skip_qnn:
                            is_precompiled = model_code_gen.get("is_precompiled", False)
                            extension = "bin" if is_precompiled else "so"
                            qnn_model_path = os.path.join(
                                tmp_dir, f"{names[i]}.{extension}"
                            )
                            if is_precompiled:
                                hub.get_job(qnn_ids[i]).model.download(qnn_model_path)
                            else:
                                hub.get_job(
                                    qnn_ids[i]
                                ).model.producer.download_target_model(qnn_model_path)

                            upload_file(
                                path_or_fileobj=qnn_model_path,
                                path_in_repo=f"{names[i]}.{extension}",
                                repo_id=f"qualcomm/{model_info.name}",
                            )
        else:
            try:
                delete_repo(repo_id=repo_id)
            except Exception:
                pass


def _get_compiled_model_upload_section(model_package: str, model_components: list):
    each_model_upload = ""
    for component in model_components:
        each_model_upload += f"""
{component}_model = hub.upload_model(model.{component}.get_target_model_path())"""

    return f"""
Step1: **Upload compiled model**

Upload compiled models from `{model_package}` on hub.
```python
import torch

import qai_hub as hub
from {model_package} import Model

# Load the model
model = Model.from_precompiled()
{each_model_upload}
```"""


def _get_compilation_section(model_package: str):
    return f"""
Step1: **Compile model**

To compile a PyTorch model to TFLite, we must first generate a TorchScript model in memory using the `jit.trace` method in PyTorch.

```python
import torch

import qai_hub as hub
from {model_package} import Model

# Load the model
torch_model = Model.from_pretrained()
torch_model.eval()

# Device
device = hub.Device("Samsung Galaxy S23")

# Trace model
input_shape = torch_model.get_input_spec()
sample_inputs = torch_model.sample_inputs()

pt_model = torch.jit.trace(torch_model, [torch.tensor(data[0]) for _, data in sample_inputs.items()])

# Compile model on a specific device
compile_job = hub.submit_compile_job(
    model=pt_model,
    device=device,
    input_specs=torch_model.get_input_spec(),
)

# Get target model to run on-device (see step 2 for how to run model on-device)
target_model = compile_job.get_target_model()

```"""


def _get_profile_models_section(is_precompiled: bool, model_components: list):
    if not is_precompiled:
        return """
profile_job = hub.submit_profile_job(
    model=target_model ,
    device=device,
)
"""
    all_model_profile = ""
    for component in model_components:
        all_model_profile += f"""
profile_job_{component} = hub.submit_profile_job(
    model={component}_model,
    device=device,
)"""
    return all_model_profile


def _get_inference_models_section(is_precompiled: bool, model_components: list):
    if not is_precompiled:
        return """
input_data = torch_model.sample_inputs()
inference_job = hub.submit_inference_job(
    model=target_model,
    device=device,
    inputs=input_data,
)

on_device_output = inference_job.download_output_data()
"""
    all_model_inference = ""
    for component in model_components:
        all_model_inference += f"""
input_data_{component} = {component}_model.sample_inputs()
inference_job_{component} = hub.submit_inference_job(
    model={component}_model,
    device=device,
    inputs=input_data_{component},
)
on_device_output_{component} = inference_job_{component}.download_output_data()
"""
    return all_model_inference


def _get_profile_model_intro(is_precompiled_model):
    model_state = "uploading compiled" if is_precompiled_model else "compiling"
    return f"After {model_state} models from step 1"


def _get_load_model_section(model_package):
    return f"""
### Load the model

Load the model:

```python
from {model_package} import Model

model = Model.from_pretrained()
```"""


def generate_hf_model_card(
    model_info: QAIHMModelInfo,
    model_perf: QAIHMModelPerf,
    model_code_gen: dict,
    needs_install_instructions: bool,
    model_card: str = MODEL_CARD_TEMPLATE,
    add_export_out: bool = True,
) -> str:
    """Generate a model_card for this model from the template found at hf_model_card_template.md"""

    is_precompiled_model = model_code_gen.get("is_precompiled", False)
    has_assets = not model_code_gen.get("no_assets", False)
    model_package = model_info.get_package_name()

    # Replace placeholders
    placeholder_to_replacement_map = [
        [
            "{hugging_face_metadata}",
            str(yaml.dump(model_info.get_hugging_face_metadata())),
        ],
        ["{model_details}", model_info.get_model_details()],
        [
            "{static_image}",
            ASSET_CONFIG.get_web_asset_url(model_info.id, QAIHM_WEB_ASSET.STATIC_IMG),
        ],
        ["{model_definition_url}", str(model_info.get_model_definition_path())],
        ["{demo_url}", str(model_info.get_demo_path())],
        [
            "{package_install_instructions}",
            PACKAGE_INSTALL_INSTRUCTIONS_WITH_EXTRAS
            if needs_install_instructions
            else PACKAGE_INSTALL_INSTRUCTIONS,
        ],
        ["{model_id}", model_info.id],
        ["{model_package}", model_package],
        ["{model_name}", model_info.name],
        [
            "{model_url}",
            f"qai_hub_models/models/{model_info.id}",
        ],
        ["{model_headline}", model_info.headline.strip(".")],
        ["{model_description}", model_info.description],
        ["{research_paper_title}", model_info.research_paper_title],
        ["{research_paper_url}", model_info.research_paper],
        ["{source_repo}", model_info.source_repo],
        [
            "{license_url}",
            model_info.license
            if model_info.license.casefold() != "none"
            else NO_LICENSE,
        ],
        ["{header_perf_table}", HEADER_FOR_PERF_TABLE],
        [
            "{body_perf_table}",
            model_perf.body_perf(is_precompiled_model, has_assets),
        ],
        [
            "{qaism_repo_url}",
            (
                ASSET_CONFIG.repo_url[:-1]
                if ASSET_CONFIG.repo_url.endswith("/")
                else ASSET_CONFIG
            ),
        ],
    ]

    model_components = model_code_gen.get("default_components", [])
    upload_or_compilation_section = (
        _get_compiled_model_upload_section(model_package, model_components)
        if is_precompiled_model
        else _get_compilation_section(model_package)
    )
    placeholder_to_replacement_map += [
        ["{compilation_section}", upload_or_compilation_section],
        ["{profile_model_intro}", _get_profile_model_intro(is_precompiled_model)],
        [
            "{profile_models}",
            _get_profile_models_section(is_precompiled_model, model_components),
        ],
        [
            "{inference_models}",
            _get_inference_models_section(is_precompiled_model, model_components),
        ],
    ]

    # Skip `Load model` section for pre-compiled models
    # since there is not much to do my loading this model class
    # in python.
    placeholder_to_replacement_map += [
        [
            "{load_model_section}",
            _get_load_model_section(model_package) if not is_precompiled_model else "",
        ],
    ]

    # Add placeholders for export specifically
    if add_export_out:
        if not model_perf.skip_tflite:
            placeholder_to_replacement_map += [
                ["{inference_time}", model_perf.tflite_inference_time],
                ["{peak_memory_range}", model_perf.tflite_peak_memory_range],
                ["{cu_summary}", model_perf.compute_unit_summary()],
            ]
        if not model_perf.skip_qnn:
            placeholder_to_replacement_map += [
                ["{inference_time}", model_perf.qnn_inference_time],
                ["{peak_memory_range}", model_perf.qnn_peak_memory_range],
                [
                    "{cu_summary}",
                    model_perf.compute_unit_summary(runtime_path=QNN_PATH),
                ],
            ]

    for placeholder, replacement in placeholder_to_replacement_map:
        model_card = model_card.replace(placeholder, replacement)
    return model_card


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--huggingface-token",
        type=str,
        required=True,
        help="HuggingFace token (write access needed)",
    )
    parser.add_argument(
        "--models",
        type=str,
        help="Comma-separated list of models to update on hugging face. "
        "Each entry should map to one of the folders in qai_hub_models/folders. "
        "All models within the folder that subclass from QAI Hub Models, "
        "will have their assets generated."
        "For example `--models mobilenet_v2,trocr`",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run on all models.",
    )
    parser.add_argument(
        "--skip-upload-assets",
        action="store_true",
        help="Skip uploading of assets to HuggingFace.",
    )
    parser.add_argument(
        "--public",
        action="store_true",
        help="Make the models specified public on hugging face.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
