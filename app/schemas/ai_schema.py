from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AIChatRequest(BaseModel):
    prompt: str

class AIChatResponse(BaseModel):
    reply: str
    main_topic: str
    sub_topics: List[str]
    moodboard_url: Optional[str] = None
    itinerary: Optional[List[Dict[str, Any]]] = None

class AIKeywordRequest(BaseModel):
    main_topic: str
    sub_topics: List[str]

class AIKeywordResponse(BaseModel):
    visual_keywords: List[str]

class AIGeneratedTask(BaseModel):
    sub_topic: str
    task: str
    tag: str
    suggested_position: Optional[str] = ""
    lighting_condition: Optional[str] = ""
    shooting_technique: Optional[str] = ""
    recommended_time: Optional[str] = ""

class AIGeneratedTaskList(BaseModel):
    tasks: List[AIGeneratedTask]