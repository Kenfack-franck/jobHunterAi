"""fix current boolean and technologies array types

Revision ID: 3353ac94d250
Revises: 10d7e7e0ea63
Create Date: 2026-01-30 04:17:30.316031

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3353ac94d250'
down_revision = '10d7e7e0ea63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Fix current column: VARCHAR -> Boolean avec USING
    op.execute("ALTER TABLE experiences ALTER COLUMN current TYPE BOOLEAN USING CASE WHEN current = 'True' THEN TRUE ELSE FALSE END")
    
    # Fix technologies column: TEXT -> ARRAY(String)
    op.execute("ALTER TABLE experiences ALTER COLUMN technologies TYPE VARCHAR[] USING CASE WHEN technologies IS NULL THEN NULL ELSE ARRAY[technologies] END")


def downgrade() -> None:
    # Revert technologies: ARRAY -> TEXT
    op.execute('ALTER TABLE experiences ALTER COLUMN technologies TYPE TEXT')
    
    # Revert current: Boolean -> VARCHAR
    op.execute('ALTER TABLE experiences ALTER COLUMN current TYPE VARCHAR')
