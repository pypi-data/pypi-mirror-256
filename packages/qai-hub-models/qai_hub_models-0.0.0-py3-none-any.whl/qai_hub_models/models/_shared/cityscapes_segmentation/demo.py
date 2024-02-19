import os
from typing import Type

import qai_hub as hub

from qai_hub_models.models._shared.cityscapes_segmentation.app import (
    CityscapesSegmentationApp,
)
from qai_hub_models.models._shared.cityscapes_segmentation.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    CityscapesSegmentor,
)
from qai_hub_models.utils.args import (
    TargetRuntime,
    get_model_cli_parser,
    model_from_cli_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.image_processing import pil_resize_pad, pil_undo_resize_pad
from qai_hub_models.utils.inference import HubModel, compile_zoo_model_to_hub

# This image showcases the Cityscapes classes (but is not from the dataset)
TEST_CITYSCAPES_LIKE_IMAGE_NAME = "cityscapes_like_demo_2048x1024.jpg"
TEST_CITYSCAPES_LIKE_IMAGE_ASSET = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, TEST_CITYSCAPES_LIKE_IMAGE_NAME
)


# Run Imagenet Classifier end-to-end on a sample image.
# The demo will print the predicted class to terminal.
def cityscapes_segmentation_demo(
    model_cls: Type[CityscapesSegmentor],
    model_id: str,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser.add_argument(
        "--image",
        type=str,
        help="test image file path or URL",
    )
    parser.add_argument(
        "--on-device",
        action="store_true",
        help="If set, will evalute model using hub inference job instead of torch.",
    )
    parser.add_argument(
        "--hub-model-id",
        type=str,
        default=None,
        help="If running on device inference, uses this model id.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="Samsung Galaxy S23",
        help="If running on hub inference job, use this device.",
    )
    parser.add_argument(
        "--device-os",
        default="",
        help="Optionally specified together with --device",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="if specified, will output the results to this folder instead of a pop-up window",
    )
    args = parser.parse_args([] if is_test else None)
    if args.hub_model_id is not None and not args.on_device:
        parser.error("--hub-model-id requires --on-device")

    if args.image is None:
        image = TEST_CITYSCAPES_LIKE_IMAGE_ASSET.fetch()
        image_name = TEST_CITYSCAPES_LIKE_IMAGE_NAME
    else:
        image = args.image
        image_name = os.path.basename(image)

    model = model_from_cli_args(model_cls, args)
    input_spec = model.get_input_spec()
    target_runtime = TargetRuntime.TFLITE
    assert isinstance(model, CityscapesSegmentor)
    if args.on_device:
        device = hub.Device(args.device, args.device_os)
        if args.hub_model_id:
            inference_model = HubModel(
                hub.get_model(args.hub_model_id),
                list(input_spec.keys()),
                device=device,
            )
        else:
            inference_model = compile_zoo_model_to_hub(
                model=model,
                device=device,
                source_model_format=model.preferred_hub_source_model_format(
                    target_runtime
                ),
                target_runtime=target_runtime,
            )
    else:
        inference_model = model
    app = CityscapesSegmentationApp(inference_model)
    print("Model Loaded")

    (_, _, height, width) = input_spec["image"][0]
    orig_image = load_image(image)
    image, _, padding = pil_resize_pad(orig_image, (height, width))

    # Run app
    image_annotated = app.predict(image)

    # Resize / unpad annotated image
    image_annotated = pil_undo_resize_pad(image_annotated, orig_image.size, padding)

    if args.output_dir:
        output_path = os.path.join(args.output_dir, image_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image_annotated.save(output_path)
    elif not is_test:
        image_annotated.show()
