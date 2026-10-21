# Agent Pilot

**Learn to drive AI coding agents.** A hands-on website with animated terminal walkthroughs of
opencode, OpenCode Zen, Codex CLI, Claude Code, Gemini CLI, Aider and the IDE agents — plus a real
command reference and a guide to choosing models.

**Stack:** Python 3.12+ / FastAPI (content API + static host) · React 19 / TypeScript / Vite / Tailwind CSS 4 / Framer Motion

---

## What's on the site

| Section | What it gives you |
|---|---|
| **Hero** | A looping, animated opencode session - prompt, tool calls, test run, verified result. |
| **How it works** | The six-stage loop every agent shares: request, context, model, tools, verify, review. Auto-advancing diagram. |
| **The harness** | The seven layers of a harness (model, tool protocol, context manager, loop, policy, memory, interface) plus 8 real harness projects from GitHub - openclaw, pi, hermes-agent, little-coder, late-cli, alphacode, ORG2, cli-agent-orchestrator - with what to steal from each. |
| **Skills** | The Agent Skills format end to end: SKILL.md frontmatter, discovery paths, permissions by pattern, slash exposure, the five reasons a skill does not show up - and 10 real skill packages (superpowers, agent-skills, gstack, ECC, spec-kit, claude-mem, ponytail, caveman). |
| **Protocols** | MCP, ACP, LSP, hooks, plugins and slash commands - what each is, whether it is portable, what it costs you in context. |
| **Context playbook** | Five rules for keeping the context window honest: inline the rules, reference the code, compact at boundaries, subagents for side quests, memory files over memory features, and a budget for every run. |
| **Agent directory** | 28 agents (CLI, IDE, models, platforms, control planes) with install commands, star counts, what each is for and the commands worth memorising. Filterable by kind. |
| **Walkthroughs** | 9 full guided sessions as animated terminals: step list, narration, copyable command, real output, tips. Play/pause, step, speed control, auto-advance. Includes a walkthrough that writes an agent skill from scratch. |
| **The craft** | 7 prompting rules, each with an animated before/after terminal, plus 4 ready-to-paste config files. |
| **Models** | How to pick a model by task, context-window reality, real free tiers, local models, reasoning effort, prompt caching, routers - plus the full catalogue with free/paid flags. |
| **Command reference** | 130+ commands across every agent, searchable and filterable by agent and group, copyable in one click. |
| **Comparison** | Side-by-side capability matrix for the CLI agents. |

Every command and every flag on the site was taken from the tool's own documentation - no invented
syntax. Where a project does not document a stable install command, the site says so instead of
guessing. Star counts are a GitHub snapshot from 20 October 2026.

---

## Quick start (Windows)

```bat
:: 1. Prerequisites: Python 3.12+ and Node.js 20+ on PATH
:: 2. From the project root:
start.bat
```

Or with PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

The script creates the venv, installs dependencies, builds the frontend and starts the API. The built
SPA is served by FastAPI itself, so there is one URL:

- **Site:** http://127.0.0.1:8010
- **Content API:** http://127.0.0.1:8010/api/site
- **API docs:** http://127.0.0.1:8010/docs

Stop with `.\stop.ps1`.

### Manual setup

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8010 --reload

:: in a second shell
cd frontend
npm install
npm run dev          :: http://127.0.0.1:5173, proxies /api to :8010
```

### Tests

```bat
cd backend
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe tools\smoke.py    :: boots the real server and checks every endpoint
```

---

## Content model

All site content is Python data under `backend/app/content/`, served as one JSON payload from
`/api/site`. Editing those files changes the site on the next reload.

| File | What it holds |
|---|---|
| `content/agents.py` | The agent directory: install commands, highlights, memorable commands, star counts. |
| `content/walkthroughs.py` | The walkthroughs: steps with narration, commands and terminal lines. |
| `content/cheatsheet.py` | The command reference rows. |
| `content/guide.py` | The loop stages, the craft rules, the model guide, config snippets, comparison matrix. |
| `content/harness.py` | Harness layers, harness projects, the skills format, skill packages, orchestrators, protocols, the context playbook. |
| `providers/registry.py` | Provider metadata and the model catalogue (free/paid flags, context windows). |

Terminal lines are typed with a `type` that drives the colour:

`input` · `output` · `tool` · `success` · `warn` · `muted` · `accent` · `info` · `diff`

See [docs/CONTENT.md](docs/CONTENT.md) for the exact schema and how to add an agent or a walkthrough.

---

## Architecture

```
backend/
  app/
    core/          config, logging with secret redaction, errors, rate limiting
    content/       the site content (agents, walkthroughs, cheatsheet, guide)
    providers/     provider metadata + model catalogue
    api/routes/    health, site (the content payload)
  tests/           integrity tests for every content file + API tests
  tools/smoke.py   boots the real server and asserts the payload
frontend/
  src/components/
    terminal/      TerminalFrame, TypedLines, StaticLines, useReveal, CopyButton
    site/          Hero, LoopSection, AgentsSection, WalkthroughsSection, WalkthroughPlayer,
                   CraftSection, ModelsSection, CheatsheetSection, CompareSection, Chrome
  src/pages/       Home, WalkthroughPage, AgentPage
```

**Animation engine.** `useReveal` counts visible characters across a block of terminal lines and
advances on a timer scaled by speed; `TypedLines` slices each line at its character offset so the
output appears character by character with a blinking caret. The walkthrough player keeps completed
steps static and types only the active step, then auto-advances.

**Content delivery.** One `GET /api/site` returns agents, walkthroughs, cheatsheet, loop stages, craft
rules, model guides, config snippets, the comparison matrix, providers and models. The frontend caches
it for five minutes and renders everything client-side.

---

## Configuration

Nothing is required. `backend/.env` (see `.env.example`) can hold provider keys, which the site uses
only to mark a provider as *key present* on the Models page — it never calls a model API.

| Variable | Purpose |
|---|---|
| `AMT_ENV` | `development` / `production` (production hides `/docs`) |
| `AMT_PORT` | API port (default `8010`) |
| `AMT_CORS_ORIGINS` | Comma-separated frontend origins (dev mode only) |
| `*_API_KEY` | Provider keys, used for the "key present" badge |
| `*_BASE_URL` | Endpoint overrides shown in the model tables (Ollama, LM Studio, …) |

---

## Extending the site

- **Add an agent** — append to `backend/app/content/agents.py`, then add its commands to
  `content/cheatsheet.py`. `tests/test_site.py` checks that every agent has an install command, at
  least four highlights, a command list, and that walkthrough links resolve.
- **Add a walkthrough** — append to `backend/app/content/walkthroughs.py`. Each step needs a title,
  narration, and at least one terminal line; the integrity test enforces the shape.
- **Add a command** — append to `backend/app/content/cheatsheet.py`.
- **Change the theme** — the palette lives in `frontend/src/index.css` under `@theme`; it is a
  phosphor-green terminal palette on near-black.
# ai-agent-learning
