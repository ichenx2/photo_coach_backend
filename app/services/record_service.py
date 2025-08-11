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

    updated_records = []
    for r in records:
        # 如果進度滿 1，自動升級並重置進度
        if r.progress >= 1:
            r.level += 1
            r.progress = 0
            db.add(r)
            updated_records.append(r)

    # 如果有更新等級或進度，儲存到資料庫
    if updated_records:
        db.commit()

    return [
        UserSkillOut(
            skill_id=r.skill_id,
            skill_name=r.skill.name,
            progress=r.progress,
            level=r.level 
        )
        for r in records
    ]
