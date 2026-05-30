from typing import Annotated, Literal
from pydantic import BaseModel, Field, AfterValidator
from datetime import datetime


class UserBase(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=16)]
    email: str


class UserInput(UserBase):
    password: str


class UserOutput(UserBase):
    created: datetime
