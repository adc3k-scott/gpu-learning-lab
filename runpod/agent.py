import os
import sys
from pathlib import Path

# Force UTF-8 output so Unicode characters in Claude's responses print correctly on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Resolve project root (one level above this file's directory)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to sys.path so `src` is importable
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Load .env — prefer a .env at the project root, fall back to .venv/.env
# ---------------------------------------------------------------------------
root_env = PROJECT_ROOT / ".env"
venv_env = PROJECT_ROOT / ".venv" / ".env"

if root_env.exists():
    load_dotenv(dotenv_path=root_env)
elif venv_env.exists():
    load_dotenv(dotenv_path=venv_env)
else:
    load_dotenv()  # last-resort: search upward from cwd

api_key = os.getenv("ANTHROPIC_API_KEY")
model = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")

if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set. "
        "Add it to a .env file at the project root or at .venv/.env"
    )

# ---------------------------------------------------------------------------
# Build project context and create the Anthropic client
# ---------------------------------------------------------------------------
from src.core.context_builder import build_system_context
from src.core.orchestrator import create_orchestrator

print("Scanning project structure...")
system_context = build_system_context(PROJECT_ROOT)

client = Anthropic(api_key=api_key)
send = create_orchestrator(client, model, system_context)

# ---------------------------------------------------------------------------
# Interactive task loop
# ---------------------------------------------------------------------------
print(f"Cloud agent node is live.  Model: {model}")
print("Type a task and press Enter. Type 'exit' to quit.\n")

while True:
    try:
        task = input("Task> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        break

    if task.lower() in {"exit", "quit"}:
        break
    if not task:
        continue

    try:
        answer = send(task)
        print(f"\nAgent:\n{answer}\n")
    except Exception as exc:
        print(f"\nERROR: {exc}\n")
