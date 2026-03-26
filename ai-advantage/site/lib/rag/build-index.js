#!/usr/bin/env node
// ROXY RAG — Playbook Index Builder
// Reads all playbook markdown files, chunks them by section, builds a keyword index.
// Run: node lib/rag/build-index.js

const fs = require("fs");
const path = require("path");

const PLAYBOOK_DIR = path.resolve(__dirname, "../../../playbooks");
const CORE_DOCS = [
  path.resolve(__dirname, "../../../ally-prompt.md"),
  path.resolve(__dirname, "../../../client-process.md"),
  path.resolve(__dirname, "../../../README.md"),
];
const OUTPUT_PATH = path.join(__dirname, "playbook-index.json");

// Simple stop words list
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

function extractIndustryTag(filename) {
  const name = path.basename(filename, ".md");
  return name.replace(/-/g, " ");
}

function chunkMarkdown(content, filename) {
  const chunks = [];
  const lines = content.split("\n");
  let currentSection = "";
  let currentContent = [];
  let sectionDepth = 0;

  for (const line of lines) {
    const headerMatch = line.match(/^(#{1,3})\s+(.+)/);
    if (headerMatch && currentContent.length > 0) {
      // Save previous section
      const text = currentContent.join("\n").trim();
      if (text.length > 50) {
        chunks.push({
          section: currentSection,
          content: text,
          file: path.basename(filename),
          industry: extractIndustryTag(filename),
        });
      }
      currentContent = [];
    }
    if (headerMatch) {
      currentSection = headerMatch[2].trim();
      sectionDepth = headerMatch[1].length;
    }
    currentContent.push(line);
  }

  // Don't forget the last section
  const text = currentContent.join("\n").trim();
  if (text.length > 50) {
    chunks.push({
      section: currentSection,
      content: text,
      file: path.basename(filename),
      industry: extractIndustryTag(filename),
    });
  }

  return chunks;
}

function buildIndex() {
  const allChunks = [];
  const invertedIndex = {};

  // Process playbooks
  if (fs.existsSync(PLAYBOOK_DIR)) {
    const files = fs.readdirSync(PLAYBOOK_DIR).filter((f) => f.endsWith(".md"));
    for (const file of files) {
      const content = fs.readFileSync(path.join(PLAYBOOK_DIR, file), "utf-8");
      const chunks = chunkMarkdown(content, file);
      allChunks.push(...chunks);
    }
  }

  // Process core docs
  for (const docPath of CORE_DOCS) {
    if (fs.existsSync(docPath)) {
      const content = fs.readFileSync(docPath, "utf-8");
      const chunks = chunkMarkdown(content, docPath);
      allChunks.push(...chunks);
    }
  }

  // Assign IDs
  allChunks.forEach((chunk, i) => {
    chunk.id = i;
  });

  // Build inverted index
  for (const chunk of allChunks) {
    const allText = `${chunk.section} ${chunk.content} ${chunk.industry}`;
    const tokens = tokenize(allText);
    const tokenSet = new Set(tokens); // Deduplicate per chunk

    for (const token of tokenSet) {
      if (!invertedIndex[token]) {
        invertedIndex[token] = [];
      }
      invertedIndex[token].push(chunk.id);
    }
  }

  const index = {
    chunks: allChunks.map((c) => ({
      id: c.id,
      section: c.section,
      content: c.content,
      file: c.file,
      industry: c.industry,
    })),
    invertedIndex,
    buildTime: new Date().toISOString(),
    stats: {
      totalChunks: allChunks.length,
      totalTerms: Object.keys(invertedIndex).length,
      playbooks: [...new Set(allChunks.map((c) => c.file))],
    },
  };

  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(index));

  console.log(`ROXY RAG Index Built:`);
  console.log(`  Chunks: ${index.stats.totalChunks}`);
  console.log(`  Terms: ${index.stats.totalTerms}`);
  console.log(`  Files: ${index.stats.playbooks.length}`);
  console.log(`  Output: ${OUTPUT_PATH}`);
  console.log(`  Size: ${(fs.statSync(OUTPUT_PATH).size / 1024).toFixed(1)} KB`);

  return index;
}

// Run if called directly
if (require.main === module) {
  buildIndex();
}

module.exports = { buildIndex };
