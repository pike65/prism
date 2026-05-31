from sqlalchemy.orm import Session

from database.models.media import Media
from schemas import media as media_schemas


# ============================================================
# MEDIA SERVICES
# ============================================================


def add_new_media(db: Session, item_data: media_schemas.MediaInput):
    db_item = Media(**item_data.model_dump())

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_media(db: Session):
    return db.query(Media).all()


def update_media(
    db: Session, item_id: int, item_data: media_schemas.MediaUpdateRequest
):
    db_item = db.query(Media).filter(Media.id == item_id).first()
    if not db_item:
        return None

    update_data = item_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_media(db: Session, item_id: int):
    db_item = db.query(Media).filter(Media.id == item_id).first()
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True