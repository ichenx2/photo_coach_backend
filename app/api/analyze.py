import uuid, os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.feedback_service import analyze_and_store_feedback
from app.schemas.feedback_schema import FeedbackResponse
from app.db.database import get_db

UPLOAD_DIR = "uploads"  # 確保資料夾存在

router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def analyze_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Analyze uploaded photo, store the image and analysis result.
    """
    try:
        # Step 1: 讀取圖片資料
        photo_data = await file.read()

        # Step 2: 產生唯一 photo_id（UUID）
        photo_id = f"{uuid.uuid4().hex}{Path(file.filename).suffix}"
        photo_path = os.path.join(UPLOAD_DIR, photo_id)

        # Step 3: 儲存圖片
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(photo_path, "wb") as f:
            f.write(photo_data)

        # Step 4: 執行分析 + 儲存分析紀錄
        analysis_result = analyze_and_store_feedback(photo_id, photo_data, db)

        # Step 5: 回傳分析結果
        return FeedbackResponse.model_validate(analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing photo: {str(e)}")
