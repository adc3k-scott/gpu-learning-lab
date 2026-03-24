/**
 * Brevo CRM Sync — Central intake for ALL form submissions
 *
 * Every form on every site calls this endpoint.
 * It creates a contact in Brevo CRM, creates a deal in the pipeline,
 * sends an auto-response to the submitter, and notifies Mission Control.
 *
 * Pipelines:
 *   - schools: School/university registrations
 *   - investors: Investor/alumni inquiries
 *   - careers: Join the team applications
 *   - contact: General contact/inquiries
 *   - phone: Phone call logs from Bland.ai
 *
 * POST /api/brevo-sync
 * Body: { pipeline, name, email, organization, phone, message, ...extra }
 */

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const BREVO_API_KEY = process.env.BREVO_API_KEY;
  if (!BREVO_API_KEY) {
    return res.status(500).json({ error: 'BREVO_API_KEY not configured' });
  }

  const headers = {
    'api-key': BREVO_API_KEY,
    'Content-Type': 'application/json',
  };

  try {
    const data = req.body;
    const pipeline = data.pipeline || 'contact';
    const name = data.name || 'Unknown';
    const email = data.email || '';
    const org = data.organization || '';
    const phone = data.phone || '';
    const message = data.message || data.needs || '';
    const parish = data.parish || '';
    const type = data.institution_type || data.type || '';

    // Step 1: Create or update contact in Brevo
    let contactCreated = false;
    if (email) {
      try {
        const contactResp = await fetch('https://api.brevo.com/v3/contacts', {
          method: 'POST',
          headers,
          body: JSON.stringify({
            email,
            attributes: {
              FIRSTNAME: name.split(' ')[0],
              LASTNAME: name.split(' ').slice(1).join(' ') || '',
              SMS: phone,
              COMPANY: org,
            },
            listIds: getListId(pipeline),
            updateEnabled: true,
          }),
        });
        contactCreated = contactResp.ok || contactResp.status === 204;
      } catch (e) {
        console.error('Contact creation failed:', e.message);
      }
    }

    // Step 2: Create deal in pipeline
    let dealCreated = false;
    try {
      const dealResp = await fetch('https://api.brevo.com/v3/crm/deals', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          name: `${getPipelineLabel(pipeline)}: ${name} — ${org || 'Individual'}`,
          attributes: {
            deal_stage: 'new',
            pipeline: pipeline,
            source_page: data.source || 'unknown',
            institution_type: type,
            parish: parish,
            notes: message,
          },
        }),
      });
      dealCreated = dealResp.ok;
      if (dealResp.ok) {
        const dealData = await dealResp.json();
        console.log(`Deal created: ${dealData.id}`);
      }
    } catch (e) {
      console.error('Deal creation failed:', e.message);
    }

    // Step 3: Send auto-response to submitter
    let responseSent = false;
    if (email) {
      try {
        const autoResponse = getAutoResponse(pipeline, name, org, type);
        const emailResp = await fetch('https://api.brevo.com/v3/smtp/email', {
          method: 'POST',
          headers,
          body: JSON.stringify({
            sender: { name: "Louisiana's AI Infrastructure Initiative", email: 'info@louisianaai.net' },
            to: [{ email, name }],
            subject: autoResponse.subject,
            textContent: autoResponse.body,
          }),
        });
        responseSent = emailResp.ok || emailResp.status === 201;
      } catch (e) {
        console.error('Auto-response failed:', e.message);
      }
    }

    // Step 4: Notify Mission Control
    try {
      await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          sender: { name: 'Mission Control', email: 'info@louisianaai.net' },
          to: [{ email: 'info@louisianaai.net', name: 'Mission Control' }],
          subject: `[${pipeline.toUpperCase()}] New: ${name} — ${org || 'Individual'}`,
          textContent: `NEW ${pipeline.toUpperCase()} SUBMISSION\n\nName: ${name}\nEmail: ${email}\nOrg: ${org}\nPhone: ${phone}\nType: ${type}\nParish: ${parish}\nMessage: ${message}\n\nSource: ${data.source || 'unknown'}\nContact created: ${contactCreated}\nDeal created: ${dealCreated}\nAuto-response sent: ${responseSent}\n\nTimestamp: ${new Date().toISOString()}`,
        }),
      });
    } catch (e) {
      console.error('MC notification failed:', e.message);
    }

    // Step 5: If school registration, also trigger eligibility processor
    if (pipeline === 'schools' && email) {
      try {
        const baseUrl = req.headers.host ? `https://${req.headers.host}` : 'https://louisianaai.net';
        fetch(`${baseUrl}/api/process-registration`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }).catch(() => {});
      } catch (e) {}
    }

    return res.status(200).json({
      status: 'synced',
      pipeline,
      contact_created: contactCreated,
      deal_created: dealCreated,
      response_sent: responseSent,
    });

  } catch (err) {
    console.error('Brevo sync error:', err.message);
    return res.status(500).json({ error: 'Sync failed', message: err.message });
  }
}


