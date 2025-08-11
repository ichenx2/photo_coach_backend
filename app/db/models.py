# 定義SQLAlchemy資料表
from db.database import SessionLocal
from models.learning_progress import LearningProgress

db = SessionLocal()
progresses = db.query(LearningProgress).all()

for p in progresses:
    print(p.topic, p.progress)
db.close()
