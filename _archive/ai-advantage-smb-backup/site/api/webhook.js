// Bland.ai webhook receiver — captures call data and lead info
// Stores leads in Vercel KV or logs them for now

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const payload = req.body || {};

  // Log the full payload for debugging
  console.log("BLAND WEBHOOK:", JSON.stringify(payload, null, 2));

  // Extract key fields from Bland.ai webhook
  const lead = {
    timestamp: new Date().toISOString(),
    call_id: payload.call_id || null,
    from: payload.from || null,
    to: payload.to || null,
    duration: payload.call_length || payload.duration || null,
    status: payload.status || payload.completed || null,
    summary: payload.summary || null,
    transcript: payload.concatenated_transcript || payload.transcript || null,
    // Extracted variables from the pathway (name, email, business type, etc.)
    variables: payload.variables || payload.pathway_variables || {},
    analysis: payload.analysis || null,
  };

  // For now, log it. Later we can store in a database or send email notification.
  console.log("LEAD CAPTURED:", JSON.stringify(lead, null, 2));

  // Always return 200 so Bland doesn't retry
  return res.status(200).json({ received: true, call_id: lead.call_id });
};
