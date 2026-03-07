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
import logging
from typing import Any

from agents.base import BaseAgent
from agents.orchestrator.job import Job, JobStatus, Step, StepStatus
from agents.orchestrator.planner import plan
from core.event_bus import Event

logger = logging.getLogger(__name__)

# StateStore key prefix for jobs
_JOB_KEY = "jobs:{job_id}"


class OrchestratorAgent(BaseAgent):
    role = "orchestrator"

    def __init__(self, *, llm_client: Any = None, llm_model: str = "claude-opus-4-5", **kwargs):
        super().__init__(**kwargs)
        self._llm_client = llm_client
        self._llm_model = llm_model
        self._jobs: dict[str, Job] = {}   # in-process job cache
        self._step_lock = asyncio.Lock()

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
        for step in ready:
            asyncio.create_task(self._dispatch_step(job, step))

        if not ready and job.is_done():
            await self._finalise_job(job)

    async def _dispatch_step(self, job: Job, step: Step) -> None:
        step.start()
        await self._persist_job(job)

        logger.info(
            "[%s] Dispatching step %r (role=%s skill=%s) for job %s",
            self.agent_id, step.name, step.assigned_role, step.skill, job.job_id,
        )
        await self.publish("step.dispatched", {
            "job_id": job.job_id,
            "step_id": step.step_id,
            "assigned_role": step.assigned_role,
            "skill": step.skill,
            "params": step.params,
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
        await self.publish("task.requested", {
            "description": description,
            "title": title,
            "requested_by": requested_by,
        })
        # Give the event loop a tick to process the publish
        await asyncio.sleep(0)
        # Find the most recently created job
        job_ids = [j for j in self._jobs]
        return job_ids[-1] if job_ids else ""

    async def get_job(self, job_id: str) -> dict[str, Any] | None:
        """Return the persisted job dict from the state store."""
        return await self.store.get(_JOB_KEY.format(job_id=job_id))

    async def list_jobs(self) -> list[dict[str, Any]]:
        """Return all jobs currently tracked in the state store."""
        return list((await self.store.get_all("jobs:*")).values())
