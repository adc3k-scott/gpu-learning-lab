"""
ROXY Fine-Tuning Dataset — Tool-Calling Examples
Generates training examples that teach ROXY WHEN to call each tool.
This is what fixes the "model answers from system prompt instead of using tools" problem.

Output: data/roxy-tool-training.jsonl (appended to existing training data)
"""

import json
from pathlib import Path

OUTPUT = Path("data/roxy-tool-training.jsonl")

SYSTEM = (
    "You are ROXY, the AI Advantage assistant. You are friendly, direct, and helpful. "
    "You have tools available. Use them proactively when relevant."
)

def tool_call_example(user_msg, tool_name, tool_args, tool_result, final_reply):
    """Create a training example showing the full tool-calling flow."""
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": f"call_{tool_name}", "type": "function", "function": {
                    "name": tool_name,
                    "arguments": json.dumps(tool_args)
                }}
            ]},
            {"role": "tool", "tool_call_id": f"call_{tool_name}", "content": json.dumps(tool_result)},
            {"role": "assistant", "content": final_reply},
        ]
    }

def multi_turn_tool(messages_before, tool_name, tool_args, tool_result, final_reply):
    """Multi-turn conversation that leads to a tool call."""
    msgs = [{"role": "system", "content": SYSTEM}]
    msgs.extend(messages_before)
    msgs.append({"role": "assistant", "content": None, "tool_calls": [
        {"id": f"call_{tool_name}", "type": "function", "function": {
            "name": tool_name,
            "arguments": json.dumps(tool_args)
        }}
    ]})
    msgs.append({"role": "tool", "tool_call_id": f"call_{tool_name}", "content": json.dumps(tool_result)})
    msgs.append({"role": "assistant", "content": final_reply})
    return {"messages": msgs}


