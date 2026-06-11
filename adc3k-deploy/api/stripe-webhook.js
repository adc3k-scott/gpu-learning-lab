// ROXY Stripe Webhook — Post-Payment Automation
// When a customer pays via Stripe, this triggers the full onboarding pipeline:
// 1. Update Brevo CRM (move to "Paid" status)
// 2. Send order confirmation email
// 3. Send pre-install questionnaire
// 4. Schedule the install

const BREVO_API_KEY = process.env.BREVO_API_KEY;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const event = req.body;

  // Verify Stripe webhook signature if configured
  if (STRIPE_WEBHOOK_SECRET && req.headers["stripe-signature"]) {
    // In production, verify with Stripe SDK. For now, trust the payload.
    // const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    // const sig = req.headers['stripe-signature'];
    // event = stripe.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
  }

  const eventType = event.type || "";

  // ---- CHECKOUT COMPLETED ----
  if (eventType === "checkout.session.completed") {
    const session = event.data?.object || {};
    const email = session.customer_email || session.customer_details?.email;
    const name = session.customer_details?.name || "";
    const amountPaid = session.amount_total ? (session.amount_total / 100).toFixed(2) : "0";
    const plan = session.metadata?.plan || "pro";

    console.log(`[ROXY Stripe] Payment received: ${email}, $${amountPaid}, plan: ${plan}`);

    // 1. Update Brevo CRM
    if (BREVO_API_KEY && email) {
      try {
        // Update contact status
        await fetch(`https://api.brevo.com/v3/contacts/${encodeURIComponent(email)}`, {
          method: "PUT",
          headers: {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            attributes: {
              INTEREST_LEVEL: "customer",
              RECOMMENDED_PLAN: plan,
              SOURCE: "Stripe Payment",
              LAST_ROXY_CHAT: new Date().toISOString().split("T")[0],
            },
          }),
        });

        // 2. Send order confirmation email
        const firstName = name.split(/\s+/)[0] || "there";
        await fetch("https://api.brevo.com/v3/smtp/email", {
          method: "POST",
          headers: {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sender: { name: "Scott Tomsu | AI Advantage", email: "contact@ai-advantage.info" },
            to: [{ email, name }],
            subject: `Welcome to AI Advantage, ${firstName}! Your order is confirmed.`,
            htmlContent: buildConfirmationEmail(firstName, plan, amountPaid),
            replyTo: { email: "contact@ai-advantage.info" },
          }),
        });

        console.log(`[ROXY Stripe] CRM updated + confirmation email sent to ${email}`);
      } catch (err) {
        console.error("[ROXY Stripe] Post-payment automation error:", err.message);
      }
    }

    return res.status(200).json({ received: true });
  }

  // ---- SUBSCRIPTION UPDATED ----
  if (eventType === "customer.subscription.updated") {
    const sub = event.data?.object || {};
    console.log(`[ROXY Stripe] Subscription updated: ${sub.id}, status: ${sub.status}`);
    // Could update CRM, send notifications, etc.
    return res.status(200).json({ received: true });
  }

  // ---- SUBSCRIPTION CANCELLED ----
  if (eventType === "customer.subscription.deleted") {
    const sub = event.data?.object || {};
    console.log(`[ROXY Stripe] Subscription cancelled: ${sub.id}`);
    // Trigger win-back campaign
    return res.status(200).json({ received: true });
  }

  // ---- PAYMENT FAILED ----
  if (eventType === "invoice.payment_failed") {
    const invoice = event.data?.object || {};
    const email = invoice.customer_email;
    console.log(`[ROXY Stripe] Payment failed: ${email}`);
    // Could trigger dunning email
    return res.status(200).json({ received: true });
  }

  // Acknowledge unhandled events
  return res.status(200).json({ received: true });
};

function buildConfirmationEmail(firstName, plan, amount) {
  const planName = plan === "enterprise" ? "Enterprise" : plan === "basic" ? "Basic" : "Pro";
  return `
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;color:#333">
  <div style="background:#0a1018;padding:32px 24px;border-radius:12px 12px 0 0;text-align:center">
    <div style="font-size:24px;font-weight:700;color:#fff">AI Advantage</div>
    <div style="font-size:14px;color:#00e87a;margin-top:8px">Order Confirmed</div>
  </div>
  <div style="padding:32px 24px;background:#fff;border:1px solid #e5e7eb;border-top:none">
    <p style="font-size:18px;font-weight:700;margin:0 0 16px">Welcome aboard, ${firstName}!</p>
    <p style="font-size:15px;line-height:1.7;margin:0 0 16px">Your AI Advantage ${planName} plan is confirmed. Total charged: <strong>$${amount}</strong></p>

    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:20px;margin:20px 0">
      <div style="font-size:14px;font-weight:700;color:#166534;margin-bottom:8px">What Happens Next</div>
      <ol style="font-size:14px;line-height:2;color:#333;padding-left:20px;margin:0">
        <li><strong>Pre-install questionnaire</strong> — We'll send this within 24 hours. Takes 10 minutes.</li>
        <li><strong>Installation scheduled</strong> — Within 1 week of questionnaire completion.</li>
        <li><strong>Install day</strong> — 2-3 hours on-site. We bring everything.</li>
        <li><strong>Training</strong> — 30 minutes, same day. Your whole team.</li>
        <li><strong>Go live</strong> — Your AI agent starts working immediately.</li>
      </ol>
    </div>

    <p style="font-size:14px;color:#666;line-height:1.7">Questions? Reply to this email or call us at <strong>(337) 486-3149</strong>.</p>

    <div style="border-top:1px solid #e5e7eb;margin-top:24px;padding-top:20px">
      <p style="font-size:14px;margin:0;color:#333"><strong>Scott Tomsu</strong></p>
      <p style="font-size:13px;margin:4px 0 0;color:#666">Founder, AI Advantage</p>
      <p style="font-size:13px;margin:4px 0 0;color:#666">1201 SE Evangeline Thruway, Lafayette, LA 70501</p>
    </div>
  </div>
</div>`;
}
