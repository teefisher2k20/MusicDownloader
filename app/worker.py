"""
arq worker: pulls render jobs from Redis, processes them through the full
render pipeline, and updates PostgreSQL state at each stage.

Retry policy:
  - max_tries = settings.worker_max_tries (default 3)
  - arq applies exponential back-off automatically between retries.
  - After max_tries, the job transitions to "failed" and is not re-queued.
"""

import asyncio
import importlib
from datetime import datetime, timezone
from arq import Worker
from arq.connections import RedisSettings

from app.config import settings
from app.database import AsyncSessionLocal
from app.logging_config import configure_logging, logger
from app.models import JobStatus, RenderJob
from app.repository import PostgresJobRepository
from app.runner import RenderError, runner
from app.storage import storage


# ── Job function ──────────────────────────────────────────────────────────────

async def run_render_job(ctx: dict, job_id: str) -> dict:
    """
    Main job function executed by the arq worker.
    ctx['job_try'] holds the current attempt number (1-indexed).
    """
    attempt = ctx.get("job_try", 1)
    configure_logging()
    log = logger.bind(job_id=job_id, attempt=attempt)
    log.info("worker.job_received")

    async with AsyncSessionLocal() as session:
        repo = PostgresJobRepository(session)
        job = await repo.get(job_id)

        if job is None:
            log.error("worker.job_not_found")
            return {"error": "job_not_found"}

        if job.status == JobStatus.canceled:
            log.info("worker.job_canceled")
            return {"status": "canceled"}

        try:
            # ── Validating ────────────────────────────────────────────────
            job.status = JobStatus.validating
            job.progress = 5
            job.retry_count = attempt - 1
            await repo.update(job)

            # ── Template schema validation ────────────────────────────────
            _validate_props(job)

            # ── Preparing ─────────────────────────────────────────────────
            job.status = JobStatus.preparing
            job.progress = 15
            await repo.update(job)

            # ── Rendering ─────────────────────────────────────────────────
            job.status = JobStatus.rendering
            job.progress = 30
            await repo.update(job)

            def progress_cb(pct: int) -> None:
                # fire-and-forget progress; keep it simple
                job.progress = 30 + int(pct * 0.4)

            output_file = await asyncio.to_thread(
                runner.run, job.job_id, job.template_id, job.props, progress_cb
            )

            # ── Post-processing ───────────────────────────────────────────
            job.status = JobStatus.postprocessing
            job.progress = 75
            await repo.update(job)

            # ── Uploading ─────────────────────────────────────────────────
            job.status = JobStatus.uploading
            job.progress = 90
            await repo.update(job)

            object_key = f"{job.template_id}/{job.job_id}.mp4"
            await asyncio.to_thread(storage.put_file, output_file, object_key)
            job.output_url = storage.get_signed_url(
                object_key, expires_in=settings.signed_url_expires_seconds
            )

            # ── Completed ─────────────────────────────────────────────────
            job.status = JobStatus.completed
            job.progress = 100
            job.completed_at = datetime.now(timezone.utc)
            await repo.update(job)

            log.info("worker.job_completed", output_url=job.output_url)
            return {"status": "completed", "output_url": job.output_url}

        except RenderError as exc:
            log.error("worker.render_error", error_code=exc.code, message=exc.message)
            job.status = JobStatus.failed
            job.error_code = exc.code
            job.error_message = exc.message
            job.retry_count = attempt - 1
            await repo.update(job)
            # Raise so arq knows to retry (up to max_tries)
            raise

        except Exception as exc:
            log.exception("worker.unexpected_error")
            job.status = JobStatus.failed
            job.error_code = "UNEXPECTED_ERROR"
            job.error_message = str(exc)[:512]
            job.retry_count = attempt - 1
            await repo.update(job)
            raise


def _validate_props(job: RenderJob) -> None:
    """
    Dynamically imports and runs the template-specific Pydantic validator.
    Schema modules live in app/schemas/<template_id>.py.
    """
    try:
        module = importlib.import_module(f"app.schemas.{job.template_id}")
        schema_cls = getattr(module, "PropsSchema")
        schema_cls.model_validate(job.props)
    except ModuleNotFoundError:
        # No schema module means no validation (pass-through)
        pass
    except Exception as exc:
        raise RenderError("SCHEMA_VALIDATION_ERROR", str(exc)) from exc


# ── Worker settings ───────────────────────────────────────────────────────────

class WorkerSettings:
    functions = [run_render_job]
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    queue_name = "renders:p5"
    max_jobs = settings.worker_max_jobs
    job_timeout = settings.worker_job_timeout_seconds
    max_tries = settings.worker_max_tries
    # arq doubles the retry delay on each attempt
    retry_jobs = True
    # Keep result data in Redis for 1 hour after completion
    keep_result = 3600
    # Log each job start/end
    log_results = True


if __name__ == "__main__":
    from arq import run_worker
    run_worker(WorkerSettings)
