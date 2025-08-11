from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from app.db.database import Base

class LearningRecord(Base):
    __tablename__ = "learning_record"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    progress = Column(Float, default=0.0)

    __table_args__ = (UniqueConstraint('user_id', 'skill_id', name='_user_skill_uc'),)
    skill = relationship("Skill") 

