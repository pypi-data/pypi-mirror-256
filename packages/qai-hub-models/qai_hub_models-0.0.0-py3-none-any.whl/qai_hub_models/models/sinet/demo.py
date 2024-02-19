from qai_hub_models.models.sinet.app import SINetApp
from qai_hub_models.models.sinet.model import MODEL_ASSET_VERSION, MODEL_ID, SINet
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

INPUT_IMAGE_LOCAL_PATH = "sinet_demo.png"
INPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, INPUT_IMAGE_LOCAL_PATH
)


def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(SINet)
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL.",
    )
    args = parser.parse_args([] if is_test else None)

    # load image and model
    image = load_image(args.image)
    input_image = image.convert("RGB")
    app = SINetApp(model_from_cli_args(SINet, args))
    output = app.predict(input_image, False, False)
    output.save("sinet_demo_output.png")
    if not is_test:
        output.show()


if __name__ == "__main__":
    main()
