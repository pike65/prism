# models.py
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime

# Universal mapping Base
class Base(DeclarativeBase): pass

class Media(Base):
    __tablename__ = "media"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Generate a string-based UUID automatically on creation for SQLite safety
    media_id: Mapped[str] = mapped_column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    title: Mapped[str] = mapped_column(String, index=True)
    genre: Mapped[str] = mapped_column(String)
    
    # Stored as a raw text string ("Action, Anime, Mecha")
    genres: Mapped[str] = mapped_column(String) 
    
    review: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float)
    
    # Automatically apply timestamps on creation/modification
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_edited: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))