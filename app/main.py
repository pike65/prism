from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uuid import UUID
from sqlalchemy.orm import Session

from database.db import get_db, engine
import database.models as models
from schemas.schemas import MediaInput, MediaRead

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prism", description="Media Consumption Tracker", version="0.1.0")


@app.get("/")
def root():
    return FileResponse("app/static/dashboard.html")


@app.get("/media", response_model=list[MediaRead])
def get_all_media(db_session: Session = Depends(get_db)):
    db_items = db_session.query(models.Media).all()

    result = []
    for item in db_items:
        result.append(
            MediaRead(
                title=item.title,
                genre=item.genre,
                review=item.review,
                rating=item.rating,
                created_at=item.created_at,
                last_edited=item.last_edited,
            )
        )
    return result


@app.post("/media", response_model=MediaRead, status_code=status.HTTP_201_CREATED)
def create_media(media_in: MediaInput, db_session: Session = Depends(get_db)):
    new_media_row = models.Media(
        title=media_in.title,
        genre=media_in.genre,
        review=media_in.review,
        rating=media_in.rating,
    )

    db_session.add(new_media_row)
    db_session.commit()
    db_session.refresh(new_media_row)

    return MediaRead(
        title=new_media_row.title,
        genre=new_media_row.genre,
        review=new_media_row.review,
        rating=new_media_row.rating,
        created_at=new_media_row.created_at,
        last_edited=new_media_row.last_edited,
    )
