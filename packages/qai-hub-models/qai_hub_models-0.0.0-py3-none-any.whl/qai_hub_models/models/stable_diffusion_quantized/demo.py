import argparse

import numpy as np
from diffusers import DPMSolverMultistepScheduler, UNet2DConditionModel
from PIL import Image
from transformers import CLIPTokenizer

from qai_hub_models.models.stable_diffusion_quantized.app import StableDiffusionApp
from qai_hub_models.models.stable_diffusion_quantized.model import (
    ClipVITTextEncoder,
    Unet,
    VAEDecoder,
)
from qai_hub_models.utils.base_model import BasePrecompiledModel
from qai_hub_models.utils.inference import HubModel

DEFAULT_DEMO_PROMPT = "spectacular view of northern lights from Alaska"
DEFAULT_DEVICE_NAME = "Samsung Galaxy S23 Ultra"


def _get_hub_model(input_model: BasePrecompiledModel, device_name=DEFAULT_DEVICE_NAME):
    import qai_hub as hub

    # Upload model
    uploaded_model = hub.upload_model(input_model.get_target_model_path())
    inputs = list(input_model.get_input_spec().keys())
    return HubModel(uploaded_model, inputs, hub.Device(name=device_name))


# Run Stable Diffuison end-to-end on a given prompt. The demo will output an
# AI-generated image based on the description in the prompt.
def main(is_test: bool = False):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default=DEFAULT_DEMO_PROMPT,
        help="Prompt to generate image from.",
    )
    parser.add_argument(
        "--num_steps",
        default=5,
        type=int,
        help="The number of diffusion iteration steps (higher means better quality).",
    )
    parser.add_argument(
        "--seed",
        default=0,
        type=int,
        help="Random seed.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output file. By default show it interactively.",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=7.5,
        help="Strength of guidance (higher means more influence from prompt).",
    )
    parser.add_argument(
        "--device_name",
        type=str,
        default=DEFAULT_DEVICE_NAME,
        help="Device to run stable-diffusion demo on.",
    )
    args = parser.parse_args([] if is_test else None)

    # Load target models
    text_encoder = ClipVITTextEncoder.from_precompiled()
    unet = Unet.from_precompiled()
    vae_decoder = VAEDecoder.from_precompiled()

    text_encoder = _get_hub_model(text_encoder, DEFAULT_DEVICE_NAME)
    unet = _get_hub_model(unet, DEFAULT_DEVICE_NAME)
    vae_decoder = _get_hub_model(vae_decoder, DEFAULT_DEVICE_NAME)

    # Create tokenizer, scheduler and time_embedding required
    # for stable-diffusion pipeline.
    tokenizer = CLIPTokenizer.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base", subfolder="tokenizer", revision="main"
    )

    scheduler = DPMSolverMultistepScheduler(
        beta_start=0.00085,
        beta_end=0.012,
        beta_schedule="scaled_linear",
        num_train_timesteps=1000,
    )

    time_embedding = UNet2DConditionModel.from_pretrained(
        "runwayml/stable-diffusion-v1-5", subfolder="unet"
    ).time_embedding
    # Load Application
    app = StableDiffusionApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        tokenizer=tokenizer,
        scheduler=scheduler,
        time_embedding=time_embedding,
    )

    if not is_test:
        print()
        print("** Performing image generation with Stable Diffusion **")
        print()
        print("Prompt:", args.prompt)
        print("Number of steps:", args.num_steps)
        print("Guidance scale:", args.guidance_scale)
        print("Seed:", args.seed)
        print()
        print(
            "Note: This reference demo uses significant amounts of memory and may take a few minutes to run."
        )
        print()

    # Generate image
    image = app.generate_image(
        args.prompt,
        num_steps=args.num_steps,
        seed=args.seed,
        guidance_scale=args.guidance_scale,
    )

    pil_img = Image.fromarray(np.round(image.numpy() * 255).astype(np.uint8)[0])

    if not is_test:
        # Save or show image
        if args.output is None:
            pil_img.show()
        else:
            pil_img.save(args.output)
            print()
            print("Image saved to", args.output)
            print()


if __name__ == "__main__":
    main()
