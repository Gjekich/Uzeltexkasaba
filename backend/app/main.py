from fastapi import FastAPI

from app.config.settings import settings
from app.db.database import Base, engine

# Modellar
from app.models.employee import Employee

# API
from app.api.employee import router as employee_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.include_router(employee_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "API ishlayapti"
    }