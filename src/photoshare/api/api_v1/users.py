from fastapi import APIRouter

# Main router initialization for user profile and management endpoints
router = APIRouter(tags=["Users"])


# ==========================================
# User Management Routes
# ==========================================

# TODO: Activate endpoints below once dependencies and DTO schemas are integrated
#
# @router.get("/me", response_model=UserDto)
# async def get_me(user: user_dependency):
#     return user
