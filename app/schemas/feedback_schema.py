from pydantic import BaseModel, Field
from typing import List

class Techniques(BaseModel):
    構圖技巧: List[str] = Field(default_factory=list)
    光線運用: List[str] = Field(default_factory=list)
    拍攝角度: List[str] = Field(default_factory=list)

class FeedbackIn(BaseModel):
    observation: List[str] = Field(default_factory=list)
    techniques: Techniques

class FeedbackOut(BaseModel):
    feedback: str

