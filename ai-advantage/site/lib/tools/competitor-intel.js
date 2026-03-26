// ROXY Subagent: Competitor Intel
// When a customer mentions they use a specific software, ROXY knows how to position
// AI Advantage as a complement — not a replacement.

const COMPETITOR_DATA = {
  // Field Services
  servicetitan: {
    name: "ServiceTitan",
    category: "Field Service Management",
    industries: ["plumbing", "hvac", "electrical", "field services"],
    what_it_does: "Dispatch, CRM, invoicing, marketing automation for home services",
    adc_complements: [
      "AI phone answering — catches calls ServiceTitan can't handle after hours",
      "Pre-qualifying leads before they hit your dispatcher",
      "Photo-to-estimate in the field — faster than manual quoting",
      "Automated follow-ups on missed appointments",
    ],
    positioning: "We don't replace ServiceTitan — we plug into it. We handle the AI layer that ServiceTitan doesn't: phone answering, lead pre-qualification, and field quoting.",
  },
  housecallpro: {
    name: "Housecall Pro",
    category: "Field Service Management",
    industries: ["plumbing", "hvac", "electrical", "cleaning"],
    what_it_does: "Scheduling, dispatching, invoicing, online booking for home services",
    adc_complements: [
      "AI phone answering when you're on a job",
      "Smart dispatch based on tech location and skill",
      "Automated customer follow-ups after service",
    ],
    positioning: "Housecall Pro handles scheduling and invoicing well. We add the AI brain — phone answering, smart routing, and automated follow-ups your current setup doesn't do.",
  },
  jobber: {
    name: "Jobber",
    category: "Field Service Management",
    industries: ["field services", "landscaping", "cleaning"],
    what_it_does: "Quoting, scheduling, invoicing, client hub for service businesses",
    adc_complements: [
      "AI-powered phone answering and lead capture",
      "Photo-based job quoting from the field",
      "Automated rebooking for recurring services",
    ],
    positioning: "Jobber is great for operations. We add the AI front-end — catching calls, qualifying leads, and generating quotes automatically.",
  },
  // Dental/Medical
  dentrix: {
    name: "Dentrix",
    category: "Dental Practice Management",
    industries: ["dental", "medical"],
    what_it_does: "Patient records, scheduling, billing, treatment planning for dental offices",
    adc_complements: [
      "AI insurance verification — instant eligibility checks",
      "Clinical notes assistant that drafts from voice",
      "Smart scheduling that fills cancellation gaps",
      "After-hours patient communication",
    ],
    positioning: "Dentrix manages your practice. We add AI on top — insurance verification, smart scheduling, clinical note drafting. Your data stays on-site with HIPAA compliance.",
  },
  eaglesoft: {
    name: "Eaglesoft",
    category: "Dental Practice Management",
    industries: ["dental"],
    what_it_does: "Practice management, scheduling, digital imaging for dental",
    adc_complements: [
      "AI insurance verification automation",
      "Clinical notes from voice dictation",
      "Automated appointment reminders and rebooking",
    ],
    positioning: "Eaglesoft handles your practice management. We add AI capabilities it doesn't have — voice notes, insurance verification, and smart scheduling.",
  },
  // Restaurant
  toast: {
    name: "Toast POS",
    category: "Restaurant POS",
    industries: ["restaurant", "bar", "cafe"],
    what_it_does: "Point of sale, online ordering, payroll, marketing for restaurants",
    adc_complements: [
      "Real-time food cost tracking across all items",
      "Auto-reorder alerts when inventory hits threshold",
      "Recipe costing per dish with margin analysis",
      "AI-powered waste prediction and reduction",
    ],
    positioning: "Toast handles your POS and ordering. We add the AI inventory brain — food cost tracking, auto-reorder, recipe costing, and waste prediction that Toast doesn't do.",
  },
  square: {
    name: "Square",
    category: "POS / Payments",
    industries: ["restaurant", "retail", "salon"],
    what_it_does: "Payment processing, POS, online store, appointment booking",
    adc_complements: [
      "AI that analyzes your Square data for patterns",
      "Automated inventory management and reorder",
      "Customer follow-up based on purchase history",
      "AI phone answering for appointment businesses",
    ],
    positioning: "Square handles payments. We add AI analytics and automation on top — inventory prediction, customer follow-ups, and phone answering that Square doesn't provide.",
  },
  // Real Estate
  followupboss: {
    name: "Follow Up Boss",
    category: "Real Estate CRM",
    industries: ["real estate"],
    what_it_does: "Lead management, automated follow-ups, team management for real estate",
    adc_complements: [
      "Instant listing description generation",
      "AI lead qualification before it hits your CRM",
      "Market analysis and comp reports on demand",
      "24/7 lead response — under 60 seconds",
    ],
    positioning: "Follow Up Boss manages your leads. We add AI speed-to-lead response (under 60 seconds), listing description generation, and market analysis it doesn't do.",
  },
  // Accounting
  quickbooks: {
    name: "QuickBooks",
    category: "Accounting Software",
    industries: ["accounting", "small business"],
    what_it_does: "Bookkeeping, invoicing, payroll, tax prep, expense tracking",
    adc_complements: [
      "AI document intake — scan and categorize tax docs automatically",
      "Deadline tracking across all clients with smart alerts",
      "Client portal for secure document upload",
      "AI-extracted data from receipts and invoices",
    ],
    positioning: "QuickBooks handles your books. We add AI document processing — scan tax docs, extract data automatically, track deadlines across clients, and give your clients a secure upload portal.",
  },
  // Salon
  vagaro: {
    name: "Vagaro",
    category: "Salon/Spa Management",
    industries: ["salon", "barber", "spa"],
    what_it_does: "Booking, POS, payroll, marketing for salons and spas",
    adc_complements: [
      "AI-powered rebooking that targets no-shows",
      "Personalized follow-ups based on service history",
      "Smart schedule optimization to reduce gaps",
      "AI phone answering for booking requests",
    ],
    positioning: "Vagaro handles booking and POS. We add AI rebooking, personalized follow-ups, and phone answering that keep your chairs full.",
  },
  // General
  chatgpt: {
    name: "ChatGPT",
    category: "General AI Chatbot",
    industries: [],
    what_it_does: "General-purpose AI chatbot on a website. Not configured for any specific industry.",
    adc_complements: [
      "Dedicated agent built for YOUR industry — not generic",
      "Runs on secure hardware with data privacy",
      "Integrated into your actual business tools",
      "Monitored 24/7 by professionals",
      "Gets smarter with your data over time",
    ],
    positioning: "ChatGPT is a general chatbot. This is a dedicated AI agent configured specifically for your industry, running on secure hardware, monitored by professionals, and integrated into your actual business tools. It's the difference between googling a legal question and hiring a paralegal.",
  },
};

