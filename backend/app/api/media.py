from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from schemas import media as media_schemas
from services import media as media_service


router = APIRouter(prefix="/media", tags=["media"])


# ============================================================
# MEDIA ROUTES
# ============================================================


@router.post("/", status_code=201, response_model=media_schemas.MediaResponse)
def create_item(item: media_schemas.MediaCreateRequest, db: Session = Depends(get_db)):
    return media_service.add_new_media(db=db, item_data=item)


@router.get("/", response_model=List[media_schemas.MediaResponse])
def get_all_items(db: Session = Depends(get_db)):
    return media_service.get_all_media(db=db)
