import PIL.Image
import io
from PIL import ImageDraw as _ImageDraw, ImageFont as _ImageFont
import numpy as _np
import pathlib as _pathlib
import site as _site
import os as _os

from .image import Image, convert as _convert


class Font:
    ARIALNB = _os.path.join(_os.path.join(_site.getsitepackages()[1], 'apidevtools'), 'imgproc', 'fonts', 'ARIALNB.ttf')

    @staticmethod
    def fonts() -> list[str]:
        if _os.name != 'nt':
            raise OSError('system font list is available only for windows now')
        fonts_path = _pathlib.PurePath(_pathlib.Path.home().drive, _os.sep, 'windows', 'fonts')
        return [str(path.absolute()) for path in list(_pathlib.Path(fonts_path).glob('*.ttf'))]


async def generate(
        text: str = Image.default_text, size: int = 512, fonttf=Font.ARIALNB,
        bg_color: tuple[int, int, int] = (0, 0, 0), font_color: tuple[int, int, int] = (255, 255, 255)
) -> Image:
    fonttf = Font.fonts()[0]
    print(fonttf, type(fonttf))
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
    return await Image(img)


async def crop(image: bytes | io.BytesIO | PIL.Image.Image | Image) -> Image:
    """
    Crop any image to circle form.
    :param image:
    :return:
    """
    img = await _convert(image)
    size = min(img.size)
    alpha = PIL.Image.new('L', img.size, 0)
    _ImageDraw.Draw(alpha).pieslice([0, 0, size, size], 0, 360, fill=255)
    img = PIL.Image.fromarray(_np.dstack((_np.array(img), _np.array(alpha))))
    img = img.crop((0, 0, size, size))
    return await Image(img)


async def default(text: str = Image.default_text) -> Image:
    """
    Quick way to create an imgproc from some text.
    :param text:
    :return:
    """
    img = await generate(text)
    img = await crop(img)
    return img
