import asyncio
import json
import logging
import os
import re
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

from anthropic import AsyncAnthropic, Anthropic
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

# ---------------------------------------------------------------------------
# Load .env — prefer project root, fall back to .venv/.env
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
env_path = ROOT / ".env"
venv_env = ROOT / ".venv" / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
elif venv_env.exists():
    load_dotenv(dotenv_path=venv_env)
else:
    load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL   = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")

if not API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not set in .env")

anthropic_client       = Anthropic(api_key=API_KEY)
anthropic_async_client = AsyncAnthropic(api_key=API_KEY)

# ---------------------------------------------------------------------------
# API key authentication
# ---------------------------------------------------------------------------
MC_API_KEY = os.getenv("MC_API_KEY", "")

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Endpoints that don't require auth (public dashboard + static)
_PUBLIC_PATHS = frozenset({"/", "/mobile", "/docs", "/openapi.json", "/redoc", "/health", "/ready"})


async def require_api_key(
    request: Request,
    api_key: str | None = Depends(_api_key_header),
):
    """Reject requests without a valid API key.
    Accepts key via X-API-Key header or ?api_key= query param (for EventSource).
    Skipped for public paths and when MC_API_KEY is not configured (dev mode).
    """
    if not MC_API_KEY:
        return  # auth disabled — dev mode (no MC_API_KEY set)
    if request.url.path in _PUBLIC_PATHS:
        return  # public endpoints
    if api_key and api_key == MC_API_KEY:
        return  # valid header key
    # Fallback: query param (EventSource can't set headers)
    query_key = request.query_params.get("api_key")
    if query_key and query_key == MC_API_KEY:
        return
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid or missing API key. Set X-API-Key header.",
    )


# ---------------------------------------------------------------------------
# Multi-agent infrastructure
# ---------------------------------------------------------------------------
from core.config import settings
from core.event_bus import Event, EventBus
from core.metrics import metrics
from core.rate_limit import RateLimitMiddleware
from core.sanitize import mask_secrets, safe_error
from core.state_store import StateStore
from core.watchdog import AgentWatchdog
from skills.registry import registry
from agents.orchestrator import OrchestratorAgent
from agents.repo_analyst import RepoAnalystAgent
from agents.coder import CoderAgent
from agents.infra_manager import InfraManagerAgent
from agents.integration import IntegrationAgent
from agents.ui import UIAgent
from agents.notion_sync import NotionSyncAgent
from agents.news_scout import NewsScoutAgent
from agents.publisher import PublisherAgent
from agents.social import SocialAgent

bus   = EventBus(redis_url=settings.redis_url)
store = StateStore(redis_url=settings.redis_url)

orchestrator   = OrchestratorAgent(
    llm_client=anthropic_client, llm_model=MODEL,
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
repo_analyst   = RepoAnalystAgent(
    llm_client=anthropic_client, llm_model=MODEL,
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
coder          = CoderAgent(
    llm_client=anthropic_client, llm_model=MODEL,
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
infra_manager  = InfraManagerAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
    check_interval=60.0,
)
integration    = IntegrationAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
    runpod_api_key=os.getenv("RUNPOD_API_KEY", ""),
)
ui_agent       = UIAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
notion_sync    = NotionSyncAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
news_scout     = NewsScoutAgent(
    llm_client=anthropic_async_client, llm_model=MODEL,
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
publisher      = PublisherAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)
social         = SocialAgent(
    bus=bus, store=store, registry=registry, project_root=str(ROOT),
)

_ALL_AGENTS = [
    orchestrator, repo_analyst, coder, infra_manager,
    integration, ui_agent, notion_sync,
    news_scout, publisher, social,
]

# ---------------------------------------------------------------------------
# Lifespan — start/stop all agents with the server
# ---------------------------------------------------------------------------
watchdog = AgentWatchdog(bus=bus, store=store, agents=_ALL_AGENTS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from core.logging import configure_logging
    configure_logging()
    await bus.connect()
    await store.connect()
    # UIAgent starts first so it is subscribed before other agents emit events
    await ui_agent.start()
    for agent in [orchestrator, repo_analyst, coder, infra_manager, integration, notion_sync,
                  news_scout, publisher, social]:
        await agent.start()
    await watchdog.start()
    metrics.gauge("agents.total", len(_ALL_AGENTS))
    yield
    # --- Graceful shutdown ---
    logger.info("Graceful shutdown: persisting in-flight jobs")
    await orchestrator.persist_active_jobs()
    # Drain event bus queue (max 5s)
    try:
        await asyncio.wait_for(bus._queue.join(), timeout=5.0)
    except asyncio.TimeoutError:
        logger.warning("Event bus drain timed out after 5s — proceeding with shutdown")
    await watchdog.stop()
    for agent in reversed(_ALL_AGENTS):
        await agent.stop()
    await bus.disconnect()
    await store.disconnect()
    logger.info("Graceful shutdown complete")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="Mission Control", lifespan=lifespan)

_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("MC_CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_methods=["POST", "GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)
app.add_middleware(RateLimitMiddleware)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    messages: list[dict]
    system: str | None = None


class TaskRequest(BaseModel):
    description: str
    title: str = ""
    requested_by: str = "user"


# ---------------------------------------------------------------------------
# Routes — UI (dashboard)
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    index = ROOT / "web" / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="web/index.html not found")
    return FileResponse(str(index))


