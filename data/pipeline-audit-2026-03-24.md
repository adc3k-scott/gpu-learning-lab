# ADC Submission Pipeline Audit — 2026-03-24

## PART 1: COMPLETE PIPELINE INVENTORY

### Overview

ADC currently has **10 distinct submission entry points** across 2 domains, plus a **phone system** and **4 serverless API endpoints**. Data flows to **2 different email addresses** via **2 different delivery systems** (FormSubmit.co and Brevo SMTP API). There is **no central database**. There is **no unified dashboard**. Registration tracking resets on every Vercel cold start.

---

## PIPELINE MAP

### Pipeline 1: louisianaai.net — School Registration Form
- **URL**: https://louisianaai.net
- **Form action**: `formsubmit.co/info@louisianaai.net`
- **Fields**: name, email, phone, organization, parish, institution_type, needs
- **Hidden fields**: _subject ("Get Your School In"), _captcha (false), _template (table), _autoresponse, _next (redirect to /registered)
- **What happens**:
  1. FormSubmit sends email to info@louisianaai.net (raw form data)
  2. JavaScript fires `/api/process-registration` in background (non-blocking)
  3. process-registration matches institution_type to 13 programs
  4. Brevo SMTP sends eligibility report to registrant
  5. Brevo SMTP sends copy + notification to info@louisianaai.net
  6. Logs registration to `/api/registrations` (in-memory, resets on cold start)
  7. Auto-triggers `/api/filing-assistant` in background
  8. Filing assistant sends pre-filled templates to registrant via Brevo
  9. Filing assistant notifies info@louisianaai.net via Brevo
  10. User redirected to /registered confirmation page
- **Status**: WORKING but fragile. The JS fetch to process-registration fires in the background and could silently fail. No retry. No persistent storage. Scott gets 3 emails per registration (FormSubmit + eligibility notification + filing notification) but has no way to see them in a pipeline view.
- **Test result**: Endpoint responded with `{"status":"processed","programs_identified":13,"urgent_programs":2,"report_sent":false,"filing_assistant":"triggered"}`

### Pipeline 2: adc3k.com — Main Contact Form (x2)
- **URL**: https://adc3k.com (appears twice on the page — ecosystem section + contact section)
- **Form action**: `formsubmit.co/scott@adc3k.com`
- **Fields**: name, email, organization, role, message
- **Hidden fields**: _subject, _captcha (false), _template (table)
- **What happens**:
  1. FormSubmit sends email to scott@adc3k.com
  2. That's it. No automation. No auto-response. No tracking.
- **Status**: WORKING but bare minimum. No acknowledgment to submitter. No CRM entry. No pipeline tracking.

### Pipeline 3: adc3k.com — Newsletter Signup
- **URL**: https://adc3k.com (footer newsletter bar)
- **Form action**: `formsubmit.co/info@louisianaai.net`
- **Fields**: email only
- **Hidden fields**: _subject ("ADC3K Newsletter Signup")
- **What happens**:
  1. FormSubmit sends email to info@louisianaai.net with the subscriber's email
  2. That's it. No mailing list. No Brevo contact creation. No confirmation.
- **Status**: BROKEN DESIGN. Newsletter signups go to an email inbox, not a mailing list. There is no way to send newsletters to these people later without manually extracting emails from inbox.

### Pipeline 4: adc3k.com/lsu — LSU/Willow Glen Interest Form
- **URL**: https://adc3k.com/lsu
- **Form action**: `formsubmit.co/scott@adc3k.com`
- **Fields**: name, email, organization, interest, message
- **Hidden fields**: _subject, _captcha (false), _template (table)
- **What happens**:
  1. FormSubmit sends email to scott@adc3k.com
  2. That's it.
- **Status**: WORKING but no automation.

### Pipeline 5: adc3k.com/trappeys-investors — Trappeys Investor Form
- **URL**: https://adc3k.com/trappeys-investors
- **Form action**: `formsubmit.co/scott@adc3k.com`
- **Fields**: name, email, organization, interest, message
- **Hidden fields**: _subject, _captcha (false), _template (table)
- **What happens**:
  1. FormSubmit sends email to scott@adc3k.com
  2. That's it.
