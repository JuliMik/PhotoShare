from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils_jwt import decode_jwt, validate_password
from auth.service import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.photoshare.core.models.db_helper import db_helper
from src.photoshare.core.models.user import User
from src.photoshare.api.api_v1.crud.users import get_user_by_id, get_user_by_username
from src.photoshare.core.config import settings

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api.prefix}{settings.api.v1.prefix}/auth/login/",
)


async def validate_auth_user_login(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await get_user_by_username(session, username)

    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


def validate_token_type(
    payload: dict,
    token_type: str,
) -> None:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
        )


async def _get_user_from_token(
    token: str,
    token_type: str,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
    )
    try:
        payload = decode_jwt(token=token)
        user_id: str | None = payload.get("sub")

        validate_token_type(payload=payload, token_type=token_type)

        if not user_id:
            raise unauthed_exc
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}",
        )
    user = await get_user_by_id(session, int(user_id))

    if not user:
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


async def get_current_auth_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    return await _get_user_from_token(
        token=token,
        token_type=ACCESS_TOKEN_TYPE,
        session=session,
    )


async def get_current_auth_user_for_refresh(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    return await _get_user_from_token(
        token=token,
        token_type=REFRESH_TOKEN_TYPE,
        session=session,
    )


