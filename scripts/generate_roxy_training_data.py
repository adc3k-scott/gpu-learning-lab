"""
ROXY Fine-Tuning Dataset Generator
Converts AI Advantage playbooks + core docs into conversation pairs.
Output: JSONL file ready for RunPod fine-tuning or HuggingFace upload.

Usage:
    python scripts/generate_roxy_training_data.py

Output:
    data/roxy-training-data.jsonl
"""

import json
import re
from pathlib import Path

PLAYBOOK_DIR = Path("ai-advantage/playbooks")
CORE_DOCS = [
    Path("ai-advantage/ally-prompt.md"),
    Path("ai-advantage/client-process.md"),
    Path("ai-advantage/README.md"),
    Path("ai-advantage/commission-structure.md"),
    Path("ai-advantage/referral-program.md"),
]
OUTPUT = Path("data/roxy-training-data.jsonl")

SYSTEM_PROMPT = (
    "You are ROXY, the AI Advantage assistant. You are friendly, direct, and helpful. "
    "AI Advantage installs dedicated AI agents for small businesses. Based in Lafayette, Louisiana. "
    "You run on ADC's own AI infrastructure — American-owned, American-built."
)

# Industry display names
INDUSTRY_NAMES = {
    "accounting-cpa": "accounting firm",
    "auto-shop": "auto repair shop",
    "construction": "construction company",
    "ecommerce": "e-commerce business",
    "field-services": "field services company",
    "government-municipal": "government office",
    "insurance": "insurance agency",
    "law-firm": "law firm",
    "medical-dental": "dental office",
    "nonprofit-church": "nonprofit organization",
    "property-management": "property management company",
    "real-estate": "real estate agency",
    "restaurant": "restaurant",
    "retail": "retail store",
    "salon-barber": "salon",
    "trucking-logistics": "trucking company",
    "veterinary": "veterinary clinic",
}


def parse_sections(md_text):
    """Split markdown into sections by headers."""
    sections = []
    current_title = ""
    current_body = []

    for line in md_text.split("\n"):
        m = re.match(r"^(#{1,3})\s+(.+)", line)
        if m:
            if current_body:
                body = "\n".join(current_body).strip()
                if len(body) > 30:
                    sections.append((current_title, body))
            current_title = m.group(2).strip()
            current_body = []
        else:
            current_body.append(line)

    if current_body:
        body = "\n".join(current_body).strip()
        if len(body) > 30:
            sections.append((current_title, body))

    return sections


def make_conversation(system, user, assistant):
    """Create a single training example in chat format."""
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]
    }


def generate_playbook_pairs(filename, content):
    """Generate Q&A pairs from a single playbook."""
    pairs = []
    stem = filename.stem
    industry = INDUSTRY_NAMES.get(stem, stem.replace("-", " "))
    sections = parse_sections(content)

    # General "what can you do for my industry" question
    intro_sections = [s for s in sections if s[0] and any(
        kw in s[0].lower() for kw in ["who this is for", "what you", "overview", "installer"]
    )]
    if intro_sections:
        answer_text = "\n".join(s[1][:500] for s in intro_sections[:2])
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"I run a {industry}. What can AI Advantage do for me?",
            clean_answer(answer_text, industry),
        ))

    # Install-specific questions
    install_sections = [s for s in sections if any(
        kw in s[0].lower() for kw in ["install", "setup", "steps", "before you leave"]
    )]
    if install_sections:
        answer_text = "\n".join(s[1][:500] for s in install_sections[:2])
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"What does the installation process look like for a {industry}?",
            clean_answer(answer_text, industry),
        ))

    # Training questions
    training_sections = [s for s in sections if "training" in s[0].lower()]
    if training_sections:
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"How do you train my staff at a {industry}?",
            clean_answer(training_sections[0][1][:500], industry),
        ))

    # Security / compliance questions
    security_sections = [s for s in sections if any(
        kw in s[0].lower() for kw in ["security", "hipaa", "compliance", "privacy", "not to do"]
    )]
    if security_sections:
        answer_text = "\n".join(s[1][:400] for s in security_sections[:2])
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"Is this secure for a {industry}? What about data privacy?",
            clean_answer(answer_text, industry),
        ))

    # Troubleshooting
    trouble_sections = [s for s in sections if "troubleshoot" in s[0].lower()]
    if trouble_sections:
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"What if something goes wrong with the AI at my {industry}?",
            clean_answer(trouble_sections[0][1][:500], industry),
        ))

    # Client requirements
    req_sections = [s for s in sections if "requirement" in s[0].lower()]
    if req_sections:
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"What do I need to have ready before you install at my {industry}?",
            clean_answer(req_sections[0][1][:500], industry),
        ))

    # Glossary / jargon
    glossary_sections = [s for s in sections if "glossary" in s[0].lower()]
    if glossary_sections:
        pairs.append(make_conversation(
            SYSTEM_PROMPT,
            f"Can you explain the technical terms you use for {industry} AI?",
            clean_answer(glossary_sections[0][1][:500], industry),
        ))

    return pairs


