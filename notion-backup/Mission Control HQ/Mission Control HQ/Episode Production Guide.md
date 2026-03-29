# Episode Production Guide
*Notion backup — 2026-03-28*

# Episode Production Guide
> Standard process for producing a Ground Zero AI news episode end-to-end.
---
## Episode Format
- Style: AI news show — lower-third news template
- Audio: ElevenLabs eleven_multilingual_v2, stability=0.32, style=0.55
- 6 audio segments per episode
- B-roll: Pexels API (requires PEXELS_API_KEY)
- Render: local or RunPod Omniverse (requires RUNPOD_POD_IP)
---
## Production Workflow
- 1. Story selected and added to Story Pipeline database
- 2. Manifest written (episode metadata, script, segment timing)
- 3. TTS generated: python -m aido.tts_generate --episode EP00X
- 4. B-roll injected: python -m aido.inject_content --episode EP00X
- 5. Episode rendered: python -m aido.pipeline --episode EP00X --local-render
- 6. Review and approve
- 7. Upload: python -m aido.pipeline --episode EP00X --from-stage upload --privacy private
---
## Environment Variables Required
- ANTHROPIC_API_KEY — script generation
- ELEVENLABS_API_KEY — TTS audio
- PEXELS_API_KEY — B-roll footage (NOT YET SET)
- RUNPOD_POD_IP — Omniverse render mode (NOT YET SET)
- youtube_token.json — OAuth token in project root
---
## Open Blockers
> PEXELS_API_KEY not set — B-roll falls back to noise. Get key at pexels.com/api.
> RUNPOD_POD_IP not set — Omniverse render blocked. Use --local-render as workaround.