from datetime import datetime
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    full_name: str
    phone: str
    message: str


class ApplicationUpdateStatus(BaseModel):
    status: str


class ApplicationResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