@app.get("/mobile")
def mobile():
    page = ROOT / "web" / "mobile.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="web/mobile.html not found")
    return FileResponse(str(page))


# ---------------------------------------------------------------------------
# Routes — SSE live dashboard stream
# ---------------------------------------------------------------------------
@app.get("/events", dependencies=[Depends(require_api_key)])
async def sse_events(since: int = 0):
    """Server-Sent Events stream — pushes dashboard snapshots to the browser.

    Query params:
        since  — replay all events with sequence > since before switching to live
    """
    q = ui_agent.add_sse_subscriber()

    async def stream():
        # Replay missed events if client provides ?since=N
        if since > 0:
            missed = bus.replay_since(since)
            for evt in missed:
                yield f"id: {evt.sequence}\ndata: {json.dumps({'event_type': evt.event_type, 'payload': evt.payload, 'source': evt.source, 'sequence': evt.sequence})}\n\n"

        # Send current snapshot immediately on connect
        snap = json.dumps({**ui_agent.snapshot(), "sequence": bus.last_sequence})
        yield f"id: {bus.last_sequence}\ndata: {snap}\n\n"
        try:
            while True:
                try:
                    data = await asyncio.wait_for(q.get(), timeout=20.0)
                    seq = bus.last_sequence
                    yield f"id: {seq}\ndata: {data}\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"   # keep connection alive
        except asyncio.CancelledError:
            pass
        finally:
            ui_agent.remove_sse_subscriber(q)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------------------------------------------------------------------------
# Routes — model info
# ---------------------------------------------------------------------------
@app.get("/model", dependencies=[Depends(require_api_key)])
def get_model():
    return {"model": MODEL, "mode": bus.mode}


# ---------------------------------------------------------------------------
# Routes — direct Claude chat
# ---------------------------------------------------------------------------
@app.post("/chat", dependencies=[Depends(require_api_key)])
def chat(req: ChatRequest):
    system = req.system or (
        "You are Mission Control — an AI assistant with expertise in CUDA, GPU computing, "
        "RunPod, and Nvidia accelerated computing. Be concise and technical."
    )
    try:
        response = anthropic_client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system,
            messages=req.messages,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=safe_error(exc))

    content = response.content[0].text if response.content else ""
    return {
        "content": content,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }


# ---------------------------------------------------------------------------
# Routes — streaming chat
# ---------------------------------------------------------------------------

# Keywords that mean "this is a task, not a chat question"
_TASK_KEYWORDS = re.compile(
    r"\b(list|read|write|create|delete|check|run|ping|start|stop|terminate|"
    r"explain|summarise?|summarize|generate|patch|review)\b",
    re.I,
)

_CHAT_SYSTEM = (
    "You are Mission Control — an AI assistant with deep expertise in CUDA, GPU computing, "
    "RunPod, and Nvidia accelerated computing. Be concise and technical.\n\n"
    "You operate alongside a multi-agent system. When the user asks you to actually DO something "
    "(list files, check GPU, ping a URL, manage pods, etc.) tell them: "
    "'[Routing to agent system…]' and then describe what you would dispatch — but the UI "
    "will automatically route action requests for you. For pure questions, just answer directly."
)


