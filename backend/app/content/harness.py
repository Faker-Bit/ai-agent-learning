"""Harnesses, skills and the protocols around them.

The harness is the scaffolding around a model: the tool protocol, the context
manager, the loop, the policy layer, the memory. Projects here are real and
verified against GitHub on 2026-10-20; star counts are a snapshot.
"""

from __future__ import annotations

from typing import Any

HARNESS_LAYERS: list[dict[str, Any]] = [
    {
        "id": "model",
        "title": "Model",
        "body": "The raw next-token predictor. It knows nothing about your repo until the harness puts your files in front of it.",
        "control": "Which model, which reasoning effort, which temperature, how many tokens.",
        "fails": "A model that cannot do the task guesses instead of checking, and the harness never finds out.",
    },
    {
        "id": "tools",
        "title": "Tool protocol",
        "body": "How the model asks for things: read, edit, bash, grep, and whatever an MCP server exposes. The schema is the API.",
        "control": "Tool descriptions, argument schemas, which tools exist at all.",
        "fails": "A vague tool description produces vague arguments, and the model retries forever.",
    },
    {
        "id": "context",
        "title": "Context manager",
        "body": "What gets assembled into the prompt: rules, repo map, file contents, history, tool results. The most under-engineered part of every harness.",
        "control": "What you inline, what you reference, when you compact.",
        "fails": "The instruction you care about gets buried under 60K tokens of file contents.",
    },
    {
        "id": "loop",
        "title": "Agent loop",
        "body": "Observe, decide, act, observe again. Stop conditions, step budgets and retries live here.",
        "control": "Max steps, retry policy, whether it re-plans or ploughs ahead.",
        "fails": "A loop with no stop condition burns tokens until it hits a rate limit.",
    },
    {
        "id": "policy",
        "title": "Policy layer",
        "body": "Permissions, approvals, sandboxes, allow-lists. The part that decides what the agent can do without asking you.",
        "control": "Ask, allow or deny per tool, per command pattern, per agent.",
        "fails": "Everything allowed by default, so one bad turn deletes the database.",
    },
    {
        "id": "memory",
        "title": "Memory",
        "body": "What survives between sessions: rules files, skills, long-term memory stores, session history you can resume.",
        "control": "What is written, when it is written, and how it is retrieved.",
        "fails": "Memory that only ever appends, so yesterday's wrong answer fights today's right one.",
    },
    {
        "id": "interface",
        "title": "Interface",
        "body": "The TUI, the IDE panel, the web UI, the headless API. The same harness behind four different surfaces.",
        "control": "Where the agent lives for you - terminal, editor, browser, pipeline.",
        "fails": "A UI that hides the tool calls, so you cannot tell what it actually did.",
    },
]

HARNESS_PROJECTS: list[dict[str, Any]] = [
    {
        "id": "pi",
        "name": "pi",
        "repo": "earendil-works/pi",
        "stars": "116k",
        "license": "MIT",
        "tagline": "AI agent toolkit: unified LLM API, agent loop, TUI, coding agent CLI",
        "why": "It is the harness as a library rather than a product. Read the loop, then read the tools, then read the TUI - it is the shortest path to understanding what every agent does between your prompt and the edit.",
        "steal": "A minimal agent loop you can read in one sitting.",
    },
    {
        "id": "openclaw",
        "name": "openclaw",
        "repo": "openclaw/openclaw",
        "stars": "392k",
        "license": "MIT",
        "tagline": "The AI that really does things. Any OS. Any Platform.",
        "why": "The most-starred personal agent on GitHub. It shows how far the harness idea stretches when the loop is driven by scheduled tasks and real-world tools rather than a person at a terminal.",
        "steal": "Scheduling and long-running task patterns.",
    },
    {
        "id": "hermes",
        "name": "hermes-agent",
        "repo": "NousResearch/hermes-agent",
        "stars": "255k",
        "license": "MIT",
        "tagline": "The agent that grows with you",
        "why": "Built around persistence: the agent keeps what it learned and gets better across sessions. The memory layer is the product, not a feature.",
        "steal": "Memory that is written deliberately and retrieved selectively.",
    },
    {
        "id": "little-coder",
        "name": "little-coder",
        "repo": "itayinbarr/little-coder",
        "stars": "2.7k",
        "license": "Apache-2.0",
        "tagline": "A harness optimized to smaller LLMs",
        "why": "Every other harness assumes a frontier model. This one is engineered around a 7B-class model: tighter context, fewer tools, shorter loops. The best proof that the harness, not the model, does most of the work.",
        "steal": "Tool minimisation and context discipline for cheap models.",
    },
    {
        "id": "late-cli",
        "name": "late-cli",
        "repo": "mlhher/late-cli",
        "stars": "446",
        "license": "MIT",
        "tagline": "High-performance AI agent for long-horizon tasks and local models",
        "why": "Focuses on the two things that break real projects: tasks that run for hours, and models that run on your own machine.",
        "steal": "Resumable long-horizon runs and local-model paths.",
    },
    {
        "id": "alphacode",
        "name": "alphacode",
        "repo": "dragonked2/alphacode",
        "stars": "369",
        "license": "MIT",
        "tagline": "Free MIT AI coding agent - no API key needed. Built-in free model, or bring your own",
        "why": "The zero-friction path: no account, no key, no credit card. Useful to feel the loop before you spend money on it.",
        "steal": "A no-setup first run.",
    },
    {
        "id": "org2",
        "name": "ORG2",
        "repo": "org2AI/ORG2",
        "stars": "2.6k",
        "license": "AGPL-3.0",
        "tagline": "System of record for how agents build software: built-in rust harness and 20+ CLIs",
        "why": "The interesting idea is the record: every agent action becomes an artifact you can query later. When three agents touch one repo, the history is the product.",
        "steal": "Structured, queryable agent history.",
    },
    {
        "id": "cli-agent-orchestrator",
        "name": "cli-agent-orchestrator",
        "repo": "awslabs/cli-agent-orchestrator",
        "stars": "1.4k",
        "license": "Apache-2.0",
        "tagline": "Multi-agent orchestration for AI coding CLIs - Claude Code, Kiro, Codex and more",
        "why": "From AWS, and deliberately CLI-first. It treats the CLIs you already have as interchangeable workers instead of asking you to migrate.",
        "steal": "Fan-out patterns across existing CLIs.",
    },
]

