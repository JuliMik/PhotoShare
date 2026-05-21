from datetime import timedelta

from auth.utils_jwt import encode_jwt
from src.photoshare.core.config import settings
from src.photoshare.core.models import User

# Global constants defining JWT payload fields and token types
TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


# ==========================================
# Core JWT Generation Helper
# ==========================================


# Generic helper function to assemble the payload and encode a JWT
def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Base helper function to create a JSON Web Token.
    Injects the token type into the payload and delegates encoding to utility tools.
    """
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


# ==========================================
# Token Management Services
# ==========================================


# Generates a short-lived access token with full user identity information
def create_access_token(user: User) -> str:
    """
    Generates a standard short-lived ACCESS token containing essential
    user data (ID, username, email, and role) used for route authorization.
    """
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


# Generates a long-lived refresh token with minimal payload data
def create_refresh_token(user: User) -> str:
    """
    Generates a long-lived REFRESH token containing only the user ID.
    Used strictly to request new access tokens when they expire.
    """
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
