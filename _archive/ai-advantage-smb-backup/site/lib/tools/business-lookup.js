// ROXY Subagent: Business Lookup
// Searches for a visitor's business to personalize the conversation.
// Uses Google Custom Search API or falls back to basic domain check.

const GOOGLE_API_KEY = process.env.GOOGLE_SEARCH_API_KEY;
const GOOGLE_CX = process.env.GOOGLE_SEARCH_CX;

module.exports = {
  name: "business_lookup",
  description:
    "Look up information about a visitor's business by name and/or location. Returns basic business details like what they do, where they're located, and any public info. Use this when a visitor mentions their business name to personalize the conversation.",
  parameters: {
    type: "object",
    properties: {
      business_name: {
        type: "string",
        description: "The name of the business (e.g., 'Bayou Bistro', 'Acadiana Cooling')",
      },
      location: {
        type: "string",
        description: "City or area (e.g., 'Lafayette', 'Baton Rouge')",
      },
      website: {
        type: "string",
        description: "Business website URL if mentioned",
      },
    },
    required: ["business_name"],
  },
  async execute(args) {
    const results = {
      business_name: args.business_name,
      location: args.location || null,
    };

    // If they gave us a website, try to fetch basic info
    if (args.website) {
      try {
        const url = args.website.startsWith("http") ? args.website : `https://${args.website}`;
        const response = await fetch(url, {
          headers: { "User-Agent": "ROXY-AI-Advantage/1.0" },
          redirect: "follow",
        });
        if (response.ok) {
          const html = await response.text();
          // Extract title
          const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
          if (titleMatch) results.website_title = titleMatch[1].trim();
          // Extract meta description
          const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i);
          if (descMatch) results.website_description = descMatch[1].trim();
          results.website = url;
          results.website_reachable = true;
        }
      } catch (err) {
        results.website_reachable = false;
      }
    }

    // Try Google Custom Search if configured
    if (GOOGLE_API_KEY && GOOGLE_CX) {
      try {
        const query = args.location
          ? `${args.business_name} ${args.location}`
          : args.business_name;
        const url = `https://www.googleapis.com/customsearch/v1?key=${GOOGLE_API_KEY}&cx=${GOOGLE_CX}&q=${encodeURIComponent(query)}&num=3`;
        const response = await fetch(url, { headers: { Accept: "application/json" } });
        if (response.ok) {
          const data = await response.json();
          const items = data.items || [];
          if (items.length > 0) {
            results.search_results = items.slice(0, 3).map((item) => ({
              title: item.title,
              snippet: item.snippet,
              link: item.link,
            }));
            // Try to extract useful info from snippets
            const allSnippets = items.map((i) => i.snippet).join(" ");
            results.summary = allSnippets.slice(0, 500);
          }
        }
      } catch (err) {
        // Search failed, continue without it
      }
    }

    // If no search API, provide guidance based on what we know
    if (!results.search_results && !results.website_title) {
      results.note = `No search API configured. Use the business name "${args.business_name}"${args.location ? ` in ${args.location}` : ""} to personalize your response. Ask about their specific needs rather than assuming.`;
    }

    return JSON.stringify(results);
  },
};
