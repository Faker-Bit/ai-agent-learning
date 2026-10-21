"""The craft layer: how to drive an agent well, and how to pick a model."""

from __future__ import annotations

from typing import Any

LOOP_STAGES: list[dict[str, Any]] = [
    {
        "id": "prompt",
        "title": "You write the request",
        "body": "Everything downstream depends on this. Context, constraints, acceptance criteria - in the prompt or in the rules file.",
        "you_control": "State the outcome, the files in scope and what 'done' means.",
        "failure": "A vague request gets a broad, invented scope.",
    },
    {
        "id": "context",
        "title": "The agent assembles context",
        "body": "Rules files, @file references, the repo map, MCP tool definitions and the conversation history all get packed into the prompt.",
        "you_control": "Keep rules short. Reference files by name instead of pasting them.",
        "failure": "Too much context buries the instruction you actually care about.",
    },
    {
        "id": "model",
        "title": "The model decides the next action",
        "body": "The model either answers, or emits a tool call: read this file, run this command, search for this string.",
        "you_control": "Pick the model. Planning wants speed, editing wants capability.",
        "failure": "A model that is too weak for the task guesses instead of checking.",
    },
    {
        "id": "tools",
        "title": "Tools run",
        "body": "Files are read and written, commands are executed, MCP servers answer. Every tool call costs tokens and can fail.",
        "you_control": "Permissions decide what happens without asking you.",
        "failure": "Loose permissions plus an injection in a fetched page.",
    },
    {
        "id": "verify",
        "title": "The agent verifies",
        "body": "Good agents run the tests, the linter or the build before declaring victory. This loop is the whole difference between 'probably right' and 'verified'.",
        "you_control": "Require a check: 'run the tests and show me the output'.",
        "failure": "No verification step means confident, unchecked diffs.",
    },
    {
        "id": "review",
        "title": "You review",
        "body": "The diff is the evidence. Read it, narrow the scope, request changes, undo if needed.",
        "you_control": "Review the diff, not the narration.",
        "failure": "Accepting a summary instead of a diff.",
    },
]

