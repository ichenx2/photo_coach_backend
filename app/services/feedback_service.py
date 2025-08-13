# 取得拍照建議、回饋紀錄儲存等
from sqlalchemy.orm import Session
from app.db.feedback_crud import create_feedback
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate
from app.services.ai_analysis_service import analyze_image

def analyze_and_store_feedback(photo_id: str, photo_data: bytes, db: Session, user_id: int) -> Feedback:
    """
    Analyze a photo and store feedback in the database.
    :param photo_id: Unique identifier for the photo
    :param photo_data: Binary data of the photo
    :param db: Database session
    :return: FeedbackCreate schema with analysis results
    """
    # Step 1: Analyze the photo using AI
    analysis_result = analyze_image(photo_data)

    # 例外處理：若分析失敗回傳錯誤訊息
    if 'error' in analysis_result:
        raise ValueError(f"Image analysis failed: {analysis_result['error']}")

    # Step 2: Prepare feedback data
    feedback_data = FeedbackCreate(
        photo_id=photo_id,
        content_analysis={
            "ai_score": analysis_result.get('ai_score', '0.0'),
            "highlight": analysis_result.get("highlight", "無"),
            "tip": analysis_result.get("tip", "無"),
            "suggestion": analysis_result.get("suggestion", "無"),
            "challenge": analysis_result.get("challenge", "無"),
            "completed_subtasks": analysis_result.get("completed_subtasks", [])
        },
    )

    # Step 3: Store feedback in the database
    feedback = create_feedback(db, feedback_data, user_id=user_id)

    return feedback
