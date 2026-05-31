from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

from database.session import Base


# ============================================================
# MEDIA DB MODELS
# ============================================================


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    type = Column(String, nullable=False)
    review = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    created = Column(DateTime, nullable=False)
    last_edited = Column(DateTime, nullable=False)
