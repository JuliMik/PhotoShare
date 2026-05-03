from fastapi import APIRouter
from src.photoshare.api.api_v1.demo_auth.demo_jwt_auth import router as demo_jwt_auth_router

router = APIRouter()
router.include_router(demo_jwt_auth_router)
