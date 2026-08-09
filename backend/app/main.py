from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.database import router as database_router
from app.api.query import router as query_router

from app.core.config import settings
from app.core.logging_config import logger


logger.info("Starting DataMind AI Backend...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Data Analyst",
    version="1.0.0",
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(database_router)
app.include_router(query_router)