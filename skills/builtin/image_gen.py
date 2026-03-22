"""
Built-in skill: image_gen

Generate and edit images via RunPod Hub public endpoints.

Supported actions:
  generate      -- text prompt -> image (FLUX Schnell or FLUX Dev)
  edit          -- source image + text prompt -> edited image (FLUX Kontext)
  list_models   -- show configured models and endpoints
  status        -- check async job status

Models (RunPod Hub public endpoints -- no deployment needed):
  flux-schnell  -- fast text-to-image (~3s warm, ~30s cold, ~$0.003/image)
  flux-dev      -- high-quality text-to-image (~15s, ~$0.01/image)
  flux-kontext  -- image editing with text instructions (~15s, ~$0.02/edit)

Credentials:
  RUNPOD_API_KEY -- RunPod API key (shared with runpod skill)
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

import httpx

from core.sanitize import safe_error
from skills.base import BaseSkill, RetryPolicy, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_RUNPOD_BASE = "https://api.runpod.ai/v2"
_POLL_INTERVAL = 2.0
_MAX_POLL_TIME = 180.0
_SYNC_TIMEOUT = 120.0
_ASYNC_TIMEOUT = 20.0

# RunPod Hub public endpoint slugs -- these are pre-deployed by RunPod
# No custom serverless endpoint creation needed
_MODELS = {
    "flux-schnell": {
        "hub_slug": "black-forest-labs-flux-1-schnell",
        "env_var": "RUNPOD_FLUX_SCHNELL_ID",
        "description": "FLUX.1 Schnell -- fast text-to-image (~3s warm, ~$0.003/image)",
        "supports_edit": False,
    },
    "flux-dev": {
        "hub_slug": "black-forest-labs-flux-1-dev",
        "env_var": "RUNPOD_FLUX_DEV_ID",
        "description": "FLUX.1 Dev -- high-quality text-to-image (~15s, ~$0.01/image)",
        "supports_edit": False,
    },
    "flux-kontext": {
        "hub_slug": "black-forest-labs-flux-1-kontext-dev",
        "env_var": "RUNPOD_FLUX_KONTEXT_ID",
        "description": "FLUX.1 Kontext [dev] -- image editing with text instructions (~$0.02/edit)",
        "supports_edit": True,
    },
}

_DEFAULT_OUTPUT_DIR = "adc3k-deploy/renders"


class ImageGenSkill(BaseSkill):
    name = "image_gen"
    description = (
        "Generate and edit images via RunPod Hub -- "
        "FLUX Schnell (fast T2I), FLUX Dev (quality T2I), FLUX Kontext (image editing)"
    )
    version = "1.0.0"
    required_secrets = ["RUNPOD_API_KEY"]
    retry_policy = RetryPolicy(max_attempts=2, backoff_base=3.0, timeout=180.0)

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "")
        if not action:
            return SkillResult.fail("Missing required parameter: action")

        api_key = _resolve_api_key(ctx)
        if not api_key:
            return SkillResult.fail(
                "RunPod API key not configured. "
                "Set RUNPOD_API_KEY in .env or pass runpod_api_key in metadata."
            )

        try:
            if action == "generate":
                return await self._generate(api_key, ctx, params)
            elif action == "edit":
                return await self._edit(api_key, ctx, params)
            elif action == "list_models":
                return self._list_models()
            elif action == "status":
                return await self._check_status(api_key, params)
            else:
                return SkillResult.fail(
                    f"Unknown action {action!r}. Choose: generate, edit, list_models, status"
                )
        except Exception as exc:
            return SkillResult.fail(safe_error(exc))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    async def _generate(
        self, api_key: str, ctx: SkillContext, params: dict[str, Any]
    ) -> SkillResult:
        prompt = params.get("prompt", "")
        if not prompt:
            return SkillResult.fail("Missing required parameter: prompt")

        model_name = params.get("model", "flux-schnell")
        model = _MODELS.get(model_name)
        if not model:
            return SkillResult.fail(
                f"Unknown model {model_name!r}. Choose: {', '.join(_MODELS)}"
            )

        endpoint_id = _resolve_endpoint(model_name, params, ctx)

        width = params.get("width", 1024)
        height = params.get("height", 1024)
        seed = params.get("seed")
        num_images = params.get("num_images", 1)

        payload = {
            "input": {
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_images": num_images,
            }
        }
        if seed is not None:
            payload["input"]["seed"] = seed

        t0 = time.monotonic()

        # Try runsync first (blocks until done, up to 120s)
        result = await _runsync(api_key, endpoint_id, payload)

        # If runsync returns IN_QUEUE (cold start), poll
        if result.get("status") in ("IN_QUEUE", "IN_PROGRESS"):
            job_id = result.get("id", "")
            logger.info("Job %s queued (cold start), polling...", job_id)
            result = await _poll_job(api_key, endpoint_id, job_id)

        elapsed_ms = int((time.monotonic() - t0) * 1000)

        if result.get("status") == "FAILED":
            error = result.get("error", "Unknown error")
            return SkillResult.fail(f"Generation failed: {error}")

        output = result.get("output", {})
        cost = output.get("cost", 0) if isinstance(output, dict) else 0

        image_data = await _extract_image(output)
        if not image_data:
            return SkillResult.fail(
                f"No image in response. Output: {_summarize(output)}"
            )

        output_dir = params.get("output_dir", _DEFAULT_OUTPUT_DIR)
        filename = params.get("filename") or _auto_filename(model_name, prompt)
        project_root = ctx.metadata.get("project_root", ".")

        saved_path = _save_image(image_data, output_dir, filename, project_root)

        return SkillResult.ok(
            output={
                "image_path": saved_path,
                "model": model_name,
                "prompt": prompt,
                "dimensions": f"{width}x{height}",
                "job_id": result.get("id", ""),
                "cost": cost,
                "generation_time_ms": elapsed_ms,
            },
            model=model_name,
            cost=cost,
            generation_time_ms=elapsed_ms,
        )

    async def _edit(
        self, api_key: str, ctx: SkillContext, params: dict[str, Any]
    ) -> SkillResult:
        prompt = params.get("prompt", "")
        source = params.get("source_image", "")
        if not prompt:
            return SkillResult.fail("Missing required parameter: prompt")
        if not source:
            return SkillResult.fail("Missing required parameter: source_image")

        model_name = params.get("model", "flux-kontext")
        model = _MODELS.get(model_name)
        if not model:
            return SkillResult.fail(f"Unknown model {model_name!r}.")
        if not model.get("supports_edit"):
            return SkillResult.fail(
                f"Model {model_name} does not support editing. Use flux-kontext."
            )

        endpoint_id = _resolve_endpoint(model_name, params, ctx)

        # Read and encode source image
        project_root = ctx.metadata.get("project_root", ".")
        source_path = Path(project_root) / source
        if not source_path.exists():
            source_path = Path(source)
        if not source_path.exists():
            return SkillResult.fail(f"Source image not found: {source}")

        # Check file size (RunPod limit: 10MB for /run, 20MB for /runsync)
        file_size = source_path.stat().st_size
        if file_size > 15_000_000:
            return SkillResult.fail(
                f"Source image too large ({file_size:,} bytes). Max ~15MB for RunPod."
            )

        with open(source_path, "rb") as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        seed = params.get("seed")

        payload = {
            "input": {
                "prompt": prompt,
                "image": image_b64,
            }
        }
        if seed is not None:
            payload["input"]["seed"] = seed

        t0 = time.monotonic()

        # Use /run for edits (large payload)
        job_id = await _run_async(api_key, endpoint_id, payload)
        result = await _poll_job(api_key, endpoint_id, job_id)

        elapsed_ms = int((time.monotonic() - t0) * 1000)

        if result.get("status") == "FAILED":
            error = result.get("error", "Unknown error")
            return SkillResult.fail(f"Edit failed: {error}")

        output = result.get("output", {})
        cost = output.get("cost", 0) if isinstance(output, dict) else 0

        image_data = await _extract_image(output)
        if not image_data:
            return SkillResult.fail(
                f"No image in response. Output: {_summarize(output)}"
            )

        output_dir = params.get("output_dir", _DEFAULT_OUTPUT_DIR)
        filename = params.get("filename") or _auto_filename(model_name, prompt, prefix="edit")
        saved_path = _save_image(image_data, output_dir, filename, project_root)

        return SkillResult.ok(
            output={
                "image_path": saved_path,
                "model": model_name,
                "prompt": prompt,
                "source_image": str(source),
                "job_id": result.get("id", ""),
                "cost": cost,
                "generation_time_ms": elapsed_ms,
            },
            model=model_name,
            cost=cost,
            generation_time_ms=elapsed_ms,
        )

    def _list_models(self) -> SkillResult:
        models = {}
        for name, cfg in _MODELS.items():
            custom_id = os.environ.get(cfg["env_var"], "")
            models[name] = {
                "description": cfg["description"],
                "hub_slug": cfg["hub_slug"],
                "custom_endpoint": custom_id or "(using Hub public endpoint)",
                "supports_edit": cfg.get("supports_edit", False),
            }
        return SkillResult.ok(output=models)

    async def _check_status(
        self, api_key: str, params: dict[str, Any]
    ) -> SkillResult:
        job_id = params.get("job_id", "")
        model_name = params.get("model", "flux-schnell")
        if not job_id:
            return SkillResult.fail("Missing required parameter: job_id")

        endpoint_id = _resolve_endpoint(model_name, params, SkillContext())

        async with httpx.AsyncClient(timeout=_ASYNC_TIMEOUT) as client:
            resp = await client.get(
                f"{_RUNPOD_BASE}/{endpoint_id}/status/{job_id}",
                headers={"Authorization": f"Bearer {api_key}"},
            )
        if not resp.is_success:
            return SkillResult.fail(f"Status check failed: HTTP {resp.status_code}")

        return SkillResult.ok(output=resp.json())


# ---------------------------------------------------------------------------
# RunPod API helpers
# ---------------------------------------------------------------------------


def _resolve_api_key(ctx: SkillContext) -> str:
    return (
        ctx.metadata.get("runpod_api_key")
        or os.environ.get("RUNPOD_API_KEY", "")
    )


def _resolve_endpoint(
    model_name: str, params: dict[str, Any], ctx: SkillContext
) -> str:
    """Resolve endpoint ID: params > env var > Hub public slug."""
    if params.get("endpoint_id"):
        return params["endpoint_id"]

    model = _MODELS.get(model_name, {})
    env_key = model.get("env_var", "")

    # Check env var for custom endpoint override
    custom = os.environ.get(env_key, "") if env_key else ""
    if custom:
        return custom

    # Fall back to Hub public endpoint slug
    return model.get("hub_slug", "")


async def _runsync(
    api_key: str, endpoint_id: str, payload: dict
) -> dict:
    """Synchronous call -- blocks until result."""
    async with httpx.AsyncClient(timeout=_SYNC_TIMEOUT) as client:
        resp = await client.post(
            f"{_RUNPOD_BASE}/{endpoint_id}/runsync",
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
        )
    if not resp.is_success:
        raise RuntimeError(f"RunPod runsync HTTP {resp.status_code}: {resp.text[:400]}")
    return resp.json()


async def _run_async(api_key: str, endpoint_id: str, payload: dict) -> str:
    """Submit async job, return job ID."""
    async with httpx.AsyncClient(timeout=_ASYNC_TIMEOUT) as client:
        resp = await client.post(
            f"{_RUNPOD_BASE}/{endpoint_id}/run",
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
        )
    if not resp.is_success:
        raise RuntimeError(f"RunPod run HTTP {resp.status_code}: {resp.text[:400]}")
    data = resp.json()
    job_id = data.get("id", "")
    if not job_id:
        raise RuntimeError(f"No job ID in response: {data}")
    logger.info("Submitted async job %s to endpoint %s", job_id, endpoint_id)
    return job_id


async def _poll_job(api_key: str, endpoint_id: str, job_id: str) -> dict:
    """Poll until job completes or times out."""
    deadline = time.monotonic() + _MAX_POLL_TIME
    while time.monotonic() < deadline:
        async with httpx.AsyncClient(timeout=_ASYNC_TIMEOUT) as client:
            resp = await client.get(
                f"{_RUNPOD_BASE}/{endpoint_id}/status/{job_id}",
                headers={"Authorization": f"Bearer {api_key}"},
            )
        if not resp.is_success:
            raise RuntimeError(f"Poll HTTP {resp.status_code}: {resp.text[:400]}")

        data = resp.json()
        status = data.get("status", "")

        if status == "COMPLETED":
            return data
        if status == "FAILED":
            return data

        logger.debug("Job %s status: %s", job_id, status)
        await asyncio.sleep(_POLL_INTERVAL)

    raise TimeoutError(f"Job {job_id} timed out after {_MAX_POLL_TIME}s")


# ---------------------------------------------------------------------------
# Image handling
# ---------------------------------------------------------------------------


async def _extract_image(output: Any) -> bytes | None:
    """Extract image bytes from RunPod Hub response formats.

    Hub endpoints typically return: {"image_url": "https://...", "cost": 0.00x}
    """
    if isinstance(output, dict):
        # Hub format: image_url
        for key in ("image_url", "image", "images", "output", "result"):
            val = output.get(key)
            if not val:
                continue

            if isinstance(val, str):
                if val.startswith("http"):
                    return await _download_url(val)
                try:
                    return base64.b64decode(val)
                except Exception:
                    pass

            elif isinstance(val, list) and val:
                first = val[0]
                if isinstance(first, str):
                    if first.startswith("http"):
                        return await _download_url(first)
                    try:
                        return base64.b64decode(first)
                    except Exception:
                        pass
                elif isinstance(first, dict):
                    for k in ("image_url", "image", "url", "base64"):
                        v = first.get(k)
                        if v and isinstance(v, str):
                            if v.startswith("http"):
                                return await _download_url(v)
                            try:
                                return base64.b64decode(v)
                            except Exception:
                                pass

    elif isinstance(output, str):
        if output.startswith("http"):
            return await _download_url(output)
        try:
            return base64.b64decode(output)
        except Exception:
            pass

    return None


async def _download_url(url: str) -> bytes:
    """Download image from URL."""
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content


def _save_image(
    image_data: bytes, output_dir: str, filename: str, project_root: str
) -> str:
    """Save image to disk with path-traversal guard."""
    root = Path(project_root).resolve()
    out = (root / output_dir).resolve()

    # Path traversal guard
    try:
        out.relative_to(root)
    except ValueError:
        raise ValueError(f"Output directory {output_dir} escapes project root")

    out.mkdir(parents=True, exist_ok=True)

    # Ensure image extension
    if not filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
        filename += ".jpg"

    filepath = out / filename

    # Don't overwrite -- add suffix if exists
    if filepath.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        i = 1
        while filepath.exists():
            filepath = out / f"{stem}_{i}{suffix}"
            i += 1

    filepath.write_bytes(image_data)
    logger.info("Saved image: %s (%d bytes)", filepath, len(image_data))

    # Return relative path from project root
    try:
        return str(filepath.relative_to(root))
    except ValueError:
        return str(filepath)


def _auto_filename(model: str, prompt: str, prefix: str = "gen") -> str:
    """Generate descriptive filename from model + prompt."""
    slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower().strip())[:40].strip("-")
    ts = time.strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{model}_{slug}_{ts}.jpg"


def _summarize(output: Any) -> str:
    """Summarize output for error messages."""
    if isinstance(output, dict):
        return f"dict with keys: {list(output.keys())}"
    if isinstance(output, list):
        return f"list[{len(output)}]"
    return f"{type(output).__name__}: {str(output)[:100]}"
