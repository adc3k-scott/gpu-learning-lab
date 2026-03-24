/**
 * Registration Tracker API
 *
 * GET /api/registrations — returns count and list of all registrations
 * POST /api/registrations — logs a new registration (called by process-registration)
 *
 * Uses Vercel Edge Config or in-memory for now.
 * TODO: Replace with proper database (Supabase, KV store, etc.)
 */

// In-memory store (resets on cold start — good enough for now,
// real data is in Brevo sent emails + FormSubmit notifications)
let registrations = [];

export default async function handler(req, res) {
  if (req.method === 'GET') {
    // Return registration stats
    // Since in-memory resets, also check Brevo campaign stats
    const BREVO_API_KEY = process.env.BREVO_API_KEY;

    let brevoStats = null;
    if (BREVO_API_KEY) {
      try {
        const resp = await fetch('https://api.brevo.com/v3/smtp/statistics/aggregatedReport?days=7', {
          headers: { 'api-key': BREVO_API_KEY }
        });
        if (resp.ok) {
          brevoStats = await resp.json();
        }
      } catch (e) {}
    }

    return res.status(200).json({
      status: 'ok',
      registrations_in_memory: registrations.length,
      registrations: registrations,
      brevo_stats: brevoStats,
      note: 'In-memory store resets on cold start. Check scott@adc3k.com inbox for complete FormSubmit history.',
    });
  }

  if (req.method === 'POST') {
    // Log a registration
    const data = req.body;
    registrations.push({
      timestamp: new Date().toISOString(),
      name: data.name || 'Unknown',
      email: data.email || '',
      organization: data.organization || '',
      institution_type: data.institution_type || '',
      parish: data.parish || '',
      programs_identified: data.programs_identified || 0,
    });

    return res.status(200).json({
      status: 'logged',
      total: registrations.length
    });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