CRAFT: list[dict[str, Any]] = [
    {
        "id": "scope",
        "title": "Give it a target, not a topic",
        "body": (
            "The difference between an agent that helps and one that rewrites your project is the request. "
            "Name the files, the behaviour and the check that proves it."
        ),
        "before": {
            "lines": [
                {"type": "input", "text": "improve the auth code"},
                {"type": "muted", "text": "  agent reads 40 files, refactors the auth layer, renames things,"},
                {"type": "muted", "text": "  changes 12 files, and stops when the diff is 900 lines"},
            ]
        },
        "after": {
            "lines": [
                {"type": "input", "text": "In backend/app/core/security.py, the token comparison uses == instead of"},
                {"type": "input", "text": "hmac.compare_digest. Change it to compare_digest, and add a test that"},
                {"type": "input", "text": "two different tokens are rejected. Run pytest -q afterwards."},
                {"type": "tool", "text": "  Edit(1)   backend/app/core/security.py"},
                {"type": "tool", "text": "  Write(1)  backend/tests/test_security.py"},
                {"type": "tool", "text": "  Bash(1)   pytest -q"},
                {"type": "success", "text": "  29 passed in 1.7s"},
            ]
        },
        "rule": "Files + behaviour + a check. Three parts, one sentence each.",
    },
    {
        "id": "plan",
        "title": "Plan before build, every time",
        "body": (
            "Every serious agent has a planning mode: opencode's Plan agent, Claude Code's plan mode, "
            "Cline's Plan/Act split, Aider's architect mode. They exist because arguing with a plan is "
            "cheap and rewriting finished code is not."
        ),
        "before": {
            "lines": [
                {"type": "muted", "text": "  build mode, straight to the edit"},
                {"type": "tool", "text": "  Write(6)  api/rate_limit.py, api/routes/*.py, tests/..."},
                {"type": "warn", "text": "  ! 6 files changed  |  the limit is applied per-path, not per-client"},
            ]
        },
        "after": {
            "lines": [
                {"type": "muted", "text": "  plan mode first"},
                {"type": "output", "text": "  Plan"},
                {"type": "output", "text": "   1. middleware in app/core/rate_limit.py - one instance, app-wide"},
                {"type": "output", "text": "   2. key on client IP + route template"},
                {"type": "output", "text": "   3. exempt /api/health and OPTIONS"},
                {"type": "output", "text": "   4. tests: allow, block, exempt"},
                {"type": "input", "text": "the key should include the route template - show me where routes are mounted"},
                {"type": "output", "text": "  Revised: key on app.state.router_path + client IP"},
            ]
        },
        "rule": "Plan, then argue, then build. The plan is where the thinking happens.",
    },
    {
        "id": "context",
        "title": "Point at files, do not paste them",
        "body": (
            "Agents can open files. Pasting the file instead burns tokens, goes stale and hides the rest of "
            "the repo from the model. Reference by path and let the agent pull what it needs."
        ),
        "before": {
            "lines": [
                {"type": "input", "text": "here is our auth module, it is 400 lines, see below ..."},
                {"type": "muted", "text": "  ... 400 lines pasted into the prompt ..."},
                {"type": "muted", "text": "  ... and the same 400 lines pasted again next turn ..."},
            ]
        },
        "after": {
            "lines": [
                {"type": "input", "text": "how does @backend/app/core/security.py verify a token?"},
                {"type": "tool", "text": "  Read(1)   backend/app/core/security.py"},
                {"type": "output", "text": "  hmac.compare_digest against the signature, then a DB lookup for expiry"},
            ]
        },
        "rule": "@file in opencode, @Docs in Cursor, /add in aider, file mentions in Claude Code.",
    },
    {
        "id": "verify",
        "title": "Make the agent prove it",
        "body": (
            "A model claiming 'done' is a hypothesis. A test run is evidence. Put the check in the prompt "
            "and the agent will do it every time, without being reminded."
        ),
        "before": {
            "lines": [
                {"type": "tool", "text": "  Edit(2)   backend/app/api/routes/health.py"},
                {"type": "success", "text": "  ok Added the /health endpoint as requested"},
            ]
        },
        "after": {
            "lines": [
                {"type": "tool", "text": "  Edit(2)   backend/app/api/routes/health.py"},
                {"type": "tool", "text": "  Write(1)  backend/tests/test_health.py"},
                {"type": "tool", "text": "  Bash(1)   cd backend && pytest -q"},
                {"type": "output", "text": "  1 failed, 27 passed"},
                {"type": "tool", "text": "  Edit(1)   backend/tests/test_health.py"},
                {"type": "tool", "text": "  Bash(1)   cd backend && pytest -q"},
                {"type": "success", "text": "  28 passed in 1.9s"},
            ]
        },
        "rule": "End every request with the command that proves the work: pytest, npm run build, cargo test.",
    },
    {
        "id": "rules",
        "title": "Put the rules in a file, not in your memory",
        "body": (
            "AGENTS.md, CLAUDE.md and GEMINI.md are the same idea: project knowledge that survives between "
            "sessions and gets shared with the team. Write the commands, the layout and the three traps."
        ),
        "before": {
            "lines": [
                {"type": "input", "text": "remember to always run the linter before you commit"},
                {"type": "muted", "text": "  (works, until the session ends and you forget to say it again)"},
            ]
        },
        "after": {
            "lines": [
                {"type": "muted", "text": "  # AGENTS.md - committed, read every session"},
                {"type": "accent", "text": "  - Run `cd frontend && npm run lint` before claiming a change is done"},
                {"type": "accent", "text": "  - Never edit backend/alembic/versions by hand"},
                {"type": "accent", "text": "  - Backend is FastAPI + SQLAlchemy async; keep handlers thin"},
                {"type": "muted", "text": "  next session: rules are already in context"},
            ]
        },
        "rule": "One rules file per repo. Commit it. Keep it under a page.",
    },
    {
        "id": "permissions",
        "title": "Give the agent a leash you can see",
        "body": (
            "Permission systems exist so that a wrong instruction costs a keystroke instead of a deleted "
            "database. Use them: ask for writes, allow reads, deny the dangerous commands."
        ),
        "before": {
            "lines": [
                {"type": "muted", "text": "  everything allowed, no prompts"},
                {"type": "tool", "text": "  Bash(1)   rm -rf ./data"},
                {"type": "warn", "text": "  ! gone. that was not what you asked for."},
            ]
        },
        "after": {
            "lines": [
                {"type": "muted", "text": "  // opencode.json"},
                {"type": "accent", "text": "  \"permission\": {"},
                {"type": "accent", "text": "    \"edit\": \"ask\","},
                {"type": "accent", "text": "    \"bash\": { \"*\": \"ask\", \"git status\": \"allow\", \"pytest*\": \"allow\" }"},
                {"type": "accent", "text": "  }"},
                {"type": "muted", "text": "  rm -rf now stops and asks"},
            ]
        },
        "rule": "read: allow | write: ask | destructive commands: deny",
    },
    {
        "id": "budget",
        "title": "Watch the tokens, route the models",
        "body": (
            "Most agent cost is context re-reading, not thinking. Route cheap models to exploration and "
            "strong models to edits, and read the stats command until the numbers make sense."
        ),
        "before": {
            "lines": [
                {"type": "muted", "text": "  one expensive model for everything"},
                {"type": "output", "text": "  1.42M input tokens  |  $12.80 for one afternoon"},
            ]
        },
        "after": {
            "lines": [
                {"type": "muted", "text": "  // opencode.json"},
                {"type": "accent", "text": "  \"agent\": {"},
                {"type": "accent", "text": "    \"plan\":  { \"model\": \"opencode/mimo-v2.5-flash-free\" },"},
                {"type": "accent", "text": "    \"build\": { \"model\": \"opencode/mimo-v2.5-pro-free\" }"},
                {"type": "accent", "text": "  }"},
                {"type": "output", "text": "  1.42M input tokens  |  $0.38 for the same afternoon"},
            ]
        },
        "rule": "Cheap model for the plan, strong model for the code, stats for the truth.",
    },
]

