# Agent Design for Remotion Pipeline

## Purpose

Define stable agent boundaries and handoff contracts so new features do not create architecture drift.

## Agent Topology (Initial)

1. Intake Agent
2. Timeline Agent
3. Render Orchestrator Agent
4. QA Agent
5. Distribution Agent

## 1) Intake Agent

- Responsibility:
  - Accept render requests and normalize payloads.
  - Validate API key and idempotency key usage.
- Inputs:
  - `RenderCreateRequest` from `POST /v1/renders`.
- Outputs:
  - Canonical render request persisted as job row.
- Existing module mapping:
  - `app/routes.py#create_render`
  - `app/models.py#RenderCreateRequest`

## 2) Timeline Agent

- Responsibility:
  - Convert high-level request into scene graph compatible props.
  - Apply hero-template defaults for `release_trailer`.
- Inputs:
  - Canonical request payload.
  - Template schema rules.
- Outputs:
  - `props` object for Remotion composition.
- Existing module mapping:
  - `app/schemas/release_trailer.py`
  - `app/worker.py#_validate_props`
- Planned module additions:
  - `app/scene_compiler.py` (future)

## 3) Render Orchestrator Agent

- Responsibility:
  - Execute render state machine and retry behavior.
  - Manage render subprocess and output artifact path.
- Inputs:
  - `job_id`
  - validated props
- Outputs:
  - output file path, storage object key, signed URL
- Existing module mapping:
  - `app/worker.py#run_render_job`
  - `app/runner.py#RenderRunner.run`
  - `app/storage.py`

## 4) QA Agent

- Responsibility:
  - Run post-render checks and generate QA summary.
  - Block publish/distribution if hard rules fail.
- Inputs:
  - rendered MP4
  - expected template constraints
- Outputs:
  - QA summary object and decision (`pass` or `fail`)
- Existing module mapping:
  - New logic to be added in `app/worker.py` post-render path
  - Persist via `app/repository.py`

## 5) Distribution Agent

- Responsibility:
  - Execute playlist actions only for completed and QA-passed jobs.
- Inputs:
  - playlist action records
  - render readiness and QA status
- Outputs:
  - queueable channel-specific distribution tasks
- Existing module mapping:
  - `app/routes.py#queue_playlist_action`
  - `app/routes.py#delete_playlist_action`

## Handoff Contracts

- Intake -> Timeline:
  - `{job_id, template_id, template_version, props, priority}`
- Timeline -> Orchestrator:
  - `{job_id, composition_id, input_props, render_profile}`
- Orchestrator -> QA:
  - `{job_id, output_file, output_url, duration_hint}`
- QA -> Distribution:
  - `{job_id, qa_status, qa_summary, output_url}`

## Retry and Idempotency Rules

- API idempotency at intake via `idempotency_key`.
- Worker retries only for transient render failures.
- Distribution must be deduplicated by action ID.

## Rollout Strategy

1. Implement only Intake + Timeline + Orchestrator for `release_trailer`.
2. Add QA Agent checks after first stable real renders.
3. Add Distribution Agent hard-gating when QA status exists.
