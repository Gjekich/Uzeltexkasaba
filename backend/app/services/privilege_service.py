from sqlalchemy.orm import Session

from app.models.privilege import Privilege
from app.schemas.privilege import PrivilegeCreate, PrivilegeUpdate


class PrivilegeService:

    @staticmethod
    def create(db: Session, privilege: PrivilegeCreate) -> Privilege:
        db_privilege = Privilege(**privilege.model_dump())
        db.add(db_privilege)
        db.commit()
        db.refresh(db_privilege)
        return db_privilege

    @staticmethod
    def get_all(db: Session, search: str = None, page: int = 1, size: int = 50):
        query = db.query(Privilege)
        if search:
            query = query.filter(Privilege.title.ilike(f"%{search}%") | Privilege.description.ilike(f"%{search}%"))
        return query.order_by(Privilege.created_at.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, privilege_id: int) -> Privilege | None:
        return db.query(Privilege).filter(Privilege.id == privilege_id).first()

    @staticmethod
    def update(db: Session, privilege_id: int, privilege: PrivilegeUpdate) -> Privilege | None:
        db_privilege = db.query(Privilege).filter(Privilege.id == privilege_id).first()
        if not db_privilege:
            return None
        for key, value in privilege.model_dump().items():
            setattr(db_privilege, key, value)
        db.commit()
        db.refresh(db_privilege)
        return db_privilege

    @staticmethod
    def delete(db: Session, privilege_id: int) -> bool:
        db_privilege = db.query(Privilege).filter(Privilege.id == privilege_id).first()
        if not db_privilege:
            return False
        db.delete(db_privilege)
        db.commit()
        return True
