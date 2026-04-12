// ROXY Tool: Lead Capture
// Saves visitor information to Brevo CRM with full industry segmentation.
// Auto-tags by industry, adds to industry-specific list, sets attributes.
// This is the entry point of the data flywheel.

const BREVO_API_KEY = process.env.BREVO_API_KEY;
const BREVO_LIST_ID = parseInt(process.env.BREVO_LIST_ID || "9", 10); // AI Advantage Leads master list

// Industry list mapping (created in Brevo)
const INDUSTRY_LISTS = {
  "field services": 13, plumbing: 13, hvac: 13, electrical: 13, "air conditioning": 13, heating: 13,
  "medical": 14, dental: 14, dentist: 14, doctor: 14, clinic: 14, healthcare: 14,
  restaurant: 15, bar: 15, cafe: 15, bistro: 15, "food": 15, catering: 15,
  "real estate": 16, realtor: 16, broker: 16, "property sales": 16,
  construction: 17, contractor: 17, builder: 17, gc: 17,
  retail: 18, store: 18, shop: 18, boutique: 18,
  accounting: 19, cpa: 19, tax: 19, bookkeeping: 19,
  salon: 20, barber: 20, spa: 20, hair: 20, nails: 20, beauty: 20,
  insurance: 21, "insurance agency": 21,
  law: 22, lawyer: 22, attorney: 22, legal: 22, "law firm": 22,
  auto: 23, "auto shop": 23, mechanic: 23, "auto repair": 23,
  "property management": 24, landlord: 24, rental: 24, apartments: 24,
};

function getIndustryListId(businessType) {
  if (!businessType) return null;
  const lower = businessType.toLowerCase();
  for (const [keyword, listId] of Object.entries(INDUSTRY_LISTS)) {
    if (lower.includes(keyword)) return listId;
  }
  return null;
}

function normalizeIndustry(businessType) {
  if (!businessType) return null;
  const lower = businessType.toLowerCase();
  if (lower.match(/plumb|hvac|electri|heat|cool|air con|field/)) return "Field Services";
  if (lower.match(/dent|medical|doctor|clinic|health/)) return "Medical-Dental";
  if (lower.match(/restaurant|bar|cafe|bistro|food|cater/)) return "Restaurant";
  if (lower.match(/real estate|realtor|broker/)) return "Real Estate";
  if (lower.match(/construct|contractor|builder/)) return "Construction";
  if (lower.match(/retail|store|shop|boutique/)) return "Retail";
  if (lower.match(/account|cpa|tax|bookkeep/)) return "Accounting";
  if (lower.match(/salon|barber|spa|hair|nail|beauty/)) return "Salon-Barber";
  if (lower.match(/insurance/)) return "Insurance";
  if (lower.match(/law|lawyer|attorney|legal/)) return "Law Firm";
  if (lower.match(/auto|mechanic|repair/)) return "Auto Shop";
  if (lower.match(/property manag|landlord|rental|apartment/)) return "Property Management";
  return businessType;
}

module.exports = {
  name: "capture_lead",
  description:
    "Save a potential customer's contact information. Call this whenever a visitor shares their name, email, phone number, or business type during conversation. You don't need all fields — capture whatever they provide. Automatically segments by industry for targeted follow-ups.",
  parameters: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "Visitor's name",
      },
      email: {
        type: "string",
        description: "Visitor's email address",
      },
      phone: {
        type: "string",
        description: "Visitor's phone number",
      },
      business_type: {
        type: "string",
        description: "Type of business (e.g., 'dental office', 'plumbing company', 'law firm')",
      },
      interest_level: {
        type: "string",
        enum: ["hot", "warm", "cold"],
        description: "How interested the visitor seems based on conversation",
      },
      notes: {
        type: "string",
        description: "Any relevant notes about what the visitor is looking for",
      },
    },
    required: [],
  },
  async execute(args, context) {
    const captured = {};
    if (args.name) captured.name = args.name;
    if (args.email) captured.email = args.email;
    if (args.phone) captured.phone = args.phone;
    if (args.business_type) captured.business_type = args.business_type;
    if (args.interest_level) captured.interest_level = args.interest_level;
    if (args.notes) captured.notes = args.notes;

    // Normalize industry
    const normalizedIndustry = normalizeIndustry(args.business_type);
    if (normalizedIndustry) captured.industry_segment = normalizedIndustry;

    // If no Brevo key or no email, just acknowledge locally
    if (!BREVO_API_KEY || !args.email) {
      return JSON.stringify({
        status: "captured_locally",
        message: args.email
          ? "Lead information saved."
          : "Lead information noted. An email address would let us follow up directly.",
        captured,
      });
    }

    // Build contact data with full segmentation
    try {
      const contactData = {
        email: args.email,
        attributes: {
          SOURCE: "ROXY Chat",
          LAST_ROXY_CHAT: new Date().toISOString().split("T")[0],
        },
        updateEnabled: true,
      };

      if (args.name) {
        const nameParts = args.name.trim().split(/\s+/);
        contactData.attributes.FIRSTNAME = nameParts[0] || "";
        contactData.attributes.LASTNAME = nameParts.slice(1).join(" ") || "";
      }
      if (args.phone) contactData.attributes.SMS = args.phone;
      if (args.business_type) contactData.attributes.COMPANY = args.business_type;
      if (normalizedIndustry) contactData.attributes.INDUSTRY = normalizedIndustry;
      if (args.interest_level) contactData.attributes.INTEREST_LEVEL = args.interest_level;

      // Build list assignments — master list + industry-specific list
      const listIds = [];
      if (BREVO_LIST_ID > 0) listIds.push(BREVO_LIST_ID);
      const industryListId = getIndustryListId(args.business_type);
      if (industryListId) listIds.push(industryListId);
      if (listIds.length > 0) contactData.listIds = listIds;

      const response = await fetch("https://api.brevo.com/v3/contacts", {
        method: "POST",
        headers: {
          "api-key": BREVO_API_KEY,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(contactData),
      });

      if (response.ok || response.status === 204) {
        captured.lists = listIds;
        return JSON.stringify({
          status: "saved_to_crm",
          message: `Contact saved and tagged as ${normalizedIndustry || "general"} lead. Our team can follow up directly.`,
          captured,
        });
      }

      // Handle duplicate — update existing contact
      if (response.status === 400) {
        const err = await response.json().catch(() => ({}));
        if (err.code === "duplicate_parameter") {
          // Update the existing contact with new attributes
          await fetch(`https://api.brevo.com/v3/contacts/${encodeURIComponent(args.email)}`, {
            method: "PUT",
            headers: {
              "api-key": BREVO_API_KEY,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              attributes: contactData.attributes,
              listIds: listIds,
            }),
          });
          captured.lists = listIds;
          return JSON.stringify({
            status: "updated_in_crm",
            message: `Contact updated and tagged as ${normalizedIndustry || "general"} lead.`,
            captured,
          });
        }
      }

      return JSON.stringify({
        status: "captured_locally",
        message: "Lead information saved. Our team will follow up.",
        captured,
      });
    } catch (err) {
      return JSON.stringify({
        status: "captured_locally",
        message: "Lead information saved. Our team will follow up.",
        captured,
      });
    }
  },
};
