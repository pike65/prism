from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from database.session import get_db
from . import schemas, service


router = APIRouter(prefix="/api/media", tags=["media"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.MediaResponse
)
def create_media(media_in: schemas.MediaCreateRequest, db: Session = Depends(get_db)):
    return service.add_new_media(db=db, media_in=media_in)


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.MediaResponse]
)
def get_all_media(db: Session = Depends(get_db)):
    return service.get_all_media(db=db)


@router.get(
    "/{media_id}", status_code=status.HTTP_200_OK, response_model=schemas.MediaResponse
)
def get_media(
    media_id: Annotated[int, Path(..., ge=1, description="The ID of the media item")],
    db: Session = Depends(get_db),
):
    db_media = service.get_media_by_id(db=db, media_id=media_id)
    if not db_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
        )
    return db_media


@router.patch(
    "/{media_id}", status_code=status.HTTP_200_OK, response_model=schemas.MediaResponse
)
def update_media(
    media_id: Annotated[int, Path(..., ge=1)],
    media_in: schemas.MediaUpdateRequest,
    db: Session = Depends(get_db),
):
    updated_media = service.update_media(db=db, media_id=media_id, media_in=media_in)
    if not updated_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
        )
    return updated_media


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
    media_id: Annotated[int, Path(..., ge=1)], db: Session = Depends(get_db)
):
    success = service.delete_media(db=db, media_id=media_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found"
        )
    return None