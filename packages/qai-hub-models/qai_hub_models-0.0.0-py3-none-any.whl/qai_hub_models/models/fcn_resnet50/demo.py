from qai_hub_models.models.fcn_resnet50.app import FCN_ResNet50App
from qai_hub_models.models.fcn_resnet50.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    FCN_ResNet50,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

# Demo image comes from https://github.com/pytorch/hub/raw/master/images/deeplab1.png
# and has had alpha channel removed for use as input
INPUT_IMAGE_LOCAL_PATH = "fcn_demo.png"
INPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, INPUT_IMAGE_LOCAL_PATH
)


def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(FCN_ResNet50)
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL.",
    )

    args = parser.parse_args([] if is_test else None)

    # This FCN ResNet 50 demo comes from
    # https://pytorch.org/hub/pytorch_vision_fcn_resnet101/
    # load image and model
    image = load_image(args.image)
    input_image = image.convert("RGB")
    app = FCN_ResNet50App(model_from_cli_args(FCN_ResNet50, args))
    output = app.predict(input_image, False)

    if not is_test:
        output.show()


if __name__ == "__main__":
    main()
