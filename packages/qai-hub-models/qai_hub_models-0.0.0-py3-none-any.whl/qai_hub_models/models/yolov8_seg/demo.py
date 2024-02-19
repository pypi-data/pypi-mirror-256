from __future__ import annotations

from typing import Callable, Tuple

import qai_hub as hub
import torch

from qai_hub_models.models.yolov8_seg.app import YoloV8SegmentationApp
from qai_hub_models.models.yolov8_seg.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    YoloV8Segmentor,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.inference import HubModel

WEIGHTS_HELP_MSG = f"YoloV8-Segment checkpoint name. Valid checkpoints can be found in qai_hub_models/{MODEL_ID}/model.py"

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/bus.jpg"
)
OUTPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/out_bus_with_mask.png"
)


def yolov8_seg_demo(
    model_type: Callable[
        ...,
        Callable[
            [torch.Tensor],
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        ],
    ],
    default_weights: str,
    weights_help_msg: str,
    default_image: str,
    stride_multiple: int | None = None,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_type)
    image_help = "image file path or URL."
    if stride_multiple:
        image_help = f"{image_help} Image spatial dimensions (x and y) must be multiples of {stride_multiple}."

    parser.add_argument("--image", type=str, default=default_image, help=image_help)
    parser.add_argument(
        "--score_threshold",
        type=float,
        default=0.45,
        help="Score threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--iou_threshold",
        type=float,
        default=0.7,
        help="Intersection over Union (IoU) threshold for NonMaximumSuppression",
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
        "--device-name",
        type=str,
        default="Samsung Galaxy S23",
        help="If running on hub inference job, use this device.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="If specified, saves output image to this instead of showing.",
    )

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(model_type, args)
    if args.on_device:
        input_names = list(model.get_input_spec().keys())
        model_from_hub = hub.get_model(args.hub_model_id)
        hub_model = HubModel(
            model_from_hub, input_names, hub.Device(name=args.device_name)
        )
        app = YoloV8SegmentationApp(hub_model, args.score_threshold, args.iou_threshold)
    else:
        app = YoloV8SegmentationApp(model, args.score_threshold, args.iou_threshold)

    print("Model Loaded")

    image = load_image(args.image)
    output_image_with_masks = app.predict_segmentation_from_image(image)
    if not is_test:
        for i, img in enumerate(output_image_with_masks):
            if args.output_path:
                filename = args.output_path + f"_{i}.png"
                print(f"Image written to {filename}")
                img.save(filename)
            else:
                img.show()


def main(is_test: bool = False):
    yolov8_seg_demo(
        YoloV8Segmentor,
        DEFAULT_WEIGHTS,
        WEIGHTS_HELP_MSG,
        IMAGE_ADDRESS,
        is_test=is_test,
    )


if __name__ == "__main__":
    main()
