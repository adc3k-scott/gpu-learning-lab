// ROXY Tool: Live Demo Generator
// Creates a personalized "day in the life" walkthrough for the prospect's industry.
// Makes the product tangible in 60 seconds — kills "I can't picture this" objection.

const DEMO_SCENARIOS = {
  plumbing: {
    business: "plumbing company",
    scenarios: [
      {
        time: "7:15 AM",
        event: "Customer calls about a burst pipe — you're still drinking coffee",
        without_ai: "Phone goes to voicemail. Customer calls the next plumber on Google. You lost a $400 emergency job.",
        with_ai: "ROXY's AI answers instantly. Qualifies the emergency, gets the address, dispatches your nearest truck. You get a text: 'Emergency dispatch — 123 Main St, burst pipe, ETA 25 min.' Customer is already booked before you finish your coffee.",
      },
      {
        time: "10:30 AM",
        event: "Tech finishes a water heater install — needs to quote a re-pipe",
        without_ai: "Tech calls the office. Office is on another call. Tech sits in the driveway for 20 minutes waiting. Customer gets impatient.",
        with_ai: "Tech snaps photos of the pipes, sends to the AI. Gets a detailed estimate in 90 seconds. Shows the customer on the spot. Customer approves while the tech is still there. No waiting, no callback.",
      },
      {
        time: "6:45 PM",
        event: "Three after-hours calls come in — you're at dinner with your family",
        without_ai: "All three go to voicemail. By morning, two have called competitors. You'll never know.",
        with_ai: "AI answers all three. Qualifies: one emergency (dispatches on-call tech), one appointment (books for tomorrow 8 AM), one price inquiry (sends quote via text). You see a summary in the morning. Zero calls lost.",
      },
    ],
  },
  hvac: {
    business: "HVAC company",
    scenarios: [
      {
        time: "2:00 PM — July",
        event: "AC goes out at a restaurant during lunch rush — they're desperate",
        without_ai: "They call, you're on another job. Voicemail. They call the next guy. $800 emergency job gone.",
        with_ai: "AI answers, identifies it as a commercial emergency, checks your tech locations, dispatches the closest one with the right parts on the truck. Customer gets a text: 'Tech en route, ETA 35 minutes.' You didn't even have to pick up the phone.",
      },
      {
        time: "8:00 AM",
        event: "Monday morning — 14 voicemails from the weekend",
        without_ai: "Your office manager spends 2 hours returning calls. Half don't answer. Three already booked someone else.",
        with_ai: "AI handled all 14 over the weekend. 9 appointments already booked. 3 estimates sent. 2 were spam. Your Monday starts with a full schedule instead of a voicemail backlog.",
      },
    ],
  },
  dental: {
    business: "dental office",
    scenarios: [
      {
        time: "8:30 AM",
        event: "Patient calls to check if their insurance covers a crown",
        without_ai: "Front desk puts them on hold, logs into the insurance portal, navigates 6 screens, comes back 8 minutes later. Two other patients are waiting to check in.",
        with_ai: "AI verifies insurance eligibility in 12 seconds. Tells the patient their coverage, copay estimate, and asks if they'd like to schedule. Front desk never had to stop what they were doing.",
      },
      {
        time: "11:00 AM",
        event: "Dr. Chen finishes a complex procedure — needs to write clinical notes",
        without_ai: "Spends 15 minutes typing notes between patients. Running late the rest of the day.",
        with_ai: "Dictates notes in 2 minutes. AI drafts the full clinical note in proper format. Dr. Chen reviews, approves, moves to the next patient on time.",
      },
      {
        time: "3:00 PM",
        event: "Tomorrow's 2 PM cleaning just cancelled",
        without_ai: "Front desk starts calling patients from the waitlist. Gets 3 voicemails before someone picks up. Slot might stay empty.",
        with_ai: "AI instantly texts 5 patients on the waitlist: 'An appointment opened tomorrow at 2 PM — reply YES to book.' First reply comes in 4 minutes. Slot filled.",
      },
    ],
  },
  restaurant: {
    business: "restaurant",
    scenarios: [
      {
        time: "Tuesday 3:00 PM",
        event: "You're prepping for dinner service — phone won't stop ringing",
        without_ai: "You answer with flour on your hands. Take a reservation while burning the roux. Miss two other calls.",
        with_ai: "AI handles all reservation calls. Books tables, answers 'do you have outdoor seating?' and 'are you open Monday?', and texts you a summary. You focus on the food.",
      },
      {
        time: "Thursday 10:00 AM",
        event: "Crawfish delivery is short 40 pounds — Friday is your busiest night",
        without_ai: "You don't notice until Friday morning prep. Scramble to find crawfish. Pay premium. Menu items get 86'd anyway.",
        with_ai: "AI flagged the shortage at receiving. Auto-reorder triggered to your backup supplier Thursday at noon. Full stock for Friday. No panic.",
      },
    ],
  },
  "real estate": {
    business: "real estate agency",
    scenarios: [
      {
        time: "Saturday 9:00 PM",
        event: "Hot lead submits inquiry on your listing — they want to see it tomorrow",
        without_ai: "Email sits in your inbox until Monday morning. By then they've already toured with another agent.",
        with_ai: "AI responds in 11 seconds. Sends property details, comparable sales, and available showing times. Books a Sunday 10 AM showing. You wake up to a confirmed appointment.",
      },
      {
        time: "Monday 2:00 PM",
        event: "Seller wants a listing description for their new property",
        without_ai: "You spend 45 minutes writing copy, pulling comps, formatting the MLS entry.",
        with_ai: "AI generates the listing description from your notes and photos in 30 seconds. Professional copy with neighborhood highlights, recent sales data, and SEO-optimized keywords. You review, tweak one line, and post.",
      },
    ],
  },
  salon: {
    business: "salon",
    scenarios: [
      {
        time: "Wednesday",
        event: "3 no-shows today — that's $195 in empty chair time",
        without_ai: "You post on Instagram complaining about no-shows. Nothing changes next week.",
        with_ai: "AI sent confirmation texts 24 hours before AND 2 hours before each appointment. Two of the three confirmed or rescheduled. One no-showed — AI immediately texted the waitlist and filled the slot in 20 minutes. Net loss: $0.",
      },
    ],
  },
  "auto shop": {
    business: "auto shop",
    scenarios: [
      {
        time: "Customer drops off a car with hail damage",
        event: "You need to write a detailed estimate for insurance",
        without_ai: "Spend 40 minutes documenting every dent, looking up parts prices, typing the estimate. Customer waits.",
        with_ai: "Snap 6 photos of the damage. AI identifies each dent, matches body parts, pulls current prices, and generates a formatted insurance estimate in 3 minutes. Customer gets it texted to approve before they leave the lot.",
      },
    ],
  },
  law: {
    business: "law firm",
    scenarios: [
      {
        time: "New client drops off a box of 200 documents for their case",
        event: "Your paralegal needs to review, categorize, and find the 5 that matter",
        without_ai: "3 days of manual review. Paralegal bills 24 hours at $75/hr = $1,800 in labor. Might miss something.",
        with_ai: "AI scans all 200 documents overnight. By morning: categorized by type, indexed by date and party, flagged the 5 critical ones with relevant passages highlighted. Paralegal reviews the AI's work in 2 hours instead of 3 days. Attorney-client privilege stays on-device — nothing leaves the building.",
      },
    ],
  },
};

