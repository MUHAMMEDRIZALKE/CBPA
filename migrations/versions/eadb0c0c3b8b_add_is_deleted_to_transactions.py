"""Add is_deleted flag to transactions

Revision ID: eadb0c0c3b8b
Revises: 67cd49dac240
Create Date: 2026-02-24 18:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eadb0c0c3b8b"
down_revision: Union[str, Sequence[str], None] = "67cd49dac240"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add soft-delete flag to transactions; default existing rows to not deleted.
    op.add_column(
        "transactions",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    # Optional: drop server_default after backfill to keep schema clean.
    op.alter_column("transactions", "is_deleted", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("transactions", "is_deleted")

