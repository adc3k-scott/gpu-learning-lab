"""
ADC 3K — Pipeline Site Scout Agent
===================================
Sends Claude agents to search for industrial/agricultural land listings
near Louisiana gas pipelines, scores them, checks FEMA flood zones,
and outputs a JSON file compatible with site-intel.html.

Run:
    python scripts/pipeline_scout.py
    python scripts/pipeline_scout.py --corridors "Henry Hub" "Teche"
    python scripts/pipeline_scout.py --max-sites 30 --output data/sites.json

Output:
    data/pipeline_sites.json  — importable into site-intel.html
    data/pipeline_sites.csv   — spreadsheet version
"""
import sys, os, json, csv, time, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import anthropic
from datetime import datetime, timezone
from agents.site_scout.fema import get_flood_zone
from agents.site_scout.scorer import score_site, pipeline_distance_score, haversine_miles

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE CORRIDORS — search targets
# Each corridor defines the parishes to search and approximate pipeline coords
# ─────────────────────────────────────────────────────────────────────────────
CORRIDORS = {
    "Henry Hub": {
        "desc": "Henry Hub / Acadian Gas — Vermilion, St. Mary, Iberia parishes",
        "parishes": ["Vermilion", "St. Mary", "Iberia", "Lafayette"],
        "pipe_nodes": [(29.6,-92.2),(29.8,-92.1),(30.0,-92.0),(30.21,-91.9)],
        "keywords": ["industrial land", "agricultural land", "commercial property", "acreage for sale"],
    },
    "Tennessee Gas": {
        "desc": "Tennessee Gas Pipeline — St. Landry, Evangeline, Acadia corridors",
        "parishes": ["St. Landry", "Evangeline", "Acadia", "Allen"],
        "pipe_nodes": [(30.0,-93.2),(30.05,-92.8),(30.1,-92.2),(30.18,-91.8),(30.538,-91.752)],
        "keywords": ["industrial tract", "land for sale", "commercial acreage", "industrial site"],
    },
    "Southern Natural": {
        "desc": "Southern Natural Gas — I-10 corridor, Iberia to Jefferson Davis",
        "parishes": ["Iberia", "St. Mary", "Jefferson Davis", "Calcasieu"],
        "pipe_nodes": [(30.2,-93.5),(30.22,-93.0),(30.24,-92.5),(30.237,-92.82)],
        "keywords": ["industrial land", "land for sale near pipeline", "industrial zoned acreage"],
    },
    "Teche": {
        "desc": "Bayou Teche / Coastal corridor — St. Martin, Assumption, Terrebonne",
        "parishes": ["St. Martin", "Assumption", "Terrebonne", "Lafourche"],
        "pipe_nodes": [(29.7,-91.2),(29.8,-91.0),(29.9,-90.8),(30.0,-90.6)],
        "keywords": ["industrial property", "waterfront industrial", "commercial land for sale"],
    },
    "Sabine": {
        "desc": "Sabine Pass corridor — Calcasieu, Beauregard, Sabine parishes",
        "parishes": ["Calcasieu", "Beauregard", "Sabine", "Vernon"],
        "pipe_nodes": [(30.19,-93.58),(30.3,-93.3),(30.5,-93.1),(30.7,-93.0)],
        "keywords": ["industrial land near pipeline", "industrial zoned property", "commercial acreage"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# TOOLS FOR CLAUDE
# ─────────────────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for Louisiana land/property listings near gas pipelines.",
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
            "Use your best judgment to fill all fields from listing data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name":        {"type": "string",  "description": "Descriptive site name, e.g. 'Krotz Springs Industrial Tract (Hwy 190)'"},
                "parish":      {"type": "string",  "description": "Louisiana parish name"},
                "lat":         {"type": "number",  "description": "Latitude (decimal degrees)"},
                "lng":         {"type": "number",  "description": "Longitude (decimal degrees, negative for Louisiana)"},
                "acres":       {"type": "number",  "description": "Parcel size in acres"},
                "price_total": {"type": "number",  "description": "Total asking price in USD"},
                "price_acre":  {"type": "number",  "description": "Price per acre in USD"},
                "zoning":      {"type": "string",  "enum": ["industrial","agricultural","commercial","mixed","residential","unknown"]},
                "pipeline_dist_miles": {"type": "number", "description": "Estimated distance to nearest gas pipeline in miles"},
                "power_dist_miles":    {"type": "number", "description": "Estimated distance to nearest electrical substation in miles"},
                "road_access": {"type": "string",  "enum": ["paved_truck","paved_needs_work","gravel","none"]},
                "listing_url": {"type": "string",  "description": "URL of the listing if found"},
                "notes":       {"type": "string",  "description": "Key observations: listing source, owner contact if available, special features"},
            },
            "required": ["name", "parish", "zoning"],
        },
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ROAD ACCESS CONVERSION
# ─────────────────────────────────────────────────────────────────────────────
ROAD_MAP = {"paved_truck": 3, "paved_needs_work": 2, "gravel": 1, "none": 0}

SIZE_SCORE = lambda ac: (
    5 if ac >= 20 else
    4 if ac >= 10 else
    3 if ac >= 5  else
    2 if ac >= 2  else 1
)
POWER_SCORE = lambda mi: (
    5 if mi < 0.5 else
    4 if mi < 1   else
    3 if mi < 2   else
    2 if mi < 3   else 1
)

# ─────────────────────────────────────────────────────────────────────────────
# SCOUT AGENT
# ─────────────────────────────────────────────────────────────────────────────
def run_scout(corridor_name: str, corridor: dict, client: anthropic.Anthropic,
              max_sites: int = 5) -> list[dict]:
    """Run one Claude agent for a single pipeline corridor. Returns list of sites."""

    parishes = ", ".join(corridor["parishes"])
    keywords = " | ".join(corridor["keywords"])

    system = f"""You are a real estate intelligence agent for ADC 3K, an AI data center company
building infrastructure along Louisiana gas pipelines.

Your mission: Find {max_sites} real property listings for sale in {parishes} parishes
that are near or adjacent to gas pipeline infrastructure.

Ideal sites:
- Industrial or agricultural land, 2+ acres
- Close to a gas transmission pipeline (Tennessee Gas, Southern Natural Gas,
  Acadian Gas, Henry Hub feeds, Gulf South, Transcontinental)
- Low flood risk (FEMA Zone X preferred — avoid Zone AE/VE)
- Accessible by paved road, truck traffic
- Near an electrical substation
- Price under $20,000/acre for rural/ag, under $50,000/acre for industrial

For each site found, call record_site with as much detail as possible.
Use web_search to find listings on LoopNet, LandWatch, Land.com, Lands of America,
parish assessor sites, or commercial real estate sites.
Be specific in searches — include parish names and property types.
Find real, current listings — do not invent properties.
If you cannot find a real listing with GPS, omit lat/lng rather than guessing.
"""

    messages = [{"role": "user", "content":
        f"Search for industrial and agricultural land listings for sale in the "
        f"{corridor['desc']} corridor. "
        f"Search keywords to try: {keywords}. "
        f"Find {max_sites} real sites. Record each one with record_site."
    }]

    discovered = []
    iterations = 0
    max_iterations = 20

    print(f"\n  Agent running for corridor: {corridor_name}")
    print(f"  Target parishes: {parishes}")

    while iterations < max_iterations:
        iterations += 1
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        # Append assistant response
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print(f"  Agent finished after {iterations} iterations. Found {len(discovered)} sites.")
            break

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            if block.name == "web_search":
                query = block.input.get("query", "")
                print(f"    [search] {query[:80]}")
                result = _web_search(query, client)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            elif block.name == "record_site":
                site_raw = block.input
                print(f"    [record] {site_raw.get('name','?')} — {site_raw.get('parish','?')} — {site_raw.get('acres','?')} acres")
                # Enrich and score
                site = _enrich_site(site_raw, corridor)
                discovered.append(site)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Recorded: {site['name']} | Score: {site['score']} | Tier: {site['tier']}",
                })
                if len(discovered) >= max_sites:
                    print(f"  Reached max sites ({max_sites}). Stopping agent.")
                    return discovered

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    return discovered


