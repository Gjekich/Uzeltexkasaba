from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
