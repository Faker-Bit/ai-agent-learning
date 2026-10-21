"""Turn the research file into a curated, categorised resource catalogue.

Output: backend/app/content/resources.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parent.parent / "app" / "content" / "_research.json"
OUT = Path(__file__).resolve().parent.parent / "app" / "content" / "resources.py"

CATEGORIES: list[dict[str, Any]] = [
    {
        "id": "prompt-engineering",
        "short": "Prompting",
        "title": "Prompt engineering",
        "blurb": "Guides, courses and tooling for writing prompts that actually produce the output you wanted.",
        "picks": [
            "dair-ai/Prompt-Engineering-Guide",
            "microsoft/generative-ai-for-beginners",
            "f/awesome-chatgpt-prompts",
            "f/prompts.chat",
            "rohitg00/ai-engineering-from-scratch",
            "linshenkx/prompt-optimizer",
            "langgptai/LangGPT",
            "asgeirtj/system_prompts_leaks",
            "openai/openai-cookbook",
            "mlabonne/llm-course",
            "huggingface/transformers",
        ],
    },
    {
        "id": "prompt-security",
        "short": "Security",
        "title": "Injection, jailbreaks & red teaming",
        "blurb": "The security side: attack research, scanners, sandboxes and safe testing harnesses.",
        "picks": [
            "promptfoo/promptfoo",
            "NVIDIA/garak",
            "microsoft/AI-Red-Teaming-Playground-Labs",
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
            "invariantlabs-ai/mcp-scan",
            "protectai/modelscan",
            "centerforaisafety/HarmBench",
        ],
    },
    {
        "id": "guardrails",
        "short": "Guardrails",
        "title": "Guardrails & gateways",
        "blurb": "Policy enforcement that lives outside the model: gateways, rails and output filters.",
        "picks": [
            "NVIDIA/NeMo-Guardrails",
            "Portkey-AI/gateway",
            "guardrails-ai/guardrails",
            "BerriAI/litellm",
        ],
    },
    {
        "id": "model-servers",
        "short": "Serving",
        "title": "Serving models yourself",
        "blurb": "Run the weights on your own hardware, or route to every hosted provider through one endpoint.",
        "picks": [
            "ollama/ollama",
            "vllm-project/vllm",
            "sgl-project/sglang",
            "ggerganov/llama.cpp",
            "BerriAI/litellm",
        ],
    },
    {
        "id": "chat-uis",
        "short": "Chat UIs",
        "title": "Chat interfaces",
        "blurb": "A UI for talking to models you host or route - handy for evaluating behaviour by hand.",
        "picks": [
            "open-webui/open-webui",
            "danny-avila/LibreChat",
            "ChatGPTNextWeb/NextChat",
            "HKUDS/nanobot",
        ],
    },
    {
        "id": "agent-frameworks",
        "short": "Frameworks",
        "title": "Agent frameworks",
        "blurb": "Building agents in code instead of in a terminal - multi-agent, planning, tool loops.",
        "picks": [
            "All-Hands-AI/OpenHands",
            "bytedance/deer-flow",
            "crewAIInc/crewAI",
            "block/goose",
            "microsoft/ai-agents-for-beginners",
            "microsoft/autogen",
            "run-llama/llama_index",
            "microsoft/semantic-kernel",
            "openai/openai-agents-python",
            "google/adk-python",
            "strands-agents/sdk-python",
            "pydantic/pydantic-ai",
            "agno-agi/agno",
            "stanford-oval/storm",
        ],
    },
    {
        "id": "agent-skills",
        "short": "Skills",
        "title": "Skills & context",
        "blurb": "Packaged procedures, memory and context compression for agents that have to remember.",
        "picks": [
            "obra/superpowers",
            "garrytan/gstack",
            "addyosmani/agent-skills",
            "mattpocock/skills",
            "JuliusBrussee/caveman",
            "DietrichGebert/ponytail",
            "thedotmack/claude-mem",
            "github/spec-kit",
            "headroomlabs-ai/headroom",
            "github/awesome-copilot",
        ],
    },
    {
        "id": "eval-and-observability",
        "short": "Evals",
        "title": "Evals & observability",
        "blurb": "Trace what your agent did, score it, and catch regressions before your users do.",
        "picks": [
            "langfuse/langfuse",
            "Arize-ai/phoenix",
            "truera/trulens",
            "lmnr-ai/lmnr",
            "langwatch/langwatch",
        ],
    },
    {
        "id": "model-tooling",
        "short": "Model tools",
        "title": "Per-model tooling",
        "blurb": "The official and community tooling around each model family.",
        "picks": [
            "openai/codex",
            "anthropics/claude-code",
            "google-gemini/gemini-cli",
            "QwenLM/qwen-code",
            "deepseek-ai/deepseek-harness",
            "deepseek-ai/DeepSeek-V3",
            "QwenLM/Qwen3-Coder",
            "meta-llama/llama-models",
            "GAIR-NLP/CLIProxyAPI-1",
            "linuxhsj/WebModel",
        ],
    },
    {
        "id": "fine-tuning",
        "short": "Fine-tuning",
        "title": "Fine-tuning & training",
        "blurb": "Make a model yours: SFT, LoRA, DPO and the data plumbing around them.",
        "picks": [
            "huggingface/trl",
            "huggingface/transformers",
            "mlabonne/llm-course",
        ],
    },
]

FALLBACK_DESCRIPTIONS = {
    "deepseek-ai/DeepSeek-V3": "Reference implementation and weights for the DeepSeek-V3 mixture-of-experts model family.",
    "QwenLM/Qwen3-Coder": "The open Qwen3-Coder model family - agentic tool use and long context, Apache-2.0 weights.",
    "meta-llama/llama-models": "Reference weights, licences and evaluation notes for the Llama family of models.",
    "protectai/modelscan": "Scans machine learning model files for malicious code hidden in pickles and archives.",
    "centerforaisafety/HarmBench": "A standardised evaluation suite and dataset for measuring refusal robustness and jailbreak resistance.",
    "microsoft/AI-Red-Teaming-Playground-Labs": "Notebooks and tools for red teaming generative AI systems: attack generation, scoring and examples.",
    "invariantlabs-ai/mcp-scan": "Scans MCP servers for tool poisoning, rug pulls and hidden instructions.",
}

NOTES: dict[str, str] = {
    "microsoft/AI-Red-Teaming-Playground-Labs": "Microsoft's open AI red team tooling: prompt attack generation, scoring, and notebooks you can run against your own endpoints.",
    "guardrails-ai/guardrails": "Validate model output against structure and business rules - a JSON schema, a regex, a lookup - instead of hoping the prompt held.",
    "sgl-project/sglang": "Fast serving with RadixAttention prefix caching, which pays off when many requests share a long system prompt.",
    "ggerganov/llama.cpp": "The C++ engine under most local inference. GGUF quantisation, CPU, Metal and Vulkan backends.",
    "HKUDS/nanobot": "A tiny self-hosted agent framework with a web UI, tools and memory - small enough to read in an afternoon.",
    "google/adk-python": "Google's Agent Development Kit: model-agnostic agents with tools, sessions and evaluation.",
    "strands-agents/sdk-python": "AWS's agent SDK, built around MCP tools and a model-driven loop.",
    "pydantic/pydantic-ai": "A small, typed agent framework where every tool signature and output is validated by the model.",
    "agno-agi/agno": "A performance-focused agent framework with reasoning and memory built in.",
    "microsoft/autogen": "Microsoft's multi-agent framework, still the reference implementation for agent conversations.",
    "microsoft/semantic-kernel": "A plugin-style SDK with a model-agnostic core across Python, C# and Java.",
    "run-llama/llama_index": "The data layer for LLM apps: ingestion, retrieval, agents, evaluation.",
    "openai/openai-agents-python": "The OpenAI Agents SDK: handoffs between agents, guardrails, sessions and tracing.",
    "huggingface/trl": "The post-training library: SFT, DPO and reward modelling behind one API.",
    "microsoft/ai-agents-for-beginners": "18 lessons on building agents, from a single agent to multi-agent orchestration.",
    "crewAIInc/crewAI": "Role-based multi-agent orchestration in Python - the clearest example of the crew pattern.",
    "protectai/modelscan": "Scan model files before you load them: malicious pickles and embedded payloads are a real supply-chain risk.",
    "centerforaisafety/HarmBench": "The HarmBench suite and dataset - the standard reference for measuring refusal robustness.",
    "invariantlabs-ai/mcp-scan": "Scan MCP servers for tool poisoning and rug pulls before you connect them to an agent.",
    "BishopFox/sliver": "Adversary emulation framework from Bishop Fox. Not LLM-specific, but the tradecraft transfers directly.",
    "portkey-ai/gateway": "A gateway with guardrails, routing, caching and fallbacks sitting in front of your models.",
    "NVIDIA/NeMo-Guardrails": "Programmable rails: define the allowed conversation flows in Colang and enforce them in the app.",
    "protectai/llm-guard": "Input and output scanners for prompt injection, sensitive data and topic restrictions.",
    "dair-ai/Prompt-Engineering-Guide": "Start here. Technique-by-technique guide with papers, notebooks and evals - the best single map of the field.",
    "microsoft/generative-ai-for-beginners": "21 free lessons from Microsoft. Works in Python and TypeScript, each lesson ends with an exercise.",
    "f/awesome-chatgpt-prompts": "The classic prompt collection. Useful as a catalogue of task shapes; the new project name is prompts.chat.",
    "f/prompts.chat": "The same collection rebuilt as a shareable app, with a CLI for creating your own prompt library.",
    "rohitg00/ai-engineering-from-scratch": "Builds real systems rather than demos: retrieval, evals, agents, deployment. Good for the 'how do I ship this' stage.",
    "linshenkx/prompt-optimizer": "A prompt optimiser that rewrites a prompt for a target model. Run it, then diff the before and after against your own eval set.",
    "langgptai/LangGPT": "Structured prompt templates with roles and constraints. Read the templates even if you never install it.",
    "asgeirtj/system_prompts_leaks": "Documented system prompts from the major products. Useful for seeing how vendors actually structure instructions.",
    "openai/openai-cookbook": "Official recipes: structured output, tool calling, RAG, evaluation, embeddings. Copy-paste ready.",
    "mlabonne/llm-course": "A full course from fine-tuning to deployment, with Colab notebooks. The best single repo if you want the maths behind it.",
    "huggingface/transformers": "The library behind most open model work. Use it when you need full control over the model, not for API calls.",
    "promptfoo/promptfoo": "The practical one. Declare your prompts, run an attack suite or an eval, and diff results in CI. Works with any provider.",
    "NVIDIA/garak": "The LLM vulnerability scanner. It probes a target model with thousands of probes and reports what got through.",
    "Azure/PyRIT": "Microsoft's red-team toolkit: generate, probe and score attacks against a target in a controlled loop.",
    "NVIDIA/SkillSpector": "Scans agent skills and MCP servers for malicious instructions before you install them. Run it on every third-party skill.",
    "usestrix/strix": "Open-source AI penetration testing for web apps: an agent that finds and proves real vulnerabilities.",
    "KeygraphHQ/shannon": "An AI pentester for web applications and APIs that reads your source to find attack surfaces.",
    "ifixai-ai/iFixAi": "Independent auditing of AI agents - run it by a human or by the agent itself, across providers.",
    "data-privacy-stack/presidio": "Detects and redacts PII in text before it reaches a model or a log. A quiet hero for any RAG pipeline.",
    "mukul975/Anthropic-Cybersecurity-Skills": "817 cybersecurity skills for agents, mapped to MITRE ATT&CK, NIST CSF and MITRE ATLAS.",
    "elder-plinius/CL4R1T4S": "A catalogue of leaked system prompts from the major products. Read it to learn how vendors scope their models.",
    "elder-plinius/L1B3RT4S": "A large archive of community jailbreak prompts. Treat as research material, and re-test every payload before trusting it.",
    "LouisShark/chatgpt_system_prompt": "System prompts plus notes on prompt injection and leakage - good for the defensive reading of a product's prompt.",
    "0xk1h0/ChatGPT_DAN": "An early archive of role-play jailbreak prompts. Historical interest; the mechanism is what matters.",
    "BishopFox/sliver": "Adversary emulation framework from Bishop Fox. Not LLM-specific, but the tradecraft translates directly.",
    "invariantlabs-ai/mcp-scan": "Scans MCP servers for tool poisoning, rug pulls and hidden instructions. Run before you add a server.",
    "protectai/modelscan": "Scans model files for malicious pickles and embedded payloads. Use it before loading weights you did not build.",
    "centerforaisafety/HarmBench": "The HarmBench evaluation suite and dataset - the standard reference for measuring refusal robustness.",
    "ethz-spylab/llm-draco": "A formal framework for analysing and defending against prompt injection, with the security properties spelled out.",
    "microsoft/safety-toolkit": "Prompt shields, jailbreak detection and the tooling behind Microsoft's AI red team work.",
    "meta-llama/Prompt-Guard-86M": "A small classifier that flags prompt injection attempts. Cheap enough to run on every request.",
    "microsoft/AI-Red-Teaming-Playground": "Tools and guidance for red teaming generative AI: prompt attack generation, scoring and examples.",
    "deepfence/llm-firewall": "A firewall that inspects traffic to LLM apps and blocks prompt injection and sensitive-data leakage.",
    "google/oss-fuzz-genai": "Fuzzing for generative AI code, including LLM integrations. Find the crash before an attacker does.",
    "NVIDIA/NeMo-Guardrails": "Programmable rails: define the allowed flows in Colang, enforce them in your app.",
    "Portkey-AI/gateway": "A gateway with guardrails, routing, caching and fallbacks in front of your models.",
    "protectai/llm-guard": "Input and output scanners for prompt injection, sensitive data and topic restrictions.",
    "guidrails-ai/guidrails": "Validate model output against structure and business rules instead of hoping the prompt was followed.",
    "BerriAI/litellm": "One OpenAI-compatible endpoint for 100+ providers, with a proxy, caching, budgets and key management.",
    "ollama/ollama": "The easiest local runner. `ollama pull qwen2.5-coder` and you have an OpenAI-compatible server on port 11434.",
    "vllm-project/vllm": "The production serving engine: continuous batching, tensor parallelism, OpenAI-compatible API.",
    "sgl-project/sglang": "Fast serving with RadixAttention prefix caching - strong when many requests share a long prompt.",
    "ggerganov/llama.cpp": "The C++ engine underneath most local inference. GGUF quantisation, CPU and Metal support.",
    "open-webui/open-webui": "A full web UI for Ollama and OpenAI-compatible endpoints, with RAG, tools and multi-user support.",
    "danny-avila/LibreChat": "A ChatGPT-style UI with agents, MCP and skills, and every major provider wired in.",
    "ChatGPTNextWeb/NextChat": "A deploy-it-anywhere chat front end that needs no backend.",
    "HKUDS/nanobot": "A very small self-hosted agent framework with a web UI, tools and memory - good to read end to end.",
    "All-Hands-AI/OpenHands": "The open agent platform: a sandboxed runtime, a web UI and an API you can drive from code.",
    "bytedance/deer-flow": "A long-horizon super agent that researches, codes and creates, with sandboxed execution.",
    "crewAIInc/crewAI": "Role-based multi-agent orchestration in Python. The clearest example of the crew pattern.",
    "block/goose": "Block's open agent. Everything is an MCP extension, and the CLI is the same as the desktop app.",
    "microsoft/ai-agents-for-beginners": "18 lessons on building agents, from a single agent to multi-agent orchestration.",
    "microsoft/autogen": "The multi-agent framework Microsoft ships and documents heavily. Good for research and prototyping.",
    "run-llama/llama_index": "The data layer for LLM apps: ingestion, retrieval, agents and evaluation.",
    "microsoft/semantic-kernel": "A plugin-style SDK for building agents in Python, C# and Java with a model-agnostic core.",
    "openai/openai-agents-python": "The OpenAI Agents SDK: handoffs, guardrails, sessions and tracing in a small package.",
    "google/adk-python": "Google's Agent Development Kit: model-agnostic agents with tools, sessions and evaluation.",
    "strands-agents/sdk-python": "AWS's agent SDK - model-driven agents that use MCP tools by default.",
    "pydantic/pydantic-ai": "A typed, small agent framework where every tool and output is a validated model.",
    "agno-agi/agno": "A performance-focused agent framework with a built-in reasoning and memory layer.",
    "stanford-oval/storm": "The research system behind AI-generated Wikipedia-style articles. Good architecture to read.",
    "obra/superpowers": "A skills framework plus a development method. The skills are how the method is delivered - read the method first.",
    "garrytan/gstack": "23 opinionated tools that each act as a different role. Shows how far the role-play pattern goes.",
    "addyosmani/agent-skills": "Production-grade engineering skills, written as SKILL.md files. The format at scale.",
    "mattpocock/skills": "A real engineer's personal skill set published as-is. Good for the tone and length of a well-written skill.",
    "JuliusBrussee/caveman": "A skill plus a proxy that shrinks the context. The clearest demonstration that the harness controls the bill.",
    "DietrichGebert/ponytail": "A behaviour skill: the best code is the code you never wrote. Fewer diffs, fewer tokens.",
    "thedotmack/claude-mem": "Persistent memory across sessions for any agent. Worth reading before you build your own memory layer.",
    "github/spec-kit": "GitHub's spec-driven development toolkit: write the spec, generate the plan, implement against it.",
    "headroomlabs-ai/headroom": "Compresses tool output, logs and RAG chunks before they reach the model. Real token savings.",
    "github/awesome-copilot": "Community instructions, agents and skills for Copilot - the same pattern, a different host.",
    "langfuse/langfuse": "Open-source tracing, evals and prompt management. The default observability choice for agent apps.",
    "Arize-ai/phoenix": "Open-source tracing and evaluation with a notebook workflow. `pip install arize-phoenix` and you are running.",
    "truera/trulens": "Evaluation and tracking for LLM experiments, with OpenTelemetry-based instrumentation.",
    "lmnr-ai/lmnr": "A lightweight tracing and eval layer that drops into an existing app in a few lines.",
    "langwatch/langwatch": "Scenario-based evals and prompt optimisation with a managed platform behind it.",
    "openai/codex": "The OpenAI coding agent. Reads your AGENTS.md, runs in a sandbox and asks before anything destructive.",
    "anthropics/claude-code": "The Anthropic agent. Hooks, skills, subagents and CLAUDE.md make it the most extensible of the CLIs.",
    "google-gemini/gemini-cli": "Google's agent and the reference for the open agent CLI. Free tier, GEMINI.md, MCP support.",
    "QwenLM/qwen-code": "The open-source Gemini CLI fork from Alibaba, with Qwen3-Coder behind it.",
    "deepseek-ai/deepseek-harness": "DeepSeek's agent framework - everything is a plugin, and the models are very cheap.",
    "deepseek-ai/DeepSeek-V3": "The model weights and the paper. Read the paper if you want to know why the price is what it is.",
    "QwenLM/Qwen3-Coder": "The open coding model behind a lot of agent traffic. Strong tool use for its size.",
    "meta-llama/llama-models": "Reference weights, licences and evaluation notes for the Llama family.",
    "GAIR-NLP/CLIProxyAPI-1": "Wraps CLI-based model subscriptions behind an OpenAI or Anthropic compatible API - handy if you already pay for a subscription.",
    "linuxhsj/WebModel": "Bridges web chat interfaces to an OpenAI-compatible API. Useful for experimenting with a model you only have in the browser.",
    "huggingface/trl": "The post-training library: SFT, DPO and reward modelling with a single API surface.",
    "github/awesome-guides": "A broad index of guides worth knowing about across the ecosystem.",
}


def ascii_only(value: str) -> str:
    """Keep the generated module pure ASCII so it can never be garbled."""
    return value.encode("ascii", "ignore").decode("ascii")


def main() -> int:
    data = json.loads(RESEARCH.read_text(encoding="utf-8"))
    repos = {r["full_name"]: r for r in data["repos"]}

    categories: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []
    missing: list[str] = []

    for category in CATEGORIES:
        picks = []
        for full in category["picks"]:
            repo = repos.get(full)
            if repo is None:
                missing.append(full)
                continue
            picks.append(full)
            resources.append(
                {
                    "id": f"{category['id']}--{full.replace('/', '--')}",
                    "name": repo["full_name"].split("/")[-1],
                    "repo": repo["full_name"],
                    "url": repo["url"],
                    "category": category["id"],
                    "category_title": category["title"],
                    "stars": repo.get("stars", 0),
                    "license": repo["license"] or "see repo",
                    "pushed": repo.get("pushed", ""),
                    "description": ascii_only(repo.get("description") or FALLBACK_DESCRIPTIONS.get(full, "")),
                    "topics": [ascii_only(x) for x in (repo.get("topics") or [])[:6]],
                    "language": repo.get("language") or "",
                    "install": ascii_only(repo.get("install") or ""),
                    "example": [ascii_only(line) for line in (repo.get("example") or [])],
                    "note": ascii_only(NOTES.get(full, "")),
                    "homepage": repo.get("homepage") or "",
                }
            )
        categories.append(
            {
                "id": category["id"],
                "short": category.get("short", category["title"]),
                "title": category["title"],
                "blurb": category["blurb"],
                "count": len(picks),
            }
        )

    header = (
        '"""Curated resource catalogue generated by tools/build_resources.py.\n\n'
        "Every entry was fetched from the GitHub API on the date in GENERATED, with its\n"
        "install command and usage example extracted from the project README.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "from typing import Any\n\n"
        f'GENERATED = "{data["generated"]}"\n\n'
        "RESOURCE_CATEGORIES: list[dict[str, Any]] = "
        + json.dumps(categories, indent=4, ensure_ascii=False)
        + "\n\n"
        "RESOURCES: list[dict[str, Any]] = "
        + json.dumps(resources, indent=4, ensure_ascii=False)
        + "\n"
    )
    OUT.write_text(header, encoding="utf-8")
    print(f"wrote {len(resources)} resources in {len(categories)} categories -> {OUT.name}")
    if missing:
        print(f"MISSING ({len(missing)}): {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
