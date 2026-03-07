"""
Built-in skill: runpod

Interact with the RunPod cloud GPU platform via its GraphQL API.

Supported actions:
  list_pods     — list all pods on the account
  pod_status    — get detailed status of one pod (requires pod_id)
  start_pod     — resume a stopped pod (requires pod_id)
  stop_pod      — stop a running pod (requires pod_id)
  terminate_pod — permanently terminate a pod (requires pod_id)

Credentials:
  The skill reads the API key from ctx.metadata["runpod_api_key"] first,
  then falls back to the RUNPOD_API_KEY environment variable.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_RUNPOD_API_BASE = "https://api.runpod.io/graphql"
_TIMEOUT = 15.0


class RunPodSkill(BaseSkill):
    name = "runpod"
    description = "Manage RunPod cloud GPU pods — list, start, stop, terminate, get status"
    version = "0.1.0"
    required_secrets = ["RUNPOD_API_KEY"]

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "")
        if not action:
            return SkillResult.fail("Missing required parameter: action")

        api_key = (
            ctx.metadata.get("runpod_api_key")
            or os.environ.get("RUNPOD_API_KEY", "")
        )
        if not api_key:
            return SkillResult.fail(
                "RunPod API key not configured. "
                "Set RUNPOD_API_KEY in .env or pass runpod_api_key in skill metadata."
            )

        pod_id = params.get("pod_id", "")
        if action in ("pod_status", "start_pod", "stop_pod", "terminate_pod") and not pod_id:
            return SkillResult.fail(f"Action '{action}' requires a 'pod_id' parameter")

        try:
            query, variables = _build_query(action, pod_id)
        except ValueError as exc:
            return SkillResult.fail(str(exc))

        try:
            data = await _graphql(query, variables, api_key)
        except Exception as exc:
            return SkillResult.fail(str(exc))

        return SkillResult.ok(output=data)


# ---------------------------------------------------------------------------
# GraphQL helpers
# ---------------------------------------------------------------------------

def _build_query(action: str, pod_id: str) -> tuple[str, dict]:
    if action == "list_pods":
        return (
            "query { myself { pods { id name desiredStatus runtime { uptimeInSeconds } } } }",
            {},
        )
    if action == "pod_status":
        return (
            "query Pod($id: String!) { pod(input: { podId: $id }) { "
            "id name desiredStatus runtime { uptimeInSeconds gpus { id memoryInGb } } } }",
            {"id": pod_id},
        )
    if action == "start_pod":
        return (
            "mutation StartPod($id: String!) { "
            "podResume(input: { podId: $id, gpuCount: 1 }) { id desiredStatus } }",
            {"id": pod_id},
        )
    if action == "stop_pod":
        return (
            "mutation StopPod($id: String!) { "
            "podStop(input: { podId: $id }) { id desiredStatus } }",
            {"id": pod_id},
        )
    if action == "terminate_pod":
        return (
            "mutation TerminatePod($id: String!) { podTerminate(input: { podId: $id }) }",
            {"id": pod_id},
        )
    valid = "list_pods, pod_status, start_pod, stop_pod, terminate_pod"
    raise ValueError(f"Unknown action {action!r}. Choose: {valid}")


async def _graphql(query: str, variables: dict, api_key: str) -> Any:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(
            _RUNPOD_API_BASE,
            json={"query": query, "variables": variables},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )

    if not resp.is_success:
        raise RuntimeError(f"RunPod API HTTP {resp.status_code}: {resp.text[:400]}")

    body = resp.json()
    if "errors" in body:
        messages = "; ".join(e.get("message", str(e)) for e in body["errors"])
        raise RuntimeError(f"RunPod GraphQL error: {messages}")

    return body.get("data", body)
