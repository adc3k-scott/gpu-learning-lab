"""
Planner -- converts a natural-language task description into a Job with Steps.

Strategy:
  1. Try to match the request against known patterns (fast, no LLM call)
  2. Fall back to asking Claude to decompose the task into an executable step plan
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from agents.orchestrator.job import Job, Step

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Input sanitisation — defence against prompt injection
# ---------------------------------------------------------------------------

_MAX_DESCRIPTION_LEN = 2000  # hard cap on user input length

# Patterns that attempt to override the system prompt
_INJECTION_PATTERNS = [
    re.compile(r"\[?\s*SYSTEM\s*[:\]]\s*", re.I),           # [SYSTEM: ...] or SYSTEM: ...
    re.compile(r"<\s*system\s*>", re.I),                     # <system> tags
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?)", re.I),
    re.compile(r"you\s+are\s+now\s+", re.I),                 # "you are now DAN"
    re.compile(r"forget\s+(all\s+)?(previous|prior|your)\s+(instructions?|rules?)", re.I),
    re.compile(r"new\s+instructions?\s*:", re.I),
    re.compile(r"override\s+(system|prompt|instructions?)", re.I),
    re.compile(r"act\s+as\s+(if\s+)?(you\s+)?(are|were)\s+", re.I),
]


def sanitize_input(description: str) -> str:
    """
    Sanitise user task description before it reaches the LLM or regex planner.

    - Truncates to _MAX_DESCRIPTION_LEN characters
    - Strips known prompt-injection patterns
    - Removes control characters (except newline/tab)
    """
    # Length cap
    if len(description) > _MAX_DESCRIPTION_LEN:
        description = description[:_MAX_DESCRIPTION_LEN]
        logger.warning("Task description truncated to %d chars", _MAX_DESCRIPTION_LEN)

    # Strip control characters (keep \n \t)
    description = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", description)

    # Neutralise injection attempts by replacing with [FILTERED]
    for pat in _INJECTION_PATTERNS:
        if pat.search(description):
            description = pat.sub("[FILTERED] ", description)
            logger.warning("Prompt injection pattern detected and filtered")

    return description.strip()


_ALLOWED_ROLES = frozenset({
    "orchestrator", "repo_analyst", "coder", "infra_manager",
    "integration", "ui",
})

_ALLOWED_SKILLS = frozenset({
    "", "file_manager", "http_client", "runpod", "runpod_exec",
    "notion", "marlie_notion", "browser",
})


def _validate_step_dicts(step_dicts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Validate and sanitise LLM-generated step dicts.

    - Reject unknown roles/skills
    - Cap param string values at 5000 chars
    - Remove any step with suspicious params
    """
    validated = []
    for sd in step_dicts:
        role = sd.get("assigned_role", "")
        skill = sd.get("skill", "")

        if role not in _ALLOWED_ROLES:
            logger.warning("LLM produced unknown role %r — dropping step %r", role, sd.get("name"))
            continue

        if skill not in _ALLOWED_SKILLS:
            logger.warning("LLM produced unknown skill %r — dropping step %r", skill, sd.get("name"))
            continue

        # Cap param string lengths
        params = sd.get("params") or {}
        clean_params = {}
        for k, v in params.items():
            if isinstance(v, str) and len(v) > 5000:
                v = v[:5000]
            clean_params[k] = v
        sd["params"] = clean_params

        validated.append(sd)

    return validated


# ---------------------------------------------------------------------------
# Regex pattern rules (no LLM cost)
# ---------------------------------------------------------------------------

_PATH_RE = re.compile(
    r"(?:file|path|open|read|show|write|delete)\s+([\w./\\-]+\.\w+)", re.I
)
_URL_RE = re.compile(r"https?://\S+", re.I)


def _extract_path(description: str) -> str:
    m = _PATH_RE.search(description)
    return m.group(1) if m else ""


def _extract_url(description: str) -> str:
    m = _URL_RE.search(description)
    return m.group(0) if m else ""


