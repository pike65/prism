import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime


class Base(DeclarativeBase):
    pass


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    media_id: Mapped[str] = mapped_column(
        String, default=lambda: str(uuid.uuid4()), unique=True, index=True
    )

    title: Mapped[str] = mapped_column(String, index=True)
    genre: Mapped[str] = mapped_column(String)

    genres: Mapped[str] = mapped_column(String)

    review: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    last_edited: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
