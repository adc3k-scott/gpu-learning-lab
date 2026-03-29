# 🎨 Asset Library
*Notion backup — 2026-03-28*

Visual assets, templates, and branding references for the AI Daily Omniverse.
---
## 🖥️ Dashboard Template
File: AI_Daily_Omniverse_Dashboard.jsx
Type: React component — mission-control style dark UI
Status: ✅ Built — Phase 1 ready
Features:
- Real-time clock (UTC)
- Scrolling news ticker
- 5 interactive story cards with segment color coding
- Global Activity Map with pulsing location markers
- Sector Signals sidebar
- Tomorrow’s Watch panel
- Key metrics row (stories tracked, capital deployed, threat level, launches)
- Status bar with scanning animation
How to update daily: Replace the STORIES, GLOBAL_ACTIVITY, and TICKER_ITEMS arrays with today’s data. The dashboard re-renders automatically.
---
## 🎨 Branding Guide
Color Palette:
- Background: #06080d (near-black)
- Primary accent: #00f0ff (cyan)
- Headline segment: #00f0ff (cyan)
- Breakthrough segment: #ff3366 (hot pink)
- Infrastructure segment: #ffaa00 (gold)
- Global Map segment: #00ff88 (green)
- Future Watch segment: #bf5af2 (purple)
Typography:
- Headlines: Chakra Petch (bold)
- Monospace/labels: Share Tech Mono
- Body text: IBM Plex Sans
Visual Tone: Futuristic command center. Dark backgrounds. Glowing accent colors. Grid lines and scanline effects. Clean data visualization. No clutter.
Impact Badges:
- CRITICAL = red border
- HIGH = gold border
- MEDIUM = green border
---
## 🖼️ Segment Visual Templates
| Segment | Visual Type | Notes |
| Headline | Full-width story card + metric overlay | Largest visual, most screen time |
| Breakthrough | Diagram or architecture exploded view | Technical illustration |
| Global Map | Animated world map with location pulses | 3–5 markers per episode |
| Infrastructure | Satellite overlay or facility diagram | Data center / GPU cluster focus |
| Future Watch | Abstract or experimental visual | Most creative freedom |
---
## 📹 Video Specs
Resolution: 1920×1080 minimum (4K preferred for future-proofing)
Frame rate: 30fps
Aspect ratio: 16:9
Export format: H.264 / MP4
Thumbnail: 1280×720, dashboard visual with headline overlay, high contrast text
---
## 📁 File Naming Convention
AIDO_EP[###]_[YYYY-MM-DD]_[descriptor].[ext]
Examples:
- AIDO_EP001_2026-03-04_script.md
- AIDO_EP001_2026-03-04_dashboard.jsx
- AIDO_EP001_2026-03-04_final.mp4
- AIDO_EP001_2026-03-04_thumbnail.png