function getListId(pipeline) {
  // Brevo list IDs — create these lists in Brevo
  const lists = {
    schools: [4],      // School Districts list
    universities: [6], // Universities list
    investors: [10],   // Will be created
    careers: [12],     // Will be created
    contact: [14],     // Will be created
    phone: [16],       // Will be created
  };
  return lists[pipeline] || [14];
}


function getPipelineLabel(pipeline) {
  const labels = {
    schools: 'School Registration',
    investors: 'Investor Inquiry',
    careers: 'Career Application',
    contact: 'General Contact',
    phone: 'Phone Call',
    universities: 'University Registration',
  };
  return labels[pipeline] || 'Contact';
}


function getAutoResponse(pipeline, name, org, type) {
  const responses = {
    schools: {
      subject: `Welcome to Louisiana's AI Infrastructure Initiative — ${org}`,
      body: `Dear ${name},\n\nThank you for registering ${org} with Louisiana's AI Infrastructure Initiative.\n\nHere's what happens next:\n\n1. WITHIN MINUTES — You will receive a custom eligibility report identifying which federal and state programs your institution qualifies for.\n\n2. FILING ASSISTANCE — You will receive step-by-step filing instructions with pre-filled application templates.\n\n3. DEADLINE TRACKING — We monitor every deadline and send you alerts.\n\nThe NVIDIA Academic Grant closes March 31. If your institution qualifies, we'll flag it as urgent.\n\nQuestions? Call (337) 448-4242 — we answer 24/7.\n\nThis service is 100% free.\n\nLouisiana's AI Infrastructure Initiative\n(337) 448-4242 | info@louisianaai.net | louisianaai.net`,
    },
    investors: {
      subject: `Thank you for your interest — Louisiana's AI Infrastructure Initiative`,
      body: `Dear ${name},\n\nThank you for your interest in investing in Louisiana's AI infrastructure.\n\nWe received your registration and a member of our team will review your profile and reach out within 24 hours with information appropriate to your investment level.\n\nIn the meantime, you can explore:\n- Our campus sites: adc3k.com/lsu (Tiger Compute Campus) and adc3k.com/trappeys (Ragin' Cajun Compute Campus)\n- Engineering blueprints: adc3k.com/blueprints\n- Power architecture: adc3k.com/power-lsu\n\nIf you have immediate questions, call (337) 448-4242.\n\nScott Tomsu\nFounder — Advantage Design & Construction\nscott@adc3k.com | adc3k.com`,
    },
    careers: {
      subject: `Application received — Louisiana's AI Infrastructure Initiative`,
      body: `Dear ${name},\n\nThank you for your interest in joining the team. We received your application and will review it promptly.\n\nWe're building something unprecedented — two AI factory campuses in Louisiana, a statewide education initiative, and the autonomous systems to run it all. We need people who can think big and move fast.\n\nWe'll be in touch within 48 hours.\n\nScott Tomsu\nFounder — Advantage Design & Construction\n(337) 448-4242 | scott@adc3k.com`,
    },
    contact: {
      subject: `We received your message — Louisiana's AI Infrastructure Initiative`,
      body: `Dear ${name},\n\nThank you for reaching out. We received your message and will respond within 24 hours.\n\nIf this is urgent, call (337) 448-4242 — our AI assistant is available 24/7.\n\nLouisiana's AI Infrastructure Initiative\ninfo@louisianaai.net | louisianaai.net`,
    },
    phone: {
      subject: `Follow-up from your call — Louisiana's AI Infrastructure Initiative`,
      body: `Dear ${name},\n\nThank you for calling Louisiana's AI Infrastructure Initiative. This is a follow-up with additional information based on your call.\n\nVisit louisianaai.net to register your institution or learn more about our programs.\n\nCall us back anytime at (337) 448-4242.\n\nLouisiana's AI Infrastructure Initiative`,
    },
  };
  return responses[pipeline] || responses.contact;
}
