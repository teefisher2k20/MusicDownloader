from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models import (
    JobStatus,
    PlaylistActionRecord,
    PlaylistActionRequest,
    PlaylistActionResponse,
    RenderCreateRequest,
    RenderCreateResponse,
    RenderJob,
    RenderListResponse,
    RenderStatusResponse,
)
from app.queue_service import enqueue_render
from app.repository import PostgresJobRepository

router = APIRouter(tags=["renders"])


# ── Auth guard ────────────────────────────────────────────────────────────────

def _require_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> None:
    if x_api_key is None or x_api_key != settings.api_key_secret:
        raise HTTPException(status_code=401, detail="Invalid API key.")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/renders",
    response_model=RenderCreateResponse,
    status_code=202,
    summary="Submit a render job",
    response_description="Accepted render job.",
    dependencies=[Depends(_require_api_key)],
)
async def create_render(
    req: RenderCreateRequest,
    session: AsyncSession = Depends(get_session),
) -> RenderCreateResponse:
    """
    Submit a new render job. If a job with the same `idempotency_key` already
    exists, the original job is returned without creating a duplicate.
    """
    repo = PostgresJobRepository(session)

    existing = await repo.get_by_idempotency(req.idempotency_key)
    if existing:
        return RenderCreateResponse(
            job_id=existing.job_id,
            status=existing.status,
            created_at=existing.created_at,
        )

    job = RenderJob(
        template_id=req.template_id,
        template_version=req.template_version,
        props=req.props,
        priority=req.priority,
        idempotency_key=req.idempotency_key,
        status=JobStatus.queued,
    )
    job = await repo.create(job)
    await enqueue_render(job.job_id, priority=req.priority)

    return RenderCreateResponse(
        job_id=job.job_id,
        status=job.status,
        created_at=job.created_at,
    )


@router.get(
    "/renders/{job_id}",
    response_model=RenderStatusResponse,
    summary="Get render job status",
    dependencies=[Depends(_require_api_key)],
)
async def get_render(
    job_id: str,
    session: AsyncSession = Depends(get_session),
) -> RenderStatusResponse:
    repo = PostgresJobRepository(session)
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    return RenderStatusResponse(
        job_id=job.job_id,
        template_id=job.template_id,
        template_version=job.template_version,
        status=job.status,
        progress=job.progress,
        output_url=job.output_url,
        error_code=job.error_code,
        error_message=job.error_message,
        retry_count=job.retry_count,
        playlist_name=job.playlist_name,
        playlist_actions=job.playlist_actions,
        completed_at=job.completed_at,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.delete(
    "/renders/{job_id}",
    status_code=204,
    summary="Cancel a queued render job",
    dependencies=[Depends(_require_api_key)],
)
async def cancel_render(
    job_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = PostgresJobRepository(session)
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job.status not in (JobStatus.queued, JobStatus.validating):
        raise HTTPException(
            status_code=409,
            detail=f"Cannot cancel job in state '{job.status.value}'.",
        )

    job.status = JobStatus.canceled
    await repo.update(job)


@router.get(
    "/renders",
    response_model=RenderListResponse,
    summary="List render jobs",
    dependencies=[Depends(_require_api_key)],
)
async def list_renders(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = Query(default=None),
    template_id: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> RenderListResponse:
    repo = PostgresJobRepository(session)
    jobs, total = await repo.list_jobs(
        page=page, page_size=page_size, status=status, template_id=template_id
    )

    return RenderListResponse(
        items=[
            RenderStatusResponse(
                job_id=j.job_id,
                template_id=j.template_id,
                template_version=j.template_version,
                status=j.status,
                progress=j.progress,
                output_url=j.output_url,
                error_code=j.error_code,
                error_message=j.error_message,
                retry_count=j.retry_count,
                playlist_name=j.playlist_name,
                playlist_actions=j.playlist_actions,
                completed_at=j.completed_at,
                created_at=j.created_at,
                updated_at=j.updated_at,
            )
            for j in jobs
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/renders/{job_id}/playlist",
    response_model=PlaylistActionResponse,
    status_code=202,
    summary="Queue a post-completion playlist action",
    dependencies=[Depends(_require_api_key)],
)
async def queue_playlist_action(
    job_id: str,
    req: PlaylistActionRequest,
    session: AsyncSession = Depends(get_session),
) -> PlaylistActionResponse:
    repo = PostgresJobRepository(session)
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job.status != JobStatus.completed:
        raise HTTPException(
            status_code=409,
            detail="Playlist actions can be queued only after render completion.",
        )
    if not job.output_url:
        raise HTTPException(
            status_code=409,
            detail="Completed job does not have an output URL yet.",
        )

    record = PlaylistActionRecord(
        action=req.action,
        playlist_name=req.playlist_name,
        destination=req.destination,
        status="queued",
    )
    job.playlist_name = req.playlist_name
    job.playlist_actions.append(record)
    updated = await repo.update(job)

    return PlaylistActionResponse(
        job_id=updated.job_id,
        status=updated.status,
        output_url=updated.output_url,
        playlist_name=updated.playlist_name,
        actions=updated.playlist_actions,
    )


@router.get(
    "/renders/{job_id}/playlist",
    response_model=PlaylistActionResponse,
    summary="Get post-completion playlist actions",
    dependencies=[Depends(_require_api_key)],
)
async def get_playlist_actions(
    job_id: str,
    session: AsyncSession = Depends(get_session),
) -> PlaylistActionResponse:
    repo = PostgresJobRepository(session)
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    return PlaylistActionResponse(
        job_id=job.job_id,
        status=job.status,
        output_url=job.output_url,
        playlist_name=job.playlist_name,
        actions=job.playlist_actions,
    )


@router.delete(
    "/renders/{job_id}/playlist/{action_id}",
    status_code=204,
    summary="Remove a queued playlist action",
    dependencies=[Depends(_require_api_key)],
)
async def delete_playlist_action(
    job_id: str,
    action_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    repo = PostgresJobRepository(session)
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    original_len = len(job.playlist_actions)
    job.playlist_actions = [a for a in job.playlist_actions if a.action_id != action_id]
    if len(job.playlist_actions) == original_len:
        raise HTTPException(status_code=404, detail="Playlist action not found.")

    await repo.update(job)
