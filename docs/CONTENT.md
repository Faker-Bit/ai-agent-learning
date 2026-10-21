# Editing the content

Everything the site renders is Python data. Restart the API (or wait for `--reload`) and the change is
live.

## Terminal lines

A terminal line is `{"type": ..., "text": ...}`. The type drives the colour and prefix.

| type | prefix | colour | use it for |
|---|---|---|---|
| `input` | `$ ` | phosphor green | something the user typed |
| `output` | two spaces | body text | program output |
| `tool` | `⎿ ` | cyan | an agent tool call (`Read(2)  file.ts`) |
| `success` | `✓ ` | phosphor green | a verified result |
| `warn` | `⚠ ` | amber | a warning or a failure |
| `muted` | two spaces | muted grey | commentary, separators, hints |
| `accent` | two spaces | violet | config, notes |
| `info` | two spaces | body text | informational output |
| `diff` | none | green for `+`, red for `-` | diff lines |

Lines are typed character by character, so keep them short — a line longer than ~90 characters wraps.

## Adding an agent

```python
{
    "id": "my-agent",
    "name": "my-agent",
    "tagline": "One line that says what it is",
    "kind": "CLI",                  # CLI | IDE | Models | Platform
    "license": "MIT",
    "docs": "https://example.com/docs",
    "repo": "https://github.com/example/my-agent",
    "install": "npm install -g my-agent",
    "install_alt": "brew install my-agent",
    "install_windows": "npm install -g my-agent",
    "best_for": "The one job this tool is genuinely best at.",
    "highlights": ["...", "...", "...", "..."],   # at least four
    "commands": [["my-agent", "What it does"]],   # command + description
    "walkthroughs": ["walkthrough-id"],           # must exist in walkthroughs.py
    "accent": "green",
}
```

Then add its commands to `content/cheatsheet.py`:

```python
{"agent": "my-agent", "group": "My Agent", "command": "my-agent --help", "description": "Show the CLI help"},
```

## Adding a walkthrough

```python
{
    "id": "my-agent-basics",
    "title": "My agent in 20 minutes",
    "agent": "my-agent",           # must exist in agents.py
    "level": "beginner",
    "duration_min": 20,
    "summary": "One paragraph: what this session covers.",
    "outcome": ["What the learner can do afterwards", "..."],
    "steps": [
        {
            "id": "s1",
            "title": "Install it",
            "narration": "Why this step matters and what to watch for.",
            "command": "npm install -g my-agent",     # optional, copyable
            "lines": [
                {"type": "input", "text": "npm install -g my-agent"},
                {"type": "success", "text": "  added 1 package in 4s"},
            ],
            "tip": "An optional aside that appears under the terminal.",
        },
    ],
}
```

Rules the test suite enforces: at least five steps, every step has a title, narration and at least one
line, every line uses a known type, and the `agent` field matches an agent id.

## Adding a craft rule

`content/guide.py` → `CRAFT`. Each entry needs a `before` and `after` block of terminal lines — the
before shows the vague version, the after shows the version that works. They animate side by side
when they scroll into view.

## Adding a model or provider

`providers/registry.py`:

- `PROVIDER_META` — one entry per provider: id, label, kind, tier (`free`, `paid`, `local`,
  `free+paid`), signup URL, note, env key, default base URL.
- `CURATED_MODELS` — one entry per model: id, name, provider, description, context window, `free`
  flag, `requires_key`.

## After editing

```bat
cd backend
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe tools\smoke.py
```

The integrity tests will tell you exactly which entry is malformed.
