from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import ApplicationCreate


class ApplicationService:

    @staticmethod
    def create(db: Session, app_data: ApplicationCreate) -> Application:
        db_app = Application(**app_data.model_dump())
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def get_all(db: Session, status: str = None, page: int = 1, size: int = 50):
        query = db.query(Application)
        if status:
            query = query.filter(Application.status == status)
        return query.order_by(Application.created_at.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, app_id: int) -> Application | None:
        return db.query(Application).filter(Application.id == app_id).first()

    @staticmethod
    def update_status(db: Session, app_id: int, status: str) -> Application | None:
        db_app = db.query(Application).filter(Application.id == app_id).first()
        if not db_app:
            return None
        db_app.status = status
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def delete(db: Session, app_id: int) -> bool:
        db_app = db.query(Application).filter(Application.id == app_id).first()
        if not db_app:
            return False
        db.delete(db_app)
        db.commit()
        return True
