"""
Schema: geo_story_maps
Template ID: geo_story_maps

Validates props for the Geo Story Map Narratives generator.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)
    timestamp: Optional[str] = Field(
        default=None,
        description="ISO 8601 datetime at this point.",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
    )
    speed_kmh: Optional[float] = Field(default=None, ge=0.0)
    altitude_m: Optional[float] = Field(default=None)


class RouteEvent(BaseModel):
    event_id: str = Field(max_length=64)
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)
    timestamp: Optional[str] = Field(default=None)
    title: str = Field(max_length=120)
    description: Optional[str] = Field(default=None, max_length=400)
    icon_key: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Marker icon from the Mapbox icon pack.",
    )
    chapter_number: Optional[int] = Field(
        default=None,
        ge=1,
        description="Groups events into named chapters.",
    )


class CameraKeyframe(BaseModel):
    frame_index: int = Field(ge=0)
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)
    zoom: float = Field(ge=0.0, le=22.0)
    pitch: float = Field(ge=0.0, le=85.0)
    bearing: float = Field(ge=0.0, le=360.0)


class PropsSchema(BaseModel):
    story_title: str = Field(max_length=200)
    route_points: List[GeoPoint] = Field(
        min_length=2,
        max_length=5000,
        description="Ordered GPS track points.",
    )
    events: Optional[List[RouteEvent]] = Field(
        default=None,
        max_length=50,
        description="Key events along the route to annotate.",
    )
    camera_keyframes: Optional[List[CameraKeyframe]] = Field(
        default=None,
        max_length=100,
        description="Manual camera overrides. Auto-planned if omitted.",
    )
    map_style: Literal[
        "mapbox://styles/mapbox/standard",
        "mapbox://styles/mapbox/satellite-streets-v12",
        "mapbox://styles/mapbox/light-v11",
        "mapbox://styles/mapbox/dark-v11",
    ] = Field(default="mapbox://styles/mapbox/standard")
    mapbox_token: str = Field(
        min_length=10,
        description="Mapbox public token for tile loading.",
    )
    route_line_color: str = Field(default="#EF4444", pattern=r"^#[0-9A-Fa-f]{6}$")
    narration_script: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Full narration text for TTS. Synced to camera path.",
    )
    fps: int = Field(default=30, ge=24, le=60)
    duration_seconds: int = Field(
        default=60,
        ge=10,
        le=600,
        description="Target render duration. Camera path is scaled to fit.",
    )
    output_format: Literal["16:9", "9:16"] = Field(default="16:9")
    language_code: str = Field(default="en", max_length=8)
