from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered data analyst using natural language and SQL",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "status": "running"
    }