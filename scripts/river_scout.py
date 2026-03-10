"""
ADC 3K — River + Pipeline Site Scout Agent
============================================
Searches for industrial/agricultural land near BOTH Louisiana gas pipelines
AND the Atchafalaya River or Mississippi River. River water = natural heat sink
for cooling, pipeline = fuel source. Double cost advantage.

Run:
    python scripts/river_scout.py
    python scripts/river_scout.py --corridors "Atchafalaya Basin" "Mississippi River"
    python scripts/river_scout.py --max-sites 8 --output data/river_sites.json

Output:
    data/river_sites.json  — importable into site-intel.html
    data/river_sites.csv   — spreadsheet version
"""
import sys, os, json, csv, time, argparse, math
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import anthropic
from datetime import datetime, timezone
from agents.site_scout.fema import get_flood_zone
from agents.site_scout.scorer import haversine_miles

# ─────────────────────────────────────────────────────────────────────────────
# RIVER REFERENCE POINTS — sampled coordinates along each waterway
# Used to calculate distance-to-river for scoring
# ─────────────────────────────────────────────────────────────────────────────
RIVERS = {
    "Atchafalaya": [
        (30.833, -91.690),   # Simmesport / Old River Control
        (30.720, -91.700),   # Melville
        (30.537, -91.752),   # Krotz Springs
        (30.410, -91.755),   # Arnaudville area
        (30.293, -91.795),   # Henderson / Atchafalaya Basin Bridge
        (30.210, -91.830),   # Breaux Bridge area
        (30.050, -91.820),   # St. Martinville area
        (29.950, -91.650),   # Charenton / Jeanerette
        (29.870, -91.530),   # Franklin
        (29.693, -91.210),   # Morgan City
        (29.580, -91.170),   # Berwick / Lower Atchafalaya
    ],
    "Mississippi": [
        (30.990, -91.520),   # Angola / Tunica Hills
        (30.815, -91.480),   # St. Francisville
        (30.595, -91.280),   # Port Hudson
        (30.450, -91.190),   # Baton Rouge
        (30.350, -91.100),   # Port Allen
        (30.200, -91.020),   # Plaquemine
        (30.100, -90.940),   # Donaldsonville
        (30.030, -90.830),   # Convent
        (29.940, -90.760),   # Gramercy / Lutcher
        (29.860, -90.550),   # Destrehan / LaPlace
    ],
    "Bayou Teche": [
        (30.380, -91.830),   # Arnaudville
        (30.290, -91.815),   # Breaux Bridge area
        (30.130, -91.835),   # St. Martinville
        (30.050, -91.870),   # Parks / Loreauville
        (29.950, -91.820),   # New Iberia
        (29.870, -91.670),   # Jeanerette
        (29.800, -91.520),   # Franklin
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE CORRIDORS — focused on river-adjacent pipeline crossings
# ─────────────────────────────────────────────────────────────────────────────
CORRIDORS = {
    "Atchafalaya Basin": {
        "desc": "Atchafalaya River corridor — Morgan City to Krotz Springs. Pipeline crossings + river cooling.",
        "parishes": ["St. Mary", "Iberia", "St. Martin", "St. Landry", "Pointe Coupee", "Iberville", "Assumption"],
        "pipe_nodes": [
            (29.693, -91.210),   # Morgan City area pipelines
            (29.870, -91.530),   # Franklin / Garden City crossing
            (30.050, -91.820),   # St. Martinville
            (30.293, -91.795),   # Henderson Levee area
            (30.410, -91.755),   # Arnaudville
            (30.537, -91.752),   # Krotz Springs (Tennessee Gas / Gulf South crossing)
            (30.720, -91.700),   # Melville
        ],
        "rivers": ["Atchafalaya", "Bayou Teche"],
        "keywords": [
            "industrial land near Atchafalaya",
            "waterfront industrial property",
            "land for sale near river",
            "commercial acreage near pipeline",
            "industrial site Morgan City",
            "land Krotz Springs",
            "industrial property Henderson",
            "undeveloped land Atchafalaya",
            "swamp land for sale St. Mary",
            "timber land for sale Iberville",
            "camp land Atchafalaya basin",
            "hunting camp land for sale",
            "recreational land near river Louisiana",
            "undeveloped acreage pipeline corridor",
        ],
    },
    "Mississippi River": {
        "desc": "Mississippi River corridor — Baton Rouge to Donaldsonville. Refinery row, pipeline-dense.",
        "parishes": ["East Baton Rouge", "West Baton Rouge", "Iberville", "Ascension", "St. James", "St. John the Baptist"],
        "pipe_nodes": [
            (30.450, -91.190),   # Baton Rouge industrial
            (30.350, -91.100),   # Port Allen
            (30.200, -91.020),   # Plaquemine
            (30.100, -90.940),   # Donaldsonville
            (30.030, -90.830),   # Convent
            (29.940, -90.760),   # Gramercy / Lutcher
        ],
        "rivers": ["Mississippi"],
        "keywords": [
            "industrial land Mississippi River Louisiana",
            "waterfront industrial Baton Rouge",
            "land for sale near river Iberville",
            "commercial acreage Donaldsonville",
            "industrial site Plaquemine",
            "land for sale Port Allen",
            "pipeline access industrial property Louisiana",
            "undeveloped land Mississippi River",
            "timber land Iberville Parish",
            "swamp land for sale Ascension",
            "camp property riverfront Louisiana",
            "hunting land near river Baton Rouge",
            "recreational acreage Mississippi River",
        ],
    },
    "Bayou Teche": {
        "desc": "Bayou Teche corridor — New Iberia to Breaux Bridge. Pipeline + bayou cooling.",
        "parishes": ["Iberia", "St. Martin", "St. Mary", "Lafayette"],
        "pipe_nodes": [
            (29.950, -91.820),   # New Iberia (Hwy 90 pipeline crossing)
            (30.050, -91.870),   # Loreauville
            (30.130, -91.835),   # St. Martinville
            (30.290, -91.815),   # Breaux Bridge
            (29.800, -91.520),   # Franklin
        ],
        "rivers": ["Bayou Teche", "Atchafalaya"],
        "keywords": [
            "industrial land New Iberia",
            "waterfront property Bayou Teche",
            "land near pipeline St. Martin Parish",
            "commercial property Breaux Bridge",
            "industrial site Jeanerette",
            "acreage for sale near water",
            "undeveloped land Bayou Teche",
            "swamp land St. Martin Parish",
            "timber land for sale Iberia Parish",
            "camp land Bayou Teche",
            "hunting camp for sale near water Louisiana",
            "recreational property Breaux Bridge",
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# SCORING — updated weights with river proximity
# ─────────────────────────────────────────────────────────────────────────────
WEIGHTS = {
    "pipeline":  20,   # was 25 — still critical
    "river":     20,   # NEW — river proximity for cooling
    "flood":     15,   # was 20 — reduced because pilings solve flood risk
    "size":      15,   # unchanged
    "power":     10,   # was 15 — less critical with on-site gen
    "zoning":    10,   # was 15 — industrial zoning near rivers is common
    "road":      10,   # unchanged
}

MAXES = {
    "pipeline": 5,
    "river":    5,
    "flood":    5,
    "size":     5,
    "power":    5,
    "zoning":   5,
    "road":     3,
}

ZONING_SCORES = {
    "industrial": 5, "agricultural": 4, "commercial": 3,
    "mixed": 2, "residential": 1, "unknown": 1,
}

ROAD_MAP = {"paved_truck": 3, "paved_needs_work": 2, "gravel": 1, "none": 0}
SIZE_SCORE = lambda ac: 5 if ac >= 20 else 4 if ac >= 10 else 3 if ac >= 5 else 2 if ac >= 2 else 1
POWER_SCORE = lambda mi: 5 if mi < 0.5 else 4 if mi < 1 else 3 if mi < 2 else 2 if mi < 3 else 1


def pipeline_distance_score(miles: float) -> int:
    if miles < 0.1:  return 5
    if miles < 0.5:  return 4
    if miles < 1.0:  return 3
    if miles < 2.0:  return 2
    if miles < 5.0:  return 1
    return 0


def river_distance_score(miles: float) -> int:
    """Score river proximity. Closer = better for cooling water access."""
    if miles < 0.25: return 5   # Adjacent — ideal
    if miles < 0.5:  return 4   # Very close — short pipe run
    if miles < 1.0:  return 3   # Close — feasible intake
    if miles < 2.0:  return 2   # Reachable but expensive pipe
    if miles < 5.0:  return 1   # Far — marginal benefit
    return 0


def distance_to_nearest_river(lat: float, lng: float, river_names: list[str]) -> tuple[float, str]:
    """Return (miles, river_name) to nearest point on named rivers."""
    best_dist = 999
    best_river = "unknown"
    for name in river_names:
        points = RIVERS.get(name, [])
        for rlat, rlng in points:
            d = haversine_miles(lat, lng, rlat, rlng)
            if d < best_dist:
                best_dist = d
                best_river = name
    return best_dist, best_river


def score_site(site: dict) -> dict:
    """Score a site with river-aware weighting. Returns augmented dict."""
    raw = {
        "pipeline": int(site.get("pipeline", 0)),
        "river":    int(site.get("river", 0)),
        "flood":    int(site.get("flood", 0)),
        "size":     int(site.get("size", 0)),
        "power":    int(site.get("power", 0)),
        "zoning":   ZONING_SCORES.get(str(site.get("zoning", "unknown")).lower(), 1),
        "road":     int(site.get("road", 0)),
    }
    total = 0
    breakdown = {}
    for k, w in WEIGHTS.items():
        pts = round((raw[k] / MAXES[k]) * w)
        breakdown[k] = {"raw": raw[k], "max": MAXES[k], "weight": w, "pts": pts}
        total += pts

    tier = (
        {"tier": "A", "label": "Top Priority"}     if total >= 80 else
        {"tier": "B", "label": "Strong Candidate"}  if total >= 60 else
        {"tier": "C", "label": "Investigate Further"} if total >= 40 else
        {"tier": "D", "label": "Low Priority"}
    )
    return {**site, "score": total, "tier": tier["tier"], "tier_label": tier["label"], "breakdown": breakdown}


# ─────────────────────────────────────────────────────────────────────────────
# TOOLS FOR CLAUDE
# ─────────────────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for Louisiana land/property listings near gas pipelines and rivers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "record_site",
        "description": (
            "Record a discovered property site. Call this once per site found. "
            "CRITICAL: Prioritize sites near BOTH a gas pipeline AND a river (Atchafalaya, Mississippi, Bayou Teche). "
            "River proximity is as important as pipeline proximity."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name":        {"type": "string",  "description": "Descriptive site name"},
                "parish":      {"type": "string",  "description": "Louisiana parish name"},
                "lat":         {"type": "number",  "description": "Latitude (decimal degrees)"},
                "lng":         {"type": "number",  "description": "Longitude (decimal degrees, negative for LA)"},
                "acres":       {"type": "number",  "description": "Parcel size in acres"},
                "price_total": {"type": "number",  "description": "Total asking price in USD"},
                "price_acre":  {"type": "number",  "description": "Price per acre in USD"},
                "zoning":      {"type": "string",  "enum": ["industrial","agricultural","commercial","mixed","residential","unknown"]},
                "pipeline_dist_miles": {"type": "number", "description": "Estimated distance to nearest gas pipeline in miles"},
                "river_dist_miles":    {"type": "number", "description": "Estimated distance to nearest river (Atchafalaya/Mississippi/Bayou Teche) in miles"},
                "river_name":          {"type": "string", "description": "Name of nearest river"},
                "power_dist_miles":    {"type": "number", "description": "Estimated distance to nearest electrical substation in miles"},
                "road_access": {"type": "string",  "enum": ["paved_truck","paved_needs_work","gravel","none"]},
                "listing_url": {"type": "string",  "description": "URL of the listing if found"},
                "notes":       {"type": "string",  "description": "Key observations: river access type, pipeline operator, elevation, listing source"},
            },
            "required": ["name", "parish", "zoning"],
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SCOUT AGENT
# ─────────────────────────────────────────────────────────────────────────────
def run_scout(corridor_name: str, corridor: dict, client: anthropic.Anthropic,
              max_sites: int = 5) -> list[dict]:
    """Run one Claude agent for a single corridor. Returns list of scored sites."""

    parishes = ", ".join(corridor["parishes"])
    keywords = " | ".join(corridor["keywords"])
    rivers = ", ".join(corridor["rivers"])

    system = f"""You are a real estate intelligence agent for ADC 3K, an AI data center company
building GPU compute infrastructure along Louisiana gas pipelines and rivers.

YOUR MISSION: Find {max_sites} real property listings for sale in {parishes} parishes
that are near BOTH a gas pipeline AND a major waterway ({rivers}).

WHY RIVERS MATTER:
ADC 3K uses immersion cooling for AI GPU racks. River water is the most efficient
heat rejection method — a closed-loop heat exchanger using river water eliminates
the need for massive dry coolers and cooling towers. The Atchafalaya River moves
150,000+ CFS. Even a 10MW facility's thermal load is negligible in that flow.
Properties adjacent to BOTH a pipeline (fuel) AND a river (cooling) have a
double cost advantage that no desert data center can match.

IDEAL SITES:
- Within 1 mile of a navigable river (Atchafalaya, Mississippi, Bayou Teche)
- Within 2 miles of a gas transmission pipeline
- Industrial, agricultural, OR undeveloped land, 2+ acres
- Paved road access for truck traffic (or gravel with paved road nearby)
- Price under $20,000/acre for rural, under $50,000/acre for industrial
- Flood zone is ACCEPTABLE — we build on pilings. Zone AE is fine.
  Zone VE (coastal) is the only disqualifier.

IMPORTANT — SEARCH FOR THESE PROPERTY TYPES:
River-adjacent land in Louisiana is often listed as: undeveloped, swamp, timber,
camp, recreational, hunting camp, or unimproved land. These are EXACTLY what we
want — cheap land near water that nobody else is bidding on for development.
We don't need a building. We bring containerized pods on pilings.
Search for these terms in addition to industrial/commercial.

SEARCH STRATEGY:
1. Search for waterfront/river-adjacent land — industrial, agricultural, AND undeveloped/timber/camp
2. Cross-reference with known pipeline corridors
3. Check parish assessor sites for unlisted parcels near river bends
4. Look at LoopNet, LandWatch, Land.com, Lands of America, Realtor.com
5. Search for specific towns along the corridor: {', '.join(corridor['keywords'][:3])}
6. Try searches like "swamp land for sale [parish]" or "timber land near river [parish]"
7. Search "hunting camp for sale" + parish name — these are often cheap riverfront parcels

For each site found, call record_site with as much detail as possible.
Include river_dist_miles and river_name when you can estimate them.
Find REAL current listings — do not invent properties.
If you cannot confirm GPS coordinates, omit lat/lng rather than guessing.
"""

    messages = [{"role": "user", "content":
        f"Search for industrial and agricultural land listings for sale along the "
        f"{corridor['desc']} "
        f"These sites must be near both a gas pipeline and the {rivers}. "
        f"Search keywords to try: {keywords}. "
        f"Find {max_sites} real sites. Record each one with record_site."
    }]

    discovered = []
    iterations = 0
    max_iterations = 25

    print(f"\n  Agent running: {corridor_name}")
    print(f"  Target parishes: {parishes}")
    print(f"  Target rivers: {rivers}")

    while iterations < max_iterations:
        iterations += 1
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print(f"  Agent finished after {iterations} iterations. Found {len(discovered)} sites.")
            break

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            if block.name == "web_search":
                query = block.input.get("query", "")
                print(f"    [search] {query[:90]}")
                result = _web_search(query, client)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            elif block.name == "record_site":
                site_raw = block.input
                print(f"    [record] {site_raw.get('name','?')} — {site_raw.get('parish','?')} — {site_raw.get('acres','?')} ac")
                site = _enrich_site(site_raw, corridor)
                discovered.append(site)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": (
                        f"Recorded: {site['name']} | Score: {site['score']} | Tier: {site['tier']} | "
                        f"River: {site.get('_river_name','?')} @ {site.get('_river_miles','?')} mi | "
                        f"Pipeline: {site.get('_pipe_miles','?')} mi"
                    ),
                })
                if len(discovered) >= max_sites:
                    print(f"  Reached max sites ({max_sites}). Stopping agent.")
                    return discovered

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    return discovered


def _web_search(query: str, client: anthropic.Anthropic) -> str:
    """Use Claude's web search tool."""
    try:
        r = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 1}],
            messages=[{"role": "user", "content":
                f"Search for: {query}\n\n"
                f"Return a summary of the top results including property listings with "
                f"addresses, prices, acreage, and proximity to rivers or pipelines."
            }],
        )
        texts = []
        for block in r.content:
            if hasattr(block, 'text'):
                texts.append(block.text)
        return "\n".join(texts) if texts else "No results found."
    except Exception as e:
        return f"Search error: {e}"


