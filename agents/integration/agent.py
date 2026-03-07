"""
IntegrationAgent — handles all outbound HTTP and external service calls.

Handles steps dispatched with assigned_role="integration".

Capabilities:
  • Generic HTTP requests (GET/POST/PUT/DELETE) with auth header injection
  • RunPod API — list pods, start/stop pods, get pod status
  • Webhook delivery — POST a payload to any URL with retry
  • Health-check a URL and return status code + latency

All network calls use httpx with timeouts so they never block the agent loop.

Event contract
--------------
Listens on:
  step.dispatched  (filters for assigned_role == "integration")

Emits:
  step.completed   payload: {job_id, step_id, result}
  step.failed      payload: {job_id, step_id, error}

Step params schema
------------------
action: "http" | "runpod" | "webhook" | "ping"

action=http:
  method  : GET | POST | PUT | DELETE  (default GET)
  url     : str
  headers : dict  (optional)
  body    : dict  (optional, JSON)
  timeout : float (default 10.0)

action=runpod:
  operation : "list_pods" | "pod_status" | "start_pod" | "stop_pod" | "terminate_pod"
  pod_id    : str  (for pod_status/start/stop/terminate)

action=webhook:
  url     : str
  payload : dict
  secret  : str  (optional — sent as X-Webhook-Secret header)
  retries : int  (default 2)

action=ping:
  url     : str
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_RUNPOD_API_BASE = "https://api.runpod.io/graphql"
_DEFAULT_TIMEOUT = 10.0


class IntegrationAgent(BaseAgent):
    role = "integration"

    def __init__(self, *, runpod_api_key: str = "", **kwargs):
        super().__init__(**kwargs)
        self._runpod_key = runpod_api_key

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        # Pull RunPod key from state store secrets if not passed directly
        if not self._runpod_key:
            stored = await self.store.get("secrets:runpod_api_key")
            if stored:
                self._runpod_key = stored
        self.bus.subscribe("step.dispatched", self._on_step_dispatched)
        logger.info("[%s] IntegrationAgent ready", self.agent_id)

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    async def _on_step_dispatched(self, event: Event) -> None:
        payload = event.payload
        if payload.get("assigned_role") != self.role:
            return

        job_id  = payload.get("job_id", "")
        step_id = payload.get("step_id", "")
        params  = payload.get("params", {})
        action  = params.get("action", "http")

        skill_name = payload.get("skill", "")

        try:
            if skill_name:
                result_obj = await self.run_skill(skill_name, params, job_id=job_id)
                if not result_obj.success:
                    raise RuntimeError(result_obj.error)
                result = result_obj.output
            else:
                result = await self._handle(action, params)
            await self.publish("step.completed", {
                "job_id": job_id,
                "step_id": step_id,
                "result": result,
            })
        except Exception as exc:
            logger.exception("[%s] Step %s error: %s", self.agent_id, step_id, exc)
            await self.publish("step.failed", {
                "job_id": job_id,
                "step_id": step_id,
                "error": str(exc),
            })

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _handle(self, action: str, params: dict[str, Any]) -> Any:
        if action == "http":
            return await self._http_request(params)
        if action == "runpod":
            return await self._runpod(params)
        if action == "webhook":
            return await self._webhook(params)
        if action == "ping":
            return await self._ping(params)
        raise ValueError(f"Unknown action {action!r}. Choose: http, runpod, webhook, ping")

    # ------------------------------------------------------------------
    # Generic HTTP
    # ------------------------------------------------------------------

    async def _http_request(self, params: dict[str, Any]) -> dict[str, Any]:
        method  = params.get("method", "GET").upper()
        url     = params.get("url", "")
        headers = dict(params.get("headers") or {})
        body    = params.get("body")
        timeout = float(params.get("timeout", _DEFAULT_TIMEOUT))

        if not url:
            raise ValueError("http action requires a 'url' parameter")

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.request(
                method, url, headers=headers,
                json=body if body else None,
            )

        result: dict[str, Any] = {
            "status_code": resp.status_code,
            "ok": resp.is_success,
            "url": str(resp.url),
        }
        try:
            result["json"] = resp.json()
        except Exception:
            result["text"] = resp.text[:2000]
        return result

    # ------------------------------------------------------------------
    # RunPod GraphQL API
    # ------------------------------------------------------------------

    async def _runpod(self, params: dict[str, Any]) -> dict[str, Any]:
        operation = params.get("operation", "list_pods")
        pod_id    = params.get("pod_id", "")

        if not self._runpod_key:
            raise RuntimeError(
                "RunPod API key not configured. "
                "Set RUNPOD_API_KEY in .env or store under 'secrets:runpod_api_key'."
            )

        query, variables = self._build_runpod_query(operation, pod_id)

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                _RUNPOD_API_BASE,
                json={"query": query, "variables": variables},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._runpod_key}",
                },
            )

        if not resp.is_success:
            raise RuntimeError(f"RunPod API error {resp.status_code}: {resp.text[:500]}")

        data = resp.json()
        if "errors" in data:
            raise RuntimeError(f"RunPod GraphQL errors: {data['errors']}")
        return data.get("data", data)

    def _build_runpod_query(self, operation: str, pod_id: str) -> tuple[str, dict]:
        if operation == "list_pods":
            return (
                "query { myself { pods { id name desiredStatus runtime { uptimeInSeconds } } } }",
                {},
            )
        if operation == "pod_status":
            return (
                "query Pod($id: String!) { pod(input: { podId: $id }) { id name desiredStatus runtime { uptimeInSeconds gpus { id memoryInGb } } } }",
                {"id": pod_id},
            )
        if operation == "start_pod":
            return (
                "mutation StartPod($id: String!) { podResume(input: { podId: $id, gpuCount: 1 }) { id desiredStatus } }",
                {"id": pod_id},
            )
        if operation == "stop_pod":
            return (
                "mutation StopPod($id: String!) { podStop(input: { podId: $id }) { id desiredStatus } }",
                {"id": pod_id},
            )
        if operation == "terminate_pod":
            return (
                "mutation TerminatePod($id: String!) { podTerminate(input: { podId: $id }) }",
                {"id": pod_id},
            )
        raise ValueError(f"Unknown RunPod operation: {operation!r}")

    # ------------------------------------------------------------------
    # Webhook delivery
    # ------------------------------------------------------------------

    async def _webhook(self, params: dict[str, Any]) -> dict[str, Any]:
        url     = params.get("url", "")
        payload = params.get("payload", {})
        secret  = params.get("secret", "")
        retries = int(params.get("retries", 2))

        if not url:
            raise ValueError("webhook action requires a 'url' parameter")

        headers: dict[str, str] = {"Content-Type": "application/json"}
        if secret:
            headers["X-Webhook-Secret"] = secret

        last_exc: Exception | None = None
        for attempt in range(1, retries + 2):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                return {
                    "delivered": resp.is_success,
                    "status_code": resp.status_code,
                    "attempts": attempt,
                    "url": url,
                }
            except Exception as exc:
                last_exc = exc
                logger.warning("[%s] Webhook attempt %d failed: %s", self.agent_id, attempt, exc)

        raise RuntimeError(f"Webhook failed after {retries + 1} attempts: {last_exc}")

    # ------------------------------------------------------------------
    # Ping / health-check
    # ------------------------------------------------------------------

    async def _ping(self, params: dict[str, Any]) -> dict[str, Any]:
        url     = params.get("url", "")
        timeout = float(params.get("timeout", 5.0))

        if not url:
            raise ValueError("ping action requires a 'url' parameter")

        t0 = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.get(url)
            latency_ms = round((time.monotonic() - t0) * 1000, 1)
            return {
                "reachable": True,
                "status_code": resp.status_code,
                "latency_ms": latency_ms,
                "url": url,
            }
        except Exception as exc:
            latency_ms = round((time.monotonic() - t0) * 1000, 1)
            return {
                "reachable": False,
                "error": str(exc),
                "latency_ms": latency_ms,
                "url": url,
            }
