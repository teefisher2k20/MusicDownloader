# Composition Registry and Contracts

## Purpose

Standardize how Remotion compositions are declared, versioned, and validated.

## Hero Template (Phase 1)

- Template ID: `release_trailer`
- Initial Composition ID: `ReleaseTrailerV1`
- Status: single-template production candidate

## Registry Rules

- Every template maps to one canonical composition ID and version.
- Template versions are immutable after release.
- New visual behavior requires new template version.

## Props Contract Rules

- Validate props using template-specific Pydantic schemas in `app/schemas/*`.
- Keep strict required/optional separation.
- Include explicit defaults in schema, not only in UI/client payloads.

## Suggested Registry Shape

- `template_id`
- `template_version`
- `composition_id`
- `fps`
- `width`
- `height`
- `default_duration_in_frames`
- `schema_module`

## Mapping to Existing Modules

- Validation path:
  - `app/worker.py#_validate_props`
  - `app/schemas/release_trailer.py`
- Runner path:
  - `app/runner.py#RenderRunner.run`

## Multi-Ratio Expansion (Phase 2)

- Introduce render profiles:
  - `widescreen_1080p` => `1920x1080`
  - `vertical_1080x1920`
  - `square_1080`
- Keep same content props, apply profile-specific layout transforms.

## Versioning Policy

- Patch: backward-compatible schema defaults.
- Minor: non-breaking new optional props.
- Major: breaking prop contract or timing semantics.
