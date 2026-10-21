from __future__ import annotations

import httpx
import pytest


async def test_health(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["service"] == "agent-pilot-backend"


async def test_ready(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"
