from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Annotated

from database.session import get_db
from . import schemas, service


router = APIRouter(prefix="/api/user", tags=["user"])



