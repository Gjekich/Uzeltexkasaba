from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.news import NewsCreate, NewsResponse, NewsUpdate
from app.services.news_service import NewsService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.post("/", response_model=NewsResponse)
def create_news(
    news_data: NewsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NewsService.create(db, news_data)


@router.get("/", response_model=list[NewsResponse])
def get_all_news(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return NewsService.get_all(db, search, page, size)


@router.get("/{news_id}", response_model=NewsResponse)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news = NewsService.get(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="Yangilik topilmadi")
    return news


@router.put("/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: int,
    news_data: NewsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = NewsService.update(db, news_id, news_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Yangilik topilmadi")
    return updated


@router.delete("/{news_id}")
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = NewsService.delete(db, news_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Yangilik topilmadi")
    return {"message": "Yangilik muvaffaqiyatli o'chirildi"}