@app.post("/chat/stream", dependencies=[Depends(require_api_key)])
async def chat_stream(req: ChatRequest):
    """Streaming chat endpoint — returns SSE with delta tokens."""
    system = req.system or _CHAT_SYSTEM

    async def generate():
        dispatched_job_id: str | None = None

        # Smart routing: detect task-like messages and submit to orchestrator
        last_user = next(
            (m["content"] for m in reversed(req.messages) if m.get("role") == "user"), ""
        )
        if _TASK_KEYWORDS.search(last_user) and len(last_user) < 300:
            try:
                job_id = await orchestrator.submit_task(
                    description=last_user,
                    title=last_user[:60],
                    requested_by="chat",
                )
                dispatched_job_id = job_id
                routing_msg = f"[Task submitted → job {job_id[:8]}…]\n\n"
                yield f"data: {json.dumps({'delta': routing_msg, 'job_id': job_id})}\n\n"
            except Exception:
                pass

        # Stream Claude's framing response
        try:
            async with anthropic_async_client.messages.stream(
                model=MODEL,
                max_tokens=2048,
                system=system,
                messages=req.messages,
            ) as stream:
                async for text in stream.text_stream:
                    yield f"data: {json.dumps({'delta': text})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': safe_error(exc)})}\n\n"
            return

        # If a task was submitted, wait up to 15s for it to finish via waiter queue
        if dispatched_job_id:
            q = orchestrator.subscribe_job(dispatched_job_id)
            try:
                # If job already done (e.g. instant file op), check immediately
                job_obj = orchestrator._jobs.get(dispatched_job_id)
                if job_obj and job_obj.status.value in ("completed", "failed"):
                    result_text = _format_job_result(job_obj.to_dict())
                    yield f"data: {json.dumps({'delta': result_text})}\n\n"
                else:
                    try:
                        event = await asyncio.wait_for(q.get(), timeout=15.0)
                        if event.get("type") == "job.done":
                            result_text = _format_job_result(event["job"])
                            yield f"data: {json.dumps({'delta': result_text})}\n\n"
                    except asyncio.TimeoutError:
                        pass
            finally:
                orchestrator.unsubscribe_job(dispatched_job_id, q)

        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _format_job_result(job: dict) -> str:
    """Format a completed job's step results as a compact text block for the chat."""
    status = job.get("status", "unknown")
    steps  = job.get("steps", [])
    lines  = [f"\n\n**Agent result** ({status}):"]
    for step in steps:
        name   = step.get("name", "step")
        result = step.get("result")
        error  = step.get("error", "")
        if result is not None:
            body = result if isinstance(result, str) else json.dumps(result, indent=2)
            # Truncate very long results
            if len(body) > 1500:
                body = body[:1500] + "\n…[truncated]"
            lines.append(f"\n`{name}`:\n{body}")
        elif error:
            lines.append(f"\n`{name}` failed: {error}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Routes — multi-agent task API
# ---------------------------------------------------------------------------
@app.post("/tasks", dependencies=[Depends(require_api_key)])
async def submit_task(req: TaskRequest):
    job_id = await orchestrator.submit_task(
        description=req.description,
        title=req.title,
        requested_by=req.requested_by,
    )
    return {"job_id": job_id, "status": "queued"}


@app.get("/tasks/{job_id}", dependencies=[Depends(require_api_key)])
async def get_task(job_id: str):
    job = await orchestrator.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id!r} not found")
    return job


@app.get("/tasks", dependencies=[Depends(require_api_key)])
async def list_tasks():
    return await orchestrator.list_jobs()


