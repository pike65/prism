from typing import Annotated, Literal
from pydantic import BaseModel, Field, AfterValidator
from datetime import datetime

from utils import *


class MediaBase(BaseModel):
    title: Annotated[str, Field(...), AfterValidator(title_and_strip)]
    genre: Annotated[str, Field(...), AfterValidator(title_and_strip)]
    review: Annotated[str | None, Field(max_length=1000), AfterValidator(clean_optional_text)] = None
    rating: Annotated[float, Field(ge=0, le=10), AfterValidator(round_rating)]

    type: Literal[
        "Movie",
        "Series",
        "Animated Film",
        "Animated Series",
        "Anime Film",
        "Anime Series",
    ] = "Movie"


class MediaInput(MediaBase):
    pass


class MediaOutput(MediaBase):
    created: datetime
    last_edited: datetime
