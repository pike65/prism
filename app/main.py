from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uuid import UUID
from sqlalchemy.orm import Session

from database.db import get_db, engine
import database.models as models
from schemas.schemas import MediaInput, MediaRead

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prism", description="Media Consumption Tracker", version="1.0.0")


@app.get("/")
def root():
    return {"system": "is one"}


@app.get("/media", response_model=list[MediaRead])
def get_all_media(db_session: Session = Depends(get_db)):
    db_items = db_session.query(models.Media).all()

    result = []
    for item in db_items:
        genres_set = (
            {g.strip() for g in item.genres.split(",")} if item.genres else set()
        )

        result.append(
            MediaRead(
                media_id=UUID(item.media_id),
                title=item.title,
                genre=item.genre,
                genres=genres_set,
                review=item.review,
                rating=item.rating,
                created_at=item.created_at,
                last_edited=item.last_edited,
            )
        )
    return result


@app.get("/media/{media_id}", response_model=MediaRead)
def get_media(media_id: str, db_session: Session = Depends(get_db)):
    db_item = (
        db_session.query(models.Media).filter(models.Media.media_id == media_id).first()
    )

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media entry not found."
        )

    genres_set = (
        {g.strip() for g in db_item.genres.split(",")} if db_item.genres else set()
    )

    found_media = MediaRead(
        media_id=UUID(db_item.media_id),
        title=db_item.title,
        genre=db_item.genre,
        genres=genres_set,
        review=db_item.review,
        rating=db_item.rating,
        created_at=db_item.created_at,
        last_edited=db_item.last_edited,
    )

    return found_media


@app.post("/media", response_model=MediaRead, status_code=status.HTTP_201_CREATED)
def create_media(media_in: MediaInput, db_session: Session = Depends(get_db)):
    genres_string = ", ".join(media_in.genres)

    new_media_row = models.Media(
        title=media_in.title,
        genre=media_in.genre,
        genres=genres_string,
        review=media_in.review,
        rating=media_in.rating,
    )

    db_session.add(new_media_row)
    db_session.commit()
    db_session.refresh(new_media_row)

    return MediaRead(
        media_id=UUID(new_media_row.media_id),
        title=new_media_row.title,
        genre=new_media_row.genre,
        genres=media_in.genres,
        review=new_media_row.review,
        rating=new_media_row.rating,
        created_at=new_media_row.created_at,
        last_edited=new_media_row.last_edited,
    )