@app.get("/tasks/{job_id}/stream", dependencies=[Depends(require_api_key)])
async def stream_task(job_id: str):
    """SSE stream for a specific job — pushes step and job events until done."""
    async def generate():
        # Send current snapshot immediately
        job = await orchestrator.get_job(job_id)
        if not job:
            yield f"data: {json.dumps({'error': f'Job {job_id!r} not found'})}\n\n"
            return
        yield f"data: {json.dumps({'type': 'snapshot', 'job': job})}\n\n"

        # If already finished, nothing more to send
        if job.get("status") in ("completed", "failed", "cancelled"):
            yield f"data: {json.dumps({'type': 'job.done', 'job': job})}\n\n"
            return

        q = orchestrator.subscribe_job(job_id)
        try:
            while True:
                try:
                    event = await asyncio.wait_for(q.get(), timeout=20.0)
                    yield f"data: {json.dumps(event)}\n\n"
                    if event.get("type") == "job.done":
                        break
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            orchestrator.unsubscribe_job(job_id, q)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ---------------------------------------------------------------------------
# Routes — agent status
# ---------------------------------------------------------------------------
@app.get("/agents", dependencies=[Depends(require_api_key)])
async def list_agents():
    states = []
    for agent in _ALL_AGENTS:
        state = await agent.get_state()
        states.append(state.to_dict())
    return states


# ---------------------------------------------------------------------------
# Routes — metrics / observability
# ---------------------------------------------------------------------------
@app.get("/metrics", dependencies=[Depends(require_api_key)])
async def get_metrics():
    """Return full metrics snapshot (counters, gauges, histograms)."""
    snap = metrics.snapshot()
    # Inject live bus/watchdog state
    snap["gauges"]["eventbus.dlq_count"] = bus.dead_letter_count
    snap["gauges"]["watchdog.stalled_count"] = len(watchdog.stalled_agents)
    return snap


# ---------------------------------------------------------------------------
# Routes — health / readiness probes (unauthenticated for load balancers)
# ---------------------------------------------------------------------------
@app.get("/health")
async def health_check():
    """Liveness probe — returns 200 if the process is alive."""
    return {
        "status": "ok",
        "uptime_seconds": round(metrics.snapshot().get("uptime_seconds", 0), 1),
    }


@app.get("/ready")
async def readiness_check():
    """Readiness probe — returns 200 only if all critical subsystems are healthy."""
    issues = []

    # Check agent statuses
    agent_states = {}
    for agent in _ALL_AGENTS:
        state = await agent.get_state()
        status_val = state.status.value
        agent_states[state.role] = status_val
        if status_val == "error":
            issues.append(f"Agent '{state.role}' is in ERROR state")

    running = sum(1 for s in agent_states.values() if s == "running")
    error_count = sum(1 for s in agent_states.values() if s == "error")
    stalled = len(watchdog.stalled_agents)

    # Check DLQ
    dlq_count = bus.dead_letter_count
    dlq_threshold = 50
    if dlq_count >= dlq_threshold:
        issues.append(f"DLQ has {dlq_count} entries (threshold: {dlq_threshold})")

    # Check stalled agents
    if stalled > 0:
        issues.append(f"{stalled} agent(s) stalled")

    ready = len(issues) == 0
    status_code = 200 if ready else 503

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": ready,
            "issues": issues,
            "dependencies": {
                "event_bus": {"mode": bus.mode, "dlq_count": dlq_count},
                "state_store": {"mode": store.mode},
                "agents": {
                    "total": len(_ALL_AGENTS),
                    "running": running,
                    "error": error_count,
                    "stalled": stalled,
                },
            },
        },
    )


# ---------------------------------------------------------------------------
# Routes — infrastructure health
# ---------------------------------------------------------------------------
@app.get("/infra", dependencies=[Depends(require_api_key)])
async def get_infra():
    cached = await store.get("infra:health")
    if cached:
        return cached
    return await infra_manager._health()


@app.post("/infra/check", dependencies=[Depends(require_api_key)])
async def trigger_infra_check():
    await bus.publish(Event(event_type="infra.check", payload={}, source="api"))
    return {"status": "check triggered"}


@app.get("/infra/dlq", dependencies=[Depends(require_api_key)])
async def get_dead_letters():
    """Return dead-lettered events from the event bus."""
    return {
        "count": bus.dead_letter_count,
        "entries": [
            {
                "event_type": dl.event.event_type,
                "event_id": dl.event.event_id,
                "handler": dl.handler_name,
                "error": dl.error,
                "attempts": dl.attempts,
                "timestamp": dl.timestamp,
            }
            for dl in bus.dead_letters
        ],
    }


