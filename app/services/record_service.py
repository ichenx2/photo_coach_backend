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
def update_progress_from_photo(user_id: int, photo_result: dict, db: Session) -> list[UserSkillOut]:
    """
    photo_result 範例：
    {
        "構圖技巧": ["中心構圖"],
        "光線運用": ["柔光"],
        "拍攝角度": ["平視"]
    }
    """

    updated_records = []

    for category, skills in photo_result.items():
        for skill_name in skills:
            # 找到對應 skill
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                continue  # 如果資料庫沒有這個技能，跳過

            # 找到使用者的學習紀錄
            record = db.query(LearningRecord).filter_by(
                user_id=user_id,
                skill_id=skill.id
            ).first()

            if record:
                # 增加 0.1 進度
                record.progress = min(record.progress + 0.1, 1.0)  # 不超過 1.0

                # 如果進度滿 1，自動升級並重置
                if record.progress >= 1.0:
                    record.level += 1
                    record.progress = 0.0

                db.add(record)
                updated_records.append(record)

    if updated_records:
        db.commit()

    # 回傳最新資料
    return [
        UserSkillOut(
            skill_id=r.skill_id,
            skill_name=r.skill.name,
            progress=r.progress,
            level=r.level
        )
        for r in updated_records
    ]