from datetime import datetime
from pydantic import BaseModel


class LegislationBase(BaseModel):
    title: str
    title_ru: str | None = None
    title_en: str | None = None
    description: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    file_url: str | None = None
    category: str


class LegislationCreate(LegislationBase):
    pass


class LegislationUpdate(LegislationBase):
    pass


class LegislationResponse(LegislationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
