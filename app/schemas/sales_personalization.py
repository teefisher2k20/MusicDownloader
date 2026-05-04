"""
Schema: sales_personalization
Template ID: sales_personalization

Validates props for the Sales Personalization Video Bot.
Each field maps directly to a scene slot in the Remotion composition.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl


class BrandTheme(BaseModel):
    primary_color: str = Field(
        default="#2563EB",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color for primary UI elements.",
    )
    logo_url: Optional[str] = Field(
        default=None,
        description="HTTPS URL to the company logo (PNG/SVG, max 1 MB).",
    )


class ProofPoint(BaseModel):
    metric: str = Field(max_length=80, description="e.g. '43% reduction in onboarding time'")
    source: Optional[str] = Field(default=None, max_length=120)


class PropsSchema(BaseModel):
    # Required
    account_name: str = Field(
        min_length=1,
        max_length=120,
        description="Target company name shown in the opener.",
        examples=["Acme Corp"],
    )
    persona_title: str = Field(
        min_length=1,
        max_length=80,
        description="Recipient's role shown in the personalised greeting.",
        examples=["VP of Engineering"],
    )
    pain_point: str = Field(
        min_length=1,
        max_length=200,
        description="Primary problem statement for the problem-statement scene.",
        examples=["Manual release pipelines slow down your team."],
    )
    proof_point: ProofPoint = Field(
        description="Social proof metric shown on the proof scene."
    )
    cta_text: str = Field(
        min_length=1,
        max_length=80,
        description="Call-to-action button label on the final scene.",
        examples=["Book a 15-min demo"],
    )

    # Optional overrides
    industry: Optional[str] = Field(
        default=None,
        max_length=80,
        description="Drives conditional B-roll selection.",
        examples=["SaaS", "FinTech", "Healthcare"],
    )
    sender_name: Optional[str] = Field(
        default=None,
        max_length=80,
        description="SDR/AE name shown in the opener.",
    )
    campaign_id: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Used for deduplication and analytics.",
    )
    brand: BrandTheme = Field(default_factory=BrandTheme)

    # Template output controls
    duration_seconds: int = Field(
        default=30,
        ge=10,
        le=120,
        description="Requested video duration. Actual duration may vary slightly.",
    )
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = Field(
        default="16:9",
        description="Output aspect ratio.",
    )
