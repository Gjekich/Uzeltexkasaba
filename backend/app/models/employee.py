from sqlalchemy import Boolean, Column, Integer, String, Text

from app.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    position = Column(String(255))

    work_experience = Column(String(100))

    union_experience = Column(String(100))

    phone = Column(String(30))

    marital_status = Column(String(100))

    children_count = Column(Integer, default=0)

    children_under_14 = Column(Integer, default=0)

    disability = Column(Boolean, default=False)

    disability_group = Column(String(50))

    disability_person = Column(String(100))

    pensioner = Column(Boolean, default=False)

    privileged = Column(Boolean, default=False)

    passport = Column(String(20))

    chronic_disease = Column(String(255))

    objective = Column(Text)