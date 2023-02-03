from PIL import ImageDraw, Image, ImageFont
from numpy import array, dstack
from io import BytesIO
from dataclasses import dataclass
from abc import ABC

from ..telegraph import upload


@dataclass
class AvatarPicture:
    image: Image
    default_text = 'N/S'

    def bytes(self) -> bytes:
        return self.bytesio().getvalue()

    def bytesio(self) -> BytesIO:
        output = BytesIO()
        self.image.save(output, 'PNG')
        return output

    async def url(self) -> str:
        return await upload(self.bytesio())


class Avatar(ABC):
    @staticmethod
    def picture(
            data: dict | str = AvatarPicture.default_text, size: int = 512, fonttf='fonts/ARIALNB.TTF',
            bg_color: tuple[int, int, int] = (0, 0, 0), font_color: tuple[int, int, int] = (255, 255, 255)
    ) -> AvatarPicture:
        text = ''.join([str(value)[0] for value in data.values()]).upper() if isinstance(data, dict) else data
        font = ImageFont.truetype(font=fonttf, size=int(size * 0.6))
        image = Image.new(mode='RGB', size=(size, size), color=bg_color)
        draw = ImageDraw.Draw(image)
        _, _, width, height = draw.textbbox((0, 0), text, font=font)
        draw.text(xy=((size - width) / 2, (size - height) / 3), text=text, font=font, fill=font_color)
        return AvatarPicture(image)

    @staticmethod
    def crop(img_bytes: BytesIO) -> AvatarPicture:
        image = Image.open(img_bytes)
        size = min(image.size)
        alpha = Image.new('L', image.size, 0)
        ImageDraw.Draw(alpha).pieslice([0, 0, size, size], 0, 360, fill=255)
        image = Image.fromarray(dstack((array(image), array(alpha))))
        image = image.crop((0, 0, size, size))
        return AvatarPicture(image)

    @staticmethod
    def default(data: dict | str = AvatarPicture.default_text) -> AvatarPicture:
        avatar = Avatar.picture(data)
        avatar = Avatar.crop(avatar.bytesio())
        return avatar
