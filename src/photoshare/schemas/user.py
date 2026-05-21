from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .enums import UserRole


# ==========================================
# Base Identity Profile Schemas
# ==========================================

class UserBase(BaseModel):
    """
    Core validation contract establishing shared domain parameters for user properties.
    Ensures structural integrity for email formats and username queries system-wide.
    """
    email: EmailStr
    username: str


# ==========================================
# Inbound Registration Payload Schemas
# ==========================================

class UserCreate(UserBase):
    """
    Inbound validation model handling account registration details.
    Enforces password structural complexity rules prior to cryptographic hashing.
    """
    password: str = Field(min_length=8)


# ==========================================
# Outbound Serialized Response Schemas
# ==========================================

class UserResponse(UserBase):
    """
    Outbound Serialization DTO defining public data exposures across read API gateways.
    Maps complex relational entity instances into strict data schemas safely.
    """
    model_config = ConfigDict(
        from_attributes=True,  # Permits automated extraction directly from SQLAlchemy ORM fields
    )
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
