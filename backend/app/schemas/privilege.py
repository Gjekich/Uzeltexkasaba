from datetime import datetime
from pydantic import BaseModel


class PrivilegeBase(BaseModel):
    title: str
    title_ru: str | None = None
    title_en: str | None = None
    description: str
    description_ru: str | None = None
    description_en: str | None = None
    icon: str | None = None
    content: str | None = None
    content_ru: str | None = None
    content_en: str | None = None


class PrivilegeCreate(PrivilegeBase):
    pass


class PrivilegeUpdate(PrivilegeBase):
    pass


class PrivilegeResponse(PrivilegeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
