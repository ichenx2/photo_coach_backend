from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, timezone

class Feedback(Base):
    """
    Database model for storing feedback or photo analysis results.
    """
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # 和使用者關聯
    photo_id = Column(String, unique=True, nullable=False)  # Unique identifier for the photo
    content_analysis = Column(JSON, nullable=False)         # Textual analysis of the photo content
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="feedbacks")