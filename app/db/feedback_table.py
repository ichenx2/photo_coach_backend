from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.db.database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    image_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    captured_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 1:1 
    analysis = relationship(
        "PhotoAnalysis",
        back_populates="photo",
        uselist=False,
        cascade="all, delete-orphan"  # 刪照片時連動刪分析
    )

class PhotoAnalysis(Base):
    __tablename__ = "photo_analysis"

    # PK 同時是 FK：與 Photo 1:1
    photo_id = Column(String, ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True)
    observation_json = Column(Text, nullable=False)   # JSON 字串：list[str]
    techniques_json  = Column(Text, nullable=False)   # JSON 字串：dict[str, list[str]]
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    photo = relationship("Photo", back_populates="analysis")
