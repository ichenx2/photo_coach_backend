# 圖片上傳、圖片格式處理等
import os
import uuid
from pathlib import Path

from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.schemas.photo_schema import PhotoIn
from app.db.photo_crud import create_photo

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_photo(photo_data: bytes, filename: str, user_id: int, subtask_id: int, db: Session) -> Photo:

    # Step 1: 產生唯一 photo_id（UUID）
    photo_id = f"{uuid.uuid4().hex}{Path(filename).suffix}"
    photo_path = os.path.join(UPLOAD_DIR, photo_id)

    # Step 2: 儲存圖片
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(photo_path, "wb") as f:
        f.write(photo_data)

    # Step 3: 儲存圖片資訊到資料庫
    photo = create_photo(db, PhotoIn(
        user_id=user_id,
        subtask_id=subtask_id, 
        file_path=photo_path 
    ))

    return photo
    
    

