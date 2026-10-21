# Windows setup

## Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.12+ (tested on 3.14.7) | `python --version` |
| Node.js | 20+ (tested on 24.20) | `node --version` |

If `npm` fails with *"cannot be loaded because running scripts is disabled"*, that is the PowerShell
execution policy, not a broken install. Use `npm.cmd` instead of `npm`, or run `start.bat` (which
already calls `npm.cmd`).

## First run

```bat
start.bat
```

It will:

1. create `backend\.venv` if missing;
2. install `backend\requirements.txt`;
3. copy `backend\.env.example` to `backend\.env` if it does not exist;
4. install `frontend\node_modules` if missing;
5. run `npm run build` in `frontend`;
6. start the API on `http://127.0.0.1:8010` and open it.

The SPA is served by FastAPI from `frontend\dist`, so a single port is enough. For hot reload during
development run the API and Vite separately:

```bat
:: shell 1
cd backend
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8010 --reload

:: shell 2
cd frontend
npm run dev
```

Then open `http://127.0.0.1:5173` â€” Vite proxies `/api` to `:8010`.

## Port conflicts

The backend defaults to **8010** (8000 is often taken by other local apps). Change it in
`backend\.env`:

```
AMT_PORT=8011
```

If you run Vite on a different port, add it to the CORS allowlist:

```
AMT_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174
```

## Adding a provider

1. Open **Settings â†’ Providers**.
2. Paste the key under the provider and press **Save**.
3. Press **Test** â€” it lists the provider's models or sends a one-token probe.

Keys are written to `amt.db` (SQLite) on this machine and never sent to the browser again. Environment
variables in `backend\.env` take precedence over stored keys.

Free tiers worth starting with:

| Provider | Why |
|---|---|
| Google AI Studio | Generous flash quotas, no credit card, 1M context |
| Groq | Fastest inference, 14k requests/day on small models |
| OpenCode Zen | Nine free coding models, OpenAI-compatible |
| Cerebras | 1.5M free tokens/day, 2,400 tok/s |
| OpenRouter | Any model, `:free` suffix for the free ones |

## The sandbox

Code exercises run in a separate Python process with:

- a 10-second wall clock limit (`AMT_SANDBOX_TIMEOUT_SECONDS`);
- a scrubbed environment (no inherited PATH beyond the system, no user site-packages);
- a static denylist for dangerous imports, calls and dunder access;
- on POSIX, an address-space and CPU rlimit.

The denylist blocks `os`, `subprocess`, `socket`, `pathlib`, `sys`, `open`, `eval`, `exec` and friends.
This is a learning sandbox, not a security boundary for untrusted code â€” do not run code you did not
write.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| **"Could not load the site content" with a Retry button** | The API is not running, or an **old server from a previous build** still owns port 8010 and serves the previous API (the SPA is new, the API is old â†’ `/api/site` 404). | Run `start.bat` again â€” it now kills whatever is listening on 8010 first. Or run `.\stop.ps1`. |
| Page renders but an amber banner says "showing the bundled copy" | The backend is down or unreachable; the site fell back to the copy bundled at build time. | Start the backend (`start.bat`). Everything still works read-only. |
| Banner is missing and the site loads live | Normal. The bundled copy is only used when `/api/site` fails. | â€” |
| `ModuleNotFoundError: No module named 'app'` | Running from the wrong directory | Start the API from `backend\` |
| Frontend loads but every call fails | Vite proxy target wrong | `set VITE_PROXY_TARGET=http://127.0.0.1:8010` before `npm run dev` |
| `429 Too many requests` | Rate limiter (240 requests/minute per IP) | Wait a minute; raise `AMT_RATE_LIMIT_REQUESTS` if needed |
| Tutor/model tools say the key is missing | No provider configured | Settings â†’ Providers â†’ paste a key â†’ Save |
| Port 8010 in use | Another process | `netstat -ano \| findstr :8010`, or change `AMT_PORT` |

### How the content reaches the page

```
backend/app/content/*.py   (the source of truth)
        â”‚  tools/export_content.py
        â–¼
frontend/src/content/site.json   (bundled copy â€” the site renders even if the API is down)
        â”‚
        â–¼
GET /api/site   (live payload, same content)
```

Re-run `python backend/tools/export_content.py` after editing the Python content, or just run
`start.bat`, which does it for you before building the frontend.

## Resetting local state

Progress, sessions, quiz history and stored keys all live in `backend\amt.db`. Delete it to start
clean:

```bat
del backend\amt.db
```

The catalog, lessons, glossary and provider catalog are seeded from code, not from the database, so
they come back automatically.
