// ROXY Tool: Franchise Qualifier
// Detects multi-location prospects and generates franchise-tier quotes.
// One franchise deal = 8x revenue vs single location.

const PLAN_COSTS = { basic: 199, pro: 699, enterprise: 1299 };
const HARDWARE_COSTS = { cloud: 0, starter: 1200, "mac-mini": 1699, "dgx-spark": 5499 };
const INSTALL_BASE = 1000; // Base install fee per location

// Discount tiers from franchise-playbook.md
function getDiscount(locations) {
  if (locations >= 10) return 0.20;
  if (locations >= 5) return 0.15;
  if (locations >= 3) return 0.10;
  return 0;
}

module.exports = {
  name: "franchise_qualifier",
  description:
    "Qualify and quote a multi-location or franchise prospect. Use this when a visitor mentions multiple locations, franchises, chains, or says they have more than one store/office/location. Generates a franchise-specific quote with volume discounts and shows the total deal value.",
  parameters: {
    type: "object",
    properties: {
      locations: {
        type: "number",
        description: "Number of locations (or expected locations)",
      },
      industry: {
        type: "string",
        description: "The business industry",
      },
      plan: {
        type: "string",
        enum: ["basic", "pro", "enterprise"],
        description: "Monthly plan tier (default: pro)",
      },
      hardware: {
        type: "string",
        enum: ["cloud", "starter", "mac-mini", "dgx-spark"],
        description: "Hardware per location (default: mac-mini)",
      },
      same_systems: {
        type: "boolean",
        description: "Whether all locations use the same POS/software",
      },
      decision_maker: {
        type: "string",
        description: "Who makes the purchasing decision (owner, ops manager, etc.)",
      },
    },
    required: ["locations"],
  },
  async execute(args) {
    const locations = args.locations || 1;
    const plan = args.plan || "pro";
    const hardware = args.hardware || "mac-mini";
    const discount = getDiscount(locations);
    const discountPct = Math.round(discount * 100);

    const basePlanCost = PLAN_COSTS[plan] || 699;
    const baseHardwareCost = HARDWARE_COSTS[hardware] || 1699;

    // First location = full price. Locations 2+ get discount.
    const firstLocationMonthly = basePlanCost;
    const additionalLocationMonthly = Math.round(basePlanCost * (1 - discount));
    const totalMonthly = firstLocationMonthly + (additionalLocationMonthly * (locations - 1));
    const totalAnnual = totalMonthly * 12;

    // Install fees
    const firstInstallFee = INSTALL_BASE; // Full 3-hour install
    const additionalInstallFee = Math.round(INSTALL_BASE * (1 - discount)); // 1-hour clone
    const totalInstallFees = firstInstallFee + (additionalInstallFee * (locations - 1));

    // Hardware
    const totalHardware = baseHardwareCost * locations;

    // Year 1 total
    const yearOneTotal = totalAnnual + totalInstallFees + totalHardware;

    // Compare to single-location pricing
    const singleLocationAnnual = (basePlanCost * 12) + INSTALL_BASE + baseHardwareCost;
    const singleLocationEquivalent = singleLocationAnnual * locations;
    const savings = singleLocationEquivalent - yearOneTotal;

    const quote = {
      deal_type: "Franchise / Multi-Location",
      locations,
      discount: discountPct > 0 ? `${discountPct}% volume discount` : "Standard pricing (discount at 3+ locations)",
      industry: args.industry || "Not specified",

      // Per-location breakdown
      first_location: {
        monthly: `$${firstLocationMonthly}/mo`,
        install: `$${firstInstallFee} (full 3-hour install)`,
        hardware: `$${baseHardwareCost.toLocaleString()}`,
        setup_time: "3 hours",
      },
      additional_locations: locations > 1 ? {
        monthly_each: `$${additionalLocationMonthly}/mo`,
        install_each: `$${additionalInstallFee} (1-hour clone deploy)`,
        hardware_each: `$${baseHardwareCost.toLocaleString()}`,
        setup_time: "1 hour each (clone from master config)",
      } : null,

      // Totals
      total_monthly: `$${totalMonthly.toLocaleString()}/mo`,
      total_annual: `$${totalAnnual.toLocaleString()}/yr`,
      total_install_fees: `$${totalInstallFees.toLocaleString()}`,
      total_hardware: `$${totalHardware.toLocaleString()}`,
      year_one_total: `$${yearOneTotal.toLocaleString()}`,

      // Savings vs buying individually
      savings_vs_individual: savings > 0 ? `$${savings.toLocaleString()} saved vs individual pricing` : null,

      // How it works
      deployment_model: [
        "One discovery call with the owner/ops manager",
        "Build master config from flagship location",
        `Clone deploy to ${locations - 1} additional locations (1 hour each)`,
        "Single dashboard shows all locations",
        "Each location manager sees only their site",
        "Centralized monitoring from MARLIE I",
      ],

      // The pitch
      value_prop: `${locations} locations, one decision. Master config clones to every site in 1 hour. Single dashboard for the owner. Individual dashboards for each manager. All running on ADC's infrastructure.`,
    };

    if (args.same_systems === false) {
      quote.note = "Different systems across locations adds complexity. First install may take 4 hours instead of 3. Clone deploys still work for the AI agent — just the integration layer varies per site.";
    }

    return JSON.stringify(quote);
  },
};
