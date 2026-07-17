import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.settings import settings
from app.db.database import Base, engine

# Register models in SQLAlchemy metadata
from app.models.user import User
from app.models.news import News
from app.models.privilege import Privilege
from app.models.legislation import Legislation
from app.models.application import Application

# API Routers
from app.api.auth import router as auth_router
from app.api.news import router as news_router
from app.api.privilege import router as privilege_router
from app.api.legislation import router as legislation_router
from app.api.application import router as application_router
from app.api.upload import router as upload_router

# Create DB tables and populate demo data
Base.metadata.create_all(bind=engine)
from app.db.init_db import populate_db
populate_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers under /api prefix
app.include_router(auth_router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(privilege_router, prefix="/api")
app.include_router(legislation_router, prefix="/api")
app.include_router(application_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

# Static files for uploads (images, PDFs)
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount frontend at root. We ensure this is mounted AFTER API routes.
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")