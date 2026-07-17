from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


class StaffService:

    @staticmethod
    def create(db: Session, staff_data: StaffCreate) -> Staff:
        db_staff = Staff(**staff_data.model_dump())
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        return db_staff

    @staticmethod
    def get_all(db: Session, search: str = None, page: int = 1, size: int = 100):
        query = db.query(Staff)
        if search:
            query = query.filter(
                Staff.full_name.ilike(f"%{search}%") | 
                Staff.position.ilike(f"%{search}%")
            )
        return query.order_by(Staff.full_name.asc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, staff_id: int) -> Staff | None:
        return db.query(Staff).filter(Staff.id == staff_id).first()

    @staticmethod
    def update(db: Session, staff_id: int, staff_data: StaffUpdate) -> Staff | None:
        db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not db_staff:
            return None
        for key, value in staff_data.model_dump().items():
            setattr(db_staff, key, value)
        db.commit()
        db.refresh(db_staff)
        return db_staff

    @staticmethod
    def delete(db: Session, staff_id: int) -> bool:
        db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not db_staff:
            return False
        db.delete(db_staff)
        db.commit()
        return True
