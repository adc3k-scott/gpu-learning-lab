"""
ROXY v3 Training Data — Focused on gaps:
1. search_playbooks (30 examples forcing the tool)
2. respond_to_review (15 examples with proper structured format)
3. Multi-tool chains (15 examples with 2-3 tools per message)
"""
import json
from pathlib import Path

SYS = "You are ROXY, the AI Advantage assistant. You are friendly, direct, and helpful. You have tools available. Use them proactively when relevant."

def tc(name, args):
    return [{"id": f"call_{name}", "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}]

def ex(user, tool, args, result, reply):
    return {"messages": [
        {"role": "system", "content": SYS},
        {"role": "user", "content": user},
        {"role": "assistant", "content": None, "tool_calls": tc(tool, args)},
        {"role": "tool", "tool_call_id": f"call_{tool}", "content": json.dumps(result)},
        {"role": "assistant", "content": reply},
    ]}

def multi_tool(user, chain):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user}]
    for tool, args, result, reply in chain:
        msgs.append({"role": "assistant", "content": None, "tool_calls": tc(tool, args)})
        msgs.append({"role": "tool", "tool_call_id": f"call_{tool}", "content": json.dumps(result)})
        if reply:
            msgs.append({"role": "assistant", "content": reply})
    return {"messages": msgs}

examples = []

# ===== SEARCH_PLAYBOOKS (30 examples) =====
industries = [
    ("plumbing", "plumbing company", "phone answering, smart dispatch, field quoting, emergency routing"),
    ("hvac", "HVAC company", "AC repair dispatch, seasonal booking, maintenance scheduling"),
    ("dental", "dental office", "insurance verification, clinical notes, smart scheduling, HIPAA compliance"),
    ("restaurant", "restaurant", "food cost tracking, auto-reorder, recipe costing, waste prediction"),
    ("law", "law firm", "document Q&A, contract drafting, case file search, attorney-client privilege on-device"),
    ("salon", "salon", "automated rebooking, no-show follow-ups, client history, schedule optimization"),
    ("auto shop", "auto repair shop", "photo-to-estimate, customer approval workflows, parts ordering"),
    ("real estate", "real estate agency", "speed-to-lead response, listing descriptions, CRM automation"),
    ("construction", "construction company", "change orders, draw schedules, daily logs, subcontractor coordination"),
    ("insurance", "insurance agency", "multi-carrier quoting, renewal tracking, policy comparison"),
    ("accounting", "accounting firm", "tax document intake, deadline tracking, client portal, data extraction"),
    ("property management", "property management company", "maintenance dispatch, tenant portal, owner reporting"),
    ("retail", "retail store", "auto-reorder, margin analysis, inventory prediction"),
    ("veterinary", "veterinary clinic", "appointment scheduling, patient records, prescription tracking"),
    ("trucking", "trucking company", "dispatch optimization, load tracking, compliance documentation"),
]

for ind, biz, features in industries:
    # Question 1: "What do you do for X?"
    examples.append(ex(
        f"What exactly do you do for {biz}s?",
        "search_playbooks",
        {"query": f"{ind} features capabilities", "industry": ind},
        {"results": f"AI Advantage {ind} playbook: {features}"},
        f"For {biz}s, we install AI that handles {features}. Everything monitored 24/7 from our facility in Lafayette. Want to see the full details?"
    ))
    # Question 2: "Tell me about your X solution"
    examples.append(ex(
        f"Tell me about your {ind} AI solution.",
        "search_playbooks",
        {"query": f"{ind} installation features details", "industry": ind},
        {"results": f"Full {ind} playbook: {features}. On-site install 2-3 hours. Training 30 min."},
        f"Our {ind} playbook covers {features}. We install in 2-3 hours, train your team in 30 minutes, and monitor 24/7. Want a quote?"
    ))

# ===== RESPOND_TO_REVIEW (15 examples) =====
reviews = [
    (1, "Terrible service. Waited 2 hours.", "Karen M", "Karen M, thank you for letting us know. This is not the standard we hold ourselves to. Reliability is something we pride ourselves on, and we clearly missed the mark. Please reach out directly so we can address this personally."),
    (2, "Overcharged by $200 and rude about it.", "Mike T", "Mike, transparent pricing is non-negotiable for us, and I want to review what happened. Please contact us directly so we can make this right."),
    (1, "Worst experience. Staff was unprofessional.", "Sarah L", "Sarah, every customer deserves to be treated with respect. I am sorry we fell short. Please reach out to us directly so we can address this personally."),
    (3, "It was okay. Nothing special.", "Tom B", "Tom, thank you for your feedback. We are always working to improve. We would love the chance to exceed your expectations next time."),
    (3, "Good food but slow service.", "Amy R", "Amy, we understand that wait times can be frustrating. Thank you for the kind words about the food. We are actively working to serve you faster."),
    (5, "Best plumber in Lafayette! Fixed our leak in 30 minutes.", "Chad D", "Thank you so much, Chad! We make it a priority to deliver fast, reliable service. We appreciate you trusting us!"),
    (5, "Amazing dental experience. So friendly.", "Happy Patient", "Thank you! Our team works hard to make every visit comfortable, and it means the world when patients notice."),
    (5, "Love this salon! Lisa always knows what I want.", "Loyal Client", "Thank you so much! Lisa will love hearing this. We appreciate your loyalty!"),
    (4, "Good work but pricey.", "Budget Bob", "Bob, thank you for the kind words. We strive to offer the best value for the quality of service we provide."),
    (2, "AC broke again 2 weeks after they fixed it.", "Fred", "Fred, we stand behind our work. This should not have happened. Please contact us directly and we will send a tech out at no additional charge."),
    (1, "No-show. Nobody showed up for my appointment.", "Angry Customer", "We sincerely apologize. This is completely unacceptable. Please contact us directly so we can reschedule immediately and make this right."),
    (5, "Incredible auto work. Honest pricing and fast turnaround.", "Happy Driver", "Thank you! Honest pricing and fast turnaround are exactly what we aim for every time. See you next time!"),
    (2, "They lost my paperwork and I had to resubmit everything.", "Frustrated Client", "We take document handling seriously and this should never have happened. Please reach out directly so we can resolve this and ensure it does not happen again."),
    (4, "Great service, just wish they had weekend hours.", "Weekend Worker", "Thank you for the kind words! We hear you on weekend hours and are looking into expanding our availability."),
    (5, "Moved here from Texas and these guys are the best I have found.", "New Resident", "Welcome to Louisiana! We are glad you found us and honored to be your go-to. Looking forward to taking care of you!"),
]

