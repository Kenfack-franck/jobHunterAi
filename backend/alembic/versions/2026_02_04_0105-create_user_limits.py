"""Create user_limits table

Revision ID: create_user_limits_001
Revises: add_user_role_001
Create Date: 2026-02-04 01:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_user_limits_001'
down_revision = 'add_user_role_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_limits table
    op.create_table('user_limits',
        # Primary key
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        
        # Foreign key to users
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        
        # Current usage counters
        sa.Column('saved_offers_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('searches_today_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('profiles_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('applications_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cv_parsed_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('watched_companies_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('generated_cv_today_count', sa.Integer(), nullable=False, server_default='0'),
        
        # Custom limits (NULL = use default)
        sa.Column('max_saved_offers', sa.Integer(), nullable=True),
        sa.Column('max_searches_per_day', sa.Integer(), nullable=True),
        sa.Column('max_profiles', sa.Integer(), nullable=True),
        sa.Column('max_applications', sa.Integer(), nullable=True),
        sa.Column('max_cv_parses', sa.Integer(), nullable=True),
        sa.Column('max_watched_companies', sa.Integer(), nullable=True),
        sa.Column('max_generated_cv_per_day', sa.Integer(), nullable=True),
        
        # Metadata for daily resets
        sa.Column('last_search_date', sa.Date(), nullable=True),
        sa.Column('last_cv_generation_date', sa.Date(), nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    # Create indexes
    op.create_index(op.f('ix_user_limits_user_id'), 'user_limits', ['user_id'], unique=True)
    op.create_index(op.f('ix_user_limits_last_search_date'), 'user_limits', ['last_search_date'], unique=False)


def downgrade() -> None:
    # Drop indexes first
    op.drop_index(op.f('ix_user_limits_last_search_date'), table_name='user_limits')
    op.drop_index(op.f('ix_user_limits_user_id'), table_name='user_limits')
    
    # Drop table
    op.drop_table('user_limits')
