from datetime import datetime
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: str
    image_url: str | None = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
