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


def _extract_pod_id(description: str) -> str:
    m = _POD_ID_RE.search(description)
    if m:
        return m.group(1) or m.group(2) or ""
    return ""


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
        "match": re.compile(r"\bping\b|\bcheck.*url\b|url.*reachable", re.I),
        "steps": lambda desc: [
            {"name": "ping_url", "skill": "", "assigned_role": "integration",
             "description": desc,
             "params": {"action": "ping", "url": _extract_url(desc)}},
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
    "    action=read,   path=<relative path>\n"
    "    action=write,  path=<relative path>, content=<string>\n"
    "    action=list,   path=<relative path, default '.'>\n"
    "    action=exists, path=<relative path>\n"
    "    action=delete, path=<relative path>\n"
    "\n"
    "  integration role -- HTTP/ping (skill=''):\n"
    "    action=ping,  url=<url>\n"
    "    action=http,  method=GET|POST, url=<url>, headers={}, body={}\n"
    "\n"
    "  integration role -- RunPod (skill='runpod'):\n"
    "    action=list_pods\n"
    "    action=pod_status,    pod_id=<id>\n"
    "    action=start_pod,     pod_id=<id>\n"
    "    action=stop_pod,      pod_id=<id>\n"
    "    action=terminate_pod, pod_id=<id>\n"
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
