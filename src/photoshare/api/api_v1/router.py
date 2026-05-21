from fastapi import APIRouter
from src.photoshare.api.api_v1.auth.auth import router as auth_router

# Core router initialization for API Version 1
router = APIRouter()


# ==========================================
# API v1 Router Composition
# ==========================================

# Include sub-routers to structure v1 endpoints
router.include_router(auth_router)
