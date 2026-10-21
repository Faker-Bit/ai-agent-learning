"""Export the site content to a JSON file the frontend can bundle.

This lets the website render even when the API is not running (static hosting,
offline demo, or a stale server on the port).

    python tools/export_content.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))

from app.api.routes.site import build_payload  # noqa: E402

TARGET = BACKEND.parent / "frontend" / "src" / "content" / "site.json"


def main() -> int:
    payload = asyncio.run(build_payload())
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    size_kb = TARGET.stat().st_size / 1024
    print(
        f"exported {len(payload['agents'])} agents, "
        f"{len(payload['walkthroughs'])} walkthroughs, "
        f"{len(payload['cheatsheet'])} commands -> {TARGET} ({size_kb:.0f} KB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
