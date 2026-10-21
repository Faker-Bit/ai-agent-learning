"""Research the GitHub ecosystem for the Model Hub and the security section.

Runs a set of GitHub searches, pulls the README of every kept repo, extracts the
install command and a usage snippet, and writes backend/app/content/_research.json.

    python tools/research.py
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import httpx

OUT = Path(__file__).resolve().parent.parent / "app" / "content" / "_research.json"

SEARCHES: list[tuple[str, str]] = [
    ("prompt-engineering", "prompt engineering library in:name,description,readme"),
    ("prompt-templates", "prompt templates library in:name,description"),
    ("prompt-injection", "prompt injection in:name,description,readme"),
    ("jailbreak", "jailbreak llm in:name,description,readme"),
    ("llm-red-team", "llm red team fuzzing in:name,description,readme"),
    ("llm-security", "llm security scanner in:name,description,readme"),
    ("guardrails", "guardrails ai agents in:name,description,readme"),
    ("ai-evaluation", "llm evaluation eval harness in:name,description,readme"),
    ("agent-frameworks", "ai agent framework tools in:name,description"),
    ("model-servers", "llm inference server openai compatible in:name,description"),
    ("chat-uis", "chat ui llm web frontend in:name,description"),
    ("tokenizers", "tokenizer count tokens llm in:name,description"),
    ("prompt-libraries", "awesome prompts cheatsheet in:name,description"),
    ("model-providers", "chatgpt claude gemini deepseek qwen grok model in:name,description"),
    ("agent-skills", "agent skills claude opencode in:name,description,readme"),
    ("context-engineering", "context engineering agents in:name,description,readme"),
]

# Repos we want regardless of what the searches return.
FORCE_INCLUDE = [
    "anthropics/claude-code",
    "openai/codex",
    "google-gemini/gemini-cli",
    "anomalyco/opencode",
    "Aider-AI/aider",
    "cline/cline",
    "RooCodeInc/Roo-Code",
    "block/goose",
    "All-Hands-AI/OpenHands",
    "QwenLM/qwen-code",
    "deepseek-ai/DeepSeek-V3",
    "meta-llama/llama-models",
    "microsoft/generative-ai-for-beginners",
    "microsoft/ai-agents-for-beginners",
    "dair-ai/Prompt-Engineering-Guide",
    "f/awesome-chatgpt-prompts",
    "PlexPt/awesome-chatgpt-prompts-zh",
    "promptfoo/promptfoo",
    "NVIDIA/garak",
    "Azure/PyRIT",
    "centerforaisafety/HarmBench",
    "ethz-spylab/llm-draco",
    "microsoft/llmail-infrastructure-challenges",
    "google/oss-fuzz-genai",
    "protectai/modelscan",
    "meta-llama/Prompt-Guard-86M",
    "NVIDIA/NeMo-Guardrails",
    "microsoft/safety-toolkit",
    "meta-llama/llama-agentic-system",
    "QwenLM/Qwen3-Coder",
    "stanford-oval/storm",
    "huggingface/transformers",
    "ollama/ollama",
    "open-webui/open-webui",
    "danny-avila/LibreChat",
    "lm-sys/FastChat",
    "BerriAI/litellm",
    "comfyanonymous/ComfyUI",
    "sst/opencode",
    "garrytan/gstack",
    "obra/superpowers",
    "addyosmani/agent-skills",
    "github/spec-kit",
    "patiofinance/patio",
    "invariantlabs-ai/mcp-scan",
    "protectai/modelscan",
    "microsoft/AI-Red-Teaming-Playground",
    "carolynvs/AI-Researcher",
    "deepfence/llm-firewall",
    "mindspore-ai/mindspore",
    "TheAlgorithms/Python",
]

INSTALL_PATTERNS = [
    re.compile(r"^\s*(?:\$\s*)?(pip[3]? install .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(uv (?:tool )?install .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(npm (?:install|i) [-@].+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(npx .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(pnpm (?:add|dlx) .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(bun (?:add|x) .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(brew install .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(cargo install .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(go install .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(docker (?:run|pull) .+)$", re.IGNORECASE),
    re.compile(r"^\s*(?:\$\s*)?(git clone .+)$", re.IGNORECASE),
]

RELEVANCE_WORDS = {
    "prompt-engineering": ["prompt", "template", "llm", "ai", "agent"],
    "prompt-templates": ["prompt", "template"],
    "prompt-injection": ["injection", "prompt", "llm", "security"],
    "jailbreak": ["jailbreak", "jail", "red", "llm", "guardrail", "safety"],
    "llm-red-team": ["red", "team", "fuzz", "adversarial", "llm", "attack"],
    "llm-security": ["security", "scan", "llm", "guardrail", "firewall", "audit"],
    "guardrails": ["guardrail", "safety", "policy", "filter"],
    "ai-evaluation": ["eval", "benchmark", "llm", "judge", "arena"],
    "agent-frameworks": ["agent", "framework", "llm", "orchestrat"],
    "model-servers": ["server", "inference", "llm", "openai", "vllm", "ollama"],
    "chat-uis": ["chat", "ui", "frontend", "llm"],
    "tokenizers": ["token", "count", "llm"],
    "prompt-libraries": ["awesome", "prompt", "cheatsheet", "guide"],
    "model-providers": ["gpt", "claude", "gemini", "deepseek", "qwen", "grok", "llama", "mistral"],
    "agent-skills": ["skill", "agent", "claude", "opencode"],
    "context-engineering": ["context", "agent", "memory", "prompt"],
}

SKIP_LANGUAGES = {"", "Jupyter Notebook"}


def load_token() -> str:
    path = Path.home() / ".git-credentials"
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "github.com" in line and "@" in line:
            creds = line.split("://", 1)[1].split("@", 1)[0]
            if ":" in creds:
                return creds.split(":", 1)[1]
    return ""


def headers(token: str) -> dict[str, str]:
    head = {"Accept": "application/vnd.github+json", "User-Agent": "agent-pilot-research"}
    if token:
        head["Authorization"] = f"Bearer {token}"
    return head


def search(client: httpx.Client, query: str) -> list[dict[str, Any]]:
    resp = client.get(
        "/search/repositories",
        params={"q": query, "sort": "stars", "order": "desc", "per_page": 30},
    )
    if resp.status_code != 200:
        print(f"  search failed ({resp.status_code}) for {query}")
        return []
    return resp.json().get("items", [])


def readme(client: httpx.Client, full_name: str, branch: str) -> str:
    for ref in (branch, "main", "master"):
        url = f"https://raw.githubusercontent.com/{full_name}/{ref}/README.md"
        try:
            resp = client.get(url, timeout=20, follow_redirects=True)
        except httpx.HTTPError:
            continue
        if resp.status_code == 200 and len(resp.text) > 200:
            return resp.text
    return ""


def extract_install(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("#"):
            continue
        for pattern in INSTALL_PATTERNS:
            match = pattern.match(line)
            if match:
                command = match.group(1).strip()
                if len(command) < 120:
                    return command
    return ""


def extract_example(text: str) -> list[str]:
    blocks = re.findall(r"```[a-zA-Z0-9_+-]*\n(.*?)```", text, re.DOTALL)
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()][:8]
        if len(lines) >= 2 and any("install" not in line.lower() for line in lines):
            return lines
    return []


def score(repo: dict[str, Any], category: str) -> int:
    words = RELEVANCE_WORDS.get(category, [])
    haystack = " ".join(
        [
            repo.get("name", ""),
            repo.get("description") or "",
            " ".join(repo.get("topics") or []),
        ]
    ).lower()
    hits = sum(1 for word in words if word in haystack)
    stars = repo.get("stargazers_count", 0)
    return hits * 25 + min(stars // 500, 40)


def main() -> int:
    token = load_token()
    print(f"token: {'found' if token else 'none (rate limited)'}")
    head = headers(token)
    collected: dict[str, dict[str, Any]] = {}

    with httpx.Client(
        base_url="https://api.github.com", headers=head, timeout=30, follow_redirects=True
    ) as client:
        for category, query in SEARCHES:
            print(f"search: {category}")
            for repo in search(client, query):
                if repo.get("archived") or repo.get("fork"):
                    continue
                if repo.get("language") in SKIP_LANGUAGES and not repo.get("topics"):
                    continue
                if repo.get("stargazers_count", 0) < 40:
                    continue
                full = repo["full_name"]
                entry = collected.setdefault(
                    full,
                    {
                        "full_name": full,
                        "stars": repo.get("stargazers_count", 0),
                        "description": repo.get("description") or "",
                        "topics": repo.get("topics") or [],
                        "language": repo.get("language") or "",
                        "license": (repo.get("license") or {}).get("spdx_id") or "",
                        "pushed_at": repo.get("pushed_at", "")[:10],
                        "url": repo.get("html_url", f"https://github.com/{full}"),
                        "homepage": repo.get("homepage") or "",
                        "categories": [],
                    },
                )
                entry["categories"].append(category)
            time.sleep(2.5)

        print("fetching forced repos")
        for full in FORCE_INCLUDE:
            if full in collected:
                continue
            resp = client.get(f"/repos/{full}")
            if resp.status_code != 200:
                continue
            repo = resp.json()
            if repo.get("archived"):
                continue
            collected[full] = {
                "full_name": full,
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description") or "",
                "topics": repo.get("topics") or [],
                "language": repo.get("language") or "",
                "license": (repo.get("license") or {}).get("spdx_id") or "",
                "pushed_at": (repo.get("pushed_at") or "")[:10],
                "url": repo.get("html_url", f"https://github.com/{full}"),
                "homepage": repo.get("homepage") or "",
                "categories": ["curated"],
            }
            time.sleep(0.4)

        print("fetching readmes")
        items = list(collected.values())
        items.sort(key=lambda item: -item["stars"])
        for index, entry in enumerate(items):
            if index % 20 == 0:
                print(f"  readme {index}/{len(items)}")
            text = readme(client, entry["full_name"], "HEAD")
            entry["install"] = extract_install(text)
            entry["example"] = extract_example(text)[:6]
            time.sleep(0.15)

    payload = {
        "generated": time.strftime("%Y-%m-%d"),
        "repos": items,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(items)} repos -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
