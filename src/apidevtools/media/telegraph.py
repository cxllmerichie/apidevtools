# async def telegraph_upload(f: BytesIO, mime: str = 'image/png') -> Union[str, bool]:
#     """
#     Upload a file to Telegra.ph
#     :param f: File BytesIO
#     :param mime: File MIME type
#     :return: File URL on success
#     """
#     # f = await (max(message.photo, key=lambda c: c.width)).download(destination=BytesIO())
#     data = aiohttp.FormData()
#     data.add_field('file', f.read(), filename=f'file.{mime.split("/")[1]}', content_type=mime)
#     try:
#         async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
#                                          json_serialize=json.dumps) as session:
#             async with session.post(url='https://telegra.ph/upload', data=data) as r:
#                 r = await r.json()
#                 if isinstance(r, dict) and r.get('error'):
#                     return False
#                 if not r[-1]["src"].startswith('/'):
#                     r[-1]["src"] = '/' + r[-1]["src"]
#                 return f'https://telegra.ph{r[-1]["src"]}'
#     except aiohttp.ClientError:
#         return False


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


async def download(url: str) -> bytes | None:
    """
    Download media from any source
    :param url:
    :return:
    """
    async with _aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
    return None
