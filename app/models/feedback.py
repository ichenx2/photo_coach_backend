from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey
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
    photo_id = Column(Integer, ForeignKey("photos.id"))  # 一對一關聯到 Photo
    content_analysis = Column(JSON, nullable=False)         # Textual analysis of the photo content
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="feedbacks")
    photo = relationship("Photo", back_populates="feedback", uselist=False)  # 一對一關聯