"""
Schema: student_progress_reels
Template ID: student_progress_reels

Validates props for the University Student Progress Reels generator.
Privacy note: props must not include raw PII beyond display names.
Data retention and consent must be enforced at the API layer before
props reach this schema.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class SubjectGrade(BaseModel):
    subject: str = Field(max_length=120)
    grade: str = Field(max_length=16, description="e.g. 'A', '85%', 'Pass'.")
    trend: Literal["improving", "stable", "needs_attention"] = "stable"


class Achievement(BaseModel):
    title: str = Field(max_length=120)
    icon_key: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Icon identifier from the institution's asset pack.",
    )
    date: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )


class GoalItem(BaseModel):
    goal: str = Field(max_length=200)
    timeframe: Optional[str] = Field(default=None, max_length=64)


class PropsSchema(BaseModel):
    # Student identity (display only — no student ID or SSN)
    student_display_name: str = Field(
        max_length=80,
        description="First name or preferred name for personalised greeting.",
        examples=["Alex"],
    )
    institution_name: str = Field(max_length=120)
    academic_period: str = Field(
        max_length=80,
        description="e.g. 'Spring Semester 2026', 'Term 3 2026'.",
    )
    grade_band: Literal["k12", "undergraduate", "postgraduate"] = Field(
        description="Controls template variant and language level.",
    )

    # Academic content
    subjects: List[SubjectGrade] = Field(min_length=1, max_length=12)
    gpa_or_equivalent: Optional[str] = Field(
        default=None,
        max_length=16,
        description="Overall performance indicator, if applicable.",
    )
    achievements: Optional[List[Achievement]] = Field(default=None, max_length=8)
    goals: Optional[List[GoalItem]] = Field(default=None, max_length=5)
    advisor_message: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Personalised message from the academic advisor.",
    )

    # Delivery controls
    language_code: str = Field(
        default="en",
        max_length=8,
        description="BCP 47 language tag for subtitle generation.",
    )
    institution_brand_color: str = Field(
        default="#003087",
        pattern=r"^#[0-9A-Fa-f]{6}$",
    )
    institution_logo_url: Optional[str] = Field(default=None)
    consent_reference_id: str = Field(
        min_length=1,
        max_length=128,
        description="Opaque reference to the verified consent record. Required.",
    )
