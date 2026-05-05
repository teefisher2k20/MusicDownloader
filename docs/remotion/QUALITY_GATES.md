# Quality Gates for Render Pipeline

## Purpose

Define objective checks that determine if a render can proceed to playlist/distribution.

## Gate Levels

1. Blocking gates (must pass)
2. Advisory gates (warn but allow)

## Blocking Gates (Phase 2)

1. Render artifact exists and is readable.
2. Duration is within template tolerance.
3. Captions do not exceed frame bounds.
4. No fatal render errors in logs.
5. Output upload and signed URL generation succeed.

## Advisory Gates

1. Loudness outside preferred range.
2. Caption density too high per second.
3. CTA appears too late in timeline.
4. Visual-safe area overflow warnings.

## Gate Output Schema

- `qa_status`: `pass` or `fail`
- `blocking_failures`: array of strings
- `advisories`: array of strings
- `checked_at`: timestamp

## Mapping to Existing Modules

- Evaluate in worker after render:
  - `app/worker.py` (post-processing section)
- Persist result:
  - `app/repository.py`
  - `app/database.py` (new columns in future migration)
- Enforce distribution gating:
  - `app/routes.py#queue_playlist_action`

## Initial Rollout

1. Start with artifact-exists and upload-success checks.
2. Add caption and duration checks once Scene DSL is active.
3. Enforce hard block in playlist API after confidence period.
