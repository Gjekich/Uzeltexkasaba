from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=False)
    category = Column(String(100), default="tadbirlar")
    created_at = Column(DateTime, default=datetime.utcnow)
