#學習記錄用
from sqlalchemy.orm import Session
from app.models import LearningRecord, Skill
from app.schemas.skill_schema import UserSkillOut

def get_user_skills_with_names(user_id: int, db: Session) -> list[UserSkillOut]:
    records = (
        db.query(LearningRecord)
        .join(Skill, LearningRecord.skill_id == Skill.id)
        .filter(LearningRecord.user_id == user_id)
        .all()
    )

    return [
        UserSkillOut(
            skill_id=r.skill_id,
            skill_name=r.skill.name,
            progress=r.progress
        )
        for r in records
    ]