MODEL_GUIDE: list[dict[str, Any]] = [
    {
        "id": "pick",
        "title": "Pick by task, not by leaderboard",
        "body": (
            "A frontier model is the wrong tool for half of what agents do. Reading a file, grepping a "
            "symbol, renaming a variable - these want speed. Writing a tricky diff wants capability."
        ),
        "rows": [
            ["Plan / explore / read", "Fast small model (flash tier, local 8B)", "Cheap, high volume, enough to read code"],
            ["Edit / refactor", "Mid-tier coding model", "Balance of price and patch quality"],
            ["Architecture / hard bugs", "Frontier reasoning model", "Worst case is worth the price"],
            ["Bulk chores (docs, tests, renames)", "Free tier or local model", "Volume work should never cost money"],
        ],
    },
    {
        "id": "context",
        "title": "Context window is the real limit",
        "body": (
            "Before choosing a model, count what you are about to send: rules file, repo map, history, "
            "tool outputs. A 200K window does not help if the agent re-reads the repository on every turn."
        ),
        "rows": [
            ["Typical repo session", "40-120K", "Most agent loops fit in a large window"],
            ["Large monorepo with repo map", "120-400K", "Long-context models start to pay off"],
            ["Whole-book context", "400K+", "Rare; usually a sign you want retrieval instead"],
        ],
    },
    {
        "id": "free",
        "title": "The free tiers are genuinely usable",
        "body": (
            "Free catalogues (OpenCode Zen, Groq, Cerebras, NVIDIA NIM, Gemini flash, OpenRouter's :free "
            "models) are enough for learning, for bulk chores and for a whole project if you route "
            "sensibly. Start free, upgrade only where a specific task needs it."
        ),
        "rows": [
            ["Gemini flash", "~1,500 requests/day", "Long context, generous quota, no card"],
            ["Groq", "~14,400 requests/day (8B)", "Fastest responses; great for exploration agents"],
            ["OpenCode Zen", "9 free models", "Curated, verified, works with opencode out of the box"],
            ["Cerebras", "~1.5M tokens/day", "Very high throughput for bulk work"],
            ["OpenRouter :free", "50 requests/day", "Any model, rotate the id when one is busy"],
        ],
    },
    {
        "id": "local",
        "title": "Local models are the privacy play",
        "body": (
            "Ollama and LM Studio expose an OpenAI-compatible endpoint, so any CLI agent can use a model "
            "that never leaves the machine. Point the agent at http://localhost:11434/v1 and carry on."
        ),
        "rows": [
            ["Ollama", "http://localhost:11434/v1", "llama3.2, qwen2.5-coder, gemma3"],
            ["LM Studio", "http://localhost:1234/v1", "any loaded GGUF model"],
            ["vLLM", "http://localhost:8000/v1", "your own fine-tune, served locally"],
        ],
    },
    {
        "id": "reasoning",
        "title": "Reasoning effort is a dial, not a personality",
        "body": (
            "Reasoning models let you spend more compute per answer. In opencode that is a model variant "
            "(ctrl+t cycles it), and in an agent config you can pass provider-specific options such as "
            "reasoningEffort straight through. Turn it up for hard architecture, turn it down for "
            "mechanical edits - the latency and token bill scale with it."
        ),
        "rows": [
            ["Mechanical edit", "low effort", "Fast, cheap, and usually enough"],
            ["Multi-file refactor", "medium", "The default for build agents"],
            ["Architecture or a nasty bug", "high", "Slow and pricey, worth it here"],
            ["Cost control", "step limit", "A step cap bounds the spend more reliably"],
        ],
    },
    {
        "id": "caching",
        "title": "Prompt caching is free speed",
        "body": (
            "Most providers cache the stable prefix of a prompt - your rules file, the repo map, the tool "
            "definitions. Keep that prefix byte-identical between requests and the cached portion costs "
            "a fraction. Put the volatile part (your new message) at the end, never the front."
        ),
        "rows": [
            ["Stable prefix", "rules + tools + repo map", "Cache hit, cheap"],
            ["Volatile tail", "your latest message", "Always re-read"],
            ["Don't", "reorder the system prompt", "One changed byte invalidates the cache"],
            ["Measure it", "opencode stats", "Compare token counts across runs"],
        ],
    },
    {
        "id": "routers",
        "title": "Routers pick the model for you",
        "body": (
            "A router sits between the agent and several providers and picks per task - a cheap model "
            "for exploration, a frontier one for the diff. This is the same routing you would write in "
            "opencode.json, done dynamically, and it is where multi-provider agents earn their keep."
        ),
        "rows": [
            ["opencode.json", "static per agent", "Plan to cheap, build to strong"],
            ["Provider router", "dynamic per request", "Picks by difficulty or quota"],
            ["Control plane", "dynamic per team", "Rotation when a provider runs out"],
            ["Watch for", "silent fallbacks", "You get a worse answer and never know why"],
        ],
    },
]

