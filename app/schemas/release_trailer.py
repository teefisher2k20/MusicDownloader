"""
Schema: release_trailer
Template ID: release_trailer

Validates props for the Product Release Auto-Trailer generator.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class FeatureCard(BaseModel):
    title: str = Field(max_length=80, description="Feature headline.")
    description: str = Field(max_length=300, description="One to two sentence feature summary.")
    screenshot_url: Optional[str] = Field(
        default=None,
        description="HTTPS URL of a product screenshot (PNG/JPG, 1920x1080 recommended).",
    )
    impact_tag: Literal["performance", "ux", "security", "api", "infra", "other"] = Field(
        default="other"
    )
    priority_rank: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Higher rank features get more screen time.",
    )


class ReleaseMetrics(BaseModel):
    commits: Optional[int] = Field(default=None, ge=0)
    contributors: Optional[int] = Field(default=None, ge=0)
    issues_closed: Optional[int] = Field(default=None, ge=0)
    adoption_percent: Optional[float] = Field(default=None, ge=0, le=100)


class PropsSchema(BaseModel):
    version_name: str = Field(
        min_length=1,
        max_length=64,
        description="Release version or codename shown in the opener.",
        examples=["v3.4.0 - Aurora"],
    )
    release_date: str = Field(
        description="ISO 8601 date string shown in the trailer.",
        examples=["2026-05-04"],
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    headline: str = Field(
        min_length=1,
        max_length=200,
        description="Top-level narrative hook for the trailer.",
    )
    features: List[FeatureCard] = Field(
        min_length=1,
        max_length=12,
        description="Feature cards to include. Ordered by priority_rank descending.",
    )
    metrics: Optional[ReleaseMetrics] = Field(
        default=None,
        description="Optional stats shown in the metrics scene.",
    )
    cta_text: str = Field(
        default="Explore the release",
        max_length=80,
    )
    cta_url: Optional[str] = Field(
        default=None,
        description="URL displayed on the final CTA scene.",
    )
    brand_color: str = Field(
        default="#7C3AED",
        pattern=r"^#[0-9A-Fa-f]{6}$",
    )
    channel: Literal["youtube", "linkedin", "twitter", "internal"] = Field(
        default="youtube",
        description="Drives aspect ratio and safe-area margins.",
    )
