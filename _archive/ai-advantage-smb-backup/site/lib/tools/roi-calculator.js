// ROXY Tool: ROI Calculator
// Calculates return on investment based on the visitor's specific business pain points.
// Uses industry-specific benchmarks to show dollar impact.

// Industry benchmarks — conservative estimates
const INDUSTRY_DATA = {
  plumbing: {
    avg_job_value: 200,
    avg_missed_calls_week: 5,
    avg_no_show_rate: 0.12,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 20,
    avg_follow_up_conversion: 0.25,
    label: "plumbing company",
  },
  hvac: {
    avg_job_value: 350,
    avg_missed_calls_week: 5,
    avg_no_show_rate: 0.10,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 20,
    avg_follow_up_conversion: 0.25,
    label: "HVAC company",
  },
  electrical: {
    avg_job_value: 250,
    avg_missed_calls_week: 4,
    avg_no_show_rate: 0.10,
    avg_admin_hours_week: 12,
    admin_hourly_cost: 20,
    avg_follow_up_conversion: 0.25,
    label: "electrical company",
  },
  dental: {
    avg_job_value: 450,
    avg_missed_calls_week: 8,
    avg_no_show_rate: 0.15,
    avg_admin_hours_week: 20,
    admin_hourly_cost: 22,
    avg_follow_up_conversion: 0.30,
    label: "dental office",
  },
  medical: {
    avg_job_value: 300,
    avg_missed_calls_week: 10,
    avg_no_show_rate: 0.18,
    avg_admin_hours_week: 25,
    admin_hourly_cost: 22,
    avg_follow_up_conversion: 0.30,
    label: "medical practice",
  },
  restaurant: {
    avg_job_value: 35,
    avg_missed_calls_week: 15,
    avg_no_show_rate: 0.12,
    avg_admin_hours_week: 10,
    admin_hourly_cost: 15,
    avg_follow_up_conversion: 0.20,
    food_waste_pct: 0.08,
    avg_monthly_food_cost: 15000,
    label: "restaurant",
  },
  "auto shop": {
    avg_job_value: 400,
    avg_missed_calls_week: 4,
    avg_no_show_rate: 0.08,
    avg_admin_hours_week: 12,
    admin_hourly_cost: 18,
    avg_follow_up_conversion: 0.30,
    label: "auto shop",
  },
  "real estate": {
    avg_job_value: 8000,
    avg_missed_calls_week: 3,
    avg_no_show_rate: 0.05,
    avg_admin_hours_week: 10,
    admin_hourly_cost: 25,
    avg_follow_up_conversion: 0.15,
    speed_to_lead_value: 2000,
    label: "real estate agency",
  },
  construction: {
    avg_job_value: 5000,
    avg_missed_calls_week: 3,
    avg_no_show_rate: 0.05,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 25,
    avg_follow_up_conversion: 0.20,
    label: "construction company",
  },
  "property management": {
    avg_job_value: 150,
    avg_missed_calls_week: 8,
    avg_no_show_rate: 0.10,
    avg_admin_hours_week: 20,
    admin_hourly_cost: 18,
    avg_follow_up_conversion: 0.25,
    label: "property management company",
  },
  retail: {
    avg_job_value: 50,
    avg_missed_calls_week: 5,
    avg_no_show_rate: 0.0,
    avg_admin_hours_week: 10,
    admin_hourly_cost: 15,
    avg_follow_up_conversion: 0.20,
    inventory_waste_pct: 0.05,
    avg_monthly_inventory: 20000,
    label: "retail store",
  },
  accounting: {
    avg_job_value: 500,
    avg_missed_calls_week: 3,
    avg_no_show_rate: 0.05,
    avg_admin_hours_week: 20,
    admin_hourly_cost: 30,
    avg_follow_up_conversion: 0.30,
    label: "accounting firm",
  },
  salon: {
    avg_job_value: 65,
    avg_missed_calls_week: 8,
    avg_no_show_rate: 0.20,
    avg_admin_hours_week: 8,
    admin_hourly_cost: 15,
    avg_follow_up_conversion: 0.35,
    label: "salon",
  },
  insurance: {
    avg_job_value: 1200,
    avg_missed_calls_week: 4,
    avg_no_show_rate: 0.08,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 22,
    avg_follow_up_conversion: 0.20,
    label: "insurance agency",
  },
  law: {
    avg_job_value: 2000,
    avg_missed_calls_week: 3,
    avg_no_show_rate: 0.05,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 35,
    avg_follow_up_conversion: 0.25,
    label: "law firm",
  },
  veterinary: {
    avg_job_value: 200,
    avg_missed_calls_week: 6,
    avg_no_show_rate: 0.12,
    avg_admin_hours_week: 15,
    admin_hourly_cost: 18,
    avg_follow_up_conversion: 0.30,
    label: "veterinary clinic",
  },
  trucking: {
    avg_job_value: 1500,
    avg_missed_calls_week: 3,
    avg_no_show_rate: 0.05,
    avg_admin_hours_week: 20,
    admin_hourly_cost: 22,
    avg_follow_up_conversion: 0.20,
    label: "trucking company",
  },
};

