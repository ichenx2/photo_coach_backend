from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AIChatRequest(BaseModel):
    prompt: str

class AIChatResponse(BaseModel):
    reply: str
    sub_topics: List[str]
    visual_keywords: List[str]
    moodboard_url: Optional[str] = None
    itinerary: Optional[List[Dict[str, Any]]] = None
