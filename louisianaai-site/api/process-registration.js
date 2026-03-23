/**
 * Automated Registration Processor
 *
 * Receives form data, matches institution type to eligible programs,
 * generates eligibility report, sends it to the registrant AND to
 * info@louisianaai.net. Fully autonomous — no human in the loop.
 */

// Program eligibility matrix
const PROGRAMS = {
  federal: [
    {
      name: "NVIDIA Academic Grant",
      deadline: "March 31, 2026",
      urgent: true,
      amount: "Varies (hardware + support)",
      eligible: ["university", "university-private", "community-college"],
      description: "NVIDIA provides GPU hardware, software licenses, and technical support for AI research and education programs.",
      action: "Apply at academicgrants.nvidia.com — DEADLINE IN DAYS",
      url: "https://academicgrants.nvidia.com"
    },
    {
      name: "DOE SPARK Concept Paper",
      deadline: "April 2, 2026",
      urgent: true,
      amount: "$1-5M",
      eligible: ["university", "university-private"],
      description: "Department of Energy funding for innovative energy infrastructure including 800V DC microgrids and solar-direct architecture.",
      action: "Submit concept paper at EERE Exchange",
      url: "https://eere-exchange.energy.gov"
    },
    {
      name: "NSF EPSCoR E-CORE",
      deadline: "Multiple windows through 2026",
      urgent: false,
      amount: "Up to $10M (4-year award)",
      eligible: ["university", "university-private"],
      description: "Louisiana is EPSCoR-eligible. Multi-institutional research infrastructure improvement. Must align with state S&T plan.",
      action: "Contact Louisiana EPSCoR office through Board of Regents (kim.reed@laregents.edu)",
      url: "https://www.nsf.gov/funding/opportunities/e-core-epscor-research-infrastructure-improvement-program-epscor/nsf25-523/solicitation"
    },
    {
      name: "NSF MRI (Major Research Instrumentation)",
      deadline: "October 15 - November 16, 2026",
      urgent: false,
      amount: "Up to $4M",
      eligible: ["university", "university-private"],
      description: "GPU compute clusters qualify. 30% cost-share required for doctoral institutions. Internal limited-submission competition required.",
      action: "Start internal university process NOW for October 2026 window",
      url: "https://www.nsf.gov/funding/opportunities/mri-major-research-instrumentation-program"
    },
    {
      name: "DOE EPSCoR State/Lab Partnerships",
      deadline: "May 21, 2026 (full application)",
      urgent: false,
      amount: "$1-3M",
      eligible: ["university", "university-private"],
      description: "Building partnerships between Louisiana universities and national laboratories for energy research.",
      action: "File through EERE Exchange",
      url: "https://eere-exchange.energy.gov"
    },
    {
      name: "NSF EPSCoR Graduate Fellowship (EGFP)",
      deadline: "June 1, 2026",
      urgent: false,
      amount: "$37K/year stipend + $16K education per Fellow, 3 years",
      eligible: ["university", "university-private"],
      description: "Graduate fellowships for AI/compute research. Minimum 3 Fellows per institution.",
      action: "File through Research.gov",
      url: "https://www.research.gov"
    },
    {
      name: "CHIPS Act — Domestic AI Infrastructure",
      deadline: "Ongoing",
      urgent: false,
      amount: "Part of $50B program",
      eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"],
      description: "100% US hardware supply chain positions Louisiana institutions for FEOC-clean federal procurement and EDA Tech Hub designation.",
      action: "Ensure all equipment purchases are US-manufactured",
      url: "https://www.nist.gov/chips"
    },
    {
      name: "BEAD Broadband ($1.355B to Louisiana)",
      deadline: "Ongoing — first state approved Nov 2025",
      urgent: false,
      amount: "Part of $1.355B Louisiana allocation",
      eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"],
      description: "8th largest broadband allocation nationally. Schools as anchor institutions for fiber buildout.",
      action: "Contact ConnectLA at broadband.la.gov",
      url: "https://broadband.la.gov"
    }
  ],
  state: [
    {
      name: "LED FastStart — FREE Workforce Training",
      deadline: "Ongoing — apply anytime",
      urgent: false,
      amount: "100% FREE (state-funded)",
      eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"],
      description: "#1 ranked workforce program 13 years running. Custom-designed AI compute technician training. Zero cost to your institution.",
      action: "Contact LED FastStart at opportunitylouisiana.gov/faststart",
      url: "https://www.opportunitylouisiana.gov/faststart"
    },
    {
      name: "LEQSF (Louisiana Education Quality Support Fund)",
      deadline: "Annual cycle",
      urgent: false,
      amount: "Varies by program",
      eligible: ["university", "university-private"],
      description: "State research funding administered through Board of Regents. Multiple subprograms for research infrastructure.",
      action: "Contact Board of Regents (kim.reed@laregents.edu)",
      url: "https://regents.la.gov/divisions/research-and-sponsored-programs/"
    },
    {
      name: "R&D Tax Credit (State)",
      deadline: "Next allocation July 1, 2026",
      urgent: false,
      amount: "Up to 30% of R&D spending",
      eligible: ["university", "university-private", "community-college"],
      description: "30% credit for institutions with <50 employees. Also 30% on SBIR/STTR grants. $12M annual cap.",
      action: "Apply through LED",
      url: "https://www.opportunitylouisiana.gov/business-incentives/research-and-development-tax-credit"
    },
    {
      name: "CSTAG (Computer Science & Technology for All Grant)",
      deadline: "Annual cycle",
      urgent: false,
      amount: "Up to $40K per school system",
      eligible: ["k12-public", "k12-charter", "school-district"],
      description: "Louisiana BESE-administered grants for K-12 computer science education infrastructure and curriculum.",
      action: "Contact LDOE STEM team at STEM@la.gov",
      url: "https://doe.louisiana.gov/educators/instructional-support/louisiana-stem-initiative"
    },
    {
      name: "K-12 CS Standards Implementation Support",
      deadline: "Ongoing — standards live 2025-2026",
      urgent: false,
      amount: "Training + curriculum resources (free)",
      eligible: ["k12-public", "k12-private", "k12-charter", "school-district"],
      description: "Louisiana adopted first-ever K-12 CS Standards in 2024, live 2025-2026. Support available for implementation.",
      action: "Contact LDOE at DigitalLearning@la.gov",
      url: "https://doe.louisiana.gov"
    }
  ],
  nvidia: [
    {
      name: "NVIDIA DLI Teaching Kits",
      deadline: "Ongoing",
      urgent: false,
      amount: "Free curriculum + resources",
      eligible: ["university", "university-private", "community-college"],
      description: "Free deep learning and AI curriculum materials for university courses. Includes lecture slides, labs, and GPU cloud access.",
      action: "Apply at nvidia.com/dli",
      url: "https://www.nvidia.com/en-us/training/teaching-kits/"
    },
    {
      name: "NVIDIA AI Workforce Hub",
      deadline: "Ongoing",
      urgent: false,
      amount: "Free training platform access",
      eligible: ["university", "university-private", "community-college", "k12-public", "k12-private", "k12-charter", "school-district"],
      description: "Free AI training courses and certifications for students and educators.",
      action: "Register at nvidia.com/training",
      url: "https://www.nvidia.com/en-us/training/"
    }
  ]
};

