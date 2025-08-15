from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum

class TechniqueCategory(str, Enum):
    composition = "構圖技巧"
    lighting = "光線運用"
    angle = "拍攝角度"

class Technique(Base):
    __tablename__ = "techniques"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(SqlEnum(TechniqueCategory, native_enum=False), nullable=False)
    description = Column(Text, nullable=True)

    feedback_links = relationship("FeedbackTechniqueLink", back_populates="technique")