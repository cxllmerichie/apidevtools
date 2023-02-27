import telegraph as _telegraph
import aiohttp as _aiohttp
import io


__telegraph: _telegraph.Telegraph = _telegraph.Telegraph()


async def upload(files: io.BytesIO | str | list[io.BytesIO | str]) -> None | str | list[str]:
    """
    Upload media to telegra.ph
    :param files:
    :return:
    """
    sources: list = await __telegraph.upload_file(f=files)
    urls = [f"https://telegra.ph{source.get('src')}" for source in sources]
    if len(urls) == 1:
        return urls[0]
    if len(urls) > 1:
        return urls
    return None
from asyncio import get_event_loop


if __name__ == '__main__':
    loop = get_event_loop()

    with open('LDR.jpg', 'rb') as file:
        img_bytes = file.read()
        img = Image(img_bytes)
        url = loop.run_until_complete(upload(img.bytesio))
        print(url)
