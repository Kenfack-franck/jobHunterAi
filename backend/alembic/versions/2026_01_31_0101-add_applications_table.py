"""Add applications table

Revision ID: add_applications_001
Revises: c1e4b2da5903
Create Date: 2026-01-31 01:01:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "add_applications_001"
down_revision = "c1e4b2da5903"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_offer_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("job_title", sa.String(length=255), nullable=False),
        sa.Column("email_to", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("documents_sent", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_offer_id"], ["job_offers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_applications_user", "applications", ["user_id"])
    op.create_index("idx_applications_status", "applications", ["status"])
    op.create_index("idx_applications_applied_at", "applications", ["applied_at"])


def downgrade() -> None:
    op.drop_index("idx_applications_applied_at", table_name="applications")
    op.drop_index("idx_applications_status", table_name="applications")
    op.drop_index("idx_applications_user", table_name="applications")
    op.drop_table("applications")
