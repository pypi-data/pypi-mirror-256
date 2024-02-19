from typing import Callable

import torch
from PIL.Image import fromarray

from qai_hub_models.models.unet_segmentation.app import UNetSegmentationApp
from qai_hub_models.models.unet_segmentation.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    UNet,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "unet_test_image.jpg"
)


# Run unet segmentation app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
def unet_demo(
    model: Callable[..., Callable[[torch.Tensor, torch.Tensor], torch.Tensor]],
    default_image: str,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(UNet)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(UNet, args)
    image = load_image(args.image)
    print("Model Loaded")

    # Run app
    app = UNetSegmentationApp(model)
    mask = fromarray(app.predict(image))
    if not is_test:
        image.show(title="Model Input")
        mask.show(title="Mask (Model Output)")


def main(is_test: bool = False):
    unet_demo(
        UNet,
        IMAGE_ADDRESS,
        is_test,
    )


if __name__ == "__main__":
    main()
