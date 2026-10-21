from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, site
from app.core.config import get_settings
from app.core.errors import SiteError, site_error_handler
from app.core.logging import get_logger, setup_logging
from app.core.rate_limit import RateLimitMiddleware, build_limiter

log = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = get_settings()
    setup_logging(cfg.amt_debug)
    log.info("Agent Pilot backend started (env=%s)", cfg.amt_env)
    yield


def create_app() -> FastAPI:
    cfg = get_settings()
    app = FastAPI(
        title="Agent Pilot",
        version="1.0.0",
        description="Learn to drive AI coding agents: opencode, Zen, Codex, Claude Code, Gemini CLI, Aider and more.",
        lifespan=lifespan,
        docs_url="/docs" if not cfg.is_production else None,
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware, limiter=build_limiter())
    app.add_exception_handler(SiteError, site_error_handler)

    @app.exception_handler(Exception)
    async def unhandled(request: Request, exc: Exception):
        log.exception("unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error.",
                    "details": {},
                }
            },
        )

    app.include_router(health.router, prefix="/api")
    app.include_router(site.router, prefix="/api")
    app.include_router(site.resources_router, prefix="/api")

    _mount_frontend(app, cfg)
    return app


def _mount_frontend(app: FastAPI, cfg) -> None:
    """Serve the built SPA from the backend, with a fallback for client-side routes."""
    dist = cfg.project_root / "frontend" / "dist"
    if not dist.exists():
        return

    from fastapi import HTTPException
    from fastapi.responses import FileResponse

    index = dist / "index.html"
    dist_root = str(dist.resolve())

    media_types = {
        ".html": "text/html; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".ico": "image/x-icon",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".txt": "text/plain; charset=utf-8",
        ".webmanifest": "application/manifest+json",
    }

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        if full_path:
            candidate = (dist / full_path).resolve()
            if candidate.is_file() and str(candidate).startswith(dist_root):
                media_type = media_types.get(candidate.suffix.lower())
                return FileResponse(candidate, media_type=media_type)
        # Client-side route (e.g. /walkthrough/opencode-first-hour) -> index.html
        return FileResponse(index, media_type="text/html; charset=utf-8")


app = create_app()
