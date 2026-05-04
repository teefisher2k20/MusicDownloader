"""API route tests."""

import pytest
from datetime import datetime, timezone

from app.models import JobStatus
from app.repository import PostgresJobRepository

API_KEY = "changeme"  # matches config.py default: api_key_secret = "changeme"
AUTH_HEADERS = {"X-API-Key": API_KEY}

SALES_PROPS = {
    "account_name": "Acme Corp",
    "persona_title": "VP of Engineering",
    "pain_point": "Pipelines are slow.",
    "proof_point": {"metric": "43%", "source": "G2"},
    "cta_text": "Book a demo",
    "duration_seconds": 30,
    "aspect_ratio": "16:9",
    "brand": {"primary_color": "#2563EB"},
}


def _render_payload(idempotency_key: str, props: dict = SALES_PROPS) -> dict:
    return {
        "template_id": "sales_personalization",
        "template_version": "v1",
        "priority": 5,
        "idempotency_key": idempotency_key,
        "props": props,
    }


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_render_happy_path(client, monkeypatch):
    # Monkeypatch enqueue so the test doesn't need a real Redis connection
    async def _noop_enqueue(job_id: str, priority: int):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    r = await client.post("/v1/renders", json=_render_payload("idem-key-1"), headers=AUTH_HEADERS)
    assert r.status_code == 202
    body = r.json()
    assert "job_id" in body
    assert body["status"] == "queued"


@pytest.mark.asyncio
async def test_create_render_idempotency(client, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    payload = _render_payload("idem-key-dup")
    r1 = await client.post("/v1/renders", json=payload, headers=AUTH_HEADERS)
    r2 = await client.post("/v1/renders", json=payload, headers=AUTH_HEADERS)
    assert r1.status_code == 202
    assert r2.status_code == 202
    assert r1.json()["job_id"] == r2.json()["job_id"]


@pytest.mark.asyncio
async def test_create_render_unauthorized(client):
    r = await client.post("/v1/renders", json=_render_payload("idem-no-auth"))
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_render_not_found(client):
    r = await client.get("/v1/renders/nonexistent-id", headers=AUTH_HEADERS)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_render_found(client, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-get-test"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]

    get_r = await client.get(f"/v1/renders/{job_id}", headers=AUTH_HEADERS)
    assert get_r.status_code == 200
    assert get_r.json()["job_id"] == job_id


@pytest.mark.asyncio
async def test_list_renders_empty(client):
    r = await client.get("/v1/renders", headers=AUTH_HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["items"] == []
    assert body["total"] == 0


@pytest.mark.asyncio
async def test_cancel_render_not_found(client):
    r = await client.delete("/v1/renders/no-such-job", headers=AUTH_HEADERS)
    assert r.status_code == 404


async def _mark_completed(db_session, job_id: str) -> None:
    repo = PostgresJobRepository(db_session)
    job = await repo.get(job_id)
    assert job is not None
    job.status = JobStatus.completed
    job.progress = 100
    job.output_url = "https://cdn.example.com/renders/final.mp4"
    job.completed_at = datetime.now(timezone.utc)
    await repo.update(job)


@pytest.mark.asyncio
async def test_playlist_action_requires_completion(client, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-playlist-precomplete"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]

    action_r = await client.post(
        f"/v1/renders/{job_id}/playlist",
        json={"action": "download", "playlist_name": "Weekly Launches"},
        headers=AUTH_HEADERS,
    )
    assert action_r.status_code == 409


@pytest.mark.asyncio
async def test_playlist_action_after_completion(client, db_session, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-playlist-complete"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]
    await _mark_completed(db_session, job_id)

    action_r = await client.post(
        f"/v1/renders/{job_id}/playlist",
        json={
            "action": "deploy",
            "playlist_name": "Weekly Launches",
            "destination": "roku-living-room",
        },
        headers=AUTH_HEADERS,
    )
    assert action_r.status_code == 202
    body = action_r.json()
    assert body["job_id"] == job_id
    assert body["playlist_name"] == "Weekly Launches"
    assert body["actions"][0]["action"] == "deploy"
    assert body["actions"][0]["destination"] == "roku-living-room"


@pytest.mark.asyncio
async def test_get_playlist_actions(client, db_session, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-playlist-read"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]
    await _mark_completed(db_session, job_id)

    await client.post(
        f"/v1/renders/{job_id}/playlist",
        json={"action": "listen", "playlist_name": "Audio Queue", "destination": "podcast-app"},
        headers=AUTH_HEADERS,
    )

    get_r = await client.get(f"/v1/renders/{job_id}/playlist", headers=AUTH_HEADERS)
    assert get_r.status_code == 200
    body = get_r.json()
    assert body["job_id"] == job_id
    assert body["actions"][0]["action"] == "listen"
    assert body["actions"][0]["playlist_name"] == "Audio Queue"


@pytest.mark.asyncio
async def test_delete_playlist_action(client, db_session, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-playlist-delete"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]
    await _mark_completed(db_session, job_id)

    action_r = await client.post(
        f"/v1/renders/{job_id}/playlist",
        json={"action": "share", "playlist_name": "Team Feed", "destination": "slack-channel"},
        headers=AUTH_HEADERS,
    )
    assert action_r.status_code == 202
    action_id = action_r.json()["actions"][0]["action_id"]

    delete_r = await client.delete(
        f"/v1/renders/{job_id}/playlist/{action_id}", headers=AUTH_HEADERS
    )
    assert delete_r.status_code == 204

    get_r = await client.get(f"/v1/renders/{job_id}/playlist", headers=AUTH_HEADERS)
    assert get_r.json()["actions"] == []


@pytest.mark.asyncio
async def test_delete_playlist_action_not_found(client, db_session, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-playlist-del-404"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]

    r = await client.delete(
        f"/v1/renders/{job_id}/playlist/nonexistent-uuid", headers=AUTH_HEADERS
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_completed_at_present_in_status_response(client, db_session, monkeypatch):
    async def _noop_enqueue(job_id, priority):
        return None

    monkeypatch.setattr("app.routes.enqueue_render", _noop_enqueue)

    create_r = await client.post(
        "/v1/renders", json=_render_payload("idem-completed-at"), headers=AUTH_HEADERS
    )
    job_id = create_r.json()["job_id"]
    await _mark_completed(db_session, job_id)

    get_r = await client.get(f"/v1/renders/{job_id}", headers=AUTH_HEADERS)
    assert get_r.status_code == 200
    body = get_r.json()
    assert body["completed_at"] is not None
