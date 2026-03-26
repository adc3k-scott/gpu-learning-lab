// ROXY Tool: Payment Link Generator
// Generates a Stripe payment link so customers can pay in-session.
// This is the closer — turns conversations into revenue.

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;

// Product catalog — maps to Stripe price IDs once configured
// For now, generates descriptive links. Once Stripe is set up, swap to real price IDs.
const PRODUCTS = {
  // Monthly plans
  basic_monthly: { name: "AI Advantage Basic", price: 199, interval: "month" },
  pro_monthly: { name: "AI Advantage Pro", price: 699, interval: "month" },
  enterprise_monthly: { name: "AI Advantage Enterprise", price: 1299, interval: "month" },
  // Hardware (one-time)
  starter_kit: { name: "Starter Kit", price: 1200, interval: null },
  mac_mini: { name: "Mac Mini On-Site AI", price: 1699, interval: null },
  dgx_spark: { name: "DGX Spark AI Supercomputer", price: 5499, interval: null },
};

// Map Stripe price IDs when available
const STRIPE_PRICES = {
  basic_monthly: process.env.STRIPE_PRICE_BASIC,
  pro_monthly: process.env.STRIPE_PRICE_PRO,
  enterprise_monthly: process.env.STRIPE_PRICE_ENTERPRISE,
  starter_kit: process.env.STRIPE_PRICE_STARTER,
  mac_mini: process.env.STRIPE_PRICE_MACMINI,
  dgx_spark: process.env.STRIPE_PRICE_DGX,
};

module.exports = {
  name: "generate_payment_link",
  description:
    "Generate a payment link so the customer can pay right now in the chat. Use this when a customer says they're ready to buy, wants to get started, or asks 'how do I pay?' Creates a Stripe checkout link with their specific plan and hardware choice. This is the closer — don't hesitate to offer it when the prospect is hot.",
  parameters: {
    type: "object",
    properties: {
      plan: {
        type: "string",
        enum: ["basic", "pro", "enterprise"],
        description: "The monthly plan tier",
      },
      hardware: {
        type: "string",
        enum: ["none", "starter", "mac-mini", "dgx-spark"],
        description: "Hardware selection (none = cloud only)",
      },
      customer_email: {
        type: "string",
        description: "Customer email for the checkout",
      },
      customer_name: {
        type: "string",
        description: "Customer name",
      },
      discount_code: {
        type: "string",
        description: "Any promo or referral code to apply",
      },
    },
    required: ["plan"],
  },
  async execute(args) {
    const plan = PRODUCTS[`${args.plan}_monthly`];
    if (!plan) {
      return JSON.stringify({ status: "error", message: "Invalid plan selected" });
    }

    const hardwareKey = args.hardware === "starter" ? "starter_kit"
      : args.hardware === "mac-mini" ? "mac_mini"
      : args.hardware === "dgx-spark" ? "dgx_spark"
      : null;
    const hardware = hardwareKey ? PRODUCTS[hardwareKey] : null;

    // Calculate totals
    const monthlyTotal = plan.price;
    const hardwareTotal = hardware ? hardware.price : 0;
    const firstPayment = monthlyTotal + hardwareTotal;

    // If Stripe is configured, generate a real checkout link
    if (STRIPE_SECRET_KEY) {
      try {
        const lineItems = [];

        // Add subscription plan
        const planPriceId = STRIPE_PRICES[`${args.plan}_monthly`];
        if (planPriceId) {
          lineItems.push({ price: planPriceId, quantity: 1 });
        }

        // Add hardware (one-time)
        if (hardwareKey) {
          const hwPriceId = STRIPE_PRICES[hardwareKey];
          if (hwPriceId) {
            lineItems.push({ price: hwPriceId, quantity: 1 });
          }
        }

        if (lineItems.length > 0) {
          const params = new URLSearchParams();
          lineItems.forEach((item, i) => {
            params.append(`line_items[${i}][price]`, item.price);
            params.append(`line_items[${i}][quantity]`, item.quantity.toString());
          });
          params.append("mode", "subscription");
          params.append("success_url", "https://ai-advantage.info?payment=success");
          params.append("cancel_url", "https://ai-advantage.info?payment=cancelled");
          if (args.customer_email) {
            params.append("customer_email", args.customer_email);
          }

          const response = await fetch("https://api.stripe.com/v1/checkout/sessions", {
            method: "POST",
            headers: {
              Authorization: `Bearer ${STRIPE_SECRET_KEY}`,
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: params.toString(),
          });

          if (response.ok) {
            const session = await response.json();
            return JSON.stringify({
              status: "link_ready",
              payment_url: session.url,
              plan: plan.name,
              monthly: `$${monthlyTotal}/mo`,
              hardware: hardware ? `${hardware.name} ($${hardwareTotal.toLocaleString()})` : "Cloud Only (free)",
              first_payment: `$${firstPayment.toLocaleString()}`,
              message: "Click the link to complete your purchase. Secure checkout powered by Stripe.",
            });
          }
        }
      } catch (err) {
        console.error("[ROXY] Stripe error:", err.message);
      }
    }

    // No Stripe configured — return a summary with CTA
    return JSON.stringify({
      status: "quote_ready",
      plan: plan.name,
      monthly: `$${monthlyTotal}/mo`,
      hardware: hardware ? `${hardware.name} ($${hardwareTotal.toLocaleString()})` : "Cloud Only (free)",
      first_payment: `$${firstPayment.toLocaleString()}`,
      ongoing: `$${monthlyTotal}/mo after first payment`,
      next_step: "To complete your purchase, call us at (337) 486-3149 or email contact@ai-advantage.info. We'll have you set up within 48 hours.",
      includes: [
        "Professional on-site installation (2-3 hours)",
        "Team training (30 minutes)",
        "24/7 monitoring from MARLIE I",
        "No long-term contract",
      ],
      message: "Payment processing is being set up. For now, call or email us to complete your order — we'll lock in your pricing.",
    });
  },
};
