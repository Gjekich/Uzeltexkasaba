from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="Pending")  # e.g., Pending, In Progress, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)
