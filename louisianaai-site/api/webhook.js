/**
 * Bland.ai Webhook Receiver
 *
 * Receives post-call data from Bland.ai after every phone call.
 * Formats it and forwards to email for tracking.
 *
 * Bland sends: caller info, duration, transcript, pathway taken, etc.
 * We extract: name, phone, email, organization, what they need, which bot handled it.
 */

export default async function handler(req, res) {
  // Only accept POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Basic origin validation — check for Bland.ai user agent or call_id
  const data = req.body;
  if (!data || (!data.call_id && !data.c_id && !data.status)) {
    return res.status(400).json({ error: 'Invalid payload' });
  }

  try {

    // Extract key fields from Bland webhook payload
    const callId = data.call_id || data.id || 'unknown';
    const phoneNumber = data.from || data.phone_number || 'unknown';
    const duration = data.call_length || data.duration || 0;
    const status = data.status || data.completed || 'unknown';
    const transcript = data.concatenated_transcript || data.transcript || '';
    const summary = data.summary || '';
    const answeredBy = data.answered_by || '';
    const startedAt = data.started_at || data.created_at || new Date().toISOString();
    const pathwayLogs = data.pathway_logs || '';

    // Try to extract collected info from transcript/variables
    const variables = data.variables || {};
    const callerName = variables.name || extractFromTranscript(transcript, 'name');
    const callerEmail = variables.email || extractFromTranscript(transcript, 'email');
    const callerOrg = variables.organization || extractFromTranscript(transcript, 'organization');
    const callerNeed = variables.need || variables.interest || '';

    // Determine which bot handled the call
    let department = 'General';
    if (pathwayLogs) {
      if (typeof pathwayLogs === 'string') {
        if (pathwayLogs.includes('Michelle')) department = 'Education';
        else if (pathwayLogs.includes('James')) department = 'Investor/Vendor';
      }
    }
    if (transcript) {
      if (transcript.includes('Michelle') || transcript.includes('education')) department = 'Education';
      if (transcript.includes('James') || transcript.includes('invest') || transcript.includes('infrastructure')) department = 'Investor/Vendor';
    }

    // Format the call log
    const callLog = {
      timestamp: startedAt,
      call_id: callId,
      caller_phone: phoneNumber,
      caller_name: callerName,
      caller_email: callerEmail,
      caller_org: callerOrg,
      caller_need: callerNeed,
      department: department,
      duration_seconds: Math.round(duration),
      status: status,
      summary: summary,
      transcript_preview: transcript.substring(0, 500)
    };

    // Send formatted email via FormSubmit
    const emailBody = `
NEW CALL LOG — Louisiana's AI Infrastructure Initiative
═══════════════════════════════════════════════════════

Time: ${new Date(startedAt).toLocaleString('en-US', { timeZone: 'America/Chicago' })}
Phone: ${phoneNumber}
Duration: ${Math.round(duration)} seconds
Department: ${department}

CALLER INFO:
Name: ${callerName || 'Not collected'}
Email: ${callerEmail || 'Not collected'}
Organization: ${callerOrg || 'Not collected'}
Need: ${callerNeed || 'Not specified'}

CALL SUMMARY:
${summary || 'No summary available'}

TRANSCRIPT (first 500 chars):
${transcript.substring(0, 500) || 'No transcript available'}

═══════════════════════════════════════════════════════
Call ID: ${callId}
    `.trim();

    // Forward to email using FormSubmit API
    try {
      await fetch('https://formsubmit.co/ajax/info@louisianaai.net', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          name: `Call Log: ${callerName || phoneNumber}`,
          email: 'calls@louisianaai.net',
          _subject: `📞 ${department} Call — ${callerName || phoneNumber} — ${Math.round(duration)}s`,
          message: emailBody,
          _template: 'box'
        })
      });
    } catch (emailErr) {
      console.error('Email forward failed:', emailErr.message);
    }

    // Sync to Brevo CRM
    try {
      const baseUrl = req.headers.host ? `https://${req.headers.host}` : 'https://louisianaai.net';
      fetch(`${baseUrl}/api/brevo-sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pipeline: 'phone',
          name: callerName || phoneNumber,
          email: callerEmail || '',
          organization: callerOrg || '',
          phone: phoneNumber,
          message: summary || transcript.substring(0, 200),
          source: 'phone-call',
        })
      }).catch(function() {});
    } catch (e) {}

    // Return success to Bland
    return res.status(200).json({
      status: 'received',
      call_id: callId,
      department: department,
      logged: true
    });

  } catch (err) {
    console.error('Webhook error:', err.message);
    return res.status(500).json({ error: 'Internal error', message: err.message });
  }
}

/**
 * Try to extract info from transcript text
 */
function extractFromTranscript(transcript, field) {
  if (!transcript) return '';

  const lower = transcript.toLowerCase();

  if (field === 'name') {
    // Look for "my name is X" pattern
    const nameMatch = lower.match(/my name is ([a-z]+ [a-z]+)/i);
    if (nameMatch) return nameMatch[1].split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  if (field === 'email') {
    // Look for email pattern
    const emailMatch = transcript.match(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/);
    if (emailMatch) return emailMatch[1];
  }

  if (field === 'organization') {
    // Look for "from X" or "at X" or "with X"
    const orgMatch = lower.match(/(?:from|at|with) ([a-z]+ (?:university|school|college|academy|parish|district|company|inc|llc|corp))/i);
    if (orgMatch) return orgMatch[1].split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  return '';
}
