// ROXY Tool Selector
// Pre-filters which tools the LLM sees based on conversation context.
// Solves two problems: model doesn't fire tools (too many choices) + system prompt too long.
// Instead of 23 tools every time, ROXY sees 6-10 relevant ones.

const ALWAYS_AVAILABLE = [
  "search_playbooks",
  "get_contact_info",
  "capture_lead",
  "book_appointment",
];

// Tool groups by conversation phase / intent
const TOOL_GROUPS = {
  // First message / discovery phase
  discovery: [
    "search_playbooks",
    "local_market_intel",
    "generate_live_demo",
  ],
  // Visitor shared personal info (name, email, phone)
  has_contact_info: [
    "capture_lead",
    "crm_lookup",
    "send_followup_email",
    "send_sms",
  ],
  // Pricing / quoting phase
  pricing: [
    "build_quote",
    "calculate_roi",
    "franchise_qualifier",
    "generate_payment_link",
  ],
  // Objection handling / fence-sitting
  objection: [
    "create_urgency_offer",
    "calculate_roi",
    "competitor_intel",
    "generate_live_demo",
    "local_market_intel",
  ],
  // Competitor mentioned
  competitor: [
    "competitor_intel",
    "calculate_roi",
    "local_market_intel",
  ],
  // Multi-location / franchise signals
  franchise: [
    "franchise_qualifier",
    "build_quote",
    "generate_payment_link",
  ],
  // Marketing / SaaS tools (existing customer or marketing discussion)
  marketing: [
    "generate_ad_copy",
    "generate_social_posts",
    "respond_to_review",
    "request_review",
    "generate_lead_magnet",
    "build_email_campaign",
  ],
  // Closing phase (ready to buy)
  closing: [
    "generate_payment_link",
    "book_appointment",
    "send_followup_email",
    "send_sms",
    "create_urgency_offer",
    "score_lead",
    "initiate_outbound_call",
  ],
  // Post-sale / onboarding
  onboarding: [
    "onboard_client",
    "generate_widget",
    "send_followup_email",
  ],
  // Callback requested
  callback: [
    "initiate_outbound_call",
    "capture_lead",
    "score_lead",
  ],
  // Conversation ending
  wrapup: [
    "log_conversation",
    "send_followup_email",
    "book_appointment",
  ],
};

// Intent detection keywords
const INTENT_PATTERNS = {
  has_contact_info: /\b(my name|my email|@|\.com|\.net|\.org|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|phone|call me|reach me|contact me)\b/i,
  pricing: /\b(cost|price|pricing|how much|afford|budget|expensive|cheap|quote|rate|monthly|per month|\/mo)\b/i,
  objection: /\b(think about|not sure|maybe later|too much|expensive|already have|don't need|not ready|can't afford|worth it|pay for itself)\b/i,
  competitor: /\b(servicetitan|housecall|jobber|dentrix|eaglesoft|toast|square|quickbooks|vagaro|chatgpt|follow up boss|yelp|google ads)\b/i,
  franchise: /\b(locations?|franchise|chain|multi.?location|stores?|offices?|branches?|sites?)\b/i,
  marketing: /\b(marketing|advertis|social media|facebook|instagram|google ads?|review|post|content|email campaign|lead magnet|seo)\b/i,
  closing: /\b(sign up|get started|ready|let'?s do|want to buy|how do i pay|take my money|i'?m in|where do i sign)\b/i,
  wrapup: /\b(thanks|thank you|bye|goodbye|that'?s all|got it|appreciate|have a good|talk later)\b/i,
  demo: /\b(show me|how.?does it work|what.?does it do|demo|example|walk me through|can't picture|looks? like)\b/i,
  callback: /\b(call me|call back|give me a call|phone me|ring me|want a call|callback)\b/i,
  onboarding: /\b(get started|set up|install|onboard|ready to go|next step|what do i need|prepare|pre.?install)\b/i,
};

/**
 * Select relevant tools based on the conversation context.
 * @param {Array} messages - Conversation history
 * @param {Object} sessionContext - Known visitor info
 * @param {Array} allTools - Full tool definitions
 * @returns {Array} Filtered tool definitions
 */
function selectTools(messages, sessionContext, allTools) {
  // Analyze the full conversation for intent signals
  const fullText = messages
    .filter((m) => m.role === "user")
    .map((m) => m.content)
    .join(" ");

  const lastMessage = messages
    .filter((m) => m.role === "user")
    .pop()?.content || "";

  // Detect active intents
  const activeGroups = new Set(["discovery"]); // Always start with discovery

  for (const [intent, pattern] of Object.entries(INTENT_PATTERNS)) {
    if (pattern.test(fullText) || pattern.test(lastMessage)) {
      activeGroups.add(intent);
    }
  }

  // If demo keywords detected, add discovery tools
  if (INTENT_PATTERNS.demo.test(lastMessage)) {
    activeGroups.add("discovery");
  }

  // Session context signals
  if (sessionContext?.visitorEmail || sessionContext?.visitorName) {
    activeGroups.add("has_contact_info");
  }
  if (sessionContext?.leadCaptured) {
    activeGroups.add("closing");
    activeGroups.add("wrapup");
  }

  // Multi-message conversation = probably past discovery
  if (messages.filter((m) => m.role === "user").length >= 3) {
    activeGroups.add("closing");
  }

  // Build the selected tool names
  const selectedNames = new Set(ALWAYS_AVAILABLE);

  for (const group of activeGroups) {
    const groupTools = TOOL_GROUPS[group] || [];
    for (const name of groupTools) {
      selectedNames.add(name);
    }
  }

  // Filter the full tool definitions to only selected ones
  const selected = allTools.filter(
    (t) => selectedNames.has(t.function?.name || t.name)
  );

  return selected;
}

module.exports = { selectTools };
