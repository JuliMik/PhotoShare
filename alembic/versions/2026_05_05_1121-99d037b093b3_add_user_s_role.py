"""add user's role

Revision ID: 99d037b093b3
Revises: 74cb36a94193
Create Date: 2026-05-05 11:21:36.107659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "99d037b093b3"
down_revision: Union[str, Sequence[str], None] = "74cb36a94193"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = sa.Enum("USER", "MODERATOR", "ADMIN", name="userrole")
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(),
        type_=sa.Enum("USER", "MODERATOR", "ADMIN", name="userrole"),
        postgresql_using="role::userrole",
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("USER", "MODERATOR", "ADMIN", name="userrole"),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
