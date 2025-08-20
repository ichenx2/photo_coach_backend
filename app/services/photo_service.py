# 圖片上傳、圖片格式處理等
import os
import uuid
from pathlib import Path

from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.schemas.photo_schema import PhotoIn
from app.db.photo_crud import create_photo

# 使用絕對路徑，與 main.py 中的 STATIC_DIR 保持一致
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_photo(file: UploadFile, user_id: int, subtask_id: int, db: Session):
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # 儲存實際文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 3: 儲存圖片資訊到資料庫
    photo = create_photo(db, PhotoIn(
        user_id=user_id,
        subtask_id=subtask_id,
        file_path=filename  # 儲存完整的 URL 路徑
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return new_photo