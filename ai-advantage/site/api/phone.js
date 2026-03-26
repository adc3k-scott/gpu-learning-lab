// ROXY Phone Agent — Bland.ai integration
// When someone calls (337) 486-3149, Bland.ai handles the voice.
// This endpoint gives Bland.ai access to ROXY's brain for real-time answers.
//
// Bland.ai calls this webhook mid-conversation to get ROXY's response
// to customer questions. Same 23 tools, same playbook knowledge, just on the phone.

const { run: runAgent } = require("../lib/agent/loop");

const BLAND_WEBHOOK_SECRET = process.env.BLAND_WEBHOOK_SECRET;

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Optional: verify Bland.ai webhook signature
  if (BLAND_WEBHOOK_SECRET) {
    const sig = req.headers["x-bland-signature"] || req.headers["authorization"];
    if (sig !== BLAND_WEBHOOK_SECRET && sig !== `Bearer ${BLAND_WEBHOOK_SECRET}`) {
      return res.status(401).json({ error: "Unauthorized" });
    }
  }

  const payload = req.body || {};

  // Bland.ai sends different payloads depending on the integration type:
  // 1. "dynamic_data" — mid-call request for information
  // 2. "call_ended" — post-call summary for lead capture
  const eventType = payload.event || payload.type || "dynamic_data";

  // ---- MID-CALL: Bland.ai asks ROXY for an answer ----
  if (eventType === "dynamic_data" || payload.text || payload.message) {
    const customerMessage = payload.text || payload.message || payload.transcript_last || "";
    const callerId = payload.from || payload.caller_id || "unknown";

    if (!customerMessage) {
      return res.status(200).json({ response: "How can I help you today?" });
    }

    // Build conversation from Bland.ai's transcript
    const messages = [];

    // If Bland sends a transcript array, use it
    if (payload.transcript && Array.isArray(payload.transcript)) {
      for (const turn of payload.transcript.slice(-10)) {
        messages.push({
          role: turn.speaker === "agent" ? "assistant" : "user",
          content: turn.text || turn.content || "",
        });
      }
    } else {
      // Single message mode
      messages.push({ role: "user", content: customerMessage });
    }

    // Extract any known info from Bland's variables
    const sessionContext = {
      _channel: "phone",
      _callerId: callerId,
    };
    if (payload.variables) {
      if (payload.variables.name) sessionContext.visitorName = payload.variables.name;
      if (payload.variables.email) sessionContext.visitorEmail = payload.variables.email;
      if (payload.variables.business_type) sessionContext.businessType = payload.variables.business_type;
    }

    try {
      const result = await runAgent({
        messages,
        sessionId: `phone_${payload.call_id || Date.now()}`,
        sessionContext,
      });

      // Return response in Bland.ai's expected format
      return res.status(200).json({
        response: result.reply,
        // Pass any captured data back to Bland.ai as variables
        variables: {
          visitor_name: result.sessionContext.visitorName || null,
          visitor_email: result.sessionContext.visitorEmail || null,
          business_type: result.sessionContext.businessType || null,
          lead_captured: result.sessionContext.leadCaptured || false,
          tools_used: result.toolsUsed.join(", "),
        },
      });
    } catch (err) {
      console.error("[ROXY Phone] Agent error:", err.message);
      return res.status(200).json({
        response: "I'd love to help with that. Let me connect you with our team directly. Can I get your name and the best number to reach you?",
      });
    }
  }

  // ---- POST-CALL: Bland.ai sends call summary for lead capture ----
  if (eventType === "call_ended" || payload.status === "completed") {
    const vars = payload.variables || {};
    const summary = payload.summary || payload.concatenated_transcript || "";

    // If we got contact info from the call, capture the lead
    if (vars.email || vars.name || vars.phone) {
      try {
        const { executeTool } = require("../lib/tools");
        await executeTool("capture_lead", {
          name: vars.name || null,
          email: vars.email || null,
          phone: vars.phone || payload.from || null,
          business_type: vars.business_type || null,
          interest_level: vars.lead_captured ? "hot" : "warm",
          notes: `Phone call via (337) 486-3149. Duration: ${payload.call_length || "unknown"}s. ${summary.slice(0, 200)}`,
        }, { sessionId: `phone_${payload.call_id}` });
      } catch (err) {
        console.error("[ROXY Phone] Lead capture error:", err.message);
      }
    }

    console.log("[ROXY Phone] Call ended:", {
      from: payload.from,
      duration: payload.call_length,
      lead: vars.name || "unknown",
      tools: vars.tools_used || "none",
    });

    return res.status(200).json({ status: "processed" });
  }

  // Unknown event type — acknowledge
  return res.status(200).json({ status: "ok" });
};
