from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.photo_service import save_uploaded_photo
from app.models.photo import Photo
from app.schemas.photo_schema import PhotoOut
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    topic: str = Form(...),
    db: Session = Depends(get_db)
):
    photo = await save_uploaded_photo(file, user_id, topic, db)
    return {"message": "上傳成功", "photo_id": photo.id, "file_path": photo.file_path}

@router.get("/user/{user_id}", response_model=List[PhotoOut])
def get_user_photos(user_id: int, db: Session = Depends(get_db)):
    return db.query(Photo).filter(Photo.user_id == user_id).order_by(Photo.created_at.desc()).all()




from fastapi import HTTPException

# 修改
# def update_photo_file_path(photo_id: int, file_path: str, db: Session = Depends(get_db)):
#     photo = db.query(Photo).filter(Photo.id == photo_id).first()
#     if not photo:
#         raise HTTPException(status_code=404, detail="Photo not found")

#     photo.file_path = file_path
#     db.commit()
#     db.refresh(photo)
#     return {"message": "更新成功", "photo_id": photo.id, "new_path": photo.file_path}

# 刪除
@router.delete("/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="找不到這張照片")

    # 若需要一併刪除實體圖片檔案：
    try:
        import os
        if os.path.exists(photo.file_path):
            os.remove(photo.file_path)
    except Exception as e:
        print(f"刪檔失敗: {e}")

    db.delete(photo)
    db.commit()
    return {"message": "照片已刪除"}
