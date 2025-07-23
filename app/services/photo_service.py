# 圖片上傳、圖片格式處理等
import os
import uuid
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.photo import Photo

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_photo(file: UploadFile, user_id: int, topic: str, db: Session):
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    file_path = file_path.replace("\\", "/")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_photo = Photo(
        user_id=user_id,
        topic=topic,
        file_path=file_path
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo
