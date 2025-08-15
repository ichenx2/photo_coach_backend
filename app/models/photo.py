from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subtask_id = Column(Integer, ForeignKey("subtasks.id"))  # 任務關聯
    file_path = Column(String, nullable=False)
    topic = Column(String, nullable=True)  # 可保留作搜尋/標記用途
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subtask = relationship("SubTask", back_populates="photos")  # 反向連結