#!/usr/bin/env node
/**
 * sync-louisiana.js — Push Louisiana AI Initiative bot prompts to Bland.ai
 *
 * Usage:
 *   node sync-louisiana.js              # Sync all 3 bots
 *   node sync-louisiana.js --sarah      # Sync front desk only
 *   node sync-louisiana.js --michelle   # Sync education bot only
 *   node sync-louisiana.js --james      # Sync investor bot only
 *   node sync-louisiana.js --dry-run    # Show what would be sent
 *
 * Env vars (set in .env or export):
 *   BLAND_API_KEY              — Your Bland.ai API key
 *   BLAND_LOUISIANA_MAIN       — Main phone number (Sarah)
 *   BLAND_LOUISIANA_EDUCATION  — Education line (Michelle)
 *   BLAND_LOUISIANA_INVESTOR   — Investor line (James)
 */

const fs = require("fs");
const path = require("path");

// ---------- Config ----------
const BLAND_API_KEY = process.env.BLAND_API_KEY || "";
const PHONES = {
  sarah: process.env.BLAND_LOUISIANA_MAIN || "",
  michelle: process.env.BLAND_LOUISIANA_EDUCATION || "",
  james: process.env.BLAND_LOUISIANA_INVESTOR || "",
};

const PROMPT_FILES = {
  sarah: path.join(__dirname, "front-desk-prompt.md"),
  michelle: path.join(__dirname, "education-bot-prompt.md"),
  james: path.join(__dirname, "investor-bot-prompt.md"),
};

const FIRST_SENTENCES = {
  sarah:
    "Thank you for calling Louisiana's AI Infrastructure Initiative. This is Sarah. How can I help you today?",
  michelle:
    "Hi, this is Michelle with Education and University Relations. How can I help you?",
  james:
    "This is James with Infrastructure and Investment Relations. What can I help you with today?",
};

const WEBHOOKS = {
  sarah: "https://louisianaai.net/api/webhook",
  michelle: "https://louisianaai.net/api/webhook",
  james: "https://louisianaai.net/api/webhook",
};

// ---------- Parse prompt file ----------
function parsePrompt(filepath) {
  const raw = fs.readFileSync(filepath, "utf-8");
  const sections = raw.split(/^## /m).slice(1);

  let prompt = "";
  for (const section of sections) {
    const lines = section.split("\n");
    const title = lines[0].trim();
    const body = lines
      .slice(1)
      .join("\n")
      .replace(/\*\*/g, "")
      .trim();
    prompt += `${title.toUpperCase()}:\n${body}\n\n`;
  }

  return prompt.trim();
}

// ---------- Sync to Bland.ai ----------
async function syncBot(name, dryRun) {
  const phone = PHONES[name];
  const promptFile = PROMPT_FILES[name];
  const firstSentence = FIRST_SENTENCES[name];
  const webhook = WEBHOOKS[name];

  if (!phone) {
    console.log(`\n[${name.toUpperCase()}] No phone number set. Skipping.`);
    console.log(`  Set: export BLAND_LOUISIANA_${name === "sarah" ? "MAIN" : name === "michelle" ? "EDUCATION" : "INVESTOR"}=+1XXXXXXXXXX`);
    return false;
  }

  if (!BLAND_API_KEY) {
    console.log(`\n[${name.toUpperCase()}] BLAND_API_KEY not set. Skipping.`);
    return false;
  }

  const prompt = parsePrompt(promptFile);

  const payload = {
    prompt,
    first_sentence: firstSentence,
    webhook,
    max_duration: 900, // 15 minutes
  };

  if (dryRun) {
    console.log(`\n[${name.toUpperCase()}] DRY RUN:`);
    console.log(`  Phone: ${phone}`);
    console.log(`  Prompt: ${promptFile}`);
    console.log(`  Prompt length: ${prompt.length} chars`);
    console.log(`  First sentence: ${firstSentence}`);
    console.log(`  Webhook: ${webhook}`);
    return true;
  }

  console.log(`\n[${name.toUpperCase()}] Syncing to Bland.ai (${phone})...`);

  const phoneForUrl = phone.replace("+", "");
  const res = await fetch(`https://api.bland.ai/v1/inbound/${phoneForUrl}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${BLAND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (res.ok && data.status === "success") {
    console.log(`  [OK] ${name} agent updated.`);
    return true;
  } else {
    console.error(`  [FAIL]`, JSON.stringify(data, null, 2));
    return false;
  }
}

// ---------- Main ----------
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const sarahOnly = args.includes("--sarah");
  const michelleOnly = args.includes("--michelle");
  const jamesOnly = args.includes("--james");
  const doAll = !sarahOnly && !michelleOnly && !jamesOnly;

  console.log("=== Louisiana AI Infrastructure Initiative — Bot Sync ===");
  console.log(`Bland API Key: ${BLAND_API_KEY ? "SET" : "NOT SET"}`);
  console.log(`Main Phone: ${PHONES.sarah || "NOT SET"}`);
  console.log(`Education Phone: ${PHONES.michelle || "NOT SET"}`);
  console.log(`Investor Phone: ${PHONES.james || "NOT SET"}`);

  if (doAll || sarahOnly) await syncBot("sarah", dryRun);
  if (doAll || michelleOnly) await syncBot("michelle", dryRun);
  if (doAll || jamesOnly) await syncBot("james", dryRun);

  console.log("\nDone.");
}

main().catch((err) => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
