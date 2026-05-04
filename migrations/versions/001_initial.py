"""Initial schema: render_jobs table

Revision ID: 001
Revises:
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "render_jobs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("idempotency_key", sa.String(length=256), nullable=False),
        sa.Column("template_id", sa.String(length=128), nullable=False),
        sa.Column("template_version", sa.String(length=32), nullable=False),
        sa.Column("props", JSONB(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_url", sa.Text(), nullable=True),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_render_jobs_job_id", "render_jobs", ["job_id"], unique=True)
    op.create_index(
        "ix_render_jobs_idempotency_key", "render_jobs", ["idempotency_key"], unique=True
    )
    op.create_index("ix_render_jobs_status", "render_jobs", ["status"])
    op.create_index("ix_render_jobs_template_id", "render_jobs", ["template_id"])


def downgrade() -> None:
    op.drop_table("render_jobs")
