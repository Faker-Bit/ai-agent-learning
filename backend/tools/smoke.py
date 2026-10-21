"""End-to-end smoke test: boots the real server and exercises the API."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx

BACKEND = Path(__file__).resolve().parent.parent
PORT = 8099
BASE = f"http://127.0.0.1:{PORT}"


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(BACKEND),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    logs: list[str] = []

    def drain() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            logs.append(line.rstrip())

    threading.Thread(target=drain, daemon=True).start()

    try:
        ready = False
        for _ in range(60):
            time.sleep(0.5)
            try:
                if httpx.get(f"{BASE}/api/health", timeout=2).status_code == 200:
                    ready = True
                    break
            except Exception:
                continue
        if not ready:
            print("SERVER DID NOT START", flush=True)
            print("\n".join(logs[-40:]), flush=True)
            return 1

        failures: list[str] = []

        def check(name: str, condition: bool, detail: str = "") -> None:
            status = "PASS" if condition else "FAIL"
            extra = f" - {detail}" if detail and not condition else ""
            print(f"[{status}] {name}{extra}", flush=True)
            if not condition:
                failures.append(name)

        health = httpx.get(f"{BASE}/api/health", timeout=5).json()
        check("health", health["status"] == "ok")

        site = httpx.get(f"{BASE}/api/site", timeout=10).json()
        check("agents listed", len(site["agents"]) >= 25, str(len(site["agents"])))
        check("walkthroughs listed", len(site["walkthroughs"]) >= 9, str(len(site["walkthroughs"])))
        check("cheatsheet rows", len(site["cheatsheet"]) >= 120, str(len(site["cheatsheet"])))
        check("loop stages", len(site["loop_stages"]) == 6)
        check("craft rules", len(site["craft"]) >= 6)
        check("model guides", len(site["model_guide"]) >= 7)
        check("config snippets", len(site["config_snippets"]) >= 4)
        check("comparison matrix", len(site["comparison"]) >= 8)
        check("providers", len(site["providers"]) >= 15)
        check("models", len(site["models"]) >= 40)
        check("harness layers", len(site["harness_layers"]) == 7)
        check("harness projects", len(site["harness_projects"]) >= 6)
        check("skill packages", len(site["skill_packages"]) >= 8)
        check("orchestrators", len(site["orchestrators"]) >= 6)
        check("protocols", len(site["protocols"]) >= 5)
        check("context playbook", len(site["context_playbook"]) >= 4)
        check("skills walkthrough", any(w["id"] == "opencode-skills" for w in site["walkthroughs"]))

        check(
            "walkthrough steps have narration",
            all(step["narration"] and step["lines"] for step in site["walkthroughs"][0]["steps"]),
        )
        check(
            "agent install commands present",
            all(agent["install"] and agent["highlights"] for agent in site["agents"]),
        )
        check(
            "free models present",
            len([m for m in site["models"] if m["free"]]) >= 20,
        )

        index = httpx.get(f"{BASE}/", timeout=5)
        if index.status_code == 200:
            check("spa served", "Agent Pilot" in index.text)
        else:
            print("[SKIP] frontend/dist not built", flush=True)

        deep = httpx.get(f"{BASE}/walkthrough/opencode-first-hour", timeout=5)
        check("spa deep link fallback", deep.status_code == 200 and "Agent Pilot" in deep.text)

        missing_api = httpx.get(f"{BASE}/api/does-not-exist", timeout=5)
        check("unknown api route 404s", missing_api.status_code == 404)

        # The bundled copy must match the API so the site renders offline too.
        bundled_path = BACKEND.parent / "frontend" / "src" / "content" / "site.json"
        if bundled_path.exists():
            bundled = json.loads(bundled_path.read_text(encoding="utf-8"))
            check("bundled copy matches api", len(bundled["agents"]) == len(site["agents"]))
        else:
            check("bundled copy present", False, "run tools/export_content.py")

        dist = BACKEND.parent / "frontend" / "dist"
        if dist.exists():
            bundle_text = ""
            for asset in dist.glob("assets/*.js"):
                bundle_text += asset.read_text(encoding="utf-8", errors="ignore")
            check("offline copy bundled", "OpenCode Zen" in bundle_text)
        else:
            print("[SKIP] frontend/dist not built", flush=True)

        print(flush=True)
        if failures:
            print(f"{len(failures)} FAILURES: {failures}", flush=True)
            return 1
        print("ALL CHECKS PASSED", flush=True)
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
