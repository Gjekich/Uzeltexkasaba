from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.employee_service import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return EmployeeService.create(db, employee)


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return EmployeeService.get_all(db, search, page, size)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = EmployeeService.get(db, employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    updated = EmployeeService.update(db, employee_id, employee)

    if updated is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return updated


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted = EmployeeService.delete(db, employee_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        "message": "Employee deleted successfully"
    }