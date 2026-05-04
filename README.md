# Video Orchestration Platform

## Prerequisites

- Docker Desktop (running)
- Node.js 20+ (for `render.js`; a development stub is included)
- Python 3.12+ (for running tests locally without Docker)

## Quick start (Docker)

```bash
# 1. Copy environment file and set your API key
cp .env.example .env
# Edit .env — set API_KEY_SECRET to a strong random string

# 2. Build and start all services (postgres, redis, migrate, api, worker)
docker compose up --build -d

# 3. Verify the API is healthy
curl http://localhost:8000/health
```

The `migrate` service runs `alembic upgrade head` and exits before the `api`
and `worker` services start.

## Running tests locally

```bash
pip install -r requirements-dev.txt
pytest --cov=app --cov-report=term-missing
```

## Replacing the render.js stub

`render.js` in the project root is a minimal stub that writes a placeholder MP4
so the full worker pipeline can run end-to-end during development. In production,
replace it with a real [Remotion](https://www.remotion.dev/) render harness:

```bash
# Install Remotion
npm install @remotion/renderer

# Then update render.js to call the Remotion CLI or use the Node API
```

## Usage: Completion to Playlist Flow

Use this sequence for post-completion distribution actions:

1. Submit render
2. Poll until status is `completed`
3. Queue a playlist action (`listen`, `export`, `download`, `share`, or `deploy`)
4. Fetch all queued actions — or delete one by `action_id`

> **Note:** Playlist actions are stored and returned by the API, but the actual
> dispatch work (e.g. pushing to a streaming device, uploading to a platform)
> must be wired up to your own integration layer. The `status` field will read
> `"queued"` until you implement a background processor that marks actions
> `"processing"` / `"done"` / `"failed"`.

### Example requests

Set variables:

- `BASE_URL=http://localhost:8000`
- `API_KEY=changeme`

Submit render:

```bash
curl -X POST "$BASE_URL/v1/renders" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "sales_personalization",
    "template_version": "v1",
    "priority": 5,
    "idempotency_key": "demo-sequence-001",
    "props": {
      "account_name": "Acme Corp",
      "persona_title": "VP of Engineering",
      "pain_point": "Manual release pipelines are slow.",
      "proof_point": {"metric": "43% faster deploys", "source": "G2"},
      "cta_text": "Book a demo",
      "duration_seconds": 30,
      "aspect_ratio": "16:9",
      "brand": {"primary_color": "#2563EB"}
    }
  }'
```

Poll until completed (replace `<job_id>` from the submit response):

```bash
curl -X GET "$BASE_URL/v1/renders/<job_id>" \
  -H "X-API-Key: $API_KEY"
```

Queue playlist action after completion:

```bash
curl -X POST "$BASE_URL/v1/renders/<job_id>/playlist" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "deploy",
    "playlist_name": "Living Room Screens",
    "destination": "roku-living-room"
  }'
```

Fetch playlist actions:

```bash
curl -X GET "$BASE_URL/v1/renders/<job_id>/playlist" \
  -H "X-API-Key: $API_KEY"
```

Remove a specific playlist action:

```bash
curl -X DELETE "$BASE_URL/v1/renders/<job_id>/playlist/<action_id>" \
  -H "X-API-Key: $API_KEY"
```
