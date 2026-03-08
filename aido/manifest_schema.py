"""
AIDO Content Manifest Schema v1.0

JSON contract between editorial (Notion) and the render pipeline.
Every episode starts as a manifest; the pipeline reads nothing else.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MANIFEST_VERSION = "1.0"

SEGMENT_TYPES = (
    "cold_open",
    "ai_headline",
    "tech_breakthrough",
    "global_map",
    "infrastructure_watch",
    "future_watch",
)


@dataclass
class Segment:
    id: str                        # e.g. "seg_01_cold_open"
    type: str                      # one of SEGMENT_TYPES
    title: str
    narration: str                 # plain text sent to TTS
    duration_hint: float = 30.0   # target seconds
    b_roll_tags: list[str] = field(default_factory=list)
    usd_overrides: dict[str, Any] = field(default_factory=dict)
    audio_path: str = ""           # filled by tts_generate.py
    render_path: str = ""          # filled by render_episode.py


@dataclass
class EpisodeManifest:
    version: str
    episode_id: str               # e.g. "EP001"
    title: str
    subtitle: str
    publish_date: str             # ISO-8601
    voice_id: str                 # ElevenLabs voice ID
    scene_usd: str                # path to base .usda scene file
    segments: list[Segment]
    notion_page_id: str = ""
    youtube_playlist_id: str = ""
    output_dir: str = ""          # filled at pipeline start
    final_mp4: str = ""           # filled by assemble.py

    def to_dict(self) -> dict[str, Any]:
        import dataclasses
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "EpisodeManifest":
        segs = [Segment(**s) for s in d.pop("segments", [])]
        return cls(segments=segs, **d)


# ---------------------------------------------------------------------------
# EP001 manifest — hard-coded for first render
# ---------------------------------------------------------------------------

EP001: EpisodeManifest = EpisodeManifest(
    version=MANIFEST_VERSION,
    episode_id="EP001",
    title="AI Daily Omniverse — Episode 1",
    subtitle="The Week the Models Woke Up",
    publish_date="2026-03-10",
    voice_id="XjLkpWUlnhS8i7gGz3lZ",          # David Castlemore
    scene_usd="workspace/scenes/AIDO_TestScene_v0.1.usda",
    notion_page_id="",
    youtube_playlist_id="",
    segments=[
        Segment(
            id="seg_01_cold_open",
            type="cold_open",
            title="Cold Open",
            narration=(
                "The machines are learning faster than ever. "
                "Welcome to AI Daily Omniverse — your front-row seat "
                "to the technologies reshaping civilization. "
                "I'm your host. Let's go."
            ),
            duration_hint=18.0,
        ),
        Segment(
            id="seg_02_ai_headline",
            type="ai_headline",
            title="AI Headline",
            narration=(
                "This week's headline: Anthropic's Claude 4.6 achieved state-of-the-art "
                "performance on every major reasoning benchmark, while simultaneously "
                "demonstrating real-time tool use at enterprise scale. "
                "The gap between frontier models and everything else just got wider."
            ),
            duration_hint=30.0,
        ),
        Segment(
            id="seg_03_tech_breakthrough",
            type="tech_breakthrough",
            title="Tech Breakthrough",
            narration=(
                "In hardware news — NVIDIA's Blackwell B200 GPUs are shipping to hyperscalers "
                "at 700 teraflops FP8. That's three times Hopper. "
                "RunPod has confirmed B200 pods will be available at twelve dollars an hour. "
                "For small studios and indie developers, that's a game changer."
            ),
            duration_hint=35.0,
        ),
        Segment(
            id="seg_04_global_map",
            type="global_map",
            title="Global AI Map",
            narration=(
                "On the geopolitical map this week — the EU AI Act enforcement phase begins. "
                "High-risk AI systems must now carry certification marks. "
                "Meanwhile, China deployed a national AI infrastructure backbone connecting "
                "forty data centers across twelve provinces. "
                "The race is very much on."
            ),
            duration_hint=35.0,
        ),
        Segment(
            id="seg_05_infrastructure_watch",
            type="infrastructure_watch",
            title="Infrastructure Watch",
            narration=(
                "Infrastructure Watch: Internet of Things sensor networks are integrating "
                "edge AI at a record pace. "
                "Seventy percent of new industrial IoT deployments now include on-device "
                "inference — eliminating cloud round-trips and cutting latency by ninety percent. "
                "Our Mission Control subscribers are already getting daily JSON feeds of these signals."
            ),
            duration_hint=35.0,
        ),
        Segment(
            id="seg_06_future_watch",
            type="future_watch",
            title="Future Watch",
            narration=(
                "Looking ahead — agentic AI systems will be running entire business workflows "
                "without human-in-the-loop checkpoints by Q4 2026. "
                "The organizations building orchestration infrastructure today "
                "will own the operating system of tomorrow. "
                "Stay sharp. Stay subscribed. See you tomorrow."
            ),
            duration_hint=30.0,
        ),
    ],
)
