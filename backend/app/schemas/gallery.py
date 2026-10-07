from datetime import datetime
from pydantic import BaseModel


class GalleryBase(BaseModel):
    title: str
    title_ru: str | None = None
    title_en: str | None = None
    image_url: str
    category: str = "tadbirlar"


class GalleryCreate(GalleryBase):
    pass


class GalleryUpdate(BaseModel):
    title: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    image_url: str | None = None
    category: str | None = None


class GalleryResponse(GalleryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
