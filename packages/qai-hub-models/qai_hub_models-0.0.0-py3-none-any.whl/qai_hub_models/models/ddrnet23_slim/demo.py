from qai_hub_models.models.ddrnet23_slim.app import DDRNetApp
from qai_hub_models.models.ddrnet23_slim.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DDRNet,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

INPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_input_image.png"
)


# Run DDRNet end-to-end on a sample image.
# The demo will display a image with the predicted segmentation map overlaid.
def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(DDRNet)
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(DDRNet, args)
    image = load_image(args.image)
    print("Model Loaded")

    app = DDRNetApp(model)
    output_img = app.segment_image(image)[0]
    if not is_test:
        output_img.show()


if __name__ == "__main__":
    main()
