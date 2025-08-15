from fastapi import APIRouter
from app.schemas.feedback_schema import FeedbackIn, FeedbackOut
from app.services.feedback_service import generate_feedback  # ← 呼叫服務產出文字

router = APIRouter()

@router.post("/generate-feedback", response_model=FeedbackOut)
async def generate_feedback_endpoint(payload: FeedbackIn):
    # 交給服務層用新格式組 Prompt 並呼叫模型
    text = generate_feedback(payload.model_dump())
    return FeedbackOut(feedback=text)
