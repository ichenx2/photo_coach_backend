from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer,nullable=False)
    #1.構圖技巧 2.光線運用 3.拍攝角度