// ROXY Tool: Book Appointment
// Generates a booking link for a 15-minute discovery call

const BOOKING_URL = process.env.BOOKING_URL || "https://ai-advantage.info";

module.exports = {
  name: "book_appointment",
  description:
    "Generate a booking link for a free 15-minute discovery call. Use this when a visitor wants to schedule a call or meeting.",
  parameters: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "Visitor's name (for pre-filling the form)",
      },
      email: {
        type: "string",
        description: "Visitor's email (for pre-filling the form)",
      },
      phone: {
        type: "string",
        description: "Visitor's phone number",
      },
    },
    required: [],
  },
  async execute(args) {
    // Build the booking URL with any available params
    const params = new URLSearchParams();
    if (args.name) params.set("name", args.name);
    if (args.email) params.set("email", args.email);
    if (args.phone) params.set("phone", args.phone);

    const queryStr = params.toString();
    const url = queryStr ? `${BOOKING_URL}?${queryStr}` : BOOKING_URL;

    return JSON.stringify({
      booking_url: url,
      call_type: "15-minute discovery call",
      cost: "Free",
      what_happens: "We learn about your business and match you to the right industry playbook. No commitment, no pressure.",
      alternative: "You can also call us directly at (337) 486-3149 or email contact@ai-advantage.info",
    });
  },
};
