from fastapi import APIRouter
from src.photoshare.api.api_v1.router import router as api_v1_router
from src.photoshare.core.config import settings

# Top-level API entry point router
router = APIRouter()


# ==========================================
# Global API Versioning & Routing
# ==========================================

# Dynamically include versioned sub-routers using system configuration path prefixes
router.include_router(api_v1_router, prefix=settings.api.v1.prefix)
