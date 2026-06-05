from typing import Annotated, Literal
from pydantic import BaseModel, Field, AfterValidator
from datetime import datetime

from schemas import utils


# ============================================================
# MEDIA SCHEMAS
# ============================================================


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


class MediaUpdateRequest(MediaBase):
    pass


class MediaResponse(MediaBase):
    id: int
    created: datetime
    last_edited: datetime

    class Config:
        from_attributes = True
