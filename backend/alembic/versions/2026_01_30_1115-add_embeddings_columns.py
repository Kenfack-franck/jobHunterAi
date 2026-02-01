"""add embeddings columns

Revision ID: 5d8e9f1a2b3c
Revises: a114cb0976fd
Create Date: 2026-01-30 11:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '5d8e9f1a2b3c'
down_revision = 'a114cb0976fd'
branch_labels = None
depends_on = None


def upgrade():
    # Add embedding column to profiles
    op.add_column('profiles', 
        sa.Column('embedding', Vector(384), nullable=True)
    )
    
    # Add embedding column to job_offers
    op.add_column('job_offers',
        sa.Column('embedding', Vector(384), nullable=True)
    )
    
    # Create HNSW indexes for fast similarity search
    # HNSW is optimized for approximate nearest neighbor search
    op.execute(
        "CREATE INDEX IF NOT EXISTS profile_embedding_idx ON profiles "
        "USING hnsw (embedding vector_cosine_ops)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS job_offer_embedding_idx ON job_offers "
        "USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade():
    # Drop indexes first
    op.execute("DROP INDEX IF EXISTS profile_embedding_idx")
    op.execute("DROP INDEX IF EXISTS job_offer_embedding_idx")
    
    # Drop columns
    op.drop_column('profiles', 'embedding')
    op.drop_column('job_offers', 'embedding')
