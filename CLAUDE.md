# CLAUDE.md

## Project Overview
gpu-learning-lab is a repository for CUDA, GPU Computing, RunPod experiments, and Nvidia accelerated computing tutorials. It includes an AI-powered CLI agent (Mission Control) that has full knowledge of the codebase.

## Repository Structure
```
├── agents/
│   ├── base.py              # BaseAgent ABC — lifecycle, pub/sub, skill dispatch
│   ├── orchestrator/        # OrchestratorAgent — job/step state machines + planner
│   ├── repo_analyst/        # RepoAnalystAgent — file listing, code explanation
│   ├── coder/               # CoderAgent — read/write/patch/generate code files
│   ├── infra_manager/       # InfraManagerAgent — GPU/CPU/RAM/Docker/Redis health
│   ├── integration/         # IntegrationAgent — HTTP, RunPod GraphQL, webhooks
│   └── ui/                  # UIAgent — SSE broadcast, dashboard state snapshot
├── core/
│   ├── event_bus.py         # In-memory pub/sub (fnmatch wildcards); Redis Streams ready
│   └── state_store.py       # In-memory KV store with TTL; Redis ready
├── skills/
│   ├── base.py              # BaseSkill ABC, SkillResult, SkillContext, RetryPolicy
│   ├── registry.py          # Auto-discovery from skills.builtin + skills.custom
│   └── builtin/
│       ├── file_manager.py  # read/write/list/exists/delete with traversal guard
│       ├── runpod.py        # list/start/stop/terminate RunPod cloud GPU pods
│       ├── http_client.py   # GET/POST/ping outbound HTTP with JSON parsing
│       └── notion.py        # Notion workspace — pages, databases, blocks
├── tests/                   # pytest-asyncio suite — 145 tests, all green
├── tutorials/               # Accelerated Python notebooks (NumPy, CUDA, etc.)
├── web/index.html           # Mission Control dashboard (SSE, 5-panel grid)
└── main.py                  # FastAPI server — all 6 agents, SSE, REST API
```

## Key Commands

### Run the Mission Control server
```bash
uvicorn main:app --port 8000
# Dashboard: http://localhost:8000
```
> **Note:** Do NOT use `--reload` when testing SSE features (`/events`, `/chat/stream`, `/tasks/{id}/stream`).
> StatReload kills in-flight SSE connections on every file save.

### Run tests
```bash
pytest tests/ -v
```

### Install dependencies
```bash
pip install -e ".[dev]"
# or: pip install -r requirements.txt
```

## Environment Setup
`.env` credentials live at `.venv/.env`. To move them to project root:
```
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_MODEL=claude-opus-4-5
```
The agent checks project root first, then falls back to `.venv/.env`.

## Architecture Notes
- **Event bus** — in-memory asyncio pub/sub with fnmatch wildcards; drop-in Redis Streams swap via `REDIS_URL` env var
- **State store** — in-memory KV with TTL; same Redis swap path
- **Planner** — regex fast-path (5 patterns, no API cost) → LLM fallback (Claude in thread executor, non-blocking)
- **Skill plugin system** — drop a file in `skills/builtin/` or `skills/custom/`; auto-discovered at startup
- **UIAgent** — starts FIRST in lifespan so it catches all agent.started events; bootstraps from state store on restart
- **SSE** — 20s heartbeat keepalive; snapshot sent immediately on connect
- **Streaming chat** (`/chat/stream`) — SSE endpoint; smart-routes action verbs to orchestrator, streams Claude response in parallel, appends agent result inline when job finishes
- **Job-specific SSE** (`/tasks/{id}/stream`) — live step/job events via `_job_waiters` queues in `OrchestratorAgent`; `subscribe_job`/`unsubscribe_job` API

## Code Conventions
- Python 3.10+, UTF-8 everywhere
- `asyncio_mode = "auto"` in pyproject.toml — all test classes use `async def` methods
- Notebooks live under `tutorials/<topic>/notebooks/<level>/`
- New skills: subclass `BaseSkill`, set `name`/`description`, implement `async execute()`, drop in `skills/builtin/`

## Infrastructure
- Redis: `docker compose up redis -d` (port 6379)
- `docker-compose.yml` at project root — Redis + API containers
- `pyproject.toml` replaces `requirements.txt` as source of truth for deps
- New deps added: `pydantic-settings`, `redis`, `httpx`

## Current Status
| Area | Status |
|------|--------|
| FastAPI server + REST API | Working |
| Mission Control dashboard (SSE) | Working |
| BaseAgent + skill dispatch | Working |
| OrchestratorAgent + Job/Step state machines | Working |
| Planner (regex fast-path + LLM fallback) | Working |
| RepoAnalystAgent | Working |
| CoderAgent (read/write/patch/generate) | Working |
| InfraManagerAgent (GPU/CPU/RAM/Docker/Redis) | Working |
| IntegrationAgent (HTTP/RunPod GraphQL/webhooks) | Working |
| UIAgent (SSE broadcast + state bootstrap) | Working |
| Test suite | 303 tests, all green |
| RunPod exec skill (SSH bridge) | Working |
| Adaptive replanning (LLM recovery) | Working |
| Prompt injection sanitization | Working |
| Secret masking (error responses) | Working |
| Rate limiting middleware | Working |
| Dead letter queue (EventBus) | Working |
| Metrics collector (counters/gauges/histograms) | Working |
| Agent watchdog (stall detection + alerts) | Working |
| Skill retry + exponential backoff | Working |
| Job cleanup sweep (TTL enforcement) | Working |
| Event sequence numbers + SSE replay buffer | Working |
| Skill execution timeouts | Working |
| Graceful shutdown + job recovery | Working |
| Circuit breaker (external services) | Working |
| Structured logging (JSON + context) | Working |
| Agent capability declaration | Working |
| Health/readiness probes (/health, /ready) | Working |
| RunPod skill (builtin plugin) | Working |
| HTTP client skill (builtin plugin) | Working |
| Notion skill (builtin plugin) | Working — needs NOTION_API_KEY in .env |
| NotionSyncAgent (work folder) | Working — set NOTION_WORK_DB_ID in .env or via POST /config |
| GPU/CUDA tutorial content | One NumPy notebook |

## User Preferences
- Direct, concise communication — no filler
- No emojis unless asked
- Apply changes immediately rather than proposing them
- Mission Control framing — the AI agent is the command center for the project