@app.delete("/infra/dlq", dependencies=[Depends(require_api_key)])
async def clear_dead_letters():
    """Clear the dead letter queue."""
    cleared = bus.clear_dead_letters()
    return {"cleared": cleared}


# ---------------------------------------------------------------------------
# Routes — runtime config (Notion work folder, etc.)
# ---------------------------------------------------------------------------

_ALLOWED_CONFIG_KEYS = {
    "notion_work_db_id",
    "notion_api_key",
    "runpod_api_key",
    "runpod_flux_schnell_id",
    "runpod_flux_dev_id",
    "runpod_flux_kontext_id",
}

_ENV_KEY_MAP = {
    "notion_api_key":    "NOTION_API_KEY",
    "notion_work_db_id": "NOTION_WORK_DB_ID",
    "runpod_api_key":    "RUNPOD_API_KEY",
    "runpod_flux_schnell_id": "RUNPOD_FLUX_SCHNELL_ID",
    "runpod_flux_dev_id":     "RUNPOD_FLUX_DEV_ID",
    "runpod_flux_kontext_id": "RUNPOD_FLUX_KONTEXT_ID",
}


def _persist_to_env(key: str, value: str) -> None:
    """Write or update a KEY=value line in the project .env file."""
    env_file = ROOT / ".env"
    lines = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    upper = key.upper()
    found = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{upper}=") or line.startswith(f"{upper} ="):
            new_lines.append(f"{upper}={value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{upper}={value}")
    sep = chr(10)
    env_file.write_text(sep.join(new_lines) + sep, encoding="utf-8")
    os.environ[upper] = value  # apply to running process too


class ConfigRequest(BaseModel):
    key: str
    value: str


@app.get("/config", dependencies=[Depends(require_api_key)])
async def get_config():
    """Return current runtime configuration (sensitive values masked)."""
    runpod_key_stored = await store.get("config:runpod_api_key") or ""
    return {
        "notion_work_db_id":  notion_sync.get_config()["notion_work_db_id"],
        "notion_api_key_set": notion_sync.get_config()["notion_api_key_set"],
        "runpod_api_key_set": "yes" if (runpod_key_stored or os.getenv("RUNPOD_API_KEY")) else "no",
        "model": MODEL,
    }


@app.post("/config", dependencies=[Depends(require_api_key)])
async def set_config(req: ConfigRequest):
    """Set a runtime config value. Stored in StateStore and persisted to .env."""
    if req.key not in _ALLOWED_CONFIG_KEYS:
        raise HTTPException(status_code=400, detail=f"Unknown config key {req.key!r}")

    store_key = f"config:{req.key}"
    await store.set(store_key, req.value)

    # Persist to .env so the value survives server restarts
    env_var = _ENV_KEY_MAP.get(req.key)
    if env_var:
        _persist_to_env(env_var, req.value)

    # Notify agents so they pick up the change immediately
    await bus.publish(Event(event_type="config.updated", payload={"key": store_key, "value": req.value}, source="api"))

    # Apply to notion_sync directly for instant effect
    if req.key == "notion_work_db_id":
        notion_sync.set_config(db_id=req.value)
    elif req.key == "notion_api_key":
        notion_sync.set_config(api_key=req.value)

    return {"key": req.key, "status": "updated"}


# ---------------------------------------------------------------------------
# Routes — file upload (IoT data, logs, CSVs, zips, etc.)
# ---------------------------------------------------------------------------

WORKSPACE = ROOT / "workspace"
WORKSPACE.mkdir(exist_ok=True)

_MAX_UPLOAD_BYTES = 200 * 1024 * 1024   # 200 MB (zips can be large)
_MAX_EXTRACT_BYTES = 500 * 1024 * 1024  # 500 MB total uncompressed guard


