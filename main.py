import asyncio
import json
import os
import re
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

from anthropic import AsyncAnthropic, Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

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
# Multi-agent infrastructure
# ---------------------------------------------------------------------------
from core.config import settings
from core.event_bus import Event, EventBus
from core.state_store import StateStore
from skills.registry import registry
from agents.orchestrator import OrchestratorAgent
from agents.repo_analyst import RepoAnalystAgent
from agents.coder import CoderAgent
from agents.infra_manager import InfraManagerAgent
from agents.integration import IntegrationAgent
from agents.ui import UIAgent
from agents.notion_sync import NotionSyncAgent

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

_ALL_AGENTS = [orchestrator, repo_analyst, coder, infra_manager, integration, ui_agent, notion_sync]

# ---------------------------------------------------------------------------
# Lifespan — start/stop all agents with the server
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bus.connect()
    await store.connect()
    # UIAgent starts first so it is subscribed before other agents emit events
    await ui_agent.start()
    for agent in [orchestrator, repo_analyst, coder, infra_manager, integration, notion_sync]:
        await agent.start()
    yield
    for agent in reversed(_ALL_AGENTS):
        await agent.stop()
    await bus.disconnect()
    await store.disconnect()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="Mission Control", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


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


# ---------------------------------------------------------------------------
# Routes — SSE live dashboard stream
# ---------------------------------------------------------------------------
@app.get("/events")
async def sse_events():
    """Server-Sent Events stream — pushes dashboard snapshots to the browser."""
    q = ui_agent.add_sse_subscriber()

    async def stream():
        # Send current snapshot immediately on connect
        snap = json.dumps(ui_agent.snapshot())
        yield f"data: {snap}\n\n"
        try:
            while True:
                try:
                    data = await asyncio.wait_for(q.get(), timeout=20.0)
                    yield f"data: {data}\n\n"
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
@app.get("/model")
def get_model():
    return {"model": MODEL, "mode": bus.mode}


# ---------------------------------------------------------------------------
# Routes — direct Claude chat
# ---------------------------------------------------------------------------
@app.post("/chat")
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
        raise HTTPException(status_code=502, detail=str(exc))

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


@app.post("/chat/stream")
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
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
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
@app.post("/tasks")
async def submit_task(req: TaskRequest):
    job_id = await orchestrator.submit_task(
        description=req.description,
        title=req.title,
        requested_by=req.requested_by,
    )
    return {"job_id": job_id, "status": "queued"}


@app.get("/tasks/{job_id}")
async def get_task(job_id: str):
    job = await orchestrator.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id!r} not found")
    return job


@app.get("/tasks")
async def list_tasks():
    return await orchestrator.list_jobs()


@app.get("/tasks/{job_id}/stream")
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
@app.get("/agents")
async def list_agents():
    states = []
    for agent in _ALL_AGENTS:
        state = await agent.get_state()
        states.append(state.to_dict())
    return states


# ---------------------------------------------------------------------------
# Routes — infrastructure health
# ---------------------------------------------------------------------------
@app.get("/infra")
async def get_infra():
    cached = await store.get("infra:health")
    if cached:
        return cached
    return await infra_manager._health()


@app.post("/infra/check")
async def trigger_infra_check():
    await bus.publish(Event(event_type="infra.check", payload={}, source="api"))
    return {"status": "check triggered"}


# ---------------------------------------------------------------------------
# Routes — runtime config (Notion work folder, etc.)
# ---------------------------------------------------------------------------

_ALLOWED_CONFIG_KEYS = {
    "notion_work_db_id",
    "notion_api_key",
    "runpod_api_key",
}


class ConfigRequest(BaseModel):
    key: str
    value: str


@app.get("/config")
async def get_config():
    """Return current runtime configuration (sensitive values masked)."""
    notion_key_stored = await store.get("config:notion_api_key") or ""
    runpod_key_stored = await store.get("config:runpod_api_key") or ""
    return {
        "notion_work_db_id":  notion_sync.get_config()["notion_work_db_id"],
        "notion_api_key_set": notion_sync.get_config()["notion_api_key_set"],
        "runpod_api_key_set": "yes" if (runpod_key_stored or os.getenv("RUNPOD_API_KEY")) else "no",
        "model": MODEL,
    }


@app.post("/config")
async def set_config(req: ConfigRequest):
    """Set a runtime config value. Stored in StateStore; persists until server restart."""
    if req.key not in _ALLOWED_CONFIG_KEYS:
        raise HTTPException(status_code=400, detail=f"Unknown config key {req.key!r}")

    store_key = f"config:{req.key}"
    await store.set(store_key, req.value)

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


@app.post("/upload")
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
        raise HTTPException(status_code=500, detail=str(exc))

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
            raise HTTPException(status_code=413, detail=str(exc))
        except Exception as exc:
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"Extraction failed: {exc}")
        finally:
            dest.unlink(missing_ok=True)  # remove the zip itself after extraction

        return {"filename": filename, "size": size, "files": extracted, "zip": True}

    return {"filename": filename, "size": size, "path": f"workspace/{filename}", "zip": False}


@app.get("/files")
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
@app.get("/snapshot")
async def get_snapshot():
    """Return the current UIAgent dashboard snapshot."""
    return ui_agent.snapshot()
