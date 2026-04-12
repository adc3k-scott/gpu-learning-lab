// ROXY SaaS Tool: Review Responder
// Drafts professional responses to Google/Yelp reviews.
// Most businesses ignore reviews — this responds for them.

module.exports = {
  name: "respond_to_review",
  description:
    "Draft a professional response to a customer review (Google, Yelp, Facebook). Use when a business owner shares a review they received and wants help responding. Handles positive reviews (thank + reinforce), neutral reviews (acknowledge + invite back), and negative reviews (empathize + resolve + take offline).",
  parameters: {
    type: "object",
    properties: {
      review_text: {
        type: "string",
        description: "The customer's review text",
      },
      star_rating: {
        type: "number",
        description: "Star rating (1-5)",
      },
      reviewer_name: {
        type: "string",
        description: "The reviewer's name",
      },
      business_name: {
        type: "string",
        description: "The business name",
      },
      owner_name: {
        type: "string",
        description: "The business owner's name for signing the response",
      },
      industry: {
        type: "string",
        description: "The business industry",
      },
    },
    required: ["review_text"],
  },
  async execute(args) {
    const stars = args.star_rating || 0;
    const reviewer = args.reviewer_name || "there";
    const bizName = args.business_name || "our business";
    const owner = args.owner_name || "The Team";
    const isPositive = stars >= 4;
    const isNeutral = stars === 3;
    const isNegative = stars <= 2 && stars > 0;
    const noRating = stars === 0;

    let response = "";
    let tone = "";
    let tips = [];

    if (isPositive) {
      tone = "grateful + reinforcing";
      response = `Thank you so much, ${reviewer}! We're thrilled to hear this. ${getPositiveReinforcement(args.review_text, args.industry)} We appreciate you trusting ${bizName} and look forward to seeing you again!\n\n— ${owner}`;
      tips = [
        "Respond within 24 hours for maximum impact",
        "Share this review on your social media — it's free advertising",
        "Consider asking this customer for a referral",
      ];
    } else if (isNeutral) {
      tone = "appreciative + improvement-focused";
      response = `Thank you for your feedback, ${reviewer}. We're glad you chose ${bizName}, and we hear you — we're always working to improve. ${getNeutralBridge(args.review_text)} We'd love the chance to exceed your expectations next time. Please don't hesitate to reach out directly if there's anything we can do.\n\n— ${owner}`;
      tips = [
        "Respond within 12 hours — neutral reviews can go either way",
        "The goal is to turn a 3 into a 5 on their next visit",
        "Consider offering a small gesture (discount, priority booking)",
      ];
    } else if (isNegative) {
      tone = "empathetic + resolution-focused + take offline";
      response = `${reviewer}, thank you for letting us know about this experience. This isn't the standard we hold ourselves to at ${bizName}, and I'm sorry we fell short. ${getNegativeResolution(args.review_text)} I'd like to make this right — please reach out to us directly so we can address this personally.\n\n— ${owner}`;
      tips = [
        "Respond within 6 hours — speed shows you care",
        "NEVER argue or get defensive in a public response",
        "Always take the resolution offline (phone or email)",
        "After resolving, ask if they'd consider updating their review",
        "One great recovery can turn a critic into your biggest advocate",
      ];
    } else {
      // No rating — generate based on sentiment in text
      tone = "professional + appreciative";
      response = `Thank you for sharing your experience, ${reviewer}. We value every piece of feedback at ${bizName}. ${getGenericBridge(args.review_text)} We're always here if you need anything.\n\n— ${owner}`;
      tips = ["Respond to every review — it shows potential customers you're engaged"];
    }

    return JSON.stringify({
      response,
      tone,
      character_count: response.length,
      tips,
      platform_notes: {
        google: "Keep under 4,000 characters. Use the owner's name for authenticity.",
        yelp: "Keep under 5,000 characters. Don't offer incentives for review changes (violates TOS).",
        facebook: "Can be longer. Consider adding a photo of the team for personal touch.",
      },
      important: "Review this response and personalize it before posting. Add any specific details about the customer's visit if you remember them — personalization shows you actually read the review.",
    });
  },
};

function getPositiveReinforcement(text, industry) {
  const lower = (text || "").toLowerCase();
  if (lower.includes("staff") || lower.includes("team") || lower.includes("friendly"))
    return "Our team works hard to make every visit great, and it means the world when customers notice.";
  if (lower.includes("fast") || lower.includes("quick") || lower.includes("on time"))
    return "We know your time is valuable, and we make it a priority to deliver fast, reliable service.";
  if (lower.includes("clean") || lower.includes("professional"))
    return "Professionalism is at the core of everything we do.";
  if (lower.includes("price") || lower.includes("fair") || lower.includes("value"))
    return "We believe in transparent, fair pricing — no surprises.";
  return "Your kind words motivate our entire team to keep raising the bar.";
}

function getNeutralBridge(text) {
  const lower = (text || "").toLowerCase();
  if (lower.includes("wait") || lower.includes("slow") || lower.includes("time"))
    return "We understand that wait times can be frustrating, and we're actively working on solutions to serve you faster.";
  if (lower.includes("price") || lower.includes("expensive"))
    return "We strive to offer the best value for the quality of service we provide.";
  return "Your feedback helps us identify areas where we can do better.";
}

function getNegativeResolution(text) {
  const lower = (text || "").toLowerCase();
  if (lower.includes("rude") || lower.includes("unprofessional") || lower.includes("attitude"))
    return "Every customer deserves to be treated with respect, and we take this very seriously.";
  if (lower.includes("wait") || lower.includes("late") || lower.includes("no show"))
    return "Reliability is something we pride ourselves on, and we clearly missed the mark here.";
  if (lower.includes("wrong") || lower.includes("mistake") || lower.includes("broke"))
    return "We stand behind our work, and we want to make sure this gets resolved correctly.";
  if (lower.includes("price") || lower.includes("charge") || lower.includes("bill"))
    return "Transparent pricing is non-negotiable for us, and I want to review what happened with your bill.";
  return "We take this feedback seriously and want to understand what went wrong.";
}

function getGenericBridge(text) {
  return "We're always looking for ways to improve and provide the best experience for our customers.";
}
