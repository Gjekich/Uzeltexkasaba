from typing import Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):

    full_name: str

    position: Optional[str] = None

    work_experience: Optional[str] = None

    union_experience: Optional[str] = None

    phone: Optional[str] = None

    marital_status: Optional[str] = None

    children_count: Optional[int] = 0

    children_under_14: Optional[int] = 0

    disability: Optional[bool] = False

    disability_group: Optional[str] = None

    disability_person: Optional[str] = None

    pensioner: Optional[bool] = False

    privileged: Optional[bool] = False

    passport: Optional[str] = None

    chronic_disease: Optional[str] = None

    objective: Optional[str] = None


class EmployeeResponse(EmployeeCreate):

    id: int

    class Config:
        from_attributes = True