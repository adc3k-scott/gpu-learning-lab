// ROXY SaaS Tool: Ad Copy Generator
// Generates Facebook, Instagram, and Google ad copy tailored to the business.
// This is what marketing agencies charge $500-2K/mo for.

const AD_TEMPLATES = {
  facebook: {
    format: "Facebook/Instagram Feed Ad",
    specs: "Primary text: 125 chars optimal (up to 250). Headline: 40 chars. Description: 30 chars. CTA button.",
  },
  instagram_story: {
    format: "Instagram Story Ad",
    specs: "Short, punchy. 1-2 sentences max. Swipe up CTA.",
  },
  google_search: {
    format: "Google Search Ad",
    specs: "3 headlines (30 chars each). 2 descriptions (90 chars each). Display URL.",
  },
  google_local: {
    format: "Google Local Services Ad",
    specs: "Business category + service area + trust signals.",
  },
};

const INDUSTRY_ANGLES = {
  plumbing: {
    pain_points: ["burst pipes at 2 AM", "waiting all day for a plumber", "surprise bills", "no-show plumbers"],
    value_props: ["same-day service", "upfront pricing", "licensed & insured", "24/7 emergency"],
    seasonal: { summer: "AC drain lines clogging", winter: "frozen pipes", spring: "water heater flush season" },
    keywords: ["plumber near me", "emergency plumber", "water heater repair", "drain cleaning"],
  },
  hvac: {
    pain_points: ["AC dies in July", "heating bill too high", "uneven temperatures", "old system breaking down"],
    value_props: ["same-day repair", "free estimates", "financing available", "energy savings"],
    seasonal: { summer: "AC tune-up before the heat", winter: "heater repair season", spring: "AC maintenance" },
    keywords: ["AC repair near me", "HVAC service", "air conditioning installation", "heating repair"],
  },
  dental: {
    pain_points: ["afraid of the dentist", "no insurance", "can't get an appointment", "tooth pain now"],
    value_props: ["gentle care", "same-day appointments", "payment plans", "family-friendly"],
    seasonal: { summer: "back-to-school checkups", winter: "use your benefits before Dec 31", spring: "spring cleaning for your smile" },
    keywords: ["dentist near me", "emergency dentist", "teeth cleaning", "dental implants"],
  },
  restaurant: {
    pain_points: ["long wait times", "bad reviews", "can't find good staff", "food quality inconsistent"],
    value_props: ["fresh ingredients", "family recipes", "fast service", "local favorite"],
    seasonal: { summer: "patio season", winter: "comfort food", spring: "crawfish season", fall: "football watch parties" },
    keywords: ["restaurants near me", "best food Lafayette", "lunch specials", "catering"],
  },
  salon: {
    pain_points: ["bad haircut last time", "can't get an appointment", "too expensive", "boring look"],
    value_props: ["expert stylists", "same-day availability", "loyalty rewards", "trendsetting looks"],
    seasonal: { summer: "summer color refresh", winter: "holiday glam", spring: "new season new look", fall: "back to school cuts" },
    keywords: ["hair salon near me", "best hairstylist", "color specialist", "blowout bar"],
  },
  "real estate": {
    pain_points: ["house sat on market", "lowball offers", "can't find the right home", "lost bidding war"],
    value_props: ["sells fast", "top dollar", "local expert", "personalized search"],
    seasonal: { spring: "spring selling season", summer: "move before school starts", fall: "less competition", winter: "motivated buyers" },
    keywords: ["homes for sale", "realtor near me", "sell my house", "buy a home"],
  },
  "auto shop": {
    pain_points: ["check engine light on", "overcharged at the dealer", "car won't start", "need it fixed today"],
    value_props: ["honest pricing", "fast turnaround", "certified mechanics", "warranty on repairs"],
    seasonal: { summer: "AC recharge season", winter: "battery and tire checks", spring: "road trip ready" },
    keywords: ["auto repair near me", "mechanic", "oil change", "brake repair"],
  },
  law: {
    pain_points: ["injured in accident", "facing charges", "business dispute", "need a will"],
    value_props: ["free consultation", "no fee unless we win", "aggressive representation", "local trusted firm"],
    seasonal: {},
    keywords: ["lawyer near me", "personal injury attorney", "criminal defense", "estate planning"],
  },
  insurance: {
    pain_points: ["paying too much", "bad coverage", "claim denied", "agent never calls back"],
    value_props: ["save up to 30%", "multiple carriers", "local agent", "claims advocacy"],
    seasonal: { fall: "open enrollment", spring: "policy review season" },
    keywords: ["insurance quotes", "auto insurance", "home insurance", "life insurance"],
  },
};

function getIndustryData(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, data] of Object.entries(INDUSTRY_ANGLES)) {
    if (lower.includes(key)) return { key, ...data };
  }
  if (lower.match(/plumb/)) return { key: "plumbing", ...INDUSTRY_ANGLES.plumbing };
  if (lower.match(/hvac|cool|heat|air con/)) return { key: "hvac", ...INDUSTRY_ANGLES.hvac };
  if (lower.match(/dent/)) return { key: "dental", ...INDUSTRY_ANGLES.dental };
  if (lower.match(/restaurant|bar|food/)) return { key: "restaurant", ...INDUSTRY_ANGLES.restaurant };
  if (lower.match(/salon|barber|hair/)) return { key: "salon", ...INDUSTRY_ANGLES.salon };
  if (lower.match(/real estate|realtor/)) return { key: "real estate", ...INDUSTRY_ANGLES["real estate"] };
  if (lower.match(/auto|mechanic/)) return { key: "auto shop", ...INDUSTRY_ANGLES["auto shop"] };
  if (lower.match(/law|attorney/)) return { key: "law", ...INDUSTRY_ANGLES.law };
  if (lower.match(/insur/)) return { key: "insurance", ...INDUSTRY_ANGLES.insurance };
  return null;
}

