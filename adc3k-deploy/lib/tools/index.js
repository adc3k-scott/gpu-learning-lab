// ROXY Tool Registry
// Explicit imports for Vercel serverless bundling (nft can't trace fs.readdirSync)

const tools = new Map();

// Explicit tool imports — add new tools here
const TOOL_MODULES = [
  require("./contact-info"),
  require("./quote-builder"),
  require("./lead-capture"),
  require("./playbook-rag"),
  require("./book-appointment"),
  require("./send-followup"),
  require("./crm-lookup"),
  require("./business-lookup"),
  require("./competitor-intel"),
  require("./roi-calculator"),
  require("./send-sms"),
  require("./log-conversation"),
  require("./payment-link"),
  require("./franchise-qualifier"),
  require("./urgency-offer"),
  require("./live-demo"),
  require("./local-market-intel"),
  require("./generate-ad-copy"),
  require("./review-responder"),
  require("./social-posts"),
  require("./review-request"),
  require("./lead-magnet"),
  require("./email-campaign"),
  require("./generate-widget"),
  require("./outbound-call"),
  require("./score-lead"),
  require("./onboard-client"),
];

for (const tool of TOOL_MODULES) {
  if (tool.name && tool.description && tool.parameters && tool.execute) {
    tools.set(tool.name, tool);
  }
}

/** Get OpenAI-compatible tool definitions for the LLM */
function getToolDefinitions() {
  return Array.from(tools.values()).map((t) => ({
    type: "function",
    function: {
      name: t.name,
      description: t.description,
      parameters: t.parameters,
    },
  }));
}

/** Get Anthropic-compatible tool definitions for Claude fallback */
function getAnthropicToolDefinitions() {
  return Array.from(tools.values()).map((t) => ({
    name: t.name,
    description: t.description,
    input_schema: t.parameters,
  }));
}

/** Execute a tool by name */
async function executeTool(name, args, context) {
  const tool = tools.get(name);
  if (!tool) {
    return { error: `Unknown tool: ${name}` };
  }
  try {
    const timeout = tool.timeout || 5000;
    const result = await Promise.race([
      tool.execute(args, context),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Tool timeout")), timeout)
      ),
    ]);
    return { result: typeof result === "string" ? result : JSON.stringify(result) };
  } catch (err) {
    return { error: `Tool error: ${err.message}` };
  }
}

/** List all registered tool names */
function listTools() {
  return Array.from(tools.keys());
}

module.exports = {
  getToolDefinitions,
  getAnthropicToolDefinitions,
  executeTool,
  listTools,
};
