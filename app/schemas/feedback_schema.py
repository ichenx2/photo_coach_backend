# 分析回饋資料的request/response結構
from pydantic import BaseModel

class AnalysisInput(BaseModel):
    highlight: str
    challenge: str
    tip: str
    suggestion: str

class FeedbackOutput(BaseModel):
    feedback: str