def _enrich_site(raw: dict, corridor: dict) -> dict:
    """Add FEMA flood check, river proximity, scoring, and metadata."""
    lat = raw.get("lat")
    lng = raw.get("lng")

    # FEMA flood zone
    flood_info = {"zone": "unknown", "score": 3, "description": "No GPS — flood zone not checked"}
    if lat and lng:
        print(f"      [fema] checking flood zone at {lat:.4f},{lng:.4f}...")
        flood_info = get_flood_zone(lat, lng)
        time.sleep(0.3)

    # Pipeline distance score
    pipe_score = 0
    pipe_miles = raw.get("pipeline_dist_miles")
    if pipe_miles is not None:
        pipe_score = pipeline_distance_score(float(pipe_miles))
    elif lat and lng:
        min_dist = min(
            haversine_miles(lat, lng, plat, plng)
            for plat, plng in corridor["pipe_nodes"]
        )
        pipe_score = pipeline_distance_score(min_dist)
        pipe_miles = round(min_dist, 2)

    # River distance score
    river_score = 0
    river_miles = raw.get("river_dist_miles")
    river_name = raw.get("river_name", "unknown")
    if river_miles is not None:
        river_score = river_distance_score(float(river_miles))
    elif lat and lng:
        river_miles, river_name = distance_to_nearest_river(lat, lng, corridor["rivers"])
        river_score = river_distance_score(river_miles)
        river_miles = round(river_miles, 2)

    # Flood zone adjustment for pilings feasibility
    # Zone AE gets a bump because pilings solve it; only VE stays at 0
    flood_score = flood_info["score"]
    if flood_info["zone"] in ("A", "AE", "AH", "AO") and river_score >= 3:
        # Near river + floodplain = expected. Pilings solve this. Bump from 1 to 2.
        flood_score = max(flood_score, 2)

    # Other scores
    acres = raw.get("acres") or 0
    power_mi = raw.get("power_dist_miles") or 2.0
    road_val = ROAD_MAP.get(raw.get("road_access", "paved_needs_work"), 2)

    price_acre = raw.get("price_acre")
    if not price_acre and raw.get("price_total") and acres:
        price_acre = round(raw["price_total"] / acres)

    site = {
        "id": f"rv_{int(time.time()*1000)}_{hash(raw.get('name',''))&0xFFFF:04x}",
        "name":     raw.get("name", "Unnamed Site"),
        "parish":   raw.get("parish", "Unknown"),
        "zoning":   raw.get("zoning", "unknown"),
        "lat":      lat,
        "lng":      lng,
        "pipeline": str(pipe_score),
        "river":    str(river_score),
        "flood":    str(flood_score),
        "size":     str(SIZE_SCORE(acres) if acres else 1),
        "power":    str(POWER_SCORE(float(power_mi))),
        "road":     str(road_val),
        "price":    str(int(price_acre)) if price_acre else "",
        "notes":    (
            f"{raw.get('notes','')}\n"
            f"River: {river_name} @ {river_miles:.1f} mi | "
            f"Pipeline est: {pipe_miles:.1f} mi | "
            f"Flood: {flood_info['description']} | "
            f"Acres: {acres} | "
            f"Pilings: {'required' if flood_info['zone'] in ('A','AE','AH','AO') else 'not required'} | "
            f"{raw.get('listing_url','')}"
        ).strip(),
        "status":   "identified",
        "added":    datetime.now(timezone.utc).isoformat(),
        "source":   "river_scout_agent",
        # Extra fields
        "_acres":       acres,
        "_price_total": raw.get("price_total"),
        "_price_acre":  price_acre,
        "_flood_zone":  flood_info["zone"],
        "_pipe_miles":  pipe_miles,
        "_river_miles": river_miles,
        "_river_name":  river_name,
        "_listing_url": raw.get("listing_url", ""),
    }

    scored = score_site(site)
    pipe_str = f"{pipe_miles:.1f} mi" if pipe_miles is not None else "unknown"
    river_str = f"{river_miles:.1f} mi" if river_miles is not None else "unknown"
    print(f"      Score: {scored['score']} Tier {scored['tier']} | "
          f"River: {river_name} @ {river_str} | Pipeline: {pipe_str} | "
          f"Flood: {flood_info['zone']}")
    return scored


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
def save_json(sites: list, path: str):
    existing = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing_ids = {s.get("id") for s in existing}
    clean = list(existing)
    added = 0
    for s in sites:
        if s.get("id") in existing_ids:
            continue
        c = {k: v for k, v in s.items() if not k.startswith("_")}
        c.pop("breakdown", None)
        c.pop("tier_label", None)
        clean.append(c)
        added += 1

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    print(f"\nJSON saved: {path}  ({len(clean)} total sites, {added} new)")