_POD_ID_RE = re.compile(r"\bpod[_\s-]?id[:\s=]+([a-z0-9_-]+)\b|pod\s+([a-z0-9]{8,})\b", re.I)
_WORKSPACE_FILE_RE = re.compile(r"workspace[\\/]([\w.\-]+)", re.I)


def _extract_workspace_file(description: str) -> str:
    """Return 'workspace/<name>' if a workspace path is mentioned, else ''."""
    m = _WORKSPACE_FILE_RE.search(description)
    return f"workspace/{m.group(1)}" if m else ""

_NOTION_ID_RE = re.compile(
    r"(?:page|database|block)[_\s-]?id[:\s=]+([a-f0-9-]{32,36})"  # explicit id= form
    r"|([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",  # bare UUID
    re.I,
)
_NOTION_QUERY_RE = re.compile(r'"([^"]{2,})"', re.I)  # quoted search term


def _extract_pod_id(description: str) -> str:
    m = _POD_ID_RE.search(description)
    if m:
        return m.group(1) or m.group(2) or ""
    return ""


def _extract_notion_id(description: str) -> str:
    """Return a properly-hyphenated Notion UUID, or '' if none found."""
    m = _NOTION_ID_RE.search(description)
    if not m:
        return ""
    raw = (m.group(1) or m.group(2) or "").replace("-", "")
    if len(raw) == 32:
        # Re-insert hyphens: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
    return raw


def _extract_notion_query(description: str) -> str:
    m = _NOTION_QUERY_RE.search(description)
    return m.group(1) if m else description


