"""
Built-in skill: gpu_job

End-to-end GPU job pipeline: start pod → wait ready → submit job →
poll status → download results → stop pod.

Designed for the render agent (port 8501) but extensible to any
FastAPI service running on a RunPod pod.

Supported actions:
  render        — submit a render job and wait for results
  submit        — submit a job without waiting (returns job_id)
  status        — check status of a running job
  results       — download results from a completed job
  full_pipeline — start pod, render, download, stop pod (all-in-one)

Credentials:
  RUNPOD_API_KEY — for pod start/stop
  JUPYTER_TOKEN  — for exec bridge fallback
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any

import httpx

from core.sanitize import safe_error
from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_RUNPOD_GQL = "https://api.runpod.io/graphql"
_AGENT_PORT = 8501
_POLL_INTERVAL = 15  # seconds between status checks
_MAX_WAIT = 600  # max seconds to wait for a job
_POD_READY_TIMEOUT = 180  # max seconds to wait for pod to come online
_POD_READY_POLL = 10  # seconds between pod ready checks


class GpuJobSkill(BaseSkill):
    name = "gpu_job"
    description = (
        "End-to-end GPU job pipeline — submit render/inference jobs to "
        "RunPod pods, poll for completion, download results"
    )
    version = "1.0.0"
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
            return SkillResult.fail("RUNPOD_API_KEY not configured")

        pod_id = params.get("pod_id", "")
        if not pod_id:
            return SkillResult.fail("Missing required parameter: pod_id")

        port = params.get("port", _AGENT_PORT)

        try:
            if action == "render":
                return await self._render(api_key, pod_id, port, params)
            elif action == "submit":
                return await self._submit(pod_id, port, params)
            elif action == "status":
                return await self._status(pod_id, port, params)
            elif action == "results":
                return await self._results(pod_id, port, params)
            elif action == "full_pipeline":
                return await self._full_pipeline(api_key, pod_id, port, params, ctx)
            else:
                return SkillResult.fail(
                    f"Unknown action {action!r}. "
                    "Choose: render, submit, status, results, full_pipeline"
                )
        except Exception as exc:
            return SkillResult.fail(safe_error(exc))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    async def _render(
        self, api_key: str, pod_id: str, port: int, params: dict
    ) -> SkillResult:
        """Submit a render job and wait for completion."""
        # Build job request
        job_req = {
            "prompt": params.get("prompt", "all angles"),
            "style": params.get("style", "bright_daylight"),
            "resolution": params.get("resolution", "1920x1080"),
            "num_outputs": params.get("num_outputs", 12),
            "settle_frames": params.get("settle_frames", 300),
        }
        if params.get("cameras"):
            job_req["cameras"] = params["cameras"]

        # Submit
        base = _pod_url(pod_id, port)
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{base}/submit_job", json=job_req)
            resp.raise_for_status()
            submit_data = resp.json()

        job_id = submit_data.get("job_id")
        if not job_id:
            return SkillResult.fail(f"No job_id in response: {submit_data}")

        logger.info("GPU job %s submitted to pod %s", job_id, pod_id)

        # Poll for completion
        result = await self._poll_job(pod_id, port, job_id)
        return result

    async def _submit(self, pod_id: str, port: int, params: dict) -> SkillResult:
        """Submit a job without waiting."""
        job_req = {
            "prompt": params.get("prompt", "all angles"),
            "style": params.get("style", "bright_daylight"),
            "resolution": params.get("resolution", "1920x1080"),
            "num_outputs": params.get("num_outputs", 12),
            "settle_frames": params.get("settle_frames", 300),
        }
        if params.get("cameras"):
            job_req["cameras"] = params["cameras"]

        base = _pod_url(pod_id, port)
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{base}/submit_job", json=job_req)
            resp.raise_for_status()
            data = resp.json()

        return SkillResult.ok(output=data)

    async def _status(self, pod_id: str, port: int, params: dict) -> SkillResult:
        """Check job status."""
        job_id = params.get("job_id", "")
        if not job_id:
            return SkillResult.fail("Missing job_id for status check")

        base = _pod_url(pod_id, port)
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{base}/job_status/{job_id}")
            resp.raise_for_status()
            data = resp.json()

        return SkillResult.ok(output=data)

    async def _results(self, pod_id: str, port: int, params: dict) -> SkillResult:
        """Get results (image list + URLs) from a completed job."""
        job_id = params.get("job_id", "")
        if not job_id:
            return SkillResult.fail("Missing job_id for results")

        base = _pod_url(pod_id, port)
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{base}/results/{job_id}")
            resp.raise_for_status()
            data = resp.json()

        return SkillResult.ok(output=data)

    async def _full_pipeline(
        self, api_key: str, pod_id: str, port: int, params: dict, ctx: SkillContext
    ) -> SkillResult:
        """Full pipeline: start pod → wait ready → render → stop pod."""
        timeline = {"start": time.time()}

        # Step 1: Start pod
        logger.info("Starting pod %s", pod_id)
        await _runpod_mutation(
            "mutation($id:String!){podResume(input:{podId:$id,gpuCount:1}){id desiredStatus}}",
            {"id": pod_id},
            api_key,
        )
        timeline["pod_resume_sent"] = time.time()

        # Step 2: Wait for pod + render agent to be ready
        logger.info("Waiting for pod %s to be ready...", pod_id)
        base = _pod_url(pod_id, port)
        ready = False
        deadline = time.time() + _POD_READY_TIMEOUT
        while time.time() < deadline:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(f"{base}/")
                    if resp.is_success:
                        data = resp.json()
                        if data.get("service") == "ADC Render Agent":
                            ready = True
                            break
            except Exception:
                pass
            await asyncio.sleep(_POD_READY_POLL)

        if not ready:
            return SkillResult.fail(
                f"Pod {pod_id} did not become ready within {_POD_READY_TIMEOUT}s. "
                "Render agent may not be running. Start it with: "
                "python /workspace/render_agent.py &"
            )
        timeline["pod_ready"] = time.time()
        logger.info("Pod %s ready in %.0fs", pod_id, timeline["pod_ready"] - timeline["start"])

        # Step 3: Submit render job
        render_result = await self._render(api_key, pod_id, port, params)
        timeline["render_complete"] = time.time()

        if not render_result.success:
            # Don't stop pod on failure — might want to debug
            return render_result

        # Step 4: Stop pod
        logger.info("Stopping pod %s", pod_id)
        await _runpod_mutation(
            "mutation($id:String!){podStop(input:{podId:$id}){id desiredStatus}}",
            {"id": pod_id},
            api_key,
        )
        timeline["pod_stopped"] = time.time()

        # Enrich output with timeline
        output = render_result.output
        if isinstance(output, dict):
            output["pipeline_timeline"] = {
                "total_seconds": round(timeline["pod_stopped"] - timeline["start"], 1),
                "pod_startup": round(timeline["pod_ready"] - timeline["start"], 1),
                "render_time": round(
                    timeline["render_complete"] - timeline["pod_ready"], 1
                ),
            }

        return SkillResult.ok(output=output)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _poll_job(self, pod_id: str, port: int, job_id: str) -> SkillResult:
        """Poll job status until complete or timeout."""
        base = _pod_url(pod_id, port)
        deadline = time.time() + _MAX_WAIT

        while time.time() < deadline:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.get(f"{base}/job_status/{job_id}")
                    resp.raise_for_status()
                    data = resp.json()

                status = data.get("status", "unknown")
                progress = data.get("progress", "")
                logger.info("Job %s: %s (%s)", job_id, status, progress)

                if status == "complete":
                    return SkillResult.ok(output=data)
                elif status == "failed":
                    errors = data.get("errors", [])
                    return SkillResult.fail(
                        f"Job {job_id} failed: {errors}"
                    )
            except Exception as exc:
                logger.warning("Poll error for job %s: %s", job_id, exc)

            await asyncio.sleep(_POLL_INTERVAL)

        return SkillResult.fail(
            f"Job {job_id} timed out after {_MAX_WAIT}s"
        )


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------


def _pod_url(pod_id: str, port: int) -> str:
    """Build the RunPod proxy URL for a pod's service port."""
    return f"https://{pod_id}-{port}.proxy.runpod.net"


async def _runpod_mutation(query: str, variables: dict, api_key: str) -> dict:
    """Execute a RunPod GraphQL mutation."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            _RUNPOD_GQL,
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
        msgs = "; ".join(e.get("message", str(e)) for e in body["errors"])
        raise RuntimeError(f"RunPod GraphQL error: {msgs}")
    return body.get("data", body)