def save_csv(sites: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["name", "parish", "score", "tier", "status", "zoning",
                  "_acres", "_price_acre", "_price_total", "_flood_zone",
                  "_pipe_miles", "_river_miles", "_river_name",
                  "pipeline", "river", "flood", "size", "power", "road",
                  "lat", "lng", "_listing_url", "notes", "added"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(sites, key=lambda s: -s.get("score", 0)))
    print(f"CSV saved:  {path}")


def print_summary(sites: list):
    print("\n" + "=" * 70)
    print("RIVER + PIPELINE SCOUT — RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total sites found: {len(sites)}")
    tiers = {"A": 0, "B": 0, "C": 0, "D": 0}
    for s in sites:
        tiers[s.get("tier", "D")] += 1
    print(f"Tier A (80+): {tiers['A']}  Tier B (60-79): {tiers['B']}  "
          f"Tier C (40-59): {tiers['C']}  Tier D (<40): {tiers['D']}")
    print()
    header = f"{'RK':<3} {'SC':<4} {'T':<2} {'NAME':<35} {'PARISH':<14} {'RIVER':<14} {'R-MI':<6} {'P-MI':<6} {'FLD':<5}"
    print(header)
    print("-" * len(header))
    for i, s in enumerate(sorted(sites, key=lambda x: -x.get("score", 0)), 1):
        print(f"{i:<3} {s.get('score',0):<4} {s.get('tier','?'):<2} "
              f"{s.get('name','')[:33]:<35} {s.get('parish','')[:12]:<14} "
              f"{s.get('_river_name','?')[:12]:<14} "
              f"{str(s.get('_river_miles','?'))[:5]:<6} "
              f"{str(s.get('_pipe_miles','?'))[:5]:<6} "
              f"{s.get('_flood_zone','?'):<5}")
    print()

    # Best site callout
    if sites:
        best = max(sites, key=lambda s: s.get("score", 0))
        print(f"TOP SITE: {best['name']} — Score {best['score']} Tier {best['tier']}")
        print(f"  River: {best.get('_river_name','?')} @ {best.get('_river_miles','?')} mi")
        print(f"  Pipeline: {best.get('_pipe_miles','?')} mi")
        print(f"  Flood: {best.get('_flood_zone','?')} — pilings {'required' if best.get('_flood_zone','X') in ('A','AE','AH','AO') else 'not required'}")
    print()


def generate_import_script(json_path: str, output_path: str):
    script = f"""// ADC 3K — Import river scout results into site-intel.html
// Open site-intel.html → DevTools Console → paste this:

(async function() {{
  const resp = await fetch('{json_path.replace(chr(92),'/')}');
  const newSites = await resp.json();
  const existing = JSON.parse(localStorage.getItem('adc3k_sites') || '[]');
  const existingIds = new Set(existing.map(s => s.id));
  const toAdd = newSites.filter(s => !existingIds.has(s.id));
  localStorage.setItem('adc3k_sites', JSON.stringify([...existing, ...toAdd]));
  console.log('Imported ' + toAdd.length + ' new river sites. Reload the page.');
  location.reload();
}})();
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"Import script: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="ADC 3K River + Pipeline Site Scout")
    parser.add_argument("--corridors", nargs="*", choices=list(CORRIDORS.keys()),
                        default=list(CORRIDORS.keys()),
                        help="Which corridors to scout (default: all)")
    parser.add_argument("--max-sites", type=int, default=5,
                        help="Max sites per corridor (default: 5)")
    parser.add_argument("--output", default="data/river_sites.json",
                        help="Output JSON path")
    args = parser.parse_args()

    from dotenv import load_dotenv
    load_dotenv(".env")
    load_dotenv(".venv/.env")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("=" * 70)
    print("ADC 3K — RIVER + PIPELINE SITE SCOUT")
    print("=" * 70)
    print(f"Corridors: {', '.join(args.corridors)}")
    print(f"Max sites per corridor: {args.max_sites}")
    print(f"Output: {args.output}")
    print()
    print("THESIS: Pipeline (fuel) + River (cooling) = double cost advantage.")
    print("        Pilings handle flood risk. Zone VE only disqualifier.")
    print()

    all_sites = []
    for name in args.corridors:
        corridor = CORRIDORS[name]
        try:
            sites = run_scout(name, corridor, client, max_sites=args.max_sites)
            all_sites.extend(sites)
            print(f"  [{name}] {len(sites)} sites collected.")
        except KeyboardInterrupt:
            print("\nInterrupted. Saving results so far...")
            break
        except Exception as e:
            print(f"  [{name}] ERROR: {e}")
            continue

    if not all_sites:
        print("No sites collected.")
        return

    json_path = args.output
    csv_path = json_path.replace(".json", ".csv")
    js_path = json_path.replace(".json", "_import.js")

    save_json(all_sites, json_path)
    save_csv(all_sites, csv_path)
    generate_import_script(json_path, js_path)
    print_summary(all_sites)

    print("Next steps:")
    print(f"  1. Review {csv_path} — sort by score, check river + pipeline distances")
    print(f"  2. Open site-intel.html in browser")
    print(f"  3. Open DevTools console, paste contents of {js_path}")
    print(f"  4. River sites load into the intelligence map")
    print(f"  5. Drive the top Tier A sites — verify river access + pipeline markers")


if __name__ == "__main__":
    main()
