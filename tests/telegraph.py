from src.apidevtools.media.telegraph import upload, download
from asyncio import get_event_loop
from src.apidevtools.media.imgproc import default
from io import BytesIO


if __name__ == '__main__':
    loop = get_event_loop()

    # with open('LDR.jpg', 'rb') as file:
    #     img = BytesIO(file.read())
    #     url = loop.run_until_complete(upload(img))
    #     print(url)

    data = loop.run_until_complete(download('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png'))