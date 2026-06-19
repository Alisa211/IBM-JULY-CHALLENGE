"""Add vector indexes

Revision ID: 72963a089897
Revises: 094327909e15
Create Date: 2026-06-16 00:11:43.019173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72963a089897'
down_revision: Union[str, None] = '094327909e15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE INDEX ON style_profiles USING hnsw (embedding vector_cosine_ops);")
    op.execute("CREATE INDEX ON ancient_art_chunks USING hnsw (embedding vector_cosine_ops);")

def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS style_profiles_embedding_idx;")
    op.execute("DROP INDEX IF EXISTS ancient_art_chunks_embedding_idx;")
