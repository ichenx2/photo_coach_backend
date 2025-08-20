from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class PhotoIn(BaseModel):
    user_id: int
    subtask_id: int
    file_path: str

    class Config:
        orm_mode = True

class PhotoOutBasic(BaseModel):
    id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
        
class PhotoCreate(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    captured_at: Optional[datetime] = None

class AnalysisIn(BaseModel):
    observation: List[str]
    techniques: Dict[str, List[str]]

class AnalysisOut(BaseModel):
    observation: List[str]
    techniques: Dict[str, List[str]]
    updated_at: Optional[datetime] = None

class PhotoOut(BaseModel):
    id: str 
    image_url: str
    thumbnail_url: Optional[str] = None
    captured_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    analysis: Optional[AnalysisOut] = None

class PhotosListResponse(BaseModel):
    items: List[PhotoOut]
    count: int