function findCompetitor(name) {
  const lower = name.toLowerCase().replace(/[^a-z0-9]/g, "");
  // Direct match
  if (COMPETITOR_DATA[lower]) return COMPETITOR_DATA[lower];
  // Partial match
  for (const [key, data] of Object.entries(COMPETITOR_DATA)) {
    if (lower.includes(key) || key.includes(lower)) return data;
    if (data.name.toLowerCase().replace(/[^a-z0-9]/g, "").includes(lower)) return data;
  }
  return null;
}

module.exports = {
  name: "competitor_intel",
  description:
    "Look up information about a competitor or software tool that a visitor mentions they already use. Returns what that tool does and how AI Advantage complements it (not replaces it). Use this when a visitor says they already use a specific software or service.",
  parameters: {
    type: "object",
    properties: {
      software_name: {
        type: "string",
        description: "The name of the software or tool the visitor mentioned (e.g., 'ServiceTitan', 'Toast', 'QuickBooks', 'ChatGPT')",
      },
      industry: {
        type: "string",
        description: "The visitor's industry if known",
      },
    },
    required: ["software_name"],
  },
  async execute(args) {
    const competitor = findCompetitor(args.software_name);

    if (!competitor) {
      return JSON.stringify({
        found: false,
        software_name: args.software_name,
        guidance: `We don't have specific intel on "${args.software_name}". Position AI Advantage as a complement — we add AI capabilities (phone answering, automation, intelligence) that most existing software doesn't have. We don't replace their tools, we make them smarter.`,
      });
    }

    return JSON.stringify({
      found: true,
      name: competitor.name,
      category: competitor.category,
      what_it_does: competitor.what_it_does,
      how_we_complement: competitor.adc_complements,
      positioning: competitor.positioning,
      key_message: "We don't replace it — we add the AI layer it doesn't have.",
    });
  },
};
