from datetime import datetime
from sqlalchemy import String, Float, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database.session import Base


# ============================================================
# MEDIA DB MODELS
# ============================================================


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    genre: Mapped[str] = mapped_column(String(32), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Movie")
    review: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    last_edited: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    __table_args__ = (
        Index("ix_media_title_genre", "title", "genre"),
    )