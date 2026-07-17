from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.privilege import PrivilegeCreate, PrivilegeResponse, PrivilegeUpdate
from app.services.privilege_service import PrivilegeService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/privileges",
    tags=["Privileges"]
)


@router.post("/", response_model=PrivilegeResponse)
def create_privilege(
    privilege_data: PrivilegeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PrivilegeService.create(db, privilege_data)


@router.get("/", response_model=list[PrivilegeResponse])
def get_all_privileges(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return PrivilegeService.get_all(db, search, page, size)


@router.get("/{privilege_id}", response_model=PrivilegeResponse)
def get_privilege(privilege_id: int, db: Session = Depends(get_db)):
    privilege = PrivilegeService.get(db, privilege_id)
    if not privilege:
        raise HTTPException(status_code=404, detail="Imtiyoz topilmadi")
    return privilege


@router.put("/{privilege_id}", response_model=PrivilegeResponse)
def update_privilege(
    privilege_id: int,
    privilege_data: PrivilegeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = PrivilegeService.update(db, privilege_id, privilege_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Imtiyoz topilmadi")
    return updated


@router.delete("/{privilege_id}")
def delete_privilege(
    privilege_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = PrivilegeService.delete(db, privilege_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Imtiyoz topilmadi")
    return {"message": "Imtiyoz muvaffaqiyatli o'chirildi"}
