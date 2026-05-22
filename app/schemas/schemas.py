from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated, Literal
from datetime import datetime, date
from uuid import UUID


def capitalize_each_word(v: str) -> str:
    """Strip whitespace and capitalize the start of every word."""
    return v.strip().title()


def sanitize_set_elements(v: set[str]) -> set[str]:
    """Loop through a set, stripping and capitalizing each string item."""
    return {capitalize_each_word(item) for item in v}

def round_rating(v: float) -> float:
    """Round up given float up to 1 digit after point."""
    return round(v, 1)


TitleString = Annotated[str, AfterValidator(capitalize_each_word)]
TitleSet = Annotated[set[str], AfterValidator(sanitize_set_elements)]
Rating = Annotated[float, AfterValidator(round_rating)]
Review = Annotated[str, Field(..., max_length=3000)]


class MediaBase(BaseModel):
    title: TitleString
    genre: TitleString
    genres: TitleSet
    review: Review | None = None
    rating: Rating


class MediaInput(MediaBase):
    pass


class MediaRead(MediaBase):
    created_at: datetime
    last_edited: datetime
    media_id: UUID

