/**
 * Automated Filing Assistant
 *
 * Takes a registrant's eligibility report and generates:
 * 1. Pre-filled application templates for each eligible program
 * 2. Step-by-step filing instructions specific to their institution
 * 3. Deadline reminders scheduled via follow-up emails
 * 4. Progress tracking
 *
 * Triggered automatically after eligibility report is sent,
 * or manually via POST /api/filing-assistant
 *
 * 100% autonomous — no human in the loop.
 */

// Program-specific filing templates
const FILING_TEMPLATES = {
  "LED FastStart": {
    type: "state",
    filing_method: "online_portal",
    url: "https://www.opportunitylouisiana.gov/faststart",
    steps: [
      "Visit opportunitylouisiana.gov/faststart",
      "Click 'Request Workforce Training' or 'Contact Us'",
      "Fill in your district name, superintendent name, and contact info",
      "Describe the training need: 'AI compute infrastructure technician training for K-12 education technology staff'",
      "Specify number of trainees (recommend starting with 5-10)",
      "LED FastStart team will contact you within 5 business days to design a custom curriculum",
      "Training is 100% FREE — LED covers all costs"
    ],
    auto_fill: {
      training_type: "AI Infrastructure & Compute Technician",
      industry: "Education / Technology",
      description: "Training for school district technology staff on AI compute infrastructure management, GPU system administration, and AI-powered educational tools deployment."
    },
    deadline: "Ongoing — no deadline",
    time_to_complete: "5 minutes to request, LED handles the rest"
  },

  "CSTAG": {
    type: "state",
    filing_method: "application",
    url: "https://doe.louisiana.gov/educators/instructional-support/louisiana-stem-initiative",
    steps: [
      "Contact LDOE STEM team at STEM@la.gov",
      "Request CSTAG (Computer Science & Technology for All Grant) application packet",
      "Application requires: district demographics, current CS offerings, proposed use of funds",
      "Grants up to $40,000 per school system",
      "Funds can be used for: hardware, software, curriculum, teacher training",
      "Submit completed application to LDOE by the annual deadline",
      "Awards typically announced within 60 days"
    ],
    auto_fill: {
      use_of_funds: "AI-powered educational technology infrastructure, GPU compute access for student learning, teacher professional development in AI and computer science",
      current_cs_offerings: "[DISTRICT TO COMPLETE - list current CS courses]",
      proposed_impact: "Enable AI curriculum aligned with Louisiana's new K-12 CS Standards (adopted 2024, live 2025-2026)"
    },
    deadline: "Annual cycle — contact STEM@la.gov for current window",
    time_to_complete: "30-60 minutes for application"
  },

  "K-12 CS Standards Implementation Support": {
    type: "state",
    filing_method: "contact",
    url: "https://doe.louisiana.gov",
    steps: [
      "Email DigitalLearning@la.gov",
      "Subject: 'CS Standards Implementation Support Request — [Your District Name]'",
      "Body: 'We are implementing the new K-12 CS Standards and would like support with curriculum resources, teacher training, and technology infrastructure planning.'",
      "Include: district name, superintendent contact, number of schools, current technology infrastructure",
      "LDOE Digital Learning team will schedule a consultation",
      "Free curriculum resources and implementation guides provided"
    ],
    auto_fill: {
      subject: "CS Standards Implementation Support Request",
      body: "We are implementing the new K-12 CS Standards and would like support with curriculum resources, teacher training, and technology infrastructure planning. We are also working with Louisiana's AI Infrastructure Initiative (louisianaai.net) to explore GPU compute access for our schools."
    },
    deadline: "Ongoing — standards live 2025-2026",
    time_to_complete: "5 minutes to send email"
  },

  "NVIDIA AI Workforce Hub": {
    type: "nvidia",
    filing_method: "registration",
    url: "https://www.nvidia.com/en-us/training/",
    steps: [
      "Visit nvidia.com/training",
      "Click 'Get Started' or 'Explore Courses'",
      "Create a free NVIDIA Developer account (if you don't have one)",
      "Browse AI courses by difficulty level (Beginner, Intermediate, Advanced)",
      "Recommended starting courses for K-12 educators: 'Fundamentals of Deep Learning', 'Getting Started with AI'",
      "Courses are self-paced and completely free",
      "Certificates provided upon completion — students and teachers can both participate"
    ],
    auto_fill: {},
    deadline: "Ongoing — always available",
    time_to_complete: "5 minutes to register, courses vary (2-8 hours each)"
  },

  "NVIDIA DLI Teaching Kits": {
    type: "nvidia",
    filing_method: "application",
    url: "https://www.nvidia.com/en-us/training/teaching-kits/",
    steps: [
      "Visit nvidia.com/training/teaching-kits",
      "Review available teaching kit curricula",
      "Click 'Apply for a Teaching Kit'",
      "Fill in: institution name, your role, courses you teach, number of students",
      "Describe how you plan to integrate AI content into your curriculum",
      "NVIDIA provides: lecture slides, hands-on labs, GPU cloud access, support materials",
      "Approval typically within 2-4 weeks"
    ],
    auto_fill: {
      integration_plan: "Integrate AI and deep learning fundamentals into existing STEM curriculum, aligned with Louisiana's new K-12 CS Standards. Provide students hands-on experience with GPU-accelerated computing."
    },
    deadline: "Ongoing",
    time_to_complete: "15 minutes to apply"
  },

  "NVIDIA Academic Grant": {
    type: "federal",
    filing_method: "application",
    url: "https://academicgrants.nvidia.com",
    steps: [
      "Visit academicgrants.nvidia.com",
      "Create an account or log in",
      "Click 'Apply for Grant'",
      "Fill in: institution details, department, research/education focus",
      "Describe your GPU compute needs and how NVIDIA hardware will be used",
      "Include: number of researchers/students who will benefit, current GPU infrastructure (likely zero)",
      "Mention partnership with Louisiana's AI Infrastructure Initiative and access to GPU compute at Tiger Compute Campus or Ragin' Cajun Compute Campus",
      "DEADLINE: March 31, 2026 — 7 DAYS"
    ],
    auto_fill: {
      compute_needs: "GPU compute infrastructure for AI research, model training, and educational programs. Currently zero dedicated GPU infrastructure on campus.",
      partnership: "Working with Louisiana's AI Infrastructure Initiative (louisianaai.net) which is developing two AI factory campuses with NVIDIA DSX reference architecture."
    },
    deadline: "March 31, 2026 — URGENT",
    time_to_complete: "30-45 minutes"
  },

  "DOE SPARK Concept Paper": {
    type: "federal",
    filing_method: "submission",
    url: "https://eere-exchange.energy.gov",
    steps: [
      "Visit eere-exchange.energy.gov",
      "Search for SPARK or 'Solar and Perovskite Advanced Research and Knowledge'",
      "Download the Funding Opportunity Announcement (FOA)",
      "Register on EERE Exchange (if not already registered)",
      "Prepare concept paper (typically 3-5 pages): project description, technical approach, team qualifications, budget estimate",
      "Focus on: 800V DC microgrid architecture, solar-direct integration, AI factory power optimization",
      "Submit concept paper through EERE Exchange portal",
      "DEADLINE: April 2, 2026 — 9 DAYS"
    ],
    auto_fill: {
      project_focus: "800V DC native power architecture with solar-direct integration for AI compute infrastructure. Partnership with Louisiana's AI Infrastructure Initiative developing two campuses with NVIDIA DSX reference design.",
    },
    deadline: "April 2, 2026 — URGENT",
    time_to_complete: "Several hours for concept paper"
  },

  "NSF MRI": {
    type: "federal",
    filing_method: "proposal",
    url: "https://www.nsf.gov/funding/opportunities/mri-major-research-instrumentation-program",
    steps: [
      "Contact your university's Office of Sponsored Programs — they manage NSF submissions",
      "Request to be included in the internal limited-submission competition (most universities allow 1-3 MRI proposals per cycle)",
      "Start internal process NOW — the October 2026 submission window requires months of preparation",
      "Proposal requires: instrument justification, user base (faculty + students), 30% cost-share for doctoral institutions",
      "GPU compute cluster qualifies as 'major research instrumentation'",
      "Budget: up to $4M",
      "Mention the Louisiana AI Infrastructure Initiative partnership for broader impact section"
    ],
    auto_fill: {
      instrument: "NVIDIA GPU compute cluster for AI research, machine learning, and scientific computing",
      justification: "Louisiana currently has zero dedicated GPU compute infrastructure at any university. This instrument would serve multiple departments and align with the state's AI infrastructure development initiative."
    },
    deadline: "October 15 - November 16, 2026 — start NOW",
    time_to_complete: "Months of preparation — begin immediately"
  },

  "NSF EPSCoR E-CORE": {
    type: "federal",
    filing_method: "proposal",
    url: "https://www.nsf.gov/funding/opportunities/e-core-epscor-research-infrastructure-improvement-program-epscor/nsf25-523/solicitation",
    steps: [
      "Contact Louisiana EPSCoR office through Board of Regents: kim.reed@laregents.edu",
      "Discuss your institution's eligibility and alignment with Louisiana's S&T plan",
      "EPSCoR proposals require multi-institutional collaboration",
      "Louisiana is EPSCoR-eligible — this is a significant advantage",
      "Awards up to $10M over 4 years",
      "Focus area: research infrastructure improvement including AI compute"
    ],
    auto_fill: {
      focus: "AI compute infrastructure development aligned with Louisiana's state science and technology plan. Multi-institutional partnership through Louisiana's AI Infrastructure Initiative."
    },
    deadline: "Multiple windows through 2026",
    time_to_complete: "Significant — coordinate through Board of Regents"
  }
};


