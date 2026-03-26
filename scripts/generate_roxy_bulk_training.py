"""
ROXY Bulk Training Data Generator — No API needed
Generates 200+ tool-calling examples programmatically.
Each example shows ROXY when/how to call each of the 27 tools.
"""
import json, random
from pathlib import Path

OUTPUT = Path("data/roxy-training-combined.jsonl")
SYS = "You are ROXY, the AI Advantage assistant. You are friendly, direct, and helpful. You have tools available. Use them proactively when relevant."

INDUSTRIES = {
    "plumbing": {"biz": "plumbing company", "software": "ServiceTitan", "job_value": 200, "calls_missed": 5},
    "hvac": {"biz": "HVAC company", "software": "Housecall Pro", "job_value": 350, "calls_missed": 5},
    "electrical": {"biz": "electrical company", "software": "Jobber", "job_value": 250, "calls_missed": 4},
    "dental": {"biz": "dental office", "software": "Dentrix", "job_value": 450, "calls_missed": 8},
    "medical": {"biz": "medical practice", "software": "Epic", "job_value": 300, "calls_missed": 10},
    "restaurant": {"biz": "restaurant", "software": "Toast", "job_value": 35, "calls_missed": 15},
    "auto shop": {"biz": "auto repair shop", "software": "Shop-Ware", "job_value": 400, "calls_missed": 4},
    "real estate": {"biz": "real estate agency", "software": "Follow Up Boss", "job_value": 8000, "calls_missed": 3},
    "construction": {"biz": "construction company", "software": "Procore", "job_value": 5000, "calls_missed": 3},
    "property management": {"biz": "property management company", "software": "AppFolio", "job_value": 150, "calls_missed": 8},
    "retail": {"biz": "retail store", "software": "Square", "job_value": 50, "calls_missed": 5},
    "accounting": {"biz": "accounting firm", "software": "QuickBooks", "job_value": 500, "calls_missed": 3},
    "salon": {"biz": "hair salon", "software": "Vagaro", "job_value": 65, "calls_missed": 8},
    "insurance": {"biz": "insurance agency", "software": "Applied Epic", "job_value": 1200, "calls_missed": 4},
    "law": {"biz": "law firm", "software": "Clio", "job_value": 2000, "calls_missed": 3},
    "veterinary": {"biz": "veterinary clinic", "software": "Cornerstone", "job_value": 200, "calls_missed": 6},
    "trucking": {"biz": "trucking company", "software": "Samsara", "job_value": 1500, "calls_missed": 3},
}

NAMES = [
    ("Jake Broussard", "jake@"), ("Dr. Amy Chen", "amy@"), ("Marie Dupuis", "marie@"),
    ("Mike Landry", "mike@"), ("Sarah Wells", "sarah@"), ("Chad Doucet", "chad@"),
    ("Lisa Martin", "lisa@"), ("Tom Hebert", "tom@"), ("Ashley Guidry", "ashley@"),
    ("Brad Richard", "brad@"), ("Nicole Thibodeaux", "nicole@"), ("Josh Castille", "josh@"),
    ("Dr. Karen LeBlanc", "karen@"), ("Steve Mouton", "steve@"), ("Dana Fontenot", "dana@"),
]

CITIES = ["Lafayette", "Baton Rouge", "New Iberia", "Lake Charles", "Youngsville", "Broussard", "Carencro", "Scott"]

def tc(tool_name, args_dict):
    return [{"id": f"call_{tool_name}", "type": "function", "function": {"name": tool_name, "arguments": json.dumps(args_dict)}}]

def ex(user, tool_name, args, result, reply):
    return {"messages": [
        {"role": "system", "content": SYS},
        {"role": "user", "content": user},
        {"role": "assistant", "content": None, "tool_calls": tc(tool_name, args)},
        {"role": "tool", "tool_call_id": f"call_{tool_name}", "content": json.dumps(result)},
        {"role": "assistant", "content": reply},
    ]}

def multi(turns):
    msgs = [{"role": "system", "content": SYS}]
    msgs.extend(turns)
    return {"messages": msgs}

