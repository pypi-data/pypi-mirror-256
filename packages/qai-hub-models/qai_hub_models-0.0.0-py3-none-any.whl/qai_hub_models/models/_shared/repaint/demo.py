from __future__ import annotations

from typing import Type

from qai_hub_models.models._shared.repaint.app import RepaintMaskApp
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebAsset, load_image
from qai_hub_models.utils.base_model import BaseModel


# Run repaint app end-to-end on a sample image.
# The demo will display the predicted image in a window.
def repaint_demo(
    model_type: Type[BaseModel],
    default_image: str | CachedWebAsset,
    default_mask: str | CachedWebAsset,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_type)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    parser.add_argument(
        "--mask",
        type=str,
        default=default_mask,
        help="test mask file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(model_type, args)
    image = load_image(args.image)
    mask = load_image(args.mask)
    print("Model Loaded")

    # Run app
    app = RepaintMaskApp(model)
    if not is_test:
        image.show(title="Model Input")
    out = app.paint_mask_on_image(image, mask)[0]

    if not is_test:
        out.show(title="Repainted (Model Output)")
