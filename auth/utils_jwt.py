import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from src.photoshare.core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode("utf-8")


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode("utf-8"),
    )


def encode_jwt(
    payload: dict,
    private_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    if private_key is None:
        private_key = settings.auth_jwt.private_key_path.read_text()

    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
