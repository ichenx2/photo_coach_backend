from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate

def create_feedback(db: Session, feedback_in: FeedbackCreate):
    feedback = Feedback(**feedback_in.model_dump(), user_id=user_id)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

def get_feedback(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def delete_feedback(db: Session, feedback_id: int):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        return None
    db.delete(feedback)
    db.commit()
    return feedback