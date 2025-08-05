from fastapi import APIRouter
from app.schemas.feedback_schema import AnalysisInput, FeedbackOutput
from app.services.feedback_service import generate_feedback

router = APIRouter()

@router.post("/generate-feedback", response_model=FeedbackOutput)
def generate_feedback_route(data: AnalysisInput):
    feedback = generate_feedback(data.dict())
    return {"feedback": feedback}
