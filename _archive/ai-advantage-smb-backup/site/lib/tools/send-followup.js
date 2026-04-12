// ROXY Tool: Send Follow-Up Email
// Sends a personalized follow-up email via Brevo after capturing a lead.
// Includes their industry playbook highlights, pricing, and booking link.

const BREVO_API_KEY = process.env.BREVO_API_KEY;
const BOOKING_URL = process.env.BOOKING_URL || "https://ai-advantage.info/#contact";

const INDUSTRY_HIGHLIGHTS = {
  "law firm": {
    emoji: "⚖️",
    features: ["Document Q&A — instant case file search", "Contract drafting assistance", "Attorney-client privilege stays on device", "Full audit trail for compliance"],
    recommended: "Pro + DGX Spark",
  },
  "dental office": {
    emoji: "🦷",
    features: ["Insurance verification automation", "Clinical notes assistant", "Smart appointment scheduling", "HIPAA-compliant on-device processing"],
    recommended: "Enterprise + DGX Spark",
  },
  "medical": {
    emoji: "🏥",
    features: ["Insurance verification automation", "Clinical notes assistant", "Smart appointment scheduling", "HIPAA-compliant on-device processing"],
    recommended: "Enterprise + DGX Spark",
  },
  "plumbing": {
    emoji: "🔧",
    features: ["AI phone answering — never miss a call", "Smart dispatch to nearest available truck", "Field quoting from job photos", "Automated customer follow-ups"],
    recommended: "Pro + Mac Mini",
  },
  "electrician": {
    emoji: "⚡",
    features: ["AI phone answering — never miss a call", "Smart dispatch to nearest available truck", "Field quoting from job photos", "Automated customer follow-ups"],
    recommended: "Pro + Mac Mini",
  },
  "hvac": {
    emoji: "❄️",
    features: ["AI phone answering — never miss a call", "Smart dispatch to nearest available truck", "Field quoting from job photos", "Automated customer follow-ups"],
    recommended: "Pro + Mac Mini",
  },
  "restaurant": {
    emoji: "🍽️",
    features: ["Real-time food cost tracking", "Auto-reorder when stock runs low", "Recipe costing per dish", "Inventory prediction to reduce waste"],
    recommended: "Basic + Mac Mini",
  },
  "auto shop": {
    emoji: "🔧",
    features: ["Photo-to-estimate — snap a pic, get a quote", "Customer approval workflows via text", "Parts ordering automation", "Service history tracking"],
    recommended: "Pro + Mac Mini",
  },
  "real estate": {
    emoji: "🏠",
    features: ["Speed-to-lead — instant response to inquiries", "Listing description generator", "CRM automation and follow-ups", "Market analysis assistant"],
    recommended: "Pro + Cloud",
  },
  "construction": {
    emoji: "🏗️",
    features: ["Change order tracking", "Draw schedule management", "Daily log automation", "Subcontractor coordination"],
    recommended: "Pro + Mac Mini",
  },
  "property management": {
    emoji: "🏢",
    features: ["AI maintenance dispatch", "Tenant communication portal", "Owner reporting automation", "Work order management"],
    recommended: "Pro + Mac Mini",
  },
  "retail": {
    emoji: "🛍️",
    features: ["Auto-reorder when inventory drops", "Margin analysis per product", "Inventory prediction", "Customer purchase pattern tracking"],
    recommended: "Basic + Mac Mini",
  },
  "accounting": {
    emoji: "📊",
    features: ["Tax document AI intake", "Deadline tracking and reminders", "Client portal for document upload", "Automated data extraction"],
    recommended: "Pro + DGX Spark",
  },
  "salon": {
    emoji: "✂️",
    features: ["Automated rebooking reminders", "No-show follow-ups via text", "Client history and preferences", "Schedule optimization"],
    recommended: "Basic + Cloud",
  },
  "insurance": {
    emoji: "📋",
    features: ["Multi-carrier quoting assistance", "Renewal tracking and alerts", "Policy comparison tool", "Client communication automation"],
    recommended: "Pro + Mac Mini",
  },
};

function getIndustryInfo(businessType) {
  if (!businessType) return null;
  const bt = businessType.toLowerCase();
  for (const [key, val] of Object.entries(INDUSTRY_HIGHLIGHTS)) {
    if (bt.includes(key)) return { key, ...val };
  }
  return null;
}

