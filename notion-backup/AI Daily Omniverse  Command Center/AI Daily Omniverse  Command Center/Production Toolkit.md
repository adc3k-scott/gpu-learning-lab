# 📋 Production Toolkit
*Notion backup — 2026-04-06*

Daily operations reference. Everything you need to produce an episode in one place.
> 📘 NEW: Mission Control Playbook v1.0 — The definitive daily execution system has been built (March 4, Session 2). It supersedes the manual checklist below with an automated workflow: Scott triggers → Mission Control (Claude) searches, curates, writes, and delivers a complete manifest + script package in one session. See the downloaded AIDO_Mission_Control_Playbook.docx for the full system including 4 trigger modes, story selection framework, script format spec with fixed transition phrases, 10 quality gates, and 6 revenue streams.
> 
> 📄 Content Manifest Schema v1.0 — The JSON contract between editorial and render pipeline is finalized. See AIDO_Content_Manifest_Schema.json. Every episode manifest includes: meta, voice config, 5 segments (narration + visuals + overlays + sources), global map with pins, scrolling ticker, render config, and YouTube metadata.
> 
> 🎙️ TTS Decision: ElevenLabs Pro ($99/mo) primary, OpenAI tts-1-hd fallback. See AIDO_TTS_Provider_Evaluation.docx for the full scored comparison.
---
## 📝 Script Template
Every episode follows this structure. Copy and fill in daily.
```javascript
# AI DAILY OMNIVERSE — EPISODE [###]
## Situation Report: [Date]

## COLD OPEN (15 seconds)
[3 hooks from today's stories]

## SEGMENT 1 — AI HEADLINE OF THE DAY (1–2 min)
### [Headline]
[Visual cues in brackets]
[Narration — ~250 words]
[Source citation]

## SEGMENT 2 — TECHNOLOGY BREAKTHROUGH (1–2 min)
### [Headline]
[Narration — ~250 words]

## SEGMENT 3 — GLOBAL AI ACTIVITY MAP (30–60 sec)
### Where AI Is Moving Today
[5 location markers with 1-sentence descriptions]

## SEGMENT 4 — AI INFRASTRUCTURE WATCH (~1 min)
### [Headline]
[Narration — ~150 words]

## SEGMENT 5 — FUTURE WATCH (30–60 sec)
### [Headline]
[Narration — ~120 words]

## SIGN-OFF (15 seconds)
[Recap + tomorrow preview]
```
---
## ✅ Daily Production Checklist
### Pre-Production
- [ ] Scan Tier 1 sources for overnight developments
- [ ] Identify top 5 stories across all categories
- [ ] Rank by impact: CRITICAL / HIGH / MEDIUM
- [ ] Confirm at least one story per segment
- [ ] Check for continuing stories from previous episodes
### Script
- [ ] Write cold open with day’s top 3 hooks
- [ ] Draft all 5 segments
- [ ] Include visual cues in brackets
- [ ] Add source citations to every claim
- [ ] Write sign-off with forward preview
- [ ] Read aloud for pacing — target 160 wpm
### Visuals
- [ ] Update dashboard with today’s stories and metrics
- [ ] Generate or source segment visuals
- [ ] Update Global Activity Map locations
- [ ] Update Sector Signals sidebar
- [ ] Update Tomorrow’s Watch
### Post-Production
- [ ] Record voiceover or generate AI narration
- [ ] Assemble: visuals + voiceover + transitions
- [ ] Review final cut for accuracy and pacing
- [ ] Export at 1080p minimum
### Publishing
- [ ] Upload to YouTube (SEO title, description, tags)
- [ ] Post highlight clip to X/Twitter
- [ ] Update website archive
- [ ] Log episode in Episode Archive database
---
## 🎥 YouTube Publishing Template
Title Format: AI Daily Omniverse EP[###] — [Headline Hook] | [Date]
Description:
Today’s AI Situation Report covers: [1-sentence per story]. Sources and timestamps below.
[Timestamps]
00:00 — Cold Open
00:15 — AI Headline: [title]
02:15 — Tech Breakthrough: [title]
04:15 — Global AI Map
05:00 — Infrastructure Watch: [title]
06:00 — Future Watch: [title]
06:45 — Sign-Off
[Source links]
Tags: AI news, artificial intelligence, AI daily, GPU technology, data centers, AI infrastructure, NVIDIA, machine learning, AI report, tech news today
---
## 📊 Story Selection Criteria
| Criteria | Include | Skip | Impact | Changes how AI is built, deployed, regulated, or funded at scale | Minor product updates, incremental benchmarks |
| Novelty | First of its kind or signals a trend shift | Expected updates on known timelines | Audience | Explainable with context in under 90 seconds | Requires 10+ minutes of background |
| Visual | Can be illustrated with maps, diagrams, or charts | Pure text-based policy analysis | Urgency | Happened in the last 24 hours | Older than 48 hours |
---
## 🎤 Voiceover Notes
Pace: 160 words per minute (broadcast standard)
Tone: Mission-control briefing — authoritative, concise, forward-looking. Not a podcast, not a lecture.
Style: Short declarative sentences. Active voice. Numbers spoken naturally ("four billion dollars" not "$4B"). Technical terms explained on first use.
---
## 📌 Quality Standards
Accuracy: Every factual claim cites a primary source.
Neutrality: Report developments factually. Multiple perspectives on policy stories.
Timeliness: Stories from the last 24 hours. Exceptions only for developing multi-day stories.
Clarity: Motivated non-expert can follow. Use analogies and visuals.
Brevity: Each segment delivers its core message in 60–90 seconds. Max 8 minutes total.
Consistency: Same segment order, visual template, and narration style every episode.