- **Status**: WORKING but no automation. An investor filling this out gets zero acknowledgment.

### Pipeline 6: adc3k.com/alumni-investors — Investor Registration Gate
- **URL**: https://adc3k.com/alumni-investors
- **Form action**: `formsubmit.co/info@louisianaai.net`
- **Fields**: name, email, phone, organization, type (dropdown), interest, message
- **Hidden fields**: _subject ("Alumni & Investor Registration"), _captcha (false), _template (table)
- **What happens**:
  1. FormSubmit sends email to info@louisianaai.net
  2. That's it. No tier assignment. No auto-response. No CRM.
- **Status**: WORKING but investors get nothing back. The tier system (described in data/investor-tiers.md) is entirely manual.

### Pipeline 7: adc3k.com/join — Join the Team
- **URL**: https://adc3k.com/join
- **Form action**: `formsubmit.co/info@louisianaai.net`
- **Fields**: name, email, phone, location, role_interest, availability, about
- **Hidden fields**: _subject, _captcha (false), _template (table), _next
- **What happens**:
  1. FormSubmit sends email to info@louisianaai.net
  2. That's it.
- **Status**: WORKING but applicants get zero acknowledgment. No tracking of candidates.

### Pipeline 8: adc3k.com/learn — Education Interest
- **URL**: https://adc3k.com/learn
- **Form action**: `formsubmit.co/info@louisianaai.net`
- **Fields**: name, email, message
- **Hidden fields**: _subject, _captcha (false), _template (table)
- **What happens**:
  1. FormSubmit sends email to info@louisianaai.net
  2. That's it.
- **Status**: WORKING but minimal.

### Pipeline 9: Bland.ai Phone System
- **Numbers**: +1 (337) 247-1020 (outbound), +1 (337) 706-8810 (outbound), +1 (337) 448-4242 (inbound)
- **Total calls to date**: 24
- **Recent activity**: 5 calls in last 3 days (mostly short — test calls, 0.1-2.8 min)
- **Webhook**: POST louisianaai.net/api/webhook
- **What happens**:
  1. Call ends, Bland.ai sends webhook with transcript, variables, pathway logs
  2. Webhook extracts caller info, determines department (Education vs Investor/Vendor)
  3. Formats call log email
  4. Sends via FormSubmit to info@louisianaai.net
  5. Returns success to Bland
- **Status**: WORKING. But call data goes to email only. No CRM. No follow-up tracking. No way to see all calls in a dashboard.
- **Test result**: `{"status":"received","call_id":"unknown","department":"General","logged":true}`

### Pipeline 10: louisianaai.net API Endpoints
- **POST /api/process-registration**: Eligibility engine. 13 programs matched. Sends via Brevo. WORKING.
- **POST /api/filing-assistant**: Generates filing templates. 7 programs with templates. Sends via Brevo. WORKING.
- **GET /api/registrations**: Returns in-memory count. Resets on cold start. Currently shows 0 registrations.
- **POST /api/webhook**: Bland.ai receiver. WORKING.
- **Brevo stats** (last 7 days): 1 email sent, 1 delivered, 2 opens, 1 unique open, 0 bounces.
- **Test result for filing-assistant**: `{"status":"sent","programs_with_templates":7,"recipient":""}` (sent to empty email because test had no email)

---

## CRITICAL PROBLEMS IDENTIFIED

### Problem 1: TWO EMAIL ADDRESSES, NO CENTRAL VIEW
- `scott@adc3k.com` receives: adc3k.com main contact, LSU interest, Trappeys investors
- `info@louisianaai.net` receives: school registrations, alumni/investors, join the team, learn interest, newsletter signups, phone call logs, eligibility reports, filing packages
- Scott has to check two inboxes. There is no unified view.

### Problem 2: NO DATABASE — EVERYTHING IS EMAIL
- Zero persistent storage for any submission
- Registration tracker is in-memory (resets on Vercel cold start — currently 0)
- The only "database" is scattered emails across two inboxes
- Cannot query "how many investors registered this month" or "what's the status of the UL Lafayette registration"

### Problem 3: NO AUTO-RESPONSES ON 7 OF 10 PIPELINES
- Only louisianaai.net school registration gets an auto-response (eligibility report + filing package)
- The other 7 form-based pipelines: submitter gets nothing. No "thanks, we got it." No timeline. Nothing.
- Investors, job applicants, LSU contacts, newsletter signups — all radio silence after submit.

