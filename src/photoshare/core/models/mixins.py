from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# ==========================================
# Database Model Mixins & Utilities
# ==========================================


class TimestampMixin:
    """
    SQLAlchemy Mixin class that automatically injects audit tracking columns.
    Provides standardized 'created_at' and 'updated_at' fields with timezone awareness.
    """

    # Tracks initial row insert event using the database engine server timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Automatically shifts to current timestamp whenever an absolute mutation occurs on the row
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