// Monthly plan costs for ROI comparison
const PLAN_COSTS = { basic: 199, pro: 699, enterprise: 1299 };

function findIndustry(input) {
  if (!input) return null;
  const lower = input.toLowerCase();
  for (const [key, data] of Object.entries(INDUSTRY_DATA)) {
    if (lower.includes(key)) return { key, ...data };
  }
  // Fuzzy matches
  if (lower.includes("plumb")) return { key: "plumbing", ...INDUSTRY_DATA.plumbing };
  if (lower.includes("heat") || lower.includes("air condition") || lower.includes("cooling"))
    return { key: "hvac", ...INDUSTRY_DATA.hvac };
  if (lower.includes("electric")) return { key: "electrical", ...INDUSTRY_DATA.electrical };
  if (lower.includes("dent")) return { key: "dental", ...INDUSTRY_DATA.dental };
  if (lower.includes("doctor") || lower.includes("clinic") || lower.includes("medical"))
    return { key: "medical", ...INDUSTRY_DATA.medical };
  if (lower.includes("food") || lower.includes("bar") || lower.includes("cafe") || lower.includes("bistro"))
    return { key: "restaurant", ...INDUSTRY_DATA.restaurant };
  if (lower.includes("car") || lower.includes("mechanic") || lower.includes("auto"))
    return { key: "auto shop", ...INDUSTRY_DATA["auto shop"] };
  if (lower.includes("real") || lower.includes("realtor") || lower.includes("agent"))
    return { key: "real estate", ...INDUSTRY_DATA["real estate"] };
  if (lower.includes("build") || lower.includes("contract") || lower.includes("gc"))
    return { key: "construction", ...INDUSTRY_DATA.construction };
  if (lower.includes("property") || lower.includes("landlord") || lower.includes("rental"))
    return { key: "property management", ...INDUSTRY_DATA["property management"] };
  if (lower.includes("shop") || lower.includes("store") || lower.includes("boutique"))
    return { key: "retail", ...INDUSTRY_DATA.retail };
  if (lower.includes("tax") || lower.includes("cpa") || lower.includes("account") || lower.includes("bookkeep"))
    return { key: "accounting", ...INDUSTRY_DATA.accounting };
  if (lower.includes("hair") || lower.includes("barber") || lower.includes("spa") || lower.includes("nail"))
    return { key: "salon", ...INDUSTRY_DATA.salon };
  if (lower.includes("insur")) return { key: "insurance", ...INDUSTRY_DATA.insurance };
  if (lower.includes("law") || lower.includes("attorney") || lower.includes("legal"))
    return { key: "law", ...INDUSTRY_DATA.law };
  if (lower.includes("vet") || lower.includes("animal") || lower.includes("pet"))
    return { key: "veterinary", ...INDUSTRY_DATA.veterinary };
  if (lower.includes("truck") || lower.includes("freight") || lower.includes("haul") || lower.includes("logist"))
    return { key: "trucking", ...INDUSTRY_DATA.trucking };
  return null;
}