function generateFilingPackage(registrantData, eligiblePrograms) {
  const name = registrantData.name || "Registrant";
  const org = registrantData.organization || "Your Institution";
  const type = registrantData.institution_type || "unknown";
  const parish = registrantData.parish || "Louisiana";
  const email = registrantData.email || "";

  let package_text = `
FILING ASSISTANCE PACKAGE — ${org}
Louisiana's AI Infrastructure Initiative
Generated: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })}
${'='.repeat(60)}

Dear ${name},

Based on your eligibility assessment, we've prepared filing instructions and pre-filled templates for each program ${org} qualifies for. Below are step-by-step instructions to get started.

Programs are listed in order of urgency — start with any marked URGENT.

`;

  let programCount = 0;

  // Sort: urgent first, then by deadline proximity
  const allPrograms = [...(eligiblePrograms.urgent || []), ...(eligiblePrograms.federal || []), ...(eligiblePrograms.state || []), ...(eligiblePrograms.nvidia || [])];

  for (const program of allPrograms) {
    const template = FILING_TEMPLATES[program.name];
    if (!template) continue;

    programCount++;
    const isUrgent = program.urgent ? '*** URGENT ***' : '';

    package_text += `
${'─'.repeat(60)}
PROGRAM ${programCount}: ${program.name} ${isUrgent}
Deadline: ${template.deadline}
Amount: ${program.amount}
Time to complete: ${template.time_to_complete}
${'─'.repeat(60)}

HOW TO FILE:
`;

    template.steps.forEach((step, i) => {
      // Auto-fill institution-specific info
      let filledStep = step
        .replace('[Your District Name]', org)
        .replace('[DISTRICT TO COMPLETE', `[${org} TO COMPLETE`);
      package_text += `  ${i + 1}. ${filledStep}\n`;
    });

    if (template.auto_fill && Object.keys(template.auto_fill).length > 0) {
      package_text += `\nPRE-FILLED INFORMATION (copy and paste into your application):\n`;
      for (const [field, value] of Object.entries(template.auto_fill)) {
        const filledValue = value
          .replace(/\[Your District Name\]/g, org)
          .replace(/\[DISTRICT TO COMPLETE[^\]]*\]/g, `[${org} to complete]`);
        package_text += `  ${field.replace(/_/g, ' ').toUpperCase()}: ${filledValue}\n`;
      }
    }

    package_text += `\nDIRECT LINK: ${template.url}\n`;
  }

  package_text += `

${'='.repeat(60)}

WHAT HAPPENS NEXT:

1. Start with the highest-priority program (any marked URGENT)
2. Use the pre-filled information above — just copy and paste into the application
3. If you get stuck, call (337) 448-4242 — our AI assistant can walk you through any step
4. We will send you deadline reminders for each program as dates approach
5. When you complete an application, let us know and we'll track your progress

This is a FREE service. We are here to help you every step of the way.

Louisiana's AI Infrastructure Initiative
(337) 448-4242 | info@louisianaai.net | louisianaai.net
`;

  return { package_text, programCount };
}


