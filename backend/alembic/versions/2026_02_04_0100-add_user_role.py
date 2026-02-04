"""Add role column to users table

Revision ID: add_user_role_001
Revises: 29ca0abe9c64
Create Date: 2026-02-04 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_role_001'
down_revision = '29ca0abe9c64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add role column to users table
    op.add_column('users', 
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user')
    )
    
    # Create index on role for faster queries
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)


def downgrade() -> None:
    # Remove index first
    op.drop_index(op.f('ix_users_role'), table_name='users')
    
    # Remove role column
    op.drop_column('users', 'role')
