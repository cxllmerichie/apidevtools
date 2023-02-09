import PIL.Image
import io
from PIL import ImageDraw, ImageFont
from numpy import array, dstack
from abc import ABC

from .image import Image, convert


class Avatar(ABC):
    @staticmethod
    def image(
            text: str = Image.default_text, size: int = 512, fonttf='fonts/ARIALNB.TTF',
            bg_color: tuple[int, int, int] = (0, 0, 0), font_color: tuple[int, int, int] = (255, 255, 255)
    ) -> Image:
        """
        Generate image from apidevtools.avatar.image.Image. Supposed to be used as for instance: user avatar.
        By default has "N/A" white text on the black background.
        :param text:
        :param size:
        :param fonttf:
        :param bg_color:
        :param font_color:
        :return:
        """
        font = ImageFont.truetype(font=fonttf, size=int(size * 0.6))
        image = PIL.Image.new(mode='RGB', size=(size, size), color=bg_color)
        draw = ImageDraw.Draw(image)
        _, _, width, height = draw.textbbox((0, 0), text, font=font)
        draw.text(xy=((size - width) / 2, (size - height) / 3), text=text, font=font, fill=font_color)
        return Image(image)

    @staticmethod
    def crop(image: bytes | io.BytesIO | PIL.Image.Image | 'apidevtools.avatar.image.Image') -> Image:
        """
        Crop any image to circle form.
        :param image:
        :return:
        """
        image = convert(image)
        size = min(image.size)
        alpha = PIL.Image.new('L', image.size, 0)
        ImageDraw.Draw(alpha).pieslice([0, 0, size, size], 0, 360, fill=255)
        image = PIL.Image.fromarray(dstack((array(image), array(alpha))))
        image = image.crop((0, 0, size, size))
        return Image(image)

    @staticmethod
    def default(text: str = Image.default_text) -> Image:
        """
        Quick way to create an avatar from some text.
        :param text:
        :return:
        """
        image = Avatar.image(text)
        image = Avatar.crop(image)
        return image
