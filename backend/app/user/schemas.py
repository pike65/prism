from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated, Literal


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    pass
