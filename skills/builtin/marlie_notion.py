"""
Built-in skill: marlie_notion

Sync the MARLIE I — Lafayette AI Factory project to the Notion workspace.
All content lives under the Mission Control HQ page.

=== PRODUCT ARCHITECTURE (critical — do not conflate) ===
MARLIE I  = permanent AI Factory at 1201 SE Evangeline Thruway, Lafayette LA.
            Building-based. NVL72 racks inside existing structure.
            HQ + NOC + primary compute. CDU liquid cooling. 4-layer power:
            L1=Nat gas gensets (PRIMARY) L2=Diesel (hurricane) L3=Solar+battery L4=LUS grid (last resort).
            This skill manages MARLIE I Notion content ONLY.

ADC 3K    = manufactured containerized pod product line. Deployed to remote sites.
            Immersion cooling (no HVAC). Networked back to MARLIE I.
            First deployment: Trappeys Cannery (metal warehouse, immersion pods).
            ADC 3K Notion content lives under ADC 3K — Project Command Center.
            Page ID: 31488f09-7e31-816d-9fdc-c6aabba4e3fa

=== ALL PROJECT Notion IDs ===
HQ root:           31288f09-7e31-81a5-bf43-e2af16379346
MARLIE I root:     31e88f09-7e31-8121-b4d2-d96b0084cc50
Trappeys root:     31288f09-7e31-80a2-8712-ef09878afd53
ADC 3K root:       31488f09-7e31-816d-9fdc-c6aabba4e3fa
KLFT 1.1:          31d88f09-7e31-80ec-b055-f69b9108355e
AI Omniverse:      31988f09-7e31-81a5-b33c-f57653d42863
MCHD Command Ctr:  31e88f09-7e31-8182-900a-cac36f525edc
Ground Zero CC:    31e88f09-7e31-81f9-b372-fbfb99c995ed
Site Acq Pipeline: 31e88f09-7e31-8136-9d4f-dbc128f55757
  Coteau LA:       31e88f09-7e31-8186-b2f2-eee7d2ef394c
  Airport Frontage:31e88f09-7e31-81fb-825a-f733cc0a93ae
  Pinhook Hotel:   31e88f09-7e31-81d2-bbde-f1400136190a
  Site Eval Frame: 31e88f09-7e31-8128-864e-d8f088c423a9

=== ADC 3K PRODUCT SPECS (confirmed March 2026) ===
Cooling fluid: Engineered Fluids EC-110 (single-phase immersion). NEVER reference 3M Novec — discontinued.
Remote ops: MARLIE I NOC manages all pods remotely. No on-site staff at remote sites.
Drone (KLFT): Skydio X10 + Skydio Dock ONLY. DJI removed — Countering CCP Drones Act risk.
KLFT pitch deck: `adc3k-deploy/skydio-deck.html` — 24 slides, LIVE at adc3k.com. Accessed via KLFT project card.

=== NOTION API PATTERNS ===
- Full tree query: paginated POST /search (pages + databases) → build parent map → print indented tree
- Append blocks: PATCH /blocks/{id}/children — use "after" param for insert position
- Update block:  PATCH /blocks/{id} with block type payload
- Delete block:  DELETE /blocks/{id}
- Table rows:    GET /blocks/{table_id}/children → each row is table_row block with "cells" list
- Update row:    PATCH /blocks/{row_id} {"table_row": {"cells": [[{rich_text}], ...]}}
- CAUTION: bulk text replace scripts mangle blocks referencing the search term. Use exact block ID targeting.
- Use get_blocks() not get_block_children() — method name in notion_util.py
- IDs in session summaries can be truncated — always search Notion to confirm before scripting
- Site Acquisition Pipeline: Type A=Full Factory(CDU), B=Pod(immersion), C=Mixed, D=EV/Drone only

=== Supported actions ===
  sync_full       — rebuild the entire MARLIE I workbook from scratch (all 9 sections)
  sync_section    — push a single named section (requires: section)
  get_status      — return URLs and IDs of all existing MARLIE I pages
  append_note     — append a quick note/update to the root MARLIE I page (requires: text)

Sections (for sync_section):
  thesis | hardware | site | funding | partners | credentials | vision | contact | financial

Credentials:
  Reads NOTION_API_KEY from env.  HQ page ID is hardcoded to the Mission Control HQ.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_NOTION_BASE = "https://api.notion.com/v1"
_NOTION_VERSION = "2022-06-28"
_TIMEOUT = 20.0
_HQ_PAGE_ID = "31288f09-7e31-81a5-bf43-e2af16379346"
_MARLIE_ROOT_TITLE = "MARLIE I — Lafayette AI Factory"


# ---------------------------------------------------------------------------
# Block helpers
# ---------------------------------------------------------------------------

def _h2(text: str) -> dict:
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def _h3(text: str) -> dict:
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def _para(text: str) -> dict:
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def _callout(text: str, emoji: str = "💡", color: str = "gray_background") -> dict:
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [{"type": "text", "text": {"content": text}}],
                        "icon": {"type": "emoji", "emoji": emoji},
                        "color": color}}


def _bullet(text: str, bold_prefix: str | None = None) -> dict:
    if bold_prefix:
        rich = [
            {"type": "text", "text": {"content": bold_prefix + ": "},
             "annotations": {"bold": True, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
            {"type": "text", "text": {"content": text},
             "annotations": {"bold": False, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
        ]
    else:
        rich = [{"type": "text", "text": {"content": text}}]
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich}}


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _quote(text: str) -> dict:
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text},
                                     "annotations": {"italic": True, "bold": False,
                                                     "strikethrough": False, "underline": False,
                                                     "code": False, "color": "default"}}]}}


# ---------------------------------------------------------------------------
# Section content definitions
# ---------------------------------------------------------------------------

def _root_blocks() -> list[dict]:
    return [
        _callout(
            "Louisiana's first next-generation AI factory — 1201 SE Evangeline Thruway, "
            "Lafayette LA 70501 — ADC3K / Scott Tomsu — CONFIDENTIAL INVESTOR DECK",
            emoji="⚡", color="yellow_background"
        ),
        _divider(),
        _h2("Project Status"),
        _bullet("Phase: Pre-deployment — investor & partner outreach active"),
        _bullet("Hardware: NVIDIA Vera Rubin NVL72 — Full Production — H2 2026 availability"),
        _bullet("Site: Owner-built, debt-free — $15K total property debt"),
        _bullet("Permits: Louisiana GC License active — build-ready"),
        _bullet("Certifications: 7 NVIDIA + FAA Private Pilot + Part 107 UAS"),
        _divider(),
        _h2("Workbook Sections"),
        _bullet("01 — Investment Thesis"),
        _bullet("02 — Hardware: NVIDIA Vera Rubin Platform"),
        _bullet("03 — Site & Building Specs"),
        _bullet("04 — Government Funding Stack"),
        _bullet("05 — Infrastructure Partners"),
        _bullet("06 — ADC3K Credentials"),
        _bullet("07 — Multi-Site Vision: Louisiana AI Network"),
        _bullet("08 — Contact & CTA"),
        _bullet("09 — Financial Architecture & ROI"),
    ]


def _thesis_blocks() -> list[dict]:
    return [
        _callout("The market is building for Blackwell. Marlie I is built for Rubin. That gap is the investment.",
                 emoji="💡", color="yellow_background"),
        _divider(),
        _h2("Thesis 01 — Skip Blackwell. Deploy Rubin."),
        _bullet("10x lower token cost vs Blackwell"),
        _bullet("4x fewer GPUs for equivalent training runs"),
        _bullet("22 TB/s memory bandwidth per GPU (HBM4)"),
        _bullet("3.6 ExaFLOPS NVFP4 inference per NVL72 rack"),
        _bullet("H2 2026 — full production — Texas factories 4 hours from Marlie I"),
        _divider(),
        _h2("Thesis 02 — Infrastructure Already Exists"),
        _bullet("Property debt: $15,000 total — owner-built, 20 years standing"),
        _bullet("LUS Fiber: ~0.8 miles — 214 Jefferson St"),
        _bullet("Atmos Energy (natural gas): ~3 miles — 1818 Eraste Landry Rd"),
        _bullet("Henry Hub gas benchmark: ~40 miles — Erath, LA"),
        _bullet("Lafayette Regional Airport (LFT): adjacent — Part 107 UAS"),
        _bullet("NVIDIA TX Manufacturing: ~4 hours — Foxconn Houston / Wistron Fort Worth"),
        _divider(),
        _h2("Thesis 03 — Federal & State Money Is Already Flowing"),
        _bullet("One Big Beautiful Bill Act (OBBBA): $500B toward domestic AI infrastructure"),
        _bullet("Louisiana Act 730: 20-year state/local sales & use tax rebate on AI factory equipment"),
        _bullet("BEAD Broadband Program: federal backhaul expansion — LUS Fiber path"),
        _bullet("Gulf OCS Revenue: $650M/year to Louisiana through 2034"),
        _bullet("Marlie I: 100% FEOC-clean, Texas-manufactured hardware, Louisiana GC — qualifies for all programs"),
        _divider(),
        _h2("Key Stats"),
        _bullet("10x — Lower token cost vs Blackwell"),
        _bullet("6 months — Estimated deploy timeline"),
        _bullet("$15K — Total property debt"),
        _bullet("20 years — Louisiana tax exemption on equipment"),
        _bullet("#1 — Louisiana industrial power rates in USA"),
    ]


def _hardware_blocks() -> list[dict]:
    return [
        _callout('Jensen Huang: "Rubin arrives at exactly the right moment... Rubin takes a giant leap toward the next frontier of AI."',
                 emoji="🤖", color="blue_background"),
        _callout('Sam Altman: "Intelligence scales with compute... The NVIDIA Rubin platform helps us keep scaling this progress."',
                 emoji="💬", color="gray_background"),
        _divider(),
        _h2("NVL72 Rack System"),
        _bullet("72 Rubin GPUs per rack"),
        _bullet("36 Vera CPUs per rack"),
        _bullet("3.6 ExaFLOPS NVFP4 inference per rack"),
        _bullet("100% liquid cooled — zero air cooling"),
        _bullet("NVLink 6 switch fabric — 3.6 TB/s GPU-to-GPU per rack"),
        _bullet("260 TB/s NVLink bandwidth across 14-rack DGX SuperPOD"),
        _bullet("50.4 ExaFLOPS per 14-rack SuperPOD"),
        _bullet("Ships fully integrated from Texas factory — 5-minute install (18x faster than prior gen)"),
        _divider(),
        _h2("Six-Chip Architecture"),
        _h3("1. Rubin GPU"),
        _bullet("288 GB HBM4 — 22 TB/s memory bandwidth — 72 per rack"),
        _h3("2. Vera CPU"),
        _bullet("88 custom Olympus cores — replaces x86 for AI workload orchestration — 36 per rack"),
        _h3("3. NVLink 6 Switch"),
        _bullet("3.6 TB/s GPU-to-GPU fabric per rack — 260 TB/s at SuperPOD scale"),
        _h3("4. ConnectX-9 SuperNIC"),
        _bullet("1.6 Tb/s aggregate per GPU — AI traffic with zero CPU involvement"),
        _h3("5. BlueField-4 DPU"),
        _bullet("Rack-scale confidential computing — unlocks healthcare, finance, government workloads"),
        _bullet("Encryption, firewall, storage I/O offloaded — GPU cycles reserved for inference"),
        _h3("6. Spectrum-X Ethernet"),
        _bullet("800G per port — co-packaged optics — AI east-west traffic at rack scale"),
        _divider(),
        _h2("5 Investor Facts"),
        _bullet("First rack-scale confidential computing — new market segments unlocked", "Fact 01"),
        _bullet("18x faster deployment — 5 min install vs 1.5 hours prior gen", "Fact 02"),
        _bullet("50.4 ExaFLOPS from 14 racks (DGX SuperPOD)", "Fact 03"),
        _bullet("260 TB/s NVLink bandwidth across full SuperPOD cluster", "Fact 04"),
        _bullet("Full production H2 2026 — 4 hours from Marlie I", "Fact 05"),
    ]


def _site_blocks() -> list[dict]:
    return [
        _callout("Scott Tomsu designed and built this building himself, 20 years ago. Multiple direct Gulf hurricane impacts — zero structural damage.",
                 emoji="🏗️", color="green_background"),
        _divider(),
        _h2("Address"),
        _para("1201 SE Evangeline Thruway, Lafayette, LA 70501 — ADC3K HQ"),
        _divider(),
        _h2("Building Dimensions"),
        _bullet("Exterior footprint: 24 ft x 40 ft"),
        _bullet("Interior Phase 1 floor: 22 ft x 35 ft — 770 sq ft"),
        _bullet("Second floor: available — Phase 2 vertical expansion"),
        _bullet("Adjacent property: owned — Phase 3 horizontal expansion"),
        _divider(),
        _h2("Ceiling & Structure"),
        _bullet("Plate height: 7 ft 11 in to bottom of ceiling assembly (measured)"),
        _bullet("Framing: 2x12"),
        _bullet("Ceiling assembly: two layers 5/8\" Type X sheetrock + insulation + full floor above"),
        _bullet("Fire rating: UL-rated assembly — built-in from day one"),
        _bullet("Insulation: heavy throughout — complete thermal shell — optimal for liquid cooling stability"),
        _bullet("Foundation: reinforced concrete slab"),
        _divider(),
        _h2("Phase 1 Floor Plan — Rack Layout (Concept)"),
        _bullet("Configuration: hot aisle / cold aisle containment"),
        _bullet("Row A: 8x NVL72 racks"),
        _bullet("Sealed hot aisle: CDU units at each end — liquid heat rejection to exterior dry coolers"),
        _bullet("Row B: 8x NVL72 racks"),
        _bullet("Cold supply plenums above and below rack rows"),
        _bullet("Network core / fiber MDA / CDU control — compact zone near entry"),
        _bullet("ALL mechanical exterior: gas generators, dry coolers, UPS batteries, security monitoring"),
        _bullet("Max Phase 1 capacity: 16 NVL72 racks = 57.6 ExaFLOPS"),
        _divider(),
        _h2("Site Specs"),
        _bullet("FEMA Zone: Zone X — Minimal Flood Hazard"),
        _bullet("Ground elevation: high ground — above regional base flood elevation"),
        _bullet("Zoning: Industrial — heavy use permitted"),
        _bullet("Property debt: $15,000 total"),
        _bullet("Storm history: multiple direct hurricanes — zero structural damage"),
        _bullet("GC Permits: Louisiana GC License — active"),
        _bullet("NVIDIA Certs: 7 active certifications"),
        _bullet("FAA Certs: Private Pilot + Part 107 UAS"),
        _divider(),
        _h2("Infrastructure Proximity"),
        _bullet("LUS Fiber: ~0.8 mi — 214 Jefferson St"),
        _bullet("LUS Power / Utilities: ~1 mi — 1314 Walker Rd"),
        _bullet("Atmos Energy: ~3 mi — 1818 Eraste Landry Rd"),
        _bullet("SLEMCO Electric: 2727 SE Evangeline Thruway"),
        _bullet("LFT Airport: adjacent — GPS 30.20529, -91.98760"),
        _bullet("Henry Hub: ~40 mi — Erath, LA"),
        _bullet("NVIDIA TX Manufacturing: ~4 hrs — Foxconn Houston / Wistron Fort Worth"),
    ]


def _funding_blocks() -> list[dict]:
    return [
        _callout("Marlie I was designed around the incentives — not retrofitted to qualify.",
                 emoji="🏛️", color="blue_background"),
        _divider(),
        _h2("Federal: One Big Beautiful Bill Act (OBBBA)"),
        _bullet("Signed July 4, 2025"),
        _bullet("FEOC restrictions: Chinese/Russian/Iranian/North Korean supply chain = disqualified"),
        _bullet("Marlie I: Texas-manufactured NVIDIA hardware, 100% US ownership, Louisiana GC — fully compliant"),
        _bullet("$500M added to BEAD broadband program"),
        _bullet("Gulf OCS revenue raised to $650M/year through 2034"),
        _bullet("$500B Stargate AI program — Marlie I FEOC-clean structure qualifies"),
        _divider(),
        _h2("Federal: BEAD Broadband Program"),
        _bullet("LUS Fiber ~0.8 miles from site"),
        _bullet("Marlie I connection accelerates BEAD eligibility for City of Lafayette"),
        _divider(),
        _h2("State: Louisiana Act 730"),
        _bullet("Effective July 1, 2024"),
        _bullet("20-year state/local sales & use tax rebate on qualifying AI factory equipment"),
        _bullet("10-year renewal option (30 years total)"),
        _bullet("Qualification: $200M+ capital investment + 50+ permanent jobs"),
        _bullet("Direct Payment Number eliminates tax liability on GPU hardware"),
        _bullet("Stackable: Quality Jobs Program (6% payroll rebate, 10yr) + LED FastStart (free workforce training)"),
        _callout("100% US ownership. Texas-manufactured NVIDIA hardware. Louisiana-licensed GC. Zero foreign entity involvement. Marlie I is not just eligible — it is the ideal candidate.",
                 emoji="✅", color="green_background"),
    ]


def _partners_blocks() -> list[dict]:
    return [
        _callout("Every infrastructure partner is not a vendor. They are a node in the same network.",
                 emoji="🔗", color="yellow_background"),
        _divider(),
        _h2("LUS Fiber"),
        _bullet("214 Jefferson St, Lafayette, LA 70501 — ~0.8 miles from Marlie I"),
        _bullet("Municipal gigabit network — city-owned, no incumbent telco gatekeeping"),
        _bullet("What LUS Fiber gains: anchor industrial fiber customer + BEAD backhaul justification for SE Evangeline corridor"),
        _divider(),
        _h2("LUS Power / Utilities"),
        _bullet("1314 Walker Rd, Lafayette, LA 70506 — ~1 mile"),
        _bullet("Marlie I is off-grid by design (natural gas primary). LUS Power = backup / grid-feed relationship"),
        _bullet("Excess generation feeds back to LUS grid — creates revenue stream + strengthens utility relationship"),
        _divider(),
        _h2("Atmos Energy — Natural Gas"),
        _bullet("1818 Eraste Landry Rd, Lafayette, LA 70506 — ~3 miles"),
        _bullet("Primary fuel supplier for on-site generation — NOT backup power"),
        _bullet("Henry Hub benchmark (Erath, LA, ~40 mi) — fuel costs locked to most competitive gas price on earth"),
        _bullet("What Atmos gains: long-term industrial contract, high-volume predictable load, rate stability"),
        _divider(),
        _h2("SLEMCO Electric"),
        _bullet("2727 SE Evangeline Thruway — same corridor as Marlie I"),
        _bullet("Secondary electric relationship"),
        _divider(),
        _h2("Lafayette Regional Airport (LFT)"),
        _bullet("GPS: 30.20529, -91.98760 — adjacent to Marlie I site"),
        _bullet("ADC3K: FAA Private Pilot Certificate + Part 107 Remote Pilot Certificate"),
        _bullet("Commercial UAS operations: inspection, survey, logistics from day one"),
        _bullet("What LFT gains: active commercial Part 107 operator on the doorstep"),
        _divider(),
        _h2("City of Lafayette / Louisiana Economic Development (LED)"),
        _bullet("Act 730 qualified — 20-year equipment tax exemption"),
        _bullet("OBBBA compliant — FEOC-clean, Texas-manufactured, Louisiana GC"),
        _bullet("50+ permanent jobs required for Act 730 certification"),
        _bullet("Lafayette becomes home to Louisiana's first Rubin-class AI factory"),
        _bullet("Hub of ADC3K Louisiana AI Network — three sites planned"),
    ]


def _credentials_blocks() -> list[dict]:
    return [
        _callout("Scott Tomsu — Owner/Operator — ADC3K (Advantage Design Construction) — Lafayette, LA",
                 emoji="🎓", color="gray_background"),
        _divider(),
        _h2("Certifications"),
        _bullet("Louisiana General Contractor License — active — eliminates 10-15% GC markup, single accountability"),
        _bullet("7 NVIDIA Certifications — AI infrastructure design, GPU compute deployment, NVIDIA partner program"),
        _bullet("FAA Private Pilot Certificate"),
        _bullet("FAA Part 107 Remote Pilot Certificate (commercial UAS)"),
        _bullet("CompTIA A+ — earned late 1990s"),
        _bullet("CompTIA Network+ — earned late 1990s"),
        _divider(),
        _h2("Background"),
        _bullet("20 years underwater robotics / ROV — Gulf of America oil and gas industry"),
        _bullet("Systems at depth, under pressure, hostile environments — zero tolerance for failure"),
        _bullet("AI factory ops demand the same: continuous uptime, redundant systems, immediate fault response"),
        _bullet("Built 1201 SE Evangeline Thruway himself — 20 years standing, hurricane-proven"),
        _divider(),
        _h2("Why This Matters"),
        _bullet("No third-party GC — Scott pulls permits, hires trades, executes buildout directly"),
        _bullet("No third-party NVIDIA integrator — 7 certifications = receive, rack, power on"),
        _bullet("Revenue from day one — no markup, no delay, no middlemen"),
        _bullet("Field-hardened systems thinking — not finance, not software — infrastructure operations"),
    ]


def _vision_blocks() -> list[dict]:
    return [
        _callout("We are not building a data center. We are building a network.",
                 emoji="🌐", color="yellow_background"),
        _divider(),
        _h2("Phase 1 — MARLIE I (Active)"),
        _bullet("Location: 1201 SE Evangeline Thruway, Lafayette, LA 70501"),
        _bullet("Target: H2 2026 operational"),
        _bullet("Floor: 22x35 ft Phase 1 + second floor available + adjacent property owned"),
        _bullet("Purpose: home base — cash flow, credibility, playbook for Phases 2 and 3"),
        _callout("Activation: NOW — investor and infrastructure partner outreach active", emoji="🟢", color="green_background"),
        _divider(),
        _h2("Phase 2 — Site Two (In Development)"),
        _bullet("Location: TBD — ADC3K Louisiana Network"),
        _bullet("Funded by Marlie I cash flow — no external fundraising required"),
        _bullet("Playbook: written. Infrastructure relationships: established. Hardware: understood."),
        _callout("Activation trigger: Marlie I reaches revenue threshold -> Site Two deploys", emoji="🟡", color="yellow_background"),
        _divider(),
        _h2("Phase 3 — Site Three (In Development)"),
        _bullet("Location: TBD — ADC3K Louisiana Network"),
        _bullet("Completes hub-and-spoke Louisiana AI architecture"),
        _bullet("Combined: enterprise + government + city infrastructure at statewide scale"),
        _bullet("Three sites. One network. One operator."),
        _callout("Activation trigger: Site Two operational -> Site Three deploys", emoji="⚫", color="gray_background"),
        _divider(),
        _h2("Partner Gains Across the Full Network"),
        _bullet("Anchor industrial fiber customer + BEAD backhaul justification", "LUS FIBER"),
        _bullet("Long-term industrial gas contract — high-volume predictable load", "ATMOS GAS"),
        _bullet("Active Part 107 commercial UAS on the doorstep", "LFT AIRPORT"),
        _bullet("Louisiana's first Rubin-class AI factory — Act 730, OBBBA, 50+ jobs, Lafayette on national map", "CITY / LED"),
        _divider(),
        _quote("ADC3K is not asking the city for a favor. ADC3K is inviting Lafayette's infrastructure partners to build the city's next chapter with us. Every site we add is another node in Lafayette's economic future."),
    ]


def _financial_blocks() -> list[dict]:
    return [
        _callout(
            "This is not a data center. This is a money machine. "
            "Every watt generates revenue. Every dollar goes to compute. The comparison is not close.",
            emoji="💰", color="yellow_background"
        ),
        _divider(),
        _h2("Capital Stack"),
        _bullet("Infrastructure raise: ~$1.17M — covers facility buildout (electrical, cooling, fiber, power distribution, commissioning)"),
        _bullet("GPU hardware financed separately: equipment financing + NVIDIA Capital programs + SBA facilities"),
        _bullet("EBITDA figures below = facility-level operating cash flow"),
        _bullet("Full investor pro forma with hardware financing and debt service available upon request"),
        _divider(),
        _h2("MARLIE I vs Legacy Data Center — Key Comparison"),
        _bullet("PUE: Legacy 1.4–1.8 (40–80% wasted) vs MARLIE I 1.10 (liquid-cooled, best-in-class)"),
        _bullet("Energy cost: Legacy $0.10–$0.18/kWh national avg vs MARLIE I $0.065/kWh Louisiana industrial"),
        _bullet("Cooling: Legacy air (CRAC units, chillers) vs MARLIE I 100% direct-to-chip liquid"),
        _bullet("Revenue per rack per year: Legacy $200K–$500K (colo) vs MARLIE I $3M–$5M+ (AI compute)"),
        _bullet("Operations: Legacy 20–50 FTE manual ops vs MARLIE I 3–5 FTE Mission Control AI"),
        _bullet("On-site generation: Legacy none (grid dependent) vs MARLIE I Bloom Energy fuel cells + gas generators"),
        _bullet("Domestic content: Legacy mixed overseas vs MARLIE I 100% USA — OBBBA compliant"),
        _divider(),
        _h2("Revenue Model — AI Compute Rental (Conservative Basis)"),
        _bullet("Rate basis: $6/GPU/hr conservative (H100 market: $2.50–$3.50). Vera Rubin 2.5x FP4 density — premium tier justified"),
        _bullet("At $8/GPU/hr mid estimate, Year 3 two-floor gross reaches $121.5M. OPEX stays flat. Upside is asymmetric."),
        _h3("Year 1 — 4 Racks Live, 40% Utilization"),
        _bullet("288 GPUs online (Floor 1 ramp)"),
        _bullet("Gross revenue: $6.1M"),
        _bullet("OPEX: ~$1.29M (4-rack scale)"),
        _bullet("EBITDA: ~$4.78M"),
        _h3("Year 2 — 8 Racks Live, 65% Utilization"),
        _bullet("1,728 GPUs online (24 racks — Floor 1 full + Floor 2 partial)"),
        _bullet("Gross revenue: $44.5M"),
        _bullet("OPEX: ~$3.0M (24-rack scale)"),
        _bullet("EBITDA: ~$41.5M"),
        _h3("Year 3 — 16 Racks Live, 75% Utilization"),
        _bullet("2,304 GPUs online (32 racks — both floors full)"),
        _bullet("Gross revenue: $91.1M"),
        _bullet("OPEX: ~$3.68M (full two-floor scale)"),
        _bullet("EBITDA: ~$87.4M"),
        _divider(),
        _h2("Power Resilience — 4-Layer Stack (Off-Grid by Design)"),
        _bullet("Layer 1 — Nat Gas Gensets (PRIMARY): prime-rated, 24/7 continuous. Two units N+1. Henry Hub pricing (~40 mi) = lowest fuel cost in country. No grid rate exposure, no demand charges."),
        _bullet("Layer 2 — Diesel Gensets (Hurricane Backup): on-site fuel = pipeline-independent. Hurricane Ida proved nat gas pipelines can fail for weeks. Diesel carries load regardless of gas supply."),
        _bullet("Layer 3 — Solar + Battery (Supplement): 300 kW solar offsets ~3.4% of daily load. 600 kWh LFP battery = instant ATS bridge during any switchover. Reduces genset fuel burn during daylight."),
        _bullet("Layer 4 — LUS Grid (Last Resort): backup only. Never primary. Eliminates grid rate exposure, demand charge risk, and utility reliability dependency."),
        _bullet("Off-grid by design: Nat gas + diesel + solar/battery = fully islanded microgrid. Grid is insurance, not a dependency."),
        _divider(),
        _h2("Investor Benefits"),
        _bullet("Reserved bandwidth: GPU compute access during off-peak hours proportional to investment tier. Estimated value: $50K–$500K/month compute credit."),
        _bullet("Early mover rate lock: investors before first rack goes live receive locked GPU rental rates below market for 24 months"),
        _bullet("Ring Power dealer relationship: single service contract covers entire Cat generator fleet (nat gas + diesel)"),
    ]


def _contact_blocks() -> list[dict]:
    return [
        _h2("ADC3K — Advantage Design Construction"),
        _bullet("Owner/Operator: Scott Tomsu"),
        _bullet("Address: 1201 SE Evangeline Thruway, Lafayette, LA 70501"),
        _bullet("Email: SCOTT@ADC3K.COM"),
        _bullet("Phone: 337-780-1535"),
        _bullet("Web: www.adc3k.com"),
        _divider(),
        _h2("Next Steps"),
        _bullet("Infrastructure partner meetings: LUS Fiber, Atmos Energy, LUS Power, LFT Airport"),
        _bullet("Louisiana Economic Development — Act 730 pre-qualification"),
        _bullet("NVIDIA partner program — NVL72 procurement pipeline"),
        _bullet("Investor term sheet discussions"),
        _bullet("Phase 1 buildout kickoff — 6 month deploy timeline"),
        _divider(),
        _callout("The federal money is flowing. The hardware is in production. The site is ready. The only question is who is at the table when Marlie I goes live.",
                 emoji="⚡", color="yellow_background"),
    ]


_SECTIONS: dict[str, dict] = {
    "thesis":      {"title": "01 — Investment Thesis",                    "icon": "💡", "blocks": _thesis_blocks},
    "hardware":    {"title": "02 — Hardware: NVIDIA Vera Rubin Platform", "icon": "🤖", "blocks": _hardware_blocks},
    "site":        {"title": "03 — Site & Building Specs",                "icon": "🏗️", "blocks": _site_blocks},
    "funding":     {"title": "04 — Government Funding Stack",             "icon": "🏛️", "blocks": _funding_blocks},
    "partners":    {"title": "05 — Infrastructure Partners",              "icon": "🔗", "blocks": _partners_blocks},
    "credentials": {"title": "06 — ADC3K Credentials",                   "icon": "🎓", "blocks": _credentials_blocks},
    "vision":      {"title": "07 — Louisiana AI Network: Multi-Site Vision", "icon": "🌐", "blocks": _vision_blocks},
    "contact":     {"title": "08 — Contact & Next Steps",                "icon": "📞", "blocks": _contact_blocks},
    "financial":   {"title": "09 — Financial Architecture & ROI",        "icon": "💰", "blocks": _financial_blocks},
}


# ---------------------------------------------------------------------------
# Skill class
# ---------------------------------------------------------------------------

class MarlieNotionSkill(BaseSkill):
    name = "marlie_notion"
    description = (
        "Sync the MARLIE I Lafayette AI Factory project to the Notion workspace. "
        "Can rebuild the full workbook (sync_full), push a single section (sync_section), "
        "check workbook status (get_status), or append a quick note (append_note)."
    )
    version = "1.0.0"
    required_secrets = ["NOTION_API_KEY"]

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "sync_full")
        api_key = os.environ.get("NOTION_API_KEY", "")
        if not api_key:
            return SkillResult.fail("NOTION_API_KEY not set in environment")

        client = _NotionClient(api_key)

        if action == "sync_full":
            return await self._sync_full(client)
        elif action == "sync_section":
            section = params.get("section", "")
            if section not in _SECTIONS:
                return SkillResult.fail(f"Unknown section '{section}'. Valid: {', '.join(_SECTIONS)}")
            return await self._sync_section(client, section)
        elif action == "get_status":
            return await self._get_status(client)
        elif action == "append_note":
            text = params.get("text", "")
            if not text:
                return SkillResult.fail("Missing required parameter: text")
            return await self._append_note(client, text)
        else:
            return SkillResult.fail(f"Unknown action '{action}'. Valid: sync_full, sync_section, get_status, append_note")

    async def _sync_full(self, client: "_NotionClient") -> SkillResult:
        """Create or recreate the entire MARLIE I workbook."""
        try:
            # Create root page
            root = await client.create_page(
                parent_id=_HQ_PAGE_ID,
                title=_MARLIE_ROOT_TITLE,
                icon="⚡",
                children=_root_blocks()[:100],
            )
            root_id = root["id"]
            root_url = root["url"]
            created = {"root": root_url}

            # Create each section as a child page
            for key, meta in _SECTIONS.items():
                blocks = meta["blocks"]()
                page = await client.create_page(
                    parent_id=root_id,
                    title=meta["title"],
                    icon=meta["icon"],
                )
                await client.append_blocks(page["id"], blocks)
                created[key] = page["url"]
                logger.info("Created section: %s", meta["title"])

            return SkillResult.ok(
                f"MARLIE I workbook created — {len(created)} pages",
                data={"pages": created, "root_url": root_url}
            )
        except Exception as exc:
            logger.exception("sync_full failed")
            return SkillResult.fail(str(exc))

    async def _sync_section(self, client: "_NotionClient", section: str) -> SkillResult:
        """Push a single section as a standalone page under HQ."""
        try:
            meta = _SECTIONS[section]
            blocks = meta["blocks"]()
            page = await client.create_page(
                parent_id=_HQ_PAGE_ID,
                title=f"[UPDATE] {meta['title']}",
                icon=meta["icon"],
            )
            await client.append_blocks(page["id"], blocks)
            return SkillResult.ok(
                f"Section '{section}' synced to Notion",
                data={"url": page["url"], "section": section}
            )
        except Exception as exc:
            logger.exception("sync_section failed")
            return SkillResult.fail(str(exc))

    async def _get_status(self, client: "_NotionClient") -> SkillResult:
        """Search for the MARLIE I root page and return its URL."""
        try:
            results = await client.search(_MARLIE_ROOT_TITLE)
            pages = [{"title": r.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", "?"),
                      "url": r.get("url", ""),
                      "id": r.get("id", "")}
                     for r in results.get("results", [])
                     if r.get("object") == "page"]
            return SkillResult.ok(f"Found {len(pages)} MARLIE I page(s) in Notion", data={"pages": pages})
        except Exception as exc:
            logger.exception("get_status failed")
            return SkillResult.fail(str(exc))

    async def _append_note(self, client: "_NotionClient", text: str) -> SkillResult:
        """Append a timestamped note to the MARLIE I root page."""
        try:
            # Find root page
            results = await client.search(_MARLIE_ROOT_TITLE)
            pages = [r for r in results.get("results", []) if r.get("object") == "page"]
            if not pages:
                return SkillResult.fail("MARLIE I root page not found in Notion. Run sync_full first.")
            page_id = pages[0]["id"]
            await client.append_blocks(page_id, [
                _divider(),
                _callout(text, emoji="📝", color="gray_background"),
            ])
            return SkillResult.ok("Note appended to MARLIE I Notion page", data={"page_url": pages[0]["url"]})
        except Exception as exc:
            logger.exception("append_note failed")
            return SkillResult.fail(str(exc))


# ---------------------------------------------------------------------------
# Notion HTTP client
# ---------------------------------------------------------------------------

class _NotionClient:
    def __init__(self, api_key: str):
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": _NOTION_VERSION,
            "Content-Type": "application/json",
        }

    async def _request(self, method: str, path: str, data: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as http:
            r = await http.request(method, f"{_NOTION_BASE}{path}", headers=self._headers, json=data)
            r.raise_for_status()
            return r.json()

    async def create_page(self, parent_id: str, title: str, icon: str, children: list | None = None) -> dict:
        payload: dict[str, Any] = {
            "parent": {"page_id": parent_id},
            "icon": {"type": "emoji", "emoji": icon},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
        if children:
            payload["children"] = children[:100]
        return await self._request("POST", "/pages", payload)

    async def append_blocks(self, page_id: str, blocks: list) -> None:
        for i in range(0, len(blocks), 95):
            await self._request("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+95]})

    async def search(self, query: str) -> dict:
        return await self._request("POST", "/search", {"query": query, "filter": {"value": "page", "property": "object"}})
