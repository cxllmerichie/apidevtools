from telegraph.aio import Telegraph
from aiohttp import ClientSession
import io

from .avatar.image import Image


telegraph: Telegraph = Telegraph()


async def upload(files: io.BytesIO | str | list[io.BytesIO | str]) -> None | str | list[str]:
    """
    Upload to telegra.ph
    :param files:
    :return:
    """
    sources: list = await telegraph.upload_file(f=files)
    urls = [f"https://telegra.ph{source.get('src')}" for source in sources]
    if len(urls) == 1:
        return urls[0]
    if len(urls) > 1:
        return urls
    return None


async def download(url: str) -> Image | None:
    """
    Download picture by url from any source
    :param url:
    :return:
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return Image(await response.read())
    return None
