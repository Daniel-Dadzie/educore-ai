"""enable pgvector extension

Revision ID: 9e5c5d9734ae
Revises:
Create Date: 2026-09-10 16:44:31.328036

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e5c5d9734ae"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Enable the pgvector extension (idempotent)."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade() -> None:
    """Disable the pgvector extension.

    WARNING: dropping this extension will cascade and destroy all vector
    columns and indexes.  Only run in a non-production environment or after
    confirming no vector data exists.
    """
    op.execute("DROP EXTENSION IF EXISTS vector CASCADE;")
