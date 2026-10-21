from __future__ import annotations

import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import get_settings


class RateLimiter:
    """Simple fixed-window in-memory limiter (single-process local app)."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str) -> bool:
        now = time.monotonic()
        window_start = now - self.window
        hits = [t for t in self._hits[key] if t > window_start]
        if len(hits) >= self.max_requests:
            self._hits[key] = hits
            return False
        hits.append(now)
        self._hits[key] = hits
        return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: RateLimiter) -> None:
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ("/api/health", "/api/ready", "/docs", "/openapi.json"):
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        if not self.limiter.check(client):
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limited",
                        "message": "Too many requests. Slow down.",
                        "details": {},
                    }
                },
            )
        return await call_next(request)


def build_limiter() -> RateLimiter:
    s = get_settings()
    return RateLimiter(s.amt_rate_limit_requests, s.amt_rate_limit_window_seconds)
