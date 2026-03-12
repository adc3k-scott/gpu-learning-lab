"""
Built-in skill: runpod_exec

Execute commands and transfer files on RunPod GPU pods via SSH.

Supported actions:
  execute     — Run a shell command on a running pod (requires pod_id, command)
  deploy      — Upload a local file/directory to a pod (requires pod_id, local_path, remote_path)
  pull        — Download a file from a pod (requires pod_id, remote_path, local_path)
  run_script  — Deploy a script then execute it (requires pod_id, local_path; optional args)

Prerequisites:
  - Pod must be running (use runpod skill to start it first)
  - RUNPOD_API_KEY must be set (used to look up pod SSH connection info)
  - Pod must expose SSH (RunPod pods expose SSH on a dynamic port by default)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shlex
from pathlib import Path
from typing import Any

import httpx

from core.sanitize import safe_error
from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_RUNPOD_API_BASE = "https://api.runpod.io/graphql"
_SSH_TIMEOUT = 120  # seconds
_COMMAND_TIMEOUT = 300  # 5 minutes for GPU workloads
_TRANSFER_TIMEOUT = 600  # 10 minutes for large files


class RunPodExecSkill(BaseSkill):
    name = "runpod_exec"
    description = "Execute commands and transfer files on RunPod GPU pods via SSH"
    version = "0.1.0"
    required_secrets = ["RUNPOD_API_KEY"]

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "")
        if not action:
            return SkillResult.fail("Missing required parameter: action")

        pod_id = params.get("pod_id", "")
        if not pod_id:
            return SkillResult.fail("Missing required parameter: pod_id")

        api_key = (
            ctx.metadata.get("runpod_api_key")
            or os.environ.get("RUNPOD_API_KEY", "")
        )
        if not api_key:
            return SkillResult.fail(
                "RunPod API key not configured. "
                "Set RUNPOD_API_KEY in .env or pass runpod_api_key in skill metadata."
            )

        # Get pod SSH connection info
        try:
            ssh_info = await _get_pod_ssh_info(pod_id, api_key)
        except Exception as exc:
            return SkillResult.fail(f"Failed to get pod SSH info: {safe_error(exc)}")

        if not ssh_info:
            return SkillResult.fail(
                f"Pod {pod_id} has no SSH connection info. "
                "Is the pod running? RunPod pods need to be in RUNNING state."
            )

        host = ssh_info["host"]
        port = ssh_info["port"]

        try:
            if action == "execute":
                return await _execute_command(host, port, params)
            elif action == "deploy":
                return await _deploy_files(host, port, params)
            elif action == "pull":
                return await _pull_files(host, port, params)
            elif action == "run_script":
                return await _run_script(host, port, params)
            else:
                return SkillResult.fail(
                    f"Unknown action {action!r}. "
                    "Choose: execute, deploy, pull, run_script"
                )
        except asyncio.TimeoutError:
            return SkillResult.fail(f"SSH operation timed out after {_COMMAND_TIMEOUT}s")
        except Exception as exc:
            return SkillResult.fail(f"SSH operation failed: {safe_error(exc)}")


# ---------------------------------------------------------------------------
# Pod SSH info lookup via RunPod API
# ---------------------------------------------------------------------------

async def _get_pod_ssh_info(pod_id: str, api_key: str) -> dict[str, Any] | None:
    """Query RunPod API for pod SSH connection details."""
    query = (
        "query Pod($id: String!) { pod(input: { podId: $id }) { "
        "id name desiredStatus runtime { "
        "uptimeInSeconds ports { ip isIpPublic privatePort publicPort type } "
        "} } }"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            _RUNPOD_API_BASE,
            json={"query": query, "variables": {"id": pod_id}},
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

    pod = body.get("data", {}).get("pod")
    if not pod or not pod.get("runtime"):
        return None

    # Find SSH port (private port 22)
    ports = pod["runtime"].get("ports") or []
    for p in ports:
        if p.get("privatePort") == 22 and p.get("isIpPublic"):
            return {
                "host": p["ip"],
                "port": p["publicPort"],
                "pod_id": pod_id,
                "name": pod.get("name", ""),
                "status": pod.get("desiredStatus", ""),
            }

    # Fallback: RunPod standard SSH format
    # Pods are typically accessible at ssh {pod_id}@ssh.runpod.io -p <port>
    # But we need the actual port from the API
    return None


# ---------------------------------------------------------------------------
# SSH command helpers
# ---------------------------------------------------------------------------

def _ssh_base_args(host: str, port: int) -> list[str]:
    """Build base SSH argument list with standard options."""
    return [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "LogLevel=ERROR",
        "-o", f"ConnectTimeout={_SSH_TIMEOUT}",
        "-p", str(port),
        f"root@{host}",
    ]


async def _run_ssh(args: list[str], timeout: int = _COMMAND_TIMEOUT) -> tuple[str, str, int]:
    """Run an SSH command and return (stdout, stderr, returncode)."""
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(
        proc.communicate(), timeout=timeout
    )
    return (
        stdout.decode("utf-8", errors="replace"),
        stderr.decode("utf-8", errors="replace"),
        proc.returncode or 0,
    )


async def _execute_command(
    host: str, port: int, params: dict[str, Any]
) -> SkillResult:
    """Execute a shell command on the pod."""
    command = params.get("command", "")
    if not command:
        return SkillResult.fail("Missing required parameter: command")

    timeout = int(params.get("timeout", _COMMAND_TIMEOUT))
    args = _ssh_base_args(host, port) + [command]

    stdout, stderr, rc = await _run_ssh(args, timeout=timeout)

    # Cap output to prevent massive results
    max_output = 32 * 1024
    if len(stdout) > max_output:
        stdout = stdout[:max_output] + "\n…[truncated]"

    output = {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": rc,
        "command": command,
    }

    if rc != 0:
        return SkillResult(
            success=False,
            output=output,
            error=f"Command exited with code {rc}: {stderr[:500]}",
        )

    return SkillResult.ok(output=output)


async def _deploy_files(
    host: str, port: int, params: dict[str, Any]
) -> SkillResult:
    """Upload files to the pod via scp/rsync."""
    local_path = params.get("local_path", "")
    remote_path = params.get("remote_path", "/workspace/")

    if not local_path:
        return SkillResult.fail("Missing required parameter: local_path")

    local = Path(local_path)
    if not local.exists():
        return SkillResult.fail(f"Local path does not exist: {local_path}")

    # Use scp for single files, rsync for directories
    if local.is_file():
        args = [
            "scp",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "LogLevel=ERROR",
            "-P", str(port),
            str(local),
            f"root@{host}:{remote_path}",
        ]
    else:
        # rsync for directories
        args = [
            "rsync", "-avz", "--progress",
            "-e", f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -p {port}",
            str(local) + "/",
            f"root@{host}:{remote_path}",
        ]

    stdout, stderr, rc = await _run_ssh(args, timeout=_TRANSFER_TIMEOUT)

    if rc != 0:
        return SkillResult.fail(f"File transfer failed (exit {rc}): {stderr[:500]}")

    return SkillResult.ok(output={
        "action": "deploy",
        "local_path": local_path,
        "remote_path": remote_path,
        "stdout": stdout[:2048],
    })


async def _pull_files(
    host: str, port: int, params: dict[str, Any]
) -> SkillResult:
    """Download files from the pod via scp."""
    remote_path = params.get("remote_path", "")
    local_path = params.get("local_path", "")

    if not remote_path:
        return SkillResult.fail("Missing required parameter: remote_path")
    if not local_path:
        return SkillResult.fail("Missing required parameter: local_path")

    # Ensure local directory exists
    local = Path(local_path)
    local.parent.mkdir(parents=True, exist_ok=True)

    args = [
        "scp",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "LogLevel=ERROR",
        "-P", str(port),
        "-r",  # recursive for directories
        f"root@{host}:{remote_path}",
        str(local),
    ]

    stdout, stderr, rc = await _run_ssh(args, timeout=_TRANSFER_TIMEOUT)

    if rc != 0:
        return SkillResult.fail(f"File pull failed (exit {rc}): {stderr[:500]}")

    return SkillResult.ok(output={
        "action": "pull",
        "remote_path": remote_path,
        "local_path": local_path,
        "stdout": stdout[:2048],
    })


async def _run_script(
    host: str, port: int, params: dict[str, Any]
) -> SkillResult:
    """Deploy a script and execute it on the pod in one step."""
    local_path = params.get("local_path", "")
    if not local_path:
        return SkillResult.fail("Missing required parameter: local_path")

    local = Path(local_path)
    if not local.exists():
        return SkillResult.fail(f"Script does not exist: {local_path}")

    script_name = local.name
    remote_dir = params.get("remote_path", "/workspace/")
    remote_script = f"{remote_dir.rstrip('/')}/{script_name}"
    script_args = params.get("args", "")
    timeout = int(params.get("timeout", _COMMAND_TIMEOUT))

    # Step 1: Upload the script
    deploy_result = await _deploy_files(host, port, {
        "local_path": local_path,
        "remote_path": remote_dir,
    })
    if not deploy_result.success:
        return SkillResult.fail(f"Script upload failed: {deploy_result.error}")

    # Step 2: Make executable and run
    command = f"chmod +x {shlex.quote(remote_script)} && {shlex.quote(remote_script)}"
    if script_args:
        command += f" {script_args}"

    args = _ssh_base_args(host, port) + [command]
    stdout, stderr, rc = await _run_ssh(args, timeout=timeout)

    max_output = 32 * 1024
    if len(stdout) > max_output:
        stdout = stdout[:max_output] + "\n…[truncated]"

    output = {
        "action": "run_script",
        "script": script_name,
        "remote_path": remote_script,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": rc,
    }

    if rc != 0:
        return SkillResult(
            success=False,
            output=output,
            error=f"Script exited with code {rc}: {stderr[:500]}",
        )

    return SkillResult.ok(output=output)
