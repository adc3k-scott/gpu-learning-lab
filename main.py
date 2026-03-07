import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from anthropic import Anthropic

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
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")

if not API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not set in .env")

client = Anthropic(api_key=API_KEY)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="Mission Control")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    messages: list[dict]
    system: str | None = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    index = ROOT / "web" / "index.html"
    if not index.exists():
        raise HTTPException(
            status_code=404,
            detail="web/index.html not found — run write_ui.py first",
        )
    return FileResponse(str(index))


@app.get("/model")
def get_model():
    return {"model": MODEL}


@app.post("/chat")
def chat(req: ChatRequest):
    system = req.system or (
        "You are Mission Control — an AI assistant with expertise in CUDA, GPU computing, "
        "RunPod, and Nvidia accelerated computing. Be concise and technical."
    )
    try:
        response = client.messages.create(
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
