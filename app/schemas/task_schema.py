from pydantic import BaseModel
from datetime import datetime
from typing import List

# --- SubTask schemas ---

class SubTaskCreate(BaseModel):
    content: str
    tag: str
    suggested_position: str
    lighting_condition: str
    shooting_technique: str
    recommended_time: str

class SubTaskResponse(SubTaskCreate):
    id: int
    is_completed: bool

    model_config = {
        "from_attributes": True 
    }

# --- Task schemas ---

class TaskCreate(BaseModel):
    main_topic: str
    image_url: str
    subtasks: List[SubTaskCreate]

class TaskResponse(BaseModel):
    id: int
    main_topic: str
    image_url: str
    subtasks: List[SubTaskResponse]
    created_at: datetime

    model_config = {
        "from_attributes": True 
    }

class TaskUpdate(TaskCreate):
    id: int

    model_config = {
        "from_attributes": True 
    }