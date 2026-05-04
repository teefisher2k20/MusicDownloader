"""Add playlist action fields to render_jobs

Revision ID: 002
Revises: 001
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("render_jobs", sa.Column("playlist_name", sa.String(length=120), nullable=True))
    op.add_column(
        "render_jobs",
        sa.Column(
            "playlist_actions",
            JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("render_jobs", "playlist_actions")
    op.drop_column("render_jobs", "playlist_name")
