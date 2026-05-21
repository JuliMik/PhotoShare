from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import (
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    validate_auth_user_login,
    http_bearer,
)
from auth.service import create_access_token, create_refresh_token
from src.photoshare.schemas.user import UserResponse, UserCreate
from src.photoshare.schemas.token import TokenInfo
from src.photoshare.core.models.db_helper import db_helper
from src.photoshare.api.api_v1.crud.users import create_user
from src.photoshare.core.models import User

# Router configuration for authentication endpoints
router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


# ==========================================
# User Registration & Authentication
# ==========================================


# Endpoint to register a new user in the system
@router.post(
    "/sign_up/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Registers a new user.
    Checks for username or email conflicts before calling the CRUD creation layer.
    """
    query = select(User).where(
        (User.email == user_in.email) | (User.username == user_in.username)
    )
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists",
        )
    user = await create_user(session=session, user_in=user_in)
    return user


# Endpoint to authenticate a user and issue access/refresh tokens
@router.post("/login/", response_model=TokenInfo)
async def login(
    user: User = Depends(validate_auth_user_login),
):
    """
    Authenticates user credentials via Form data dependency
    and returns a fresh pair of Access and Refresh tokens.
    """
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# ==========================================
# Token Lifecycle & Identity
# ==========================================


# Endpoint to reissue an access token using a valid refresh token
@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_token(user: User = Depends(get_current_auth_user_for_refresh)):
    """
    Issues a new short-lived access token.
    Requires a valid long-lived refresh token in the request.
    """
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


# Endpoint to retrieve current user information
@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_auth_user)):
    """
    Returns the profile data of the currently authenticated user.
    Protected by the access token validation dependency.
    """
    return current_user
