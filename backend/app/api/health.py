from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
def health_check():
    return {
        "app": settings.APP_NAME,
        "status": "running"
    }