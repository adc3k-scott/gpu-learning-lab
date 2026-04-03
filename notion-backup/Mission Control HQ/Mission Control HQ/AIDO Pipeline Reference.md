# AIDO Pipeline Reference
*Notion backup — 2026-04-03*

# AIDO Pipeline Reference
AI Daily Omniverse pipeline modules — located in aido/ directory of gpu-learning-lab repo.
---
## Pipeline Modules
- manifest_schema — episode manifest validation
- tts_generate — ElevenLabs TTS audio generation
- inject_content — B-roll and asset injection
- render_episode — Omniverse scene render
- assemble — combine audio, video, lower-thirds
- render_local — local render fallback (no RunPod)
- upload_youtube — YouTube OAuth upload
- pipeline — full orchestrator, runs all stages
---
## TTS Settings (EP001 reference)
- Model: eleven_multilingual_v2
- Stability: 0.32
- Style: 0.55
- 6 segments per episode
---
## YouTube OAuth
- Token file: youtube_token.json in project root
- Google account: dedicated business account
- Chrome profile: dedicated Ground Zero profile
- Handle: @GroundZero-ai
---
## Common Commands
Full render from scratch: python -m aido.pipeline --episode EP002 --local-render
Upload only: python -m aido.pipeline --episode EP002 --from-stage upload --privacy private
TTS only: python -m aido.tts_generate --episode EP002