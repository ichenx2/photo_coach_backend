from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class Techniques(BaseModel):
    構圖技巧: List[str] = Field(default_factory=list)
    光線運用: List[str] = Field(default_factory=list)
    拍攝角度: List[str] = Field(default_factory=list)

class FeedbackIn(BaseModel):
    observation: List[str] = Field(default_factory=list)
    techniques: Techniques

class FeedbackOut(BaseModel):
    feedback: str

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