SKILL_FORMAT: dict[str, Any] = {
    "id": "skill",
    "title": "Skills: the Agent Skills format",
    "body": (
        "A skill is a folder with one file in it: SKILL.md. The harness advertises the name and "
        "description of every skill it finds, and the model loads the full text on demand. That is "
        "progressive disclosure - the cheap part (a name and one line) is always in context, the "
        "expensive part (the whole procedure) is read only when the task calls for it."
    ),
    "why_it_matters": (
        "Rules files are always loaded, so they should be short. Skills are loaded on demand, so "
        "they can be long and specific. That split is what lets you keep a thousand procedures "
        "around without paying for them in every session."
    ),
    "locations": [
        ".opencode/skills/<name>/SKILL.md",
        "~/.config/opencode/skills/<name>/SKILL.md",
        ".claude/skills/<name>/SKILL.md",
        ".agents/skills/<name>/SKILL.md",
    ],
    "frontmatter": {
        "name": "required, 1-64 chars, lowercase with single hyphens, must match the folder name",
        "description": "required, 1-1024 chars, specific enough for the model to choose correctly",
        "license": "optional",
        "compatibility": "optional",
        "metadata": "optional string map - opencode/slash and opencode/autoinvoke live here",
    },
    "example": """---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
  opencode/slash: "true"
  opencode/autoinvoke: "false"
---
## What I do
- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command
## When to use me
Use this when you are preparing a tagged release.""",
    "permissions": """{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}""",
    "troubleshooting": [
        "SKILL.md must be spelled in all caps",
        "Frontmatter needs both name and description",
        "Names must be unique across every discovery location",
        "A denied skill is hidden from the agent entirely",
        'metadata opencode/autoinvoke: "false" hides it from model-facing selection',
    ],
}

