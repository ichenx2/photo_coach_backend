# 定義上傳圖片、分析結果等格式
from pydantic import BaseModel
from datetime import datetime


class PhotoIn(BaseModel):
    user_id: int
    subtask_id: int
    file_path: str

    class Config:
        orm_mode = True

class PhotoOut(BaseModel):
    id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
