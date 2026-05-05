# Remotion Architecture (Plan A First)

## Purpose

This document defines the target architecture for integrating real Remotion rendering into the Video Orchestration Platform while shipping quickly with one hero template: `release_trailer`.

## Scope

- In scope:
  - Replace placeholder render flow with real Remotion execution.
  - Support one hero composition (`release_trailer`) end-to-end.
  - Add agent-oriented planning boundaries to avoid architecture drift.
  - Stabilize single-template rendering before bulk and multi-ratio rollout.
- Out of scope (Phase 1):
  - Multi-template authoring UI.
  - Full publish adapter matrix.
  - Advanced optimization and autoscaling policies.

## Existing Modules (Current System)

- API ingress: `app/routes.py`
- App lifecycle + health: `app/main.py`
- Queue submit: `app/queue_service.py`
- Worker orchestration: `app/worker.py`
- Render subprocess runner: `app/runner.py`
- Persistence/repository: `app/repository.py`
- Data models/schemas: `app/models.py`, `app/database.py`, `app/schemas/*`
- Artifact storage abstraction: `app/storage.py`

## Target Runtime Flow

1. Client calls `POST /v1/renders` with `template_id=release_trailer`.
2. API validates idempotency and stores job record.
3. API enqueues render job on `renders:p5` via ARQ.
4. Worker validates props schema and transitions job states.
5. Runner calls Node Remotion renderer with composition + props.
6. Produced MP4 is uploaded via storage adapter.
7. Signed URL is generated and persisted.
8. Job is marked `completed` with `completed_at`.

## Control Plane and Data Plane

- Control plane:
  - FastAPI endpoints, DB status updates, queueing, idempotency, auth.
- Data plane:
  - Node Remotion render process, temporary files, final MP4 upload.

## Agent Boundaries

- Intake Agent (API boundary): request normalization, idempotency check.
- Timeline Agent (planning boundary): map high-level payload to scene input props.
- Render Orchestrator Agent (worker boundary): execute state machine and retries.
- QA Agent (post-render boundary): enforce quality gates before playlist/distribution.

## State Machine (Phase 1)

- `queued`
- `validating`
- `preparing`
- `rendering`
- `postprocessing`
- `uploading`
- `completed`
- `failed`
- `canceled`

## Phase 2 Additions (after stable hero template)

- Bulk job graph (parent + child jobs)
- Multi-ratio profiles (`16:9`, `9:16`, `1:1`)
- QA gate transitions (`qa_pending`, `qa_failed`, `qa_passed`)

## Concrete Task Breakdown Mapped to Existing Modules

1. Real Remotion render path in `app/runner.py`
   - Replace placeholder assumptions with composition-aware Node command contract.
   - Parse structured stderr/stdout markers for better error mapping.
2. Hero template schema hardening in `app/schemas/release_trailer.py`
   - Enforce required fields and safe defaults for first production composition.
3. API contract extension in `app/models.py` and `app/routes.py`
   - Add optional render profile fields (future-proof for multi-ratio).
4. Worker state + retries in `app/worker.py`
   - Preserve deterministic state transitions and retry metadata.
5. Persist render metadata in `app/database.py` and `app/repository.py`
   - Add fields for rendition profile and QA summary in phase 2.
6. Storage and signed URL policy in `app/storage.py`
   - Ensure output naming supports parent/child bulk lineage.
7. Playlist/distribution safety in `app/routes.py`
   - Restrict downstream actions until render and QA gates pass.

## Deployment Notes

- Render and Railway both supported via `render.yaml` and `railway.toml`.
- Production should use non-local object storage backend.
- Keep API and worker as separate services in deployment topology.
