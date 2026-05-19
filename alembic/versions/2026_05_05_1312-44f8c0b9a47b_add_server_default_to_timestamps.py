"""add server default to timestamps

Revision ID: 44f8c0b9a47b
Revises: d98fe461b063
Create Date: 2026-05-05 13:12:40.950419

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "44f8c0b9a47b"
down_revision: Union[str, Sequence[str], None] = "d98fe461b063"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.func.now()

    )
    op.alter_column(
        "users",
        "updated_at",
        server_default=sa.func.now()
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        server_default=None
    )
    op.alter_column(
        "users",
        "updated_at",
        server_default=None
    )
