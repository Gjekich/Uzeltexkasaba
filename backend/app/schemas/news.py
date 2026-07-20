from datetime import datetime
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    title_ru: str | None = None
    title_en: str | None = None
    content: str
    content_ru: str | None = None
    content_en: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