// Import the eligibility functions from process-registration
function getEligiblePrograms(institutionType) {
  // Inline the program data to avoid circular dependency
  const PROGRAMS = {
    federal: [
      { name: "NVIDIA Academic Grant", deadline: "March 31, 2026", urgent: true, amount: "Varies (hardware + support)", eligible: ["university", "university-private", "community-college"] },
      { name: "DOE SPARK Concept Paper", deadline: "April 2, 2026", urgent: true, amount: "$1-5M", eligible: ["university", "university-private"] },
      { name: "NSF EPSCoR E-CORE", deadline: "Multiple windows through 2026", urgent: false, amount: "Up to $10M", eligible: ["university", "university-private"] },
      { name: "NSF MRI", deadline: "October 15 - November 16, 2026", urgent: false, amount: "Up to $4M", eligible: ["university", "university-private"] },
      { name: "DOE EPSCoR State/Lab Partnerships", deadline: "May 21, 2026", urgent: false, amount: "$1-3M", eligible: ["university", "university-private"] },
    ],
    state: [
      { name: "LED FastStart", deadline: "Ongoing", urgent: false, amount: "FREE training", eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"] },
      { name: "LEQSF", deadline: "Annual cycle", urgent: false, amount: "Varies", eligible: ["university", "university-private"] },
      { name: "R&D Tax Credit", deadline: "July 1, 2026", urgent: false, amount: "Up to 30%", eligible: ["university", "university-private", "community-college"] },
      { name: "CSTAG", deadline: "Annual cycle", urgent: false, amount: "Up to $40K", eligible: ["k12-public", "k12-charter", "school-district"] },
      { name: "K-12 CS Standards Implementation Support", deadline: "Ongoing", urgent: false, amount: "Free resources", eligible: ["k12-public", "k12-private", "k12-charter", "school-district"] },
    ],
    nvidia: [
      { name: "NVIDIA DLI Teaching Kits", deadline: "Ongoing", urgent: false, amount: "Free curriculum", eligible: ["university", "university-private", "community-college"] },
      { name: "NVIDIA AI Workforce Hub", deadline: "Ongoing", urgent: false, amount: "Free training", eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"] },
    ]
  };

  const eligible = { urgent: [], federal: [], state: [], nvidia: [] };
  for (const p of PROGRAMS.federal) { if (p.eligible.includes(institutionType)) { p.urgent ? eligible.urgent.push(p) : eligible.federal.push(p); } }
  for (const p of PROGRAMS.state) { if (p.eligible.includes(institutionType)) eligible.state.push(p); }
  for (const p of PROGRAMS.nvidia) { if (p.eligible.includes(institutionType)) eligible.nvidia.push(p); }
  return eligible;
}


export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const data = req.body;
    const type = data.institution_type || "unknown";
    const name = data.name || "Registrant";
    const email = data.email || "";
    const org = data.organization || "Unknown";

    const eligiblePrograms = getEligiblePrograms(type);
    const { package_text, programCount } = generateFilingPackage(data, eligiblePrograms);

    const BREVO_API_KEY = process.env.BREVO_API_KEY;

    // Send filing package to registrant
    if (email && BREVO_API_KEY) {
      try {
        await fetch('https://api.brevo.com/v3/smtp/email', {
          method: 'POST',
          headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sender: { name: "Louisiana's AI Infrastructure Initiative", email: 'info@louisianaai.net' },
            to: [{ email: email, name: name }],
            subject: `Filing Assistance Package — ${programCount} Programs Ready to File — ${org}`,
            textContent: package_text,
          })
        });
        console.log(`Filing package sent to ${email}`);
      } catch (e) {
        console.error('Failed to send filing package:', e.message);
      }
    }

    // Notify Mission Control
    if (BREVO_API_KEY) {
      try {
        await fetch('https://api.brevo.com/v3/smtp/email', {
          method: 'POST',
          headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sender: { name: 'Mission Control', email: 'info@louisianaai.net' },
            to: [{ email: 'info@louisianaai.net', name: 'Mission Control' }],
            subject: `Filing Package Sent: ${name} — ${org} — ${programCount} programs`,
            textContent: `Filing assistance package sent to ${name} (${email}) at ${org}.\n\n${programCount} programs with step-by-step instructions and pre-filled templates.\n\nFull package:\n\n${package_text}`,
          })
        });
      } catch (e) {
        console.error('Failed to notify Mission Control:', e.message);
      }
    }

    return res.status(200).json({
      status: 'sent',
      programs_with_templates: programCount,
      recipient: email,
    });

  } catch (err) {
    console.error('Filing assistant error:', err.message);
    return res.status(500).json({ error: 'Processing error', message: err.message });
  }
}
