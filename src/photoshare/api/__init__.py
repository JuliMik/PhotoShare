from fastapi import APIRouter
# from src.photoshare.api.api_v1.demo_auth.demo_jwt_auth import router as demo_jwt_auth_router

from src.photoshare.api.api_v1.auth.auth import router as user_router

router = APIRouter()
# router.include_router(demo_jwt_auth_router)
router.include_router(user_router)
