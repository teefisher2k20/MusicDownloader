"""
Schema: ecommerce_ad_composer
Template ID: ecommerce_ad_composer

Validates props for the E-commerce Dynamic Ad Composer.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ProductItem(BaseModel):
    sku_id: str = Field(max_length=64)
    name: str = Field(max_length=120)
    image_url: str = Field(description="HTTPS URL of the primary product image.")
    price: str = Field(max_length=32, description="Formatted price, e.g. '$49.99'.")
    original_price: Optional[str] = Field(
        default=None,
        max_length=32,
        description="Shown as strikethrough if provided.",
    )
    badge: Optional[str] = Field(
        default=None,
        max_length=32,
        description="e.g. 'New', 'Sale', 'Bestseller'.",
    )
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    review_count: Optional[int] = Field(default=None, ge=0)


class BenefitPoint(BaseModel):
    icon_key: Optional[str] = Field(default=None, max_length=64)
    text: str = Field(max_length=80)


class AudienceSegment(BaseModel):
    segment_id: str = Field(max_length=64)
    label: str = Field(max_length=80, description="e.g. 'High-intent returners'.")
    tone: Literal["urgent", "aspirational", "informative", "playful"] = "informative"


class PropsSchema(BaseModel):
    campaign_name: str = Field(max_length=120)
    products: List[ProductItem] = Field(
        min_length=1,
        max_length=5,
        description="Products to feature. Multi-product ads use a carousel pattern.",
    )
    offer_headline: str = Field(
        max_length=100,
        description="Primary offer message, e.g. 'Up to 40% off this weekend'.",
    )
    benefits: Optional[List[BenefitPoint]] = Field(
        default=None,
        max_length=4,
        description="Short benefit bullets shown in the product scene.",
    )
    cta_text: str = Field(
        default="Shop Now",
        max_length=40,
    )
    urgency_text: Optional[str] = Field(
        default=None,
        max_length=80,
        description="Urgency line, e.g. 'Offer ends midnight Sunday'.",
    )
    audience: AudienceSegment
    brand_color: str = Field(default="#E11D48", pattern=r"^#[0-9A-Fa-f]{6}$")
    logo_url: Optional[str] = Field(default=None)
    channel: Literal["meta", "tiktok", "youtube", "display"] = Field(
        default="meta",
        description="Drives safe-area margins and aspect ratio.",
    )
    aspect_ratio: Literal["9:16", "1:1", "16:9", "4:5"] = Field(default="1:1")
    duration_seconds: int = Field(default=15, ge=6, le=60)
    variant_id: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Experiment arm identifier for A/B tracking.",
    )
