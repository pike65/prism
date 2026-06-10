from contextlib import contextmanager
from sqlalchemy.orm import Session

from .models import Media
from . import schemas


@contextmanager
def transaction_scope(db: Session):
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_all_media(db: Session):
    return db.query(Media).all()


def add_new_media(db: Session, item_data: schemas.MediaCreateRequest):
    db_item = Media(**item_data.model_dump())

    with transaction_scope(db):
        db.add(db_item)

    db.refresh(db_item)
    return db_item


def update_media(db: Session, item_id: int, item_data: schemas.MediaUpdateRequest):
    db_item = db.query(Media).filter(Media.id == item_id).first()
    if not db_item:
        return None

    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    with transaction_scope(db):
        db.add(db_item)

    db.refresh(db_item)
    return db_item


def delete_media(db: Session, item_id: int):
    db_item = db.query(Media).filter(Media.id == item_id).first()
    if not db_item:
        return False

    with transaction_scope(db):
        db.delete(db_item)

    return True
