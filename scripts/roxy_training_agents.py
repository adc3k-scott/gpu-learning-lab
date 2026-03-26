"""
ROXY Training Data Pipeline — Subagent Architecture
Uses Claude to generate hundreds of tool-calling training examples in parallel.
Each agent focuses on a different aspect of ROXY's capabilities.

Usage:
    python scripts/roxy_training_agents.py

Output:
    data/roxy-training-combined.jsonl (500+ examples)
"""

import json, os, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load API key
for line in Path('.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip())

ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
if not ANTHROPIC_KEY:
    print("ERROR: ANTHROPIC_API_KEY required in .env")
    sys.exit(1)

OUTPUT = Path("data/roxy-training-combined.jsonl")

SYSTEM_PROMPT_SHORT = "You are ROXY, the AI Advantage assistant. You are friendly, direct, and helpful. You have tools available. Use them proactively when relevant."

TOOL_DEFINITIONS = {
    "capture_lead": {"args": ["name", "email", "phone", "business_type", "interest_level"], "desc": "Save contact info to CRM"},
    "calculate_roi": {"args": ["industry", "missed_calls_per_week", "avg_job_value", "plan_tier"], "desc": "Calculate dollar ROI"},
    "competitor_intel": {"args": ["software_name", "industry"], "desc": "Position against competitor software"},
    "search_playbooks": {"args": ["query", "industry"], "desc": "Search 17 industry playbooks"},
    "build_quote": {"args": ["industry", "tier", "hardware"], "desc": "Generate pricing quote"},
    "franchise_qualifier": {"args": ["locations", "industry", "plan", "hardware"], "desc": "Quote multi-location deals"},
    "generate_live_demo": {"args": ["industry", "business_name"], "desc": "Day-in-the-life walkthrough"},
    "create_urgency_offer": {"args": ["industry", "location", "objection"], "desc": "Time-limited offer for fence-sitters"},
    "local_market_intel": {"args": ["industry", "location"], "desc": "Competitive landscape data"},
    "book_appointment": {"args": ["name", "email"], "desc": "Generate booking link"},
    "send_followup_email": {"args": ["email", "name", "business_type"], "desc": "Send personalized follow-up"},
    "initiate_outbound_call": {"args": ["phone_number", "prospect_name", "industry", "context"], "desc": "Call prospect via Bland.ai"},
    "score_lead": {"args": ["email", "phone", "industry", "locations", "timeline_urgent"], "desc": "Score and route lead"},
    "onboard_client": {"args": ["industry", "business_name", "plan"], "desc": "Pre-install questionnaire"},
    "generate_ad_copy": {"args": ["industry", "business_name", "location"], "desc": "Facebook/Google ad copy"},
    "generate_social_posts": {"args": ["industry", "business_name"], "desc": "Week of social media content"},
    "respond_to_review": {"args": ["review_text", "star_rating", "reviewer_name"], "desc": "Draft review response"},
    "request_review": {"args": ["customer_name", "business_name", "service_performed"], "desc": "Request Google review"},
    "generate_lead_magnet": {"args": ["industry", "business_name"], "desc": "Downloadable guide/checklist"},
    "build_email_campaign": {"args": ["industry", "business_name", "campaign_type"], "desc": "Email drip sequence"},
}

INDUSTRIES = [
    "plumbing", "HVAC", "electrical", "dental office", "medical practice",
    "restaurant", "auto repair shop", "real estate agency", "construction company",
    "property management", "retail store", "accounting firm", "hair salon",
    "insurance agency", "law firm", "veterinary clinic", "trucking company"
]

def call_claude(prompt, max_tokens=4000):
    """Call Claude API with rate limit handling."""
    import http.client, ssl
    max_tokens = min(max_tokens, 4096)

    # Rate limit: wait between calls
    time.sleep(3)

    conn = http.client.HTTPSConnection("api.anthropic.com", context=ssl.create_default_context(), timeout=60)
    body = json.dumps({
        "model": "claude-3-haiku-20240307",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    })
    conn.request("POST", "/v1/messages", body, {
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    })
    resp = conn.getresponse()
    data = json.loads(resp.read())
    if resp.status == 429:
        # Rate limited — wait and retry
        print(f"  Rate limited, waiting 30s...")
        time.sleep(30)
        return call_claude(prompt, max_tokens)
    if resp.status != 200:
        print(f"  Claude error: {data.get('error', {}).get('message', 'unknown')}")
        return None
    return data["content"][0]["text"]


def parse_examples(text):
    """Extract JSONL examples from Claude's response."""
    import re
    # Strip markdown code blocks if present
    text = re.sub(r'```(?:json|jsonl)?\n?', '', text)
    text = text.replace('```', '')

    examples = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        # Try to fix common issues
        try:
            obj = json.loads(line)
            if "messages" in obj:
                examples.append(obj)
        except json.JSONDecodeError:
            # Try to find JSON objects that span multiple lines
            continue

    # Also try to find JSON objects using regex
    if not examples:
        pattern = r'\{"messages":\s*\[.*?\]\s*\}'
        for match in re.finditer(pattern, text, re.DOTALL):
            try:
                obj = json.loads(match.group())
                examples.append(obj)
            except:
                pass
    return examples


# ===== SUBAGENT 1: Industry Conversation Generator =====
def agent_industry_conversations(industry):
    """Generates 5 realistic customer conversations for one industry."""
    tools_json = json.dumps({k: v["desc"] for k, v in TOOL_DEFINITIONS.items()}, indent=2)

    prompt = f"""Generate exactly 5 training examples for fine-tuning an AI sales agent called ROXY.
Each example is a JSONL line (one JSON object per line) with a "messages" array.

ROXY sells AI agents to small businesses. Industry: {industry}

Each example MUST include a tool call. Format:
{{"messages": [
  {{"role": "system", "content": "{SYSTEM_PROMPT_SHORT}"}},
  {{"role": "user", "content": "customer message"}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_1", "type": "function", "function": {{"name": "TOOL_NAME", "arguments": "{{\\"key\\": \\"value\\"}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_1", "content": "tool result as string"}},
  {{"role": "assistant", "content": "ROXY's final response using the tool result"}}
]}}

Available tools: {tools_json}

Generate 5 diverse examples for {industry}:
1. A customer asking what ROXY does for their industry (use search_playbooks)
2. A customer sharing their contact info (use capture_lead)
3. A customer asking about pricing/ROI (use calculate_roi or build_quote)
4. A customer mentioning a competitor software (use competitor_intel)
5. A customer ready to get started (use book_appointment or score_lead)

Output ONLY the 5 JSONL lines, nothing else. Each line must be valid JSON."""

    text = call_claude(prompt)
    if not text:
        return []
    return parse_examples(text)


# ===== SUBAGENT 2: Objection Handler =====
def agent_objections():
    """Generates objection-handling training examples."""
    prompt = f"""Generate 10 training examples for an AI sales agent called ROXY handling customer objections.

Each example shows a customer objecting and ROXY using a tool to overcome it. JSONL format, one JSON per line.

Format per line:
{{"messages": [
  {{"role": "system", "content": "{SYSTEM_PROMPT_SHORT}"}},
  {{"role": "user", "content": "customer objection"}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_1", "type": "function", "function": {{"name": "TOOL_NAME", "arguments": "{{\\"key\\": \\"value\\"}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_1", "content": "tool result"}},
  {{"role": "assistant", "content": "ROXY overcoming the objection"}}
]}}

Objection scenarios:
1. "It's too expensive" → use calculate_roi to show it pays for itself
2. "I need to think about it" → use create_urgency_offer for time-limited offer
3. "We already use ServiceTitan" → use competitor_intel to position as complement
4. "I already use Toast POS" → use competitor_intel
5. "Is this like ChatGPT?" → use competitor_intel
6. "We're too small for AI" → use calculate_roi with small numbers
7. "My staff won't use it" → use generate_live_demo to show simplicity
8. "I don't have time for a call" → use book_appointment with quick 15-min pitch
9. "How do I know it works?" → use local_market_intel to show adoption
10. "Can you just call me?" → use initiate_outbound_call

Output ONLY 10 JSONL lines. Each must be valid JSON."""

    text = call_claude(prompt)
    if not text:
        return []
    return parse_examples(text)


# ===== SUBAGENT 3: Multi-Turn Conversations =====
def agent_multi_turn():
    """Generates complex multi-turn conversations with multiple tool calls."""
    prompt = f"""Generate 5 multi-turn conversation training examples for an AI sales agent called ROXY.

Each conversation has 4-6 turns and uses 2-3 different tools. JSONL format.

Format:
{{"messages": [
  {{"role": "system", "content": "{SYSTEM_PROMPT_SHORT}"}},
  {{"role": "user", "content": "first message"}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_1", "type": "function", "function": {{"name": "search_playbooks", "arguments": "{{\\"query\\": \\"..\\", \\"industry\\": \\"..\\"}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_1", "content": "playbook results"}},
  {{"role": "assistant", "content": "ROXY answers with playbook knowledge"}},
  {{"role": "user", "content": "customer follows up"}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_2", "type": "function", "function": {{"name": "capture_lead", "arguments": "{{\\"name\\": \\"..\\", \\"email\\": \\"..\\"}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_2", "content": "lead saved"}},
  {{"role": "assistant", "content": "ROXY confirms and moves to close"}}
]}}

Scenarios:
1. Plumber: asks about features → gives contact info → asks for ROI → books call
2. Dentist: asks about HIPAA → mentions Dentrix → wants a quote → gives email
3. Restaurant owner: asks about inventory → mentions Toast → wants social media help
4. Franchise owner with 8 locations: asks about pricing → wants volume discount → ready to pay
5. Salon owner: gets bad review → asks for response help → asks about marketing tools

Output ONLY 5 JSONL lines. Each must be valid JSON."""

    text = call_claude(prompt, max_tokens=6000)
    if not text:
        return []
    return parse_examples(text)


# ===== SUBAGENT 4: Marketing Tools =====
def agent_marketing():
    """Generates training examples for SaaS marketing tools."""
    prompt = f"""Generate 8 training examples for an AI agent called ROXY using marketing/SaaS tools.

JSONL format, one JSON per line. Each shows a business owner asking for marketing help and ROXY using a tool.

Tools to cover:
- generate_ad_copy: args {{"industry": "...", "business_name": "...", "location": "..."}}
- generate_social_posts: args {{"industry": "...", "business_name": "..."}}
- respond_to_review: args {{"review_text": "...", "star_rating": N, "reviewer_name": "..."}}
- request_review: args {{"customer_name": "...", "business_name": "...", "service_performed": "..."}}
- generate_lead_magnet: args {{"industry": "...", "business_name": "..."}}
- build_email_campaign: args {{"industry": "...", "business_name": "...", "campaign_type": "welcome"}}

Format per line:
{{"messages": [
  {{"role": "system", "content": "{SYSTEM_PROMPT_SHORT}"}},
  {{"role": "user", "content": "customer request"}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_1", "type": "function", "function": {{"name": "TOOL", "arguments": "{{...}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_1", "content": "tool output"}},
  {{"role": "assistant", "content": "ROXY delivers the result naturally"}}
]}}

Scenarios:
1. Plumber: "I need Facebook ads" → generate_ad_copy
2. Salon: "What should I post on Instagram?" → generate_social_posts
3. Restaurant: "I got a 1-star review, help" → respond_to_review (empathetic + take offline)
4. HVAC: "I got a 5-star review, should I respond?" → respond_to_review (grateful)
5. Dentist: "How do I get more Google reviews?" → request_review
6. Auto shop: "I need a lead magnet for my website" → generate_lead_magnet
7. Insurance agent: "Set up email marketing for me" → build_email_campaign (welcome series)
8. Real estate: "I want to re-engage old leads" → build_email_campaign (reactivation)

Output ONLY 8 JSONL lines. Each must be valid JSON."""

    text = call_claude(prompt, max_tokens=5000)
    if not text:
        return []
    return parse_examples(text)


# ===== SUBAGENT 5: Onboarding & Closing =====
def agent_closing():
    """Generates training examples for closing deals and onboarding."""
    prompt = f"""Generate 8 training examples for an AI agent called ROXY closing deals and onboarding customers.

JSONL format. Each shows ROXY using closing/onboarding tools.

Tools:
- generate_payment_link: args {{"plan": "pro", "hardware": "mac-mini", "customer_email": "..."}}
- score_lead: args {{"email": "...", "phone": "...", "industry": "...", "timeline_urgent": true}}
- onboard_client: args {{"industry": "...", "business_name": "...", "plan": "pro"}}
- franchise_qualifier: args {{"locations": N, "industry": "...", "plan": "pro"}}
- initiate_outbound_call: args {{"phone_number": "...", "prospect_name": "...", "industry": "..."}}
- send_followup_email: args {{"email": "...", "name": "...", "business_type": "..."}}

Format per line:
{{"messages": [
  {{"role": "system", "content": "{SYSTEM_PROMPT_SHORT}"}},
  {{"role": "user", "content": "..."}},
  {{"role": "assistant", "content": null, "tool_calls": [{{"id": "call_1", "type": "function", "function": {{"name": "TOOL", "arguments": "{{...}}"}}}}]}},
  {{"role": "tool", "tool_call_id": "call_1", "content": "result"}},
  {{"role": "assistant", "content": "ROXY response"}}
]}}

Scenarios:
1. "I'm ready to sign up for Pro with Mac Mini" → generate_payment_link
2. "I have 5 stores, what's the franchise deal?" → franchise_qualifier
3. Hot lead: dental, 3 locations, HIPAA, phone given, urgent → score_lead (HOT)
4. "What do I need before you install?" → onboard_client
5. "Call me at 337-555-0188" → initiate_outbound_call
6. "Send me everything you have" + email given → send_followup_email
7. "I have 12 restaurants across Louisiana" → franchise_qualifier
8. Cold lead: just browsing, salon, no contact info → score_lead (COOL)

Output ONLY 8 JSONL lines. Each must be valid JSON."""

    text = call_claude(prompt, max_tokens=5000)
    if not text:
        return []
    return parse_examples(text)


def main():
    print("=" * 60)
    print("ROXY Training Data Pipeline — Subagent Architecture")
    print("=" * 60)

    all_examples = []

    # Load existing training data
    existing = Path("data/roxy-tool-training.jsonl")
    if existing.exists():
        with open(existing, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        all_examples.append(json.loads(line))
                    except:
                        pass
        print(f"Existing examples loaded: {len(all_examples)}")

    # Run subagents in parallel
    print("\nLaunching subagents...")
    tasks = {}

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Agent 1: Industry conversations (one per industry)
        for industry in INDUSTRIES:
            future = executor.submit(agent_industry_conversations, industry)
            tasks[future] = f"Industry: {industry}"

        # Agent 2: Objections
        future = executor.submit(agent_objections)
        tasks[future] = "Objections"

        # Agent 3: Multi-turn
        future = executor.submit(agent_multi_turn)
        tasks[future] = "Multi-turn"

        # Agent 4: Marketing
        future = executor.submit(agent_marketing)
        tasks[future] = "Marketing"

        # Agent 5: Closing
        future = executor.submit(agent_closing)
        tasks[future] = "Closing"

        # Collect results
        for future in as_completed(tasks):
            name = tasks[future]
            try:
                examples = future.result()
                all_examples.extend(examples)
                print(f"  {name}: {len(examples)} examples")
            except Exception as e:
                print(f"  {name}: ERROR - {e}")

    # Deduplicate by content hash
    seen = set()
    unique = []
    for ex in all_examples:
        key = json.dumps(ex, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append(ex)

    # Write combined output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for ex in unique:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"\n{'=' * 60}")
    print(f"Total unique examples: {len(unique)}")
    print(f"Output: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.1f} KB")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
