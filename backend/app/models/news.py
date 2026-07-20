from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    content_ru = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
