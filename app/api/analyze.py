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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze uploaded photo, store the image and analysis result.
    """
    try:
        # Step 1: 先儲存圖片（在讀取內容之前）
        photo = await save_uploaded_photo(file, current_user.id, subtask_id, db)
        
        # Step 2: 重置文件指標並讀取圖片資料用於分析
        file.file.seek(0)
        photo_data = await file.read()

        # Step 3: 執行分析 + 儲存分析紀錄
        analysis_result = analyze_and_store_feedback(photo.id, photo_data, db, current_user.id)

        # Step 4: 回傳分析結果
        return FeedbackResponse.model_validate(analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing photo: {str(e)}")


