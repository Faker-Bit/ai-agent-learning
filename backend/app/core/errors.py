from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class SiteError(Exception):
    """Base application error with a stable machine code."""

    def __init__(
        self,
        message: str,
        code: str = "site_error",
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class ProviderError(SiteError):
    def __init__(self, message: str, provider: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            code=f"provider_{provider}_error",
            status_code=502,
            details={"provider": provider, **(details or {})},
        )


class ProviderAuthError(SiteError):
    def __init__(self, provider: str, hint: str = ""):
        msg = f"Missing or invalid API key for {provider}."
        if hint:
            msg += f" {hint}"
        super().__init__(msg, code=f"provider_{provider}_auth", status_code=401, details={"provider": provider})


class NoProviderError(SiteError):
    def __init__(self, message: str = "No AI provider is configured yet."):
        super().__init__(message, code="no_provider", status_code=409, details={"provider": ""})


class RateLimitError(SiteError):
    def __init__(self, message: str = "Too many requests. Slow down."):
        super().__init__(message, code="rate_limited", status_code=429)


class NotFoundError(SiteError):
    def __init__(self, message: str = "Resource not found."):
        super().__init__(message, code="not_found", status_code=404)


class SandboxViolation(SiteError):
    def __init__(self, message: str):
        super().__init__(message, code="sandbox_violation", status_code=400)


async def site_error_handler(request: Request, exc: SiteError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
    )
