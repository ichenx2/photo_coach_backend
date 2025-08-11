# create_tables.py

from app.db.database import engine
from app.db.database import Base
from app.models.learning_record import LearningRecord
from app.db.database import SessionLocal


# app/insert_skills.py
db = SessionLocal()

from app.db.database import SessionLocal
from app.models.skills import Skill

# 技能清單：每個技能對應一個類別 ID
for skill_id in range(1, 22):  # 從 1 到 21（包含 21）
    record = LearningRecord(user_id=1, skill_id=skill_id, progress=0.3)
    db.add(record)

db.commit()
db.close()

print("已插入 21 筆測試資料")
