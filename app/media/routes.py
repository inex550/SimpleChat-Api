from . import router

from fastapi import HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from os import path
from secrets import token_hex

from . import utils

from . import schemas


@router.post('/image/upload', response_model=schemas.UploadedFile)
async def upload_image(
    image: UploadFile = File(...)
):
    if not image.content_type.startswith('image'):
        raise HTTPException("Only image awailable for this method")

    filename = token_hex(16)
    filepath = path.join(utils.base_img_path, filename)
    with open(filepath, 'wb') as file:
        file.write(await image.read())

    return schemas.UploadedFile(name=filename)


@router.get("/image/{filename}")
async def get_image(filename: str):
    image_path = path.join(utils.base_img_path, filename)
    
    if not path.exists(image_path):
        raise HTTPException(404, 'Image Not Found')

    return StreamingResponse(utils.async_file(image_path))