CONFIG_SNIPPETS: list[dict[str, str]] = [
    {
        "title": "Route a cheap model to planning and a strong one to edits",
        "language": "json",
        "code": """{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan":  { "model": "opencode/mimo-v2.5-flash-free" },
    "build": { "model": "opencode/mimo-v2.5-pro-free" }
  }
}""",
    },
    {
        "title": "Bring your own provider with any OpenAI-compatible endpoint",
        "language": "json",
        "code": """{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "my-gateway": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "https://api.example.com/v1" },
      "models": { "my-model": { "name": "My Model" } }
    }
  }
}""",
    },
    {
        "title": "Ask before writes, allow the boring reads",
        "language": "json",
        "code": """{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": { "*": "ask", "git status": "allow", "pytest*": "allow" }
  }
}""",
    },
    {
        "title": "A custom agent that can only read",
        "language": "markdown",
        "code": """---
description: Reviews code for security issues
mode: subagent
model: opencode/mimo-v2.5-flash-free
permission:
  edit: deny
  bash:
    "*": ask
    "grep *": allow
---
You are a security reviewer. Report findings; never change files.""",
    },
]


def comparison_matrix() -> list[dict[str, Any]]:
    """Rows for the agent comparison table."""
    return [
        {"feature": "Runs in a terminal", "values": {"opencode": True, "codex": True, "gemini": True, "claude": True, "aider": True, "goose": True, "openhands": True}},
        {"feature": "Ships an IDE extension", "values": {"opencode": True, "codex": True, "gemini": True, "claude": True, "aider": False, "goose": True, "openhands": False}},
        {"feature": "Open source", "values": {"opencode": True, "codex": True, "gemini": True, "claude": False, "aider": True, "goose": True, "openhands": True}},
        {"feature": "Works with any model provider", "values": {"opencode": True, "codex": False, "gemini": False, "claude": False, "aider": True, "goose": True, "openhands": True}},
        {"feature": "Free tier that is enough to learn on", "values": {"opencode": True, "codex": True, "gemini": True, "claude": False, "aider": True, "goose": True, "openhands": True}},
        {"feature": "MCP servers", "values": {"opencode": True, "codex": True, "gemini": True, "claude": True, "aider": False, "goose": True, "openhands": True}},
        {"feature": "Custom subagents", "values": {"opencode": True, "codex": False, "gemini": False, "claude": True, "aider": False, "goose": False, "openhands": True}},
        {"feature": "Scriptable / headless", "values": {"opencode": True, "codex": True, "gemini": True, "claude": True, "aider": True, "goose": True, "openhands": True}},
        {"feature": "Every change is reversible", "values": {"opencode": True, "codex": True, "gemini": True, "claude": True, "aider": True, "goose": False, "openhands": False}},
    ]
