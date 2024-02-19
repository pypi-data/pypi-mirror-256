import json


def onnx_elem_type_to_str(elem_type: int) -> str:
    if elem_type == 1:
        return "float32"
    elif elem_type == 2:
        return "uint8"
    elif elem_type == 3:
        return "int8"
    elif elem_type == 6:
        return "int8"
    elif elem_type == 10:
        return "float16"
    raise ValueError("Unsupported elem_type.")


def load_encodings(output_path, model_name):
    encodings_file = output_path / f"{model_name}.aimet" / f"{model_name}.encodings"
    with open(encodings_file) as f:
        encodings = json.load(f)
    return encodings["activation_encodings"]


def get_qnn_inputs(compile_job, sample_inputs):
    compile_job.target_shapes
    return dict(zip(compile_job.target_shapes.keys(), sample_inputs.values()))