SKILL_PACKAGES: list[dict[str, Any]] = [
    {
        "id": "superpowers",
        "name": "superpowers",
        "repo": "obra/superpowers",
        "stars": "302k",
        "license": "MIT",
        "tagline": "An agentic skills framework and software development methodology that works",
        "what": "Skills plus a method: brainstorming, planning, subagent-driven development, and a review loop. The methodology is the point - the skills are just how it is delivered.",
    },
    {
        "id": "agent-skills",
        "name": "agent-skills",
        "repo": "addyosmani/agent-skills",
        "stars": "108k",
        "license": "MIT",
        "tagline": "Production-grade engineering skills for AI coding agents",
        "what": "A large catalogue of engineering practices formatted as skills - the cheapest way to see how the format scales.",
    },
    {
        "id": "mattpocock-skills",
        "name": "skills",
        "repo": "mattpocock/skills",
        "stars": "298k",
        "license": "MIT",
        "tagline": "Skills for Real Engineers. Straight from my .agents directory",
        "what": "A real engineer's personal skill set, published as-is. Good for copying the voice and the length of a well-written skill.",
    },
    {
        "id": "gstack",
        "name": "gstack",
        "repo": "garrytan/gstack",
        "stars": "137k",
        "license": "MIT",
        "tagline": "Garry Tan's exact Claude Code setup: 23 opinionated tools",
        "what": "23 tools that each pretend to be a different role - CEO, designer, engineering manager. Shows how far the role-play pattern goes.",
    },
    {
        "id": "ecc",
        "name": "ECC",
        "repo": "affaan-m/ECC",
        "stars": "284k",
        "license": "MIT",
        "tagline": "The agent harness performance optimization system: skills, instincts, memory, security, research",
        "what": "Treats the harness as the tunable surface - instincts, memory hygiene and security rules, all packaged as skills.",
    },
    {
        "id": "caveman",
        "name": "caveman",
        "repo": "JuliusBrussee/caveman",
        "stars": "113k",
        "license": "MIT",
        "tagline": "Why use many tokens when few tokens do the trick - a skill plus a proxy that cuts context",
        "what": "A proxy that rewrites requests to be smaller. A concrete demonstration that the harness, not the model, controls your bill.",
    },
    {
        "id": "ponytail",
        "name": "ponytail",
        "repo": "DietrichGebert/ponytail",
        "stars": "169k",
        "license": "MIT",
        "tagline": "Makes your AI agent think like the laziest senior dev in the room",
        "what": "A behaviour skill: the best code is the code you never write. Cheap tokens, fewer diffs.",
    },
    {
        "id": "claude-mem",
        "name": "claude-mem",
        "repo": "thedotmack/claude-mem",
        "stars": "101k",
        "license": "MIT",
        "tagline": "Persistent context across sessions for every agent",
        "what": "Captures what the agent did and makes it retrievable next session. The memory layer, shipped.",
    },
    {
        "id": "spec-kit",
        "name": "spec-kit",
        "repo": "github/spec-kit",
        "stars": "142k",
        "license": "MIT",
        "tagline": "Toolkit to help you get started with spec-driven development",
        "what": "From GitHub itself. The specification-first workflow: write the spec, generate the plan, then let the agent implement against it.",
    },
    {
        "id": "embeddedskills",
        "name": "embeddedskills",
        "repo": "zhinkgit/embeddedskills",
        "stars": "756",
        "license": "MIT",
        "tagline": "An open-source collection of embedded development and debugging skills",
        "what": "Domain-specific skills (embedded, drivers, protocols). Shows the format working for hardware work.",
    },
]

ORCHESTRATORS: list[dict[str, Any]] = [
    {
        "id": "agent-deck",
        "name": "agent-deck",
        "repo": "asheshgoplani/agent-deck",
        "stars": "1.1k",
        "kind": "Terminal",
        "what": "One TUI that hosts sessions from Claude, Gemini, opencode, Codex and more side by side.",
    },
    {
        "id": "atlas",
        "name": "atlas",
        "repo": "pacifio/atlas",
        "stars": "9.6k",
        "kind": "Version control",
        "what": "Source control for agents: run several coding agents, track their changes, query them in one place.",
    },
    {
        "id": "nimbalyst",
        "name": "nimbalyst",
        "repo": "nimbalyst/nimbalyst",
        "stars": "1.9k",
        "kind": "Workspace",
        "what": "An open-source visual workspace for Claude Code, Codex and opencode.",
    },
    {
        "id": "amux",
        "name": "amux",
        "repo": "mixpeek/amux",
        "stars": "545",
        "kind": "Control plane",
        "what": "Run an AI engineering team: parallel Claude Code, Codex and more against one backlog.",
    },
    {
        "id": "claudexor",
        "name": "claudexor",
        "repo": "razzant/claudexor",
        "stars": "515",
        "kind": "Control plane",
        "what": "Multi-harness control plane with quota-aware rotation across providers.",
    },
    {
        "id": "cc-switch",
        "name": "cc-switch",
        "repo": "farion1231/cc-switch",
        "stars": "146k",
        "kind": "Desktop",
        "what": "A cross-platform desktop switcher for Claude Code, Codex, opencode, openclaw and Grok Build.",
    },
    {
        "id": "cli-continues",
        "name": "cli-continues",
        "repo": "yigitkonur/cli-continues",
        "stars": "1.5k",
        "kind": "Bridge",
        "what": "Resume an AI coding session in a different tool - Claude Code, Copilot, Gemini, Codex, Cursor.",
    },
    {
        "id": "history-viewer",
        "name": "claude-code-history-viewer",
        "repo": "jhlee0409/claude-code-history-viewer",
        "stars": "2.2k",
        "kind": "Analytics",
        "what": "Browse, search and analyse your agent history offline - Claude Code, Codex CLI, Copilot, Gemini CLI, Cursor, opencode.",
    },
]

