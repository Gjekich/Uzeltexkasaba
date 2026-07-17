from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdateStatus
from app.services.application_service import ApplicationService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/", response_model=ApplicationResponse)
def create_application(
    app_data: ApplicationCreate,
    db: Session = Depends(get_db)
):
    return ApplicationService.create(db, app_data)


@router.get("/", response_model=list[ApplicationResponse])
def get_all_applications(
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ApplicationService.get_all(db, status, page, size)


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app = ApplicationService.get(db, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Murojaat topilmadi")
    return app


@router.patch("/{app_id}/status", response_model=ApplicationResponse)
def update_application_status(
    app_id: int,
    status_data: ApplicationUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = ApplicationService.update_status(db, app_id, status_data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Murojaat topilmadi")
    return updated


@router.delete("/{app_id}")
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = ApplicationService.delete(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Murojaat topilmadi")
    return {"message": "Murojaat muvaffaqiyatli o'chirildi"}
