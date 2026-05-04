"""
Redis-backed queue via arq.

arq provides:
- Priority-aware job dispatch via score-sorted sets.
- Built-in retry with max_tries and exponential back-off.
- Job deduplication via job_id.
- Per-job timeout enforcement.
"""

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from app.config import settings


def _redis_settings() -> RedisSettings:
    # arq accepts a RedisSettings object built from the REDIS_URL
    return RedisSettings.from_dsn(settings.redis_url)


async def get_queue() -> ArqRedis:
    """Returns a connected arq Redis pool for enqueuing jobs."""
    return await create_pool(_redis_settings())


async def enqueue_render(job_id: str, priority: int = 5) -> None:
    """
    Enqueue a render task.
    arq uses _job_id for deduplication; passing it prevents the same
    job from being queued twice if this function is called concurrently.
    Priority is inverted: lower score = higher priority in the sorted set.
    """
    pool = await get_queue()
    try:
        await pool.enqueue_job(
            "run_render_job",
            job_id,
            _job_id=job_id,
            _queue_name=f"renders:p{priority}",
        )
    finally:
        await pool.aclose()
