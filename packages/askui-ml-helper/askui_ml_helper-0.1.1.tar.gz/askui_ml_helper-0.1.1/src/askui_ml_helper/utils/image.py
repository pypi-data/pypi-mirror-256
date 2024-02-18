import io
import os
import textwrap
from typing import Dict, Optional, Tuple

from huggingface_hub import hf_hub_download
from PIL import Image, ImageDraw, ImageFont

DEFAULT_FONT_PATH = "ybelkada/fonts"


def download_default_font():
    font_path = hf_hub_download(DEFAULT_FONT_PATH, "Arial.TTF")
    return font_path


def render_text(
    text: str,
    text_size: int = 36,
    text_color: str = "black",
    background_color: str = "white",
    left_padding: int = 5,
    right_padding: int = 5,
    top_padding: int = 5,
    bottom_padding: int = 5,
    font_bytes: Optional[bytes] = None,
    font_path: Optional[str] = None,
) -> Image.Image:
    """
    Render text. This script is entirely adapted from the original script that can be found here:
    https://github.com/google-research/pix2struct/blob/main/pix2struct/preprocessing/preprocessing_utils.py

    Args:
        text (`str`, *optional*, defaults to ):
            Text to render.
        text_size (`int`, *optional*, defaults to 36):
            Size of the text.
        text_color (`str`, *optional*, defaults to `"black"`):
            Color of the text.
        background_color (`str`, *optional*, defaults to `"white"`):
            Color of the background.
        left_padding (`int`, *optional*, defaults to 5):
            Padding on the left.
        right_padding (`int`, *optional*, defaults to 5):
            Padding on the right.
        top_padding (`int`, *optional*, defaults to 5):
            Padding on the top.
        bottom_padding (`int`, *optional*, defaults to 5):
            Padding on the bottom.
        font_bytes (`bytes`, *optional*):
            Bytes of the font to use. If `None`, the default font will be used.
        font_path (`str`, *optional*):
            Path to the font to use. If `None`, the default font will be used.
    """
    wrapper = textwrap.TextWrapper(
        width=80
    )  # Add new lines so that each line is no more than 80 characters.
    lines = wrapper.wrap(text=text)
    wrapped_text = "\n".join(lines)

    if font_bytes is not None and font_path is None:
        font = io.BytesIO(font_bytes)
    elif font_path is not None:
        font = font_path
    else:
        font = hf_hub_download(DEFAULT_FONT_PATH, "Arial.TTF")
        raise ValueError(
            "Either font_bytes or font_path must be provided. "
            f"Using default font {font}."
        )
    font = ImageFont.truetype(font, encoding="UTF-8", size=text_size)

    # Use a temporary canvas to determine the width and height in pixels when
    # rendering the text.
    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1), background_color))
    _, _, text_width, text_height = temp_draw.textbbox((0, 0), wrapped_text, font)

    # Create the actual image with a bit of padding around the text.
    image_width = text_width + left_padding + right_padding
    image_height = text_height + top_padding + bottom_padding
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)
    draw.text(
        xy=(left_padding, top_padding), text=wrapped_text, fill=text_color, font=font
    )
    return image


# Adapted from https://github.com/google-research/pix2struct/blob/0e1779af0f4db4b652c1d92b3bbd2550a7399123/pix2struct/preprocessing/preprocessing_utils.py#L87
def render_header(
    image: Image.Image, header: str, bbox: Dict[str, float], font_path: str, **kwargs
) -> Tuple[Image.Image, Tuple[float, float, float, float]]:
    """
    Renders the input text as a header on the input image and updates the bounding box.

    Args:
        image (Image.Image):
            The image to render the header on.
        header (str):
            The header text.
        bbox (Dict[str,float]):
            The bounding box in relative position (0-1), format ("x_min": 0,
                                                                 "y_min": 0,
                                                                 "x_max": 0,
                                                                 "y_max": 0).
        input_data_format (Union[str, ChildProcessError], optional):
            The data format of the image.

    Returns:
        Tuple[Image.Image, Dict[str, float] ]:
        The image with the header rendered and the updated bounding box.
    """
    assert os.path.exists(font_path), f"Font path {font_path} does not exist."
    header_image = render_text(text=header, font_path=font_path, **kwargs)
    new_width = max(header_image.width, image.width)

    new_height = int(image.height * (new_width / image.width))
    new_header_height = int(header_image.height * (new_width / header_image.width))

    new_image = Image.new("RGB", (new_width, new_height + new_header_height), "white")
    new_image.paste(header_image.resize((new_width, new_header_height)), (0, 0))
    new_image.paste(image.resize((new_width, new_height)), (0, new_header_height))

    new_total_height = new_image.height

    new_bbox = {
        "xmin": bbox["xmin"],
        "ymin": ((bbox["ymin"] * new_height) + new_header_height)
        / new_total_height,  # shift y_min down by the header's relative height
        "xmax": bbox["xmax"],
        "ymax": ((bbox["ymax"] * new_height) + new_header_height)
        / new_total_height,  # shift y_min down by the header's relative height
    }

    return (
        new_image,
        new_bbox,
        {
            "width": new_width,
            "height": new_height,
            "header_height": new_header_height,
            "total_height": new_total_height,
        },
    )