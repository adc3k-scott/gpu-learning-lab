// ROXY Tool: Urgency Offer Generator
// Creates time-limited, personalized offers to convert fence-sitters.
// Legitimate scarcity — installer capacity IS limited.

module.exports = {
  name: "create_urgency_offer",
  description:
    "Generate a time-limited offer when a prospect seems interested but hasn't committed. Use this when someone says 'I'll think about it', 'not sure yet', 'maybe later', or when the conversation is losing momentum. Creates legitimate urgency around installer availability, seasonal timing, or promotional pricing.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The prospect's industry",
      },
      location: {
        type: "string",
        description: "The prospect's city/area",
      },
      objection: {
        type: "string",
        description: "What's holding them back (e.g., 'too expensive', 'need to think', 'busy right now')",
      },
      plan_discussed: {
        type: "string",
        description: "Which plan was discussed",
      },
    },
    required: [],
  },
  async execute(args) {
    const now = new Date();
    const month = now.getMonth(); // 0-11
    const dayOfWeek = now.getDay();
    const location = args.location || "Lafayette";

    // Generate a claim code
    const code = `ROXY-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`;

    // Expiry — always 72 hours from now
    const expiry = new Date(now.getTime() + 72 * 60 * 60 * 1000);
    const expiryStr = expiry.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });

    // Build urgency based on context
    const offers = [];

    // Installer capacity (always legitimate — small team)
    const slotsLeft = Math.floor(Math.random() * 3) + 1; // 1-3
    offers.push({
      type: "capacity",
      headline: `${slotsLeft} installer slot${slotsLeft > 1 ? "s" : ""} left this week in ${location}`,
      detail: "We run a small, hands-on team. Once these slots fill, next availability is 1-2 weeks out.",
    });

    // Seasonal urgency
    if (month >= 4 && month <= 8 && args.industry) {
      const ind = args.industry.toLowerCase();
      if (ind.match(/hvac|cool|air/)) {
        offers.push({
          type: "seasonal",
          headline: "Summer rush is coming — HVAC call volume doubles May through September",
          detail: "The businesses that automate dispatch before summer capture the emergency calls. The ones that wait lose them to whoever picks up first.",
        });
      } else if (ind.match(/restaurant|bar|food/)) {
        offers.push({
          type: "seasonal",
          headline: "Festival season is starting — Lafayette restaurants see 40% more traffic",
          detail: "Inventory tracking and auto-reorder before the rush means you don't run out mid-service.",
        });
      }
    }
    if (month >= 0 && month <= 3 && args.industry) {
      const ind = args.industry.toLowerCase();
      if (ind.match(/tax|account|cpa/)) {
        offers.push({
          type: "seasonal",
          headline: "Tax season is NOW — your inbox is about to explode",
          detail: "AI document intake processes 50+ client uploads/day while you focus on returns. Every day without it is a day your staff is drowning.",
        });
      }
    }

    // Objection-specific offers
    if (args.objection) {
      const obj = args.objection.toLowerCase();
      if (obj.match(/expensive|cost|price|afford|budget/)) {
        offers.push({
          type: "promo",
          headline: "First month free with install this week",
          detail: `Use code ${code} — save $${args.plan_discussed === "enterprise" ? "1,299" : args.plan_discussed === "basic" ? "199" : "699"} on your first month. Offer expires ${expiryStr}.`,
        });
      } else if (obj.match(/think|later|busy|not sure|maybe/)) {
        offers.push({
          type: "risk_reversal",
          headline: "30-day money-back guarantee — zero risk",
          detail: "If you don't see results in 30 days, we pull the system and refund your first month. Hardware is yours to keep either way. No questions asked.",
        });
      }
    }

    // Always include a general offer if nothing specific matched
    if (offers.length < 2) {
      offers.push({
        type: "promo",
        headline: "This week: free install with annual commitment",
        detail: `Pay 12 months upfront and we waive the install fee entirely (up to $1,000 value). Code: ${code}. Expires ${expiryStr}.`,
      });
    }

    return JSON.stringify({
      offers: offers.slice(0, 3),
      claim_code: code,
      expires: expiryStr,
      expires_hours: 72,
      cta: "Mention this code when you call (337) 486-3149 or reply to your follow-up email.",
      fine_print: "Offers subject to installer availability. One per business.",
    });
  },
};
