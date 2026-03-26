// ROXY Tool: Outbound Calling via Bland.ai
// Triggers ROXY to CALL a prospect. Same brain, same tools, but by phone.
// "We'll call you in 2 minutes" — and ROXY actually does.

const BLAND_API_KEY = process.env.BLAND_API_KEY;
const BLAND_PHONE_NUMBER = process.env.BLAND_PHONE_NUMBER || "+13374863149"; // AI Advantage line
const PHONE_WEBHOOK_URL = process.env.PHONE_WEBHOOK_URL || "https://ai-advantage.info/api/phone";

module.exports = {
  name: "initiate_outbound_call",
  description:
    "Call a prospect on the phone using ROXY's AI. Use this when a hot lead wants a callback, when a prospect says 'call me', or to follow up with a captured lead who provided their phone number. ROXY will call them, qualify them, and capture the lead — all automatically.",
  parameters: {
    type: "object",
    properties: {
      phone_number: {
        type: "string",
        description: "The prospect's phone number to call",
      },
      prospect_name: {
        type: "string",
        description: "The prospect's name for personalization",
      },
      industry: {
        type: "string",
        description: "Their industry so ROXY knows which playbook to use",
      },
      context: {
        type: "string",
        description: "Brief context about why we're calling (e.g., 'They asked about plumbing AI during chat')",
      },
      delay_minutes: {
        type: "number",
        description: "Minutes to wait before calling (default: 0 = immediate). Use 2 for 'we'll call you right back'.",
      },
    },
    required: ["phone_number"],
  },
  async execute(args) {
    if (!BLAND_API_KEY) {
      return JSON.stringify({
        status: "not_configured",
        message: "Outbound calling is being set up. Our team will call the prospect directly at " + args.phone_number,
        fallback: `Please have someone call ${args.prospect_name || "the prospect"} at ${args.phone_number}. Context: ${args.context || "Interested in AI Advantage."}`,
      });
    }

    // Format phone number
    let phone = args.phone_number.replace(/[^0-9+]/g, "");
    if (!phone.startsWith("+")) {
      phone = phone.length === 10 ? "+1" + phone : "+" + phone;
    }

    // Build the call prompt — ROXY's phone personality
    const firstName = args.prospect_name ? args.prospect_name.split(/\s+/)[0] : "";
    const greeting = firstName
      ? `Hey ${firstName}, this is ROXY calling from AI Advantage. ${args.context ? args.context : "You were just chatting with me on our website and I wanted to follow up personally."}`
      : `Hi, this is ROXY from AI Advantage. ${args.context ? args.context : "I'm calling to follow up on your interest in our AI solutions."}`;

    const task = `${greeting}

Your goal is to:
1. Confirm they're interested in AI for their ${args.industry || "business"}
2. Ask what their biggest operational pain point is
3. Briefly explain how AI Advantage solves it (reference the ${args.industry || "general"} playbook)
4. Book a 15-minute discovery call or get their email to send more info
5. Be warm, conversational, and brief — this is a phone call, not a lecture

Keep responses short (1-3 sentences). Be friendly with a slight Southern charm.
If they're busy, ask for a better time and offer to call back.
If they're not interested, thank them and move on gracefully.

Contact info to share if asked:
- Phone: (337) 486-3149
- Website: ai-advantage.info
- Email: contact@ai-advantage.info`;

    try {
      const body = {
        phone_number: phone,
        from: BLAND_PHONE_NUMBER,
        task,
        model: "enhanced",
        language: "en",
        voice: "maya",
        max_duration: 300, // 5 minutes max
        wait_for_greeting: true,
        record: true,
        webhook: PHONE_WEBHOOK_URL,
        metadata: {
          source: "roxy_outbound",
          prospect_name: args.prospect_name || null,
          industry: args.industry || null,
          context: args.context || null,
        },
      };

      // Delay if requested
      if (args.delay_minutes && args.delay_minutes > 0) {
        body.start_time = new Date(Date.now() + args.delay_minutes * 60 * 1000).toISOString();
      }

      const response = await fetch("https://api.bland.ai/v1/calls", {
        method: "POST",
        headers: {
          Authorization: BLAND_API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        const timing = args.delay_minutes
          ? `in ${args.delay_minutes} minutes`
          : "right now";

        return JSON.stringify({
          status: "call_initiated",
          call_id: data.call_id || data.id,
          message: `ROXY is calling ${args.prospect_name || phone} ${timing}. She'll qualify them, pitch the ${args.industry || "relevant"} playbook, and try to book a discovery call.`,
          phone_called: phone,
          timing,
        });
      }

      const err = await response.json().catch(() => ({}));
      console.error("[ROXY] Bland.ai call error:", JSON.stringify(err));
      return JSON.stringify({
        status: "call_failed",
        message: `Couldn't initiate the call right now. Please have someone call ${args.prospect_name || "the prospect"} at ${phone} manually.`,
        error: err.message || "API error",
      });
    } catch (err) {
      return JSON.stringify({
        status: "call_failed",
        message: `Call system temporarily unavailable. Please call ${phone} manually.`,
      });
    }
  },
};
