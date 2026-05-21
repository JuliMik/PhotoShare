import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper

from src.photoshare.api.router import router as main_router


# ==========================================
# Application Lifecycle Management (Lifespan)
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles system startup and shutdown event triggers.
    Ensures critical external resources and network connection pools 
    are gracefully cleaned up before application termination.
    """
    # Startup tasks logic executes here before accepting client traffic
    yield
    # Shutdown tasks logic executes here upon receiving termination signals
    await db_helper.dispose()


# ==========================================
# FastAPI Application Initialization
# ==========================================

main_app = FastAPI(lifespan=lifespan)

# Register top-level versioned API gateways with dynamic prefixing
main_app.include_router(
    main_router,
    prefix=settings.api.prefix,
)


# ==========================================
# ASGI Server Local Execution Wrapper
# ==========================================

if __name__ == "__main__":
    # Boots up the local uvicorn development environment matching app profile specifications
    uvicorn.run(
        "main:main_app",
        port=settings.run.port,
        host=settings.run.host,
        reload=True,
    )