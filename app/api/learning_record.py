from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Skill, LearningRecord
from app.schemas.skill_schema import SkillOut, UpdateProgress,UserSkillOut
from app.services.record_service import get_user_skills_with_names

from typing import List

router = APIRouter()

@router.get("/skills", response_model=List[SkillOut])
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

@router.get("/users/{user_id}/skills", response_model=List[UserSkillOut])
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    return get_user_skills_with_names(user_id, db)

@router.put("/users/{user_id}/skills/{skill_id}")
def update_progress(user_id: int, skill_id: int, progress: UpdateProgress, db: Session = Depends(get_db)):
    user_skill = db.query(LearningRecord).filter_by(user_id=user_id, skill_id=skill_id).first()
    if user_skill:
        user_skill.progress = progress.progress
        db.commit()
        return {"message": "更新成功"}
    else:
        return {"error": "找不到資料"}
