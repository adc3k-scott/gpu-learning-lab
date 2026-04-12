// ROXY Subagent: CRM Lookup
// Checks Brevo for existing contacts before creating duplicates.
// Enables "Welcome back" and conversation continuity across sessions.

const BREVO_API_KEY = process.env.BREVO_API_KEY;

module.exports = {
  name: "crm_lookup",
  description:
    "Look up a visitor in the CRM by email to check if they're an existing lead or returning customer. Use this BEFORE capture_lead when a visitor provides their email, to avoid duplicates and to personalize the conversation if they've been here before.",
  parameters: {
    type: "object",
    properties: {
      email: {
        type: "string",
        description: "The visitor's email address to look up",
      },
    },
    required: ["email"],
  },
  async execute(args) {
    if (!BREVO_API_KEY || !args.email) {
      return JSON.stringify({ found: false, reason: "CRM not configured or no email provided" });
    }

    try {
      const response = await fetch(
        `https://api.brevo.com/v3/contacts/${encodeURIComponent(args.email)}`,
        {
          headers: {
            "api-key": BREVO_API_KEY,
            Accept: "application/json",
          },
        }
      );

      if (response.status === 404) {
        return JSON.stringify({
          found: false,
          message: "New visitor — not in CRM yet.",
        });
      }

      if (!response.ok) {
        return JSON.stringify({ found: false, reason: "CRM lookup failed" });
      }

      const contact = await response.json();
      const attrs = contact.attributes || {};
      const lists = contact.listIds || [];

      const result = {
        found: true,
        email: contact.email,
        firstName: attrs.FIRSTNAME || null,
        lastName: attrs.LASTNAME || null,
        company: attrs.COMPANY || null,
        phone: attrs.SMS || null,
        createdAt: contact.createdAt,
        isAIAdvantageLead: lists.includes(9),
        listCount: lists.length,
        message: "Returning visitor — already in CRM.",
      };

      // Calculate how long ago they were added
      if (contact.createdAt) {
        const created = new Date(contact.createdAt);
        const now = new Date();
        const daysAgo = Math.floor((now - created) / (1000 * 60 * 60 * 24));
        if (daysAgo === 0) {
          result.lastSeen = "today";
        } else if (daysAgo === 1) {
          result.lastSeen = "yesterday";
        } else if (daysAgo < 30) {
          result.lastSeen = `${daysAgo} days ago`;
        } else {
          result.lastSeen = `${Math.floor(daysAgo / 30)} months ago`;
        }
      }

      return JSON.stringify(result);
    } catch (err) {
      return JSON.stringify({ found: false, reason: "CRM lookup error" });
    }
  },
};