for stars, text, name, reply in reviews:
    tip = "Respond within 6 hours. Never argue publicly. Take it offline." if stars <= 2 else "Respond within 24 hours. Share on social media." if stars >= 4 else "Respond within 12 hours. Goal: turn this into a 5-star next visit."
    examples.append(ex(
        f"I got a {stars}-star review: \"{text}\" from {name}. Help me respond.",
        "respond_to_review",
        {"review_text": text, "star_rating": stars, "reviewer_name": name},
        {"response": reply, "tone": "empathetic" if stars <= 2 else "grateful" if stars >= 4 else "appreciative"},
        f"Here is your response:\n\n\"{reply}\"\n\n{tip}"
    ))

# ===== MULTI-TOOL CHAINS (15 examples) =====

# Pattern A: capture_lead + score_lead + send_followup_email (5 examples)
for ind, biz, features in industries[:5]:
    examples.append(multi_tool(
        f"My name is Test User, test@{ind.replace(' ','')}biz.com, 337-555-0100. I run a {biz}.",
        [
            ("capture_lead", {"name": "Test User", "email": f"test@{ind.replace(' ','')}biz.com", "phone": "337-555-0100", "business_type": biz, "interest_level": "hot"},
             {"status": "saved_to_crm"}, None),
            ("score_lead", {"email": f"test@{ind.replace(' ','')}biz.com", "phone": "337-555-0100", "industry": ind},
             {"score": 85, "temperature": "HOT"}, None),
            ("send_followup_email", {"email": f"test@{ind.replace(' ','')}biz.com", "name": "Test User", "business_type": biz},
             {"status": "sent"}, f"I saved your info, scored you as a hot lead, and sent you a detailed email about our {biz} solution. Our team will call you within 5 minutes!"),
        ]
    ))

# Pattern B: search_playbooks + calculate_roi + build_quote (5 examples)
for ind, biz, features in industries[5:10]:
    examples.append(multi_tool(
        f"I run a {biz} and miss about 8 calls a week. What do you do for us and how much?",
        [
            ("search_playbooks", {"query": f"{ind} features", "industry": ind},
             {"results": features}, None),
            ("calculate_roi", {"industry": ind, "missed_calls_per_week": 8},
             {"calculated": True, "net_monthly_roi": "$5,200", "roi_multiple": "8.4x"}, None),
            ("build_quote", {"industry": ind, "tier": "pro", "hardware": "mac-mini"},
             {"plan": "Pro", "monthly": "$699/mo", "year_one_total": "$10,087"},
             f"For {biz}s we handle {features}. At 8 missed calls a week, you recover about $5,200/month. That is 8.4x return on $699/month. Year one with Mac Mini: $10,087."),
        ]
    ))

# Pattern C: competitor_intel + calculate_roi + create_urgency_offer (5 examples)
competitors = [
    ("ServiceTitan", "plumbing"), ("Toast", "restaurant"), ("Dentrix", "dental"),
    ("QuickBooks", "accounting"), ("Vagaro", "salon"),
]
for sw, ind in competitors:
    examples.append(multi_tool(
        f"We already use {sw} and I am not sure I need this. Seems expensive.",
        [
            ("competitor_intel", {"software_name": sw, "industry": ind},
             {"positioning": f"We do not replace {sw}. We add the AI layer it does not have."}, None),
            ("calculate_roi", {"industry": ind},
             {"net_monthly_roi": "$3,500", "payback_period": "4 days"}, None),
            ("create_urgency_offer", {"objection": "too expensive"},
             {"offers": [{"headline": "First month free this week"}], "claim_code": "ROXY-SAVE"},
             f"We plug into {sw}, not replace it. The math: pays for itself in 4 days, nets $3,500/month. First month free this week with code ROXY-SAVE."),
        ]
    ))


# Load existing and combine
existing = []
for f in [Path("data/roxy-training-combined.jsonl")]:
    if f.exists():
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    try: existing.append(json.loads(line))
                    except: pass

all_ex = existing + examples
seen = set()
unique = []
for e in all_ex:
    user_msgs = [m.get("content","") for m in e.get("messages",[]) if m.get("role") == "user"]
    key = "|".join(str(u) for u in user_msgs)[:200]
    if key not in seen:
        seen.add(key)
        unique.append(e)

out = Path("data/roxy-training-v3.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for e in unique:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

tool_ex = sum(1 for e in unique if any(m.get("tool_calls") for m in e.get("messages",[])))
multi = sum(1 for e in unique if sum(1 for m in e.get("messages",[]) if m.get("tool_calls")) > 1)

print(f"Previous: {len(existing)}")
print(f"New: {len(examples)}")
print(f"Total unique: {len(unique)}")
print(f"Tool-calling: {tool_ex}")
print(f"Multi-tool chains: {multi}")
print(f"Size: {out.stat().st_size / 1024:.1f} KB")
