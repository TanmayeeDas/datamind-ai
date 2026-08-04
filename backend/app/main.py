from fastapi import FastAPI
from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered data analyst using natural language and SQL",
    version="1.0.0",
)

app.include_router(health_router)