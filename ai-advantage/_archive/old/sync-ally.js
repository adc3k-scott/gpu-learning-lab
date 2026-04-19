#!/usr/bin/env node
/**
 * sync-ally.js — Push Ally's prompt to Bland.ai phone agent + generate chat.js system prompt
 *
 * Usage:
 *   node sync-ally.js              # Sync both phone + chat
 *   node sync-ally.js --phone      # Sync phone only
 *   node sync-ally.js --chat       # Rebuild chat prompt only
 *   node sync-ally.js --dry-run    # Show what would be sent, don't send
 *
 * Env vars (set in .env or export):
 *   BLAND_API_KEY     — Your Bland.ai API key
 *   BLAND_PHONE       — Phone number to update (default: +13374863149)
 */

const fs = require("fs");
const path = require("path");

// ---------- Config ----------
const BLAND_PHONE = process.env.BLAND_PHONE || "+13374863149";
const BLAND_API_KEY = process.env.BLAND_API_KEY || "";
const PROMPT_FILE = path.join(__dirname, "ally-prompt.md");
const CHAT_JS = path.join(__dirname, "site", "api", "chat.js");

// ---------- Parse prompt file ----------
function parsePrompt() {
  const raw = fs.readFileSync(PROMPT_FILE, "utf-8");

  // Strip the header (everything before first ## section)
  const sections = raw.split(/^## /m).slice(1); // drop preamble

  // Build plain-text prompt from markdown
  let prompt = "";
  for (const section of sections) {
    const lines = section.split("\n");
    const title = lines[0].trim();
    const body = lines
      .slice(1)
      .join("\n")
      .replace(/\*\*/g, "") // strip bold
      .trim();

    // Skip phone-only rules for chat, skip chat-only rules for phone
    prompt += `${title.toUpperCase()}:\n${body}\n\n`;
  }

  return prompt.trim();
}

function buildChatPrompt() {
  const full = parsePrompt();
  // Remove the phone-specific section for chat
  return full
    .replace(/BEHAVIOR RULES \(PHONE — ADDITIONAL\):[\s\S]*$/, "")
    .trim();
}

function buildPhonePrompt() {
  const full = parsePrompt();
  // Merge both behavior sections for phone
  return full
    .replace("BEHAVIOR RULES (CHAT):", "YOUR BEHAVIOR RULES:")
    .replace("BEHAVIOR RULES (PHONE — ADDITIONAL):", "ADDITIONAL PHONE RULES:")
    .trim();
}

// ---------- Sync to Bland.ai ----------
async function syncPhone(dryRun) {
  const prompt = buildPhonePrompt();

  if (!BLAND_API_KEY) {
    console.log("\n[PHONE] BLAND_API_KEY not set. Skipping phone sync.");
    console.log("  Set it: export BLAND_API_KEY=your-key-here");
    return false;
  }

  const payload = {
    prompt,
    first_sentence:
      "Thanks for calling AI Advantage! This is Ally. How can I help you today?",
    webhook: "https://ai-advantage.info/api/webhook",
    max_duration: 600, // 10 minutes
  };

  if (dryRun) {
    console.log("\n[PHONE] DRY RUN — would send to Bland.ai:");
    console.log(`  Phone: ${BLAND_PHONE}`);
    console.log(`  Prompt length: ${prompt.length} chars`);
    console.log(`  First sentence: ${payload.first_sentence}`);
    console.log(`  Webhook: ${payload.webhook}`);
    return true;
  }

  console.log(`\n[PHONE] Syncing to Bland.ai (${BLAND_PHONE})...`);

  const phoneForUrl = BLAND_PHONE.replace("+", "");
  const res = await fetch(
    `https://api.bland.ai/v1/inbound/${phoneForUrl}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${BLAND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  const data = await res.json();

  if (res.ok && data.status === "success") {
    console.log("  [OK] Phone agent updated.");
    return true;
  } else {
    console.error("  [FAIL]", JSON.stringify(data, null, 2));
    return false;
  }
}

// ---------- Update chat.js system prompt ----------
function syncChat(dryRun) {
  const prompt = buildChatPrompt();
  const chatCode = fs.readFileSync(CHAT_JS, "utf-8");

  // Replace the SYSTEM_PROMPT template literal
  const startMarker = "const SYSTEM_PROMPT = `";
  const endMarker = "`;";

  const startIdx = chatCode.indexOf(startMarker);
  if (startIdx === -1) {
    console.log("\n[CHAT] Could not find SYSTEM_PROMPT in chat.js. Skipping.");
    return false;
  }

  const afterStart = startIdx + startMarker.length;
  const endIdx = chatCode.indexOf(endMarker, afterStart);
  if (endIdx === -1) {
    console.log("\n[CHAT] Could not find end of SYSTEM_PROMPT. Skipping.");
    return false;
  }

  // Rebuild the prompt as a JS template literal body
  const jsPrompt = prompt.replace(/`/g, "\\`").replace(/\$/g, "\\$");
  const newCode =
    chatCode.substring(0, afterStart) + jsPrompt + chatCode.substring(endIdx);

  if (dryRun) {
    console.log("\n[CHAT] DRY RUN — would update chat.js:");
    console.log(`  Prompt length: ${prompt.length} chars`);
    return true;
  }

  fs.writeFileSync(CHAT_JS, newCode, "utf-8");
  console.log("\n[CHAT] Updated chat.js SYSTEM_PROMPT.");
  console.log("  Remember to deploy: cd site && npx vercel --prod --yes");
  return true;
}

// ---------- Main ----------
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const phoneOnly = args.includes("--phone");
  const chatOnly = args.includes("--chat");
  const doAll = !phoneOnly && !chatOnly;

  console.log("=== Ally Prompt Sync ===");
  console.log(`Source: ${PROMPT_FILE}`);

  if (doAll || phoneOnly) await syncPhone(dryRun);
  if (doAll || chatOnly) syncChat(dryRun);

  console.log("\nDone.");
}

main().catch((err) => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
