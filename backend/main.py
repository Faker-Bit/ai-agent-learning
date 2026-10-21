from __future__ import annotations

"""Uvicorn entrypoint: `python -m uvicorn main:app --reload` from `backend/`."""

from app.main import app

__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn

    from app.core.config import get_settings

    cfg = get_settings()
    uvicorn.run(
        "main:app",
        host=cfg.amt_host,
        port=cfg.amt_port,
        reload=not cfg.is_production,
    )
