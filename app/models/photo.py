from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subtask_id = Column(Integer, ForeignKey("subtasks.id"))
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="photos")
    subtask = relationship("SubTask", back_populates="photo")
    feedback = relationship("Feedback", back_populates="photo", uselist=False, cascade="all, delete-orphan")  # 一對一關聯