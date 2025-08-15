from sqlalchemy.orm import Session
from app.schemas.photo_schema import PhotoIn
from app.models.photo import Photo


def create_photo(db: Session, photo_in: PhotoIn):
    photo = Photo(**photo_in.model_dump())
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo