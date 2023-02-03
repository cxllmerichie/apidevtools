from telegraph.aio import Telegraph
from io import BytesIO


TELEGRAPH = Telegraph()


async def upload(files: BytesIO | str | list[BytesIO | str]) -> None | str | list[str]:
    sources: list = await TELEGRAPH.upload_file(f=files)
    urls = [f"https://telegra.ph{source.get('src')}" for source in sources]
    if len(urls) == 1:
        return urls[0]
    if len(urls) > 1:
        return urls
    return None
