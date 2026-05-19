from fastapi import APIRouter
from src.photoshare.api.api_v1.router import router as api_v1_router
from src.photoshare.core.config import settings

router = APIRouter()

router.include_router(api_v1_router, prefix=settings.api.v1.prefix)
