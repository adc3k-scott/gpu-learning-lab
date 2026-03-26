// ROXY LLM Providers — vLLM (primary) + Anthropic (fallback)
// Normalized interface so the agent loop doesn't care which backend is active.

const ADC_INFERENCE_URL =
  process.env.ADC_INFERENCE_URL ||
  "https://38df7s7h46h8u4-8000.proxy.runpod.net/v1/chat/completions";
const ADC_MODEL = process.env.ADC_MODEL || "Qwen/Qwen3-8B";
const ANTHROPIC_FALLBACK = !!process.env.ANTHROPIC_API_KEY;

// Track whether vLLM supports tool calling (tested once per cold start)
let vllmToolsSupported = null;

/**
 * Call vLLM (self-hosted, OpenAI-compatible)
 * Returns normalized response: { type: "text"|"tool_calls", content?, calls? }
 */
async function callVLLM(messages, tools) {
  const body = {
    model: ADC_MODEL,
    messages,
    max_tokens: 1024,
    temperature: 0.7,
    chat_template_kwargs: { enable_thinking: false },
  };

  // Only include tools if vLLM supports them
  if (tools && tools.length > 0 && vllmToolsSupported !== false) {
    body.tools = tools;
    body.tool_choice = "auto";
  }

  const response = await fetch(ADC_INFERENCE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  // If vLLM rejects tools, retry without them and remember for this cold start
  if (!response.ok && body.tools) {
    const errText = await response.text();
    if (errText.includes("tool-call-parser") || errText.includes("tool choice") || response.status === 400) {
      console.log("[ROXY] vLLM does not support tool calling, retrying without tools");
      vllmToolsSupported = false;
      delete body.tools;
      delete body.tool_choice;
      const retryResponse = await fetch(ADC_INFERENCE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!retryResponse.ok) {
        throw new Error(`vLLM ${retryResponse.status}: ${await retryResponse.text()}`);
      }
      const retryData = await retryResponse.json();
      const retryChoice = retryData.choices?.[0];
      if (!retryChoice) throw new Error("No response from vLLM");
      let content = retryChoice.message?.content || "";
      content = content.replace(/<think>[\s\S]*?<\/think>/g, "").trim();
      // Signal that tools were requested but not available
      return { type: "text", content, rawMessage: retryChoice.message, toolsUnavailable: true };
    }
    throw new Error(`vLLM ${response.status}: ${errText}`);
  }

  if (!response.ok) {
    throw new Error(`vLLM ${response.status}: ${await response.text()}`);
  }
  if (body.tools) vllmToolsSupported = true;

  const data = await response.json();
  const choice = data.choices?.[0];

  if (!choice) {
    throw new Error("No response from vLLM");
  }

  // Check for tool calls
  if (choice.message?.tool_calls && choice.message.tool_calls.length > 0) {
    return {
      type: "tool_calls",
      calls: choice.message.tool_calls.map((tc) => ({
        id: tc.id || `call_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        name: tc.function.name,
        args: typeof tc.function.arguments === "string"
          ? JSON.parse(tc.function.arguments)
          : tc.function.arguments,
      })),
      // Include the raw message for conversation history
      rawMessage: choice.message,
    };
  }

  // Regular text response
  let content = choice.message?.content || "";
  // Strip any <think> tags that slip through
  content = content.replace(/<think>[\s\S]*?<\/think>/g, "").trim();

  return { type: "text", content, rawMessage: choice.message };
}

/**
 * Call Anthropic Claude (fallback)
 * Returns normalized response matching vLLM format
 */
async function callAnthropic(messages, tools) {
  const Anthropic =
    require("@anthropic-ai/sdk").default || require("@anthropic-ai/sdk");
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

  // Separate system message from conversation
  const systemMsg = messages.find((m) => m.role === "system");
  const conversationMsgs = messages.filter((m) => m.role !== "system");

  // Convert OpenAI tool_calls format to Anthropic format in conversation
  const anthropicMessages = convertToAnthropicMessages(conversationMsgs);

  const params = {
    model: process.env.ANTHROPIC_MODEL || "claude-3-haiku-20240307",
    max_tokens: 1024,
    system: systemMsg?.content || "",
    messages: anthropicMessages,
  };

  // Add tools if available
  if (tools && tools.length > 0) {
    params.tools = tools.map((t) => ({
      name: t.function.name,
      description: t.function.description,
      input_schema: t.function.parameters,
    }));
  }

  const response = await client.messages.create(params);

  // Check for tool use
  const toolUseBlocks = response.content.filter((b) => b.type === "tool_use");
  if (toolUseBlocks.length > 0) {
    return {
      type: "tool_calls",
      calls: toolUseBlocks.map((tb) => ({
        id: tb.id,
        name: tb.name,
        args: tb.input,
      })),
      rawMessage: {
        role: "assistant",
        content: null,
        tool_calls: toolUseBlocks.map((tb) => ({
          id: tb.id,
          type: "function",
          function: { name: tb.name, arguments: JSON.stringify(tb.input) },
        })),
      },
      // Include any text blocks too
      textContent: response.content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join(""),
      // Store the raw Anthropic response for history reconstruction
      _anthropicContent: response.content,
    };
  }

  // Regular text
  const content = response.content
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("");

  return {
    type: "text",
    content,
    rawMessage: { role: "assistant", content },
  };
}

/** Convert OpenAI-style messages to Anthropic format */
function convertToAnthropicMessages(messages) {
  const result = [];
  for (const msg of messages) {
    if (msg.role === "assistant" && msg.tool_calls) {
      // Convert tool calls to Anthropic content blocks
      const content = [];
      if (msg.content) {
        content.push({ type: "text", text: msg.content });
      }
      for (const tc of msg.tool_calls) {
        content.push({
          type: "tool_use",
          id: tc.id,
          name: tc.function.name,
          input: typeof tc.function.arguments === "string"
            ? JSON.parse(tc.function.arguments)
            : tc.function.arguments,
        });
      }
      result.push({ role: "assistant", content });
    } else if (msg.role === "tool") {
      // Convert tool result to Anthropic format
      result.push({
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: msg.tool_call_id,
            content: msg.content,
          },
        ],
      });
    } else {
      result.push({ role: msg.role, content: msg.content });
    }
  }
  return result;
}

/**
 * Main call function — tries vLLM first, falls back to Anthropic
 * @param {Array} messages - OpenAI-format message array
 * @param {Array} tools - OpenAI-format tool definitions
 * @param {string} [forceProvider] - "vllm" or "anthropic" to force a provider
 * @returns {{ type, content?, calls?, rawMessage, source }}
 */
async function call(messages, tools, forceProvider) {
  if (forceProvider === "anthropic" || !ADC_INFERENCE_URL) {
    const result = await callAnthropic(messages, tools);
    return { ...result, source: "anthropic-fallback" };
  }

  try {
    const result = await callVLLM(messages, tools);
    return { ...result, source: "adc-self-hosted" };
  } catch (err) {
    console.error("[ROXY] vLLM failed, trying Anthropic:", err.message);
    if (ANTHROPIC_FALLBACK) {
      const result = await callAnthropic(messages, tools);
      return { ...result, source: "anthropic-fallback" };
    }
    throw err;
  }
}

module.exports = { call };
