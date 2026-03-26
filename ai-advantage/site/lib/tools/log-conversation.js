// ROXY Tool: Conversation Logger
// Logs conversation summaries to Brevo as deal notes and saves raw data for training.
// This is the data flywheel — every conversation makes ROXY smarter.

const BREVO_API_KEY = process.env.BREVO_API_KEY;

module.exports = {
  name: "log_conversation",
  description:
    "Log a conversation summary when a meaningful interaction ends. Call this when the visitor says goodbye, stops responding after getting a quote, or at the end of a productive conversation. Summarize what was discussed, what tools were used, and the outcome (lead captured, quote given, booking made, etc.).",
  parameters: {
    type: "object",
    properties: {
      email: {
        type: "string",
        description: "The visitor's email if captured",
      },
      summary: {
        type: "string",
        description: "Brief summary of the conversation (2-3 sentences max)",
      },
      industry: {
        type: "string",
        description: "The visitor's industry if identified",
      },
      outcome: {
        type: "string",
        enum: ["lead_captured", "quote_given", "booking_made", "info_only", "objection_handled", "lost"],
        description: "The outcome of the conversation",
      },
      objections: {
        type: "string",
        description: "Any objections raised (e.g., 'too expensive', 'already have a system', 'not ready yet')",
      },
      competitor_mentioned: {
        type: "string",
        description: "Any competitor software mentioned (e.g., 'ServiceTitan', 'Toast')",
      },
      recommended_plan: {
        type: "string",
        description: "The plan ROXY recommended (e.g., 'Pro + Mac Mini')",
      },
      interest_level: {
        type: "string",
        enum: ["hot", "warm", "cold"],
        description: "How interested the visitor seemed",
      },
    },
    required: ["summary", "outcome"],
  },
  async execute(args, context) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      sessionId: context?.sessionId || "unknown",
      email: args.email || null,
      summary: args.summary,
      industry: args.industry || null,
      outcome: args.outcome,
      objections: args.objections || null,
      competitor_mentioned: args.competitor_mentioned || null,
      recommended_plan: args.recommended_plan || null,
      interest_level: args.interest_level || "warm",
    };

    // If we have the visitor's email, add a note to their Brevo contact
    if (BREVO_API_KEY && args.email) {
      try {
        // Build the note text
        const noteParts = [`ROXY Chat (${new Date().toLocaleDateString()})`];
        noteParts.push(args.summary);
        if (args.industry) noteParts.push(`Industry: ${args.industry}`);
        if (args.outcome) noteParts.push(`Outcome: ${args.outcome.replace(/_/g, " ")}`);
        if (args.recommended_plan) noteParts.push(`Recommended: ${args.recommended_plan}`);
        if (args.interest_level) noteParts.push(`Interest: ${args.interest_level}`);
        if (args.objections) noteParts.push(`Objections: ${args.objections}`);
        if (args.competitor_mentioned) noteParts.push(`Competitor: ${args.competitor_mentioned}`);

        const noteText = noteParts.join("\n");

        // Update contact attributes with latest conversation data
        const attributes = {};
        if (args.industry) attributes.COMPANY = args.industry;

        await fetch(`https://api.brevo.com/v3/contacts/${encodeURIComponent(args.email)}`, {
          method: "PUT",
          headers: {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ attributes }),
        });

        // Create a deal to track this conversation as a sales opportunity
        // (Brevo deals are the best way to track sales pipeline from ROXY)
        try {
          await fetch("https://api.brevo.com/v3/crm/deals", {
            method: "POST",
            headers: {
              "api-key": BREVO_API_KEY,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: `ROXY Lead: ${args.email}${args.industry ? ` (${args.industry})` : ""}`,
              attributes: {
                deal_description: noteText,
                deal_stage: args.outcome === "booking_made" ? "Demo Scheduled"
                  : args.outcome === "quote_given" ? "Qualified"
                  : args.outcome === "lead_captured" ? "New Lead"
                  : "Contact Made",
              },
            }),
          });
        } catch (dealErr) {
          // Deal creation is optional — don't fail the tool
        }

        logEntry.brevo_updated = true;
      } catch (err) {
        logEntry.brevo_updated = false;
        logEntry.brevo_error = err.message;
      }
    }

    return JSON.stringify({
      status: "logged",
      message: "Conversation logged for training and follow-up.",
      entry: logEntry,
    });
  },
};
