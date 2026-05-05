# Operations Runbook

## Purpose

Provide day-1 and day-2 operational procedures for Remotion rendering.

## Day-1 Bring-Up

1. Set required env vars:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `API_KEY_SECRET`
2. Run DB migrations:
   - `alembic upgrade head`
3. Start API service.
4. Start worker service.
5. Verify health endpoint and test render submission.

## Core Health Signals

- API health: `/health`
- Queue depth (Redis key metrics)
- Worker job completion rate
- Render failure rate by error code
- Artifact upload success rate

## Incident Playbooks

### 1) Jobs stuck in queued

- Check Redis connectivity.
- Verify worker process is running.
- Confirm queue name matches (`renders:p5`).

### 2) Jobs fail in rendering

- Inspect stderr-derived `error_code` in DB.
- Confirm Node/Remotion runtime is installed in image.
- Re-run with same props locally for deterministic repro.

### 3) Output URL missing

- Check storage adapter credentials.
- Verify upload path permissions.
- Confirm signed URL generation path.

## Safe Replay Procedure

1. Identify failed job IDs and root cause class.
2. For transient errors only, re-enqueue same `job_id` with bounded retries.
3. For schema errors, reject replay until payload corrected.

## Deployment Notes

- Render deployment uses `render.yaml`.
- Railway alternative uses `railway.toml` for API and separate worker service.

## Ownership Matrix

- API contracts: `app/routes.py`, `app/models.py`
- Worker lifecycle: `app/worker.py`
- Render subprocess: `app/runner.py`
- Storage and URLs: `app/storage.py`
- Data persistence: `app/repository.py`, `app/database.py`