### Problem 4: NEWSLETTER IS DEAD ON ARRIVAL
- Newsletter signups go to FormSubmit (email inbox), not a mailing list
- There is no way to send a newsletter to these subscribers
- Brevo is already integrated for transactional email but NOT for contact list management

### Problem 5: NO STATUS TRACKING
- No way to see: new -> contacted -> in progress -> filed -> complete
- No way to know if a school that registered ever filed their applications
- No way to know if an investor inquiry was followed up on

### Problem 6: DUPLICATE NOTIFICATIONS FOR SCHOOL REGISTRATIONS
- School registration triggers: FormSubmit email + Brevo eligibility notification + Brevo filing notification = 3 emails to info@louisianaai.net for one registration

### Problem 7: NO RETRY / ERROR HANDLING
- The JS fetch to process-registration fires and forgets. If it fails, nobody knows.
- If Brevo API is down, emails silently fail (caught but only logged to Vercel console)

---

## PART 2: CRM/AUTOMATION RESEARCH & RECOMMENDATION

### Options Evaluated

#### Option A: Brevo CRM (RECOMMENDED)
- **Already integrated** for transactional email (BREVO_API_KEY in Vercel env)
- **Free plan**: 100,000 contacts, 300 emails/day, 50 open deals, 1 pipeline, automation workflows
- **CRM features**: Contact management, deal pipelines, task tracking, automation workflows
- **Forms**: Built-in form builder that auto-creates contacts
- **Automation**: Form submission triggers workflows (auto-response, deal creation, notifications)
- **Webhooks**: Inbound webhooks to receive data from external forms; outbound webhooks from automations
- **API**: Full REST API — create contacts, create deals, trigger automations programmatically
- **Cost**: FREE for ADC's current volume. Paid ($31/mo) only if >50 open deals needed.
- **Key advantage**: Zero new vendor. Already have the API key. Already sending email through it.

#### Option B: HubSpot CRM Free
- **Free plan**: Contact management, deal pipelines, forms, email tracking, basic reporting
- **Pros**: More polished dashboard, better reporting, large ecosystem
- **Cons**: New vendor, new integration, automation limited on free tier ($50+/mo for workflows), 5 active lists limit
- **Verdict**: Overkill for current stage. Would require ripping out Brevo integration.

#### Option C: Airtable + Zapier
- **Pros**: Flexible database, great views (kanban, grid, calendar)
- **Cons**: Zapier costs money for multi-step zaps, another vendor, no built-in email
- **Verdict**: Good for dashboard but doesn't solve email/automation.

#### Option D: Notion Database
- **Pros**: Already have Notion integration in Mission Control
- **Cons**: No email automation, no forms, no deal pipeline, API is slow, not a CRM
- **Verdict**: Not suitable.

---

### RECOMMENDATION: Brevo CRM as Central Hub

**Why Brevo wins:**
1. Already integrated (BREVO_API_KEY deployed on Vercel)
2. Free tier covers everything ADC needs right now
3. Single platform for: contacts, deals, email, automation, forms
4. API lets us programmatically create contacts from every pipeline
5. Built-in deal pipeline with stages (new -> contacted -> in progress -> filed -> complete)
6. Automation workflows can send auto-responses per pipeline type
7. Contact lists for newsletter (finally makes newsletter functional)
8. Dashboard shows all contacts and deals in one place

---

## IMPLEMENTATION PLAN

### Phase 1: Centralize All Submissions into Brevo Contacts (Day 1)
**Change every form submission to also create a Brevo contact via API.**

For each of the 10 pipelines, add a serverless function (or modify existing ones) that:
1. Receives form data
2. Calls Brevo API `POST /v3/contacts` to create/update contact with attributes:
   - email, firstName, lastName, SMS (phone)
   - Custom attributes: ORGANIZATION, PIPELINE_SOURCE, INSTITUTION_TYPE, PARISH, SUBMISSION_DATE
3. Adds contact to the appropriate Brevo list:
   - List 1: School Registrations
   - List 2: Investors
   - List 3: Job Applicants
   - List 4: General Inquiries
   - List 5: Newsletter Subscribers
   - List 6: Phone Calls
