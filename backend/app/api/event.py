from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import EventService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("/", response_model=EventResponse)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return EventService.create(db, event_data)


@router.get("/", response_model=list[EventResponse])
def get_all_events(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return EventService.get_all(db, search, page, size)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = EventService.get(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Tadbir topilmadi")
    return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = EventService.update(db, event_id, event_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tadbir topilmadi")
    return updated


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = EventService.delete(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tadbir topilmadi")
    return {"message": "Tadbir muvaffaqiyatli o'chirildi"}
