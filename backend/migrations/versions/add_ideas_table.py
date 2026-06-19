"""add_ideas_table

Revision ID: add_ideas_table
Revises: 1c428f795a20
Create Date: 2026-06-15 18:00:00.000000

"""
from alembic import op  # type: ignore
import sqlalchemy as sa  # type: ignore
from sqlalchemy.dialects import postgresql  # type: ignore

# revision identifiers, used by Alembic.
revision = 'add_ideas_table'
down_revision = '1c428f795a20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ideas table
    op.create_table(
        'ideas',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('artistic_rationale', sa.Text(), nullable=False),
        sa.Column('materials', sa.String(length=500), nullable=True),
        sa.Column('scale', sa.String(length=200), nullable=True),
        sa.Column('cultural_references', sa.Text(), nullable=True),
        sa.Column('brief', sa.Text(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_ideas_title'), 'ideas', ['title'], unique=False)
    op.create_index(op.f('ix_ideas_project_id'), 'ideas', ['project_id'], unique=False)
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_ideas_project_id',
        'ideas', 'projects',
        ['project_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_ideas_project_id', 'ideas', type_='foreignkey')
    
    # Drop indexes
    op.drop_index(op.f('ix_ideas_project_id'), table_name='ideas')
    op.drop_index(op.f('ix_ideas_title'), table_name='ideas')
    
    # Drop table
    op.drop_table('ideas')

# Made with Bob
