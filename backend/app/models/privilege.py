from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class Privilege(Base):
    __tablename__ = "privileges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    content = Column(Text, nullable=True)
    content_ru = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
