// ROXY Tool: Playbook RAG
// Searches the pre-built playbook knowledge base for industry-specific answers

// Load index via require() so Vercel's nft bundler traces it
let _index = null;

function getIndex() {
  if (!_index) {
    try {
      _index = require("../rag/playbook-index.json");
    } catch (err) {
      console.error("[ROXY RAG] Failed to load index:", err.message);
      _index = { chunks: [], invertedIndex: {} };
    }
  }
  return _index;
}

// Stop words (matching build-index.js)
const STOP_WORDS = new Set([
  "a","an","the","and","or","but","in","on","at","to","for","of","with","by",
  "is","are","was","were","be","been","being","have","has","had","do","does",
  "did","will","would","could","should","may","might","can","shall","not",
  "no","this","that","these","those","it","its","you","your","we","our",
  "they","their","from","as","if","then","than","so","just","also","very",
  "about","up","out","how","what","when","where","who","which","all","each",
  "every","any","both","few","more","most","some","such","only","own","same",
]);

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2 && !STOP_WORDS.has(w));
}

function search(query, industry, topK = 3) {
  const index = getIndex();
  const tokens = tokenize(query);

  if (tokens.length === 0) return [];

  // Score each chunk
  const scores = new Map();
  for (const token of tokens) {
    const chunkIds = index.invertedIndex[token] || [];
    for (const id of chunkIds) {
      scores.set(id, (scores.get(id) || 0) + 1);
    }
  }

  // Boost chunks matching the industry filter
  if (industry) {
    const industryTokens = tokenize(industry);
    for (const [id, score] of scores) {
      const chunk = index.chunks[id];
      if (chunk) {
        const chunkIndustry = chunk.industry.toLowerCase();
        for (const it of industryTokens) {
          if (chunkIndustry.includes(it)) {
            scores.set(id, score + 3); // Industry match = strong boost
          }
        }
      }
    }
  }

  // Sort by score, take top K
  const ranked = Array.from(scores.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK);

  return ranked.map(([id]) => index.chunks[id]).filter(Boolean);
}

module.exports = {
  name: "search_playbooks",
  description:
    "Search AI Advantage's industry playbooks for detailed information about features, installation steps, use cases, and capabilities for a specific industry or topic.",
  parameters: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "What to search for (e.g., 'HIPAA compliance for dental office', 'how does AI phone answering work')",
      },
      industry: {
        type: "string",
        description: "Optional industry filter (e.g., 'medical', 'law firm', 'restaurant', 'field services')",
      },
    },
    required: ["query"],
  },
  async execute(args) {
    const results = search(args.query, args.industry);

    if (results.length === 0) {
      return "No specific playbook information found for that query. Answer based on general AI Advantage knowledge.";
    }

    const formatted = results
      .map(
        (r) =>
          `[${r.file} — ${r.section}]\n${r.content.slice(0, 800)}`
      )
      .join("\n\n---\n\n");

    return formatted;
  },
};