PROTOCOLS: list[dict[str, Any]] = [
    {
        "id": "mcp",
        "name": "MCP - Model Context Protocol",
        "what": "A standard for exposing tools to a model. Local servers run a command; remote servers are a URL. Tools appear alongside built-ins, prefixed with the server name.",
        "portable": "Yes. The same server works in opencode, Claude Code, Gemini CLI and anything else that speaks MCP.",
        "cost": "Every tool definition sits in the context window. Enable the servers a task needs, not the ones you might need.",
        "example": '"mcp": { "context7": { "type": "remote", "url": "https://mcp.context7.com/mcp" } }',
    },
    {
        "id": "acp",
        "name": "ACP - Agent Client Protocol",
        "what": "The editor-side counterpart to MCP: a standard for how an editor talks to an agent. opencode ships an ACP server over stdio.",
        "portable": "Yes, in the other direction. One agent, many editors.",
        "cost": "Low. It is a control channel, not a pile of tool schemas.",
        "example": "opencode acp",
    },
    {
        "id": "lsp",
        "name": "LSP - Language Server Protocol",
        "what": "Definitions, references, diagnostics and symbols. Editors have used it for years; harnesses use it to give a model real code intelligence instead of grep.",
        "portable": "Widely supported.",
        "cost": "Cheap when the server is local. opencode can download language servers automatically.",
        "example": "The lsp tool answers \"where is this symbol defined\" without reading the file.",
    },
    {
        "id": "hooks",
        "name": "Hooks",
        "what": "Your own commands, run on tool events. The cheapest way to make an agent verify its own work: run the test suite after every edit.",
        "portable": "Conceptually yes, the syntax is per-harness.",
        "cost": "It runs on every matching event. A slow hook trains you to ignore it.",
        "example": '"PostToolUse": [{ "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "pytest -q" }] }]',
    },
    {
        "id": "plugins",
        "name": "Plugins",
        "what": "A packaged extension for the harness: tools, commands, hooks and config in one installable unit.",
        "portable": "Usually harness-specific.",
        "cost": "A plugin is trusted code with your permissions.",
        "example": "opencode plugin <module>",
    },
    {
        "id": "commands",
        "name": "Slash commands",
        "what": "Named prompts you can invoke. Arguments are positional ($1, $2) or free-form ($ARGUMENTS); shell output is injected with !`cmd`; files are pulled in with @path.",
        "portable": "The convention is spreading across harnesses even where the syntax differs.",
        "cost": "Free. This is the cheapest automation you can add to any agent.",
        "example": "/review $1 !`git diff --stat` @src/api.ts",
    },
]

CONTEXT_PLAYBOOK: list[dict[str, Any]] = [
    {
        "id": "inline-vs-reference",
        "title": "Inline the rules, reference the code",
        "body": "Always-loaded context should be a page, not a manual. Put the commands and conventions in AGENTS.md; point at the file that holds the implementation.",
        "bad": "Pasting 400 lines of a module into every prompt.",
        "good": "@backend/app/core/security.py - and let the agent read it.",
    },
    {
        "id": "compaction",
        "title": "Compact at boundaries",
        "body": "When a session gets long, summarise the finished work and start a new one. Compaction mid-debug-loop loses the thing you were actually chasing.",
        "bad": "Compacting in the middle of a failing test.",
        "good": "Compact right after a feature lands, while the plan is still clean.",
    },
    {
        "id": "subagents",
        "title": "Subagents for side quests",
        "body": "A read-only exploration subagent can sweep the repo and return a summary, without polluting the main context with 40 file contents.",
        "bad": "Your main session reads 40 files to answer one question.",
        "good": "@explore find every caller of parse_config, then report.",
    },
    {
        "id": "memory-files",
        "title": "Memory files over memory features",
        "body": "A plain markdown file you can read, edit and diff is better than a hidden store you cannot inspect. Put the facts in the repo.",
        "bad": "The agent 'remembers' something you cannot see or correct.",
        "good": "DECISIONS.md in the repo, edited by a human and by the agent.",
    },
    {
        "id": "budget",
        "title": "Give every run a budget",
        "body": "Set a step limit and a token ceiling. A loop with no stop condition is a bill with no cap.",
        "bad": "The agent retries the same failing command until the provider rate-limits you.",
        "good": '"steps": 8 on the agent, plus a token ceiling in the model config.',
    },
]
