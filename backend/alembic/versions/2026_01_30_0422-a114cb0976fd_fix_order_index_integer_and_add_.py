"""fix order_index integer and add education location

Revision ID: a114cb0976fd
Revises: 3353ac94d250
Create Date: 2026-01-30 04:22:51.078046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a114cb0976fd'
down_revision = '3353ac94d250'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add location column to educations
    op.add_column('educations', sa.Column('location', sa.String(length=255), nullable=True))
    
    # Convert order_index from VARCHAR to INTEGER with USING
    op.execute('ALTER TABLE educations ALTER COLUMN order_index TYPE INTEGER USING order_index::integer')
    op.execute('ALTER TABLE experiences ALTER COLUMN order_index TYPE INTEGER USING order_index::integer')


def downgrade() -> None:
    # Revert order_index changes
    op.execute('ALTER TABLE experiences ALTER COLUMN order_index TYPE VARCHAR')
    op.execute('ALTER TABLE educations ALTER COLUMN order_index TYPE VARCHAR')
    
    # Remove location column
    op.drop_column('educations', 'location')