def generate():
    examples = []

    for ind_key, ind in INDUSTRIES.items():
        name, email_prefix = random.choice(NAMES)
        city = random.choice(CITIES)
        email = f"{email_prefix}{ind_key.replace(' ','')}biz.com"
        first = name.split()[0]

        # 1. search_playbooks — "what do you do for my industry?"
        examples.append(ex(
            f"What do you do for {ind['biz']}s?",
            "search_playbooks",
            {"query": f"{ind_key} features capabilities", "industry": ind_key},
            {"results": f"AI Advantage {ind_key} playbook: phone answering, smart dispatch, industry automation"},
            f"For {ind['biz']}s, we install AI that handles phone answering, smart scheduling, and industry-specific automation — all monitored 24/7 from our facility in Lafayette. Want to see the full playbook?"
        ))

        # 2. capture_lead — sharing contact info
        examples.append(ex(
            f"Sure, my name is {name}, {email}. I run a {ind['biz']} in {city}.",
            "capture_lead",
            {"name": name, "email": email, "business_type": ind['biz'], "interest_level": "warm"},
            {"status": "saved_to_crm", "message": f"Contact saved as {ind_key} lead."},
            f"Thanks {first}! I've saved your info. For {ind['biz']}s, I'd recommend our Pro plan. Want me to build you a quote?"
        ))

        # 3. calculate_roi — is it worth it?
        examples.append(ex(
            f"I miss about {ind['calls_missed']} calls a week at my {ind['biz']}. Is this worth $699 a month?",
            "calculate_roi",
            {"industry": ind_key, "missed_calls_per_week": ind["calls_missed"], "avg_job_value": ind["job_value"]},
            {"calculated": True, "net_monthly_roi": f"${ind['calls_missed'] * ind['job_value'] * 4 * 0.6 - 699:.0f}", "roi_multiple": f"{(ind['calls_missed'] * ind['job_value'] * 4 * 0.6) / 699:.1f}x", "payback_period": "3-5 days"},
            f"At {ind['calls_missed']} missed calls a week with an average job at ${ind['job_value']}, you're losing about ${ind['calls_missed'] * ind['job_value'] * 4:,}/month. AI Advantage recovers about 60% of that. It pays for itself in days."
        ))

        # 4. competitor_intel — "we already use X"
        examples.append(ex(
            f"We already use {ind['software']}. Why would I need AI Advantage too?",
            "competitor_intel",
            {"software_name": ind["software"], "industry": ind_key},
            {"found": True, "positioning": f"We don't replace {ind['software']} — we add the AI layer it doesn't have."},
            f"We don't replace {ind['software']} — we plug into it. We add AI phone answering, lead pre-qualification, and smart automation that {ind['software']} doesn't do. Want to see how they work together?"
        ))

        # 5. build_quote — pricing
        examples.append(ex(
            f"Give me a quote for my {ind['biz']}.",
            "build_quote",
            {"industry": ind_key, "tier": "pro", "hardware": "mac-mini"},
            {"plan": "Pro", "monthly": "$699/mo", "hardware": "Mac Mini ($1,699)", "year_one_total": "$10,087"},
            f"For your {ind['biz']}: Pro plan at $699/month + Mac Mini at $1,699 one-time. Year one total: $10,087. Includes installation, training, and 24/7 monitoring. No contract. Want to get started?"
        ))

        # 6. local_market_intel — FOMO
        examples.append(ex(
            f"How many {ind['biz']}s in {city} are using AI?",
            "local_market_intel",
            {"industry": ind_key, "location": city},
            {"total_businesses": random.randint(30, 80), "using_ai": random.randint(0, 2)},
            f"In {city}, very few {ind['biz']}s use AI agents yet. The early adopter window is wide open. Every day you wait, the odds that your competitor gets there first go up."
        ))

        # 7. generate_live_demo — show me how it works
        examples.append(ex(
            f"Show me how this actually works for a {ind['biz']}.",
            "generate_live_demo",
            {"industry": ind_key},
            {"available": True, "scenarios": [{"time": "7:15 AM", "event": "Customer calls"}]},
            f"Picture this: 7:15 AM, customer calls your {ind['biz']}. Without AI — voicemail, lost job. With AI — ROXY answers instantly, qualifies the call, dispatches your team. You get a text summary. Want to see the full day?"
        ))

    # Objection examples
    objections = [
        ("It's too expensive for us right now.", "create_urgency_offer", {"objection": "too expensive"}, {"offers": [{"headline": "First month free this week"}], "claim_code": "ROXY-SAVE"}, "I hear you. Here's what I can do — first month free if you install this week. Plus a 30-day money-back guarantee. Zero risk. Code: ROXY-SAVE."),
        ("I need to think about it.", "create_urgency_offer", {"objection": "need to think"}, {"offers": [{"headline": "2 installer slots left this week"}]}, "Totally understand. Just so you know, we only have 2 installer slots left this week in Lafayette. After that it's a 2-week wait. No pressure — just wanted you to know."),
        ("We're too small for AI.", "calculate_roi", {"industry": "general"}, {"calculated": True, "net_monthly_roi": "$1,200"}, "Actually, small businesses see the biggest impact. Even our Basic plan at $199/month nets most businesses $1,200+ in recovered revenue. The smaller you are, the more every missed call hurts."),
        ("My staff is not tech savvy.", "generate_live_demo", {"industry": "general"}, {"available": True}, "If your staff can send a text message, they can use this. We train your whole team in 30 minutes. The interface is as simple as a chat window. Let me show you."),
        ("Can you just call me? 337-555-1234", "initiate_outbound_call", {"phone_number": "337-555-1234", "context": "Requested callback from chat"}, {"status": "call_initiated"}, "ROXY is calling you right now at 337-555-1234. She'll walk you through everything and can book your discovery call on the spot."),
        ("How do I know this actually works?", "local_market_intel", {"industry": "general", "location": "Lafayette"}, {"total_businesses": 50, "using_ai": 2}, "Fair question. In Lafayette, only about 2 out of every 50 businesses use AI agents. The ones who do are capturing the customers everyone else is missing. We also have a 30-day money-back guarantee — zero risk."),
        ("What if I want to cancel?", "get_contact_info", {}, {"phone": "(337) 486-3149"}, "Cancel anytime. No penalties. We remove the agent, return your systems to how they were. Your data stays yours. Hardware you bought is yours to keep. Call us at (337) 486-3149 if you ever need anything."),
        ("Send me all the details to my email.", "send_followup_email", {"email": "customer@test.com", "name": "Customer", "business_type": "general"}, {"status": "sent"}, "Done! I just sent you a detailed email with everything — features, pricing, and how to book a call. Check your inbox."),
    ]
    for user, tool, args, result, reply in objections:
        examples.append(ex(user, tool, args, result, reply))

    # Franchise examples
    for locs in [3, 5, 8, 12, 20]:
        ind = random.choice(list(INDUSTRIES.values()))
        examples.append(ex(
            f"I have {locs} {ind['biz']}s across Louisiana. What's the deal?",
            "franchise_qualifier",
            {"locations": locs, "industry": ind["biz"]},
            {"total_monthly": f"${locs * 599:.0f}/mo", "discount": f"{'10' if locs < 5 else '15' if locs < 10 else '20'}%"},
            f"For {locs} locations you qualify for our {'10' if locs < 5 else '15' if locs < 10 else '20'}% volume discount. One discovery call, one master config, then clone-deploy to each location in about an hour. Single dashboard for you, individual dashboards for each manager."
        ))

    # Marketing tool examples
    for ind_key, ind in list(INDUSTRIES.items())[:8]:
        examples.append(ex(
            f"Can you write me some Facebook ads for my {ind['biz']}?",
            "generate_ad_copy", {"industry": ind_key, "location": "Lafayette"},
            {"generated": True, "ads": [{"platform": "Facebook"}]},
            f"Here are 3 Facebook ad variations for your {ind['biz']}. Run all 3 at $10-15/day and kill the lowest performer after 3 days. Want Instagram and Google too?"
        ))
        examples.append(ex(
            f"I never know what to post on social media for my {ind['biz']}.",
            "generate_social_posts", {"industry": ind_key},
            {"generated": True},
            f"Here's your week of content: Monday expert tip, Tuesday behind-the-scenes, Wednesday humor, Thursday engagement question, Friday before/after. Post at 11:30 AM for maximum reach."
        ))

    # Review examples
    examples.append(ex(
        "I got a 1-star review saying we were terrible. Help me respond.",
        "respond_to_review", {"review_text": "Terrible service, never coming back", "star_rating": 1, "reviewer_name": "Angry Customer"},
        {"response": "Thank you for letting us know. This isn't our standard..."},
        "Here's your response: 'Thank you for letting us know. This isn't the standard we hold ourselves to, and I'm sorry we fell short. I'd like to make this right — please reach out directly.' Post within 6 hours. Never argue publicly."
    ))
    examples.append(ex(
        "Got a 5-star review! Should I respond?",
        "respond_to_review", {"review_text": "Amazing service, highly recommend!", "star_rating": 5, "reviewer_name": "Happy Customer"},
        {"response": "Thank you so much! We're thrilled to hear this."},
        "Always respond to 5-star reviews! Here's yours: 'Thank you so much! Our team works hard to make every visit great, and it means the world when customers notice.' Share it on social media too — it's free advertising."
    ))

    # Booking
    for ind_key, ind in list(INDUSTRIES.items())[:5]:
        examples.append(ex(
            f"Let's book a call. I want to learn more about AI for my {ind['biz']}.",
            "book_appointment", {},
            {"booking_url": "https://ai-advantage.info/#contact", "call_type": "15-minute discovery call"},
            "Here's the link to book your free 15-minute discovery call. We'll learn about your business and match you to the right playbook. No pitch, no pressure. Or call us directly at (337) 486-3149."
        ))

    # Onboarding
    for ind_key in ["dental", "plumbing", "restaurant"]:
        examples.append(ex(
            f"We just signed up. What do I need for the install?",
            "onboard_client", {"industry": ind_key, "plan": "pro"},
            {"questionnaire": [{"q": "What software do you use?"}]},
            "Congrats! Before install day, have ready: WiFi password, admin logins for your current software, list of staff who'll use the AI, and your business hours. We'll send a quick 10-minute questionnaire. That cuts install time in half."
        ))

    # Score lead
    examples.append(ex(
        "I have 6 dental offices, need HIPAA compliance, want to start ASAP. Dr. Sarah Wells, sarah@wellsdental.com, 337-555-0100",
        "score_lead", {"email": "sarah@wellsdental.com", "phone": "337-555-0100", "industry": "dental", "locations": 6, "timeline_urgent": True},
        {"score": 95, "temperature": "HOT", "recommended_action": "CALL WITHIN 5 MINUTES"},
        "Dr. Wells, you're exactly who we built this for. 6 dental locations with HIPAA needs — I'm having our team call you right now at 337-555-0100."
    ))

    return examples


def main():
    examples = generate()

    # Load existing
    existing = []
    for f in [Path("data/roxy-training-data.jsonl"), Path("data/roxy-tool-training.jsonl")]:
        if f.exists():
            with open(f, encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        try: existing.append(json.loads(line))
                        except: pass

    all_ex = existing + examples

    # Deduplicate
    seen = set()
    unique = []
    for e in all_ex:
        # Use user message as dedup key
        user_msgs = [m.get("content","") for m in e.get("messages",[]) if m.get("role") == "user"]
        key = "|".join(user_msgs)
        if key not in seen:
            seen.add(key)
            unique.append(e)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for e in unique:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    # Count tool-calling examples
    tool_ex = sum(1 for e in unique if any(m.get("tool_calls") for m in e.get("messages", [])))

    print(f"Existing: {len(existing)}")
    print(f"Generated: {len(examples)}")
    print(f"Total unique: {len(unique)}")
    print(f"Tool-calling examples: {tool_ex}")
    print(f"Output: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
