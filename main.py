import asyncio
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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

anthropic_client = Anthropic(api_key=API_KEY)

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

_ALL_AGENTS = [orchestrator, repo_analyst, coder, infra_manager, integration, ui_agent]

# ---------------------------------------------------------------------------
# Lifespan — start/stop all agents with the server
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bus.connect()
    await store.connect()
    # UIAgent starts first so it is subscribed before other agents emit events
    await ui_agent.start()
    for agent in [orchestrator, repo_analyst, coder, infra_manager, integration]:
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
# Routes — snapshot (for polling fallback)
# ---------------------------------------------------------------------------
@app.get("/snapshot")
async def get_snapshot():
    """Return the current UIAgent dashboard snapshot."""
    return ui_agent.snapshot()
