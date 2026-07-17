from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.staff import StaffCreate, StaffResponse, StaffUpdate
from app.services.staff_service import StaffService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)


@router.post("/", response_model=StaffResponse)
def create_staff(
    staff_data: StaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StaffService.create(db, staff_data)


@router.get("/", response_model=list[StaffResponse])
def get_all_staff(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return StaffService.get_all(db, search, page, size)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = StaffService.get(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Xodim topilmadi")
    return staff


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    staff_data: StaffUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = StaffService.update(db, staff_id, staff_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Xodim topilmadi")
    return updated


@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = StaffService.delete(db, staff_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Xodim topilmadi")
    return {"message": "Xodim o'chirildi"}
