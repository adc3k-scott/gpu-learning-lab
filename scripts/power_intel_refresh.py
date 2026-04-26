"""
Power Intel Refresh — runs weekly via GitHub Action.
Searches for natural gas power generation news and opportunities,
then uses Claude to format them into feed.json for the dashboard.

Requirements: pip install anthropic duckduckgo-search
Env: ANTHROPIC_API_KEY
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

try:
    from duckduckgo_search import DDGS
except ImportError:
    print("duckduckgo-search not installed. Run: pip install duckduckgo-search")
    sys.exit(1)

FEED_PATH = Path(__file__).parent.parent / "adc3k-deploy" / "power-tracker" / "feed.json"

SEARCH_QUERIES = [
    "surplus natural gas generator turbine for sale MW 2026",
    "Wärtsilä INNIO Jenbacher data center power cancellation slot available 2026",
    "ProEnergy PE6000 natural gas turbine data center availability",
    "natural gas generator decommission sale power plant 2026",
    "data center behind the meter natural gas power news 2026",
    "Solar Turbines surplus used Mars Taurus genset for sale",
    "Gulf Mexico offshore platform decommission generator turbine",
]

URGENCY_KEYWORDS = {
    "critical": ["cancellation slot", "available now", "immediate", "for sale now", "in stock"],
    "high": ["surplus", "decommission", "available", "for sale", "new listing", "just released"],
    "medium": ["order", "delivery", "lead time", "backlog", "announced"],
    "low": ["analysis", "outlook", "forecast", "trend"],
}


def run_searches():
    results = []
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            try:
                hits = list(ddgs.text(query, max_results=5))
                results.extend(hits)
                print(f"  ✓ '{query[:50]}…' → {len(hits)} results")
            except Exception as e:
                print(f"  ✗ Search failed for '{query[:40]}': {e}")
    return results


def load_existing_feed():
    if FEED_PATH.exists():
        with open(FEED_PATH) as f:
            return json.load(f)
    return {"intel": [], "opportunity_leads": []}


def refresh_feed():
    print("=== Power Intel Refresh ===")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    print("\n[1/3] Running searches...")
    raw_results = run_searches()
    print(f"Total results collected: {len(raw_results)}")

    # Format results for Claude
    results_text = "\n\n".join([
        f"Title: {r.get('title','')}\nURL: {r.get('href','')}\nSnippet: {r.get('body','')}"
        for r in raw_results[:30]
    ])

    print("\n[2/3] Analyzing with Claude...")
    client = anthropic.Anthropic(api_key=api_key)

    existing = load_existing_feed()
    existing_ids = {item["id"] for item in existing.get("intel", [])}

    prompt = f"""You are analyzing natural gas power generation search results for a procurement intelligence dashboard.
The operator is sourcing 100 MW of behind-the-meter natural gas generation for a data center in Lafayette, Louisiana.
He is open to: new OEM equipment, used/surplus units, aero-derivative turbines (PE6000/CF6 cores), engine-only for self-build, PPA/rental bridge power.

Today's date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

SEARCH RESULTS:
{results_text}

Extract 3-6 intelligence items that would be most useful for this operator. For each item, assign:
- urgency: "critical" (asset available NOW or slot opening), "high" (near-term opportunity or important OEM news), "medium" (market intel), "low" (background)
- category: "listing" (specific unit for sale), "oem" (OEM news/lead times), "market" (market conditions), "news" (industry news)

Also extract 0-3 specific opportunity leads (actual equipment for sale or available).

Return ONLY valid JSON in this exact format:
{{
  "intel": [
    {{
      "id": "auto_{datetime.now().strftime('%Y%m%d')}_001",
      "date": "{datetime.now().strftime('%Y-%m-%d')}",
      "category": "listing|oem|market|news",
      "urgency": "critical|high|medium|low",
      "headline": "concise headline under 80 chars",
      "detail": "2-3 sentences of detail relevant to the Louisiana data center operator",
      "source": "source name",
      "action": "specific action the operator should take (start with a verb)"
    }}
  ],
  "opportunity_leads": [
    {{
      "id": "feed_{datetime.now().strftime('%Y%m%d')}_001",
      "oem": "OEM or seller name",
      "model": "model or description",
      "mw": null,
      "mw_unit": null,
      "qty": 1,
      "condition": "new|refurb|used|engine-only",
      "status": "new",
      "tier": "1|2|3",
      "lead_weeks": null,
      "price_per_kw": null,
      "contact": "contact info or URL",
      "location": "location",
      "notes": "key details",
      "tags": ["tag1", "tag2"],
      "last_contact": null,
      "next_follow_up": "{(datetime.now()).strftime('%Y-%m-%d')}",
      "updated": "{datetime.now(timezone.utc).isoformat()}",
      "created": "{datetime.now(timezone.utc).isoformat()}"
    }}
  ]
}}

Only include items that are genuinely relevant and actionable. If search results have nothing new, return fewer items. Do not fabricate specific prices or unit counts you cannot verify."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        parsed = json.loads(raw)
        print(f"  Claude returned {len(parsed.get('intel',[]))} intel items, {len(parsed.get('opportunity_leads',[]))} leads")
    except json.JSONDecodeError as e:
        print(f"  Claude response was not valid JSON: {e}")
        print(f"  Raw response: {raw[:500]}")
        parsed = {"intel": [], "opportunity_leads": []}
    except Exception as e:
        print(f"  Claude call failed: {e}")
        parsed = {"intel": [], "opportunity_leads": []}

    print("\n[3/3] Merging and writing feed.json...")

    # Merge: keep existing intel, prepend new items (deduplicate by id)
    new_intel = parsed.get("intel", [])
    existing_intel = existing.get("intel", [])
    merged_ids = {item["id"] for item in new_intel}
    kept_existing = [item for item in existing_intel if item["id"] not in merged_ids]

    # Keep max 20 intel items total
    all_intel = new_intel + kept_existing
    all_intel = sorted(
        all_intel,
        key=lambda x: ({"critical":0,"high":1,"medium":2,"low":3}.get(x.get("urgency","low"),9), x.get("date",""))
    )[:20]

    # Merge opportunity leads: only add new IDs
    existing_lead_ids = {o["id"] for o in existing.get("opportunity_leads", [])}
    new_leads = [o for o in parsed.get("opportunity_leads", []) if o["id"] not in existing_lead_ids]
    all_leads = existing.get("opportunity_leads", []) + new_leads

    feed = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "intel": all_intel,
        "opportunity_leads": all_leads
    }

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(FEED_PATH, "w") as f:
        json.dump(feed, f, indent=2)

    print(f"  Feed written: {len(all_intel)} intel items, {len(all_leads)} opportunity leads")
    print(f"  Path: {FEED_PATH}")
    print("\n=== Done ===")


if __name__ == "__main__":
    refresh_feed()
