from datetime import datetime
from pydantic import BaseModel


class PrivilegeBase(BaseModel):
    title: str
    description: str
    icon: str | None = None
    content: str | None = None


class PrivilegeCreate(PrivilegeBase):
    pass


class PrivilegeUpdate(PrivilegeBase):
    pass


class PrivilegeResponse(PrivilegeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
