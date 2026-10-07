from datetime import datetime
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    title_ru: str | None = None
    title_en: str | None = None
    description: str
    description_ru: str | None = None
    description_en: str | None = None
    category: str = "Seminar"
    category_ru: str | None = None
    category_en: str | None = None
    date_day: str
    date_month: str
    date_month_ru: str | None = None
    date_month_en: str | None = None
    location: str | None = None
    location_ru: str | None = None
    location_en: str | None = None
    time: str | None = None
    color_theme: str = "primary"


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    description: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    category: str | None = None
    category_ru: str | None = None
    category_en: str | None = None
    date_day: str | None = None
    date_month: str | None = None
    date_month_ru: str | None = None
    date_month_en: str | None = None
    location: str | None = None
    location_ru: str | None = None
    location_en: str | None = None
    time: str | None = None
    color_theme: str | None = None


class EventResponse(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
