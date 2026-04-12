// ROXY SaaS Tool: Social Media Post Generator
// Creates a week of social media content in 60 seconds.
// What social media managers charge $1-3K/mo for.

const POST_TYPES = {
  tip: { label: "Expert Tip", emoji: "💡", engagement: "high" },
  behind_scenes: { label: "Behind the Scenes", emoji: "🎬", engagement: "very high" },
  testimonial: { label: "Customer Win", emoji: "⭐", engagement: "high" },
  seasonal: { label: "Seasonal", emoji: "📅", engagement: "medium" },
  humor: { label: "Industry Humor", emoji: "😂", engagement: "very high" },
  before_after: { label: "Before & After", emoji: "📸", engagement: "highest" },
  question: { label: "Engagement Question", emoji: "❓", engagement: "high" },
};

const INDUSTRY_CONTENT = {
  plumbing: {
    tips: [
      "Your water heater's life expectancy is 8-12 years. If yours is older, it's not a matter of IF it fails — it's WHEN. Pro move: schedule a flush before it becomes an emergency.",
      "That slow drain isn't going away on its own. Every week you wait, the clog gets worse (and more expensive). A $150 cleaning now saves a $800 snake job later.",
      "Know where your main water shutoff is BEFORE the pipe bursts. Test it once a year. If it's stuck, call us now — not at 2 AM when water's pouring into your living room.",
    ],
    humor: [
      "Customer: 'I tried to fix it myself with YouTube.' Us: *sees the aftermath* 'We see this a lot.' 😅 Some things are worth calling a pro for.",
      "Weekend plans: ❌ Relax | ✅ Emergency call at 6 AM because someone flushed something they shouldn't have. Happy Saturday! 🔧",
    ],
    questions: [
      "What's the worst plumbing surprise you've ever come home to? 💧 Drop your horror stories below — we've probably seen worse. 😂",
      "Hot take: Is it worth paying more for a plumber who shows up on time, or just go with whoever's cheapest? Debate below. 👇",
    ],
    behind_scenes: [
      "7 AM truck check ✅ Every morning our techs inspect their gear, restock parts, and review the day's jobs. This is how we show up prepared — not scrambling. 🔧",
    ],
    before_after: [
      "BEFORE: Homeowner tried to patch a leaking pipe with duct tape and a prayer. AFTER: New copper fitting, bone dry, done in 45 minutes. Sometimes the right tool matters more than effort. 📸",
    ],
  },
  dental: {
    tips: [
      "Flossing isn't optional — it's where 40% of tooth surfaces are. Brushing without flossing is like washing only half your car. Your dentist knows.",
      "That tooth sensitivity to cold drinks? It's not normal. It could be a cracked tooth, a cavity, or worn enamel. Don't wait for it to become a root canal.",
      "Electric toothbrush vs manual: Electric wins. Period. 2 minutes, 3x more plaque removal. It's the best $50 you'll spend on your health this year.",
    ],
    humor: [
      "Patient: 'I floss every day.' Us: 'Your gums say otherwise.' 😅 It's okay — no judgment. Let's just start from today.",
      "When the patient says they only came in because their spouse made them 😂 Hey, whatever gets you in the chair. We're glad you're here!",
    ],
    questions: [
      "Be honest: when was your last dental cleaning? 🦷 No judgment. Drop a ✅ if you're overdue and we'll help you fix that.",
    ],
  },
  restaurant: {
    tips: [
      "The secret to great restaurant food isn't talent — it's consistency. Same recipe, same portions, same quality every single time. That's what brings people back.",
      "If your food cost is over 30%, you're leaving money on the table. Track every ingredient, every waste bin, every portion. The math matters.",
    ],
    humor: [
      "'Can I get this completely customized with 15 modifications?' Sure! That'll be ready in... *checks notes* ...about 45 minutes. 😂",
      "The Yelp reviewer who orders the one thing we're famous for, asks to modify everything about it, then gives 3 stars because 'it wasn't what I expected.' 🙃",
    ],
    questions: [
      "What's your go-to comfort food when you've had a rough day? Tell us below — our chef might make it a special this week. 👨‍🍳",
    ],
    behind_scenes: [
      "5:30 AM. Farmer's market run before the sun is up. This is where tonight's specials start — fresh, local, and hand-picked by our chef. 🌿",
    ],
  },
  hvac: {
    tips: [
      "Change your air filter every 30-90 days. A dirty filter makes your AC work harder, drives up your bill, and shortens the system's life. It's a $10 fix that saves thousands.",
      "Set your thermostat to 78°F in summer. Every degree lower costs you 3-5% more on your bill. A ceiling fan makes 78 feel like 72.",
    ],
    humor: [
      "Louisiana in July: 'Is your AC broken?' Us: 'No, it's 108° outside and 97% humidity. Your AC is a hero right now.' 😅🔥",
    ],
    questions: [
      "What temperature do you set your thermostat to? Be honest — we won't judge. (We've seen 62°F and lived to tell the tale.) ❄️",
    ],
  },
  salon: {
    tips: [
      "Stop washing your hair every day. Seriously. 2-3 times a week is ideal for most hair types. Your natural oils are doing important work.",
      "Your stylist isn't just cutting hair — they're reading your face shape, bone structure, and lifestyle to find the cut that makes YOU look amazing. That's worth showing up for.",
    ],
    humor: [
      "'Just a little trim.' *shows photo of completely different hairstyle* 😂 We love a challenge. Bring us your Pinterest boards — we'll make it happen.",
    ],
    questions: [
      "What's the worst haircut you've ever gotten? 💇 Share your horror story — we promise we won't repeat it. 😅",
    ],
    before_after: [
      "BEFORE: 6 months of quarantine hair. AFTER: Color, cut, and confidence restored in 2 hours. This is why we do what we do. ✂️✨",
    ],
  },
};

