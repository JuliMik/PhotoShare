"""add default to timestamps

Revision ID: 080847371067
Revises: 44f8c0b9a47b
Create Date: 2026-05-06 10:45:58.847942

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "080847371067"
down_revision: Union[str, Sequence[str], None] = "44f8c0b9a47b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
