"""
Built-in skill: http_client

Make outbound HTTP requests from inside the agent pipeline.

Supported actions:
  get    — HTTP GET  (alias: http with method=GET)
  post   — HTTP POST (alias: http with method=POST)
  ping   — HEAD or GET to check reachability; returns {status, ok, latency_ms}

Params:
  action  : "get" | "post" | "ping" | "http"
  url     : str   (required)
  method  : str   (default inferred from action, or "GET")
  headers : dict  (optional, default {})
  body    : any   (optional; serialised as JSON for POST/PUT/PATCH)
  params  : dict  (optional query-string params)
  timeout : float (seconds, default 15.0)
  follow_redirects : bool (default True)

Result output:
  {
    "status": <int>,
    "ok":     <bool>,
    "headers": {<response headers>},
    "text":   <response body as string, truncated at 32 KB>,
    "json":   <parsed JSON if content-type is application/json>,
  }
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_MAX_BODY_BYTES = 32 * 1024   # 32 KB — cap response body stored in result
_DEFAULT_TIMEOUT = 15.0


class HttpClientSkill(BaseSkill):
    name = "http_client"
    description = (
        "Make outbound HTTP requests (GET, POST, ping) and return status + body. "
        "Use for webhooks, health checks, and API calls."
    )
    version = "0.1.0"

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "http").lower()
        url = params.get("url", "").strip()

        if not url:
            return SkillResult.fail("Missing required parameter: url")

        method = params.get("method", "").upper()
        if not method:
            method = {"get": "GET", "post": "POST", "ping": "HEAD", "http": "GET"}.get(action, "GET")

        headers: dict[str, str] = params.get("headers") or {}
        body = params.get("body")
        query = params.get("params") or {}
        timeout = float(params.get("timeout", _DEFAULT_TIMEOUT))
        follow_redirects = bool(params.get("follow_redirects", True))

        try:
            return await self._request(
                method=method,
                url=url,
                headers=headers,
                body=body,
                query=query,
                timeout=timeout,
                follow_redirects=follow_redirects,
                is_ping=(action == "ping"),
            )
        except httpx.TimeoutException:
            return SkillResult.fail(f"Request timed out after {timeout}s: {url}")
        except httpx.InvalidURL as exc:
            return SkillResult.fail(f"Invalid URL {url!r}: {exc}")
        except Exception as exc:
            logger.exception("http_client error: %s", exc)
            return SkillResult.fail(str(exc))

    async def _request(
        self,
        *,
        method: str,
        url: str,
        headers: dict,
        body: Any,
        query: dict,
        timeout: float,
        follow_redirects: bool,
        is_ping: bool,
    ) -> SkillResult:
        t0 = time.perf_counter()

        async with httpx.AsyncClient(
            follow_redirects=follow_redirects,
            timeout=timeout,
        ) as client:
            kwargs: dict[str, Any] = {"headers": headers, "params": query}
            if body is not None:
                if isinstance(body, (dict, list)):
                    kwargs["json"] = body
                else:
                    kwargs["content"] = str(body).encode()

            response = await client.request(method, url, **kwargs)

        latency_ms = round((time.perf_counter() - t0) * 1000, 1)

        # Build result dict
        resp_headers = dict(response.headers)
        content_type = response.headers.get("content-type", "")

        result: dict[str, Any] = {
            "status": response.status_code,
            "ok": response.is_success,
            "latency_ms": latency_ms,
            "headers": resp_headers,
        }

        if not is_ping:
            raw = response.content[:_MAX_BODY_BYTES]
            try:
                text = raw.decode("utf-8", errors="replace")
            except Exception:
                text = repr(raw)
            result["text"] = text
            if "application/json" in content_type:
                try:
                    result["json"] = response.json()
                except Exception:
                    pass

        return SkillResult.ok(output=result, latency_ms=latency_ms)