function getContentForIndustry(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, data] of Object.entries(INDUSTRY_CONTENT)) {
    if (lower.includes(key)) return { key, ...data };
  }
  if (lower.match(/plumb/)) return { key: "plumbing", ...INDUSTRY_CONTENT.plumbing };
  if (lower.match(/hvac|cool|heat/)) return { key: "hvac", ...INDUSTRY_CONTENT.hvac };
  if (lower.match(/dent/)) return { key: "dental", ...INDUSTRY_CONTENT.dental };
  if (lower.match(/restaurant|bar|food/)) return { key: "restaurant", ...INDUSTRY_CONTENT.restaurant };
  if (lower.match(/salon|barber|hair/)) return { key: "salon", ...INDUSTRY_CONTENT.salon };
  return null;
}

module.exports = {
  name: "generate_social_posts",
  description:
    "Generate a week of social media posts tailored to the business's industry. Creates a mix of tips, humor, behind-the-scenes, customer wins, and engagement questions. Use when a customer asks about social media, marketing, or says they don't know what to post.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The business industry",
      },
      business_name: {
        type: "string",
        description: "The business name for personalization",
      },
      num_posts: {
        type: "number",
        description: "Number of posts to generate (default: 7 for one week)",
      },
      platform: {
        type: "string",
        enum: ["facebook", "instagram", "both"],
        description: "Target platform (default: both)",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const content = getContentForIndustry(args.industry);
    const numPosts = args.num_posts || 7;
    const bizName = args.business_name || "your business";

    if (!content) {
      return JSON.stringify({
        generated: false,
        message: `I can create custom social content for ${args.industry} — let's discuss your brand voice on a discovery call.`,
      });
    }

    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const schedule = [];

    // Build a balanced week
    const postPlan = [
      { type: "tip", source: "tips" },
      { type: "behind_scenes", source: "behind_scenes" },
      { type: "humor", source: "humor" },
      { type: "question", source: "questions" },
      { type: "tip", source: "tips" },
      { type: "before_after", source: "before_after" },
      { type: "humor", source: "humor" },
    ];

    for (let i = 0; i < Math.min(numPosts, 7); i++) {
      const plan = postPlan[i % postPlan.length];
      const typeInfo = POST_TYPES[plan.type] || POST_TYPES.tip;
      const pool = content[plan.source] || content.tips || [];
      const postContent = pool[i % pool.length] || content.tips[0];

      schedule.push({
        day: days[i],
        type: typeInfo.label,
        emoji: typeInfo.emoji,
        expected_engagement: typeInfo.engagement,
        content: postContent,
        best_time: i < 5 ? "11:30 AM - 1:00 PM (lunch scroll)" : "9:00 AM - 11:00 AM (weekend morning)",
        hashtags: `#${content.key.replace(/\s/g, "")} #${(args.business_name || content.key).replace(/\s/g, "")} #smallbusiness #lafayette #louisiana`,
      });
    }

    return JSON.stringify({
      generated: true,
      business: bizName,
      industry: content.key,
      week_schedule: schedule,
      strategy_tips: [
        "Post consistently — same times, same days. The algorithm rewards reliability.",
        "Before/After photos get 3-5x more engagement than text posts. Use them.",
        "Respond to EVERY comment within 1 hour. The algorithm boosts posts with active comment sections.",
        "Humor posts get shared. Shares = free reach. Don't be afraid to be funny.",
        `Use your location tag on every post — people search '${content.key} near me' on Instagram.`,
      ],
      next_step: "Want me to create next week's content too? Or focus on a specific platform?",
    });
  },
};