4. Creates a Brevo Deal in the appropriate pipeline stage

**Technical approach**: Create a single `api/brevo-sync.js` serverless function on both sites that all forms POST to (in addition to FormSubmit). This keeps FormSubmit as backup while Brevo becomes the source of truth.

### Phase 2: Auto-Responses for Every Pipeline (Day 2)
Set up Brevo automation workflows:
- **Investor submission** -> immediate acknowledgment email + deal created in "Investor" pipeline
- **Job application** -> confirmation email with timeline + deal created in "Recruiting" pipeline
- **LSU interest** -> acknowledgment + relevant project info
- **Newsletter signup** -> welcome email + added to newsletter list (finally works)
- **School registration** -> keep existing eligibility engine, but also create Brevo contact + deal
- **Phone call** -> keep existing webhook, add Brevo contact creation

### Phase 3: Scott's Dashboard (Day 3)
- Brevo CRM dashboard shows all contacts, all deals, all pipeline stages
- Filter by list (investors vs schools vs applicants)
- Deal pipeline kanban: New -> Contacted -> In Progress -> Filed -> Complete
- No more checking two email inboxes

### Phase 4: Consolidate Email Addresses (Day 4)
- Route all FormSubmit forms to `scott@adc3k.com` (one inbox for backup)
- Brevo handles all real notification/tracking (info@louisianaai.net as sender)
- Scott only needs to check Brevo CRM dashboard + one email inbox

### Phase 5: Kill FormSubmit Dependency (Week 2)
- Once Brevo is confirmed working, switch forms from FormSubmit to direct API submission
- Eliminates the third-party dependency entirely
- All form data goes: browser -> Vercel serverless -> Brevo API
- Brevo handles: contact creation, deal creation, auto-response, notification to Scott

---

## API SKETCH: brevo-sync.js

```javascript
// Unified Brevo sync endpoint — all forms POST here
// POST /api/brevo-sync
export default async function handler(req, res) {
  const BREVO_API_KEY = process.env.BREVO_API_KEY;
  const data = req.body;

  // 1. Create/update contact
  await fetch('https://api.brevo.com/v3/contacts', {
    method: 'POST',
    headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: data.email,
      attributes: {
        FIRSTNAME: data.name?.split(' ')[0],
        LASTNAME: data.name?.split(' ').slice(1).join(' '),
        SMS: data.phone,
        ORGANIZATION: data.organization,
        SOURCE: data._pipeline, // "school", "investor", "job", "newsletter", etc.
      },
      listIds: [getListId(data._pipeline)],
      updateEnabled: true, // update if exists
    })
  });

  // 2. Create deal
  await fetch('https://api.brevo.com/v3/crm/deals', {
    method: 'POST',
    headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: `${data.name} — ${data.organization || 'Individual'}`,
      attributes: { pipeline_source: data._pipeline },
    })
  });

  // 3. Link contact to deal
  // (requires deal ID from step 2)

  return res.status(200).json({ status: 'synced' });
}
```

---

## COST

| Item | Cost |
|------|------|
| Brevo Free Plan | $0 |
| FormSubmit.co | $0 (already free) |
| Brevo 100K contacts | Included free |
| Brevo 300 emails/day | Included free |
| Brevo 50 open deals | Included free |
| Brevo 1 pipeline | Included free |
| Brevo automation | Included free (limited) |
| **Total** | **$0/month** |

Upgrade to Brevo Starter ($9/mo) only if >300 emails/day. Upgrade to Sales Essentials ($31/mo) only if >50 open deals.

---

## SUMMARY

**Current state**: 10 entry points, 2 email addresses, 0 databases, 0 dashboards, 7/10 pipelines with no auto-response. Data scattered across email inboxes. Newsletter signups go nowhere. No status tracking.

**Target state**: All submissions flow into Brevo CRM. Every submitter gets an auto-response. Scott sees one dashboard with all contacts, all deals, all pipeline stages. Newsletter actually works. Nothing falls through cracks.

**Tool**: Brevo (already integrated, free tier sufficient).

**Effort**: 4 days to full implementation. Day 1 is the critical one (brevo-sync.js).