_PATTERNS: list[dict[str, Any]] = [
    {
        "match": re.compile(r"\bread\b.+file|open.+file|show.+file", re.I),
        "steps": lambda desc: [
            {"name": "read_file", "skill": "file_manager", "assigned_role": "coder",
             "description": "Read the requested file",
             "params": {"action": "read", "path": _extract_path(desc)}},
        ],
    },
    {
        "match": re.compile(r"\blist\b.+files?|what files?|directory", re.I),
        "steps": lambda desc: [
            {"name": "list_files", "skill": "file_manager", "assigned_role": "repo_analyst",
             "description": "List files in the project",
             "params": {"action": "list", "path": _extract_path(desc) or "."}},
        ],
    },
    {
        "match": re.compile(r"\bexplain\b|\bsummarise?\b|\bwhat (is|does|are)\b|\boverview\b|\bdescribe\b", re.I),
        "steps": lambda desc: [
            {"name": "analyse_repo", "skill": "", "assigned_role": "repo_analyst",
             "description": desc,
             "params": {"path": _extract_path(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bping\b|\bcheck.*url\b|url.*reachable|is.*up\b|health.?check", re.I),
        "steps": lambda desc: [
            {"name": "ping_url", "skill": "http_client", "assigned_role": "integration",
             "description": "Ping URL and return reachability + latency",
             "params": {"action": "ping", "url": _extract_url(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bhttp\s+(get|post|put|delete|patch)\b|fetch\s+https?://|curl\s+https?://", re.I),
        "steps": lambda desc: [
            {"name": "http_request", "skill": "http_client", "assigned_role": "integration",
             "description": "Make an HTTP request",
             "params": {"action": "http", "method": "GET", "url": _extract_url(desc)}},
        ],
    },
    {
        "match": re.compile(r"\blist.*pods?\b|runpod.*pods?\b|my pods?\b", re.I),
        "steps": lambda desc: [
            {"name": "list_pods", "skill": "runpod", "assigned_role": "integration",
             "description": "List all RunPod pods",
             "params": {"action": "list_pods"}},
        ],
    },
    {
        "match": re.compile(r"\bpod.*(status|info|detail)\b|(status|info|detail).*pod\b", re.I),
        "steps": lambda desc: [
            {"name": "pod_status", "skill": "runpod", "assigned_role": "integration",
             "description": "Get RunPod pod status",
             "params": {"action": "pod_status", "pod_id": _extract_pod_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bstart.*pod\b|resume.*pod\b", re.I),
        "steps": lambda desc: [
            {"name": "start_pod", "skill": "runpod", "assigned_role": "integration",
             "description": "Start a RunPod pod",
             "params": {"action": "start_pod", "pod_id": _extract_pod_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bstop.*pod\b|pause.*pod\b", re.I),
        "steps": lambda desc: [
            {"name": "stop_pod", "skill": "runpod", "assigned_role": "integration",
             "description": "Stop a RunPod pod",
             "params": {"action": "stop_pod", "pod_id": _extract_pod_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bterminate.*pod\b|destroy.*pod\b|delete.*pod\b", re.I),
        "steps": lambda desc: [
            {"name": "terminate_pod", "skill": "runpod", "assigned_role": "integration",
             "description": "Terminate (permanently delete) a RunPod pod",
             "params": {"action": "terminate_pod", "pod_id": _extract_pod_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bwrite\b.+file|create\b.+file|save\b.+file", re.I),
        "steps": lambda desc: [
            {"name": "write_file", "skill": "file_manager", "assigned_role": "coder",
             "description": "Write content to a file",
             "params": {"action": "write", "path": _extract_path(desc), "content": ""}},
        ],
    },
    {
        "match": re.compile(r"\bgenerate\b.+(code|script|function|class|module)|write\b.+(script|function|class)\b", re.I),
        "steps": lambda desc: [
            {"name": "generate_code", "skill": "", "assigned_role": "coder",
             "description": desc,
             "params": {"action": "generate", "path": _extract_path(desc), "prompt": desc}},
        ],
    },
    {
        "match": re.compile(r"\bsend.*webhook\b|post.*webhook\b|webhook.*url\b|notify.*https?://", re.I),
        "steps": lambda desc: [
            {"name": "send_webhook", "skill": "", "assigned_role": "integration",
             "description": "Deliver webhook payload",
             "params": {"action": "webhook", "url": _extract_url(desc), "payload": {}}},
        ],
    },
    {
        "match": re.compile(r"\bnotion\b.*(search|find|look\s*up)\b|search\s+notion\b", re.I),
        "steps": lambda desc: [
            {"name": "notion_search", "skill": "notion", "assigned_role": "integration",
             "description": "Search Notion workspace",
             "params": {"action": "search", "query": _extract_notion_query(desc)}},
        ],
    },
    {
        "match": re.compile(r"\b(get|read|fetch|show|open)\b.*(notion\s+page|notion\s+doc)\b", re.I),
        "steps": lambda desc: [
            {"name": "get_notion_page", "skill": "notion", "assigned_role": "integration",
             "description": "Get a Notion page",
             "params": {"action": "get_page", "page_id": _extract_notion_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bcreate\b.*(notion\s+page|page\s+in\s+notion)\b|add.*page.*notion\b", re.I),
        "steps": lambda desc: [
            {"name": "create_notion_page", "skill": "notion", "assigned_role": "integration",
             "description": "Create a new Notion page",
             "params": {"action": "create_page", "parent_id": _extract_notion_id(desc), "title": desc[:80]}},
        ],
    },
    {
        "match": re.compile(r"\bquery\b.*(notion\s+database|notion\s+db)\b|list.*rows.*notion\b", re.I),
        "steps": lambda desc: [
            {"name": "query_notion_db", "skill": "notion", "assigned_role": "integration",
             "description": "Query a Notion database",
             "params": {"action": "query_database", "database_id": _extract_notion_id(desc)}},
        ],
    },
    {
        "match": re.compile(r"\bappend\b.*(notion|block)\b|add.*block.*notion\b|write.*to.*notion\b", re.I),
        "steps": lambda desc: [
            {"name": "append_notion_blocks", "skill": "notion", "assigned_role": "integration",
             "description": "Append content blocks to a Notion page",
             "params": {"action": "append_blocks", "page_id": _extract_notion_id(desc),
                        "blocks": [_extract_notion_query(desc)]}},
        ],
    },
    {
        "match": re.compile(r"\blist\b.+workspace\b|list.*uploads?\b|workspace\s+files?\b|what.*uploaded\b", re.I),
        "steps": lambda desc: [
            {"name": "list_workspace", "skill": "file_manager", "assigned_role": "repo_analyst",
             "description": "List uploaded files in workspace",
             "params": {"action": "list", "path": "workspace"}},
        ],
    },
    {
        "match": re.compile(
            r"\banalyse?\b.+file|\binspect\b.+file"
            r"|\banalyse?\b.+(data|csv|json|iot|sensor|log)\b"
            r"|\binspect\b.+(data|csv|json|iot|sensor)\b",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "read_data_file", "skill": "file_manager", "assigned_role": "coder",
             "description": "Read the data file",
             "params": {"action": "read", "path": _extract_path(desc) or _extract_workspace_file(desc) or "workspace"}},
            {"name": "analyse_data", "skill": "", "assigned_role": "coder",
             "description": desc,
             "params": {"action": "analyse", "prompt": desc, "content": "{{read_data_file}}"},
             "depends_on": ["read_data_file"]},
        ],
    },
    {
        "match": re.compile(r"\bparse\b.+(csv|json|tsv|log|ndjson)\b|\bload\b.+(csv|json|dataset)\b", re.I),
        "steps": lambda desc: [
            {"name": "read_file", "skill": "file_manager", "assigned_role": "coder",
             "description": "Read the data file",
             "params": {"action": "read", "path": _extract_path(desc) or _extract_workspace_file(desc)}},
            {"name": "parse_data", "skill": "", "assigned_role": "coder",
             "description": desc,
             "params": {"action": "analyse", "prompt": desc, "content": "{{read_file}}"},
             "depends_on": ["read_file"]},
        ],
    },
    {
        "match": re.compile(
            r"\bcompute\b.+stats?\b|\bcalculate\b.+stats?\b|\bstatistics\b"
            r"|\bsummary\b.+data\b|\bdata\b.+summary\b|\bsummarise?\b.+data\b",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "read_file", "skill": "file_manager", "assigned_role": "coder",
             "description": "Read the target data file",
             "params": {"action": "read", "path": _extract_path(desc) or _extract_workspace_file(desc)}},
            {"name": "compute_stats", "skill": "", "assigned_role": "coder",
             "description": desc,
             "params": {"action": "analyse", "prompt": desc, "content": "{{read_file}}"},
             "depends_on": ["read_file"]},
        ],
    },
    {
        "match": re.compile(r"\binfra\b|system (health|status)|gpu status|check.*resources?", re.I),
        "steps": lambda desc: [
            {"name": "infra_health", "skill": "", "assigned_role": "infra_manager",
             "description": "Get infrastructure health report",
             "params": {"action": "health"}},
        ],
    },
    # ── MARLIE I Notion sync ────────────────────────────────────────────
    {
        "match": re.compile(
            r"\bmarlie\b.*(sync|push|notion|update|export)\b"
            r"|\b(sync|push|export)\b.*marlie\b"
            r"|sync.*notion.*workbook|push.*notion.*workbook"
            r"|rebuild.*marlie.*notion|marlie.*full.*sync",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "marlie_sync_full", "skill": "marlie_notion", "assigned_role": "integration",
             "description": "Sync full MARLIE I workbook to Notion",
             "params": {"action": "sync_full"}},
        ],
    },
    {
        "match": re.compile(
            r"\bmarlie\b.*(status|where|notion.*page|find.*notion)\b"
            r"|notion.*marlie.*status|find.*marlie.*notion",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "marlie_status", "skill": "marlie_notion", "assigned_role": "integration",
             "description": "Get MARLIE I Notion workbook status and URLs",
             "params": {"action": "get_status"}},
        ],
    },
    {
        "match": re.compile(
            r"\bmarlie\b.*(note|update|log|add)\b.*(notion)?"
            r"|\bappend.*marlie\b|add.*note.*marlie\b",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "marlie_append_note", "skill": "marlie_notion", "assigned_role": "integration",
             "description": "Append a note to the MARLIE I Notion page",
             "params": {"action": "append_note", "text": desc}},
        ],
    },
    {
        "match": re.compile(
            r"\bsync\b.*(thesis|hardware|site|funding|partners?|credentials?|vision|contact)\b.*\b(marlie|notion)\b"
            r"|\bmarlie\b.*(thesis|hardware|site|funding|partners?|credentials?|vision|contact).*\b(sync|push|update)\b"
            r"|\bpush\b.*(thesis|hardware|site|funding|partners?|credentials?|vision|contact)\b.*notion",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "marlie_sync_section", "skill": "marlie_notion", "assigned_role": "integration",
             "description": f"Sync MARLIE I section to Notion: {desc}",
             "params": {"action": "sync_section",
                        "section": next(
                            (s for s in ["thesis", "hardware", "site", "funding",
                                         "partners", "credentials", "vision", "contact"]
                             if re.search(s.rstrip("s"), desc, re.I)), "thesis"
                        )}},
        ],
    },
    # ── Pipeline site scout ────────────────────────────────────────────
    {
        "match": re.compile(
            r"\b(scout|scan|search).*(pipeline|sites?|corridor)\b"
            r"|\bpipeline.*(scout|scan|find|search)\b"
            r"|\bsite.?intel\b|find.*sites.*near.*pipeline"
            r"|\bsabine|henry hub|teche|southern natural|tennessee gas\b",
            re.I,
        ),
        "steps": lambda desc: [
            {"name": "run_pipeline_scout", "skill": "", "assigned_role": "coder",
             "description": "Run pipeline site scout agent to find and score land listings",
             "params": {"action": "generate", "prompt": desc,
                        "path": "scripts/pipeline_scout.py"}},
        ],
    },
    # ------------------------------------------------------------------
    # RunPod GPU execution
    # ------------------------------------------------------------------
    {
        "match": re.compile(
            r"\b(run|execute|exec)\b.*(on|at|in)\s+(pod|runpod|gpu)\b"
            r"|\bssh.*pod\b|\bpod.*command\b", re.I
        ),
        "steps": lambda desc: [
            {"name": "exec_on_pod", "skill": "runpod_exec", "assigned_role": "integration",
             "description": "Execute command on RunPod GPU pod",
             "params": {"action": "execute", "pod_id": _extract_pod_id(desc), "command": ""}},
        ],
    },
    {
        "match": re.compile(
            r"\b(deploy|upload|push)\b.*(to|on)\s+(pod|runpod|gpu)\b"
            r"|\bscp.*pod\b|\brsync.*pod\b", re.I
        ),
        "steps": lambda desc: [
            {"name": "deploy_to_pod", "skill": "runpod_exec", "assigned_role": "integration",
             "description": "Deploy files to RunPod GPU pod",
             "params": {"action": "deploy", "pod_id": _extract_pod_id(desc),
                        "local_path": _extract_path(desc), "remote_path": "/workspace/"}},
        ],
    },
    {
        "match": re.compile(
            r"\b(pull|download|fetch)\b.*(from)\s+(pod|runpod|gpu)\b"
            r"|\bpod.*download\b|\bget.*results?.*pod\b", re.I
        ),
        "steps": lambda desc: [
            {"name": "pull_from_pod", "skill": "runpod_exec", "assigned_role": "integration",
             "description": "Pull files from RunPod GPU pod",
             "params": {"action": "pull", "pod_id": _extract_pod_id(desc),
                        "remote_path": "", "local_path": "workspace/"}},
        ],
    },
    {
        "match": re.compile(
            r"\b(run|launch)\b.*(script|training|train|benchmark)\b.*(on|at)\s+(pod|runpod|gpu)\b"
            r"|\bgpu.*train\b|\btrain.*gpu\b", re.I
        ),
        "steps": lambda desc: [
            {"name": "start_gpu_pod", "skill": "runpod", "assigned_role": "integration",
             "description": "Ensure GPU pod is running",
             "params": {"action": "start_pod", "pod_id": _extract_pod_id(desc)}},
            {"name": "run_on_gpu", "skill": "runpod_exec", "assigned_role": "integration",
             "description": "Deploy and run script on GPU pod",
             "params": {"action": "run_script", "pod_id": _extract_pod_id(desc),
                        "local_path": _extract_path(desc)},
             "depends_on": ["start_gpu_pod"]},
        ],
    },
    # ------------------------------------------------------------------
    # Browser automation
    # ------------------------------------------------------------------
    {
        "match": re.compile(
            r"\b(navigate|open browser|go to url|browse to|screenshot page|"
            r"click button|fill form|browser automation|playwright)\b", re.I
        ),
        "steps": lambda desc: [
            {
                "name": "browser_session",
                "skill": "browser",
                "assigned_role": "integration",
                "description": desc,
                "params": {"action": "navigate", "url": ""},
            }
        ],
    },
]


def _pattern_plan(description: str) -> list[dict[str, Any]] | None:
    for rule in _PATTERNS:
        if rule["match"].search(description):
            return rule["steps"](description)
    return None


# ---------------------------------------------------------------------------
# LLM system prompt -- tells Claude exactly what roles/skills/params exist
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are the Planner for Mission Control, an AI-powered GPU computing platform.\n"
    "Given a task description, decompose it into a minimal, executable list of steps.\n"
    "\n"
    "AVAILABLE AGENT ROLES:\n"
    "  coder         -- reads, writes, patches, reviews code files\n"
    "  repo_analyst  -- explains code, answers questions, lists files\n"
    "  infra_manager -- GPU/CPU/RAM/disk status, Docker, Redis\n"
    "  integration   -- HTTP requests, RunPod API, webhooks, pings\n"
    "  orchestrator  -- coordination only, no direct skill\n"
    "\n"
    "AVAILABLE SKILLS AND PARAMS:\n"
    "  file_manager (roles: coder, repo_analyst)\n"
    "    action=read,   path=<relative path>   -- reads text/CSV/JSON/log files\n"
    "    action=write,  path=<relative path>, content=<string>\n"
    "    action=list,   path=<relative path, default '.'>\n"
    "    action=exists, path=<relative path>\n"
    "    action=delete, path=<relative path>\n"
    "    NOTE: uploaded IoT/sensor files land in workspace/ (e.g. workspace/data.csv)\n"
    "\n"
    "  http_client (role: integration) -- outbound HTTP:\n"
    "    action=ping,  url=<url>                           (reachability check)\n"
    "    action=get,   url=<url>, headers={}, params={}    (HTTP GET)\n"
    "    action=post,  url=<url>, headers={}, body={}      (HTTP POST JSON)\n"
    "    action=http,  method=GET|POST|PUT|DELETE, url=<url>, headers={}, body={}\n"
    "\n"
    "  runpod (role: integration) -- RunPod GPU cloud:\n"
    "    action=list_pods\n"
    "    action=pod_status,    pod_id=<id>\n"
    "    action=start_pod,     pod_id=<id>\n"
    "    action=stop_pod,      pod_id=<id>\n"
    "    action=terminate_pod, pod_id=<id>   (permanent — use with caution)\n"
    "\n"
    "  runpod_exec (role: integration) -- Execute on RunPod GPU pods via SSH:\n"
    "    action=execute,    pod_id=<id>, command=<shell command>, timeout=300\n"
    "    action=deploy,     pod_id=<id>, local_path=<path>, remote_path='/workspace/'\n"
    "    action=pull,       pod_id=<id>, remote_path=<path>, local_path='workspace/'\n"
    "    action=run_script, pod_id=<id>, local_path=<script>, args='', timeout=300\n"
    "    NOTE: pod must be RUNNING first (use runpod skill to start)\n"
    "\n"
    "  notion (role: integration) -- Notion workspace:\n"
    "    action=search,           query=<str>\n"
    "    action=get_page,         page_id=<uuid>\n"
    "    action=get_page_blocks,  page_id=<uuid>\n"
    "    action=create_page,      parent_id=<uuid>, parent_type='database_id'|'page_id',\n"
    "                             title=<str>, properties={}, blocks=[]\n"
    "    action=update_page,      page_id=<uuid>, properties={}\n"
    "    action=append_blocks,    page_id=<uuid>, blocks=[<block_obj_or_plain_str>]\n"
    "    action=query_database,   database_id=<uuid>, filter={}, sorts=[], page_size=50\n"
    "\n"
    "  marlie_notion (role: integration) -- MARLIE I Lafayette AI Factory Notion workbook:\n"
    "    action=sync_full                              -- rebuild entire 8-section workbook\n"
    "    action=sync_section, section=<name>          -- push one section (thesis|hardware|site|funding|partners|credentials|vision|contact)\n"
    "    action=get_status                            -- find MARLIE I pages in Notion, return URLs\n"
    "    action=append_note, text=<str>              -- append timestamped note to root MARLIE I page\n"
    "\n"
    "  site_scout -- pipeline site intelligence (scripts/pipeline_scout.py):\n"
    "    Run as coder role with action=generate, prompt=<user request>, path=scripts/pipeline_scout.py\n"
    "    Corridors: 'Henry Hub' | 'Tennessee Gas' | 'Southern Natural' | 'Teche' | 'Sabine'\n"
    "    Output: data/pipeline_sites.json (16 sites already), data/pipeline_sites_import.js\n"
    "    FEMA endpoint: hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query\n"
    "    Scoring: pipeline(25%) + flood(20%) + size(15%) + power(15%) + zoning(15%) + road(10%)\n"
    "\n"
    "  integration role -- webhook (skill=''):\n"
    "    action=webhook, url=<url>, payload=<dict>, secret=<str optional>\n"
    "\n"
    "  coder role -- LLM-assisted coding and data analysis (skill=''):\n"
    "    action=generate, path=<output file>, prompt=<what to generate>\n"
    "    action=review,   path=<file to review>, prompt=<review instructions>\n"
    "    action=patch,    path=<file>, diff=<unified diff string>\n"
    "    action=analyse,  prompt=<question>, content=<data or {{prior_step}}>\n"
    "      -- use for: CSV parsing, IoT data stats, anomaly detection, summarising logs\n"
    "\n"
    "  infra_manager role (skill='', use params):\n"
    "    action=health | gpu | system | docker | redis | process\n"
    "\n"
    "  repo_analyst or coder -- free-form LLM analysis (skill=''):\n"
    "    Put the question in description; params may include path=<file>\n"
    "\n"
    "OUTPUT FORMAT -- respond with ONLY a valid JSON array, no markdown:\n"
    "[\n"
    "  {\n"
    "    \"name\": \"short_snake_case_name\",\n"
    "    \"description\": \"what this step does\",\n"
    "    \"assigned_role\": \"<role>\",\n"
    "    \"skill\": \"<skill name or empty string>\",\n"
    "    \"params\": {},\n"
    "    \"depends_on\": [\"other_step_name\"]\n"
    "  }\n"
    "]\n"
    "\n"
    "Rules:\n"
    "- 1-3 steps unless genuinely multi-stage\n"
    "- depends_on uses step NAMES from this same plan\n"
    "- Never invent roles or skills not listed above\n"
    "- To pass a prior step's result into a later step's param, use {{step_name}} as the value\n"
    "  e.g. {\"content\": \"{{read_file}}\"} passes the read_file step result as the content param\n"
)


async def _llm_plan_async(description: str, client: Any, model: str) -> list[dict[str, Any]]:
    """Call Claude in a thread executor -- never blocks the event loop."""
    safe_desc = sanitize_input(description)

    def _call() -> list[dict[str, Any]]:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": safe_desc}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw).rstrip("`").strip()
        return _validate_step_dicts(json.loads(raw))

    return await asyncio.get_event_loop().run_in_executor(None, _call)


# ---------------------------------------------------------------------------
# Public factory -- async
# ---------------------------------------------------------------------------

_REPLAN_SYSTEM_PROMPT = (
    "You are the Replanner for Mission Control.\n"
    "A task was partially executed but a step failed. You must decide:\n"
    "  1. Can the remaining work be achieved by a different approach?\n"
    "  2. If yes, output a revised JSON step array (same format as the Planner).\n"
    "  3. If no, output the JSON: [{\"abort\": true, \"reason\": \"...\"}]\n"
    "\n"
    "You will receive:\n"
    "  - The original task description\n"
    "  - Steps already completed (with their results)\n"
    "  - The failed step (with its error)\n"
    "  - Any remaining PENDING steps\n"
    "\n"
    "RULES:\n"
    "- Do NOT repeat completed steps.\n"
    "- You may modify, replace, or remove remaining steps.\n"
    "- You may add new steps if needed.\n"
    "- Use the same roles, skills, and params as the Planner.\n"
    "- Output ONLY valid JSON, no markdown.\n"
    "\n" + _SYSTEM_PROMPT.split("AVAILABLE AGENT ROLES:")[1]
)


async def replan(
    original_description: str,
    completed_steps: list[dict[str, Any]],
    failed_step: dict[str, Any],
    pending_steps: list[dict[str, Any]],
    llm_client: Any = None,
    llm_model: str = "claude-opus-4-5",
) -> list[dict[str, Any]] | None:
    """
    Given a partial execution with a failure, ask Claude for a revised plan.

    Returns:
        - A list of new step dicts to replace remaining work, OR
        - None if the LLM says to abort or replanning fails.
    """
    if llm_client is None:
        logger.warning("No LLM client for replanning — cannot replan")
        return None

    context = (
        f"ORIGINAL TASK: {original_description}\n\n"
        f"COMPLETED STEPS:\n{json.dumps(completed_steps, indent=2)}\n\n"
        f"FAILED STEP:\n{json.dumps(failed_step, indent=2)}\n\n"
        f"REMAINING PENDING STEPS:\n{json.dumps(pending_steps, indent=2)}\n"
    )

    def _call() -> list[dict[str, Any]]:
        response = llm_client.messages.create(
            model=llm_model,
            max_tokens=1024,
            system=_REPLAN_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": context}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw).rstrip("`").strip()
        return json.loads(raw)

    try:
        step_dicts = await asyncio.get_event_loop().run_in_executor(None, _call)
    except Exception as exc:
        logger.warning("Replanning LLM call failed: %s", exc)
        return None

    # Check for abort signal
    if step_dicts and isinstance(step_dicts[0], dict) and step_dicts[0].get("abort"):
        reason = step_dicts[0].get("reason", "unknown")
        logger.info("Replanner decided to abort: %s", reason)
        return None

    step_dicts = _validate_step_dicts(step_dicts)
    logger.info("Replanner produced %d revised step(s)", len(step_dicts))
    return step_dicts


async def plan(
    description: str,
    title: str = "",
    requested_by: str = "user",
    llm_client: Any = None,
    llm_model: str = "claude-opus-4-5",
) -> Job:
    """
    Build a Job from *description*.

    Fast regex patterns tried first (no API cost).
    Falls back to Claude when no pattern matches and a client is provided.
    Last resort: single generic step for repo_analyst to handle.
    """
    # Sanitise input before any processing
    description = sanitize_input(description)

    job = Job(
        title=title or description[:80],
        description=description,
        requested_by=requested_by,
    )

    step_dicts = _pattern_plan(description)

    if step_dicts is None and llm_client is not None:
        try:
            step_dicts = await _llm_plan_async(description, llm_client, llm_model)
            logger.info("LLM planned %d step(s) for: %r", len(step_dicts), description[:60])
        except Exception as exc:
            logger.warning("LLM planning failed (%s) -- falling back to generic step", exc)

    if not step_dicts:
        step_dicts = [
            {
                "name": "execute_task",
                "description": description,
                "assigned_role": "repo_analyst",
                "skill": "",
                "params": {},
                "depends_on": [],
            }
        ]

    # Build Step objects, resolving depends_on by NAME -> step_id
    name_to_id: dict[str, str] = {}
    for sd in step_dicts:
        step = Step(
            name=sd.get("name", "step"),
            description=sd.get("description", ""),
            assigned_role=sd.get("assigned_role", "orchestrator"),
            skill=sd.get("skill", ""),
            params=sd.get("params") or {},
            depends_on=[name_to_id[n] for n in sd.get("depends_on", []) if n in name_to_id],
        )
        name_to_id[step.name] = step.step_id
        job.add_step(step)

    logger.info("Planned job %r with %d step(s)", job.title, len(job.steps))
    return job
