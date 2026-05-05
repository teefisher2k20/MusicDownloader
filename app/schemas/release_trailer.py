"""
Schema: release_trailer
Template ID: release_trailer

Validates props for the Product Release Auto-Trailer generator.
"""

from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator


class FeatureCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(max_length=80, description="Feature headline.")
    description: str = Field(max_length=300, description="One to two sentence feature summary.")
    screenshot_url: Optional[HttpUrl] = Field(
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
    model_config = ConfigDict(extra="forbid")

    commits: Optional[int] = Field(default=None, ge=0)
    contributors: Optional[int] = Field(default=None, ge=0)
    issues_closed: Optional[int] = Field(default=None, ge=0)
    adoption_percent: Optional[float] = Field(default=None, ge=0, le=100)


class PropsSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version_name: str = Field(
        min_length=1,
        max_length=64,
        description="Release version or codename shown in the opener.",
        examples=["v3.4.0 - Aurora"],
    )
    release_date: date = Field(
        description="ISO 8601 date string shown in the trailer.",
        examples=["2026-05-04"],
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
    cta_url: Optional[HttpUrl] = Field(
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

    @field_validator("version_name", "headline", "cta_text")
    @classmethod
    def _strip_and_require_text(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("must not be empty")
        return text

    @field_validator("release_date")
    @classmethod
    def _reasonable_release_date(cls, value: date) -> date:
        if value.year < 2000:
            raise ValueError("release_date year must be >= 2000")
        return value

    @model_validator(mode="after")
    def _validate_features(self) -> "PropsSchema":
        # Require distinct feature titles to avoid duplicate slides.
        titles = [f.title.strip().lower() for f in self.features]
        if len(set(titles)) != len(titles):
            raise ValueError("features must have unique titles")

        # For external channels, keep CTA fully actionable.
        if self.channel in {"youtube", "linkedin", "twitter"} and self.cta_url is None:
            raise ValueError("cta_url is required for external channels")

        return self