def clean_answer(text, industry=""):
    """Clean markdown formatting and make conversational."""
    # Strip markdown headers
    text = re.sub(r"^#{1,4}\s+.*$", "", text, flags=re.MULTILINE)
    # Strip bold/italic markers but keep text
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Clean up list items
    text = re.sub(r"^[-*]\s+", "- ", text, flags=re.MULTILINE)
    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    # Truncate if too long
    if len(text) > 600:
        text = text[:597] + "..."
    return text


def generate_pricing_pairs():
    """Generate pricing Q&A pairs."""
    pairs = []

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "How much does AI Advantage cost?",
        "We have three monthly plans: Basic at $199/month (1-2 users, core AI features), Pro at $699/month which is our most popular (up to 5 users, AI phone answering, full integrations), and Enterprise at $1,299/month (unlimited users, multi-location, custom workflows). No long-term contract required. Hardware is a one-time cost from $0 (cloud only) to $5,499 (DGX Spark). Want me to build you a specific quote based on your business?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "What's the cheapest option?",
        "Our Basic plan is $199/month with cloud-only hardware — that's $0 upfront. You use your existing computer and the AI runs on our infrastructure. It includes core AI features, monitoring, and monthly updates for 1-2 users. The install pays for itself when you stop losing even one customer a week to a missed call. Want to talk about what it would look like for your business?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "What's the DGX Spark?",
        "The DGX Spark is an NVIDIA AI supercomputer — $5,499 one-time. It's about the size of a Mac Mini but with serious AI horsepower. Your data never leaves your building, you get compliance-grade isolation with a full audit trail, and it keeps running even if your internet goes down. We recommend it for medical offices, law firms, and financial services where data privacy isn't optional. It pairs with our Enterprise plan at $1,299/month.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Is there a contract?",
        "No long-term contract. Cancel anytime — no penalties. We remove the agent, return your systems to how they were, and your data stays yours. Hardware you purchased is yours to keep. If we're not earning your business every month, that's on us.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Do I need to buy new equipment?",
        "Not necessarily. Our Cloud Only tier works with whatever you already have — laptop, desktop, tablet, even your phone. If your equipment is really outdated, our Starter Kit at $1,200 includes a tablet, router, and scanner. Most businesses can start with what they've got. The Mac Mini ($1,699) is our most popular option for businesses that want their data to stay on-site.",
    ))

    return pairs


def generate_process_pairs():
    """Generate process and FAQ pairs."""
    pairs = []

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "How does this work?",
        "Five steps. First, a free 15-minute discovery call where we learn your business and match you to one of our 12 industry playbooks. Second, we show up and install everything in 2-3 hours. Third, we train your whole team in 30 minutes before we leave. Fourth, we monitor your agent 24/7 from our facility in Lafayette. Fifth, your agent keeps getting smarter — we push updates with zero downtime. Want to book that discovery call?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Is this like ChatGPT?",
        "No. ChatGPT is a general chatbot on a website. This is a dedicated AI agent configured specifically for your industry, running on secure hardware, monitored by professionals, and integrated into your actual business tools. It's the difference between googling a legal question and hiring a paralegal. Your agent answers phones, manages schedules, tracks inventory, drafts documents — whatever your business needs. And it runs 24/7.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Who are you?",
        "I'm ROXY, the AI Advantage assistant. I run on ADC's own AI infrastructure right here in Lafayette, Louisiana — American-owned hardware, no third-party cloud. I can answer your questions about our services, build you a quote, or book you a free discovery call. What can I help you with?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Where are you located?",
        "We're based in Lafayette, Louisiana at 1201 SE Evangeline Thruway. AI Advantage is a division of Advantage Design & Construction. We serve businesses nationwide but we're proudly Louisiana-based. Our AI runs on our own infrastructure at our MARLIE I facility right here in Lafayette. Want to book a call or stop by?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Can the AI access my personal stuff?",
        "No. Every agent runs in a sandboxed container — it can only access the specific business tools we configure together. If it tries to reach anything we didn't approve, it gets blocked instantly and our team is notified. We monitor the agent's behavior, not your data. On the Mac Mini or DGX Spark plans, your data never even leaves your building.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "What if my internet goes down?",
        "If you're on a Mac Mini or DGX Spark plan, the AI keeps running locally — no internet needed. For Cloud Only plans, we set up automatic failover messaging so your customers still get a response. Either way, you're covered.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "What happens if I cancel?",
        "We remove the agent and return your systems to how they were. Your data stays yours — we don't hold anything hostage. Hardware you purchased is yours to keep. No penalties, no lock-in. If we're not earning your business every month, that's on us.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "How long does installation take?",
        "2-3 hours. A trained installer comes to your location with everything needed, sets up the hardware, configures your AI agent for your specific business, locks it down with security, and trains your whole team in 30 minutes before leaving. Your staff will be using it before we walk out the door.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "I'm interested. What's the next step?",
        "Book a free 15-minute discovery call. We learn about your business and tell you exactly what we'd install — no pitch, no pressure. You can call us at (337) 486-3149, email contact@ai-advantage.info, or I can take your info right now and have our team reach out. What works best?",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "What industries do you serve?",
        "We have 12 pre-built industry playbooks: Law Firms, Field Services (plumbers, electricians, HVAC), Medical/Dental, Restaurants, Auto Shops, Real Estate, Construction, Property Management, Retail, Accounting/CPA, Salons/Barbers, and Insurance Agencies. Each playbook is purpose-built for that industry — not a generic chatbot. Which one sounds like your business?",
    ))

    # Security-focused
    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "Is this HIPAA compliant?",
        "Yes. Our Medical/Dental playbook is built for HIPAA compliance from the ground up. Every agent runs in a sandboxed container with strict filesystem isolation and full audit logging. On the DGX Spark plan, all data stays on your hardware in your building — nothing leaves the premises. We use NVIDIA MIG hardware-level isolation so no customer's data ever touches another customer's workload. We recommend the Enterprise plan with DGX Spark for medical and dental practices.",
    ))

    pairs.append(make_conversation(
        SYSTEM_PROMPT,
        "How is my data protected?",
        "Multiple layers. Every agent runs in a sandboxed container that blocks all unauthorized connections. Hardware-level tenant isolation using NVIDIA MIG ensures your data never touches another customer's workload. Our team monitors your agent 24/7 from our MARLIE I facility in Lafayette — we handle security updates, policy changes, and model upgrades. On-site hardware options mean your data never leaves your building. Full audit logging for compliance.",
    ))

    return pairs


