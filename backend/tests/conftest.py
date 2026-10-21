from __future__ import annotations

import os
import pathlib
import tempfile

import httpx
import pytest
import pytest_asyncio

TMP_DIR = pathlib.Path(tempfile.gettempdir()) / "amt_tests"
TMP_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("AMT_ENV", "test")
os.environ.setdefault("AMT_DEBUG", "false")

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
