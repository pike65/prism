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
    review: Annotated[
        str | None,
        Field(None, max_length=1000),
        AfterValidator(utils.clean_optional_text),
    ] = None
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
    pass


class MediaUpdateRequest(MediaBase):
    pass


class MediaResponse(MediaBase):
    id: int
    created: datetime

    class Config:
        from_attributes = True
