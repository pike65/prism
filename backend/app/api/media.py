from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import Field
from typing import List, Annotated

from database.session import get_db
from schemas import media as media_schemas
from services import media as media_service


router = APIRouter(prefix="/api/media", tags=["media"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=media_schemas.MediaResponse
)
def create_item(item: media_schemas.MediaCreateRequest, db: Session = Depends(get_db)):
    return media_service.add_new_media(db=db, item_data=item)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[media_schemas.MediaResponse],
)
def get_all_items(db: Session = Depends(get_db)):
    return media_service.get_all_media(db=db)


@router.patch(
    "/{media_id}",
    status_code=status.HTTP_200_OK,
    response_model=media_schemas.MediaResponse,
)
def update_item(
    media_id: Annotated[int, Field(..., ge=1)],
    item: media_schemas.MediaUpdateRequest,
    db: Session = Depends(get_db),
):
    updated_media = media_service.update_media(db=db, item_id=media_id, item_data=item)
    if not updated_media:
        raise HTTPException(status_code=404, detail="Media not found")
    return updated_media


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    media_id: Annotated[int, Field(..., ge=1)], db: Session = Depends(get_db)
):
    success = media_service.delete_media(db=db, item_id=media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media iem not found")
    return None
