// ROXY — ADC AI Factory Agent
// Self-hosted inference on ADC's own GPU hardware
// Tool-calling agent with playbook RAG, lead capture, quoting, and booking
// Endpoint: RunPod (temporary) -> MARLIE I NVL72 (permanent)

const { isRateLimited } = require("../lib/util/rate-limiter");
const { run: runAgent } = require("../lib/agent/loop");

module.exports = async function handler(req, res) {
  // Only allow POST
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Rate limiting
  const ip =
    req.headers["x-forwarded-for"]?.split(",")[0]?.trim() ||
    req.headers["x-real-ip"] ||
    req.socket?.remoteAddress ||
    "unknown";

  if (isRateLimited(ip)) {
    return res
      .status(429)
      .json({ error: "Too many requests. Please wait a moment." });
  }

  // Parse request body
  const body = req.body || {};

  // Support both old format { message } and new format { messages, sessionId }
  let messages = [];
  let sessionId = body.sessionId || `s_${Date.now()}`;
  let sessionContext = body.sessionContext || {};

  if (body.messages && Array.isArray(body.messages)) {
    // New multi-turn format
    messages = body.messages;
  } else if (body.message && typeof body.message === "string") {
    // Legacy single-message format (backwards compatible)
    messages = [{ role: "user", content: body.message.trim() }];
  } else {
    return res.status(400).json({ error: "Message is required." });
  }

  // Validate the last message
  const lastMsg = messages[messages.length - 1];
  if (!lastMsg || !lastMsg.content || typeof lastMsg.content !== "string") {
    return res.status(400).json({ error: "Message is required." });
  }

  if (lastMsg.content.length > 2000) {
    return res
      .status(400)
      .json({ error: "Message too long. Please keep it under 2000 characters." });
  }

  // Cap conversation history to prevent context overflow
  if (messages.length > 20) {
    messages = messages.slice(-20);
  }

  // Pass IP to session context for analytics
  sessionContext._ip = ip;

  // Run the ROXY agent loop
  try {
    const result = await runAgent({
      messages,
      sessionId,
      sessionContext,
    });

    // Fire analytics events (non-blocking — don't await)
    const analyticsBase = `${req.headers["x-forwarded-proto"] || "https"}://${req.headers.host}/api/analytics`;
    const fireAnalytics = (evt) => {
      fetch(analyticsBase, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(evt),
      }).catch(() => {});
    };

    fireAnalytics({ type: "conversation", channel: "chat" });
    if (result.analytics) {
      fireAnalytics({
        type: "response_time",
        durationMs: result.analytics.durationMs,
        toolsAvailable: result.analytics.toolsAvailable,
        totalTools: result.analytics.totalToolsInRegistry,
      });
    }
    for (const tool of result.toolsUsed) {
      fireAnalytics({ type: "tool_used", tool });
    }
    if (result.sessionContext.leadCaptured && result.toolsUsed.includes("capture_lead")) {
      fireAnalytics({
        type: "lead_captured",
        industry: result.sessionContext.businessType,
        interest_level: "warm",
      });
    }

    return res.status(200).json({
      reply: result.reply,
      source: result.source,
      toolsUsed: result.toolsUsed,
      sessionContext: {
        visitorName: result.sessionContext.visitorName,
        visitorEmail: result.sessionContext.visitorEmail,
        visitorPhone: result.sessionContext.visitorPhone,
        businessType: result.sessionContext.businessType,
        leadCaptured: result.sessionContext.leadCaptured,
      },
    });
  } catch (err) {
    console.error("[ROXY] Agent error:", err.message, err.stack);
    return res.status(500).json({
      error: "Something went wrong. Please try again in a moment.",
    });
  }
};
