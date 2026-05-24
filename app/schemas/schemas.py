from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated
from datetime import datetime


def capitalize_each_word(v: str) -> str:
    return v.strip().title()


def round_rating(v: float) -> float:
    return round(v, 1)


TitleString = Annotated[str, AfterValidator(capitalize_each_word), Field(min_length=1, max_length=32)]
Rating = Annotated[float, AfterValidator(round_rating), Field(ge=1, le=10)]
ReviewText = Annotated[str, Field(max_length=1000)]


class MediaBase(BaseModel):
    title: TitleString
    genre: TitleString
    review: ReviewText | None = None
    rating: Rating


class MediaInput(MediaBase):
    pass


class MediaRead(MediaBase):
    created_at: datetime
    last_edited: datetime
