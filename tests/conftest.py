"""Pytest fixtures shared across all test modules."""

import asyncio
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.database import Base, get_session
from app.main import app
from app.models import JobStatus, RenderJob

# ── in-memory SQLite engine for tests ─────────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_engine) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI test client backed by an isolated in-memory database."""
    factory = async_sessionmaker(db_engine, expire_on_commit=False)

    async def _override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with factory() as session:
            yield session

    app.dependency_overrides[get_session] = _override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


def make_job(
    template_id: str = "sales_personalization",
    status: JobStatus = JobStatus.queued,
    priority: int = 5,
) -> RenderJob:
    now = datetime.now(timezone.utc)
    return RenderJob(
        job_id=str(uuid.uuid4()),
        idempotency_key=str(uuid.uuid4()),
        template_id=template_id,
        template_version="v1",
        props={"account_name": "Test"},
        priority=priority,
        status=status,
        progress=0,
        retry_count=0,
        created_at=now,
        updated_at=now,
    )
