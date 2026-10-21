from __future__ import annotations

import time

from fastapi import APIRouter

router = APIRouter(tags=["health"])

START_TIME = time.time()


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "agent-pilot-backend",
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }


@router.get("/ready")
async def ready() -> dict:
    return {"status": "ready", "content": "ok"}