module.exports = {
  name: "calculate_roi",
  description:
    "Calculate the return on investment for a potential customer based on their industry and specific pain points. Shows them exactly how much money they're losing and how AI Advantage pays for itself. Use this when a visitor mentions missed calls, no-shows, admin time waste, or asks 'is it worth it?'",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The visitor's industry (e.g., 'plumbing', 'dental', 'restaurant')",
      },
      missed_calls_per_week: {
        type: "number",
        description: "How many calls they miss per week (if mentioned)",
      },
      avg_job_value: {
        type: "number",
        description: "Their average job/transaction value in dollars (if mentioned)",
      },
      employees: {
        type: "number",
        description: "Number of employees (if mentioned)",
      },
      current_pain: {
        type: "string",
        description: "What they said their biggest problem is (e.g., 'missed calls', 'no-shows', 'too much paperwork')",
      },
      plan_tier: {
        type: "string",
        enum: ["basic", "pro", "enterprise"],
        description: "Which plan tier to calculate against (default: pro)",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const industry = findIndustry(args.industry);
    if (!industry) {
      return JSON.stringify({
        calculated: false,
        message: "I don't have specific ROI benchmarks for that industry, but I can walk you through the math on a discovery call.",
      });
    }

    const planTier = args.plan_tier || "pro";
    const monthlyCost = PLAN_COSTS[planTier] || 699;

    // Use visitor's numbers if provided, otherwise use benchmarks
    const missedCalls = args.missed_calls_per_week || industry.avg_missed_calls_week;
    const jobValue = args.avg_job_value || industry.avg_job_value;
    const adminHours = industry.avg_admin_hours_week;
    const adminCost = industry.admin_hourly_cost;
    const noShowRate = industry.avg_no_show_rate;
    const followUpConversion = industry.avg_follow_up_conversion;

    // Calculate monthly losses
    const missedCallRevenue = missedCalls * jobValue * 4.33; // weeks per month
    const recoveredCallRevenue = Math.round(missedCallRevenue * 0.6); // 60% recovery rate with AI

    const adminTimeSaved = Math.round(adminHours * 0.4); // 40% admin time reduction
    const adminSavings = Math.round(adminTimeSaved * adminCost * 4.33);

    const noShowRevenue = noShowRate > 0
      ? Math.round(noShowRate * jobValue * missedCalls * 4.33 * 0.5) // 50% of no-shows recovered
      : 0;

    // Industry-specific bonuses
    let bonusRevenue = 0;
    let bonusLabel = "";
    if (industry.food_waste_pct && industry.avg_monthly_food_cost) {
      bonusRevenue = Math.round(industry.avg_monthly_food_cost * industry.food_waste_pct * 0.5);
      bonusLabel = "Food waste reduction (50% of current waste)";
    } else if (industry.inventory_waste_pct && industry.avg_monthly_inventory) {
      bonusRevenue = Math.round(industry.avg_monthly_inventory * industry.inventory_waste_pct * 0.4);
      bonusLabel = "Inventory waste reduction (40% of current waste)";
    } else if (industry.speed_to_lead_value) {
      bonusRevenue = Math.round(industry.speed_to_lead_value * 2); // 2 extra deals/month from speed
      bonusLabel = "Speed-to-lead advantage (2 extra deals/month)";
    }

    const totalMonthlyBenefit = recoveredCallRevenue + adminSavings + noShowRevenue + bonusRevenue;
    const netMonthlyROI = totalMonthlyBenefit - monthlyCost;
    const roiMultiple = totalMonthlyBenefit > 0 ? (totalMonthlyBenefit / monthlyCost).toFixed(1) : 0;
    const paybackDays = totalMonthlyBenefit > 0 ? Math.ceil(monthlyCost / (totalMonthlyBenefit / 30)) : 999;

    const result = {
      calculated: true,
      industry: industry.label,
      plan: planTier.charAt(0).toUpperCase() + planTier.slice(1),
      monthly_cost: `$${monthlyCost}`,

      // Revenue recovery breakdown
      missed_call_recovery: {
        missed_per_week: missedCalls,
        avg_job_value: `$${jobValue}`,
        monthly_lost_revenue: `$${Math.round(missedCallRevenue).toLocaleString()}`,
        recovered_with_ai: `$${recoveredCallRevenue.toLocaleString()}`,
        assumption: "60% recovery rate with AI phone answering",
      },

      admin_time_savings: {
        hours_saved_per_week: adminTimeSaved,
        monthly_savings: `$${adminSavings.toLocaleString()}`,
        assumption: "40% admin time reduction",
      },

      total_monthly_benefit: `$${totalMonthlyBenefit.toLocaleString()}`,
      monthly_cost_of_plan: `$${monthlyCost}`,
      net_monthly_roi: `$${netMonthlyROI.toLocaleString()}`,
      roi_multiple: `${roiMultiple}x`,
      payback_period: `${paybackDays} days`,

      bottom_line: netMonthlyROI > 0
        ? `AI Advantage pays for itself in ${paybackDays} days and nets you $${netMonthlyROI.toLocaleString()}/month after that. That's ${roiMultiple}x return on your subscription.`
        : `Based on these conservative estimates, the ROI is tight. Let's talk about your specific numbers on a discovery call — most businesses do better than the benchmarks.`,
    };

    if (noShowRevenue > 0) {
      result.no_show_recovery = {
        no_show_rate: `${Math.round(noShowRate * 100)}%`,
        monthly_recovered: `$${noShowRevenue.toLocaleString()}`,
        assumption: "50% of no-shows recovered with AI reminders",
      };
    }

    if (bonusRevenue > 0) {
      result.industry_bonus = {
        label: bonusLabel,
        monthly_value: `$${bonusRevenue.toLocaleString()}`,
      };
    }

    return JSON.stringify(result);
  },
};