def _web_search(query: str, client: anthropic.Anthropic) -> str:
    """Use Claude's web search tool to execute a search query."""
    try:
        r = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 1}],
            messages=[{"role": "user", "content": f"Search for: {query}\n\nReturn a summary of the top results including any property listings found with addresses, prices, and acreage."}],
        )
        texts = []
        for block in r.content:
            if hasattr(block, 'text'):
                texts.append(block.text)
        return "\n".join(texts) if texts else "No results found."
    except Exception as e:
        return f"Search error: {e}"


def _enrich_site(raw: dict, corridor: dict) -> dict:
    """Add FEMA flood check, scoring, and metadata to a raw site record."""
    lat = raw.get("lat")
    lng = raw.get("lng")

    # FEMA flood zone
    flood_info = {"zone": "unknown", "score": 3, "description": "No GPS — flood zone not checked"}
    if lat and lng:
        print(f"      [fema] checking flood zone at {lat:.4f},{lng:.4f}...")
        flood_info = get_flood_zone(lat, lng)
        time.sleep(0.3)  # gentle rate limiting

    # Pipeline distance score
    pipe_score = 0
    pipe_miles = raw.get("pipeline_dist_miles")
    if pipe_miles is not None:
        pipe_score = pipeline_distance_score(float(pipe_miles))
    elif lat and lng:
        # Calculate distance to nearest corridor node
        min_dist = min(
            haversine_miles(lat, lng, plat, plng)
            for plat, plng in corridor["pipe_nodes"]
        )
        pipe_score = pipeline_distance_score(min_dist)
        pipe_miles = round(min_dist, 2)

    # Other scores
    acres = raw.get("acres") or 0
    power_mi = raw.get("power_dist_miles") or 2.0
    road_val = ROAD_MAP.get(raw.get("road_access", "paved_needs_work"), 2)

    # Price per acre
    price_acre = raw.get("price_acre")
    if not price_acre and raw.get("price_total") and acres:
        price_acre = round(raw["price_total"] / acres)

    site = {
        "id": f"{int(time.time()*1000)}_{hash(raw.get('name',''))&0xFFFF:04x}",
        "name":     raw.get("name", "Unnamed Site"),
        "parish":   raw.get("parish", "Unknown"),
        "zoning":   raw.get("zoning", "unknown"),
        "lat":      lat,
        "lng":      lng,
        "pipeline": str(pipe_score),
        "flood":    str(flood_info["score"]),
        "size":     str(SIZE_SCORE(acres) if acres else 1),
        "power":    str(POWER_SCORE(float(power_mi))),
        "road":     str(road_val),
        "price":    str(int(price_acre)) if price_acre else "",
        "notes":    (
            f"{raw.get('notes','')}\n"
            f"Flood: {flood_info['description']} | "
            f"Pipeline est: {pipe_miles:.1f} mi | "
            f"Acres: {acres} | "
            f"{raw.get('listing_url','')}"
        ).strip(),
        "status":   "identified",
        "added":    datetime.now(timezone.utc).isoformat(),
        "source":   "pipeline_scout_agent",
        # Extra fields for CSV
        "_acres":       acres,
        "_price_total": raw.get("price_total"),
        "_price_acre":  price_acre,
        "_flood_zone":  flood_info["zone"],
        "_pipe_miles":  pipe_miles,
        "_listing_url": raw.get("listing_url",""),
    }

    scored = score_site(site)
    print(f"      Score: {scored['score']} Tier {scored['tier']} | Flood: {flood_info['zone']} | Pipe: {pipe_miles}")
    return scored


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
def save_json(sites: list, path: str):
    """Save in site-intel.html localStorage format."""
    # Strip internal _ fields for the HTML tool
    clean = []
    for s in sites:
        c = {k: v for k, v in s.items() if not k.startswith("_")}
        # Remove scoring breakdown (not needed in HTML)
        c.pop("breakdown", None)
        c.pop("tier_label", None)
        clean.append(c)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    print(f"\nJSON saved: {path}  ({len(clean)} sites)")


