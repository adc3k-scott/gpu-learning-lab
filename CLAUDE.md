# CLAUDE.md

## Project Overview
gpu-learning-lab is a repository for CUDA, GPU Computing, RunPod experiments, and Nvidia accelerated computing tutorials. It includes an AI-powered CLI agent (Mission Control) that has full knowledge of the codebase.

## Repository Structure
```
├── runpod/          # Cloud agent — interactive CLI powered by Claude API
├── src/core/        # Agent internals: context builder, orchestrator, repo scanner
├── tutorials/       # Accelerated Python notebooks (NumPy, CUDA, etc.)
├── notes/           # Learning notes
├── web/             # Frontend for the FastAPI chat UI
└── main.py          # FastAPI web server entry point
```

## Key Commands

### Run the AI agent (interactive CLI)
```bash
.venv\Scripts\python runpod\agent.py
# or double-click run_agent.bat
```

### Run the FastAPI web server
```bash
uvicorn main:app --reload --port 8000
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Setup
`.env` credentials live at `.venv/.env`. To move them to project root:
```
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_MODEL=claude-opus-4-5
```
The agent checks project root first, then falls back to `.venv/.env`.

## Architecture Notes
- **repo_scanner.py** — walks the project tree, skips `.git`, `.venv`, `__pycache__`. Reads text files under 50KB.
- **context_builder.py** — assembles a full system prompt from the scanned structure and file contents. Priority files: README, requirements.txt, main.py.
- **orchestrator.py** — wraps the Anthropic client; maintains conversation history across turns via a stateful `send()` closure.
- **agent.py** — resolves project root from `__file__`, loads `.env`, scans repo, creates orchestrator, runs interactive loop.

## Code Conventions
- Python 3.10+, UTF-8 everywhere
- Notebooks live under `tutorials/<topic>/notebooks/<level>/`
- Add new file types to `TEXT_EXTENSIONS` in `repo_scanner.py` to include them in AI context
- Adjust `MAX_FILE_SIZE` (default 50KB) in `repo_scanner.py` for larger files

## Current Status
| Area | Status |
|------|--------|
| CLI Agent (Mission Control) | Working |
| Repo context injection | Working |
| FastAPI web server | Stub — not connected to Claude yet |
| GPU/CUDA tutorial content | Starting — one NumPy notebook |
| RunPod integration | Not yet implemented |

## User Preferences
- Direct, concise communication — no filler
- No emojis unless asked
- Apply changes immediately rather than proposing them
- Mission Control framing — the AI agent is the command center for the project
