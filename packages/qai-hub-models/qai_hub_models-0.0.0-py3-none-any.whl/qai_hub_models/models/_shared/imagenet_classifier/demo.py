from typing import Type

import torch

from qai_hub_models.models._shared.imagenet_classifier.app import ImagenetClassifierApp
from qai_hub_models.models._shared.imagenet_classifier.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    ImagenetClassifier,
)
from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    TEST_IMAGENET_IMAGE,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import (
    CachedWebModelAsset,
    load_image,
    load_json,
)
from qai_hub_models.utils.inference import compile_zoo_model_to_hub

IMAGENET_LABELS_ASSET = CachedWebModelAsset(
    "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json",
    MODEL_ID,
    MODEL_ASSET_VERSION,
    "imagenet_labels.json",
)


# Run Imagenet Classifier end-to-end on a sample image.
# The demo will print the predicted class to terminal.
def imagenet_demo(model_cls: Type[ImagenetClassifier], is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser.add_argument(
        "--image",
        type=str,
        default=TEST_IMAGENET_IMAGE,
        help="test image file path or URL",
    )
    parser.add_argument(
        "--on-device",
        action="store_true",
        help="If set, will evalute model using hub inference job instead of torch.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="Samsung Galaxy S23",
        help="If running on hub inference job, use this device.",
    )
    args = parser.parse_args([] if is_test else None)

    model = model_from_cli_args(model_cls, args)
    assert isinstance(model, ImagenetClassifier)
    if args.on_device:
        hub_model = compile_zoo_model_to_hub(
            model=model,
            device=args.device,
            target_runtime="onnx-qnn",
        )
        app = ImagenetClassifierApp(hub_model)
    else:
        app = ImagenetClassifierApp(model)
    print("Model Loaded")

    image = load_image(args.image)
    # Run app
    probabilities = app.predict(image)
    top5 = torch.topk(probabilities, 5)
    if not is_test:
        labels = load_json(IMAGENET_LABELS_ASSET)
        print("Top 5 predictions for image:\n")
        for i in range(5):
            print(f"{labels[top5.indices[i]]}: {100 * top5.values[i]:.3g}%\n")
