// ROXY Analytics Dashboard API
// Tracks conversations, tool usage, conversion rates, industry breakdown.
// GET /api/analytics — returns current stats
// POST /api/analytics — logs an event

// In-memory analytics store (resets on cold start — upgrade to Vercel KV later)
const stats = {
  startedAt: new Date().toISOString(),
  conversations: {
    total: 0,
    today: 0,
    byChannel: { chat: 0, phone: 0 },
  },
  leads: {
    total: 0,
    today: 0,
    byIndustry: {},
    byInterestLevel: { hot: 0, warm: 0, cold: 0 },
  },
  tools: {
    totalCalls: 0,
    byTool: {},
  },
  conversions: {
    chatToLead: { chats: 0, leads: 0 },
    leadToBooking: { leads: 0, bookings: 0 },
    leadToEmail: { leads: 0, emails: 0 },
  },
  performance: {
    avgResponseMs: 0,
    totalResponseMs: 0,
    responseCount: 0,
    toolSelectReduction: [], // track how much tool selector reduces
  },
  topQuestions: {},
  topObjections: {},
  competitorsMentioned: {},
  lastUpdated: null,
};

function getToday() {
  return new Date().toISOString().split("T")[0];
}

let currentDay = getToday();
function resetDailyCounters() {
  const today = getToday();
  if (today !== currentDay) {
    stats.conversations.today = 0;
    stats.leads.today = 0;
    currentDay = today;
  }
}

module.exports = async function handler(req, res) {
  // CORS for dashboard access
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-API-Key");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // GET — return current stats
  if (req.method === "GET") {
    resetDailyCounters();
    const convRate = stats.conversions.chatToLead.chats > 0
      ? ((stats.conversions.chatToLead.leads / stats.conversions.chatToLead.chats) * 100).toFixed(1)
      : "0.0";

    return res.status(200).json({
      ...stats,
      computed: {
        conversionRate: `${convRate}%`,
        avgResponseMs: stats.performance.responseCount > 0
          ? Math.round(stats.performance.totalResponseMs / stats.performance.responseCount)
          : 0,
        topIndustries: Object.entries(stats.leads.byIndustry)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5),
        topTools: Object.entries(stats.tools.byTool)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 10),
      },
    });
  }

  // POST — log an event
  if (req.method === "POST") {
    const event = req.body || {};
    resetDailyCounters();
    stats.lastUpdated = new Date().toISOString();

    switch (event.type) {
      case "conversation":
        stats.conversations.total++;
        stats.conversations.today++;
        stats.conversations.byChannel[event.channel || "chat"]++;
        stats.conversions.chatToLead.chats++;
        break;

      case "lead_captured":
        stats.leads.total++;
        stats.leads.today++;
        if (event.industry) {
          stats.leads.byIndustry[event.industry] = (stats.leads.byIndustry[event.industry] || 0) + 1;
        }
        if (event.interest_level) {
          stats.leads.byInterestLevel[event.interest_level] = (stats.leads.byInterestLevel[event.interest_level] || 0) + 1;
        }
        stats.conversions.chatToLead.leads++;
        break;

      case "tool_used":
        stats.tools.totalCalls++;
        if (event.tool) {
          stats.tools.byTool[event.tool] = (stats.tools.byTool[event.tool] || 0) + 1;
        }
        break;

      case "booking_made":
        stats.conversions.leadToBooking.bookings++;
        break;

      case "email_sent":
        stats.conversions.leadToEmail.emails++;
        break;

      case "response_time":
        if (event.durationMs) {
          stats.performance.totalResponseMs += event.durationMs;
          stats.performance.responseCount++;
        }
        if (event.toolsAvailable !== undefined && event.totalTools !== undefined) {
          stats.performance.toolSelectReduction.push({
            available: event.toolsAvailable,
            total: event.totalTools,
            reduction: `${Math.round((1 - event.toolsAvailable / event.totalTools) * 100)}%`,
          });
          // Keep only last 100 entries
          if (stats.performance.toolSelectReduction.length > 100) {
            stats.performance.toolSelectReduction = stats.performance.toolSelectReduction.slice(-50);
          }
        }
        break;

      case "competitor_mentioned":
        if (event.competitor) {
          stats.competitorsMentioned[event.competitor] = (stats.competitorsMentioned[event.competitor] || 0) + 1;
        }
        break;

      case "objection":
        if (event.objection) {
          stats.topObjections[event.objection] = (stats.topObjections[event.objection] || 0) + 1;
        }
        break;
    }

    return res.status(200).json({ status: "logged" });
  }

  return res.status(405).json({ error: "Method not allowed" });
};
