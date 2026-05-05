# Integration Contracts

## Purpose

Document external integrations and simulation/live behavior for safe rollout.

## Integration Matrix

1. Remotion renderer (Node subprocess)
2. Redis queue (ARQ)
3. PostgreSQL persistence
4. Object storage backend
5. Optional AI services (captions, voice, b-roll, script)

## Required Runtime Vars

- `DATABASE_URL`
- `REDIS_URL`
- `API_KEY_SECRET`
- `STORAGE_BACKEND`
- Storage credentials for selected backend

## Simulation vs Live Modes

- Phase A:
  - Keep non-render AI integrations optional or simulated.
  - Real rendering path must be live.
- Phase B+:
  - Add integration capability flags and observability per integration.

## Timeout and Retry Contracts

- API request timeout should not include render duration.
- Worker handles long-running render timeouts via `worker_job_timeout_seconds`.
- Retries limited by `worker_max_tries`.

## Error Taxonomy (Initial)

- `SCHEMA_VALIDATION_ERROR`
- `COMPOSITION_NOT_FOUND`
- `OUT_OF_MEMORY`
- `RENDER_TIMEOUT`
- `HEAP_EXHAUSTED`
- `ASSET_NOT_FOUND`
- `OUTPUT_MISSING`
- `RENDER_FAILURE`

## Mapping to Existing Modules

- Env/config: `app/config.py`
- Queue setup: `app/worker.py`, `app/queue_service.py`
- Error mapping: `app/runner.py`
- Storage + signed URL: `app/storage.py`

## Security Notes

- API key required for render mutation endpoints.
- Never store secret tokens in playlist action payloads.
- Use signed URLs with bounded expiry.
