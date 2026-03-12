"""
Built-in skill: browser

Drive a real browser via Playwright to interact with web pages that require
login sessions, JavaScript rendering, or UI automation.

Uses the user's existing Edge persistent profile by default -- no re-login needed
for sites the user is already signed into (Google, Notion, GitHub, etc.).

Supported actions:
  navigate      -- go to a URL, return {url, title, text, screenshot_b64}
  screenshot    -- take a screenshot of the current page, return base64 PNG
  click         -- click an element by CSS selector (tries each in a list)
  fill          -- fill a text input by CSS selector
  get_text      -- return inner text of page or a specific selector
  find          -- check if a selector exists, return {found, text}
  run_session   -- execute a sequence of steps in one browser session
                   (most powerful -- avoids relaunching browser for each step)

run_session step format:
  Each step is a dict with an "action" key plus action-specific params.
  Steps run sequentially; results collected per step.
  If a step fails and continue_on_error is False (default), session stops.

  Example steps:
    {"action": "navigate",   "url": "https://example.com"}
    {"action": "wait",       "ms": 2000}
    {"action": "screenshot"}
    {"action": "click",      "selectors": ["button:has-text('Sign in')"]}
    {"action": "fill",       "selector": "input[name='q']", "value": "hello"}
    {"action": "get_text",   "selector": "body"}
    {"action": "find",       "selector": "button:has-text('Delete')"}
    {"action": "eval",       "expression": "document.title"}

Top-level params:
  browser        : "edge" (default, uses persistent login) | "chromium" (fresh/headless)
  headless       : bool (default False for edge, True for chromium)
  slow_mo        : int ms between Playwright actions (default 300)
  screenshot_dir : directory to save named screenshots (default ".")
  continue_on_error : bool -- keep running steps after failure (default False)
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
import time
from typing import Any

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_EDGE_EXE     = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
_EDGE_PROFILE = r"C:\Users\adhsc\AppData\Local\Microsoft\Edge\User Data"
_TEXT_LIMIT   = 8 * 1024   # 8 KB cap
_DEFAULT_TIMEOUT = 15_000  # ms


class BrowserSkill(BaseSkill):
    name = "browser"
    description = (
        "Control a real browser (Edge or Chromium) via Playwright. "
        "Navigate, click, fill forms, take screenshots, extract text. "
        "Uses existing Edge login sessions -- no re-auth required."
    )
    version = "0.1.0"

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "navigate").lower()
        try:
            if action == "run_session":
                return await self._run_session(params)
            # Single-action: wrap as one-step session
            return await self._run_session({
                **params,
                "steps": [{**params, "action": action}],
                "action": "run_session",
            })
        except ImportError:
            return SkillResult.fail(
                "Playwright not installed. "
                "Run: pip install playwright && playwright install"
            )
        except Exception as exc:
            logger.exception("browser skill error: %s", exc)
            return SkillResult.fail(str(exc))

    # ------------------------------------------------------------------
    # Session runner
    # ------------------------------------------------------------------

    async def _run_session(self, params: dict[str, Any]) -> SkillResult:
        from playwright.async_api import async_playwright

        steps: list[dict]  = params.get("steps", [])
        browser_type: str  = params.get("browser", "edge").lower()
        headless: bool     = params.get("headless", browser_type != "edge")
        slow_mo: int       = int(params.get("slow_mo", 300))
        cont_on_err: bool  = params.get("continue_on_error", False)
        scr_dir: str       = params.get("screenshot_dir", ".")

        t0 = time.perf_counter()
        step_results: list[dict] = []
        final_url = final_title = ""

        async with async_playwright() as pw:
            bctx = await self._launch(pw, browser_type, headless, slow_mo)
            page = bctx.pages[0] if bctx.pages else await bctx.new_page()

            for i, step in enumerate(steps):
                act = step.get("action", "").lower()
                sr: dict[str, Any] = {"action": act, "step": i}
                try:
                    sr.update(await self._step(page, act, step, scr_dir))
                    sr["ok"] = True
                except Exception as exc:
                    sr["ok"] = False
                    sr["error"] = str(exc)
                    logger.warning("step %d (%s) failed: %s", i, act, exc)
                    step_results.append(sr)
                    if not cont_on_err:
                        break
                    continue
                step_results.append(sr)

            try:
                final_url   = page.url
                final_title = await page.title()
            except Exception:
                pass
            await bctx.close()

        elapsed = round((time.perf_counter() - t0) * 1000, 1)
        all_ok = all(s.get("ok") for s in step_results)
        output = {
            "url": final_url, "title": final_title,
            "steps": step_results, "latency_ms": elapsed,
        }

        if not all_ok:
            failed = [s for s in step_results if not s.get("ok")]
            return SkillResult.fail(
                f"{len(failed)} step(s) failed: {failed[-1].get('error', 'unknown')}",
                output=output, latency_ms=elapsed,
            )
        return SkillResult.ok(output=output, latency_ms=elapsed)

    # ------------------------------------------------------------------
    # Individual step dispatcher
    # ------------------------------------------------------------------

    async def _step(
        self, page: Any, action: str, params: dict, scr_dir: str
    ) -> dict[str, Any]:
        timeout = int(params.get("timeout", _DEFAULT_TIMEOUT))

        if action == "navigate":
            url = params.get("url") or (_ for _ in ()).throw(ValueError("navigate requires url"))
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            await page.wait_for_timeout(int(params.get("wait_ms", 2000)))
            out = {"url": page.url, "title": await page.title(),
                   "text": await self._text(page)}
            if params.get("screenshot", True):
                out["screenshot_b64"] = await self._scr_b64(page)
            return out

        if action == "wait":
            ms = int(params.get("ms", 1000))
            await page.wait_for_timeout(ms)
            return {"waited_ms": ms}

        if action == "screenshot":
            b64 = await self._scr_b64(page)
            path = params.get("path")
            if path:
                full = os.path.join(scr_dir, path)
                await page.screenshot(path=full)
                return {"saved_to": full, "screenshot_b64": b64}
            return {"screenshot_b64": b64}

        if action == "click":
            sels = params.get("selectors") or (
                [params["selector"]] if "selector" in params else []
            )
            if not sels:
                raise ValueError("click requires selector or selectors")
            per = max(timeout // len(sels), 3000)
            for sel in sels:
                try:
                    el = await page.wait_for_selector(sel, timeout=per)
                    if el:
                        txt = await el.inner_text()
                        await el.click()
                        await page.wait_for_timeout(int(params.get("wait_ms", 1000)))
                        return {"clicked": sel, "element_text": txt.strip()}
                except Exception:
                    continue
            raise ValueError(f"No element found for: {sels}")

        if action == "fill":
            sel = params.get("selector") or (_ for _ in ()).throw(ValueError("fill requires selector"))
            val = params.get("value", "")
            el = await page.wait_for_selector(sel, timeout=timeout)
            await el.fill(val)
            return {"filled": sel, "value": val}

        if action == "get_text":
            sel = params.get("selector")
            if sel:
                el = await page.wait_for_selector(sel, timeout=timeout)
                return {"text": (await el.inner_text())[:_TEXT_LIMIT]}
            return {"text": await self._text(page)}

        if action == "find":
            sels = params.get("selectors") or (
                [params["selector"]] if "selector" in params else []
            )
            if not sels:
                raise ValueError("find requires selector or selectors")
            for sel in sels:
                try:
                    el = await page.wait_for_selector(sel, timeout=min(timeout, 5000))
                    if el:
                        return {"found": True, "selector": sel,
                                "text": (await el.inner_text()).strip()}
                except Exception:
                    continue
            return {"found": False, "selectors_tried": sels}

        if action == "eval":
            if not os.getenv("BROWSER_ALLOW_EVAL"):
                raise ValueError(
                    "eval action is disabled by default (security risk). "
                    "Set BROWSER_ALLOW_EVAL=1 to enable."
                )
            expr = params.get("expression") or (_ for _ in ()).throw(ValueError("eval requires expression"))
            return {"result": await page.evaluate(expr)}

        raise ValueError(f"Unknown browser action: {action!r}")

    # ------------------------------------------------------------------
    # Launch helpers
    # ------------------------------------------------------------------

    async def _launch(self, pw: Any, browser_type: str, headless: bool, slow_mo: int) -> Any:
        if browser_type == "edge":
            # Release profile lock by killing running Edge processes
            try:
                import subprocess
                subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"],
                               capture_output=True, check=False)
                await asyncio.sleep(1.5)
            except Exception:
                pass
            return await pw.chromium.launch_persistent_context(
                user_data_dir=_EDGE_PROFILE,
                executable_path=_EDGE_EXE,
                headless=headless,
                slow_mo=slow_mo,
                args=["--profile-directory=Default"],
            )
        # Headless Chromium -- fresh session, no existing logins
        browser = await pw.chromium.launch(headless=headless, slow_mo=slow_mo)
        return await browser.new_context()

    async def _text(self, page: Any) -> str:
        try:
            return (await page.inner_text("body"))[:_TEXT_LIMIT]
        except Exception:
            return ""

    async def _scr_b64(self, page: Any) -> str:
        try:
            return base64.b64encode(await page.screenshot(type="png")).decode()
        except Exception:
            return ""
