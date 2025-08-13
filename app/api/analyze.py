from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.photo import Photo
from app.models.user import User
from app.schemas.feedback_schema import FeedbackResponse
from app.services.auth_service import get_current_user
from app.services.photo_service import save_uploaded_photo
from app.services.feedback_service import analyze_and_store_feedback


router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(
    file: UploadFile = File(...), 
    subtask_id: int = Form(...),
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze uploaded photo, store the image and analysis result.
    """
    try:
        # Step 1: 讀取圖片資料
        photo_data = await file.read()

        # Step 2: 儲存圖片
        photo = save_uploaded_photo(photo_data, file.filename, current_user.id, subtask_id, db)

        # 執行分析 + 儲存分析紀錄
        analysis_result = analyze_and_store_feedback(photo.id, photo_data, db)

        # 回傳分析結果
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing photo: {str(e)}")