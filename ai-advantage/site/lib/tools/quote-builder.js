// ROXY Tool: Quote Builder
// Generates a pricing quote based on industry, plan tier, and hardware choice

const MONTHLY_PLANS = {
  basic: {
    name: "Basic",
    price: 199,
    features: ["Core AI features", "1-2 users", "Email support", "24/7 monitoring", "Monthly updates"],
  },
  pro: {
    name: "Pro (Most Popular)",
    price: 699,
    features: [
      "All Basic features",
      "Full integrations",
      "AI phone answering",
      "Up to 5 users",
      "Phone support",
      "Priority monitoring",
      "File organization tools",
    ],
  },
  enterprise: {
    name: "Enterprise",
    price: 1299,
    features: [
      "All Pro features",
      "Unlimited users",
      "Multi-location support",
      "Custom workflows",
      "Priority phone support",
      "Dedicated account manager",
    ],
  },
};

const HARDWARE_TIERS = {
  cloud: {
    name: "Cloud Only",
    price: 0,
    description: "Agent runs on ADC infrastructure. Use your existing computer.",
    best_for: "Small operations, testing the waters",
  },
  starter: {
    name: "Starter Kit",
    price: 1200,
    description: "Tablet, router, scanner included.",
    best_for: "Businesses with aging equipment",
  },
  "mac-mini": {
    name: "Mac Mini (Most Popular)",
    price: 1699,
    description: "On-site AI. Silent, 40W. Data never leaves your building.",
    best_for: "Privacy-aware businesses",
  },
  "dgx-spark": {
    name: "DGX Spark",
    price: 5499,
    description: "NVIDIA AI supercomputer. Compliance-grade isolation, full audit trail.",
    best_for: "Medical, legal, finance — compliance-critical",
  },
};

const INDUSTRY_RECOMMENDATIONS = {
  "law-firm": { plan: "pro", hardware: "dgx-spark", playbook: "Document Shop" },
  "field-services": { plan: "pro", hardware: "mac-mini", playbook: "Dispatch Shop" },
  "medical-dental": { plan: "enterprise", hardware: "dgx-spark", playbook: "Appointment Shop" },
  "restaurant": { plan: "basic", hardware: "mac-mini", playbook: "Inventory Shop" },
  "auto-shop": { plan: "pro", hardware: "mac-mini", playbook: "Inventory Shop" },
  "real-estate": { plan: "pro", hardware: "cloud", playbook: "Deal Shop" },
  "construction": { plan: "pro", hardware: "mac-mini", playbook: "Deal Shop" },
  "property-management": { plan: "pro", hardware: "mac-mini", playbook: "Dispatch Shop" },
  "retail": { plan: "basic", hardware: "mac-mini", playbook: "Inventory Shop" },
  "accounting": { plan: "pro", hardware: "dgx-spark", playbook: "Document Shop" },
  "salon-barber": { plan: "basic", hardware: "cloud", playbook: "Appointment Shop" },
  "insurance": { plan: "pro", hardware: "mac-mini", playbook: "Deal Shop" },
};

module.exports = {
  name: "build_quote",
  description:
    "Build a pricing quote for a potential customer based on their industry, preferred plan tier, and hardware choice. If industry is provided without tier/hardware, uses recommended defaults.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The customer's industry (e.g., 'law-firm', 'restaurant', 'medical-dental', 'field-services')",
      },
      tier: {
        type: "string",
        enum: ["basic", "pro", "enterprise"],
        description: "Monthly plan tier",
      },
      hardware: {
        type: "string",
        enum: ["cloud", "starter", "mac-mini", "dgx-spark"],
        description: "Hardware tier",
      },
    },
    required: [],
  },
  async execute(args) {
    // Use industry recommendations as defaults
    const rec = args.industry
      ? INDUSTRY_RECOMMENDATIONS[args.industry] || { plan: "pro", hardware: "mac-mini" }
      : {};

    const tier = args.tier || rec.plan || "pro";
    const hw = args.hardware || rec.hardware || "mac-mini";

    const plan = MONTHLY_PLANS[tier];
    const hardware = HARDWARE_TIERS[hw];

    if (!plan || !hardware) {
      return "I don't have pricing for that configuration. Let me connect you with our team.";
    }

    const yearOneCost = hardware.price + plan.price * 12;

    const quote = {
      plan: plan.name,
      monthly_cost: `$${plan.price}/mo`,
      plan_features: plan.features,
      hardware: hardware.name,
      hardware_cost: hardware.price === 0 ? "Free" : `$${hardware.price.toLocaleString()} (one-time)`,
      hardware_description: hardware.description,
      best_for: hardware.best_for,
      year_one_total: `$${yearOneCost.toLocaleString()}`,
      monthly_after_year_one: `$${plan.price}/mo`,
      no_contract: "No long-term contract required",
      includes_install: "Professional 2-3 hour on-site installation included",
      includes_training: "30-minute team training included",
      includes_monitoring: "24/7 remote monitoring from MARLIE I facility",
    };

    if (rec.playbook) {
      quote.playbook_type = rec.playbook;
    }

    return JSON.stringify(quote);
  },
};
