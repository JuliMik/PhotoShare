from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserResponse(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
