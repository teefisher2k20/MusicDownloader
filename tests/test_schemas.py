"""Pydantic schema validation tests for all seven templates."""

import pytest
from pydantic import ValidationError

from app.schemas.sales_personalization import PropsSchema as SalesProps
from app.schemas.release_trailer import PropsSchema as TrailerProps
from app.schemas.shorts_factory import PropsSchema as ShortsProps
from app.schemas.kpi_morning_brief import PropsSchema as BriefProps
from app.schemas.student_progress_reels import PropsSchema as StudentProps
from app.schemas.ecommerce_ad_composer import PropsSchema as EcommerceProps
from app.schemas.geo_story_maps import PropsSchema as GeoProps


# ── 1. Sales Personalization ──────────────────────────────────────────────────

VALID_SALES = {
    "account_name": "Acme",
    "persona_title": "VP Eng",
    "pain_point": "Pipelines slow.",
    "proof_point": {"metric": "43%", "source": "G2"},
    "cta_text": "Book demo",
    "duration_seconds": 30,
    "aspect_ratio": "16:9",
    "brand": {"primary_color": "#2563EB"},
}


def test_sales_valid():
    p = SalesProps(**VALID_SALES)
    assert p.account_name == "Acme"


def test_sales_invalid_aspect_ratio():
    with pytest.raises(ValidationError):
        SalesProps(**{**VALID_SALES, "aspect_ratio": "4:3"})


def test_sales_missing_required():
    with pytest.raises(ValidationError):
        SalesProps(account_name="X")


# ── 2. Release Trailer ────────────────────────────────────────────────────────

VALID_TRAILER = {
    "version_name": "v3.4.0",
    "release_date": "2026-05-04",
    "headline": "Faster builds.",
    "brand_color": "#7C3AED",
    "channel": "youtube",
    "cta_text": "See release",
    "cta_url": "https://example.com",
    "features": [
        {"title": "CI speedup", "description": "90s builds.", "impact_tag": "performance", "priority_rank": 10}
    ],
}


def test_trailer_valid():
    p = TrailerProps(**VALID_TRAILER)
    assert len(p.features) == 1


def test_trailer_invalid_date():
    with pytest.raises(ValidationError):
        TrailerProps(**{**VALID_TRAILER, "release_date": "not-a-date"})


def test_trailer_too_many_features():
    with pytest.raises(ValidationError):
        TrailerProps(**{**VALID_TRAILER, "features": [
            {"title": f"F{i}", "description": "d", "impact_tag": "ux", "priority_rank": i}
            for i in range(13)
        ]})


# ── 3. Shorts Factory ─────────────────────────────────────────────────────────

VALID_SHORTS = {
    "source_title": "Ep 42",
    "aspect_ratio": "9:16",
    "hook_text": "You won't believe this...",
    "creator_handle": "@dev",
    "caption_style": {"font_family": "Inter", "font_size": 64, "highlight_color": "#FACC15", "outline": True},
    "music_url": "https://cdn.example.com/music.mp3",
    "music_volume": 0.1,
    "segments": [{"segment_id": "s1", "start_ms": 0, "end_ms": 5000, "text": "Hello world.", "hook_score": 0.8}],
}


def test_shorts_valid():
    p = ShortsProps(**VALID_SHORTS)
    assert p.creator_handle == "@dev"


def test_shorts_invalid_volume():
    with pytest.raises(ValidationError):
        ShortsProps(**{**VALID_SHORTS, "music_volume": 2.0})


# ── 4. KPI Morning Brief ──────────────────────────────────────────────────────

VALID_BRIEF = {
    "business_unit": "Revenue EMEA",
    "date_label": "Mon 4 May 2026",
    "headline": "Revenue up 8%.",
    "metrics": [{"label": "ARR", "value": "$4.2M", "trend": "up", "status": "green"}],
}


def test_brief_valid():
    p = BriefProps(**VALID_BRIEF)
    assert len(p.metrics) == 1


def test_brief_too_many_metrics():
    with pytest.raises(ValidationError):
        BriefProps(**{**VALID_BRIEF, "metrics": [
            {"label": f"M{i}", "value": "0", "trend": "flat", "status": "green"}
            for i in range(9)
        ]})


def test_brief_invalid_color():
    with pytest.raises(ValidationError):
        BriefProps(**{**VALID_BRIEF, "brand_color": "blue"})


# ── 5. Student Progress Reels ─────────────────────────────────────────────────

VALID_STUDENT = {
    "student_display_name": "Alex",
    "institution_name": "Northgate University",
    "academic_period": "Spring 2026",
    "grade_band": "undergraduate",
    "consent_reference_id": "consent-abc-123",
    "subjects": [{"subject": "CS", "grade": "A", "trend": "improving"}],
}


def test_student_valid():
    p = StudentProps(**VALID_STUDENT)
    assert p.student_display_name == "Alex"


def test_student_missing_consent():
    with pytest.raises(ValidationError):
        StudentProps(**{k: v for k, v in VALID_STUDENT.items() if k != "consent_reference_id"})


def test_student_invalid_grade_band():
    with pytest.raises(ValidationError):
        StudentProps(**{**VALID_STUDENT, "grade_band": "primary"})


# ── 6. Ecommerce Ad Composer ──────────────────────────────────────────────────

VALID_ECOMMERCE = {
    "campaign_name": "Summer Sale",
    "offer_headline": "40% off",
    "cta_text": "Shop Now",
    "brand_color": "#E11D48",
    "channel": "meta",
    "audience": {"segment_id": "seg-1", "label": "Returners", "tone": "urgent"},
    "products": [
        {"sku_id": "S1", "name": "Shoe", "image_url": "https://cdn.example.com/s.jpg", "price": "$89"}
    ],
}


def test_ecommerce_valid():
    p = EcommerceProps(**VALID_ECOMMERCE)
    assert len(p.products) == 1


def test_ecommerce_too_many_products():
    with pytest.raises(ValidationError):
        EcommerceProps(**{**VALID_ECOMMERCE, "products": [
            {"sku_id": f"S{i}", "name": "X", "image_url": "https://cdn.example.com/x.jpg", "price": "$1"}
            for i in range(6)
        ]})


def test_ecommerce_duration_out_of_range():
    with pytest.raises(ValidationError):
        EcommerceProps(**{**VALID_ECOMMERCE, "duration_seconds": 5})


# ── 7. Geo Story Maps ─────────────────────────────────────────────────────────

VALID_GEO = {
    "story_title": "London Marathon",
    "mapbox_token": "pk.example.token",
    "route_points": [
        {"lat": 51.5014, "lon": -0.1419},
        {"lat": 51.4975, "lon": -0.0753},
    ],
}


def test_geo_valid():
    p = GeoProps(**VALID_GEO)
    assert len(p.route_points) == 2


def test_geo_single_point_invalid():
    with pytest.raises(ValidationError):
        GeoProps(**{**VALID_GEO, "route_points": [{"lat": 51.5, "lon": -0.1}]})


def test_geo_lat_out_of_range():
    with pytest.raises(ValidationError):
        GeoProps(**{**VALID_GEO, "route_points": [
            {"lat": 95.0, "lon": -0.1},
            {"lat": 51.5, "lon": -0.1},
        ]})


def test_geo_duration_min():
    with pytest.raises(ValidationError):
        GeoProps(**{**VALID_GEO, "duration_seconds": 5})
