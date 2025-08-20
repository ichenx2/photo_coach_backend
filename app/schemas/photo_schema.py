# 定義上傳圖片、分析結果等格式
from pydantic import BaseModel
from datetime import datetime

class PhotoOut(BaseModel):
    id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
