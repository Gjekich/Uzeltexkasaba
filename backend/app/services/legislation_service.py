from sqlalchemy.orm import Session

from app.models.legislation import Legislation
from app.schemas.legislation import LegislationCreate, LegislationUpdate


class LegislationService:

    @staticmethod
    def create(db: Session, legislation: LegislationCreate) -> Legislation:
        db_leg = Legislation(**legislation.model_dump())
        db.add(db_leg)
        db.commit()
        db.refresh(db_leg)
        return db_leg

    @staticmethod
    def get_all(db: Session, category: str = None, search: str = None, page: int = 1, size: int = 50):
        query = db.query(Legislation)
        if category:
            query = query.filter(Legislation.category == category)
        if search:
            query = query.filter(Legislation.title.ilike(f"%{search}%") | Legislation.description.ilike(f"%{search}%"))
        return query.order_by(Legislation.created_at.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, legislation_id: int) -> Legislation | None:
        return db.query(Legislation).filter(Legislation.id == legislation_id).first()

    @staticmethod
    def update(db: Session, legislation_id: int, legislation: LegislationUpdate) -> Legislation | None:
        db_leg = db.query(Legislation).filter(Legislation.id == legislation_id).first()
        if not db_leg:
            return None
        for key, value in legislation.model_dump().items():
            setattr(db_leg, key, value)
        db.commit()
        db.refresh(db_leg)
        return db_leg

    @staticmethod
    def delete(db: Session, legislation_id: int) -> bool:
        db_leg = db.query(Legislation).filter(Legislation.id == legislation_id).first()
        if not db_leg:
            return False
        db.delete(db_leg)
        db.commit()
        return True
