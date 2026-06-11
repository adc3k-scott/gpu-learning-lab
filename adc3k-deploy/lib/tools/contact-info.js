// ROXY Tool: Contact Info
// Returns business contact details — prevents LLM hallucination

module.exports = {
  name: "get_contact_info",
  description: "Get AI Advantage business contact information including phone, email, address, and website.",
  parameters: {
    type: "object",
    properties: {},
    required: [],
  },
  async execute() {
    return JSON.stringify({
      business_name: "AI Advantage",
      parent_company: "Advantage Design & Construction",
      phone: "(337) 486-3149",
      email: "contact@ai-advantage.info",
      website: "ai-advantage.info",
      address: "1201 SE Evangeline Thruway, Lafayette, LA 70501",
      state: "Louisiana",
      booking_url: process.env.BOOKING_URL || "https://ai-advantage.info",
    });
  },
};
