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
    def _call() -> list[dict[str, Any]]:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": description}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw).rstrip("`").strip()
        return json.loads(raw)

    return await asyncio.get_event_loop().run_in_executor(None, _call)


# ---------------------------------------------------------------------------
# Public factory -- async
# ---------------------------------------------------------------------------

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
