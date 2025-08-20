from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.db.photo_repo import (
    create_photo, upsert_analysis,
    get_photo_detail, list_photos, delete_photo
)
from app.schemas.photo_schema import (
    PhotoCreate, AnalysisIn, PhotoOut, PhotosListResponse
)

router = APIRouter(prefix="/photos", tags=["photos"])

@router.post("", summary="建立照片")
def create_photo_api(body: PhotoCreate, db: Session = Depends(get_db)):
    pid = create_photo(db, body.image_url, body.thumbnail_url, body.captured_at)
    return {"id": pid}

@router.put("/{photo_id}/analysis", summary="寫入/覆寫分析（新格式）")
def upsert_analysis_api(photo_id: str, body: AnalysisIn, db: Session = Depends(get_db)):
    if not get_photo_detail(db, photo_id):
        raise HTTPException(status_code=404, detail="photo not found")
    upsert_analysis(db, photo_id, body.observation, body.techniques)
    return {"ok": True}

@router.get("/{photo_id}", response_model=PhotoOut, summary="單張（含分析）")
def get_photo_api(photo_id: str, db: Session = Depends(get_db)):
    data = get_photo_detail(db, photo_id)
    if not data:
        raise HTTPException(status_code=404, detail="photo not found")
    return data

@router.get("", response_model=PhotosListResponse, summary="列表（含分析摘要）")
def list_photos_api(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return list_photos(db, limit, offset)

@router.delete("/{photo_id}", summary="刪除照片（連動刪分析）")
def delete_photo_api(photo_id: str, db: Session = Depends(get_db)):
    ok = delete_photo(db, photo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="photo not found")
    return {"ok": True}
