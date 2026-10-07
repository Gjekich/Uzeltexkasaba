from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    @staticmethod
    def get_all(db: Session, search: str | None = None, page: int = 1, size: int = 50):
        query = db.query(Event)
        if search:
            query = query.filter(Event.title.ilike(f"%{search}%"))
        return query.order_by(Event.id.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, event_id: int):
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def create(db: Session, event_data: EventCreate):
        event = Event(**event_data.model_dump())
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def update(db: Session, event_id: int, event_data: EventUpdate):
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        for key, value in event_data.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def delete(db: Session, event_id: int):
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return False
        db.delete(event)
        db.commit()
        return True
