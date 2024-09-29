from typing import Optional, Type

from numpy import ndarray, float32
from sqlalchemy.orm import Session

from ..models.Photo import Photo


def create_photo(db: Session, file_id: str, embedding: ndarray[float32]) -> Photo:
    db_photo = Photo(file_id=file_id,
                     embedding=[element.item() for element in embedding])
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return db_photo


def get_photo_by_file_id(db: Session, file_id: str) -> Optional[Photo]:
    return db.query(Photo).filter(Photo.file_id == file_id).first()