function getEligiblePrograms(institutionType) {
  const eligible = { urgent: [], federal: [], state: [], nvidia: [] };

  for (const program of PROGRAMS.federal) {
    if (program.eligible.includes(institutionType)) {
      if (program.urgent) {
        eligible.urgent.push(program);
      } else {
        eligible.federal.push(program);
      }
    }
  }
  for (const program of PROGRAMS.state) {
    if (program.eligible.includes(institutionType)) {
      eligible.state.push(program);
    }
  }
  for (const program of PROGRAMS.nvidia) {
    if (program.eligible.includes(institutionType)) {
      eligible.nvidia.push(program);
    }
  }

  return eligible;
}

function buildEligibilityReport(data) {
  const name = data.name || "Registrant";
  const org = data.organization || "Your Institution";
  const type = data.institution_type || "university";
  const parish = data.parish || "Louisiana";

  const programs = getEligiblePrograms(type);
  const totalCount = programs.urgent.length + programs.federal.length + programs.state.length + programs.nvidia.length;

  let report = `
ELIGIBILITY REPORT — ${org}
Louisiana's AI Infrastructure Initiative
Generated: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })}
═══════════════════════════════════════════════════════

Dear ${name},

Based on your registration, we've identified ${totalCount} programs that ${org} in ${parish} Parish may be eligible for. Below is your custom eligibility assessment.

`;

  if (programs.urgent.length > 0) {
    report += `
⚠️  URGENT — DEADLINES CLOSING NOW
───────────────────────────────────
`;
    for (const p of programs.urgent) {
      report += `
${p.name}
  Deadline: ${p.deadline}
  Amount: ${p.amount}
  ${p.description}
  ACTION: ${p.action}
  URL: ${p.url}
`;
    }
  }

  if (programs.federal.length > 0) {
    report += `

FEDERAL PROGRAMS
────────────────
`;
    for (const p of programs.federal) {
      report += `
${p.name}
  Deadline: ${p.deadline}
  Amount: ${p.amount}
  ${p.description}
  ACTION: ${p.action}
  URL: ${p.url}
`;
    }
  }

  if (programs.state.length > 0) {
    report += `

STATE OF LOUISIANA PROGRAMS
───────────────────────────
`;
    for (const p of programs.state) {
      report += `
${p.name}
  Deadline: ${p.deadline}
  Amount: ${p.amount}
  ${p.description}
  ACTION: ${p.action}
  URL: ${p.url}
`;
    }
  }

  if (programs.nvidia.length > 0) {
    report += `

NVIDIA PROGRAMS
───────────────
`;
    for (const p of programs.nvidia) {
      report += `
${p.name}
  Deadline: ${p.deadline}
  Amount: ${p.amount}
  ${p.description}
  ACTION: ${p.action}
  URL: ${p.url}
`;
    }
  }

  report += `

═══════════════════════════════════════════════════════

NEXT STEPS:
1. Review the programs above — especially any marked URGENT
2. We will follow up within 24 hours with pre-filled application templates for your highest-priority programs
3. If you have questions, call (337) 448-4242 (24/7 AI-assisted) or reply to this email

This service is 100% free. We will never charge you.

Louisiana's AI Infrastructure Initiative
(337) 448-4242 | info@louisianaai.net | louisianaai.net
`;

  return { report, totalCount, urgentCount: programs.urgent.length };
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const data = req.body;
    const { report, totalCount, urgentCount } = buildEligibilityReport(data);

    const name = data.name || "Registrant";
    const email = data.email || "";
    const org = data.organization || "Unknown";
    const type = data.institution_type || "unknown";

    // Send eligibility report to the registrant
    if (email) {
      try {
        await fetch('https://formsubmit.co/ajax/' + email, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            name: "Louisiana's AI Infrastructure Initiative",
            email: 'info@louisianaai.net',
            _subject: `Your Eligibility Report — ${totalCount} Programs Identified${urgentCount > 0 ? ' (' + urgentCount + ' URGENT)' : ''}`,
            message: report,
            _template: 'box'
          })
        });
      } catch (e) {
        console.error('Failed to send eligibility report to registrant:', e.message);
      }
    }

    // Send copy + notification to Mission Control
    try {
      await fetch('https://formsubmit.co/ajax/info@louisianaai.net', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          name: `New Registration: ${name} — ${org}`,
          email: 'system@louisianaai.net',
          _subject: `📋 Registration: ${name} — ${org} (${type}) — ${totalCount} programs, ${urgentCount} urgent`,
          message: `NEW REGISTRATION\n\nName: ${name}\nEmail: ${email}\nOrg: ${org}\nType: ${type}\nParish: ${data.parish || 'N/A'}\nPhone: ${data.phone || 'N/A'}\nNeeds: ${data.needs || 'N/A'}\n\n${'='.repeat(50)}\n\nELIGIBILITY REPORT SENT TO REGISTRANT:\n\n${report}`,
          _template: 'box'
        })
      });
    } catch (e) {
      console.error('Failed to send to Mission Control:', e.message);
    }

    return res.status(200).json({
      status: 'processed',
      programs_identified: totalCount,
      urgent_programs: urgentCount,
      report_sent: !!email
    });

  } catch (err) {
    console.error('Processing error:', err.message);
    return res.status(500).json({ error: 'Processing error', message: err.message });
  }
}
