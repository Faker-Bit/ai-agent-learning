"""Guided walkthroughs: full, animated sessions for each agent.

Each step carries narration (what is happening and why it matters), an optional
command to copy, and the terminal lines that appear while it runs. The site
replays these lines as an animated terminal.
"""

from __future__ import annotations

from typing import Any

WALKTHROUGHS: list[dict[str, Any]] = [
    {
        "id": "opencode-first-hour",
        "title": "Your first hour in opencode",
        "agent": "opencode",
        "level": "beginner",
        "duration_min": 45,
        "summary": (
            "From nothing to a committed, verified change. Install, connect a provider, teach the agent "
            "about your repo with AGENTS.md, plan before it writes, then check the work like a reviewer."
        ),
        "outcome": [
            "opencode installed and pointed at a provider",
            "An AGENTS.md that describes your repo",
            "A plan you approved before a single file changed",
            "A verified change, a clean diff, and a commit",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Install the agent",
                "narration": (
                    "opencode is a single binary. The install script is the shortest path on macOS and "
                    "Linux; on Windows use npm or Scoop, or run it inside WSL for the best experience."
                ),
                "command": "curl -fsSL https://opencode.ai/install | bash",
                "lines": [
                    {"type": "muted", "text": "# macOS / Linux"},
                    {"type": "input", "text": "curl -fsSL https://opencode.ai/install | bash"},
                    {"type": "output", "text": "  installing opencode..."},
                    {"type": "success", "text": "  opencode installed  ->  ~/.opencode/bin/opencode"},
                    {"type": "muted", "text": "# Windows (PowerShell)"},
                    {"type": "input", "text": "npm install -g opencode-ai"},
                    {"type": "success", "text": "  added 1 package in 4s"},
                    {"type": "muted", "text": "# or: scoop install opencode"},
                ],
                "tip": "Check it with `opencode --version`. If the shell says 'command not found', restart the terminal so the new PATH is picked up.",
            },
            {
                "id": "s2",
                "title": "Connect a provider",
                "narration": (
                    "The agent needs a model. Run /connect inside the TUI and pick a provider. If you want "
                    "the free curated models, choose the opencode workspace - that is OpenCode Zen."
                ),
                "command": "opencode",
                "lines": [
                    {"type": "input", "text": "opencode"},
                    {"type": "muted", "text": "  opencode v1.0.0  |  type /help for commands"},
                    {"type": "accent", "text": "/connect"},
                    {"type": "output", "text": "  Select a provider"},
                    {"type": "output", "text": "    opencode        OpenCode Zen - curated + free models"},
                    {"type": "output", "text": "    anthropic      Claude"},
                    {"type": "output", "text": "    openai         GPT"},
                    {"type": "output", "text": "    groq           Llama / Qwen (free tier)"},
                    {"type": "output", "text": "    ollama         Local models"},
                    {"type": "output", "text": "  -> opencode"},
                    {"type": "muted", "text": "  opening https://opencode.ai/auth ..."},
                    {"type": "success", "text": "  provider connected  |  opencode/zen"},
                ],
                "tip": "Keys are stored in ~/.local/share/opencode/auth.json. You can also set them as environment variables or in a .env file in the project.",
            },
            {
                "id": "s3",
                "title": "Teach it about the repo",
                "narration": (
                    "/init scans the repo and writes an AGENTS.md: build and test commands, layout, and the "
                    "conventions a future session would otherwise have to rediscover. Commit it - this file "
                    "is the difference between a useful agent and a confused one."
                ),
                "command": "/init",
                "lines": [
                    {"type": "accent", "text": "/init"},
                    {"type": "tool", "text": "  Read(24)  scanning project structure"},
                    {"type": "tool", "text": "  Grep(6)   finding test and build commands"},
                    {"type": "output", "text": "  Wrote AGENTS.md"},
                    {"type": "output", "text": "    | backend/   FastAPI service, pytest suite"},
                    {"type": "output", "text": "    | frontend/  React 19 + Vite, npm run build"},
                    {"type": "output", "text": "    | commands   pytest -q  |  npm run lint  |  npm run build"},
                ],
                "tip": "Keep AGENTS.md short and factual: commands, layout, and the three rules a new contributor would get wrong.",
            },
            {
                "id": "s4",
                "title": "Ask before you change anything",
                "narration": (
                    "Reference files with @ (fuzzy search across the project) and ask how something works "
                    "before you ask for a change. The agent reads the file for you - you never paste code "
                    "it can open itself."
                ),
                "command": "How is auth handled in @backend/app/core/security.py?",
                "lines": [
                    {"type": "input", "text": "How is auth handled in @backend/app/core/security.py?"},
                    {"type": "tool", "text": "  Read(1)   backend/app/core/security.py"},
                    {"type": "output", "text": "  Tokens are signed with HMAC-SHA256 and verified in the"},
                    {"type": "output", "text": "  dependency `require_user`, which is injected into every"},
                    {"type": "output", "text": "  route. Refresh tokens live in the `sessions` table and"},
                    {"type": "output", "text": "  rotate on every refresh."},
                ],
                "tip": "The same @-syntax works inside custom commands and inside AGENTS.md.",
            },
            {
                "id": "s5",
                "title": "Plan mode first",
                "narration": (
                    "Press Tab to switch to Plan mode. The agent can read and search but every write and "
                    "every shell command asks first. Give it the requirement and the shape of the solution, "
                    "then push back on the plan while it is still cheap to change."
                ),
                "command": "Tab  ->  Plan mode",
                "lines": [
                    {"type": "muted", "text": "  [tab] switched to plan mode"},
                    {"type": "input", "text": "Add a GET /health endpoint that returns {\"status\":\"ok\"} and a test for it."},
                    {"type": "output", "text": "  Plan"},
                    {"type": "output", "text": "   1. add GET /health in backend/app/api/routes/health.py"},
                    {"type": "output", "text": "   2. return {\"status\": \"ok\", \"version\": ...}"},
                    {"type": "output", "text": "   3. add tests/test_health.py asserting status == 200"},
                    {"type": "output", "text": "   4. run pytest -q to verify"},
                    {"type": "muted", "text": "  no files changed in plan mode"},
                ],
                "tip": "Plans are cheap to argue with and expensive to discover after the code is written. Plan first, build second.",
            },
            {
                "id": "s6",
                "title": "Build it",
                "narration": (
                    "Switch back with Tab and say go. The agent writes the files, then runs the test suite "
                    "to prove the change works - it should not need to be told twice."
                ),
                "command": "Tab  ->  Build mode  |  \"go ahead\"",
                "lines": [
                    {"type": "muted", "text": "  [tab] switched to build mode"},
                    {"type": "input", "text": "go ahead"},
                    {"type": "tool", "text": "  Read(2)   backend/app/api/routes/health.py"},
                    {"type": "tool", "text": "  Edit(2)   backend/app/api/routes/health.py"},
                    {"type": "tool", "text": "  Write(1)  backend/tests/test_health.py"},
                    {"type": "tool", "text": "  Bash(1)   pytest -q"},
                    {"type": "output", "text": "  28 passed in 1.9s"},
                    {"type": "success", "text": "  ok /health returns 200 with status ok"},
                ],
                "tip": "If it stops halfway, say what remains: 'run the tests again and fix whatever fails'.",
            },
            {
                "id": "s7",
                "title": "Review like a human",
                "narration": (
                    "The agent's claim that it works is not evidence - the diff is. Read what changed, "
                    "check it matches the plan, and ask for a different approach if it drifted."
                ),
                "command": "git diff",
                "lines": [
                    {"type": "input", "text": "git diff"},
                    {"type": "diff", "text": "+ @router.get(\"/health\")"},
                    {"type": "diff", "text": "+ async def health() -> dict:"},
                    {"type": "diff", "text": "+     return {\"status\": \"ok\", \"version\": __version__}"},
                    {"type": "diff", "text": "+ def test_health(client):"},
                    {"type": "diff", "text": "+     assert client.get(\"/api/health\").json()[\"status\"] == \"ok\""},
                    {"type": "muted", "text": "  2 files changed, 7 insertions"},
                ],
                "tip": "If the diff shows scope you did not ask for, say so - agents will happily widen the change.",
            },
            {
                "id": "s8",
                "title": "Undo without fear",
                "narration": (
                    "/undo reverts the last message and its file changes using git, so a bad turn costs you "
                    "one keystroke. /redo brings it back. Commit once the diff is what you want."
                ),
                "command": "/undo",
                "lines": [
                    {"type": "accent", "text": "/undo"},
                    {"type": "muted", "text": "  reverted 2 file changes and the last message"},
                    {"type": "accent", "text": "/redo"},
                    {"type": "muted", "text": "  restored 2 file changes"},
                    {"type": "accent", "text": "/new"},
                    {"type": "success", "text": "  session started"},
                ],
                "tip": "Undo needs a git repository. Initialise one before you start - /undo and /redo both rely on it.",
            },
        ],
    },
    {
        "id": "opencode-free-models",
        "title": "Run the whole thing on free models",
        "agent": "zen",
        "level": "beginner",
        "duration_min": 30,
        "summary": (
            "OpenCode Zen is a curated catalogue of models the opencode team has actually tested, with a "
            "free tier. This session shows how to see what your key unlocks, how to route cheap models to "
            "planning and strong models to writing, and how to watch what it costs."
        ),
        "outcome": [
            "A free model running inside opencode",
            "Different models per agent (plan vs build)",
            "A live view of token spend per model",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Connect the Zen workspace",
                "narration": (
                    "Run /connect and choose opencode. You get a key from opencode.ai/auth - the free "
                    "models do not need a credit card."
                ),
                "command": "/connect",
                "lines": [
                    {"type": "accent", "text": "/connect"},
                    {"type": "output", "text": "  -> opencode (OpenCode Zen)"},
                    {"type": "success", "text": "  provider connected  |  opencode/zen"},
                ],
            },
            {
                "id": "s2",
                "title": "See what your key unlocks",
                "narration": (
                    "opencode models lists everything reachable with the keys you have configured. Filter by "
                    "provider, and refresh the cache when a provider ships new models."
                ),
                "command": "opencode models opencode",
                "lines": [
                    {"type": "input", "text": "opencode models opencode"},
                    {"type": "output", "text": "  opencode/minimax-m2.5-free"},
                    {"type": "output", "text": "  opencode/mimo-v2.5-pro-free"},
                    {"type": "output", "text": "  opencode/mimo-v2.5-omni-free"},
                    {"type": "output", "text": "  opencode/mimo-v2.5-flash-free"},
                    {"type": "output", "text": "  opencode/deepseek-v4-flash-free"},
                    {"type": "output", "text": "  opencode/nemotron-3-ultra-free"},
                    {"type": "output", "text": "  opencode/nemotron-3-super-free"},
                    {"type": "output", "text": "  opencode/qwen-3.6-plus-free"},
                    {"type": "output", "text": "  opencode/trinity-large-preview-free"},
                    {"type": "output", "text": "  opencode/north-mini-code-free"},
                ],
                "tip": "Model ids are provider/model - that exact string is what goes in opencode.json and in --model.",
            },
            {
                "id": "s3",
                "title": "Switch models mid-session",
                "narration": (
                    "Press /models in the TUI to pick a different model without losing the conversation. "
                    "Switch to a cheap model for exploration and a strong one when it is time to write code."
                ),
                "command": "/models",
                "lines": [
                    {"type": "accent", "text": "/models"},
                    {"type": "output", "text": "  select a model"},
                    {"type": "output", "text": "   > opencode/mimo-v2.5-pro-free"},
                    {"type": "output", "text": "     opencode/minimax-m2.5-free"},
                    {"type": "output", "text": "     opencode/qwen-3.6-plus-free"},
                    {"type": "success", "text": "  model set  |  opencode/mimo-v2.5-pro-free"},
                ],
                "tip": "Free tiers have tighter rate limits. If you hit a 429, wait a minute or switch to a local model.",
            },
            {
                "id": "s4",
                "title": "Route models per agent",
                "narration": (
                    "This is the highest-leverage config in the whole tool. Give the plan agent a small fast "
                    "model and the build agent a strong one - the plan rarely needs frontier reasoning and "
                    "the build always does."
                ),
                "command": "opencode.json",
                "lines": [
                    {"type": "muted", "text": "  // opencode.json"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"$schema\": \"https://opencode.ai/config.json\","},
                    {"type": "accent", "text": "    \"agent\": {"},
                    {"type": "accent", "text": "      \"plan\":  { \"model\": \"opencode/mimo-v2.5-flash-free\" },"},
                    {"type": "accent", "text": "      \"build\": { \"model\": \"opencode/mimo-v2.5-pro-free\" }"},
                    {"type": "accent", "text": "    }"},
                    {"type": "accent", "text": "  }"},
                ],
                "tip": "Same trick for review: a read-only subagent on a cheap model catches most issues before the strong model ever runs.",
            },
            {
                "id": "s5",
                "title": "Watch the spend",
                "narration": (
                    "opencode stats breaks token usage and cost down by model and by tool, so you can see "
                    "which model is actually doing the work - and which one is burning tokens on retries."
                ),
                "command": "opencode stats --models 5",
                "lines": [
                    {"type": "input", "text": "opencode stats --models 5"},
                    {"type": "output", "text": "  sessions      12"},
                    {"type": "output", "text": "  tokens        1.42M in  |  218K out"},
                    {"type": "output", "text": "  cost          $0.38"},
                    {"type": "output", "text": "  by model"},
                    {"type": "output", "text": "    opencode/mimo-v2.5-pro-free     640K in   $0.21"},
                    {"type": "output", "text": "    opencode/mimo-v2.5-flash-free    512K in   $0.09"},
                    {"type": "output", "text": "    anthropic/claude-sonnet-4-5      268K in   $0.08"},
                ],
                "tip": "If one model dominates the token count, it is usually the one being asked to re-read the whole repo. Fix the prompt, not the plan.",
            },
            {
                "id": "s6",
                "title": "Keep your own key too",
                "narration": (
                    "Zen is great for free volume, but you will sometimes want a frontier model. Adding a "
                    "second provider is one command - and both stay available in the same session."
                ),
                "command": "opencode auth login",
                "lines": [
                    {"type": "input", "text": "opencode auth login"},
                    {"type": "output", "text": "  select a provider  ->  anthropic"},
                    {"type": "output", "text": "  paste your key"},
                    {"type": "success", "text": "  authenticated  |  anthropic"},
                    {"type": "input", "text": "opencode auth list"},
                    {"type": "output", "text": "  anthropic   anthropic/claude-sonnet-4-5"},
                    {"type": "output", "text": "  opencode    opencode/mimo-v2.5-pro-free"},
                ],
                "tip": "Use the free catalogue for volume work - bulk refactors, test writing, docs - and a paid key for the hard reasoning.",
            },
        ],
    },
    {
        "id": "opencode-automation",
        "title": "Automate opencode: run, serve, attach",
        "agent": "opencode",
        "level": "intermediate",
        "duration_min": 40,
        "summary": (
            "The TUI is only one client. opencode run gives you a one-shot agent, opencode serve exposes "
            "the whole thing over HTTP, and opencode attach connects any client to a running server - which "
            "is how you put an agent in CI."
        ),
        "outcome": [
            "A scriptable one-shot agent",
            "A headless server you can drive from anywhere",
            "A CI job that reviews a pull request",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "One-shot runs",
                "narration": (
                    "opencode run takes a prompt and exits. Attach files with --file, pick a model with "
                    "--model, and use --auto to approve anything that is not explicitly denied."
                ),
                "command": "opencode run \"summarise the diff in 5 bullets\" --format json",
                "lines": [
                    {"type": "input", "text": "opencode run \"summarise the diff in 5 bullets\" --format json"},
                    {"type": "output", "text": "  {"},
                    {"type": "output", "text": "    \"type\": \"text\","},
                    {"type": "output", "text": "    \"text\": \"* adds a /health route...\","},
                    {"type": "output", "text": "    \"sessionID\": \"ses_8f21c4\""},
                    {"type": "output", "text": "  }"},
                ],
                "tip": "--format json emits raw JSON events, which is what you want when a script has to parse the result.",
            },
            {
                "id": "s2",
                "title": "Drive it from a shell script",
                "narration": (
                    "Because the output is JSON, the agent becomes a normal Unix building block: pipe it "
                    "through jq, fail a build on a bad review, or post a comment."
                ),
                "command": "opencode run \"review this diff for security bugs\" --format json | jq -r '.text'",
                "lines": [
                    {"type": "input", "text": "opencode run \"review this diff for security bugs\" --format json | jq -r '.text'"},
                    {"type": "output", "text": "  ! backend/app/api/routes/files.py:42 - path is used without normalisation"},
                    {"type": "output", "text": "  ! backend/app/core/security.py:88 - token compared with == instead of constant time"},
                    {"type": "success", "text": "  exit code 0  |  2 findings"},
                ],
                "tip": "Give it the diff explicitly with --file, or run it inside the repo so its tools can see the working tree.",
            },
            {
                "id": "s3",
                "title": "Start a headless server",
                "narration": (
                    "opencode serve runs the whole agent as an HTTP service. This is the piece that makes "
                    "everything else composable: web UI, mobile client, or your own tooling."
                ),
                "command": "opencode serve --port 4096",
                "lines": [
                    {"type": "input", "text": "opencode serve --port 4096"},
                    {"type": "output", "text": "  opencode server listening on http://127.0.0.1:4096"},
                    {"type": "muted", "text": "  set OPENCODE_SERVER_PASSWORD to require basic auth"},
                ],
                "tip": "Never expose this to a public network without a password. It can edit files and run commands.",
            },
            {
                "id": "s4",
                "title": "Attach instead of restarting",
                "narration": (
                    "Every cold start re-boots your MCP servers, which is slow. Attaching to a running server "
                    "keeps them warm - the TUI on one machine, the agent backend on another."
                ),
                "command": "opencode attach http://127.0.0.1:4096",
                "lines": [
                    {"type": "input", "text": "opencode attach http://127.0.0.1:4096"},
                    {"type": "output", "text": "  connected  |  session list: 4"},
                    {"type": "muted", "text": "  mcp servers reused from the running backend (no cold boot)"},
                ],
                "tip": "The same trick works for scripted runs: opencode run --attach http://127.0.0.1:4096 \"...\"",
            },
            {
                "id": "s5",
                "title": "Put it in CI",
                "narration": (
                    "A pipeline job can call opencode run, fail the build on a bad review, and write the "
                    "result back to the pull request."
                ),
                "command": "opencode run --format json \"review the diff in $GITHUB_HEAD_REF\"",
                "lines": [
                    {"type": "muted", "text": "  # .github/workflows/review.yml"},
                    {"type": "input", "text": "opencode run --format json \"review the diff in $GITHUB_HEAD_REF\""},
                    {"type": "output", "text": "  fetching PR diff ..."},
                    {"type": "output", "text": "  reviewed 14 files, 3 findings"},
                    {"type": "output", "text": "  wrote /tmp/review.md"},
                ],
                "tip": "In CI, pin the model with --model and set a budget with agent steps so a loop cannot burn your credits.",
            },
            {
                "id": "s6",
                "title": "Pull request mode",
                "narration": (
                    "opencode pr checks out a pull request branch and starts a session on it - the fastest way "
                    "to review a contributor's work locally."
                ),
                "command": "opencode pr 412",
                "lines": [
                    {"type": "input", "text": "opencode pr 412"},
                    {"type": "output", "text": "  fetching PR 412 ..."},
                    {"type": "output", "text": "  checked out branch pr/412-add-health-endpoint"},
                    {"type": "success", "text": "  session ready  |  type /init if this repo has no AGENTS.md yet"},
                ],
                "tip": "opencode github install sets up the same agent inside GitHub Actions if you want it fully automated.",
            },
        ],
    },
    {
        "id": "opencode-mcp",
        "title": "Add real tools with MCP",
        "agent": "opencode",
        "level": "intermediate",
        "duration_min": 35,
        "summary": (
            "MCP gives the agent capabilities it does not have: live documentation, code search, issue "
            "trackers, your databases. This session adds three servers and then keeps their context cost "
            "under control."
        ),
        "outcome": [
            "Three MCP servers attached",
            "OAuth auth working for one of them",
            "A rule so the agent reaches for them automatically",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Add a local server",
                "narration": (
                    "opencode mcp add walks you through it, or you can write the config yourself. A local "
                    "server is just a command with optional environment variables."
                ),
                "command": "opencode mcp add",
                "lines": [
                    {"type": "input", "text": "opencode mcp add"},
                    {"type": "output", "text": "  name      -> filesystem"},
                    {"type": "output", "text": "  type      -> local"},
                    {"type": "output", "text": "  command   -> npx -y @modelcontextprotocol/server-filesystem /tmp"},
                    {"type": "success", "text": "  added 'filesystem' to opencode.json"},
                    {"type": "input", "text": "opencode mcp list"},
                    {"type": "output", "text": "  filesystem   connected"},
                ],
                "tip": "Local servers are started on demand by opencode - you do not run them yourself.",
            },
            {
                "id": "s2",
                "title": "Add a docs server",
                "narration": (
                    "Context7 searches current documentation for libraries. A remote MCP server is a URL and "
                    "sometimes a header - that is the whole config."
                ),
                "command": "opencode.json",
                "lines": [
                    {"type": "muted", "text": "  // opencode.json"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"mcp\": {"},
                    {"type": "accent", "text": "      \"context7\": {"},
                    {"type": "accent", "text": "        \"type\": \"remote\","},
                    {"type": "accent", "text": "        \"url\": \"https://mcp.context7.com/mcp\","},
                    {"type": "accent", "text": "        \"headers\": { \"CONTEXT7_API_KEY\": \"{env:CONTEXT7_API_KEY}\" }"},
                    {"type": "accent", "text": "      }"},
                    {"type": "accent", "text": "    }"},
                    {"type": "accent", "text": "  }"},
                ],
                "tip": "Reference env vars with {env:NAME} so keys never land in the config file.",
            },
            {
                "id": "s3",
                "title": "Search code on GitHub",
                "narration": (
                    "gh_grep searches public code for examples. Name the server and then ask for it by name "
                    "so the model reaches for it deliberately."
                ),
                "command": "How do I set a custom domain in an SST Astro component? use the gh_grep tool",
                "lines": [
                    {"type": "accent", "text": "  \"mcp\": { \"gh_grep\": { \"type\": \"remote\", \"url\": \"https://mcp.grep.app\" } }"},
                    {"type": "input", "text": "How do I set a custom domain in an SST Astro component? use the gh_grep tool"},
                    {"type": "tool", "text": "  gh_grep_search  \"custom domain sst astro\""},
                    {"type": "output", "text": "  found 12 examples across 6 repositories"},
                    {"type": "output", "text": "  closest match: sst/ion -> \"domain: { example.com: { zone: ... } }\""},
                ],
                "tip": "Say 'use the X tool' in the prompt. The server name is a prefix on every tool it exposes.",
            },
            {
                "id": "s4",
                "title": "OAuth servers",
                "narration": (
                    "Remote servers that use OAuth just work - opencode detects the 401 and runs the flow. "
                    "You can also trigger it yourself and check status."
                ),
                "command": "opencode mcp auth sentry",
                "lines": [
                    {"type": "input", "text": "opencode mcp auth sentry"},
                    {"type": "output", "text": "  opening browser for authorisation ..."},
                    {"type": "success", "text": "  authenticated  |  sentry"},
                    {"type": "input", "text": "opencode mcp auth list"},
                    {"type": "output", "text": "  sentry   authorised   (tokens in ~/.local/share/opencode/mcp-auth.json)"},
                ],
                "tip": "opencode mcp debug <name> shows auth status, tests connectivity and walks the discovery flow.",
            },
            {
                "id": "s5",
                "title": "Control the context cost",
                "narration": (
                    "Every MCP tool lives in the context window. Enable a server globally but disable its "
                    "tools, then turn them on only for the agent that needs them."
                ),
                "command": "opencode.json",
                "lines": [
                    {"type": "muted", "text": "  // disable everything, then opt in per agent"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"tools\": { \"*mcp*\": false },"},
                    {"type": "accent", "text": "    \"agent\": { \"researcher\": { \"tools\": { \"gh_grep*\": true, \"context7*\": true } } }"},
                    {"type": "accent", "text": "  }"},
                ],
                "tip": "The GitHub MCP server alone can add tens of thousands of tokens. Enable it only for agents that need it.",
            },
            {
                "id": "s6",
                "title": "Make it automatic",
                "narration": (
                    "The most reliable way to get an agent to use a tool is to say so in AGENTS.md, where it "
                    "is read on every session."
                ),
                "command": "AGENTS.md",
                "lines": [
                    {"type": "muted", "text": "  # AGENTS.md"},
                    {"type": "accent", "text": "  When you are unsure how to do something, use `gh_grep` to search"},
                    {"type": "accent", "text": "  real code examples on GitHub before guessing."},
                    {"type": "accent", "text": "  When you need library documentation, use `context7`."},
                ],
                "tip": "Rules beat prompting: an instruction in AGENTS.md applies to every session without you retyping it.",
            },
        ],
    },
    {
        "id": "claude-code",
        "title": "Claude Code in an afternoon",
        "agent": "claude",
        "level": "beginner",
        "duration_min": 50,
        "summary": (
            "CLAUDE.md, plan mode, MCP, hooks and print mode - the five features that make Claude Code more "
            "than a chat box, and how to set each one up."
        ),
        "outcome": [
            "A CLAUDE.md generated from your repo",
            "A plan-then-build habit",
            "A hook that runs your tests after every edit",
            "A scriptable print mode",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Install and sign in",
                "narration": (
                    "Claude Code runs from npm or the install script, then authenticates with your Anthropic "
                    "account. Starting it inside a git repository gives you the full toolset."
                ),
                "command": "npm install -g @anthropic-ai/claude-code",
                "lines": [
                    {"type": "input", "text": "npm install -g @anthropic-ai/claude-code"},
                    {"type": "success", "text": "  added 2 packages in 6s"},
                    {"type": "input", "text": "claude"},
                    {"type": "output", "text": "  Choose how to log in:"},
                    {"type": "output", "text": "    1. Claude account (subscription)"},
                    {"type": "output", "text": "    2. Anthropic Console account"},
                    {"type": "output", "text": "  -> 1"},
                    {"type": "success", "text": "  logged in"},
                ],
                "tip": "Set EDITOR=code --wait so /editor and /export open your GUI editor and wait for you.",
            },
            {
                "id": "s2",
                "title": "Generate CLAUDE.md",
                "narration": (
                    "/init reads the repo and writes CLAUDE.md - build commands, layout and conventions. "
                    "It is the equivalent of AGENTS.md and it is the first thing to commit to any repo you "
                    "work on with an agent."
                ),
                "command": "/init",
                "lines": [
                    {"type": "accent", "text": "/init"},
                    {"type": "tool", "text": "  Read(31)   scanning repository"},
                    {"type": "tool", "text": "  Grep(4)    finding test commands"},
                    {"type": "output", "text": "  Wrote CLAUDE.md"},
                    {"type": "output", "text": "    | commands: pytest -q, npm run lint, npm run build"},
                    {"type": "output", "text": "    | python code lives in backend/app, tests in backend/tests"},
                ],
                "tip": "Re-run /init any time the repo changes shape - it updates the file in place.",
            },
            {
                "id": "s3",
                "title": "Plan before you touch",
                "narration": (
                    "Shift+Tab switches into plan mode, where Claude analyses and proposes but does not edit. "
                    "Use it for anything bigger than a one-line fix."
                ),
                "command": "Shift+Tab  ->  plan mode",
                "lines": [
                    {"type": "muted", "text": "  [shift+tab] plan mode on"},
                    {"type": "input", "text": "Add rate limiting to the public API. Which layer should it live in?"},
                    {"type": "output", "text": "  Plan"},
                    {"type": "output", "text": "   1. middleware in app/core/rate_limit.py (already exists)"},
                    {"type": "output", "text": "   2. key: client IP + route template, not the full path"},
                    {"type": "output", "text": "   3. exempt /api/health"},
                    {"type": "output", "text": "   4. tests for allow, block and exempt cases"},
                    {"type": "muted", "text": "  no files changed"},
                ],
                "tip": "Ask the agent to justify the plan location - it usually reveals a better seam in your own code.",
            },
            {
                "id": "s4",
                "title": "Give it tools with MCP",
                "narration": (
                    "MCP servers are added with a command and are then available to the agent. The same "
                    "protocol opencode uses, so the servers are portable between tools."
                ),
                "command": "claude mcp add sentry --transport http https://mcp.sentry.dev/mcp",
                "lines": [
                    {"type": "input", "text": "claude mcp add sentry --transport http https://mcp.sentry.dev/mcp"},
                    {"type": "output", "text": "  added sentry"},
                    {"type": "input", "text": "claude mcp list"},
                    {"type": "output", "text": "  sentry   connected   (12 tools)"},
                ],
                "tip": "Sentry's server uses OAuth - Claude Code will run the browser flow the first time you call it.",
            },
            {
                "id": "s5",
                "title": "Hooks that guard the loop",
                "narration": (
                    "Hooks run your own commands on tool events. A PostToolUse hook that runs the test suite "
                    "after every edit turns the agent from 'usually right' into 'verified'."
                ),
                "command": "settings.json",
                "lines": [
                    {"type": "muted", "text": "  // .claude/settings.json"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"hooks\": {"},
                    {"type": "accent", "text": "      \"PostToolUse\": [{ \"matcher\": \"Edit|Write\","},
                    {"type": "accent", "text": "        \"hooks\": [{ \"type\": \"command\","},
                    {"type": "accent", "text": "          \"command\": \"cd backend && pytest -q\" }] }] }"},
                    {"type": "accent", "text": "  }"},
                ],
                "tip": "Keep the hook fast. A slow hook runs on every single edit and you will start ignoring it.",
            },
            {
                "id": "s6",
                "title": "Print mode for scripts",
                "narration": (
                    "claude -p takes a prompt, prints the answer and exits - the non-interactive version of "
                    "the agent, ready for CI and cron."
                ),
                "command": "claude -p \"summarise this repo in 5 bullets\"",
                "lines": [
                    {"type": "input", "text": "claude -p \"summarise this repo in 5 bullets\""},
                    {"type": "output", "text": "  * FastAPI backend with async SQLAlchemy and a SQLite store"},
                    {"type": "output", "text": "  * React 19 SPA built with Vite and Tailwind"},
                    {"type": "output", "text": "  * Provider layer with OpenAI-compatible, Anthropic and Gemini adapters"},
                    {"type": "output", "text": "  * 27 pytest tests covering API, grading and sandbox"},
                    {"type": "output", "text": "  * Single start.bat boots venv, build and API"},
                ],
                "tip": "Combine with --allowedTools to lock down what a scripted run may touch.",
            },
            {
                "id": "s7",
                "title": "Keep the context small",
                "narration": (
                    "Long sessions fill the window with stale detail. /compact summarises the conversation "
                    "into a plan and keeps going; /clear starts fresh with CLAUDE.md still loaded."
                ),
                "command": "/compact",
                "lines": [
                    {"type": "accent", "text": "/compact"},
                    {"type": "output", "text": "  compacted 41 messages into a summary"},
                    {"type": "output", "text": "  kept: plan for the rate limiter, 3 files edited, 2 open questions"},
                    {"type": "success", "text": "  context saved: ~52K tokens"},
                ],
                "tip": "Compact at natural boundaries - after a feature lands, not in the middle of a debug loop.",
            },
        ],
    },
    {
        "id": "codex-cli",
        "title": "Codex CLI: approvals and sandboxing",
        "agent": "codex",
        "level": "beginner",
        "duration_min": 35,
        "summary": (
            "Codex is explicit about two things: what it wants to do, and what it is allowed to touch. "
            "This session sets up the approval model, writes AGENTS.md and runs it in CI."
        ),
        "outcome": [
            "Codex running under your ChatGPT plan",
            "An approval and sandbox policy you chose on purpose",
            "A headless run in a pipeline",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Install and sign in",
                "narration": (
                    "npm, Homebrew or the standalone installer. On first run Codex offers to sign in with "
                    "your ChatGPT plan - that is the path that does not need a separate API bill."
                ),
                "command": "npm install -g @openai/codex",
                "lines": [
                    {"type": "input", "text": "npm install -g @openai/codex"},
                    {"type": "success", "text": "  added 1 package in 5s"},
                    {"type": "input", "text": "codex"},
                    {"type": "output", "text": "  Select how to sign in:"},
                    {"type": "output", "text": "    1. Sign in with ChatGPT   (Plus / Pro / Business / Edu / Enterprise)"},
                    {"type": "output", "text": "    2. Use an API key"},
                    {"type": "output", "text": "  -> 1"},
                    {"type": "success", "text": "  signed in as you@example.com"},
                ],
                "tip": "An API key works too, but then usage is billed to the API account rather than your plan.",
            },
            {
                "id": "s2",
                "title": "Understand the approval model",
                "narration": (
                    "Codex shows every action before it takes it. Reads are usually free; writes and commands "
                    "depend on the approval mode you picked at start."
                ),
                "command": "codex",
                "lines": [
                    {"type": "input", "text": "codex"},
                    {"type": "output", "text": "  approval mode: on-request"},
                    {"type": "output", "text": "  sandbox:      workspace-write"},
                    {"type": "output", "text": "  model:        gpt-5-codex"},
                    {"type": "muted", "text": "  > try 'fix the failing test in backend/tests'"},
                ],
                "tip": "on-request means Codex pauses for anything that writes or runs commands; never means it can act inside the sandbox without asking.",
            },
            {
                "id": "s3",
                "title": "Write AGENTS.md",
                "narration": (
                    "Codex reads AGENTS.md for repo-wide instructions - the same filename opencode uses, so a "
                    "repo can carry one file for both tools."
                ),
                "command": "AGENTS.md",
                "lines": [
                    {"type": "muted", "text": "  # AGENTS.md"},
                    {"type": "accent", "text": "  - Python 3.12+, FastAPI backend in backend/app"},
                    {"type": "accent", "text": "  - Tests: cd backend && pytest -q"},
                    {"type": "accent", "text": "  - Lint/format: cd frontend && npm run lint"},
                    {"type": "accent", "text": "  - Never edit files under backend/alembic/versions by hand"},
                ],
                "tip": "Say 'never do X' explicitly. Negative rules in AGENTS.md are respected more reliably than positive ones.",
            },
            {
                "id": "s4",
                "title": "Watch it work",
                "narration": (
                    "Each step is shown as a proposal. Approve the ones you want, reject the ones you do not, "
                    "and watch the sandbox keep it inside the workspace."
                ),
                "command": "fix the failing test in backend/tests",
                "lines": [
                    {"type": "input", "text": "fix the failing test in backend/tests"},
                    {"type": "tool", "text": "  Read(1)   backend/tests/test_health.py"},
                    {"type": "tool", "text": "  Bash(1)   cd backend && pytest -q tests/test_health.py"},
                    {"type": "output", "text": "  1 failed, 26 passed"},
                    {"type": "tool", "text": "  Edit(1)   backend/tests/test_health.py"},
                    {"type": "tool", "text": "  Bash(1)   cd backend && pytest -q"},
                    {"type": "success", "text": "  27 passed in 1.4s"},
                ],
                "tip": "If it asks to run something odd, read it. Approval prompts are the cheapest security you will ever get.",
            },
            {
                "id": "s5",
                "title": "Auto mode inside the sandbox",
                "narration": (
                    "When you trust the task, --full-auto lets it work without prompts while the sandbox "
                    "still confines it to the workspace."
                ),
                "command": "codex --full-auto",
                "lines": [
                    {"type": "input", "text": "codex --full-auto"},
                    {"type": "output", "text": "  approval mode: never   |   sandbox: workspace-write"},
                    {"type": "input", "text": "add a /health route and a test for it"},
                    {"type": "tool", "text": "  Edit(2) | Write(1) | Bash(1)"},
                    {"type": "success", "text": "  28 passed in 1.6s"},
                ],
                "tip": "Never use --full-auto where network access matters. The sandbox stops writes outside the repo, not outbound calls.",
            },
            {
                "id": "s6",
                "title": "Headless runs in CI",
                "narration": (
                    "codex exec is the scriptable form: a prompt in, an answer out, exit code for the "
                    "pipeline to act on."
                ),
                "command": "codex exec \"review the staged diff and print findings\"",
                "lines": [
                    {"type": "input", "text": "codex exec \"review the staged diff and print findings\""},
                    {"type": "output", "text": "  reviewing 6 staged files ..."},
                    {"type": "output", "text": "  ! api/routes/files.py - filename is built from user input"},
                    {"type": "success", "text": "  done  |  1 finding  |  exit 0"},
                ],
                "tip": "Add --output-last-message to a file if you want the final text in your build log.",
            },
        ],
    },
    {
        "id": "gemini-cli",
        "title": "Gemini CLI and the free tier",
        "agent": "gemini",
        "level": "beginner",
        "duration_min": 30,
        "summary": (
            "The most generous free agent tier available: Google AI Studio's flash quotas with no credit "
            "card. This session sets up auth, writes GEMINI.md and scripts it."
        ),
        "outcome": [
            "Gemini CLI signed in on the free tier",
            "A GEMINI.md with your project context",
            "A JSON-mode command you can call from a script",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Install it",
                "narration": (
                    "npx runs it with no install at all; npm -g is the everyday option. On Windows the npm "
                    "route is the most reliable."
                ),
                "command": "npm install -g @google/gemini-cli",
                "lines": [
                    {"type": "input", "text": "npm install -g @google/gemini-cli"},
                    {"type": "success", "text": "  added 214 packages in 21s"},
                    {"type": "input", "text": "npx @google/gemini-cli   # run once, no install"},
                ],
                "tip": "Release channels exist: @latest, @preview and @nightly. Pin @latest in anything automated.",
            },
            {
                "id": "s2",
                "title": "Pick how you authenticate",
                "narration": (
                    "Sign in with Google for the free tier, use a Gemini API key for model control, or point "
                    "at Vertex AI for enterprise workloads."
                ),
                "command": "gemini",
                "lines": [
                    {"type": "input", "text": "gemini"},
                    {"type": "output", "text": "  1. Login with Google"},
                    {"type": "output", "text": "  2. Gemini API key"},
                    {"type": "output", "text": "  3. Vertex AI"},
                    {"type": "output", "text": "  -> 1"},
                    {"type": "success", "text": "  authenticated  |  free tier  |  ~1500 requests/day"},
                ],
                "tip": "The free tier caps out at 1,500 requests a day on flash models with no card required - perfect for a side project.",
            },
            {
                "id": "s3",
                "title": "Write GEMINI.md",
                "narration": (
                    "GEMINI.md is the equivalent of AGENTS.md and CLAUDE.md: project context loaded on every "
                    "session. The ecosystem converged on one filename for a reason."
                ),
                "command": "GEMINI.md",
                "lines": [
                    {"type": "muted", "text": "  # GEMINI.md"},
                    {"type": "accent", "text": "  This repo has a FastAPI backend in backend/ and a React app in frontend/."},
                    {"type": "accent", "text": "  Run tests with `cd backend && pytest -q`."},
                    {"type": "accent", "text": "  Never edit backend/alembic/versions by hand."},
                ],
                "tip": "You can have both GEMINI.md and AGENTS.md - different tools read different files, and they do not conflict.",
            },
            {
                "id": "s4",
                "title": "Include other directories",
                "narration": (
                    "Monorepos and sibling libraries are one flag away. Context that is out of the working "
                    "directory is invisible unless you say so."
                ),
                "command": "gemini --include-directories ../lib,../docs",
                "lines": [
                    {"type": "input", "text": "gemini --include-directories ../lib,../docs"},
                    {"type": "output", "text": "  context: /repo  +  ../lib  +  ../docs"},
                    {"type": "input", "text": "how does ../lib emit the events we consume in api/hooks?"},
                    {"type": "tool", "text": "  Grep(3)   ../lib/events"},
                    {"type": "output", "text": "  ../lib/events.ts emits on commit and on user.created"},
                ],
                "tip": "The same idea as @file references, but for whole directories.",
            },
            {
                "id": "s5",
                "title": "Script it with JSON output",
                "narration": (
                    "-p runs a prompt non-interactively. --output-format json gives structured output for "
                    "scripts, and stream-json gives live events for progress UIs."
                ),
                "command": "gemini -p \"list the endpoints in api/\" --output-format json",
                "lines": [
                    {"type": "input", "text": "gemini -p \"list the endpoints in api/\" --output-format json"},
                    {"type": "output", "text": "  {"},
                    {"type": "output", "text": "    \"response\": \"GET /api/health, POST /api/chat, ...\","},
                    {"type": "output", "text": "    \"stats\": { \"duration_ms\": 2410, \"models\": [\"gemini-2.5-flash\"] }"},
                    {"type": "output", "text": "  }"},
                ],
                "tip": "Use --output-format stream-json when you want progress in a long-running job instead of one blob at the end.",
            },
            {
                "id": "s6",
                "title": "MCP and where this is heading",
                "narration": (
                    "MCP servers live in ~/.gemini/settings.json. Note for 2026: Google has moved unpaid and "
                    "Google One users to Antigravity CLI, and recommends it for the newest Gemini models."
                ),
                "command": "~/.gemini/settings.json",
                "lines": [
                    {"type": "muted", "text": "  ~/.gemini/settings.json"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"mcpServers\": {"},
                    {"type": "accent", "text": "      \"github\": { \"command\": \"npx\", \"args\": [\"-y\", \"@modelcontextprotocol/server-github\"] }"},
                    {"type": "accent", "text": "    }"},
                    {"type": "accent", "text": "  }"},
                    {"type": "muted", "text": "  note: Gemini CLI was replaced by Antigravity CLI for unpaid"},
                    {"type": "muted", "text": "        and Google One tiers on 18 June 2026."},
                ],
                "tip": "Keep both installed if you use Google models - Antigravity CLI is the one tuned for the newest Gemini models.",
            },
        ],
    },
    {
        "id": "aider",
        "title": "Aider: architect plus editor",
        "agent": "aider",
        "level": "intermediate",
        "duration_min": 35,
        "summary": (
            "Aider treats every edit as a commit and splits thinking from editing, so a frontier model can "
            "plan while a cheap model does the typing. That combination is how you run a strong agent on a "
            "small budget."
        ),
        "outcome": [
            "A git-aware agent that commits every change",
            "A repo map that keeps context proportional",
            "Two models: one for architecture, one for edits",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Install and start in a repo",
                "narration": (
                    "Aider requires a git repository - that is how it tracks every change it makes. It "
                    "installs a helper binary so it can manage git without polluting your PATH."
                ),
                "command": "python -m pip install aider-install && aider-install",
                "lines": [
                    {"type": "input", "text": "python -m pip install aider-install && aider-install"},
                    {"type": "success", "text": "  installed aider 0.86.0"},
                    {"type": "input", "text": "cd ~/projects/my-app && aider"},
                    {"type": "output", "text": "  git repo detected  |  branch main  |  3 files in context"},
                ],
                "tip": "Run git init first if the folder is not a repo yet - aider will refuse to start otherwise.",
            },
            {
                "id": "s2",
                "title": "Load the right files",
                "narration": (
                    "The repo map is aider's trick: it builds a compact index of the whole repository so the "
                    "model knows where things live without reading everything. Add specific files when you "
                    "want them verbatim."
                ),
                "command": "/add backend/app/api/routes/health.py",
                "lines": [
                    {"type": "input", "text": "/add backend/app/api/routes/health.py"},
                    {"type": "output", "text": "  added 1 file  |  418 tokens"},
                    {"type": "output", "text": "  repo map: 87 files, 4,201 tokens of signatures"},
                    {"type": "muted", "text": "  (the map grows as the repo grows - you never paste whole files)"},
                ],
                "tip": "Use /read to pull a file into context permanently, /drop to remove it. Context is a budget - spend it deliberately.",
            },
            {
                "id": "s3",
                "title": "Ask before editing",
                "narration": (
                    "/ask runs a question in read-only mode. It is the cheapest way to understand code you "
                    "have not touched, and it never dirties your working tree."
                ),
                "command": "/ask why is the retry logic in three different places?",
                "lines": [
                    {"type": "input", "text": "/ask why is the retry logic in three different places?"},
                    {"type": "tool", "text": "  Read(3)   api/client.py, api/queue.py, workers/sync.py"},
                    {"type": "output", "text": "  Each was written for a different transport. api/client.py retries"},
                    {"type": "output", "text": "  HTTP 5xx, queue.py retries job failures, workers/sync.py retries"},
                    {"type": "output", "text": "  the nightly sync. They share no backoff policy."},
                ],
                "tip": "Questions are free - they cost no edit churn and no commits. Use them to explore first.",
            },
            {
                "id": "s4",
                "title": "Split architect and editor",
                "narration": (
                    "With --architect, a strong model writes the plan and a cheaper model applies it. The "
                    "expensive model thinks once; the cheap model writes the code."
                ),
                "command": "aider --architect --model gpt-4.1 --editor-model gpt-4o-mini",
                "lines": [
                    {"type": "input", "text": "aider --architect --model gpt-4.1 --editor-model gpt-4o-mini"},
                    {"type": "output", "text": "  architect model: gpt-4.1"},
                    {"type": "output", "text": "  editor model:    gpt-4o-mini"},
                    {"type": "input", "text": "extract the retry helper into api/retry.py and use it in all three places"},
                    {"type": "output", "text": "  ARCHITECT: create api/retry.py with retry(fn, attempts=3, backoff=0.5)"},
                    {"type": "output", "text": "  EDITOR:    applied to 4 files"},
                    {"type": "success", "text": "  commit 9f3a1c2  extract retry helper"},
                ],
                "tip": "This is the cheapest path to frontier-quality output: pay for the plan, not for every token of the diff.",
            },
            {
                "id": "s5",
                "title": "Review the diff",
                "narration": (
                    "Because every change is a commit, the diff is always available and always reversible. "
                    "/diff shows what is pending before you accept it."
                ),
                "command": "/diff",
                "lines": [
                    {"type": "input", "text": "/diff"},
                    {"type": "diff", "text": "  api/retry.py            +24"},
                    {"type": "diff", "text": "  api/client.py          +6   -11"},
                    {"type": "diff", "text": "  api/queue.py           +3   -9"},
                    {"type": "diff", "text": "  workers/sync.py        +2   -7"},
                    {"type": "muted", "text": "  4 files changed, 35 insertions, 27 deletions"},
                ],
                "tip": "/undo reverts the last change; /commit forces a commit right now instead of waiting for aider's own.",
            },
            {
                "id": "s6",
                "title": "Automate it",
                "narration": (
                    "--message starts with the task already loaded, so aider can run unattended in a script "
                    "or a pipeline."
                ),
                "command": "aider --message \"add a test for the retry helper\" --yes",
                "lines": [
                    {"type": "input", "text": "aider --message \"add a test for the retry helper\" --yes"},
                    {"type": "tool", "text": "  Read(1)   api/retry.py"},
                    {"type": "tool", "text": "  Write(1)  tests/test_retry.py"},
                    {"type": "success", "text": "  commit 41b7de9  add tests for retry helper"},
                ],
                "tip": "--yes accepts edits without prompting. Use it only in a throwaway branch.",
            },
        ],
    },
    {
        "id": "opencode-skills",
        "title": "Write your first agent skill",
        "agent": "opencode",
        "level": "intermediate",
        "duration_min": 30,
        "summary": (
            "Skills are the cheapest way to give an agent a procedure. One folder, one SKILL.md, and the "
            "harness advertises it by name so the model can pull the full text when the task calls for it."
        ),
        "outcome": [
            "A skill that loads on demand in any agent that speaks the format",
            "Permissions so a skill cannot be triggered by the wrong agent",
            "A slash command version of the skill for manual invocation",
        ],
        "steps": [
            {
                "id": "s1",
                "title": "Know when to use a skill",
                "narration": (
                    "Rules files are always in context, so they must stay short. Skills are advertised by "
                    "name and loaded only when needed, so they can be long and specific. If a procedure "
                    "only applies to one kind of task, it belongs in a skill."
                ),
                "lines": [
                    {"type": "muted", "text": "  AGENTS.md       always loaded   -> keep it under a page"},
                    {"type": "muted", "text": "  SKILL.md        loaded on demand -> can be a whole playbook"},
                    {"type": "muted", "text": "  MCP server      external tools    -> costs context on every turn"},
                ],
                "tip": "If you catch yourself pasting the same six steps into every prompt, that is a skill.",
            },
            {
                "id": "s2",
                "title": "Create the folder",
                "narration": (
                    "One directory per skill, named exactly like the skill, with SKILL.md inside in all "
                    "caps. The name must match the folder or the skill will not load."
                ),
                "command": "mkdir -p .opencode/skills/git-release",
                "lines": [
                    {"type": "input", "text": "mkdir -p .opencode/skills/git-release"},
                    {"type": "muted", "text": "  .opencode/skills/git-release/SKILL.md"},
                    {"type": "muted", "text": "  (the directory name must match the name in the frontmatter)"},
                ],
                "tip": "Project skills live in .opencode/skills/, global ones in ~/.config/opencode/skills/.",
            },
            {
                "id": "s3",
                "title": "Write the frontmatter",
                "narration": (
                    "Two required fields: name and description. The description is what the model reads to "
                    "decide whether to load the skill, so it has to say when to use it, not just what the "
                    "skill is about."
                ),
                "command": "cat .opencode/skills/git-release/SKILL.md",
                "lines": [
                    {"type": "muted", "text": "  ---"},
                    {"type": "accent", "text": "  name: git-release"},
                    {"type": "accent", "text": "  description: Create consistent releases and changelogs"},
                    {"type": "accent", "text": "  license: MIT"},
                    {"type": "accent", "text": "  compatibility: opencode"},
                    {"type": "accent", "text": "  metadata:"},
                    {"type": "accent", "text": "    audience: maintainers"},
                    {"type": "accent", "text": "    workflow: github"},
                    {"type": "accent", "text": "  ---"},
                    {"type": "output", "text": "  ## What I do"},
                    {"type": "output", "text": "  - Draft release notes from merged PRs"},
                    {"type": "output", "text": "  - Propose a version bump"},
                    {"type": "output", "text": "  - Provide a copy-pasteable `gh release create` command"},
                ],
                "tip": "Name rules: 1-64 characters, lowercase, single hyphens, no leading or trailing hyphen.",
            },
            {
                "id": "s4",
                "title": "See how the model finds it",
                "narration": (
                    "The harness lists every skill's name and description in the tool description. That is "
                    "the only part that costs context until the model decides to load the skill."
                ),
                "lines": [
                    {"type": "muted", "text": "  the skill tool description contains:"},
                    {"type": "output", "text": "  <available_skills>"},
                    {"type": "output", "text": "    <skill>"},
                    {"type": "output", "text": "      <name>git-release</name>"},
                    {"type": "output", "text": "      <description>Create consistent releases and changelogs</description>"},
                    {"type": "output", "text": "    </skill>"},
                    {"type": "output", "text": "  </available_skills>"},
                    {"type": "tool", "text": "  skill({ name: \"git-release\" })"},
                ],
                "tip": "Set metadata opencode/autoinvoke to \"false\" and the skill is still loadable by name, just not advertised.",
            },
            {
                "id": "s5",
                "title": "Control who can use it",
                "narration": (
                    "Skills are permissions like any other tool. Allow the ones you want, deny the "
                    "internal ones, ask for the experimental ones - with glob patterns."
                ),
                "command": "opencode.json",
                "lines": [
                    {"type": "muted", "text": "  // opencode.json"},
                    {"type": "accent", "text": "  {"},
                    {"type": "accent", "text": "    \"permission\": {"},
                    {"type": "accent", "text": "      \"skill\": {"},
                    {"type": "accent", "text": "        \"*\": \"allow\","},
                    {"type": "accent", "text": "        \"internal-*\": \"deny\","},
                    {"type": "accent", "text": "        \"experimental-*\": \"ask\""},
                    {"type": "accent", "text": "      }"},
                    {"type": "accent", "text": "    }"},
                    {"type": "accent", "text": "  }"},
                ],
                "tip": "Per agent, put the same permission block in the agent frontmatter or in opencode.json under agent.<name>.permission.",
            },
            {
                "id": "s6",
                "title": "Also expose it as a command",
                "narration": (
                    "Sometimes you want to trigger the skill yourself rather than let the model decide. One "
                    "metadata key turns it into a slash command in the TUI."
                ),
                "command": "/git-release",
                "lines": [
                    {"type": "accent", "text": "  metadata:"},
                    {"type": "accent", "text": "    opencode/slash: \"true\""},
                    {"type": "input", "text": "/git-release"},
                    {"type": "output", "text": "  loading skill git-release ..."},
                    {"type": "output", "text": "  merged PRs since the last tag: 14"},
                    {"type": "output", "text": "  proposed version: 2.4.0 (minor - new endpoint, no breaking changes)"},
                    {"type": "output", "text": "  gh release create v2.4.0 --generate-notes"},
                ],
                "tip": "Slash and autoinvoke are independent: you can expose a command and still keep it out of automatic selection.",
            },
            {
                "id": "s7",
                "title": "Debug the two common failures",
                "narration": (
                    "Almost every 'my skill does not show up' problem is one of five things. Check them in "
                    "order and it takes thirty seconds."
                ),
                "lines": [
                    {"type": "muted", "text": "  1. SKILL.md spelled in all caps"},
                    {"type": "muted", "text": "  2. frontmatter has both name and description"},
                    {"type": "muted", "text": "  3. name is unique across every discovery location"},
                    {"type": "muted", "text": "  4. no permission denies it"},
                    {"type": "muted", "text": "  5. metadata opencode/autoinvoke is not \"false\""},
                    {"type": "success", "text": "  -> skill listed in the tool description"},
                ],
                "tip": "Skills are also portable: the same folder works from .claude/skills and .agents/skills.",
            },
        ],
    },
]


WALKTHROUGH_IDS = [w["id"] for w in WALKTHROUGHS]


def walkthrough_by_id(walkthrough_id: str) -> dict[str, Any] | None:
    for walkthrough in WALKTHROUGHS:
        if walkthrough["id"] == walkthrough_id:
            return walkthrough
    return None
