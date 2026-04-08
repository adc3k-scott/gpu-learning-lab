# Mission Control — Workstation Recovery Guide

**If this machine dies, this file is on GitHub. Read it from any browser.**
**GitHub: github.com/Scottay007 → gpu-learning-lab**

---

## The Two Keys

Store these in a password manager (1Password, Bitwarden, or Apple Keychain). Do not store in a text file.

```
ANTHROPIC_API_KEY   = sk-ant-...   (console.anthropic.com → API Keys)
NOTION_API_KEY      = secret_...   (notion.so → Settings → Connections → Develop your own integrations)
```

These two keys are all Mission Control needs to be fully operational on any machine.

---

## What Survives a Crash (Already Protected)

| Asset | Location | Status |
|-------|----------|--------|
| All code + skill files | GitHub: Scottay007/gpu-learning-lab | Safe |
| Mission Control memory (MEMORY.md + project files) | GitHub: gpu-learning-lab/memory/ | Safe (as of 2026-03-09) |
| All Notion knowledge (every page, every folder) | Notion cloud — never on local disk | Safe |
| STATE.md, CLAUDE.md | GitHub | Safe |
| Investor deck HTML/PDF | OneDrive sync (project is in OneDrive folder) | Safe |
| Mission Control HD code | GitHub: Scottay007/mission-control | Safe |

---

## New Machine Setup — 30 Minutes to Fully Operational

### Step 1 — Install Prerequisites
```
1. Install Python 3.10+ (python.org)
2. Install Git (git-scm.com)
3. Install Claude Code CLI: npm install -g @anthropic-ai/claude-code
   (requires Node.js — nodejs.org)
4. Sign into Claude Code with your Anthropic account
```

### Step 2 — Clone the Repo
```bash
# Put it in the same OneDrive path so memory paths stay consistent
cd "C:\Users\adhsc\OneDrive\Documents\GitHub"
git clone https://github.com/Scottay007/gpu-learning-lab
cd gpu-learning-lab
```

### Step 3 — Restore API Keys
```bash
# Create the env file
mkdir .venv
# Create .venv/.env with these contents:
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
NOTION_API_KEY=secret_YOUR_KEY_HERE
ANTHROPIC_MODEL=claude-sonnet-4-6
```

### Step 4 — Install Dependencies
```bash
pip install -e ".[dev]"
```

### Step 5 — Restore Claude Code Memory
```bash
# Copy memory files from the repo into Claude Code's auto-memory location
# (Claude Code creates this directory automatically on first run)
mkdir -p "C:\Users\adhsc\.claude\projects\c--Users-adhsc-OneDrive-Documents-GitHub-gpu-learning-lab\memory\projects"

copy memory\MEMORY.md "C:\Users\adhsc\.claude\projects\c--Users-adhsc-OneDrive-Documents-GitHub-gpu-learning-lab\memory\MEMORY.md"
copy memory\projects\*.md "C:\Users\adhsc\.claude\projects\c--Users-adhsc-OneDrive-Documents-GitHub-gpu-learning-lab\memory\projects\"
```

### Step 6 — Verify
```bash
# Open Claude Code in the project
claude

# Test Notion connection
python -c "from skills.builtin.notion_util import print_tree; print_tree(encode='utf-8')"

# Run tests
pytest tests/ -v
```

### Step 7 — Start Mission Control Dashboard
```bash
uvicorn main:app --port 8000
# Open http://localhost:8000
```

---

## If Username Changes on New Machine

The Claude Code memory path includes the Windows username (`adhsc`). If the new machine uses a different username, the memory restore path in Step 5 changes. Update `adhsc` to whatever the new username is.

**To avoid this entirely: use the same Windows username `adhsc` on the new machine.**

---

## Keep Memory Backup Current

After every major session, run this to keep the git backup in sync with the live memory:

```bash
cd "c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab"
cp "C:/Users/adhsc/.claude/projects/c--Users-adhsc-OneDrive-Documents-GitHub-gpu-learning-lab/memory/MEMORY.md" memory/MEMORY.md
cp "C:/Users/adhsc/.claude/projects/c--Users-adhsc-OneDrive-Documents-GitHub-gpu-learning-lab/memory/projects/"*.md memory/projects/
git add memory/ && git commit -m "backup: sync memory files to git"
```

Or just do it as part of the standard session close-out.

---

## Key Accounts (for reference — passwords in password manager)

| Service | Account | URL |
|---------|----------|-----|
| GitHub | Scottay007 | github.com |
| Anthropic | adhscott@yahoo.com | console.anthropic.com |
| Notion | (Notion account) | notion.so |
| Vercel | via GitHub | vercel.com |
| Supabase | adhscott@yahoo.com | supabase.com |
| Stripe | adhscott@yahoo.com | dashboard.stripe.com |
| Namecheap | Scottay007 | namecheap.com |

---

## Notion — Always Available Regardless of Local Machine

Everything built in Notion (MARLIE 1, ADC 3K, KLFT, Ground Zero, Site Acquisition Pipeline, Vendor Strategy, etc.) lives in the cloud. Even if Mission Control is offline, all project knowledge is accessible directly at notion.so from any browser or phone.

Mission Control HQ root: `31288f09-7e31-81a5-bf43-e2af16379346`

---

*Last updated: 2026-03-09*
*Recovery time estimate: 30 minutes on a clean machine with all credentials in hand*