function buildEmailHtml(name, businessType, industry) {
  const firstName = name ? name.split(/\s+/)[0] : "there";
  const featureList = industry
    ? industry.features.map((f) => `<li style="margin-bottom:6px">${f}</li>`).join("")
    : "";

  return `
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;color:#333">
  <div style="background:#0a1018;padding:32px 24px;border-radius:12px 12px 0 0;text-align:center">
    <div style="font-size:24px;font-weight:700;color:#fff;letter-spacing:1px">AI Advantage</div>
    <div style="font-size:13px;color:#8fa4bc;margin-top:4px">Your AI. Your Business. Your Data.</div>
  </div>

  <div style="padding:32px 24px;background:#fff;border:1px solid #e5e7eb;border-top:none">
    <p style="font-size:16px;line-height:1.6;margin:0 0 16px">Hey ${firstName},</p>

    <p style="font-size:15px;line-height:1.7;margin:0 0 16px">Thanks for chatting with ROXY! I wanted to follow up with everything we discussed${businessType ? ` about AI for your ${businessType}` : ""}.</p>

    ${industry ? `
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:20px;margin:20px 0">
      <div style="font-size:14px;font-weight:700;color:#166534;margin-bottom:12px">${industry.emoji || "🤖"} What AI Advantage Does for Your Business</div>
      <ul style="font-size:14px;line-height:1.8;color:#333;padding-left:20px;margin:0">${featureList}</ul>
      <div style="font-size:12px;color:#666;margin-top:12px">Recommended setup: <strong>${industry.recommended}</strong></div>
    </div>
    ` : ""}

    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:20px;margin:20px 0">
      <div style="font-size:14px;font-weight:700;color:#1e293b;margin-bottom:12px">How It Works — 5 Steps</div>
      <ol style="font-size:14px;line-height:1.8;color:#333;padding-left:20px;margin:0">
        <li><strong>Discovery</strong> — Free 15-minute call</li>
        <li><strong>Install</strong> — 2-3 hours at your location</li>
        <li><strong>Training</strong> — 30 minutes, whole team</li>
        <li><strong>Monitor</strong> — 24/7 from our facility</li>
        <li><strong>Grow</strong> — Gets smarter over time</li>
      </ol>
    </div>

    <div style="text-align:center;margin:28px 0">
      <a href="${BOOKING_URL}" style="background:#2563eb;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px;display:inline-block">Book Your Free Discovery Call</a>
    </div>

    <p style="font-size:14px;line-height:1.7;color:#666;margin:20px 0 0">Or just reply to this email — I'll get right back to you.</p>

    <div style="border-top:1px solid #e5e7eb;margin-top:28px;padding-top:20px">
      <p style="font-size:14px;margin:0;color:#333"><strong>Scott Tomsu</strong></p>
      <p style="font-size:13px;margin:4px 0 0;color:#666">Founder, AI Advantage</p>
      <p style="font-size:13px;margin:4px 0 0;color:#666">(337) 486-3149 · contact@ai-advantage.info</p>
      <p style="font-size:13px;margin:4px 0 0;color:#666">1201 SE Evangeline Thruway, Lafayette, LA 70501</p>
    </div>
  </div>

  <div style="background:#f8fafc;padding:16px 24px;border-radius:0 0 12px 12px;border:1px solid #e5e7eb;border-top:none;text-align:center">
    <p style="font-size:11px;color:#94a3b8;margin:0">Powered by ADC AI Infrastructure · Lafayette, Louisiana · American-Owned</p>
  </div>
</div>`;
}

module.exports = {
  name: "send_followup_email",
  description:
    "Send a personalized follow-up email to a lead after capturing their information. Includes their industry playbook highlights, the 5-step process, and a booking link. Only call this AFTER capture_lead has been used and you have the visitor's email.",
  parameters: {
    type: "object",
    properties: {
      email: {
        type: "string",
        description: "The visitor's email address (required)",
      },
      name: {
        type: "string",
        description: "The visitor's name",
      },
      business_type: {
        type: "string",
        description: "The visitor's business type (e.g., 'dental office', 'plumbing company')",
      },
    },
    required: ["email"],
  },
  async execute(args) {
    if (!BREVO_API_KEY) {
      return JSON.stringify({ status: "skipped", reason: "Email service not configured" });
    }

    if (!args.email || !args.email.includes("@")) {
      return JSON.stringify({ status: "skipped", reason: "Invalid email address" });
    }

    const industry = getIndustryInfo(args.business_type);
    const htmlContent = buildEmailHtml(args.name, args.business_type, industry);

    const firstName = args.name ? args.name.split(/\s+/)[0] : "";
    const subject = firstName
      ? `${firstName}, here's what AI Advantage can do for your business`
      : "Here's what AI Advantage can do for your business";

    try {
      const response = await fetch("https://api.brevo.com/v3/smtp/email", {
        method: "POST",
        headers: {
          "api-key": BREVO_API_KEY,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          sender: { name: "Scott Tomsu | AI Advantage", email: "contact@ai-advantage.info" },
          to: [{ email: args.email, name: args.name || "" }],
          subject,
          htmlContent,
          replyTo: { email: "contact@ai-advantage.info", name: "AI Advantage" },
        }),
      });

      if (response.ok) {
        return JSON.stringify({
          status: "sent",
          message: "Follow-up email sent successfully with industry details and booking link.",
        });
      }

      const err = await response.json().catch(() => ({}));
      console.error("[ROXY] Brevo email error:", JSON.stringify(err));
      return JSON.stringify({
        status: "failed",
        message: "Could not send email right now, but the lead has been saved.",
      });
    } catch (err) {
      console.error("[ROXY] Email send error:", err.message);
      return JSON.stringify({
        status: "failed",
        message: "Could not send email right now, but the lead has been saved.",
      });
    }
  },
};
