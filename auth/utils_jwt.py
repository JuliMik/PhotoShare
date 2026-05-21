import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from src.photoshare.core.config import settings

# ==========================================
# Password Hashing & Verification
# ==========================================


# Hashes a plain text password using bcrypt with a random salt
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using the bcrypt algorithm.
    Generates a secure salt automatically and returns a UTF-8 string.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode("utf-8")


# Verifies if a raw password matches the stored bcrypt hash
def validate_password(password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password against a stored bcrypt hash.
    Returns True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode("utf-8"),
    )


# ==========================================
# JWT Encoding & Decoding
# ==========================================


# Encodes data payload into a secure JWT using a private key
def encode_jwt(
    payload: dict,
    private_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    """
    Encodes a dictionary payload into a signed JSON Web Token.
    Automatically injects 'iat' (issued at) and 'exp' (expiration) timestamps
    and signs the token using an asymmetric private key.
    """
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


# Decodes and verifies a JWT using a public key
def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Decodes a JWT and verifies its cryptographic signature using a public key.
    Raises an error automatically if the token is expired or altered.
    """
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
