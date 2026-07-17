from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.legislation import LegislationCreate, LegislationResponse, LegislationUpdate
from app.services.legislation_service import LegislationService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/legislations",
    tags=["Legislations"]
)


@router.post("/", response_model=LegislationResponse)
def create_legislation(
    leg_data: LegislationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return LegislationService.create(db, leg_data)


@router.get("/", response_model=list[LegislationResponse])
def get_all_legislations(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return LegislationService.get_all(db, category, search, page, size)


@router.get("/{legislation_id}", response_model=LegislationResponse)
def get_legislation(legislation_id: int, db: Session = Depends(get_db)):
    leg = LegislationService.get(db, legislation_id)
    if not leg:
        raise HTTPException(status_code=404, detail="Qonunchilik hujjati topilmadi")
    return leg


@router.put("/{legislation_id}", response_model=LegislationResponse)
def update_legislation(
    legislation_id: int,
    leg_data: LegislationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = LegislationService.update(db, legislation_id, leg_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Qonunchilik hujjati topilmadi")
    return updated


@router.delete("/{legislation_id}")
def delete_legislation(
    legislation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = LegislationService.delete(db, legislation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Qonunchilik hujjati topilmadi")
    return {"message": "Qonunchilik hujjati muvaffaqiyatli o'chirildi"}
