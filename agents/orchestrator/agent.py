"""
OrchestratorAgent — the central coordinator of Mission Control.

Responsibilities:
  • Accept task requests via events ("task.requested")
  • Use the Planner to decompose tasks into Jobs with Steps
  • Dispatch each Step to the appropriate specialist agent
  • Track job progress in the StateStore
  • Emit lifecycle events for every state transition
  • Retry failed steps up to their max_attempts limit
  • Mark jobs completed / failed when all steps finish

Event contract
--------------
Listens on:
  task.requested   payload: {description, title?, requested_by?}
  step.completed   payload: {job_id, step_id, result}
  step.failed      payload: {job_id, step_id, error}

Emits:
  job.created      payload: {job_id, title, steps: [...]}
  job.started      payload: {job_id}
  job.completed    payload: {job_id, results: {...}}
  job.failed       payload: {job_id, error}
  step.dispatched  payload: {job_id, step_id, assigned_role, skill}
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from agents.base import BaseAgent
from agents.orchestrator.job import Job, JobStatus, Step, StepStatus
from agents.orchestrator.planner import plan, replan
from core.event_bus import Event

logger = logging.getLogger(__name__)

# StateStore key prefix for jobs
_JOB_KEY = "jobs:{job_id}"

# Matches {{step_name}} or {{step_name.result}} in param string values
_TEMPLATE_RE = re.compile(r"\{\{([\w.]+)\}\}")


def _resolve_params(params: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    """
    Substitute {{step_name}} references in param values with prior step results.

    Rules:
    - If a string value is exactly "{{step_name}}", it is replaced with the raw result
      (which may be any JSON-serialisable type).
    - If a string value contains "{{step_name}}" alongside other text, the result is
      JSON-serialised and interpolated into the string.
    - Nested dicts and lists are traversed recursively.
    - Unknown references are left as-is.
    """
    def _sub(value: Any) -> Any:
        if isinstance(value, str):
            # Exact match — return the raw result value (preserves type)
            m = _TEMPLATE_RE.fullmatch(value.strip())
            if m:
                key = m.group(1).split(".")[0]   # {{step_name}} or {{step_name.result}}
                return results.get(key, value)
            # Partial match — stringify the result into the template
            def _replace(match: re.Match) -> str:
                key = match.group(1).split(".")[0]
                val = results.get(key)
                if val is None:
                    return match.group(0)   # leave unchanged
                return val if isinstance(val, str) else json.dumps(val)
            return _TEMPLATE_RE.sub(_replace, value)
        if isinstance(value, dict):
            return {k: _sub(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_sub(v) for v in value]
        return value

    return {k: _sub(v) for k, v in params.items()}


class OrchestratorAgent(BaseAgent):
    role = "orchestrator"

    def __init__(self, *, llm_client: Any = None, llm_model: str = "claude-opus-4-5", **kwargs):
        super().__init__(**kwargs)
        self._llm_client = llm_client
        self._llm_model = llm_model
        self._jobs: dict[str, Job] = {}                      # in-process job cache
        self._step_lock = asyncio.Lock()
        self._job_waiters: dict[str, list[asyncio.Queue]] = {}  # job_id → SSE queues

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("task.requested", self._on_task_requested)
        self.bus.subscribe("step.completed", self._on_step_completed)
        self.bus.subscribe("step.failed", self._on_step_failed)
        logger.info("[%s] OrchestratorAgent ready", self.agent_id)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    async def _on_task_requested(self, event: Event) -> None:
        payload = event.payload
        description = payload.get("description", "")
        if not description:
            logger.warning("task.requested received with no description")
            return

        job = await plan(
            description=description,
            title=payload.get("title", ""),
            requested_by=payload.get("requested_by", event.source or "user"),
            llm_client=self._llm_client,
            llm_model=self._llm_model,
        )

        # Honour a pre-assigned job_id from submit_task() so callers can track immediately
        if preset_id := payload.get("job_id"):
            job.job_id = preset_id

        await self._register_job(job)
        await self.publish("job.created", {
            "job_id": job.job_id,
            "title": job.title,
            "steps": [s.to_dict() for s in job.steps],
        })

        await self._advance_job(job)

    async def _on_step_completed(self, event: Event) -> None:
        async with self._step_lock:
            job_id = event.payload.get("job_id", "")
            step_id = event.payload.get("step_id", "")
            result = event.payload.get("result")

            job = self._jobs.get(job_id)
            if not job:
                return

            step = job.get_step(step_id)
            if step:
                step.complete(result)
                logger.info("[%s] Step %s completed in job %s", self.agent_id, step_id, job_id)
                self._push_job_event(job_id, {"type": "step.completed", "step": step.to_dict()})

            await self._persist_job(job)

        await self._advance_job(job)

    async def _on_step_failed(self, event: Event) -> None:
        async with self._step_lock:
            job_id = event.payload.get("job_id", "")
            step_id = event.payload.get("step_id", "")
            error = event.payload.get("error", "unknown error")

            job = self._jobs.get(job_id)
            if not job:
                return

            step = job.get_step(step_id)
            if step:
                step.fail(error)
                logger.warning("[%s] Step %s failed: %s", self.agent_id, step_id, error)
                self._push_job_event(job_id, {"type": "step.failed", "step": step.to_dict()})

            await self._persist_job(job)

        await self._advance_job(job)

    # ------------------------------------------------------------------
    # Job execution engine
    # ------------------------------------------------------------------

    async def _advance_job(self, job: Job) -> None:
        """Dispatch all ready steps; finalise the job if nothing left to do."""
        if job.status == JobStatus.PENDING:
            job.start()
            await self.publish("job.started", {"job_id": job.job_id})

        # Retry eligible failed steps first
        for step in job.retryable_steps():
            step.status = StepStatus.PENDING   # reset so ready_steps() picks it up

        ready = job.ready_steps()

        # --- Adaptive replanning ---
        # If no ready steps, there are exhausted failures, and we haven't replanned yet,
        # ask the LLM for a revised plan before giving up.
        if (
            not ready
            and not job.is_done()
            and job.has_failures()
            and not job.metadata.get("replanned")
            and self._llm_client is not None
        ):
            await self._attempt_replan(job)
            # Re-check after replanning
            ready = job.ready_steps()

        for step in ready:
            asyncio.create_task(self._dispatch_step(job, step))

        if not ready and job.is_done():
            await self._finalise_job(job)

    async def _attempt_replan(self, job: Job) -> None:
        """Ask the planner for a revised plan after a step failure."""
        job.metadata["replanned"] = True  # only try once per job

        completed = [
            {"name": s.name, "result": s.result}
            for s in job.steps if s.status == StepStatus.COMPLETED
        ]
        failed = next(
            ({"name": s.name, "error": s.error, "params": s.params}
             for s in job.steps if s.status == StepStatus.FAILED),
            None,
        )
        pending = [
            {"name": s.name, "description": s.description, "skill": s.skill,
             "assigned_role": s.assigned_role, "params": s.params}
            for s in job.steps if s.status == StepStatus.PENDING
        ]

        if not failed:
            return

        logger.info("[%s] Attempting replan for job %s", self.agent_id, job.job_id)

        revised = await replan(
            original_description=job.description,
            completed_steps=completed,
            failed_step=failed,
            pending_steps=pending,
            llm_client=self._llm_client,
            llm_model=self._llm_model,
        )

        if not revised:
            logger.info("[%s] Replan returned no alternative — job will fail", self.agent_id)
            return

        # Remove all PENDING and FAILED steps, replace with revised plan
        job.steps = [s for s in job.steps if s.status == StepStatus.COMPLETED]

        # Build name→id mapping including completed steps
        name_to_id = {s.name: s.step_id for s in job.steps}

        for sd in revised:
            step = Step(
                name=sd.get("name", "step"),
                description=sd.get("description", ""),
                assigned_role=sd.get("assigned_role", "orchestrator"),
                skill=sd.get("skill", ""),
                params=sd.get("params") or {},
                depends_on=[name_to_id[n] for n in sd.get("depends_on", []) if n in name_to_id],
            )
            name_to_id[step.name] = step.step_id
            job.steps.append(step)

        await self._persist_job(job)
        self._push_job_event(job.job_id, {
            "type": "job.replanned",
            "steps": [s.to_dict() for s in job.steps],
        })
        logger.info(
            "[%s] Replanned job %s with %d new step(s)",
            self.agent_id, job.job_id, len(revised),
        )

    async def _dispatch_step(self, job: Job, step: Step) -> None:
        step.start()
        await self._persist_job(job)

        # Resolve {{step_name}} template references in params using prior results
        resolved_params = _resolve_params(step.params, job.results_by_name())

        logger.info(
            "[%s] Dispatching step %r (role=%s skill=%s) for job %s",
            self.agent_id, step.name, step.assigned_role, step.skill, job.job_id,
        )
        await self.publish("step.dispatched", {
            "job_id": job.job_id,
            "step_id": step.step_id,
            "assigned_role": step.assigned_role,
            "skill": step.skill,
            "params": resolved_params,
            "description": step.description,
        })

        # If the step is assigned to orchestrator itself and has a skill, run it directly
        if step.assigned_role == self.role and step.skill:
            result = await self.run_skill(step.skill, step.params, job_id=job.job_id)
            if result.success:
                await self.publish("step.completed", {
                    "job_id": job.job_id,
                    "step_id": step.step_id,
                    "result": result.output,
                })
            else:
                await self.publish("step.failed", {
                    "job_id": job.job_id,
                    "step_id": step.step_id,
                    "error": result.error,
                })

    def _push_job_event(self, job_id: str, event: dict) -> None:
        """Push a job-level event dict to all SSE waiters for this job."""
        for q in self._job_waiters.get(job_id, []):
            q.put_nowait(event)

    def subscribe_job(self, job_id: str) -> asyncio.Queue:
        """Return a queue that will receive job progress events until unsubscribed."""
        q: asyncio.Queue = asyncio.Queue()
        self._job_waiters.setdefault(job_id, []).append(q)
        return q

    def unsubscribe_job(self, job_id: str, q: asyncio.Queue) -> None:
        waiters = self._job_waiters.get(job_id, [])
        if q in waiters:
            waiters.remove(q)
        if not waiters:
            self._job_waiters.pop(job_id, None)

    async def _finalise_job(self, job: Job) -> None:
        if job.has_failures():
            failed = [s.name for s in job.steps if s.status == StepStatus.FAILED]
            job.fail(f"Steps failed: {', '.join(failed)}")
            await self.publish("job.failed", {"job_id": job.job_id, "error": job.error})
            logger.warning("[%s] Job %s FAILED: %s", self.agent_id, job.job_id, job.error)
        else:
            job.complete()
            results = {
                s.name: s.result
                for s in job.steps
                if s.status == StepStatus.COMPLETED
            }
            await self.publish("job.completed", {"job_id": job.job_id, "results": results})
            logger.info("[%s] Job %s COMPLETED", self.agent_id, job.job_id)

        await self._persist_job(job)
        # Signal all waiters that the job is done
        self._push_job_event(job.job_id, {"type": "job.done", "job": job.to_dict()})

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    async def _register_job(self, job: Job) -> None:
        self._jobs[job.job_id] = job
        await self._persist_job(job)

    async def _persist_job(self, job: Job) -> None:
        await self.store.set(_JOB_KEY.format(job_id=job.job_id), job.to_dict(), ttl=86400)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def submit_task(self, description: str, title: str = "", requested_by: str = "user") -> str:
        """
        Programmatic shortcut — submit a task without going through the event bus.
        Returns the job_id.
        """
        from uuid import uuid4
        preset_job_id = str(uuid4())
        await self.publish("task.requested", {
            "description": description,
            "title": title,
            "requested_by": requested_by,
            "job_id": preset_job_id,
        })
        return preset_job_id

    async def get_job(self, job_id: str) -> dict[str, Any] | None:
        """Return the persisted job dict from the state store."""
        return await self.store.get(_JOB_KEY.format(job_id=job_id))

    async def list_jobs(self) -> list[dict[str, Any]]:
        """Return all jobs currently tracked in the state store."""
        return list((await self.store.get_all("jobs:*")).values())
