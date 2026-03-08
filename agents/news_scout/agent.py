"""
NewsScoutAgent — Daily intelligence gathering for all Mission Control verticals.

Pulls RSS feeds, scores stories by relevance, drafts segment narration,
and writes episode manifests to Notion + StateStore for the PublisherAgent.

Verticals:
  ai          — AI Daily Omniverse (AIDO)
  auv         — Autonomous Underwater Vehicles / Maritime
  robotics    — Robotics & automation
  aviation    — eVTOL, SAF, airspace, avionics
  motorcycle  — EV moto, connected gear, racing tech, culture

Event contract
--------------
Listens:
  news.scout.run        — {vertical, max_stories}  trigger a scout run
  news.scout.schedule   — fires on cron (set up at startup)

Emits:
  news.stories.ready    — {vertical, stories: [...], episode_draft: {...}}
  news.scout.error      — {vertical, error}

StateStore keys
---------------
  news:latest:{vertical}        — last scout result
  news:stories:{vertical}       — list of scored stories
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import xml.etree.ElementTree as ET
from typing import Any

import httpx
from anthropic import AsyncAnthropic

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# RSS feed registry — one list per vertical
# ---------------------------------------------------------------------------

FEEDS: dict[str, list[str]] = {
    "ai": [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://venturebeat.com/ai/feed/",
        "https://www.technologyreview.com/feed/",
        "https://blogs.nvidia.com/feed/",
        "https://www.anthropic.com/rss.xml",
        "https://openai.com/blog/rss.xml",
    ],
    "auv": [
        "https://www.navalnews.com/feed/",
        "https://www.therobotreport.com/feed/",
        "https://www.offshore-technology.com/feed/",
        "https://gcaptain.com/feed/",
    ],
    "robotics": [
        "https://www.therobotreport.com/feed/",
        "https://spectrum.ieee.org/feeds/topic/robotics.rss",
        "https://techcrunch.com/tag/robotics/feed/",
        "https://www.automationworld.com/rss.xml",
    ],
    "aviation": [
        "https://simpleflying.com/feed/",
        "https://www.avweb.com/feed/",
        "https://aviationweek.com/rss.xml",
        "https://techcrunch.com/tag/evtol/feed/",
        "https://www.ainonline.com/rss.xml",
    ],
    "motorcycle": [
        "https://www.cycleworld.com/rss/all.xml/",
        "https://www.motorcyclistonline.com/rss/all.xml/",
        "https://www.rideapart.com/rss/all.xml/",
        "https://www.visordown.com/rss.xml",
        "https://electrek.co/tag/electric-motorcycle/feed/",
    ],
}

_RELEVANCE_SYSTEM = """\
You are a senior editor for Mission Control, a daily technology intelligence network.
Score each story 1-10 for relevance to the vertical. Return JSON only.
High scores: new products/models, technical breakthroughs, regulations, funding rounds, deployments.
Low scores: opinion pieces, listicles, celebrity gossip, unrelated topics.
"""


class NewsScoutAgent(BaseAgent):
    role = "news_scout"

    def __init__(self, *, llm_client: AsyncAnthropic, llm_model: str, **kwargs):
        super().__init__(**kwargs)
        self._llm = llm_client
        self._model = llm_model
        self._scout_interval = 3600 * 6    # every 6 hours by default
        self._scout_task: asyncio.Task | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("news.scout.run", self._on_scout_run)
        self._scout_task = asyncio.create_task(self._scheduled_scout())
        logger.info("[%s] NewsScoutAgent ready — verticals: %s", self.agent_id, list(FEEDS))

    async def _teardown(self) -> None:
        if self._scout_task:
            self._scout_task.cancel()

    # ------------------------------------------------------------------
    # Scheduled + manual triggers
    # ------------------------------------------------------------------

    async def _scheduled_scout(self) -> None:
        """Run all verticals on a schedule."""
        await asyncio.sleep(30)    # let server fully start first
        while self._running:
            for vertical in FEEDS:
                try:
                    await self._run_vertical(vertical, max_stories=5)
                    await asyncio.sleep(2)
                except Exception as exc:
                    logger.error("[%s] Scout error (%s): %s", self.agent_id, vertical, exc)
            await asyncio.sleep(self._scout_interval)

    async def _on_scout_run(self, event: Event) -> None:
        vertical = event.payload.get("vertical", "ai")
        max_stories = int(event.payload.get("max_stories", 5))
        await self._run_vertical(vertical, max_stories)

    # ------------------------------------------------------------------
    # Core scout logic
    # ------------------------------------------------------------------

    async def _run_vertical(self, vertical: str, max_stories: int = 5) -> None:
        logger.info("[%s] Scouting vertical: %s", self.agent_id, vertical)
        feeds = FEEDS.get(vertical, [])
        if not feeds:
            logger.warning("[%s] Unknown vertical: %s", self.agent_id, vertical)
            return

        # Pull and parse all feeds
        raw_stories: list[dict] = []
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            for feed_url in feeds:
                try:
                    resp = await client.get(feed_url, headers={"User-Agent": "MissionControl/1.0"})
                    if resp.is_success:
                        items = _parse_rss(resp.text, feed_url)
                        raw_stories.extend(items)
                except Exception as exc:
                    logger.debug("[%s] Feed error %s: %s", self.agent_id, feed_url, exc)

        if not raw_stories:
            logger.warning("[%s] No stories fetched for %s", self.agent_id, vertical)
            await self.publish("news.scout.error", {"vertical": vertical, "error": "No RSS items fetched"})
            return

        # Deduplicate by title
        seen: set[str] = set()
        unique: list[dict] = []
        for s in raw_stories:
            key = s["title"].lower()[:60]
            if key not in seen:
                seen.add(key)
                unique.append(s)

        # Score and rank
        scored = await self._score_stories(unique[:30], vertical)
        top = sorted(scored, key=lambda x: x.get("score", 0), reverse=True)[:max_stories]

        # Draft narration for each segment
        episode_draft = await self._draft_episode(top, vertical)

        # Persist
        result = {
            "vertical": vertical,
            "fetched_at": time.time(),
            "story_count": len(top),
            "stories": top,
            "episode_draft": episode_draft,
        }
        await self.store.set(f"news:latest:{vertical}", result, ttl=86400)
        await self.store.set(f"news:stories:{vertical}", top, ttl=86400)

        logger.info("[%s] Scout complete: %s — %d stories", self.agent_id, vertical, len(top))
        await self.publish("news.stories.ready", result)

    # ------------------------------------------------------------------
    # LLM: score stories
    # ------------------------------------------------------------------

    async def _score_stories(self, stories: list[dict], vertical: str) -> list[dict]:
        stories_text = json.dumps([{"title": s["title"], "summary": s["summary"][:200]} for s in stories], indent=2)
        prompt = (
            f"Vertical: {vertical}\n\n"
            f"Stories:\n{stories_text}\n\n"
            f"Return a JSON array: [{{'index': 0, 'score': 8, 'reason': '...'}},...] "
            f"Score each story 1-10. Return ONLY valid JSON, no markdown."
        )
        try:
            resp = await self._llm.messages.create(
                model=self._model,
                max_tokens=1024,
                system=_RELEVANCE_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            scores_raw = resp.content[0].text.strip()
            # Strip markdown fences if present
            if scores_raw.startswith("```"):
                scores_raw = scores_raw.split("```")[1]
                if scores_raw.startswith("json"):
                    scores_raw = scores_raw[4:]
            scores = json.loads(scores_raw)
            for item in scores:
                idx = item.get("index", 0)
                if 0 <= idx < len(stories):
                    stories[idx]["score"] = item.get("score", 5)
                    stories[idx]["score_reason"] = item.get("reason", "")
        except Exception as exc:
            logger.warning("[%s] Scoring LLM error: %s — using default scores", self.agent_id, exc)
            for s in stories:
                s.setdefault("score", 5)
        return stories

    # ------------------------------------------------------------------
    # LLM: draft episode narration
    # ------------------------------------------------------------------

    async def _draft_episode(self, stories: list[dict], vertical: str) -> dict[str, Any]:
        stories_text = "\n\n".join(
            f"STORY {i+1}: {s['title']}\n{s['summary'][:400]}"
            for i, s in enumerate(stories)
        )
        system = (
            "You are the head writer for Mission Control, a daily AI-powered news broadcast. "
            "Write concise, punchy narration in present tense. "
            "Each segment: 2-4 sentences, 30-45 words. No fluff, no filler. "
            "Return JSON only."
        )
        prompt = (
            f"Vertical: {vertical}\n\nTop stories today:\n{stories_text}\n\n"
            f"Write a 4-segment episode draft. Return JSON:\n"
            f'{{"title": "...", "segments": [{{"id": "seg_01", "type": "headline", "title": "...", "narration": "..."}},...]}}'
            f"\nReturn ONLY valid JSON."
        )
        try:
            resp = await self._llm.messages.create(
                model=self._model,
                max_tokens=1500,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except Exception as exc:
            logger.warning("[%s] Draft LLM error: %s", self.agent_id, exc)
            return {"title": f"Mission Control — {vertical.title()} Briefing", "segments": []}


# ---------------------------------------------------------------------------
# RSS parser (no external library required)
# ---------------------------------------------------------------------------

def _parse_rss(xml_text: str, source_url: str) -> list[dict]:
    items: list[dict] = []
    try:
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # Standard RSS 2.0
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link") or "").strip()
            desc  = (item.findtext("description") or "").strip()
            pub   = (item.findtext("pubDate") or "").strip()
            if title:
                items.append({
                    "title": title,
                    "url": link,
                    "summary": _strip_html(desc)[:500],
                    "published": pub,
                    "source": source_url,
                    "score": 5,
                })

        # Atom feeds
        if not items:
            for entry in root.findall("atom:entry", ns):
                title = (entry.findtext("atom:title", namespaces=ns) or "").strip()
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                summary = (entry.findtext("atom:summary", namespaces=ns) or "").strip()
                if title:
                    items.append({
                        "title": title,
                        "url": link,
                        "summary": _strip_html(summary)[:500],
                        "published": "",
                        "source": source_url,
                        "score": 5,
                    })
    except Exception as exc:
        logger.debug("RSS parse error for %s: %s", source_url, exc)
    return items


def _strip_html(text: str) -> str:
    import re
    return re.sub(r"<[^>]+>", " ", text).strip()
