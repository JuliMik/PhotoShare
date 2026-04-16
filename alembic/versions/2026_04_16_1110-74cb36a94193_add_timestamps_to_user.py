"""add timestamps to user

Revision ID: 74cb36a94193
Revises: b28cd8266ddd
Create Date: 2026-04-16 11:10:55.178125

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "74cb36a94193"
down_revision: Union[str, Sequence[str], None] = "b28cd8266ddd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "users", sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
