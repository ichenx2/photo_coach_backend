from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.technique_service import analyze_image_techniques
from app.services.feedback_service import analyze_and_store_feedback
from app.schemas.feedback_schema import FeedbackResponse
from app.db.database import get_db
from app.models.photo import Photo
from app.services.photo_service import save_uploaded_photo


router = APIRouter()

@router.post("/techniques")
async def analyze_techniques(file: UploadFile = File(...)):
    """
    上傳照片 -> LLM (Gemini Vision) 判斷攝影技巧
    """
    photo_data = await file.read()
    result = analyze_image_techniques(photo_data)
    return result

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

        # Step 3: 執行分析 + 儲存分析紀錄
        analysis_result = analyze_and_store_feedback(photo.id, photo_data, db, user_id=current_user.id)

        # Step 4: 執行分析 + 儲存分析紀錄
        analysis_result = analyze_and_store_feedback(photo_id, photo_data, db, user_id=current_user.id)

        return FeedbackResponse.model_validate(analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing photo: {str(e)}")


