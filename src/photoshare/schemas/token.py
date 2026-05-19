from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    email: str | None = None
    role: str | None = None
