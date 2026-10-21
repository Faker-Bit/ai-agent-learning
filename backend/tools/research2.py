"""Second research pass: topic-scoped and name/description-scoped searches."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import httpx

from research import extract_example, extract_install, load_token, readme, headers

TARGET = Path(__file__).resolve().parent.parent / "app" / "content" / "_research.json"

SEARCHES: list[tuple[str, str]] = [
    ("jailbreak", "topic:jailbreak"),
    ("jailbreak", "jailbreak in:name,description"),
    ("jailbreak", "jailbreak chatbot in:name,description"),
    ("prompt-injection", "topic:prompt-injection"),
    ("prompt-injection", "prompt injection in:name,description"),
    ("llm-red-team", "red team llm in:name,description"),
    ("llm-red-team", "topic:red-teaming"),
    ("llm-red-team", "adversarial prompts llm in:name,description"),
    ("llm-security", "topic:llm-security"),
    ("llm-security", "llm security scanner in:name,description"),
    ("llm-security", "topic:ai-security"),
    ("guardrails", "topic:guardrails"),
    ("guardrails", "guardrails in:name,description"),
    ("ai-evaluation", "topic:llm-evaluation"),
    ("ai-evaluation", "promptfoo in:name,description"),
    ("prompt-engineering", "topic:prompt-engineering"),
    ("prompt-engineering", "prompt engineering in:name,description"),
    ("prompt-templates", "topic:prompt-library"),
    ("agent-skills", "topic:agent-skills"),
    ("agent-skills", "claude skills in:name,description"),
    ("context-engineering", "context engineering in:name,description"),
    ("model-servers", "topic:llm-serving"),
    ("chat-uis", "topic:llm-ui"),
    ("chat-uis", "chatgpt webui in:name,description"),
    ("tokenizers", "tiktoken in:name,description"),
    ("ai-education", "topic:ai-education"),
    ("ai-education", "llm course tutorial in:name,description"),
    ("model-providers", "qwen code in:name,description"),
    ("model-providers", "deepseek in:name,description"),
    ("model-providers", "grok in:name,description"),
    ("model-providers", "llm api client in:name,description"),
]

SKIP = {"Jupyter Notebook", "", "TeX"}


def main() -> int:
    token = load_token()
    head = headers(token)
    payload = json.loads(TARGET.read_text(encoding="utf-8"))
    repos: dict[str, dict[str, Any]] = {r["full_name"]: r for r in payload["repos"]}

    with httpx.Client(
        base_url="https://api.github.com", headers=head, timeout=30, follow_redirects=True
    ) as client:
        for category, query in SEARCHES:
            resp = client.get(
                "/search/repositories",
                params={"q": query, "sort": "stars", "order": "desc", "per_page": 25},
            )
            if resp.status_code != 200:
                print(f"  fail {resp.status_code} {query}")
                time.sleep(3)
                continue
            items = resp.json().get("items", [])
            kept = 0
            for repo in items:
                if repo.get("archived") or repo.get("fork"):
                    continue
                if repo.get("language") in SKIP:
                    continue
                if repo.get("stargazers_count", 0) < 60:
                    continue
                full = repo["full_name"]
                entry = repos.get(full)
                if entry is None:
                    entry = {
                        "full_name": full,
                        "stars": repo.get("stargazers_count", 0),
                        "description": repo.get("description") or "",
                        "topics": repo.get("topics") or [],
                        "language": repo.get("language") or "",
                        "license": (repo.get("license") or {}).get("spdx_id") or "",
                        "pushed_at": (repo.get("pushed_at") or "")[:10],
                        "url": repo.get("html_url", f"https://github.com/{full}"),
                        "homepage": repo.get("homepage") or "",
                        "categories": [],
                        "install": "",
                        "example": [],
                    }
                    repos[full] = entry
                if category not in entry["categories"]:
                    entry["categories"].append(category)
                kept += 1
            print(f"{category:<22} {query:<45} -> {kept}")
            time.sleep(2.2)

    print("fetching readmes for new repos")
    new = [
        r
        for r in repos.values()
        if not r.get("install") and not r.get("example") and r.get("stars", 0) >= 120
    ]
    with httpx.Client(headers=head, timeout=20, follow_redirects=True) as raw:
        for index, entry in enumerate(new):
            if index % 25 == 0:
                print(f"  {index}/{len(new)}")
            text = readme(raw, entry["full_name"], "HEAD")
            entry["install"] = extract_install(text)
            entry["example"] = extract_example(text)[:6]
            time.sleep(0.1)

    payload["repos"] = sorted(repos.values(), key=lambda r: -r["stars"])
    payload["generated"] = time.strftime("%Y-%m-%d")
    TARGET.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"total repos: {len(payload['repos'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
