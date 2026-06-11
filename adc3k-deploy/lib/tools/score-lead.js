// ROXY Tool: Lead Scorer
// Auto-scores leads and triggers the right follow-up action.
// Hot leads get called within 5 minutes. Warm leads get email drip.

module.exports = {
  name: "score_lead",
  description:
    "Score a lead's temperature and trigger the appropriate follow-up. Call this after capturing a lead to determine urgency. Hot leads should get an immediate callback. Use this whenever capture_lead fires and you have enough context to score.",
  parameters: {
    type: "object",
    properties: {
      email: { type: "string", description: "Lead's email" },
      phone: { type: "string", description: "Lead's phone number" },
      name: { type: "string", description: "Lead's name" },
      industry: { type: "string", description: "Business industry" },
      locations: { type: "number", description: "Number of locations (1 = single, 2+ = franchise)" },
      budget_mentioned: { type: "boolean", description: "Did they mention budget/pricing positively?" },
      timeline_urgent: { type: "boolean", description: "Did they mention urgency (need it now, ASAP, etc.)?" },
      objection_overcome: { type: "boolean", description: "Was an objection handled and resolved?" },
      roi_shown: { type: "boolean", description: "Did ROXY show them ROI numbers?" },
      competitor_mentioned: { type: "string", description: "Any competitor software mentioned" },
      requested_callback: { type: "boolean", description: "Did they ask for a callback?" },
      engagement_level: {
        type: "string",
        enum: ["high", "medium", "low"],
        description: "How engaged were they in the conversation (number of messages, detail of questions)",
      },
    },
    required: [],
  },
  async execute(args) {
    let score = 0;
    const signals = [];

    // Scoring criteria
    if (args.email) { score += 15; signals.push("+15: provided email"); }
    if (args.phone) { score += 20; signals.push("+20: provided phone number"); }
    if (args.name) { score += 5; signals.push("+5: provided name"); }

    // Industry value (higher ARPU industries score higher)
    const highValueIndustries = ["dental", "medical", "law", "insurance", "accounting"];
    const midValueIndustries = ["construction", "real estate", "hvac", "plumbing", "auto"];
    if (args.industry) {
      const ind = args.industry.toLowerCase();
      if (highValueIndustries.some(i => ind.includes(i))) {
        score += 15;
        signals.push("+15: high-value industry");
      } else if (midValueIndustries.some(i => ind.includes(i))) {
        score += 10;
        signals.push("+10: mid-value industry");
      } else {
        score += 5;
        signals.push("+5: industry identified");
      }
    }

    // Multi-location = massive multiplier
    if (args.locations && args.locations >= 3) {
      score += 25;
      signals.push(`+25: franchise (${args.locations} locations)`);
    } else if (args.locations && args.locations === 2) {
      score += 10;
      signals.push("+10: two locations");
    }

    // Buying signals
    if (args.budget_mentioned) { score += 10; signals.push("+10: budget discussed positively"); }
    if (args.timeline_urgent) { score += 15; signals.push("+15: urgent timeline"); }
    if (args.objection_overcome) { score += 10; signals.push("+10: objection overcome"); }
    if (args.roi_shown) { score += 10; signals.push("+10: ROI presented"); }
    if (args.requested_callback) { score += 20; signals.push("+20: requested callback"); }

    // Engagement
    if (args.engagement_level === "high") { score += 10; signals.push("+10: high engagement"); }
    else if (args.engagement_level === "medium") { score += 5; signals.push("+5: medium engagement"); }

    // Cap at 100
    score = Math.min(score, 100);

    // Determine temperature and action
    let temperature, action, priority;
    if (score >= 70) {
      temperature = "HOT";
      priority = "IMMEDIATE";
      action = args.phone
        ? "CALL WITHIN 5 MINUTES. Use initiate_outbound_call to dial them now."
        : "SEND FOLLOW-UP EMAIL IMMEDIATELY with booking link.";
    } else if (score >= 40) {
      temperature = "WARM";
      priority = "SAME DAY";
      action = "Send personalized follow-up email within 1 hour. Add to weekly nurture campaign.";
    } else {
      temperature = "COOL";
      priority = "WEEKLY";
      action = "Add to industry drip campaign. Re-engage in 7 days with relevant content.";
    }

    // Estimate deal value
    const monthlyBase = args.locations && args.locations >= 3 ? 699 * args.locations * 0.85 : 699;
    const annualValue = Math.round(monthlyBase * 12);

    return JSON.stringify({
      score,
      temperature,
      priority,
      recommended_action: action,
      signals,
      estimated_annual_value: `$${annualValue.toLocaleString()}`,
      trigger_callback: temperature === "HOT" && !!args.phone,
      trigger_email: temperature === "HOT" || temperature === "WARM",
      trigger_drip: temperature === "COOL",
    });
  },
};
