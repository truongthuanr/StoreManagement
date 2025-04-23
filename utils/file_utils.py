import os
import uuid
from fastapi import UploadFile

async def save_upload_image(image: UploadFile, upload_dir: str):
    ext = os.path.splitext(image.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_dir, filename)

    os.makedirs(upload_dir, exist_ok=True)

    with open(filepath, "wb") as f:
        content = await image.read()
        f.write(content)

    return filename
