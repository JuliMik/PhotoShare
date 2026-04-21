import jwt
from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = None,
        algorithm: str = settings.auth_jwt.algorithm,
):
    if private_key is None:
        private_key = settings.auth_jwt.private_key_path.read_text()

    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = None,
        algorithm: str = settings.auth_jwt.algorithm,
):
    if public_key is None:
        public_key = settings.auth_jwt.public_key_path.read_text()

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