def _safe_extract_zip(zip_path: Path, dest_dir: Path) -> list[str]:
    """
    Extract a zip into dest_dir with full path-traversal protection.
    Returns relative paths (from project root) of all extracted files.
    Raises ValueError on zip-slip attempts or size limit breach.
    """
    dest_resolved = dest_dir.resolve()
    extracted: list[str] = []
    total_bytes = 0

    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.infolist():
            # Reject absolute paths and dot-dot components
            raw = Path(member.filename)
            if raw.is_absolute() or ".." in raw.parts:
                continue

            target = (dest_dir / raw).resolve()

            # Zip-slip guard: target must stay inside dest_dir
            try:
                target.relative_to(dest_resolved)
            except ValueError:
                continue

            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue

            total_bytes += member.file_size
            if total_bytes > _MAX_EXTRACT_BYTES:
                raise ValueError(
                    f"Zip contents exceed {_MAX_EXTRACT_BYTES // 1024 // 1024} MB limit"
                )

            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, target.open("wb") as dst:
                dst.write(src.read())

            extracted.append("workspace/" + str(target.relative_to(dest_dir)).replace("\\", "/"))

    return extracted


@app.post("/upload", dependencies=[Depends(require_api_key)])
async def upload_file(file: UploadFile = File(...)):
    """
    Accept a file upload and save it to workspace/.
    If the file is a .zip it is automatically extracted (with zip-slip protection).
    Regular files: returns {filename, size, path, zip: false}
    Zip files:     returns {filename, size, files: [...], zip: true}
    """
    filename = Path(file.filename or "upload").name
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    dest = WORKSPACE / filename
    size = 0
    try:
        with dest.open("wb") as fh:
            while chunk := await file.read(65_536):
                size += len(chunk)
                if size > _MAX_UPLOAD_BYTES:
                    dest.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File too large (max {_MAX_UPLOAD_BYTES // 1024 // 1024} MB)",
                    )
                fh.write(chunk)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))

    # Auto-extract zips
    is_zip = filename.lower().endswith(".zip") or (
        file.content_type in ("application/zip", "application/x-zip-compressed")
    )
    if is_zip:
        if not zipfile.is_zipfile(dest):
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="File is not a valid zip archive")
        try:
            extracted = _safe_extract_zip(dest, WORKSPACE)
        except ValueError as exc:
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=413, detail=safe_error(exc))
        except Exception as exc:
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"Extraction failed: {exc}")
        finally:
            dest.unlink(missing_ok=True)  # remove the zip itself after extraction

        return {"filename": filename, "size": size, "files": extracted, "zip": True}

    return {"filename": filename, "size": size, "path": f"workspace/{filename}", "zip": False}


@app.get("/files", dependencies=[Depends(require_api_key)])
async def list_workspace_files():
    """List all files in workspace/ (recursive) available for analysis."""
    if not WORKSPACE.exists():
        return []
    result = []
    for p in sorted(WORKSPACE.rglob("*")):
        if p.is_file():
            rel = "workspace/" + str(p.relative_to(WORKSPACE)).replace("\\", "/")
            result.append({"name": p.name, "size": p.stat().st_size, "path": rel})
    return result


# ---------------------------------------------------------------------------
# Routes — snapshot (for polling fallback)
# ---------------------------------------------------------------------------
@app.get("/snapshot", dependencies=[Depends(require_api_key)])
async def get_snapshot():
    """Return the current UIAgent dashboard snapshot."""
    return ui_agent.snapshot()

# ---------------------------------------------------------------------------
# Notion tree — no bash needed, call via WebFetch when server is running
# ---------------------------------------------------------------------------
@app.get("/notion/tree", dependencies=[Depends(require_api_key)])
async def notion_tree():
    """Return the full Notion workspace tree as structured JSON + plain text."""
    try:
        import sys
        sys.path.insert(0, str(ROOT))
        from skills.builtin.notion_util import NotionClient
        nc = NotionClient()
        tree = nc.full_tree()
        lines = []
        def _walk(nodes, depth=0):
            for n in nodes:
                indent = "  " * depth
                ntype = n.get("type", "PAGE")
                title = n.get("title", "(untitled)")
                nid   = n.get("id", "")[:8]
                lines.append(f"{indent}[{ntype}] {title}  ({nid})")
                if n.get("children"):
                    _walk(n["children"], depth + 1)
        _walk(tree)
        return {
            "total": sum(1 for _ in lines),
            "tree": tree,
            "text": "\n".join(lines),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=safe_error(e))
