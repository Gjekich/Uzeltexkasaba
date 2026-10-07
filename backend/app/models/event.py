from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    category = Column(String(100), default="Seminar")
    category_ru = Column(String(100), nullable=True)
    category_en = Column(String(100), nullable=True)
    date_day = Column(String(20), nullable=False)
    date_month = Column(String(50), nullable=False)
    date_month_ru = Column(String(50), nullable=True)
    date_month_en = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    location_ru = Column(String(255), nullable=True)
    location_en = Column(String(255), nullable=True)
    time = Column(String(100), nullable=True)
    color_theme = Column(String(50), default="primary")
    created_at = Column(DateTime, default=datetime.utcnow)
