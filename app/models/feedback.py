from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.db.database import Base
from datetime import datetime, timezone

class Feedback(Base):
    """
    Database model for storing feedback or photo analysis results.
    """
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(String, unique=True, nullable=False)  # Unique identifier for the photo
    ai_score = Column(Integer, nullable=False)  # AI score for the photo
    content_analysis = Column(JSON, nullable=False)  # Textual analysis of the photo content
    techniques = Column(JSON, nullable=True)  # Types of techniques included
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
