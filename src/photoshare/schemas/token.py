from pydantic import BaseModel


# ==========================================
# Authentication Token Data Transfer Objects
# ==========================================

class TokenInfo(BaseModel):
    """
    Data Transfer Object (DTO) defining the strict JSON body layout
    returned to clients upon successful authentication or token renewal.
    """
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


# ==========================================
# Cryptographic Token Decoded Payloads
# ==========================================

class TokenPayload(BaseModel):
    """
    Internal validation schema representing verified data structures extracted
    directly out of decoded JSON Web Token (JWT) cryptographic signatures.
    """
    sub: str | None = None
    email: str | None = None
    role: str | None = None
