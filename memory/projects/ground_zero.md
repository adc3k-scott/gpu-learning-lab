# Ground Zero — YouTube Channel
Last updated: 2026-03-08

## What It Is
Daily AI technology situation report. Documents the AI revolution in real time.
Mission Control (Claude) produces episode manifest + script packages on command.

## Status: OPERATIONAL — Content Pipeline Live
- Channel: Ground Zero | Handle: @GroundZero-ai
- OAuth token: `youtube_token.json` in project root
- Dedicated Chrome profile + Google account for business (separate from personal)
- EP001 v3 published (private): https://www.youtube.com/watch?v=2B-W9d6aLEw

## Pipeline
Run: `python -m aido.pipeline --episode EP001 --local-render`
Upload only: `python -m aido.pipeline --episode EP001 --from-stage upload --privacy private`
- TTS: ElevenLabs Pro ($99/mo) primary, OpenAI tts-1-hd fallback
- Voice: eleven_multilingual_v2, stability=0.32, style=0.55
- Video: news lower-third template (90px bar, GROUND ZERO red brand, segment title, date)
- Render modes: --skip-render (static dark, fast) | --local-render (Pexels B-roll or noise fallback)
- PEXELS_API_KEY: needs real key for B-roll (free at pexels.com/api)
- RUNPOD_POD_IP: not set — needed for Omniverse render mode

## Episode Format
5 segments: AI Headline | Technology Breakthrough | Global AI Activity Map | Infrastructure/Energy | Future Watch
Cold open: 3 hooks, 15 seconds. Total runtime ~6-8 min. Target: 160 wpm narration.

## Blocking Issues
- Omniverse render pipeline not yet connected (RUNPOD_POD_IP missing)
- Pexels API key not set (B-roll falls back to noise)

## Social Accounts Still Needed
TikTok | Instagram | X/Twitter | LinkedIn — all as @GroundZeroAI
Domain: groundzeroai.com (check availability)

## Notion Location
AI Daily Omniverse — Command Center: 31988f09-7e31-81a5-b33c-f57653d42863
Sub-pages: Production Toolkit | Omniverse Scene Design v1.0 | Asset Library
Databases: Story Pipeline | Episode Archive
