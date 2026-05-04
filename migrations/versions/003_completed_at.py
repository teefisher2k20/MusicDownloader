"""Add completed_at timestamp to render_jobs

Revision ID: 003
Revises: 002
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "render_jobs",
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("render_jobs", "completed_at")
