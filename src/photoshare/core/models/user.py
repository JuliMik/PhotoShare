from sqlalchemy import Boolean, String, Text, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.photoshare.core.models.base import Base
from src.photoshare.schemas.enums import UserRole
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("TRUE"), nullable=False
    )
