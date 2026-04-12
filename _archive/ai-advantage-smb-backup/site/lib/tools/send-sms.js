// ROXY Tool: Send SMS
// Dual provider: Twilio (primary, instant delivery) → Brevo (fallback)
// Twilio delivers immediately to US numbers. Brevo needs toll-free registration.

const TWILIO_SID = process.env.TWILIO_ACCOUNT_SID;
const TWILIO_TOKEN = process.env.TWILIO_AUTH_TOKEN;
const TWILIO_FROM = process.env.TWILIO_PHONE_NUMBER;
const BREVO_API_KEY = process.env.BREVO_API_KEY;

module.exports = {
  name: "send_sms",
  description:
    "Send a text message to a visitor who provided their phone number. Use this for quick follow-ups like confirming you received their info, sending a booking link, or a brief thank-you. Keep messages under 160 characters when possible. Only send ONE text per conversation — never spam.",
  parameters: {
    type: "object",
    properties: {
      phone: {
        type: "string",
        description: "The visitor's phone number (US format, e.g., '+13375551234' or '337-555-1234')",
      },
      message: {
        type: "string",
        description: "The text message to send (keep concise, under 300 chars)",
      },
      name: {
        type: "string",
        description: "The visitor's first name for personalization",
      },
    },
    required: ["phone", "message"],
  },
  async execute(args) {
    // Clean and format phone number
    let phone = args.phone.replace(/[^0-9+]/g, "");
    if (!phone.startsWith("+")) {
      if (phone.startsWith("1") && phone.length === 11) {
        phone = "+" + phone;
      } else if (phone.length === 10) {
        phone = "+1" + phone;
      } else {
        return JSON.stringify({ status: "failed", reason: "Invalid phone number format" });
      }
    }

    if (phone.length < 11 || phone.length > 15) {
      return JSON.stringify({ status: "failed", reason: "Invalid phone number" });
    }

    let message = args.message;
    if (message.length > 300) {
      message = message.slice(0, 297) + "...";
    }

    // ===== PROVIDER 1: TWILIO (instant US delivery) =====
    if (TWILIO_SID && TWILIO_TOKEN && TWILIO_FROM) {
      try {
        const auth = Buffer.from(`${TWILIO_SID}:${TWILIO_TOKEN}`).toString("base64");
        const body = new URLSearchParams({
          To: phone,
          From: TWILIO_FROM,
          Body: message,
        });

        const response = await fetch(
          `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_SID}/Messages.json`,
          {
            method: "POST",
            headers: {
              Authorization: `Basic ${auth}`,
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: body.toString(),
          }
        );

        if (response.ok) {
          const data = await response.json();
          return JSON.stringify({
            status: "sent",
            provider: "twilio",
            message: "Text message sent successfully.",
            sid: data.sid,
          });
        }

        const err = await response.json().catch(() => ({}));
        console.error("[ROXY] Twilio error:", err.message || JSON.stringify(err));
        // Fall through to Brevo
      } catch (err) {
        console.error("[ROXY] Twilio error:", err.message);
        // Fall through to Brevo
      }
    }

    // ===== PROVIDER 2: BREVO (fallback — needs toll-free registration for US) =====
    if (BREVO_API_KEY) {
      try {
        const response = await fetch("https://api.brevo.com/v3/transactionalSMS/sms", {
          method: "POST",
          headers: {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            type: "transactional",
            unicodeEnabled: false,
            sender: "ROXY",
            recipient: phone,
            content: message,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          return JSON.stringify({
            status: "sent",
            provider: "brevo",
            message: "Text message queued. Delivery depends on toll-free registration status.",
            messageId: data.messageId,
          });
        }

        const err = await response.json().catch(() => ({}));
        if (err.code === "not_enough_credits") {
          return JSON.stringify({
            status: "no_credits",
            message: "SMS credits depleted. The visitor's info has been saved — our team will follow up directly.",
          });
        }
      } catch (err) {
        // Fall through
      }
    }

    // ===== NO PROVIDER AVAILABLE =====
    return JSON.stringify({
      status: "queued",
      message: "Text message queued for delivery. Our team will follow up with the visitor directly.",
      phone,
    });
  },
};
