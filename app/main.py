from fastapi import FastAPI, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database.db import get_db, engine
import database.models as models
from schemas.schemas import MediaInput, MediaRead


models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Prism",
    description="Media Consumption Tracker",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"prism": "on"}


# 2. DATA ROUTE: Fetch all tracked watchables from the database
@app.get("/media", response_model=list[MediaRead])
def get_all_media(db_session: Session = Depends(get_db)):
    db_items = db_session.query(models.Media).all()
    
    # Map the comma-separated strings back into real Python sets for your MediaRead schema
    result = []
    for item in db_items:
        genres_set = {g.strip() for g in item.genres.split(",")} if item.genres else set()
        
        result.append(MediaRead(
            media_id=item.media_id,
            title=item.title,
            genre=item.genre,
            genres=genres_set,
            review=item.review,
            rating=item.rating,
            created_at=item.created_at,
            last_edited=item.last_edited
        ))
    return result

# 3. DATA ROUTE: Commit a new watchable entry to the database
@app.post("/media", response_model=MediaRead, status_code=status.HTTP_201_CREATED)
def create_media(media_in: MediaInput, db_session: Session = Depends(get_db)):
    # Flatten the Pydantic clean genres set into a single comma-separated string for SQLite
    genres_string = ", ".join(media_in.genres)
    
    # Build the physical model row mapper instance
    # Note: media_id, created_at, and last_edited generate automatically via models.py default configurations
    new_media_row = models.Media(
        title=media_in.title,
        genre=media_in.genre,
        genres=genres_string,
        review=media_in.review,
        rating=media_in.rating
    )

    # Stage, write, and refresh the connection state
    db_session.add(new_media_row)
    db_session.commit()
    db_session.refresh(new_media_row)
    
    # Construct and return data matching the shape of MediaRead
    return MediaRead(
        media_id=new_media_row.media_id,
        title=new_media_row.title,
        genre=new_media_row.genre,
        genres=media_in.genres, # Mirror original validated set back down
        review=new_media_row.review,
        rating=new_media_row.rating,
        created_at=new_media_row.created_at,
        last_edited=new_media_row.last_edited
    )