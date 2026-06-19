"""Stage 6 Agents Database Update

Revision ID: 036755148bed
Revises: 72963a089897
Create Date: 2026-06-16 14:11:19.728233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '036755148bed'
down_revision: Union[str, None] = '72963a089897'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create project_memory table
    op.create_table(
        'project_memory',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('historical_decisions', sa.JSON(), nullable=True),
        sa.Column('accepted_ideas', sa.JSON(), nullable=True),
        sa.Column('rejected_ideas', sa.JSON(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_memory_id'), 'project_memory', ['id'], unique=False)
    op.create_index(op.f('ix_project_memory_project_id'), 'project_memory', ['project_id'], unique=True)

    # 2. Update creative_runs table
    op.add_column('creative_runs', sa.Column('workflow_state', sa.JSON(), nullable=True))
    
    # 3. Update ideas table
    op.add_column('ideas', sa.Column('creative_run_id', sa.String(), nullable=True))
    op.add_column('ideas', sa.Column('parent_idea_id', sa.String(), nullable=True))
    op.add_column('ideas', sa.Column('version', sa.String(), nullable=True))
    op.add_column('ideas', sa.Column('status', sa.String(), nullable=True))
    op.create_foreign_key(None, 'ideas', 'creative_runs', ['creative_run_id'], ['id'])
    op.create_foreign_key(None, 'ideas', 'ideas', ['parent_idea_id'], ['id'])


def downgrade() -> None:
    # 1. Update ideas table
    op.drop_constraint(None, 'ideas', type_='foreignkey')
    op.drop_constraint(None, 'ideas', type_='foreignkey')
    op.drop_column('ideas', 'status')
    op.drop_column('ideas', 'version')
    op.drop_column('ideas', 'parent_idea_id')
    op.drop_column('ideas', 'creative_run_id')

    # 2. Update creative_runs table
    op.drop_column('creative_runs', 'workflow_state')

    # 3. Drop project_memory table
    op.drop_index(op.f('ix_project_memory_project_id'), table_name='project_memory')
    op.drop_index(op.f('ix_project_memory_id'), table_name='project_memory')
    op.drop_table('project_memory')
