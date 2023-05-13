import asyncio

from src.apidevtools.media import imgproc


async def amain():
    img = imgproc.generate()
    imgproc.crop(img)
    imgproc.default()

    img = imgproc.Image(img.bytes)
    print(img.bytesio)
    print(await img.url())
    print(img.image)
    print(img.text)
    img = imgproc.convert(img)
    print(img)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
