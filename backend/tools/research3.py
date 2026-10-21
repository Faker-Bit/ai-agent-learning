"""Fetch the specific repos that the broad searches missed, and merge them in."""

from __future__ import annotations

import json
import time
from pathlib import Path

import httpx

from research import extract_example, extract_install, headers, load_token, readme

TARGET = Path(__file__).resolve().parent.parent / "app" / "content" / "_research.json"

EXTRA = [
    "openai/openai-cookbook",
    "Azure/PyRIT",
    "meta-llama/Prompt-Guard-86M",
    "microsoft/safety-toolkit",
    "deepfence/llm-firewall",
    "google/oss-fuzz-genai",
    "GAIR-NLP/CLIProxyAPI-1",
    "langwatch/langwatch",
    "huggingface/trl",
    "guidrails-ai/guidrails",
    "microsoft/AI-Red-Teaming-Playground",
    "protectai/modelscan",
    "centerforaisafety/HarmBench",
    "ethz-spylab/llm-draco",
    "BerriAI/litellm",
    "comfyanonymous/ComfyUI",
    "ggerganov/llama.cpp",
    "sgl-project/sglang",
    "NVIDIA/NeMo-Guardrails",
    "protectai/llm-guard",
    "meta-llama/llama-models",
    "RVC-Boss/GPT-SoVITS",
    "microsoft/semantic-kernel",
    "run-llama/llama_index",
    "microsoft/autogen",
    "openai/openai-agents-python",
    "google/adk-python",
    "strands-agents/sdk-python",
    "pydantic/pydantic-ai",
    "agno-agi/agno",
    "openai/swarm",
    "garrytan/gstack",
    "obra/superpowers",
    "addyosmani/agent-skills",
    "mattpocock/skills",
    "JuliusBrussee/caveman",
    "DietrichGebert/ponytail",
    "thedotmack/claude-mem",
    "github/spec-kit",
    "NVIDIA/SkillSpector",
    "usestrix/strix",
    "KeygraphHQ/shannon",
    "ifixai-ai/iFixAi",
    "data-privacy-stack/presidio",
    "mukul975/Anthropic-Cybersecurity-Skills",
    "elder-plinius/CL4R1T4S",
    "elder-plinius/L1B3RT4S",
    "LouisShark/chatgpt_system_prompt",
    "0xk1h0/ChatGPT_DAN",
    "BishopFox/sliver",
    "Portkey-AI/gateway",
    "asgeirtj/system_prompts_leaks",
    "dair-ai/Prompt-Engineering-Guide",
    "f/awesome-chatgpt-prompts",
    "f/prompts.chat",
    "microsoft/generative-ai-for-beginners",
    "microsoft/ai-agents-for-beginners",
    "rohitg00/ai-engineering-from-scratch",
    "langgptai/LangGPT",
    "linshenkx/prompt-optimizer",
    "mlabonne/llm-course",
    "headroomlabs-ai/headroom",
    "bytedance/deer-flow",
    "crewAIInc/crewAI",
    "block/goose",
    "All-Hands-AI/OpenHands",
    "open-webui/open-webui",
    "danny-avila/LibreChat",
    "ChatGPTNextWeb/NextChat",
    "HKUDS/nanobot",
    "vllm-project/vllm",
    "ollama/ollama",
    "lm-sys/FastChat",
    "langfuse/langfuse",
    "Arize-ai/phoenix",
    "truera/trulens",
    "lmnr-ai/lmnr",
    "QwenLM/qwen-code",
    "google-gemini/gemini-cli",
    "openai/codex",
    "anthropics/claude-code",
    "deepseek-ai/deepseek-harness",
    "deepseek-ai/DeepSeek-V3",
    "QwenLM/Qwen3-Coder",
    "huggingface/transformers",
    "stanford-oval/storm",
    "git-ecosystem/awesome-guides",
]


def main() -> int:
    token = load_token()
    head = headers(token)
    payload = json.loads(TARGET.read_text(encoding="utf-8"))
    repos: dict[str, dict] = {r["full_name"]: r for r in payload["repos"]}
    added = 0

    with httpx.Client(
        base_url="https://api.github.com", headers=head, timeout=30, follow_redirects=True
    ) as client:
        for full in EXTRA:
            if full in repos:
                continue
            resp = client.get(f"/repos/{full}")
            if resp.status_code != 200:
                print(f"  miss {full} ({resp.status_code})")
                time.sleep(0.3)
                continue
            repo = resp.json()
            if repo.get("archived"):
                print(f"  archived, skipped: {full}")
                continue
            repos[full] = {
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
                "install": "",
                "example": [],
            }
            added += 1
            time.sleep(0.25)

        missing_readme = [
            r for r in repos.values() if not r.get("install") and not r.get("example")
        ]
        with httpx.Client(headers=head, timeout=20, follow_redirects=True) as raw:
            for index, entry in enumerate(missing_readme):
                if index % 25 == 0:
                    print(f"  readme {index}/{len(missing_readme)}")
                text = readme(raw, entry["full_name"], "HEAD")
                entry["install"] = extract_install(text)
                entry["example"] = extract_example(text)[:6]
                time.sleep(0.08)

    payload["repos"] = sorted(repos.values(), key=lambda r: -r["stars"])
    payload["generated"] = time.strftime("%Y-%m-%d")
    TARGET.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"added {added} repos, total {len(payload['repos'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
