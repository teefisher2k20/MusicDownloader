"""
Schema: shorts_factory
Template ID: shorts_factory

Validates props for the Creator Shorts Factory.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class CaptionWord(BaseModel):
    word: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)


class TranscriptSegment(BaseModel):
    segment_id: str = Field(max_length=64)
    start_ms: int = Field(ge=0, description="Start offset in milliseconds from source start.")
    end_ms: int = Field(ge=0, description="End offset in milliseconds.")
    text: str = Field(min_length=1, max_length=2000)
    words: Optional[List[CaptionWord]] = Field(
        default=None,
        description="Word-level timing for kinetic captions. Optional but recommended.",
    )
    hook_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Normalised score for how likely this segment is to be a hook (0-1).",
    )


class BRollSlot(BaseModel):
    position_ms: int = Field(ge=0, description="When the B-roll should appear in the short.")
    asset_url: str = Field(description="HTTPS URL of the B-roll clip or image.")
    duration_ms: int = Field(ge=500, le=10000)


class CaptionStyle(BaseModel):
    font_family: str = Field(default="Inter")
    font_size: int = Field(default=56, ge=24, le=120)
    highlight_color: str = Field(default="#FACC15", pattern=r"^#[0-9A-Fa-f]{6}$")
    outline: bool = Field(default=True)


class PropsSchema(BaseModel):
    source_title: str = Field(max_length=200, description="Source video or podcast title.")
    segments: List[TranscriptSegment] = Field(
        min_length=1,
        max_length=50,
        description="Ordered transcript segments for this specific short.",
    )
    hook_text: Optional[str] = Field(
        default=None,
        max_length=120,
        description="Override hook displayed before segments begin.",
    )
    b_roll_slots: Optional[List[BRollSlot]] = Field(
        default=None,
        max_length=10,
    )
    caption_style: CaptionStyle = Field(default_factory=CaptionStyle)
    music_url: Optional[str] = Field(
        default=None,
        description="HTTPS URL of background music track. Volume is auto-ducked.",
    )
    music_volume: float = Field(default=0.08, ge=0.0, le=1.0)
    aspect_ratio: Literal["9:16", "1:1"] = Field(default="9:16")
    creator_handle: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Handle shown in the outro frame.",
    )
    variant_label: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Label for A/B testing (e.g. 'hook-a', 'hook-b').",
    )