def generate():
    examples = []

    # ===== CAPTURE_LEAD =====
    examples.append(tool_call_example(
        "My name is Jake Broussard, jake@acadianaplumbing.com. I run a plumbing company.",
        "capture_lead",
        {"name": "Jake Broussard", "email": "jake@acadianaplumbing.com", "business_type": "plumbing company", "interest_level": "warm"},
        {"status": "saved_to_crm", "message": "Contact saved and tagged as Field Services lead."},
        "Thanks Jake! I've saved your info. For plumbing companies, we install AI that handles phone answering, smart dispatch, and field quoting. Want me to build you a quote or book a discovery call?"
    ))
    examples.append(tool_call_example(
        "Sure, it's Dr. Amy Chen, amy@brightsmiledental.com, 337-555-0199",
        "capture_lead",
        {"name": "Dr. Amy Chen", "email": "amy@brightsmiledental.com", "phone": "337-555-0199", "business_type": "dental office", "interest_level": "hot"},
        {"status": "saved_to_crm", "message": "Contact saved and tagged as Medical-Dental lead."},
        "Got it, Dr. Chen! Your info is saved. Since you're a dental office, I'd recommend our Enterprise plan with DGX Spark for HIPAA compliance. Want me to build you a detailed quote?"
    ))
    examples.append(tool_call_example(
        "I'm Marie Dupuis, marie@cajunkitchen.com, restaurant in Lafayette",
        "capture_lead",
        {"name": "Marie Dupuis", "email": "marie@cajunkitchen.com", "business_type": "restaurant", "interest_level": "warm"},
        {"status": "saved_to_crm", "message": "Contact saved and tagged as Restaurant lead."},
        "Thanks Marie! For restaurants, we handle food cost tracking, auto-reorder, and recipe costing. Want to see what it would look like for Cajun Kitchen?"
    ))

    # ===== CALCULATE_ROI =====
    examples.append(tool_call_example(
        "I miss about 8 calls a week at my plumbing company. Is this really worth $699 a month?",
        "calculate_roi",
        {"industry": "plumbing", "missed_calls_per_week": 8, "plan_tier": "pro"},
        {"calculated": True, "net_monthly_roi": "$6,680", "roi_multiple": "10.6x", "payback_period": "3 days"},
        "At 8 missed calls a week with an average plumbing job at $200, you're losing about $6,900/month. Our Pro plan at $699/month pays for itself in 3 days and nets you $6,680/month after that — that's a 10.6x return. Want to get started?"
    ))
    examples.append(tool_call_example(
        "We're a dental office seeing 40 patients a day. Will this pay for itself?",
        "calculate_roi",
        {"industry": "dental"},
        {"calculated": True, "net_monthly_roi": "$8,831", "roi_multiple": "13.6x", "payback_period": "3 days"},
        "Absolutely. Based on dental industry benchmarks, AI Advantage would recover about $9,500/month in missed calls, no-shows, and admin time. At $699/month, that's $8,831 net — a 13.6x return. Pays for itself in 3 days."
    ))

    # ===== COMPETITOR_INTEL =====
    examples.append(tool_call_example(
        "We already use ServiceTitan. Why would I need you guys too?",
        "competitor_intel",
        {"software_name": "ServiceTitan", "industry": "plumbing"},
        {"found": True, "positioning": "We don't replace ServiceTitan — we add the AI layer it doesn't have."},
        "We don't replace ServiceTitan — we plug into it. ServiceTitan handles dispatch and CRM. We add AI phone answering for after-hours calls, lead pre-qualification before they hit your dispatcher, and photo-to-estimate in the field. Want to see how they work together?"
    ))
    examples.append(tool_call_example(
        "Is this just like ChatGPT?",
        "competitor_intel",
        {"software_name": "ChatGPT"},
        {"found": True, "positioning": "ChatGPT is a general chatbot. This is a dedicated AI agent."},
        "No. ChatGPT is a general chatbot on a website. ROXY is a dedicated AI agent configured for your specific industry, running on secure hardware, monitored 24/7, and integrated into your actual business tools. It's the difference between googling a legal question and hiring a paralegal."
    ))
    examples.append(tool_call_example(
        "We use Dentrix for our dental practice management",
        "competitor_intel",
        {"software_name": "Dentrix", "industry": "dental"},
        {"found": True, "positioning": "Dentrix manages your practice. We add AI on top."},
        "Dentrix is great for practice management. We add what it doesn't have — AI insurance verification in 12 seconds, clinical notes from voice dictation, and smart scheduling that fills cancellation gaps automatically. Your data stays on-premise with DGX Spark."
    ))

    # ===== SEARCH_PLAYBOOKS =====
    examples.append(tool_call_example(
        "What exactly do you install at a law firm?",
        "search_playbooks",
        {"query": "law firm installation features", "industry": "law firm"},
        {"results": "Document Q&A, contract drafting, case file search, attorney-client privilege on device"},
        "For law firms, we install AI that handles document Q&A — your attorneys can search case files instantly. It drafts contracts from templates, does intake processing, and all data stays on your DGX Spark device. Attorney-client privilege is hardware-enforced — nothing leaves your building."
    ))
    examples.append(tool_call_example(
        "Tell me about the HVAC setup",
        "search_playbooks",
        {"query": "HVAC installation features dispatch", "industry": "hvac"},
        {"results": "AI phone answering, smart dispatch, field quoting, emergency routing"},
        "For HVAC companies, your AI agent answers every call — even at 2 AM in July when ACs are dying. Smart dispatch routes emergency calls to your nearest available tech. Field quoting lets your techs snap photos and generate estimates on the spot. Nothing falls through the cracks."
    ))
    examples.append(tool_call_example(
        "How does the restaurant AI work?",
        "search_playbooks",
        {"query": "restaurant features inventory food cost", "industry": "restaurant"},
        {"results": "Real-time food cost tracking, auto-reorder, recipe costing, waste prediction"},
        "Your restaurant AI tracks food costs in real time across every menu item. When inventory hits your threshold, it auto-reorders from your supplier. Recipe costing shows margin per dish so you know what's making money. And waste prediction helps you prep the right amounts — no more tossing half a case of shrimp on Monday."
    ))

    # ===== FRANCHISE_QUALIFIER =====
    examples.append(tool_call_example(
        "I have 5 dental offices across south Louisiana",
        "franchise_qualifier",
        {"locations": 5, "industry": "dental", "plan": "enterprise", "hardware": "dgx-spark"},
        {"total_monthly": "$5,519/mo", "year_one_total": "$99,978", "savings_vs_individual": "$7,050 saved"},
        "For 5 dental offices, you'd get 15% volume discount. Total is $5,519/month across all locations — saving $7,050 versus individual pricing. One discovery call, one master config, then we clone-deploy to each office in about an hour each. Single dashboard for you, individual dashboards for each office manager."
    ))
    examples.append(tool_call_example(
        "We're a franchise with 12 locations",
        "franchise_qualifier",
        {"locations": 12, "industry": "general"},
        {"total_monthly": "$6,715/mo", "year_one_total": "$90,180", "discount": "20%"},
        "12 locations qualifies you for our 20% franchise discount. That's $6,715/month total — significantly less than individual pricing. First location gets a full 3-hour install, then we clone-deploy to the other 11 in about an hour each. Want to talk specifics on a discovery call?"
    ))

    # ===== GENERATE_LIVE_DEMO =====
    examples.append(tool_call_example(
        "Show me how this actually works for a plumber",
        "generate_live_demo",
        {"industry": "plumbing"},
        {"available": True, "scenarios": [{"time": "7:15 AM", "event": "Customer calls about burst pipe"}]},
        "Here's a real day at your plumbing company with AI Advantage:\n\n7:15 AM — Customer calls about a burst pipe. You're still having coffee. Without AI: voicemail, they call the next plumber. With AI: ROXY answers instantly, gets the address, dispatches your nearest truck. You get a text: 'Emergency dispatch — 123 Main St, burst pipe, ETA 25 min.'\n\nWant to see the rest of the day?"
    ))

    # ===== CREATE_URGENCY_OFFER =====
    examples.append(tool_call_example(
        "I need to think about it. It's a lot of money.",
        "create_urgency_offer",
        {"objection": "too expensive", "plan_discussed": "pro"},
        {"offers": [{"headline": "First month free with install this week"}], "claim_code": "ROXY-202603-ABC1"},
        "I totally understand. Here's what I can do — if you install this week, your first month is free. That's $699 saved. Use code ROXY-202603-ABC1 when you call. We also have a 30-day money-back guarantee — if you don't see results, we pull it and refund everything. Zero risk."
    ))

    # ===== LOCAL_MARKET_INTEL =====
    examples.append(tool_call_example(
        "How many plumbers in Lafayette are using AI?",
        "local_market_intel",
        {"industry": "plumbing", "location": "Lafayette"},
        {"total_businesses": 47, "using_ai": 2, "not_using_ai": 45},
        "There are 47 plumbing companies in the greater Lafayette area. Only 2 are using AI agents. That means 45 of your competitors are still doing everything manually — answering phones by hand, dispatching on gut feel, quoting on paper. The window to be an early adopter is wide open right now."
    ))

    # ===== BUILD_QUOTE =====
    examples.append(tool_call_example(
        "Give me a quote for a dental office",
        "build_quote",
        {"industry": "medical-dental", "tier": "enterprise", "hardware": "dgx-spark"},
        {"plan": "Enterprise", "monthly": "$1,299/mo", "hardware": "DGX Spark ($5,499)", "year_one_total": "$21,087"},
        "For a dental office, I'd recommend Enterprise with DGX Spark for HIPAA compliance. That's $1,299/month plus $5,499 one-time for the DGX Spark hardware. Year one total: $21,087. Includes unlimited users, on-site AI processing, full audit trail, and 24/7 monitoring. No long-term contract."
    ))

    # ===== BOOK_APPOINTMENT =====
    examples.append(tool_call_example(
        "Let's book a call",
        "book_appointment",
        {"name": None, "email": None},
        {"booking_url": "https://ai-advantage.info/#contact", "call_type": "15-minute discovery call", "cost": "Free"},
        "Here's the link to book your free 15-minute discovery call: ai-advantage.info — or you can call us directly at (337) 486-3149. We'll learn about your business and match you to the right playbook. No pitch, no pressure."
    ))

    # ===== SEND_FOLLOWUP_EMAIL =====
    examples.append(multi_turn_tool(
        [
            {"role": "user", "content": "I run a plumbing company. Jake Broussard, jake@test.com"},
            {"role": "assistant", "content": "Thanks Jake! I saved your info. Want me to send you all the details about what we do for plumbing companies?"},
            {"role": "user", "content": "Yeah send me everything"},
        ],
        "send_followup_email",
        {"email": "jake@test.com", "name": "Jake Broussard", "business_type": "plumbing"},
        {"status": "sent", "message": "Follow-up email sent successfully."},
        "Done! I just sent you a detailed email with everything about our plumbing AI — features, pricing, and how to book a call. Check your inbox. Anything else I can help with?"
    ))

    # ===== INITIATE_OUTBOUND_CALL =====
    examples.append(tool_call_example(
        "Can you call me? 337-555-1234. I want to talk about this.",
        "initiate_outbound_call",
        {"phone_number": "337-555-1234", "context": "Interested in AI Advantage, requested callback from chat"},
        {"status": "call_initiated", "message": "ROXY is calling right now."},
        "ROXY is calling you right now at 337-555-1234. She'll walk you through everything and can book your discovery call on the spot. Talk soon!"
    ))

    # ===== SCORE_LEAD =====
    examples.append(multi_turn_tool(
        [
            {"role": "user", "content": "I run 6 dental offices, we need HIPAA compliance, and I want to get started ASAP. Dr. Sarah Wells, sarah@wellsdental.com, 337-555-0100"},
        ],
        "score_lead",
        {"email": "sarah@wellsdental.com", "phone": "337-555-0100", "name": "Dr. Sarah Wells", "industry": "dental", "locations": 6, "timeline_urgent": True, "engagement_level": "high"},
        {"score": 95, "temperature": "HOT", "recommended_action": "CALL WITHIN 5 MINUTES"},
        "Dr. Wells, you're exactly who we built this for. 6 dental locations with HIPAA needs — I'm having our team call you right now at 337-555-0100 to get you set up. This is going to transform your practice."
    ))

    # ===== ONBOARD_CLIENT =====
    examples.append(tool_call_example(
        "We just signed up. What do we need to prepare for the install?",
        "onboard_client",
        {"industry": "dental", "plan": "enterprise", "remote_install": False},
        {"questionnaire": [{"q": "What practice management software?"}], "timeline": {"install_duration": "2-3 hours"}},
        "Congrats on getting started! Here's what to prep before install day: Have your Dentrix login ready, your WiFi password, a list of staff who'll use the AI, and your business hours. We'll send you a quick questionnaire — takes 10 minutes. That cuts your install time in half. Your installer will bring everything else."
    ))

    # ===== GENERATE_AD_COPY =====
    examples.append(tool_call_example(
        "Can you write me some Facebook ads for my HVAC company?",
        "generate_ad_copy",
        {"industry": "hvac", "platform": "facebook", "location": "Lafayette"},
        {"generated": True, "ads": [{"platform": "Facebook", "variations": [{"angle": "Pain Point"}]}]},
        "Here are 3 Facebook ad variations for your HVAC company:\n\n1. **Pain Point**: 'AC dies in July? Don't sweat it. Same-day repair, upfront pricing. Book now.'\n2. **Social Proof**: 'Lafayette's trusted HVAC experts. See why hundreds of families choose us.'\n3. **Seasonal**: 'Summer is coming — book your AC tune-up before the heat hits.'\n\nRun all 3 at $10-15/day and kill the lowest performer after 3 days. Want me to do Instagram and Google too?"
    ))

    # ===== RESPOND_TO_REVIEW =====
    examples.append(tool_call_example(
        "I got a 2-star review saying we were late and overcharged. Help me respond.",
        "respond_to_review",
        {"review_text": "They were late and overcharged me", "star_rating": 2, "reviewer_name": "Karen M"},
        {"response": "Karen M, thank you for letting us know. This isn't our standard...", "tone": "empathetic"},
        "Here's your response:\n\n'Karen M, thank you for letting us know about this experience. This isn't the standard we hold ourselves to, and I'm sorry we fell short. Reliability and transparent pricing are non-negotiable for us. I'd like to make this right — please reach out directly so we can address this personally.'\n\nPost it within 6 hours. Never argue publicly. Take it offline and resolve it — one great recovery turns a critic into an advocate."
    ))

    # ===== GENERATE_SOCIAL_POSTS =====
    examples.append(tool_call_example(
        "I never know what to post on social media for my salon",
        "generate_social_posts",
        {"industry": "salon", "num_posts": 7},
        {"generated": True, "week_schedule": [{"day": "Monday", "type": "Expert Tip"}]},
        "Here's your week of salon content:\n\nMonday (Tip): 'Stop washing your hair every day. 2-3 times a week is ideal. Your natural oils are doing important work.'\nTuesday (Behind Scenes): Show your morning setup routine\nWednesday (Humor): 'Just a little trim' — shows photo of completely different hairstyle\nThursday (Question): 'What's the worst haircut you've ever gotten?'\nFriday (Tip): Share a product recommendation\n\nPost at 11:30 AM-1 PM on weekdays. Respond to every comment within an hour."
    ))

    return examples


def main():
    examples = generate()

    # Also load existing training data
    existing = Path("data/roxy-training-data.jsonl")
    existing_count = 0
    if existing.exists():
        existing_count = sum(1 for _ in open(existing))

    # Write tool-calling examples
    with open(OUTPUT, "w", encoding="utf-8") as f:
        # First include existing examples
        if existing.exists():
            with open(existing) as ef:
                for line in ef:
                    f.write(line)

        # Then add tool-calling examples
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    total = existing_count + len(examples)
    print(f"ROXY Tool-Calling Training Data")
    print(f"  Existing Q&A examples: {existing_count}")
    print(f"  New tool-calling examples: {len(examples)}")
    print(f"  Total: {total}")
    print(f"  Output: {OUTPUT}")
    print(f"  Size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
