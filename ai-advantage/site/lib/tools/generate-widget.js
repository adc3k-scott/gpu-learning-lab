// ROXY SaaS Tool: White-Label Widget Generator
// Creates an embeddable chat widget for customer websites.
// Each customer gets a branded ROXY agent on their own site.
// This is the SaaS product — recurring revenue per widget.

module.exports = {
  name: "generate_widget",
  description:
    "Generate an embeddable chat widget that a business can add to their own website. The widget is branded with their business name and colors, and powered by ROXY on ADC's infrastructure. Use when discussing the product, when a customer asks about getting AI on their website, or during onboarding.",
  parameters: {
    type: "object",
    properties: {
      business_name: {
        type: "string",
        description: "The business name for branding",
      },
      industry: {
        type: "string",
        description: "The business industry (determines default behavior)",
      },
      primary_color: {
        type: "string",
        description: "Brand color in hex (e.g., '#2563eb'). Default: blue.",
      },
      greeting: {
        type: "string",
        description: "Custom greeting message (optional)",
      },
      phone: {
        type: "string",
        description: "Business phone number to display",
      },
    },
    required: ["business_name"],
  },
  async execute(args) {
    const biz = args.business_name;
    const color = args.primary_color || "#2563eb";
    const greeting = args.greeting || `Hey! I'm the AI assistant for ${biz}. How can I help you today?`;
    const industry = args.industry || "general";
    const phone = args.phone || "";

    // Generate a unique widget ID
    const widgetId = `roxy_${biz.toLowerCase().replace(/[^a-z0-9]/g, "_").slice(0, 20)}_${Date.now().toString(36)}`;

    // The embed code
    const embedCode = `<!-- ${biz} AI Assistant — Powered by ROXY / AI Advantage -->
<script>
(function(){
  var w=document.createElement('div');w.id='${widgetId}';
  var s=document.createElement('script');
  s.src='https://ai-advantage.info/widget.js';
  s.dataset.businessName='${biz.replace(/'/g, "\\'")}';
  s.dataset.industry='${industry}';
  s.dataset.color='${color}';
  s.dataset.greeting='${greeting.replace(/'/g, "\\'")}';
  s.dataset.widgetId='${widgetId}';
  ${phone ? `s.dataset.phone='${phone}';` : ""}
  document.body.appendChild(w);document.body.appendChild(s);
})();
</script>`;

    return JSON.stringify({
      widget_id: widgetId,
      embed_code: embedCode,
      instructions: [
        "Copy the embed code above",
        "Paste it just before the closing </body> tag on your website",
        "The chat bubble will appear in the bottom-right corner",
        "It's branded with your business name and colors",
        "All AI processing runs on ADC's infrastructure — no setup needed on your end",
      ],
      customization: {
        color: color,
        greeting: greeting,
        industry: industry,
        business_name: biz,
      },
      what_it_does: [
        "Answers customer questions about your business 24/7",
        "Captures leads (name, email, phone) into your CRM",
        "Books appointments directly from the chat",
        "Sends follow-up emails automatically",
        "Handles after-hours inquiries",
        `Uses your ${industry} industry playbook for accurate answers`,
      ],
      pricing_note: "Widget is included with your Pro and Enterprise plans. Basic plan customers can add it for $99/mo.",
      next_step: "Want me to customize the colors, greeting, or behavior? Or are you ready to embed it?",
    });
  },
};
