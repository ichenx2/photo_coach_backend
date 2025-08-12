from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Skill, LearningRecord
from app.schemas.skill_schema import SkillOut, UpdateProgress,UserSkillOut
from app.services.record_service import get_user_skills_with_names, update_progress_from_photo
from typing import Dict, List
from app.schemas.skill_schema import PhotoProgressIn

router = APIRouter()

@router.get("/skills", response_model=List[SkillOut])
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

@router.get("/users/{user_id}/skills", response_model=List[UserSkillOut])
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    return get_user_skills_with_names(user_id, db)

@router.post("/users/{user_id}/photo-progress", response_model=List[UserSkillOut])
def update_photo_progress(
    user_id: int, 
    body: PhotoProgressIn, 
    db: Session = Depends(get_db)
):
    return update_progress_from_photo(user_id, body.photo_result, db)

