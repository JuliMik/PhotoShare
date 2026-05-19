from fastapi import APIRouter
from src.photoshare.api.api_v1.auth.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)
