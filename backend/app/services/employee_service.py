from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


class EmployeeService:

    @staticmethod
    def create(db: Session, employee: EmployeeCreate):

        new_employee = Employee(**employee.model_dump())

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee

    @staticmethod
    def get_all(
        db: Session,
        search: str = None,
        page: int = 1,
        size: int = 20
    ):

        query = db.query(Employee)

        if search:

            query = query.filter(

                or_(

                    Employee.full_name.ilike(f"%{search}%"),

                    Employee.position.ilike(f"%{search}%")

                )

            )

        return (

            query

            .offset((page - 1) * size)

            .limit(size)

            .all()

        )

    @staticmethod
    def get(db: Session, employee_id: int):

        return (

            db.query(Employee)

            .filter(Employee.id == employee_id)

            .first()

        )

    @staticmethod
    def update(
        db: Session,
        employee_id: int,
        employee: EmployeeCreate
    ):

        db_employee = (

            db.query(Employee)

            .filter(Employee.id == employee_id)

            .first()

        )

        if not db_employee:

            return None

        for key, value in employee.model_dump().items():

            setattr(db_employee, key, value)

        db.commit()

        db.refresh(db_employee)

        return db_employee

    @staticmethod
    def delete(
        db: Session,
        employee_id: int
    ):

        db_employee = (

            db.query(Employee)

            .filter(Employee.id == employee_id)

            .first()

        )

        if not db_employee:

            return False

        db.delete(db_employee)

        db.commit()

        return True