function getSeason() {
  const month = new Date().getMonth();
  if (month >= 2 && month <= 4) return "spring";
  if (month >= 5 && month <= 7) return "summer";
  if (month >= 8 && month <= 10) return "fall";
  return "winter";
}

module.exports = {
  name: "generate_ad_copy",
  description:
    "Generate ready-to-run ad copy for Facebook, Instagram, and Google tailored to the business's industry and location. Creates multiple variations with different angles (pain point, seasonal, value prop). Use when a customer asks about marketing, advertising, or says 'how do I get more customers?'",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The business's industry",
      },
      business_name: {
        type: "string",
        description: "The business name",
      },
      location: {
        type: "string",
        description: "City/area for geo-targeting",
      },
      platform: {
        type: "string",
        enum: ["facebook", "instagram_story", "google_search", "google_local", "all"],
        description: "Which platform (default: all)",
      },
      special_offer: {
        type: "string",
        description: "Any current promotion to include",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const data = getIndustryData(args.industry);
    const bizName = args.business_name || "Your Business";
    const location = args.location || "your area";
    const season = getSeason();
    const platform = args.platform || "all";

    if (!data) {
      return JSON.stringify({
        generated: false,
        message: `I can generate custom ad copy for ${args.industry} on a discovery call where we learn your specific value props.`,
      });
    }

    const seasonalAngle = data.seasonal[season] || null;
    const ads = [];

    // Facebook/Instagram ad
    if (platform === "all" || platform === "facebook") {
      const pain = data.pain_points[Math.floor(Math.random() * data.pain_points.length)];
      const value = data.value_props[0];
      ads.push({
        platform: "Facebook / Instagram Feed",
        variations: [
          {
            angle: "Pain Point",
            primary_text: `Tired of ${pain}? ${bizName} in ${location} delivers ${value} — guaranteed. Book online or call today.${args.special_offer ? ` ${args.special_offer}` : ""}`,
            headline: `${bizName} — ${value.charAt(0).toUpperCase() + value.slice(1)}`,
            cta: "Book Now",
          },
          {
            angle: "Social Proof",
            primary_text: `${location}'s trusted ${data.key} experts. See why hundreds of families choose ${bizName}. ⭐⭐⭐⭐⭐`,
            headline: `${location}'s #1 Rated ${data.key.charAt(0).toUpperCase() + data.key.slice(1)}`,
            cta: "Learn More",
          },
          {
            angle: seasonalAngle ? "Seasonal" : "Urgency",
            primary_text: seasonalAngle
              ? `${seasonalAngle} — don't wait until it's an emergency. ${bizName} has same-day availability this week.`
              : `Limited slots available this week at ${bizName}. ${data.value_props[1].charAt(0).toUpperCase() + data.value_props[1].slice(1)}. Book now before we're full.`,
            headline: seasonalAngle || `This Week Only — ${bizName}`,
            cta: "Book Now",
          },
        ],
      });
    }

    // Google Search ads
    if (platform === "all" || platform === "google_search") {
      ads.push({
        platform: "Google Search",
        variations: [
          {
            headlines: [
              `${bizName} — ${location}`,
              data.value_props[0].charAt(0).toUpperCase() + data.value_props[0].slice(1),
              "Call Now — Open Today",
            ],
            descriptions: [
              `${location}'s trusted ${data.key} pros. ${data.value_props[1].charAt(0).toUpperCase() + data.value_props[1].slice(1)}. ${data.value_props[2].charAt(0).toUpperCase() + data.value_props[2].slice(1)}.`,
              `${args.special_offer || data.value_props[3]?.charAt(0).toUpperCase() + data.value_props[3]?.slice(1) || "Book your appointment today"}. Call or book online.`,
            ],
            target_keywords: data.keywords.slice(0, 4),
          },
        ],
      });
    }

    // Instagram Story
    if (platform === "all" || platform === "instagram_story") {
      ads.push({
        platform: "Instagram Story",
        variations: [
          {
            text: `Need a ${data.key}? 👆 ${bizName} — ${data.value_props[0]}. Tap to book.`,
            cta: "Swipe Up",
          },
          {
            text: seasonalAngle
              ? `${seasonalAngle} 🔥 ${bizName} has you covered. Book today.`
              : `${bizName} — ${location}'s favorite ${data.key}. ⭐ Tap to see why.`,
            cta: "Swipe Up",
          },
        ],
      });
    }

    return JSON.stringify({
      generated: true,
      business: bizName,
      industry: data.key,
      location,
      season,
      ads,
      tips: [
        "Run 2-3 variations simultaneously and kill the lowest performer after 3 days",
        `Target radius: 10-25 miles from ${location} for local services`,
        "Budget: Start at $10-20/day per platform, scale what converts",
        "Always include a phone number or booking link in your landing page",
      ],
      next_step: "Want me to create a full 30-day ad calendar with rotating copy? Or focus on one platform?",
    });
  },
};
