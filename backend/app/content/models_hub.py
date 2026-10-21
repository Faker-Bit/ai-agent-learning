"""AI Model Learning Hub: a practical guide to every major model family.

Each entry covers the four things people actually need: where to use the model,
how to call it from code, how to prompt it well, and how to plug it into a
coding agent. API details were checked against each vendor's own docs.
"""

from __future__ import annotations

from typing import Any

MODEL_HUB: list[dict[str, Any]] = [
    {
        "id": "chatgpt",
        "name": "ChatGPT",
        "vendor": "OpenAI",
        "tier": "paid",
        "blurb": "The default generalist: strong reasoning, tool use, image understanding and the widest ecosystem.",
        "best_for": [
            "Everyday work where one model must do everything",
            "Tool use and function calling in your own code",
            "Data analysis with the built-in code interpreter",
        ],
        "surfaces": [
            ["Web app", "chatgpt.com - projects, custom GPTs, memory, deep research"],
            ["API", "https://api.openai.com/v1 - OpenAI SDK, Chat Completions and Responses API"],
            ["Coding agent", "Codex CLI and the Codex IDE extension"],
        ],
        "api": {
            "base_url": "https://api.openai.com/v1",
            "style": "OpenAI (chat completions + responses)",
            "key_url": "https://platform.openai.com/api-keys",
            "env": "OPENAI_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a terse senior engineer."},
        {"role": "user", "content": "Explain why this query is slow: SELECT * FROM orders"},
    ],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Put the role and the output contract in the system prompt, not in the question.",
            "Ask for a checkable output: 'reply with a JSON object matching this schema'.",
            "For hard problems, use a reasoning model (o-series / GPT-5) instead of asking the cheap model to think harder.",
            "Show one example of the output you want. One example beats a page of description.",
            "Use the file/code tools rather than pasting code - the model reads the file and stays in sync with the repo.",
        ],
        "agent_notes": [
            "In opencode: `opencode auth login` then pick the openai provider, model id `openai/gpt-4.1-mini`.",
            "Codex CLI signs in with your ChatGPT plan: `codex`, then 'Sign in with ChatGPT'.",
        ],
        "limits": [
            "Rate limits are per tier and per model; a reasoning model burns the quota faster.",
            "The chat UI and the API have different limits - a plan does not include API calls.",
        ],
        "links": [
            ["Docs", "https://platform.openai.com/docs"],
            ["Models", "https://platform.openai.com/docs/models"],
            ["Prompting guide", "https://platform.openai.com/docs/guides/prompting"],
        ],
    },
    {
        "id": "claude",
        "name": "Claude",
        "vendor": "Anthropic",
        "tier": "paid",
        "blurb": "The careful one: excellent long context, structured answers and the best behaviour inside a coding agent.",
        "best_for": [
            "Large codebases and long documents",
            "Work where a wrong answer is expensive - refactors, migrations, reviews",
            "Writing that sounds like a person wrote it",
        ],
        "surfaces": [
            ["Web app", "claude.ai - projects, artifacts, research, file analysis"],
            ["API", "https://api.anthropic.com/v1/messages - x-api-key + anthropic-version headers"],
            ["Coding agent", "Claude Code, and the Claude Code extension for VS Code"],
        ],
        "api": {
            "base_url": "https://api.anthropic.com/v1",
            "style": "Anthropic Messages API",
            "key_url": "https://console.anthropic.com/settings/keys",
            "env": "ANTHROPIC_API_KEY",
            "install": "pip install anthropic",
            "code": """import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a terse senior engineer.",
    messages=[{"role": "user", "content": "Review this diff for security bugs."}],
)
print(message.content[0].text)""",
        },
        "prompting": [
            "Give the role, the constraints and the acceptance criteria up front - Claude follows explicit contracts closely.",
            "Use XML-ish tags to delimit parts of the prompt (<context>, <task>, <output_format>).",
            "Ask it to think before answering when the task is multi-step; extended thinking is a separate control.",
            "Prompt caching pays off on a long stable prefix - keep the system prompt and reference files at the front.",
            "For code, point at the file and ask for the change plus the test, in that order.",
        ],
        "agent_notes": [
            "In opencode: pick the anthropic provider, model id `anthropic/claude-sonnet-4-5-20250929`.",
            "Claude Code reads CLAUDE.md; `/init` generates it from the repo.",
            "DeepSeek and other providers can sit behind Claude Code with ANTHROPIC_BASE_URL - see the DeepSeek entry.",
        ],
        "limits": [
            "Long system prompts plus large files can hit the per-minute token cap before the context window does.",
            "Prompt caching only applies to the stable prefix, in 5-minute and 1-hour windows.",
        ],
        "links": [
            ["Docs", "https://docs.anthropic.com/en/docs/claude-code/overview"],
            ["API", "https://docs.anthropic.com/en/api/overview"],
            ["Prompting", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview"],
        ],
    },
    {
        "id": "gemini",
        "name": "Gemini",
        "vendor": "Google",
        "tier": "free",
        "blurb": "The generous one: the largest context windows, native multimodal and a free tier that actually works.",
        "best_for": [
            "Feeding a whole repository or a folder of PDFs to a model",
            "Vision, audio and video in the same prompt",
            "Learning and side projects - the free tier is generous",
        ],
        "surfaces": [
            ["Web app", "gemini.google.com - Gems, Deep Research, canvas, image and video generation"],
            ["API", "https://generativelanguage.googleapis.com/v1beta - free tier for flash models"],
            ["Coding agent", "Gemini CLI (and Antigravity CLI for unpaid and Google One tiers)"],
        ],
        "api": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "style": "Google GenAI (also OpenAI-compatible at /v1beta/openai)",
            "key_url": "https://aistudio.google.com/apikey",
            "env": "GEMINI_API_KEY",
            "install": "pip install google-genai",
            "code": """from google import genai

client = genai.Client()  # reads GEMINI_API_KEY

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Summarise the architecture of this repository.",
)
print(response.text)""",
        },
        "prompting": [
            "Use it when the context is the hard part - a 1M window beats three retrieval steps.",
            "Anchor with the File API or a URL instead of pasting; the model can re-read them.",
            "Grounding with Google Search gives you citations and fresher facts.",
            "Turn reasoning on explicitly for maths and planning; leave it off for simple lookups.",
            "Say what to do with ambiguity: 'if the file does not exist, say so and list what you checked'.",
        ],
        "agent_notes": [
            "In opencode: pick the gemini provider, model id `gemini/gemini-3.8-flash`.",
            "Gemini CLI: `npm install -g @google/gemini-cli`, then `gemini`.",
            "Note: since 18 June 2026 Google moved unpaid and Google One users to Antigravity CLI.",
        ],
        "limits": [
            "Free tier is about 1,500 requests/day on flash models, with tighter per-minute limits.",
            "Very large prompts are billed by tokens even on the free tier, so watch the quota.",
        ],
        "links": [
            ["API docs", "https://ai.google.dev/gemini-api/docs"],
            ["Models", "https://ai.google.dev/gemini-api/docs/models"],
            ["Gemini CLI", "https://geminicli.com/docs/"],
        ],
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "vendor": "DeepSeek",
        "tier": "paid",
        "blurb": "The cheap one: frontier-level reasoning and coding for a fraction of the price, with an OpenAI-compatible API.",
        "best_for": [
            "High-volume work - bulk refactors, test generation, review passes",
            "Reasoning tasks where the price of the frontier model hurts",
            "Dropping into Claude Code or Codex without changing your code",
        ],
        "surfaces": [
            ["Web app", "chat.deepseek.com - chat and reasoner modes"],
            ["API", "https://api.deepseek.com - OpenAI-compatible, no SDK changes"],
            ["Coding agent", "Any OpenAI-compatible agent; also usable inside Claude Code"],
        ],
        "api": {
            "base_url": "https://api.deepseek.com",
            "style": "OpenAI-compatible",
            "key_url": "https://platform.deepseek.com/api_keys",
            "env": "DEEPSEEK_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-key",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-reasoner",      # or deepseek-chat for the general model
    messages=[{"role": "user", "content": "Find the bug in this function."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "deepseek-reasoner wants room to think - do not cap it at a token limit and expect an answer.",
            "Give it a concrete definition of done, like you would for a junior engineer.",
            "Chain the work: ask for the diagnosis first, the patch second.",
            "It is the cheapest sensible way to run a review agent over a whole repo.",
            "Keep the system prompt short - it is billed on every turn.",
        ],
        "agent_notes": [
            "Claude Code with DeepSeek (from the DeepSeek docs): set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic and ANTHROPIC_AUTH_TOKEN to your key.",
            "Model mapping there: claude-opus names map to deepseek-v4-pro, sonnet/haiku names map to deepseek-flash.",
            "In opencode: pick the deepseek provider, model id `deepseek/deepseek-chat`.",
        ],
        "limits": [
            "DeepSeek models are also the most jailbreak-prone of the popular open families in published tests - treat their output as untrusted.",
            "Rate limits tighten during peak hours in China.",
        ],
        "links": [
            ["API docs", "https://api-docs.deepseek.com/"],
            ["Claude Code integration", "https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/"],
            ["Models", "https://api-docs.deepseek.com/quick_start/pricing"],
        ],
    },
    {
        "id": "grok",
        "name": "Grok",
        "vendor": "xAI",
        "tier": "paid",
        "blurb": "The current-events one: live X data, image understanding and configurable reasoning.",
        "best_for": [
            "Anything that happened in the last few hours",
            "Image and video understanding on the latest events",
            "Agentic tool calling with a fast reasoning dial",
        ],
        "surfaces": [
            ["Web app", "grok.com and the Grok app, also inside X"],
            ["API", "https://api.x.ai/v1 - OpenAI-compatible"],
            ["Coding agent", "Grok Build CLI, and the opencode xai provider"],
        ],
        "api": {
            "base_url": "https://api.x.ai/v1",
            "style": "OpenAI-compatible",
            "key_url": "https://console.x.ai/",
            "env": "XAI_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(api_key="your-xai-key", base_url="https://api.x.ai/v1")

response = client.chat.completions.create(
    model="grok-4",
    messages=[{"role": "user", "content": "What broke in the ecosystem this week?"}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Say when to use live search - otherwise the model may answer from training data instead.",
            "Ask for sources when the answer is time-sensitive.",
            "Reasoning effort is configurable; raise it for planning, lower it for chat.",
            "It handles images natively - attach a screenshot and ask what is wrong with it.",
            "Keep the request concrete: 'list the three most likely causes' beats 'why is it broken'.",
        ],
        "agent_notes": [
            "In opencode: pick the xai provider, model id `xai/grok-4`.",
            "Grok Build (the CLI) is also reachable through multi-harness control planes.",
        ],
        "limits": [
            "Live search adds latency and extra tokens - it is not free.",
            "The newest flagship is priced above the cheaper models; use it where it matters.",
        ],
        "links": [
            ["Docs", "https://docs.x.ai/"],
            ["Models", "https://docs.x.ai/docs/models"],
        ],
    },
    {
        "id": "qwen",
        "name": "Qwen",
        "vendor": "Alibaba",
        "tier": "free",
        "blurb": "The coding-and-context one: Qwen3-Coder for agents, a 1M window, and a free flash tier.",
        "best_for": [
            "Coding agents that have to read a lot of code",
            "Long-context work on a budget",
            "Multilingual projects, including Chinese-language codebases",
        ],
        "surfaces": [
            ["Web app", "chat.qwen.ai - Qwen Chat, artefacts, deep research"],
            ["API", "Alibaba Cloud Model Studio - OpenAI-compatible mode, international and China regions"],
            ["Coding agent", "Qwen Code - the open-source Gemini CLI fork, and the opencode qwen provider"],
        ],
        "api": {
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "style": "OpenAI-compatible",
            "key_url": "https://modelstudio.console.alibabacloud.com/",
            "env": "DASHSCOPE_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-key",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

response = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=[{"role": "user", "content": "Refactor this module and explain the change."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Qwen3-Coder is built for agentic loops - file edits, tool calls, long diffs.",
            "Flash models handle the exploration; switch to the Coder or thinking variant for the edit.",
            "State the language and the framework version; Qwen is trained on very many stacks.",
            "For a big repo, ask for a file map first and then work file by file.",
            "Keep the output contract explicit - a schema beats a paragraph.",
        ],
        "agent_notes": [
            "Qwen Code is a fork of Gemini CLI: `npm install -g @qwen-code/qwen-code` (check the repo for the current package name).",
            "In opencode: pick the qwen provider via a custom OpenAI-compatible base URL.",
            "Alibaba also serves Qwen through OpenRouter and Model Studio - pick the region that matches your key.",
        ],
        "limits": [
            "Free quotas apply per region and change often; check the console.",
            "The international and China endpoints are separate accounts and separate keys.",
        ],
        "links": [
            ["Model Studio", "https://www.alibabacloud.com/en/product/modelstudio"],
            ["Qwen Code", "https://github.com/QwenLM/qwen-code"],
            ["Qwen models", "https://github.com/QwenLM/Qwen3-Coder"],
        ],
    },
    {
        "id": "llama",
        "name": "Llama",
        "vendor": "Meta",
        "tier": "local",
        "blurb": "The open-weights one: run it yourself, quantise it, fine-tune it, and never send your code anywhere.",
        "best_for": [
            "Private codebases and offline work",
            "Fine-tuning your own style, domain or output format",
            "Predictable cost - the hardware is a one-off",
        ],
        "surfaces": [
            ["Local", "Ollama, LM Studio, vLLM, llama.cpp - all speak OpenAI-compatible HTTP"],
            ["API", "Any host that serves open weights: Together, Fireworks, Groq, NVIDIA NIM"],
            ["Fine-tuning", "Axolotl, LLaMA Factory, Unsloth, or a hosted LoRA service"],
        ],
        "api": {
            "base_url": "http://localhost:11434/v1",
            "style": "OpenAI-compatible (local)",
            "key_url": "https://huggingface.co/settings/tokens",
            "env": "OLLAMA_API_KEY",
            "install": "curl -fsSL https://ollama.com/install.sh | sh",
            "code": """from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="qwen2.5-coder",          # or llama3.2
    messages=[{"role": "user", "content": "Write a pytest for this function."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Small models need narrower instructions - one job per prompt, not a paragraph of context.",
            "Few-shot examples matter much more than with a frontier model.",
            "Give the exact output format; small models drift without one.",
            "Lower the temperature to 0 for anything you need to be reproducible.",
            "Give the model a tool it can call instead of asking it to remember state.",
        ],
        "agent_notes": [
            "In opencode: set the ollama base URL and pick a local model id; no key required.",
            "Run a local model as a subagent for exploration while a frontier model writes the patch.",
            "Qwen2.5-Coder and Qwen3-Coder are the open models that behave best inside agents.",
        ],
        "limits": [
            "Context length and tool-calling reliability depend on the quantisation and the size you can fit in VRAM.",
            "The 4B model is fine for edits; it will not plan a refactor on its own.",
        ],
        "links": [
            ["Ollama", "https://ollama.com/"],
            ["llama.cpp", "https://github.com/ggml-org/llama.cpp"],
            ["Model weights", "https://huggingface.co/meta-llama"],
        ],
    },
    {
        "id": "mistral",
        "name": "Mistral",
        "vendor": "Mistral AI",
        "tier": "free",
        "blurb": "The European one: strong small models, Codestral for completion, and a free tier on small models.",
        "best_for": [
            "Fast, cheap, EU-hosted inference",
            "Fill-in-the-middle code completion (Codestral)",
            "Self-hosting small models with a permissive licence",
        ],
        "surfaces": [
            ["Web app", "chat.mistral.ai and Le Chat"],
            ["API", "https://api.mistral.ai/v1 - OpenAI-compatible"],
            ["Local", "Ollama and vLLM serve the open Mistral and Devstral weights"],
        ],
        "api": {
            "base_url": "https://api.mistral.ai/v1",
            "style": "OpenAI-compatible",
            "key_url": "https://console.mistral.ai/api-keys",
            "env": "MISTRAL_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(api_key="your-mistral-key", base_url="https://api.mistral.ai/v1")

response = client.chat.completions.create(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": "Summarise this changelog in three bullets."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Use small models for classification, routing and extraction - not for open-ended design.",
            "Codestral is a completion model: give it a prefix and let it continue, do not chat with it.",
            "Mistral models follow instructions tightly; give the format and the constraints together.",
            "Ask for JSON when you plan to parse the answer, and validate it anyway.",
        ],
        "agent_notes": [
            "In opencode: pick the mistral provider, model id `mistral/mistral-small-latest`.",
            "Devstral and Codestral run locally on a workstation GPU through vLLM.",
        ],
        "limits": [
            "The free tier applies to the smaller models and is rate limited per minute.",
            "Mistral models have a shorter context than the frontier models - check before pasting a repo.",
        ],
        "links": [
            ["Docs", "https://docs.mistral.ai/"],
            ["Le Chat", "https://chat.mistral.ai/"],
        ],
    },
    {
        "id": "groq",
        "name": "Groq & Cerebras",
        "vendor": "Groq / Cerebras",
        "tier": "free",
        "blurb": "The fast ones: the same open models served on custom silicon, at a speed you can feel.",
        "best_for": [
            "Fast exploration agents - grep, read, summarise, over and over",
            "Free tiers big enough to actually learn on",
            "Latency-sensitive tooling where you want sub-second first token",
        ],
        "surfaces": [
            ["API", "Groq: https://api.groq.com/openai/v1 - Cerebras: https://api.cerebras.ai/v1"],
            ["Models", "Llama 3.3 70B, Qwen3, Kimi K2, GPT-OSS on Groq"],
            ["Local", "Ollama or vLLM for the same weights on your own box"],
        ],
        "api": {
            "base_url": "https://api.groq.com/openai/v1",
            "style": "OpenAI-compatible",
            "key_url": "https://console.groq.com/keys",
            "env": "GROQ_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(api_key="your-groq-key", base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "List the public functions in this file."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "These are open models - keep the request narrow and the format explicit.",
            "Speed makes them ideal for many small calls: map the repo, then read the three files that matter.",
            "Do not ask for reasoning depth; ask for the answer.",
            "Use them as the exploration agent and save the frontier model for the edit.",
        ],
        "agent_notes": [
            "In opencode: pick groq with model id `groq/llama-3.3-70b-versatile`.",
            "Route your plan agent to a free fast model and your build agent to a strong one - that is where the savings are.",
        ],
        "limits": [
            "Free tiers are per-minute and per-day; expect 429s if you fan out too hard.",
            "Output tokens are billed differently from input - watch the reasoning models.",
        ],
        "links": [
            ["Groq console", "https://console.groq.com/keys"],
            ["Cerebras cloud", "https://cloud.cerebras.ai/"],
        ],
    },
    {
        "id": "openrouter",
        "name": "OpenRouter",
        "vendor": "OpenRouter",
        "tier": "free+paid",
        "blurb": "The one-key one: every major model behind one OpenAI-compatible endpoint, with free variants.",
        "best_for": [
            "Comparing models without signing up for five providers",
            "One bill, one key, one place to see the price of every model",
            "Free models marked with the :free suffix",
        ],
        "surfaces": [
            ["API", "https://openrouter.ai/api/v1 - OpenAI-compatible, model ids are provider/model"],
            ["Web", "openrouter.ai - a playground per model, usage and cost dashboard"],
        ],
        "api": {
            "base_url": "https://openrouter.ai/api/v1",
            "style": "OpenAI-compatible",
            "key_url": "https://openrouter.ai/keys",
            "env": "OPENROUTER_API_KEY",
            "install": "pip install openai",
            "code": """from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-key",
    base_url="https://openrouter.ai/api/v1",
)

response = client.chat.completions.create(
    model="qwen/qwen3.6-plus:free",     # ':free' = the free tier
    messages=[{"role": "user", "content": "Explain vector databases in three sentences."}],
)
print(response.choices[0].message.content)""",
        },
        "prompting": [
            "Model ids are provider/model - the provider prefix is part of the id.",
            "Free models rotate and are often busy; keep a paid fallback id in your config.",
            "Pin the provider suffix when you need a specific host's behaviour.",
            "Set a max price if you are scripting: an expensive model can appear mid-run.",
        ],
        "agent_notes": [
            "In opencode: pick openrouter and any model id from `opencode models openrouter`.",
            "It is the easiest way to test a model id in an agent before committing to a provider account.",
        ],
        "limits": [
            "The free tier is a low daily request count; it resets and rotates.",
            "Each provider has its own rate limit behind the same key.",
        ],
        "links": [
            ["Keys", "https://openrouter.ai/keys"],
            ["Models", "https://openrouter.ai/models"],
        ],
    },
    {
        "id": "antigravity",
        "name": "Antigravity CLI",
        "vendor": "Google",
        "tier": "free",
        "blurb": "Where Google moved Gemini CLI users: the new home for the newest Gemini models.",
        "best_for": [
            "The newest Gemini models in a terminal",
            "Anyone who used Gemini CLI on the unpaid or Google One tier",
            "Agentic coding on a free tier",
        ],
        "surfaces": [
            ["CLI", "The Antigravity CLI - the successor to Gemini CLI for those tiers"],
            ["API", "Same Gemini API and free tier as the Gemini entry above"],
        ],
        "api": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "style": "Google GenAI",
            "key_url": "https://aistudio.google.com/apikey",
            "env": "GEMINI_API_KEY",
            "install": "npm install -g @google/gemini-cli   # or the Antigravity CLI package",
            "code": """# Antigravity speaks to the same Gemini API surface
from google import genai

client = genai.Client()
print(client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Plan the migration of this service to FastAPI.",
).text)""",
        },
        "prompting": [
            "Everything from the Gemini entry applies - same models, same API, same limits.",
            "Expect the newest Gemini reasoning and coding behaviour here first.",
            "Keep GEMINI.md short; it is loaded on every single turn.",
            "Treat it as the place to try new Gemini features before they reach the stable CLI.",
        ],
        "agent_notes": [
            "Check the Antigravity CLI docs for the current package name - it moved out of the Gemini CLI repo.",
            "In opencode, the gemini provider still points at the same API endpoint.",
        ],
        "limits": [
            "Free-tier quotas follow the Gemini API limits.",
            "Migration notes: Google published a transition post when Gemini CLI moved.",
        ],
        "links": [
            ["Antigravity", "https://antigravity.google/product/antigravity-cli"],
            ["Gemini CLI docs", "https://geminicli.com/docs/"],
        ],
    },
]

HUB_INTRO = {
    "title": "Every major model, one page each",
    "body": (
        "Each entry answers the same four questions: where do I use it, how do I call it from code, how do I "
        "prompt it well, and how do I put it inside a coding agent. The API details were checked against each "
        "vendor's own documentation, and every model that has a free tier is marked as such."
    ),
    "principles": [
        [
            "Start free",
            "Gemini, Groq, Cerebras, OpenRouter's :free models and the OpenCode Zen catalogue are enough to learn everything on this site. Paid only when a specific task earns it.",
        ],
        [
            "One interface",
            "Almost every provider speaks the OpenAI chat-completions format. Change the base URL and the key and the same client code works everywhere.",
        ],
        [
            "Route by task",
            "Cheap and fast for exploration, strong and slow for the edit. A model router is a cost decision, not a technical one.",
        ],
        [
            "Watch the prefix",
            "A stable prompt prefix is cacheable, and a cached prefix is a fraction of the price. Put the volatile part last.",
        ],
    ],
}
