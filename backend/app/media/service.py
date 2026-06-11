from sqlalchemy.orm import Session

from .models import Media
from . import schemas


def get_all_media(db: Session):
    return db.query(Media).all()


def get_media_by_id(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()


def add_new_media(db: Session, media_in: schemas.MediaCreateRequest):
    db_media = Media(**media_in.model_dump())

    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def update_media(db: Session, media_id: int, media_in: schemas.MediaUpdateRequest):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        return None

    update_data = media_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_media, key, value)

    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def delete_media(db: Session, media_id: int):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        return False

    db.delete(db_media)
    db.commit()
    return True