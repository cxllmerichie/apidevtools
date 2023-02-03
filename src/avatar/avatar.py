from PIL import ImageDraw, Image, ImageFont
from numpy import array, dstack
from io import BytesIO

from ..telegraph import upload


def image_to_bytesio(image: Image.Image) -> BytesIO:
    output = BytesIO()
    image.save(output, 'PNG')
    return output


def avatar(data: dict, size: int = 512, fonttf='fonts/ARIALNB.TTF', bg_color: tuple[int, int, int] = (0, 0, 0),
           font_color: tuple[int, int, int] = (255, 255, 255)) -> BytesIO:
    text = ''.join([value[0] for value in data.values()])
    font = ImageFont.truetype(font=fonttf, size=int(size * 0.6))
    image = Image.new(mode='RGB', size=(size, size), color=bg_color)
    draw = ImageDraw.Draw(image)
    _, _, width, height = draw.textbbox((0, 0), text, font=font)
    draw.text(xy=((size - width) / 2, (size - height) / 3), text=text, font=font, fill=font_color)
    return image_to_bytesio(image)


def crop(img_bytes: bytes) -> BytesIO:
    image = Image.open(BytesIO(img_bytes))
    size = min(image.size)
    alpha = Image.new('L', image.size, 0)
    ImageDraw.Draw(alpha).pieslice([0, 0, size, size], 0, 360, fill=255)
    image = Image.fromarray(dstack((array(image), array(alpha))))
    image = image.crop((0, 0, size, size))
    return image_to_bytesio(image)


async def avatar_url(data: dict) -> str:
    avt = avatar(data)
    avt = crop(avt.getvalue())
    return await upload(avt)
