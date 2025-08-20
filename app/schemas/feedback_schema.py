from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime

class FeedbackContentAnalysis(BaseModel):
    ai_score: str 
    highlight: str
    tip: str
    suggestion: str
    challenge: str
    completed_subtasks: List[str]

class FeedbackCreate(BaseModel):
    """
    Schema for creating feedback.
    """
    user_id: int
    photo_id: int
    content_analysis: FeedbackContentAnalysis

class FeedbackResponse(BaseModel):
    """
    Schema for feedback response.
    """
    id: int
    photo_id: int
    content_analysis: Dict[str, Any]
    created_at: datetime

    model_config = {
        'from_attributes': True  
    }