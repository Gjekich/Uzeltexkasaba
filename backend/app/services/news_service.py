from sqlalchemy.orm import Session

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate


class NewsService:

    @staticmethod
    def create(db: Session, news: NewsCreate) -> News:
        db_news = News(**news.model_dump())
        db.add(db_news)
        db.commit()
        db.refresh(db_news)
        return db_news

    @staticmethod
    def get_all(db: Session, search: str = None, page: int = 1, size: int = 20):
        query = db.query(News)
        if search:
            query = query.filter(News.title.ilike(f"%{search}%") | News.content.ilike(f"%{search}%"))
        return query.order_by(News.created_at.desc()).offset((page - 1) * size).limit(size).all()

    @staticmethod
    def get(db: Session, news_id: int) -> News | None:
        return db.query(News).filter(News.id == news_id).first()

    @staticmethod
    def update(db: Session, news_id: int, news: NewsUpdate) -> News | None:
        db_news = db.query(News).filter(News.id == news_id).first()
        if not db_news:
            return None
        for key, value in news.model_dump().items():
            setattr(db_news, key, value)
        db.commit()
        db.refresh(db_news)
        return db_news

    @staticmethod
    def delete(db: Session, news_id: int) -> bool:
        db_news = db.query(News).filter(News.id == news_id).first()
        if not db_news:
            return False
        db.delete(db_news)
        db.commit()
        return True
