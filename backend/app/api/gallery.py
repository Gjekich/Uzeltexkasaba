from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.gallery import GalleryCreate, GalleryResponse, GalleryUpdate
from app.services.gallery_service import GalleryService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/gallery",
    tags=["Gallery"]
)


@router.post("/", response_model=GalleryResponse)
def create_gallery_item(
    item_data: GalleryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return GalleryService.create(db, item_data)


@router.get("/", response_model=list[GalleryResponse])
def get_all_gallery_items(
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return GalleryService.get_all(db, category, page, size)


@router.get("/{item_id}", response_model=GalleryResponse)
def get_gallery_item(item_id: int, db: Session = Depends(get_db)):
    item = GalleryService.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Rasm topilmadi")
    return item


@router.put("/{item_id}", response_model=GalleryResponse)
def update_gallery_item(
    item_id: int,
    item_data: GalleryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = GalleryService.update(db, item_id, item_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Rasm topilmadi")
    return updated


@router.delete("/{item_id}")
def delete_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = GalleryService.delete(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rasm topilmadi")
    return {"message": "Muvaffaqiyatli o'chirildi"}
