from sqlalchemy.orm import Session
from app.models.gallery import GalleryItem
from app.schemas.gallery import GalleryCreate, GalleryUpdate


class GalleryService:
    @staticmethod
    def get_all(db: Session, category: str | None = None, page: int = 1, size: int = 100):
        query = db.query(GalleryItem)
        if category and category != 'all':
            query = query.filter(GalleryItem.category == category)
        return query.order_by(GalleryItem.id.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, item_id: int):
        return db.query(GalleryItem).filter(GalleryItem.id == item_id).first()

    @staticmethod
    def create(db: Session, data: GalleryCreate):
        item = GalleryItem(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update(db: Session, item_id: int, data: GalleryUpdate):
        item = db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
        if not item:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item_id: int):
        item = db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
        if not item:
            return False
        db.delete(item)
        db.commit()
        return True
