from pydantic import BaseModel, condecimal
from typing import Optional

class SkillOut(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        orm_mode = True

class UserSkillOut(BaseModel):
    skill_id: int
    skill_name: str
    progress: float
    level: int

    class Config:
        orm_mode = True

class UpdateProgress(BaseModel):
    progress: condecimal(ge=0, le=1)

    class Config:
        schema_extra = {
            "example": {
                "progress": 0.5
            }
        }
