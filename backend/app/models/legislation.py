from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class Legislation(Base):
    __tablename__ = "legislations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=False)  # e.g., "Qonun", "Qaror", "Nizom"
    created_at = Column(DateTime, default=datetime.utcnow)
