from telegraph.aio import Telegraph as pypi_telegraph_Telegraph
import io
from aiohttp import ClientSession

# from .avatar.image import Image


class Telegraph:
    telegraph: pypi_telegraph_Telegraph = pypi_telegraph_Telegraph()

    @staticmethod
    async def upload(files: io.BytesIO | str | list[io.BytesIO | str]) -> None | str | list[str]:
        """
        Upload to telegra.ph
        :param files:
        :return:
        """
        sources: list = await Telegraph.telegraph.upload_file(f=files)
        urls = [f"https://telegra.ph{source.get('src')}" for source in sources]
        if len(urls) == 1:
            return urls[0]
        if len(urls) > 1:
            return urls
        return None

    # @staticmethod
    # async def download(url: str) -> Image | None:
    #     """
    #     Download picture by url from any source
    #     :param url:
    #     :return:
    #     """
    #     async with ClientSession() as session:
    #         async with session.get(url) as response:
    #             if response.status == 200:
    #                 return Image(await response.read())
    #     return None
