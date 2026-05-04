"""
Schema: kpi_morning_brief
Template ID: kpi_morning_brief

Validates props for the Live KPI Morning Brief.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class MetricCard(BaseModel):
    label: str = Field(max_length=80, description="Metric display name.")
    value: str = Field(max_length=32, description="Formatted value, e.g. '$4.2M' or '87%'.")
    delta: Optional[str] = Field(
        default=None,
        max_length=32,
        description="Change vs prior period, e.g. '+12%' or '-3pp'.",
    )
    trend: Literal["up", "down", "flat"] = Field(default="flat")
    status: Literal["green", "amber", "red"] = Field(
        default="green",
        description="RAG status driving card colour.",
    )
    unit: Optional[str] = Field(default=None, max_length=32, description="e.g. 'USD', '%', 'users'")


class AlertItem(BaseModel):
    severity: Literal["critical", "warning", "info"] = "info"
    title: str = Field(max_length=120)
    detail: Optional[str] = Field(default=None, max_length=300)


class ActionItem(BaseModel):
    owner: str = Field(max_length=80)
    action: str = Field(max_length=200)
    due: Optional[str] = Field(default=None, max_length=32, description="e.g. 'Today', 'EOW'")


class PropsSchema(BaseModel):
    business_unit: str = Field(
        max_length=120,
        description="Business unit name shown in the header.",
        examples=["Revenue - EMEA"],
    )
    date_label: str = Field(
        description="Report date shown in header, e.g. 'Monday 4 May 2026'.",
        max_length=64,
    )
    headline: str = Field(
        max_length=200,
        description="Top-level narrative sentence for the brief.",
    )
    metrics: List[MetricCard] = Field(
        min_length=1,
        max_length=8,
        description="KPI cards to display. Up to 8 per brief.",
    )
    alerts: Optional[List[AlertItem]] = Field(
        default=None,
        max_length=5,
        description="Risk or opportunity alerts shown in the alert scene.",
    )
    actions: Optional[List[ActionItem]] = Field(
        default=None,
        max_length=5,
        description="Action items shown in the closing scene.",
    )
    brand_color: str = Field(default="#1E3A5F", pattern=r"^#[0-9A-Fa-f]{6}$")
    logo_url: Optional[str] = Field(default=None)
    narration_text: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional TTS narration script for the full brief.",
    )
