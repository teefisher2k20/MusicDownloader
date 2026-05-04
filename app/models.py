from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class JobStatus(str, Enum):
    queued = "queued"
    validating = "validating"
    preparing = "preparing"
    rendering = "rendering"
    postprocessing = "postprocessing"
    uploading = "uploading"
    completed = "completed"
    failed = "failed"
    canceled = "canceled"


class PostCompletionAction(str, Enum):
    listen = "listen"
    export = "export"
    download = "download"
    share = "share"
    deploy = "deploy"


# ── Request / Response models ─────────────────────────────────────────────────

class RenderCreateRequest(BaseModel):
    template_id: str = Field(
        min_length=1,
        max_length=128,
        examples=["sales_personalization"],
        description="Registered template identifier.",
    )
    template_version: str = Field(
        min_length=1,
        max_length=32,
        examples=["v1"],
        description="Semver or named version of the template.",
    )
    props: Dict[str, Any] = Field(
        description="Template-specific input props. Must satisfy the template's schema.",
        examples=[{"account_name": "Acme Corp", "persona": "VP of Engineering"}],
    )
    priority: int = Field(
        default=5,
        ge=1,
        le=10,
        description="1 = lowest, 10 = highest. Higher priority jobs are dequeued first.",
    )
    idempotency_key: str = Field(
        min_length=1,
        max_length=256,
        description="Caller-supplied unique key. Re-submitting with the same key returns the original job.",
        examples=["account-123-campaign-q3-2026"],
    )


class RenderCreateResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime


class RenderStatusResponse(BaseModel):
    job_id: str
    template_id: str
    template_version: str
    status: JobStatus
    progress: int = Field(ge=0, le=100)
    output_url: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]
    retry_count: int
    playlist_name: Optional[str] = None
    playlist_actions: list["PlaylistActionRecord"] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class RenderListResponse(BaseModel):
    items: list[RenderStatusResponse]
    total: int
    page: int
    page_size: int


class PlaylistActionRequest(BaseModel):
    action: PostCompletionAction
    playlist_name: str = Field(min_length=1, max_length=120)
    destination: Optional[str] = Field(
        default=None,
        max_length=256,
        description="Streaming app, device, or share target.",
        examples=["spotify:my-podcast", "roku-living-room", "youtube-channel-main"],
    )


class PlaylistActionRecord(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: PostCompletionAction
    playlist_name: str
    destination: Optional[str] = None
    status: str = "queued"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlaylistActionResponse(BaseModel):
    job_id: str
    status: JobStatus
    output_url: Optional[str]
    playlist_name: Optional[str]
    actions: list[PlaylistActionRecord]


# ── Internal domain model ─────────────────────────────────────────────────────

class RenderJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: str
    template_version: str
    props: Dict[str, Any]
    priority: int = 5
    idempotency_key: str
    status: JobStatus = JobStatus.queued
    progress: int = 0
    output_url: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    playlist_name: Optional[str] = None
    playlist_actions: list[PlaylistActionRecord] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}
