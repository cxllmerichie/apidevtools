import PIL.Image
import io
from PIL import ImageDraw as _ImageDraw, ImageFont as _ImageFont
import numpy as _np

from .image import Image, convert


def generate(
        text: str = Image.default_text, size: int = 512, fonttf='fonts/ARIALNB.TTF',
        bg_color: tuple[int, int, int] = (0, 0, 0), font_color: tuple[int, int, int] = (255, 255, 255)
) -> Image:
    """
    Generate image from apidevtools.image.Image. Supposed to be used as for instance: user
    By default has "N/A" white text on the black background.
    :param text:
    :param size:
    :param fonttf:
    :param bg_color:
    :param font_color:
    :return:
    """
    font = _ImageFont.truetype(font=fonttf, size=int(size * 0.6))
    img = PIL.Image.new(mode='RGB', size=(size, size), color=bg_color)
    draw = _ImageDraw.Draw(img)
    _, _, width, height = draw.textbbox((0, 0), text, font=font)
    draw.text(xy=((size - width) / 2, (size - height) / 3), text=text, font=font, fill=font_color)
    return Image(img)


def crop(image: bytes | io.BytesIO | PIL.Image.Image | Image) -> Image:
    """
    Crop any image to circle form.
    :param image:
    :return:
    """
    img = convert(image)
    size = min(img.size)
    alpha = PIL.Image.new('L', img.size, 0)
    _ImageDraw.Draw(alpha).pieslice([0, 0, size, size], 0, 360, fill=255)
    img = PIL.Image.fromarray(_np.dstack((_np.array(img), _np.array(alpha))))
    img = img.crop((0, 0, size, size))
    return Image(img)


def default(text: str = Image.default_text) -> Image:
    """
    Quick way to create an avatar from some text.
    :param text:
    :return:
    """
    img = generate(text)
    img = crop(img)
    return img
