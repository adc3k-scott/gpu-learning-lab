"""
InfraManagerAgent — monitors and manages platform infrastructure.

Handles steps dispatched with assigned_role="infra_manager".

Capabilities:
  • GPU status — detect available CUDA devices, VRAM, utilisation
  • System resources — CPU, RAM, disk usage
  • Docker services — check if containers are running (when Docker is available)
  • Redis status — ping and report mode (memory / redis)
  • Process list — find Python / uvicorn / agent processes
  • Health report — aggregate summary of all of the above

All checks degrade gracefully: missing drivers / Docker / tools return a
structured "unavailable" message rather than raising exceptions.

Event contract
--------------
Listens on:
  step.dispatched  (filters for assigned_role == "infra_manager")
  infra.check      (triggers an immediate health report, published to infra.report)

Emits:
  step.completed   payload: {job_id, step_id, result}
  step.failed      payload: {job_id, step_id, error}
  infra.report     payload: full health dict
"""

from __future__ import annotations

import asyncio
import logging
import platform
import shutil
import subprocess
import time
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)


class InfraManagerAgent(BaseAgent):
    role = "infra_manager"
    capabilities = ["system_health", "gpu_check", "docker_check", "redis_check"]

    def __init__(self, *, check_interval: float = 60.0, **kwargs):
        super().__init__(**kwargs)
        self._check_interval = check_interval
        self._monitor_task: asyncio.Task | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("step.dispatched", self._on_step_dispatched)
        self.bus.subscribe("infra.check", self._on_infra_check)
        self._monitor_task = asyncio.create_task(
            self._monitor_loop(), name=f"infra-monitor-{self.agent_id}"
        )
        logger.info("[%s] InfraManagerAgent ready", self.agent_id)

    async def _teardown(self) -> None:
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    async def _on_step_dispatched(self, event: Event) -> None:
        payload = event.payload
        if payload.get("assigned_role") != self.role:
            return

        job_id  = payload.get("job_id", "")
        step_id = payload.get("step_id", "")
        params  = payload.get("params", {})
        action  = params.get("action", "health")

        try:
            result = await self._handle(action, params)
            await self.publish("step.completed", {
                "job_id": job_id,
                "step_id": step_id,
                "result": result,
            })
        except Exception as exc:
            logger.exception("[%s] Error in step %s: %s", self.agent_id, step_id, exc)
            await self.publish("step.failed", {
                "job_id": job_id,
                "step_id": step_id,
                "error": str(exc),
            })

    async def _on_infra_check(self, _event: Event) -> None:
        report = await self._health()
        await self.publish("infra.report", report)

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _handle(self, action: str, params: dict[str, Any]) -> Any:
        dispatch = {
            "health":  self._health,
            "gpu":     self._gpu_status,
            "system":  self._system_resources,
            "docker":  self._docker_status,
            "redis":   self._redis_status,
            "process": self._process_list,
        }
        fn = dispatch.get(action, self._health)
        return await fn()

    # ------------------------------------------------------------------
    # Checks
    # ------------------------------------------------------------------

    async def _health(self) -> dict[str, Any]:
        """Aggregate health report — runs all checks in parallel."""
        gpu, sys_res, docker, redis_info, procs = await asyncio.gather(
            self._gpu_status(),
            self._system_resources(),
            self._docker_status(),
            self._redis_status(),
            self._process_list(),
            return_exceptions=True,
        )
        return {
            "timestamp": time.time(),
            "platform": platform.system(),
            "gpu":      gpu     if not isinstance(gpu, Exception)      else {"error": str(gpu)},
            "system":   sys_res if not isinstance(sys_res, Exception)  else {"error": str(sys_res)},
            "docker":   docker  if not isinstance(docker, Exception)   else {"error": str(docker)},
            "redis":    redis_info if not isinstance(redis_info, Exception) else {"error": str(redis_info)},
            "processes": procs  if not isinstance(procs, Exception)    else [],
        }

    async def _gpu_status(self) -> dict[str, Any]:
        """Query nvidia-smi for GPU info; fall back to graceful unavailable."""
        if not shutil.which("nvidia-smi"):
            # Try torch as a fallback
            return await asyncio.get_event_loop().run_in_executor(None, self._gpu_via_torch)

        try:
            out = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: subprocess.check_output(
                        [
                            "nvidia-smi",
                            "--query-gpu=name,memory.total,memory.free,utilization.gpu,temperature.gpu",
                            "--format=csv,noheader,nounits",
                        ],
                        text=True,
                        stderr=subprocess.DEVNULL,
                    ),
                ),
                timeout=5.0,
            )
            gpus = []
            for line in out.strip().splitlines():
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5:
                    gpus.append({
                        "name": parts[0],
                        "vram_total_mb": int(parts[1]),
                        "vram_free_mb":  int(parts[2]),
                        "utilization_pct": int(parts[3]),
                        "temperature_c": int(parts[4]),
                    })
            return {"available": True, "devices": gpus, "count": len(gpus)}
        except Exception as exc:
            return {"available": False, "reason": str(exc)}

    def _gpu_via_torch(self) -> dict[str, Any]:
        try:
            import torch  # type: ignore
            if not torch.cuda.is_available():
                return {"available": False, "reason": "CUDA not available (torch)"}
            devices = []
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                free, total = torch.cuda.mem_get_info(i)
                devices.append({
                    "name": props.name,
                    "vram_total_mb": total // (1024 * 1024),
                    "vram_free_mb":  free  // (1024 * 1024),
                    "utilization_pct": None,
                    "temperature_c": None,
                })
            return {"available": True, "devices": devices, "count": len(devices), "via": "torch"}
        except ImportError:
            return {"available": False, "reason": "nvidia-smi not found, torch not installed"}

    async def _system_resources(self) -> dict[str, Any]:
        return await asyncio.get_event_loop().run_in_executor(None, self._system_sync)

    def _system_sync(self) -> dict[str, Any]:
        result: dict[str, Any] = {"platform": platform.platform()}
        try:
            import psutil  # type: ignore
            vm = psutil.virtual_memory()
            dk = psutil.disk_usage(".")
            result.update({
                "cpu_count": psutil.cpu_count(),
                "cpu_pct": psutil.cpu_percent(interval=0.1),
                "ram_total_gb": round(vm.total / 1e9, 1),
                "ram_used_gb":  round(vm.used  / 1e9, 1),
                "ram_pct": vm.percent,
                "disk_total_gb": round(dk.total / 1e9, 1),
                "disk_used_gb":  round(dk.used  / 1e9, 1),
                "disk_pct": dk.percent,
            })
        except ImportError:
            result["note"] = "psutil not installed — install for detailed system metrics"
        return result

    async def _docker_status(self) -> dict[str, Any]:
        if not shutil.which("docker"):
            return {"available": False, "reason": "docker CLI not found"}
        try:
            out = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: subprocess.check_output(
                        ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
                        text=True,
                        stderr=subprocess.DEVNULL,
                    ),
                ),
                timeout=5.0,
            )
            containers = []
            for line in out.strip().splitlines():
                if "\t" in line:
                    name, status = line.split("\t", 1)
                    containers.append({"name": name, "status": status})
            return {"available": True, "containers": containers, "count": len(containers)}
        except subprocess.CalledProcessError:
            return {"available": False, "reason": "Docker daemon not running"}
        except Exception as exc:
            return {"available": False, "reason": str(exc)}

    async def _redis_status(self) -> dict[str, Any]:
        mode = self.store.mode
        info: dict[str, Any] = {"mode": mode}
        if mode == "redis":
            try:
                await asyncio.wait_for(self.store._redis.ping(), timeout=2.0)  # type: ignore
                info["reachable"] = True
            except Exception as exc:
                info["reachable"] = False
                info["error"] = str(exc)
        return info

    async def _process_list(self) -> list[dict[str, Any]]:
        return await asyncio.get_event_loop().run_in_executor(None, self._process_sync)

    def _process_sync(self) -> list[dict[str, Any]]:
        procs = []
        try:
            import psutil  # type: ignore
            keywords = {"python", "uvicorn", "agent"}
            for p in psutil.process_iter(["pid", "name", "cmdline", "cpu_percent", "memory_info"]):
                try:
                    cmdline = " ".join(p.info["cmdline"] or []).lower()
                    if any(k in cmdline for k in keywords):
                        procs.append({
                            "pid": p.info["pid"],
                            "name": p.info["name"],
                            "cmd": cmdline[:120],
                            "cpu_pct": p.info["cpu_percent"],
                            "ram_mb": round((p.info["memory_info"].rss or 0) / 1e6, 1),
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except ImportError:
            pass
        return procs

    # ------------------------------------------------------------------
    # Background monitor — caches health report to state store
    # ------------------------------------------------------------------

    async def _monitor_loop(self) -> None:
        while self._running:
            try:
                report = await self._health()
                await self.store.set("infra:health", report, ttl=int(self._check_interval * 2))
                logger.debug("[%s] Infra health cached", self.agent_id)
            except Exception as exc:
                logger.warning("[%s] Monitor error: %s", self.agent_id, exc)
            try:
                await asyncio.sleep(self._check_interval)
            except asyncio.CancelledError:
                break
