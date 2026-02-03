"""Add user source preferences table

Revision ID: 973f0a15e9d8
Revises: add_applications_001
Create Date: 2026-02-02 21:44:21.760127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '973f0a15e9d8'
down_revision = 'add_applications_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Créer uniquement la nouvelle table user_source_preferences
    op.create_table('user_source_preferences',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('profile_id', sa.UUID(), nullable=True),
    sa.Column('enabled_sources', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('priority_sources', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('use_cache', sa.Boolean(), nullable=False),
    sa.Column('cache_ttl_hours', sa.Integer(), nullable=False),
    sa.Column('max_priority_sources', sa.Integer(), nullable=False),
    sa.Column('background_scraping_enabled', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_source_preferences_user_id'), 'user_source_preferences', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_source_preferences_user_id'), table_name='user_source_preferences')
    op.drop_table('user_source_preferences')
