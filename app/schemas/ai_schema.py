from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AIChatRequest(BaseModel):
    prompt: str

class AIChatResponse(BaseModel):
    reply: str
    sub_topics: List[str]
    moodboard_url: Optional[str] = None
    itinerary: Optional[List[Dict[str, Any]]] = None

class AIKeywordRequest(BaseModel):
    sub_topics: List[str]

class AIKeywordResponse(BaseModel):
    visual_keywords: List[str]