// ROXY SaaS Tool: Email Campaign Builder
// Creates drip campaigns from industry templates.
// Brevo does the sending — ROXY writes the content.

module.exports = {
  name: "build_email_campaign",
  description:
    "Create an email drip campaign for a business to nurture their leads or re-engage existing customers. Generates 3-5 emails with subject lines, content, and send timing. Use when a business asks about email marketing, staying in touch with customers, or getting repeat business.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The business industry",
      },
      business_name: {
        type: "string",
        description: "Business name",
      },
      campaign_type: {
        type: "string",
        enum: ["welcome", "reactivation", "seasonal", "referral"],
        description: "Type of campaign (default: welcome)",
      },
      goal: {
        type: "string",
        description: "The business goal (e.g., 'get more repeat customers', 'fill slow days', 'get referrals')",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const biz = args.business_name || "[Your Business]";
    const type = args.campaign_type || "welcome";
    const industry = (args.industry || "").toLowerCase();

    let emails = [];

    if (type === "welcome") {
      emails = [
        {
          day: 0,
          subject: `Welcome to ${biz} — here's what to expect`,
          preview: "You made a great choice. Here's how we take care of you.",
          body_outline: [
            `Thank them for choosing ${biz}`,
            "Recap what you do / what they signed up for",
            "Set expectations (what happens next, how to reach you)",
            "Include your phone number and hours",
            "Personal touch — sign with owner's name",
          ],
          cta: "Save our number in your phone",
        },
        {
          day: 3,
          subject: getIndustrySubject(industry, "tip", biz),
          preview: "A quick tip that'll save you time and money.",
          body_outline: [
            "Share one valuable tip related to their service",
            "Position yourself as the expert",
            "Keep it short — 3-4 sentences max",
            "Link to your website or blog if applicable",
          ],
          cta: "Bookmark this for later",
        },
        {
          day: 7,
          subject: `How was your experience with ${biz}?`,
          preview: "We'd love your honest feedback.",
          body_outline: [
            "Ask how their experience was",
            "Make it easy to leave a Google review (direct link)",
            "Mention that reviews help other families find you",
            "Thank them again",
          ],
          cta: "Leave a quick review (takes 30 seconds)",
        },
        {
          day: 21,
          subject: getIndustrySubject(industry, "value", biz),
          preview: "Something useful from your friends at " + biz,
          body_outline: [
            "Share another valuable piece of content",
            "Could be a seasonal tip, maintenance reminder, or industry insight",
            "Subtle mention of your services without being salesy",
          ],
          cta: "Questions? Just reply to this email",
        },
        {
          day: 30,
          subject: `${biz} referral bonus — share the love`,
          preview: "Know someone who could use our help?",
          body_outline: [
            "Introduce your referral program",
            "Clear incentive (discount, free service, gift card)",
            "Make it easy — give them a shareable link or code",
            "Thank them for being a valued customer",
          ],
          cta: "Share with a friend",
        },
      ];
    } else if (type === "reactivation") {
      emails = [
        {
          day: 0,
          subject: `We miss you at ${biz}!`,
          preview: "It's been a while — we'd love to see you again.",
          body_outline: [
            "Acknowledge it's been a while (don't guilt trip)",
            "Remind them what you do and why they chose you",
            "Offer a 'welcome back' incentive",
          ],
          cta: "Book your next appointment",
        },
        {
          day: 5,
          subject: getIndustrySubject(industry, "seasonal", biz),
          preview: "A timely reminder that could save you money.",
          body_outline: [
            "Seasonal hook relevant to their industry",
            "Why now is the right time to come back",
            "Limited-time offer or availability",
          ],
          cta: "Schedule today",
        },
        {
          day: 14,
          subject: `Last chance: your ${biz} offer expires soon`,
          preview: "Don't miss out — this expires in 48 hours.",
          body_outline: [
            "Final reminder about the offer",
            "Create urgency (real deadline)",
            "Make it dead simple to take action (one-click booking)",
          ],
          cta: "Claim your offer now",
        },
      ];
    } else if (type === "referral") {
      emails = [
        {
          day: 0,
          subject: `You earned a reward from ${biz}`,
          preview: "Thank you for being an amazing customer.",
          body_outline: [
            "Thank them for being a loyal customer",
            "Introduce the referral program with clear terms",
            "Explain the reward (for both them and their referral)",
            "Give them their unique referral code/link",
          ],
          cta: "Share your referral link",
        },
        {
          day: 7,
          subject: `Your friends need ${biz} too`,
          preview: "Share the love — you both get rewarded.",
          body_outline: [
            "Remind them of the referral program",
            "Social proof: 'X customers have already referred friends'",
            "Make sharing easy (pre-written text they can forward)",
          ],
          cta: "Forward this to a friend",
        },
      ];
    }

    return JSON.stringify({
      campaign_type: type,
      business: biz,
      industry: args.industry,
      total_emails: emails.length,
      emails,
      setup_instructions: [
        "Create these emails in Brevo (or your email tool)",
        "Set up the automation trigger (new contact, tag, or date-based)",
        "Test with your own email first",
        "Monitor open rates — aim for 30%+ opens, 5%+ clicks",
        "A/B test subject lines after 100 sends",
      ],
      expected_results: {
        welcome: "Welcome sequences see 50-80% open rates on email 1, and 3x higher lifetime value",
        reactivation: "Reactivation campaigns typically recover 15-25% of lapsed customers",
        referral: "Referral campaigns drive 20-30% of new business for top performers",
      }[type],
      next_step: "Want me to write the full email copy for any of these? Or set up a different campaign type?",
    });
  },
};

function getIndustrySubject(industry, type, biz) {
  const subjects = {
    plumbing: {
      tip: `The $10 fix that prevents 80% of plumbing emergencies`,
      value: `${biz}: 5 things to check before winter hits your pipes`,
      seasonal: `Your pipes need attention before summer — here's why`,
    },
    hvac: {
      tip: `This simple trick cuts your AC bill by 20%`,
      value: `${biz}: Is your AC ready for Louisiana summer?`,
      seasonal: `Don't wait for the first 100° day — prep your AC now`,
    },
    dental: {
      tip: `The brushing mistake 70% of people make`,
      value: `${biz}: Your dental benefits expire Dec 31 — use them`,
      seasonal: `Back-to-school dental checkups — book before the rush`,
    },
    restaurant: {
      tip: `The menu trick that adds $3 to every check`,
      value: `${biz}: This week's specials (and a surprise for regulars)`,
      seasonal: `Festival season is here — reserve your table early`,
    },
    salon: {
      tip: `The one product your stylist actually recommends`,
      value: `${biz}: New season, new look — our latest styles`,
      seasonal: `Holiday party season — book your appointment before we're full`,
    },
  };

  for (const [key, subs] of Object.entries(subjects)) {
    if (industry.includes(key)) return subs[type] || subs.tip;
  }
  return `${biz} has something for you`;
}
