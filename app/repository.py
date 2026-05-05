from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import JobRecord
from app.models import RenderJob


def _to_domain(record: JobRecord) -> RenderJob:
    if record.playlist_actions is None:
        record.playlist_actions = []
    return RenderJob.model_validate(record)


class PostgresJobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_idempotency(self, key: str) -> Optional[RenderJob]:
        result = await self._session.execute(
            select(JobRecord).where(JobRecord.idempotency_key == key)
        )
        record = result.scalar_one_or_none()
        return _to_domain(record) if record else None

    async def create(self, job: RenderJob) -> RenderJob:
        record = JobRecord(
            job_id=job.job_id,
            idempotency_key=job.idempotency_key,
            template_id=job.template_id,
            template_version=job.template_version,
            props=job.props,
            priority=job.priority,
            status=job.status.value,
            progress=job.progress,
            retry_count=job.retry_count,
            playlist_name=job.playlist_name,
            playlist_actions=[a.model_dump(mode="json") for a in job.playlist_actions],
        )
        self._session.add(record)
        await self._session.commit()
        await self._session.refresh(record)
        return _to_domain(record)

    async def get(self, job_id: str) -> Optional[RenderJob]:
        result = await self._session.execute(
            select(JobRecord).where(JobRecord.job_id == job_id)
        )
        record = result.scalar_one_or_none()
        return _to_domain(record) if record else None

    async def update(self, job: RenderJob) -> RenderJob:
        await self._session.execute(
            update(JobRecord)
            .where(JobRecord.job_id == job.job_id)
            .values(
                status=job.status.value,
                progress=job.progress,
                output_url=job.output_url,
                error_code=job.error_code,
                error_message=job.error_message,
                retry_count=job.retry_count,
                playlist_name=job.playlist_name,
                playlist_actions=[a.model_dump(mode="json") for a in job.playlist_actions],
                completed_at=job.completed_at,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self._session.commit()
        return await self.get(job.job_id)

    async def list_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        template_id: Optional[str] = None,
    ) -> tuple[list[RenderJob], int]:
        query = select(JobRecord)

        if status:
            query = query.where(JobRecord.status == status)
        if template_id:
            query = query.where(JobRecord.template_id == template_id)

        query = query.order_by(JobRecord.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self._session.execute(query)
        records = result.scalars().all()

        count_query = select(func.count()).select_from(JobRecord)
        if status:
            count_query = count_query.where(JobRecord.status == status)
        if template_id:
            count_query = count_query.where(JobRecord.template_id == template_id)

        count_result = await self._session.execute(count_query)
        total = count_result.scalar_one()

        return [_to_domain(r) for r in records], total