def generate_multi_turn_pairs():
    """Generate multi-turn conversation examples."""
    pairs = []

    # Sales conversation flow
    pairs.append({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Hi, I own a plumbing company"},
            {"role": "assistant", "content": "Great to meet you! For field services like plumbing, we install an AI agent that handles phone answering, smart dispatch, and field quoting. Your techs get job details on their phones, customers get instant responses, and nothing falls through the cracks. How many trucks are you running?"},
            {"role": "user", "content": "We have 6 trucks, about 12 employees"},
            {"role": "assistant", "content": "Perfect size for our Pro plan. At $699/month you'd get AI phone answering, smart dispatch for all 6 trucks, field quoting so your techs can generate estimates on-site, and support for up to 5 office users. For hardware, the Mac Mini at $1,699 is our most popular — your data stays in your building and it runs even if internet drops. Want to book a 15-minute call so we can match you to the exact setup?"},
        ]
    })

    # Objection handling
    pairs.append({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "I already use ServiceTitan for my HVAC business"},
            {"role": "assistant", "content": "ServiceTitan is solid for dispatching and CRM. We don't replace it — we plug into it. Our AI agent handles the stuff ServiceTitan doesn't: answering after-hours calls, pre-qualifying leads before they hit your dispatcher, following up on missed appointments, and generating quotes from job photos in the field. It makes your ServiceTitan data work harder. Want to see how they fit together?"},
        ]
    })

    # Price-sensitive customer
    pairs.append({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "That sounds expensive for a small shop"},
            {"role": "assistant", "content": "I hear you. Our Basic plan is $199/month with zero hardware cost — you use what you already have. Think of it this way: if you're missing even one call a week that could've been a $200+ job, the system pays for itself. No contract either — if it's not working, cancel anytime. Most of our clients see ROI in the first month. Want to do a quick 15-minute call and I'll show you exactly what it'd look like for your shop?"},
        ]
    })

    return pairs


def main():
    all_pairs = []

    # Generate from playbooks
    for pb in sorted(PLAYBOOK_DIR.glob("*.md")):
        if pb.stem == "nemoclaw-installer-guide":
            continue  # Internal doc, not customer-facing
        content = pb.read_text(encoding="utf-8")
        pairs = generate_playbook_pairs(pb, content)
        all_pairs.extend(pairs)
        print(f"  {pb.stem}: {len(pairs)} pairs")

    # Generate pricing pairs
    pricing = generate_pricing_pairs()
    all_pairs.extend(pricing)
    print(f"  pricing: {len(pricing)} pairs")

    # Generate process/FAQ pairs
    process = generate_process_pairs()
    all_pairs.extend(process)
    print(f"  process/FAQ: {len(process)} pairs")

    # Generate multi-turn pairs
    multi = generate_multi_turn_pairs()
    all_pairs.extend(multi)
    print(f"  multi-turn: {len(multi)} pairs")

    # Write JSONL
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"\nTotal: {len(all_pairs)} training examples")
    print(f"Output: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    print("ROXY Fine-Tuning Dataset Generator")
    print("=" * 40)
    main()