function findDemo(industry) {
  if (!industry) return null;
  const lower = industry.toLowerCase();
  for (const [key, data] of Object.entries(DEMO_SCENARIOS)) {
    if (lower.includes(key)) return data;
  }
  if (lower.match(/plumb/)) return DEMO_SCENARIOS.plumbing;
  if (lower.match(/hvac|cool|heat|air con/)) return DEMO_SCENARIOS.hvac;
  if (lower.match(/dent|medical|doctor/)) return DEMO_SCENARIOS.dental;
  if (lower.match(/restaurant|bar|food|cafe/)) return DEMO_SCENARIOS.restaurant;
  if (lower.match(/real estate|realtor/)) return DEMO_SCENARIOS["real estate"];
  if (lower.match(/salon|barber|spa|hair/)) return DEMO_SCENARIOS.salon;
  if (lower.match(/auto|mechanic/)) return DEMO_SCENARIOS["auto shop"];
  if (lower.match(/law|attorney|legal/)) return DEMO_SCENARIOS.law;
  return null;
}

module.exports = {
  name: "generate_live_demo",
  description:
    "Generate a personalized 'day in the life' demo showing exactly how AI Advantage works for the prospect's specific business. Use this when someone says 'show me how it works', 'what does it actually do?', 'I can't picture this', or any time the prospect needs to SEE it working for their industry. The demo uses real scenarios with before/after comparisons.",
  parameters: {
    type: "object",
    properties: {
      industry: {
        type: "string",
        description: "The prospect's industry",
      },
      business_name: {
        type: "string",
        description: "Their business name if known",
      },
      employees: {
        type: "number",
        description: "Number of employees if known",
      },
      specific_pain: {
        type: "string",
        description: "Their specific pain point if mentioned",
      },
    },
    required: ["industry"],
  },
  async execute(args) {
    const demo = findDemo(args.industry);

    if (!demo) {
      return JSON.stringify({
        available: false,
        message: `I don't have a pre-built demo for ${args.industry} yet, but I can walk you through exactly how it would work on a 15-minute discovery call. Want to book one?`,
      });
    }

    const businessLabel = args.business_name || `your ${demo.business}`;

    return JSON.stringify({
      available: true,
      title: `A Day at ${businessLabel} — With AI Advantage`,
      scenarios: demo.scenarios,
      closing: `This is what it looks like when ${businessLabel} has an AI agent working 24/7. Every scenario above is a real use case from our ${demo.business} playbook. Want to see it running for your business? Let's book a 15-minute call.`,
    });
  },
};
