from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class FeedbackCreate(BaseModel):
    """
    Schema for creating feedback.
    """
    photo_id: str
    ai_score: int
    content_analysis: Dict[str, str]
    techniques: Optional[str]

class FeedbackResponse(BaseModel):
    """
    Schema for feedback response.
    """
    id: int
    photo_id: str
    ai_score: int
    content_analysis: Dict[str, str]
    techniques: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True