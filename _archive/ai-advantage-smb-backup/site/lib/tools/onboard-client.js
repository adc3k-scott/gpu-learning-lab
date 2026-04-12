// ROXY Tool: Remote Onboarding / Pre-Install Config
// Generates the pre-install questionnaire so everything is ready before showing up.
// Reduces install time from 3 hours to 1.5 hours. Makes remote installs possible.

const INDUSTRY_QUESTIONS = {
  plumbing: {
    label: "Field Services (Plumbing)",
    questions: [
      { q: "What dispatch/CRM software do you currently use?", examples: "ServiceTitan, Housecall Pro, Jobber, none" },
      { q: "How many trucks/techs do you have?", type: "number" },
      { q: "What's your service area? (cities/parishes)", type: "text" },
      { q: "Do you offer 24/7 emergency service?", type: "yes_no" },
      { q: "What's your average job value?", type: "currency" },
      { q: "Do you currently answer after-hours calls? How?", type: "text" },
      { q: "What accounting software do you use?", examples: "QuickBooks, Xero, FreshBooks, none" },
      { q: "Do your techs have smartphones for the field app?", type: "yes_no" },
    ],
    hardware_recommendation: "Mac Mini (data stays local) or Cloud Only (if you're always in the field)",
    integrations_to_check: ["ServiceTitan", "Housecall Pro", "Jobber", "QuickBooks"],
  },
  hvac: {
    label: "Field Services (HVAC)",
    questions: [
      { q: "What dispatch software do you use?", examples: "ServiceTitan, Housecall Pro, Jobber, none" },
      { q: "How many techs on staff?", type: "number" },
      { q: "Do you do commercial, residential, or both?", type: "text" },
      { q: "What's your busiest season?", type: "text" },
      { q: "Do you stock parts on trucks?", type: "yes_no" },
      { q: "What accounting software?", examples: "QuickBooks, Xero, none" },
    ],
    hardware_recommendation: "Mac Mini",
    integrations_to_check: ["ServiceTitan", "Housecall Pro", "QuickBooks"],
  },
  dental: {
    label: "Medical / Dental",
    questions: [
      { q: "What practice management software do you use?", examples: "Dentrix, Eaglesoft, Open Dental, none" },
      { q: "How many providers (dentists/hygienists)?", type: "number" },
      { q: "How many front desk staff?", type: "number" },
      { q: "Do you verify insurance manually or automatically?", type: "text" },
      { q: "Average patients per day?", type: "number" },
      { q: "Do you have a patient portal currently?", type: "yes_no" },
      { q: "Are you comfortable with AI writing clinical notes from dictation?", type: "yes_no" },
      { q: "HIPAA: Do you need a BAA with AI Advantage?", type: "yes_no" },
    ],
    hardware_recommendation: "DGX Spark (HIPAA compliance requires on-premise processing)",
    integrations_to_check: ["Dentrix", "Eaglesoft", "Open Dental"],
  },
  restaurant: {
    label: "Restaurant / Bar",
    questions: [
      { q: "What POS system do you use?", examples: "Toast, Square, Clover, Aloha, none" },
      { q: "How many seats/covers per day?", type: "number" },
      { q: "Do you do delivery/takeout?", type: "yes_no" },
      { q: "What's your approximate monthly food cost?", type: "currency" },
      { q: "Do you currently track food waste?", type: "yes_no" },
      { q: "How many staff?", type: "number" },
      { q: "Do you use any inventory management software?", type: "text" },
    ],
    hardware_recommendation: "Mac Mini (keeps kitchen data on-site)",
    integrations_to_check: ["Toast", "Square", "Clover"],
  },
  salon: {
    label: "Salon / Barber / Spa",
    questions: [
      { q: "What booking software do you use?", examples: "Vagaro, Booksy, Square Appointments, none" },
      { q: "How many stylists/chairs?", type: "number" },
      { q: "What's your no-show rate? (rough estimate)", type: "text" },
      { q: "Do you sell retail products?", type: "yes_no" },
      { q: "Do you currently send appointment reminders?", type: "yes_no" },
    ],
    hardware_recommendation: "Cloud Only (unless privacy is a concern)",
    integrations_to_check: ["Vagaro", "Booksy", "Square"],
  },
  "real estate": {
    label: "Real Estate",
    questions: [
      { q: "What CRM do you use?", examples: "Follow Up Boss, KVCore, kvCORE, Chime, none" },
      { q: "Solo agent or team?", type: "text" },
      { q: "Average response time to new leads currently?", type: "text" },
      { q: "What lead sources do you use?", examples: "Zillow, Realtor.com, Facebook, referrals" },
      { q: "Do you need listing description generation?", type: "yes_no" },
    ],
    hardware_recommendation: "Cloud Only (agents are mobile)",
    integrations_to_check: ["Follow Up Boss", "KVCore", "MLS"],
  },
  law: {
    label: "Law Firm",
    questions: [
      { q: "What practice management software?", examples: "Clio, MyCase, PracticePanther, none" },
      { q: "How many attorneys?", type: "number" },
      { q: "What practice areas?", examples: "Personal injury, criminal, family, corporate" },
      { q: "Do you need document AI (search, drafting, intake)?", type: "yes_no" },
      { q: "Attorney-client privilege: do you need all data on-premise?", type: "yes_no" },
      { q: "Do you have a dedicated IT person or firm?", type: "yes_no" },
    ],
    hardware_recommendation: "DGX Spark (privilege requires on-premise, full audit trail)",
    integrations_to_check: ["Clio", "MyCase", "PracticePanther"],
  },
  insurance: {
    label: "Insurance Agency",
    questions: [
      { q: "What agency management system?", examples: "Applied Epic, HawkSoft, EZLynx, none" },
      { q: "How many producers/agents?", type: "number" },
      { q: "What carriers do you represent?", type: "text" },
      { q: "Do you do personal, commercial, or both?", type: "text" },
      { q: "Biggest pain point: quoting, renewals, or claims?", type: "text" },
    ],
    hardware_recommendation: "Mac Mini",
    integrations_to_check: ["Applied Epic", "HawkSoft", "EZLynx"],
  },
  construction: {
    label: "Construction / GC",
    questions: [
      { q: "What project management software?", examples: "Procore, Buildertrend, CoConstruct, none" },
      { q: "How many active projects typically?", type: "number" },
      { q: "How many subcontractors do you coordinate?", type: "number" },
      { q: "Do you need AI for change orders and daily logs?", type: "yes_no" },
      { q: "What accounting software?", examples: "QuickBooks, Sage, Foundation" },
    ],
    hardware_recommendation: "Mac Mini",
    integrations_to_check: ["Procore", "Buildertrend", "QuickBooks"],
  },
};

