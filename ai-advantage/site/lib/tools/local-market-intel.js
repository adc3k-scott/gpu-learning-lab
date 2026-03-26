// ROXY Tool: Local Market Intel
// Shows the prospect how many competitors are in their area and who's adopting AI.
// Creates FOMO — "only 2 of 47 plumbers in Lafayette use AI agents."

// Lafayette-area business counts by industry (from public data / estimates)
// These are conservative estimates for the greater Lafayette MSA (~500K population)
const MARKET_DATA = {
  plumbing: { count: 47, ai_adopted: 2, growth_rate: "steady", avg_revenue: "$800K-$2M" },
  hvac: { count: 38, ai_adopted: 1, growth_rate: "growing fast (climate)", avg_revenue: "$500K-$3M" },
  electrical: { count: 35, ai_adopted: 1, growth_rate: "steady", avg_revenue: "$500K-$1.5M" },
  dental: { count: 62, ai_adopted: 0, growth_rate: "competitive", avg_revenue: "$800K-$2.5M" },
  medical: { count: 180, ai_adopted: 0, growth_rate: "consolidating", avg_revenue: "$1M-$10M" },
  restaurant: { count: 340, ai_adopted: 0, growth_rate: "high turnover", avg_revenue: "$300K-$2M" },
  "auto shop": { count: 55, ai_adopted: 0, growth_rate: "steady", avg_revenue: "$400K-$1.5M" },
  "real estate": { count: 120, ai_adopted: 1, growth_rate: "cyclical", avg_revenue: "varies widely" },
  construction: { count: 85, ai_adopted: 1, growth_rate: "booming (I-49, LNG)", avg_revenue: "$1M-$20M" },
  "property management": { count: 28, ai_adopted: 0, growth_rate: "growing (rentals up)", avg_revenue: "$200K-$2M" },
  retail: { count: 250, ai_adopted: 0, growth_rate: "shifting online", avg_revenue: "$200K-$5M" },
  accounting: { count: 45, ai_adopted: 0, growth_rate: "steady", avg_revenue: "$300K-$2M" },
  salon: { count: 95, ai_adopted: 0, growth_rate: "competitive", avg_revenue: "$100K-$500K" },
  insurance: { count: 65, ai_adopted: 0, growth_rate: "consolidating", avg_revenue: "$500K-$3M" },
  law: { count: 70, ai_adopted: 0, growth_rate: "steady", avg_revenue: "$500K-$5M" },
  veterinary: { count: 22, ai_adopted: 0, growth_rate: "growing (pet ownership up)", avg_revenue: "$500K-$2M" },
  trucking: { count: 40, ai_adopted: 0, growth_rate: "growing (LNG/oil)", avg_revenue: "$1M-$10M" },
};

function findMarket(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, data] of Object.entries(MARKET_DATA)) {
    if (lower.includes(key)) return { key, ...data };
  }
  if (lower.match(/plumb/)) return { key: "plumbing", ...MARKET_DATA.plumbing };
  if (lower.match(/hvac|cool|heat|air/)) return { key: "hvac", ...MARKET_DATA.hvac };
  if (lower.match(/electri/)) return { key: "electrical", ...MARKET_DATA.electrical };
  if (lower.match(/dent/)) return { key: "dental", ...MARKET_DATA.dental };
  if (lower.match(/doctor|clinic|health/)) return { key: "medical", ...MARKET_DATA.medical };
  if (lower.match(/restaurant|bar|food|cafe/)) return { key: "restaurant", ...MARKET_DATA.restaurant };
  if (lower.match(/auto|mechanic/)) return { key: "auto shop", ...MARKET_DATA["auto shop"] };
  if (lower.match(/real estate|realtor/)) return { key: "real estate", ...MARKET_DATA["real estate"] };
  if (lower.match(/construct|contractor|builder/)) return { key: "construction", ...MARKET_DATA.construction };
  if (lower.match(/property|landlord|rental/)) return { key: "property management", ...MARKET_DATA["property management"] };
  if (lower.match(/retail|store|boutique/)) return { key: "retail", ...MARKET_DATA.retail };
  if (lower.match(/tax|cpa|account/)) return { key: "accounting", ...MARKET_DATA.accounting };
  if (lower.match(/salon|barber|spa|hair/)) return { key: "salon", ...MARKET_DATA.salon };
  if (lower.match(/insur/)) return { key: "insurance", ...MARKET_DATA.insurance };
  if (lower.match(/law|attorney|legal/)) return { key: "law", ...MARKET_DATA.law };
  if (lower.match(/vet|animal/)) return { key: "veterinary", ...MARKET_DATA.veterinary };
  if (lower.match(/truck|freight|haul/)) return { key: "trucking", ...MARKET_DATA.trucking };
  return null;
}

module.exports = {
  name: "local_market_intel",
  description:
    "Show the prospect their local competitive landscape — how many businesses like theirs are in the area and how many use AI. Creates urgency through competitive awareness. Use this when a prospect is local to Lafayette or Louisiana, or when you need to create FOMO about being an early adopter.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The prospect's industry",
      },
      location: {
        type: "string",
        description: "Their city/area (default: Lafayette)",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const market = findMarket(args.industry);
    const location = args.location || "the greater Lafayette area";

    if (!market) {
      return JSON.stringify({
        available: false,
        message: `I don't have specific market data for ${args.industry} in ${location}, but I can tell you that AI adoption in small business is under 5% nationwide. Early movers have a massive advantage.`,
      });
    }

    const adoptionPct = ((market.ai_adopted / market.count) * 100).toFixed(1);
    const unadopted = market.count - market.ai_adopted;

    return JSON.stringify({
      available: true,
      location,
      industry: market.key,
      total_businesses: market.count,
      using_ai: market.ai_adopted,
      not_using_ai: unadopted,
      adoption_rate: `${adoptionPct}%`,
      market_trend: market.growth_rate,
      avg_revenue_range: market.avg_revenue,

      insight: market.ai_adopted === 0
        ? `There are ${market.count} ${market.key} businesses in ${location}. ZERO are using AI agents. You would be the first — that's a massive first-mover advantage in a market of ${market.count}.`
        : `There are ${market.count} ${market.key} businesses in ${location}. Only ${market.ai_adopted} use AI agents. That means ${unadopted} competitors are still doing everything manually. The window to be an early adopter is open right now — but it's closing.`,

      competitive_angle: `Every day you wait, the odds that your competitor down the street gets there first go up. In a market of ${market.count}, being one of the first ${Math.min(5, Math.ceil(market.count * 0.1))} to adopt AI means you capture the customers they're too slow to serve.`,

      fomo: market.ai_adopted > 0
        ? `${market.ai_adopted} of your competitors already made the move. They're answering calls you're missing right now.`
        : `Nobody in your market has done this yet. First mover gets the edge.`,
    });
  },
};
