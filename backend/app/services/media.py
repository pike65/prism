from datetime import datetime, timezone
from sqlalchemy.orm import Session

from database.models.media import Media
from schemas import media as media_schemas


# ============================================================
# MEDIA SERVICES
# ============================================================


def add_new_media(db: Session, item_data: media_schemas.MediaInput):
    current_time = datetime.now(timezone.utc)

    db_item = Media(
        title=item_data.title,
        genre=item_data.genre,
        type=item_data.type,
        review=item_data.review,
        rating=item_data.rating,
        created=current_time,
        last_edited=current_time,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_media(db: Session):
    return db.query(Media).all()
