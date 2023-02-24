from apidevtools.media import imgproc
from asyncio import get_event_loop


async def amain():
    img = await imgproc.generate()
    await imgproc.crop(img)
    await imgproc.default()

    img = imgproc.Image(img.bytes)
    img.bytesio
    await img.url()
    img.image
    print(img.default_text)
    img = imgproc.convert(img)
    print(img)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(amain())
