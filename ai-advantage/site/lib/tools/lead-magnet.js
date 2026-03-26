// ROXY SaaS Tool: Lead Magnet Generator
// Creates downloadable guides and checklists that businesses can use to capture leads.
// Lead magnets convert 3-5x better than cold ads.

const LEAD_MAGNETS = {
  plumbing: [
    {
      title: "10 Signs Your Water Heater Is About to Die",
      type: "Checklist",
      hook: "Don't wait for the flood. Check these 10 warning signs before it's too late.",
      items: [
        "Water heater is more than 10 years old",
        "Rusty water coming from hot water tap",
        "Rumbling or banging noises during heating",
        "Water pooling around the base",
        "Hot water runs out faster than usual",
        "Visible corrosion on tank or fittings",
        "Pilot light keeps going out (gas units)",
        "Metallic taste or smell in hot water",
        "Energy bills increasing with no other explanation",
        "Water temperature fluctuates unpredictably",
      ],
      cta: "If you checked 3 or more, call us before it becomes an emergency.",
    },
    {
      title: "The Homeowner's Emergency Plumbing Guide",
      type: "Guide",
      hook: "Know what to do in the first 5 minutes of a plumbing emergency. This guide has saved homeowners thousands.",
      sections: ["How to shut off your main water valve", "Burst pipe: immediate steps", "Toilet overflow: quick fix", "When to call a pro vs. DIY", "Your emergency contact checklist"],
      cta: "Save this guide to your phone. You'll be glad you did.",
    },
  ],
  dental: [
    {
      title: "What Your Dentist Wishes You Knew: 7 Habits That Save Your Teeth",
      type: "Guide",
      hook: "Simple daily habits that prevent 90% of dental problems. Free from your dentist.",
      sections: ["The 2-minute brushing technique most people get wrong", "Why flossing matters more than you think", "Foods that secretly destroy enamel", "The real deal on whitening", "When to see your dentist NOW vs. next month", "How to save money on dental care", "Teaching your kids habits that last a lifetime"],
      cta: "Download and share with your family. Your teeth will thank you.",
    },
  ],
  restaurant: [
    {
      title: "The Restaurant Owner's Food Cost Cheat Sheet",
      type: "Checklist",
      hook: "If your food cost is over 30%, you're leaving money on the table. This cheat sheet shows you exactly where.",
      items: [
        "Calculate food cost percentage for your top 10 menu items",
        "Identify your 3 highest-margin dishes (promote these)",
        "Find your 3 lowest-margin dishes (reprice or remove)",
        "Track daily waste in dollars (not just weight)",
        "Set par levels for every ingredient",
        "Check portion sizes against recipes weekly",
        "Compare vendor prices monthly (at least 3 suppliers)",
        "Review your menu mix: what actually sells vs. what you think sells",
      ],
      cta: "Most restaurant owners save $1,500-3,000/month just by tracking these numbers.",
    },
  ],
  hvac: [
    {
      title: "Louisiana Summer Survival Guide: 15 Ways to Cut Your AC Bill",
      type: "Guide",
      hook: "Louisiana summers are brutal. These 15 tips can cut your cooling bill by 20-40% without suffering.",
      sections: ["The optimal thermostat setting (it's not what you think)", "Ceiling fan direction matters — which way for summer", "The $10 fix that improves AC efficiency by 15%", "When to repair vs. replace your unit", "Tax credits for energy-efficient upgrades", "Smart thermostat: worth it or gimmick?"],
      cta: "Save this before July hits. Your wallet will thank you.",
    },
  ],
  salon: [
    {
      title: "Your At-Home Hair Care Routine: What Your Stylist Actually Recommends",
      type: "Guide",
      hook: "Stop guessing. Your stylist's real advice for keeping your hair salon-fresh between visits.",
      sections: ["How often to actually wash your hair (by hair type)", "The one product that makes the biggest difference", "Heat styling without the damage", "Color care: making it last 2x longer", "When to come back (honest timeline by service)"],
      cta: "Save this and tag your stylist. We love when clients take care of their hair between visits!",
    },
  ],
  "real estate": [
    {
      title: "The First-Time Homebuyer's Checklist for Louisiana",
      type: "Checklist",
      hook: "Don't miss a step. This checklist covers everything from credit to closing — specific to Louisiana.",
      items: [
        "Check your credit score (740+ for best rates)",
        "Get pre-approved (not just pre-qualified)",
        "Calculate your actual budget (include insurance, taxes, HOA)",
        "Research Louisiana homestead exemption ($75K property tax break)",
        "Flood zone check (FEMA maps — critical in LA)",
        "Home inspection (non-negotiable)",
        "Title search and title insurance",
        "Closing costs budget (2-5% of purchase price)",
        "Homeowner's insurance + flood insurance quotes",
        "Final walkthrough before closing",
      ],
      cta: "Buying in Louisiana? We know every parish. Let's find your home.",
    },
  ],
};

function getLeadMagnets(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, magnets] of Object.entries(LEAD_MAGNETS)) {
    if (lower.includes(key)) return { key, magnets };
  }
  if (lower.match(/plumb/)) return { key: "plumbing", magnets: LEAD_MAGNETS.plumbing };
  if (lower.match(/hvac|cool|heat/)) return { key: "hvac", magnets: LEAD_MAGNETS.hvac };
  if (lower.match(/dent/)) return { key: "dental", magnets: LEAD_MAGNETS.dental };
  if (lower.match(/restaurant|food/)) return { key: "restaurant", magnets: LEAD_MAGNETS.restaurant };
  if (lower.match(/salon|hair|barber/)) return { key: "salon", magnets: LEAD_MAGNETS.salon };
  if (lower.match(/real estate|realtor/)) return { key: "real estate", magnets: LEAD_MAGNETS["real estate"] };
  return null;
}

module.exports = {
  name: "generate_lead_magnet",
  description:
    "Generate a downloadable lead magnet (checklist, guide, or cheat sheet) that the business can use to capture leads on their website, social media, or ads. Lead magnets convert 3-5x better than cold advertising. Use when a business asks about marketing, lead generation, or getting more customers.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The business industry",
      },
      business_name: {
        type: "string",
        description: "Business name for branding",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const data = getLeadMagnets(args.industry);
    const biz = args.business_name || "Your Business";

    if (!data) {
      return JSON.stringify({
        generated: false,
        message: `I can create a custom lead magnet for ${args.industry} on a discovery call. Every industry has content their customers are dying to know.`,
      });
    }

    const magnets = data.magnets.map((m) => ({
      ...m,
      branded_title: m.title,
      how_to_use: [
        "Share the link on your Facebook page with a 'Download Free' CTA",
        "Run a Facebook ad: 'Free [Guide/Checklist] — Download Now' (costs ~$1-3 per lead)",
        "Add a popup on your website: 'Get our free guide — enter your email'",
        "Print QR codes on your business cards that link to the download",
        "Email it to existing customers — they share it with friends",
      ],
      estimated_leads: "20-50 leads/month with a $5-10/day ad budget",
    }));

    return JSON.stringify({
      generated: true,
      business: biz,
      industry: data.key,
      lead_magnets: magnets,
      strategy: "The lead magnet captures their email. Then your AI agent follows up automatically with industry-specific content. That's the funnel: Free guide → Email captured → AI nurtures → Discovery call → Customer.",
      next_step: "Want me to set up the landing page and email capture for this? Or create magnets for a different topic?",
    });
  },
};
