// ROXY SaaS Tool: Review Request Generator
// Creates and sends review requests to customers after service.
// 5-star reviews are the #1 growth driver for local businesses.

const BREVO_API_KEY = process.env.BREVO_API_KEY;

module.exports = {
  name: "request_review",
  description:
    "Generate and optionally send a review request to a customer after completing a job or service. Creates a personalized message asking for a Google review with a direct link. Use when a business owner says they need more reviews, or after discussing how to grow their online presence.",
  parameters: {
    type: "object",
    properties: {
      customer_name: {
        type: "string",
        description: "The customer who received the service",
      },
      customer_email: {
        type: "string",
        description: "Customer's email to send the request",
      },
      customer_phone: {
        type: "string",
        description: "Customer's phone for SMS request",
      },
      business_name: {
        type: "string",
        description: "The business requesting the review",
      },
      service_performed: {
        type: "string",
        description: "What service was done (e.g., 'water heater installation', 'teeth cleaning')",
      },
      google_place_id: {
        type: "string",
        description: "Google Place ID for direct review link (optional)",
      },
      send: {
        type: "boolean",
        description: "Whether to actually send the request via email/SMS (default: false, just generates the template)",
      },
    },
    required: ["business_name"],
  },
  async execute(args) {
    const firstName = args.customer_name ? args.customer_name.split(/\s+/)[0] : "there";
    const biz = args.business_name || "us";
    const service = args.service_performed || "your recent visit";

    // Generate Google review URL
    const reviewUrl = args.google_place_id
      ? `https://search.google.com/local/writereview?placeid=${args.google_place_id}`
      : `https://www.google.com/search?q=${encodeURIComponent(args.business_name + " reviews")}`;

    // SMS version (under 160 chars)
    const smsText = `Hey ${firstName}! Thanks for choosing ${biz}. If you had a great experience, a quick Google review would mean the world to us: ${reviewUrl}`;

    // Email version
    const emailSubject = `${firstName}, how was your experience with ${biz}?`;
    const emailHtml = `
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:500px;margin:0 auto;color:#333">
  <div style="padding:32px 24px;text-align:center">
    <div style="font-size:48px;margin-bottom:16px">⭐⭐⭐⭐⭐</div>
    <h2 style="font-size:22px;font-weight:700;margin:0 0 12px">How did we do?</h2>
    <p style="font-size:15px;line-height:1.7;color:#555;margin:0 0 24px">Hey ${firstName}, thanks for trusting ${biz} with ${service}. We hope you had a great experience!</p>
    <p style="font-size:15px;line-height:1.7;color:#555;margin:0 0 24px">If you have 30 seconds, a quick Google review helps other people in the community find us. It means more than you know.</p>
    <a href="${reviewUrl}" style="background:#4285f4;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px;display:inline-block">Leave a Review on Google</a>
    <p style="font-size:13px;color:#999;margin:24px 0 0">Thank you for choosing ${biz}! 🙏</p>
  </div>
</div>`;

    const result = {
      sms_template: smsText,
      sms_length: smsText.length,
      email_subject: emailSubject,
      email_html: emailHtml,
      review_url: reviewUrl,
      tips: [
        "Send within 2 hours of completing the job — while the experience is fresh",
        "SMS gets 3x the response rate of email for review requests",
        "Don't offer incentives for reviews — it violates Google/Yelp TOS",
        "Follow up once after 3 days if they haven't reviewed. Then stop — don't spam.",
        "Respond to every review you get (use ROXY's respond_to_review tool)",
      ],
    };

    // Send if requested and we have the means
    if (args.send && BREVO_API_KEY) {
      const sent = [];

      if (args.customer_email) {
        try {
          await fetch("https://api.brevo.com/v3/smtp/email", {
            method: "POST",
            headers: {
              "api-key": BREVO_API_KEY,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              sender: { name: biz, email: "contact@ai-advantage.info" },
              to: [{ email: args.customer_email, name: args.customer_name || "" }],
              subject: emailSubject,
              htmlContent: emailHtml,
            }),
          });
          sent.push("email");
        } catch (e) { /* non-critical */ }
      }

      if (args.customer_phone) {
        let phone = args.customer_phone.replace(/[^0-9+]/g, "");
        if (!phone.startsWith("+")) phone = phone.length === 10 ? "+1" + phone : "+" + phone;
        try {
          await fetch("https://api.brevo.com/v3/transactionalSMS/sms", {
            method: "POST",
            headers: {
              "api-key": BREVO_API_KEY,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              type: "transactional",
              sender: "ROXY",
              recipient: phone,
              content: smsText,
            }),
          });
          sent.push("sms");
        } catch (e) { /* non-critical */ }
      }

      result.sent_via = sent;
      result.message = sent.length > 0
        ? `Review request sent via ${sent.join(" and ")}!`
        : "Templates generated but no contact info provided to send.";
    } else {
      result.message = "Review request templates generated. Share these with your customer or say 'send it' to deliver automatically.";
    }

    return JSON.stringify(result);
  },
};
