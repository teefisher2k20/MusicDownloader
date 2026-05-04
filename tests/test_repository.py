"""Repository layer tests against an in-memory SQLite database."""

import pytest

from app.models import JobStatus, PlaylistActionRecord, PostCompletionAction
from app.repository import PostgresJobRepository
from tests.conftest import make_job


@pytest.mark.asyncio
async def test_create_and_get(db_session):
    repo = PostgresJobRepository(db_session)
    job = make_job()
    created = await repo.create(job)
    assert created.job_id == job.job_id

    fetched = await repo.get(job.job_id)
    assert fetched is not None
    assert fetched.template_id == job.template_id


@pytest.mark.asyncio
async def test_get_nonexistent_returns_none(db_session):
    repo = PostgresJobRepository(db_session)
    result = await repo.get("does-not-exist")
    assert result is None


@pytest.mark.asyncio
async def test_get_by_idempotency_key(db_session):
    repo = PostgresJobRepository(db_session)
    job = make_job()
    await repo.create(job)

    result = await repo.get_by_idempotency(job.idempotency_key)
    assert result is not None
    assert result.job_id == job.job_id


@pytest.mark.asyncio
async def test_update_status(db_session):
    repo = PostgresJobRepository(db_session)
    job = make_job()
    await repo.create(job)

    job.status = JobStatus.completed
    job.progress = 100
    job.output_url = "https://cdn.example.com/output.mp4"
    updated = await repo.update(job)
    assert updated.status == JobStatus.completed
    assert updated.progress == 100
    assert updated.output_url == "https://cdn.example.com/output.mp4"


@pytest.mark.asyncio
async def test_list_jobs_pagination(db_session):
    repo = PostgresJobRepository(db_session)
    for _ in range(5):
        await repo.create(make_job())

    items, total = await repo.list_jobs(page=1, page_size=2)
    assert len(items) == 2
    assert total == 5

    items2, _ = await repo.list_jobs(page=2, page_size=2)
    assert len(items2) == 2
    assert items[0].job_id != items2[0].job_id


@pytest.mark.asyncio
async def test_list_jobs_filter_by_status(db_session):
    repo = PostgresJobRepository(db_session)
    await repo.create(make_job(status=JobStatus.queued))
    await repo.create(make_job(status=JobStatus.completed))

    queued, total = await repo.list_jobs(page=1, page_size=20, status=JobStatus.queued)
    assert total == 1
    assert queued[0].status == JobStatus.queued


@pytest.mark.asyncio
async def test_list_jobs_filter_by_template(db_session):
    repo = PostgresJobRepository(db_session)
    await repo.create(make_job(template_id="sales_personalization"))
    await repo.create(make_job(template_id="release_trailer"))

    items, total = await repo.list_jobs(page=1, page_size=20, template_id="release_trailer")
    assert total == 1
    assert items[0].template_id == "release_trailer"


@pytest.mark.asyncio
async def test_update_playlist_actions(db_session):
    repo = PostgresJobRepository(db_session)
    job = make_job(status=JobStatus.completed)
    job.output_url = "https://cdn.example.com/output.mp4"
    await repo.create(job)

    job.playlist_name = "Launch Playlist"
    job.playlist_actions = [
        PlaylistActionRecord(
            action=PostCompletionAction.share,
            playlist_name="Launch Playlist",
            destination="youtube-channel-main",
        )
    ]
    updated = await repo.update(job)

    assert updated.playlist_name == "Launch Playlist"
    assert len(updated.playlist_actions) == 1
    assert updated.playlist_actions[0].action == PostCompletionAction.share
