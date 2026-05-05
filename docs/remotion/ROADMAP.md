# Remotion Roadmap

## Goal

Ship quickly with one real Remotion template, then scale to bulk/multi-ratio and QA-gated distribution.

## Phase A: Plan A MVP (Start Here)

- Target: one stable real render path using `release_trailer`.
- Deliverables:
  1. Real Remotion render execution in runner.
  2. Hero template schema hardened.
  3. End-to-end API -> queue -> worker -> storage success path.
  4. Basic remotion ideas UI page with working links.

## Phase B: Stability and Guardrails

- Target: prevent drift and improve reliability.
- Deliverables:
  1. AGENTS.md and SCENE_DSL.md contracts in active use.
  2. Structured error taxonomy and retry tuning.
  3. First QA checks in worker post-render.

## Phase C: Bulk and Multi-Ratio

- Target: campaign-grade throughput.
- Deliverables:
  1. Parent/child job graph for bulk render requests.
  2. Multi-ratio profile rendering (`16:9`, `9:16`, `1:1`).
  3. Artifact naming and lineage tracking.

## Phase D: QA-Gated Distribution

- Target: safe automated publishing.
- Deliverables:
  1. Blocking quality gates.
  2. Playlist API requires QA pass.
  3. Distribution adapters with per-channel constraints.

## Concrete Task Breakdown by Module

1. `app/routes.py`
   - Extend request model support for future render profiles.
   - Add read-only UI/ideas endpoint for discoverability.
2. `app/models.py`
   - Add optional fields for profile and QA metadata (phase B/C).
3. `app/worker.py`
   - Integrate QA gate execution before completed status finalization.
4. `app/runner.py`
   - Stabilize composition selection and structured error mapping.
5. `app/repository.py` and `app/database.py`
   - Persist profile, parent_job_id, qa_status, qa_summary.
6. `app/storage.py`
   - Ensure deterministic object keys across renditions.
7. `app/schemas/release_trailer.py`
   - Keep strict schema as hero-template contract.

## Exit Criteria

- Phase A complete when 20 consecutive `release_trailer` jobs finish successfully in target environment.
- Phase C complete when one request can produce 3 aspect-ratio outputs.
- Phase D complete when distribution blocks on QA fail and allows only QA pass.
