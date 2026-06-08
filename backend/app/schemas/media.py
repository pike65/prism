from typing import Annotated, Literal
from pydantic import BaseModel, Field, AfterValidator
from datetime import datetime

from schemas import utils


class MediaBase(BaseModel):
    title: Annotated[
        str, Field(..., max_length=32), AfterValidator(utils.title_and_strip)
    ]
    genre: Annotated[
        str, Field(..., max_length=32), AfterValidator(utils.title_and_strip)
    ]
    rating: Annotated[float, Field(ge=0, le=10), AfterValidator(utils.round_rating)]
    type: Literal[
        "Movie",
        "Series",
        "Animated Film",
        "Animated Series",
        "Anime Film",
        "Anime Series",
    ] = "Movie"


class MediaCreateRequest(MediaBase):
    review: Annotated[str, Field(..., max_length=1000)]


class MediaUpdateRequest(BaseModel):
    title: Annotated[str, Field(max_length=32), AfterValidator(utils.title_and_strip)] | None = None
    genre: Annotated[str, Field(max_length=32), AfterValidator(utils.title_and_strip)] | None = None
    rating: Annotated[float, Field(ge=0, le=10), AfterValidator(utils.round_rating)] | None = None
    type: Literal[
        "Movie",
        "Series",
        "Animated Film",
        "Animated Series",
        "Anime Film",
        "Anime Series",
    ] | None = None
    review: Annotated[str, Field(max_length=1000)] | None = None


class MediaResponse(MediaBase):
    id: int
    review: str
    created: datetime
    last_edited: datetime

    class Config:
        from_attributes = True
