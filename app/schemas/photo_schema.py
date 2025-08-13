from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class PhotoCreate(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    captured_at: Optional[datetime] = None

class AnalysisIn(BaseModel):
    observation: List[str]
    techniques: Dict[str, List[str]]  # 需包含：構圖技巧、光線運用、拍攝角度

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
