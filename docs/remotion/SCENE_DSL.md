# Scene DSL (Initial Spec)

## Purpose

Define a portable scene graph format that can be compiled into Remotion input props.

## Design Goals

- Human-editable JSON shape.
- Strict validation before enqueue.
- Stable enough for agent-to-agent handoff.

## Root Object

- `video`
  - `template_id`: string
  - `template_version`: string
  - `duration_in_frames`: integer
  - `fps`: integer
  - `profile`: string (`widescreen_1080p`, `vertical_1080x1920`, `square_1080`)
- `tracks`: array of track objects
- `meta`: object for campaign and tenant metadata

## Track Types

1. `title`
2. `subtitle`
3. `voiceover`
4. `music`
5. `broll`
6. `captions`
7. `cta`

## Common Track Fields

- `id`: string
- `type`: string
- `start`: integer frame
- `end`: integer frame
- `z_index`: integer
- `style`: object
- `payload`: object

## Example Semantics

- `title.payload.text`: headline text
- `voiceover.payload.audio_url`: URL to voice asset
- `captions.payload.segments`: array of `{start, end, text}`

## Compiler Responsibilities

- Validate timeline overlap constraints for exclusive tracks.
- Resolve missing durations from source assets when available.
- Clamp all track bounds to `duration_in_frames`.
- Output final Remotion props object expected by composition.

## Mapping to Existing Modules

- Future compiler module:
  - `app/scene_compiler.py` (planned)
- Current integration points:
  - `app/routes.py#create_render`
  - `app/worker.py#_validate_props`
  - `app/runner.py#RenderRunner.run`

## Migration Strategy

1. Keep current `props` input as-is for compatibility.
2. Accept optional `scene_dsl` payload in API.
3. If `scene_dsl` exists, compile to `props` before enqueue.
4. Persist both for auditability.