function findIndustryQuestions(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, data] of Object.entries(INDUSTRY_QUESTIONS)) {
    if (lower.includes(key)) return { key, ...data };
  }
  if (lower.match(/plumb/)) return { key: "plumbing", ...INDUSTRY_QUESTIONS.plumbing };
  if (lower.match(/hvac|cool|heat/)) return { key: "hvac", ...INDUSTRY_QUESTIONS.hvac };
  if (lower.match(/dent|medical|doctor/)) return { key: "dental", ...INDUSTRY_QUESTIONS.dental };
  if (lower.match(/restaurant|food|bar/)) return { key: "restaurant", ...INDUSTRY_QUESTIONS.restaurant };
  if (lower.match(/salon|barber|hair/)) return { key: "salon", ...INDUSTRY_QUESTIONS.salon };
  if (lower.match(/real estate|realtor/)) return { key: "real estate", ...INDUSTRY_QUESTIONS["real estate"] };
  if (lower.match(/law|attorney/)) return { key: "law", ...INDUSTRY_QUESTIONS.law };
  if (lower.match(/insur/)) return { key: "insurance", ...INDUSTRY_QUESTIONS.insurance };
  if (lower.match(/construct|contractor/)) return { key: "construction", ...INDUSTRY_QUESTIONS.construction };
  return null;
}

module.exports = {
  name: "onboard_client",
  description:
    "Generate a pre-install onboarding questionnaire for a new client based on their industry. Use this after a lead is captured and they're ready to move forward. The questionnaire captures everything the installer needs to know BEFORE showing up — reducing install time from 3 hours to 1.5 hours. Also works for fully remote installations.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "Client's industry",
      },
      business_name: {
        type: "string",
        description: "Client's business name",
      },
      client_name: {
        type: "string",
        description: "Client contact name",
      },
      plan: {
        type: "string",
        enum: ["basic", "pro", "enterprise"],
        description: "Selected plan tier",
      },
      remote_install: {
        type: "boolean",
        description: "Whether this is a remote installation (no on-site visit)",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const data = findIndustryQuestions(args.industry);
    const biz = args.business_name || "your business";
    const isRemote = args.remote_install || false;

    if (!data) {
      return JSON.stringify({
        available: false,
        message: `I'll create a custom onboarding checklist for ${args.industry}. Let's discuss on the discovery call.`,
      });
    }

    const onboarding = {
      business: biz,
      client: args.client_name || null,
      industry: data.label,
      plan: args.plan || "pro",
      install_type: isRemote ? "REMOTE" : "ON-SITE",
      hardware_recommendation: data.hardware_recommendation,

      // Pre-install questionnaire
      questionnaire: data.questions,

      // What the client needs to prepare
      client_prep: [
        "WiFi network name and password",
        "Admin login for your current business software",
        "List of staff names and roles who will use the AI",
        "Your business hours and holiday schedule",
        "Phone number you want the AI to answer (if using AI phone)",
        isRemote ? "Remote desktop access (AnyDesk or TeamViewer)" : "A desk or shelf for the hardware (if Mac Mini / DGX Spark)",
      ],

      // Integrations to verify
      integrations: data.integrations_to_check,

      // Remote install specific
      remote_steps: isRemote ? [
        "Step 1: Fill out the questionnaire above (10 minutes)",
        "Step 2: Set up remote access (AnyDesk — we'll walk you through it)",
        "Step 3: We configure your AI agent remotely (1-2 hours, you don't need to be there)",
        "Step 4: Video call training with your team (30 minutes)",
        "Step 5: Agent goes live, we monitor 24/7",
      ] : null,

      // On-site install steps
      onsite_steps: !isRemote ? [
        "Step 1: Fill out the questionnaire above (10 minutes, do this before we arrive)",
        "Step 2: Installer arrives with all equipment (we bring everything)",
        "Step 3: Hardware setup + software configuration (1.5-2 hours)",
        "Step 4: Team training (30 minutes, everyone should be present)",
        "Step 5: Installer verifies everything works, hands over",
        "Step 6: Agent goes live, we monitor 24/7",
      ] : null,

      // Timeline
      timeline: {
        questionnaire: "Complete within 24 hours of booking",
        install_scheduled: isRemote ? "Within 48 hours of questionnaire completion" : "Within 1 week, based on installer availability",
        install_duration: isRemote ? "1-2 hours (remote, no travel)" : "2-3 hours on-site",
        training: "30 minutes (same day as install)",
        live: "Same day as install",
      },

      next_step: isRemote
        ? "Let's go through the questionnaire right now — I can capture your answers as we chat."
        : "Fill out the questionnaire and we'll schedule your installation. Want to answer these questions now or should I email them to you?",
    };

    return JSON.stringify(onboarding);
  },
};
