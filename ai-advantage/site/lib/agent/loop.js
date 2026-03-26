// ROXY Agent Loop — ReAct-style tool-calling within a single request
// Max 3 iterations, fits within Vercel's 30-second timeout.

const providers = require("./providers");
const { getToolDefinitions, executeTool, listTools } = require("../tools");
const { buildSystemPrompt } = require("./system-prompt");
const { selectTools } = require("./tool-selector");
const { runWithLifecycle, getJobStats } = require("./job-manager");

const MAX_ITERATIONS = 3;

/**
 * Run the ROXY agent loop
 * @param {Object} opts
 * @param {Array} opts.messages - Conversation history [{ role, content }]
 * @param {string} opts.sessionId - Session identifier
 * @param {Object} opts.sessionContext - Known visitor info (name, email, etc.)
 * @returns {{ reply: string, source: string, toolsUsed: string[], sessionContext: Object, analytics: Object }}
 */
async function run({ messages, sessionId, sessionContext = {} }) {
  const allTools = getToolDefinitions();
  // Smart tool selection — show only relevant tools to reduce prompt size and improve accuracy
  const tools = selectTools(messages, sessionContext, allTools);
  const systemPrompt = buildSystemPrompt(sessionContext);

  // Build the full message array with system prompt
  const fullMessages = [
    { role: "system", content: systemPrompt },
    ...messages,
  ];

  const toolsUsed = [];
  let source = "adc-self-hosted";
  let iterations = 0;
  const startTime = Date.now();

  // Analytics tracking
  const analytics = {
    toolsAvailable: tools.length,
    totalToolsInRegistry: allTools.length,
    intentsDetected: [],
    timestamp: new Date().toISOString(),
  };

  let forceProvider = null;

  while (iterations < MAX_ITERATIONS) {
    iterations++;

    const response = await providers.call(fullMessages, tools, forceProvider);
    source = response.source;

    // If vLLM returned text but tools were unavailable, and this is the first
    // iteration with a fresh question, accept the answer (vLLM is good enough
    // for most questions with the rich system prompt). The tools are a bonus.
    if (response.type === "text" && response.toolsUnavailable && iterations === 1) {
      analytics.durationMs = Date.now() - startTime;
      analytics.iterations = iterations;
      return {
        reply: response.content,
        source,
        toolsUsed,
        sessionContext,
        analytics,
      };
    }

    // If it's a text response, we're done
    if (response.type === "text") {
      analytics.durationMs = Date.now() - startTime;
      analytics.iterations = iterations;
      return {
        reply: response.content,
        source,
        toolsUsed,
        sessionContext,
        analytics,
      };
    }

    // It's a tool call — execute each tool
    if (response.type === "tool_calls") {
      // Add the assistant's tool-calling message to history
      fullMessages.push(response.rawMessage);

      for (const call of response.calls) {
        toolsUsed.push(call.name);

        // Create a context object for the tool
        const toolContext = {
          sessionId,
          sessionContext,
          ip: sessionContext._ip,
        };

        // Execute tool with job lifecycle tracking
        const jobResult = await runWithLifecycle(
          { type: "tool_call", tools: [call.name], sessionId, metadata: { timeout: 8000 } },
          () => executeTool(call.name, call.args, toolContext)
        );

        const { result, error } = jobResult.result || { result: null, error: jobResult.error };

        // Update session context from tool results
        if (call.name === "capture_lead" && !error) {
          if (call.args.name) sessionContext.visitorName = call.args.name;
          if (call.args.email) sessionContext.visitorEmail = call.args.email;
          if (call.args.phone) sessionContext.visitorPhone = call.args.phone;
          if (call.args.business_type) sessionContext.businessType = call.args.business_type;
          sessionContext.leadCaptured = true;
        }

        // Add tool result to conversation
        fullMessages.push({
          role: "tool",
          tool_call_id: call.id,
          content: error || result,
        });
      }

      // Continue the loop — LLM will see tool results and either respond or call more tools
      continue;
    }

    // Unexpected response type — break out
    break;
  }

  // If we exhausted iterations, do one final call without tools to get a text response
  const finalResponse = await providers.call(fullMessages, []);
  analytics.durationMs = Date.now() - startTime;
  analytics.iterations = iterations;
  analytics.exhaustedIterations = true;
  analytics.jobStats = getJobStats();
  return {
    reply: finalResponse.content || "I'd love to help — let me connect you with our team. Call us at (337) 486-3149 or visit ai-advantage.info.",
    source: finalResponse.source || source,
    toolsUsed,
    sessionContext,
    analytics,
  };
}

module.exports = { run };
