from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class FeedbackMemory(Base):
    """
    專門給 FeedbackAgent 使用的「記憶」表，
    存放使用者過去的建議、常見錯誤等摘要。
    """
    __tablename__ = "feedback_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # 紀錄是哪個用戶的記憶
    summary = Column(String, nullable=False)           # LLM 給的建議/錯誤摘要
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="feedback_memories")
