from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class FeedbackTechniqueLink(Base):
    __tablename__ = "feedback_techniques"

    id = Column(Integer, primary_key=True)
    feedback_id = Column(Integer, ForeignKey("feedbacks.id"))
    technique_id = Column(Integer, ForeignKey("techniques.id"))

    feedback = relationship("Feedback", back_populates="technique_links")
    technique = relationship("Technique", back_populates="feedback_links")