def save_csv(sites: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["name","parish","score","tier","status","zoning",
                  "_acres","_price_acre","_price_total","_flood_zone",
                  "_pipe_miles","pipeline","flood","size","power","road",
                  "lat","lng","_listing_url","notes","added"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(sites, key=lambda s: -s.get("score",0)))
    print(f"CSV saved:  {path}")


def print_summary(sites: list):
    print("\n" + "="*60)
    print(f"PIPELINE SCOUT — RESULTS SUMMARY")
    print("="*60)
    print(f"Total sites found: {len(sites)}")
    tiers = {"A":0,"B":0,"C":0,"D":0}
    for s in sites:
        tiers[s.get("tier","D")] += 1
    print(f"Tier A (80+): {tiers['A']}  Tier B (60-79): {tiers['B']}  "
          f"Tier C (40-59): {tiers['C']}  Tier D (<40): {tiers['D']}")
    print()
    sorted_sites = sorted(sites, key=lambda s: -s.get("score",0))
    print(f"{'RANK':<4} {'SCORE':<6} {'TIER':<5} {'NAME':<40} {'PARISH':<16} {'FLOOD':<8}")
    print("-"*80)
    for i, s in enumerate(sorted_sites, 1):
        print(f"{i:<4} {s.get('score',0):<6} {s.get('tier','?'):<5} "
              f"{s.get('name','')[:38]:<40} {s.get('parish','')[:14]:<16} "
              f"{s.get('_flood_zone','?'):<8}")
    print()


def generate_import_script(json_path: str, output_path: str):
    """Generate a JS snippet to import sites into site-intel.html localStorage."""
    script = f"""// ADC 3K — Import pipeline scout results into site-intel.html
// Run this in browser console while site-intel.html is open:
//
//   1. Open site-intel.html in browser
//   2. Open DevTools → Console
//   3. Paste this script and press Enter

(async function() {{
  const resp = await fetch('{json_path.replace(chr(92),'/')}');
  const newSites = await resp.json();
  const existing = JSON.parse(localStorage.getItem('adc3k_sites') || '[]');
  const existingIds = new Set(existing.map(s => s.id));
  const toAdd = newSites.filter(s => !existingIds.has(s.id));
  localStorage.setItem('adc3k_sites', JSON.stringify([...existing, ...toAdd]));
  console.log('Imported ' + toAdd.length + ' new sites. Reload the page.');
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
    parser = argparse.ArgumentParser(description="ADC 3K Pipeline Site Scout Agent")
    parser.add_argument("--corridors", nargs="*", choices=list(CORRIDORS.keys()),
                        default=list(CORRIDORS.keys()),
                        help="Which pipeline corridors to scout (default: all)")
    parser.add_argument("--max-sites", type=int, default=5,
                        help="Max sites per corridor (default: 5)")
    parser.add_argument("--output", default="data/pipeline_sites.json",
                        help="Output JSON path")
    args = parser.parse_args()

    # Load API key
    from dotenv import load_dotenv
    load_dotenv(".env")
    load_dotenv(".venv/.env")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("="*60)
    print("ADC 3K — PIPELINE SITE SCOUT")
    print("="*60)
    print(f"Corridors: {', '.join(args.corridors)}")
    print(f"Max sites per corridor: {args.max_sites}")
    print(f"Output: {args.output}")
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

    # Save outputs
    json_path = args.output
    csv_path  = json_path.replace(".json", ".csv")
    js_path   = json_path.replace(".json", "_import.js")

    save_json(all_sites, json_path)
    save_csv(all_sites, csv_path)
    generate_import_script(json_path, js_path)
    print_summary(all_sites)

    print("\nNext steps:")
    print(f"  1. Review {csv_path} for top candidates")
    print(f"  2. Open site-intel.html in browser")
    print(f"  3. Open DevTools console, paste contents of {js_path}")
    print(f"  4. Sites load directly into the intelligence map")


if __name__ == "__main__":
    main()
