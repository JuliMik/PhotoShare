from sqlalchemy import Boolean, String, Text, text, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.photoshare.core.models.base import Base
from src.photoshare.schemas.enums import UserRole
from .mixins import TimestampMixin

# ==========================================
# Core Authentication & Identity Domain Models
# ==========================================


class User(Base, TimestampMixin):
    """
    SQLAlchemy ORM model representing user records within the database ecosystem.
    Inherits primary key capabilities from 'Base' and audit tracking fields from 'TimestampMixin'.
    """

    # Unique credential identifiers required for registration and system access
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    # Secure cryptographically hashed string containing the validation passphrase signature
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)

    # RBAC (Role-Based Access Control) specification map mapped onto native string/database enumerations
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
        server_default=UserRole.USER.value,
    )

    # System flag controlling overall profile operational access and authentication routing permissions
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("TRUE"), nullable=False
    )
