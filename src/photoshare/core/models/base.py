from datetime import datetime
from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Annotated
from src.photoshare.core.config import settings

from src.photoshare.utils import camel_case_to_snake_case

# Reusable custom type annotation for automatically tracking rows creation time
# Implements UTC-aware DateTime and leverages database-side default server time (func.now)
timestamp_tz = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now()),
]


# ==========================================
# SQLAlchemy Declarative Base Architecture
# ==========================================


class Base(DeclarativeBase):
    """
    Abstract declarative base class for all database models.
    Enforces unified naming conventions, primary key architecture, and dynamic table discovery.
    """

    __abstract__ = True

    # Integrates configuration-driven naming conventions for constraints and indexes
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Dynamically generates table names in plural snake_case format.
        Converts the class name (e.g., 'UserProfile' becomes 'user_profiles').
        """
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    # Implicitly provisions an integer primary key 'id' column for every inheriting subclass
    id: Mapped[int] = mapped_column(primary_key=True)
