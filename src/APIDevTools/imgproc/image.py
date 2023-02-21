import io
import PIL.Image

from .telegraph import upload as _upload
from ..utils import asyncinit


async def convert(image: bytes | io.BytesIO | PIL.Image.Image) -> PIL.Image.Image:
    """
    Create PIL.Image.Image from bytes or io.BytesIO.
    Also accepts PIL.Image.Image to simplify usage in Avatar and Image classes.
    :param image:
    :return:
    """
    if not isinstance(image, PIL.Image.Image):
        if isinstance(image, Image):
            image = await image.bytesio()
        elif isinstance(image, bytes):
            image = io.BytesIO(image)
        return PIL.Image.open(image)
    return image


@asyncinit
class Image:
    __image: PIL.Image.Image
    default_text = 'N/S'

    async def __init__(self, image: bytes | io.BytesIO, default_text: str = default_text):
        self.__image = await convert(image)
        self.default_text = default_text

    async def image(self) -> PIL.Image.Image:
        return self.__image

    async def bytes(self) -> bytes:
        return (await self.bytesio()).getvalue()

    async def bytesio(self) -> io.BytesIO:
        output = io.BytesIO()
        self.__image.save(output, 'PNG')
        return output

    async def url(self) -> str:
        return await _upload(await self.bytesio())
