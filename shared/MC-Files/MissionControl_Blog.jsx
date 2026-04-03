'use client';

import { useState } from 'react';
import { PLATFORMS, PLATFORM_LIST } from '@/lib/constants';

const ARTICLES = [
  { id: 1, title: 'What Does P0131 Mean on a Harley-Davidson?', excerpt: 'A complete guide to diagnosing the P0131 oxygen sensor code on Harley-Davidson motorcycles.', platform: 'harley', date: '2026-02-23', readTime: '5 min', featured: true, content: 'The P0131 code indicates a low voltage condition on the oxygen sensor circuit (Bank 1, Sensor 1). On Harley-Davidson motorcycles, this often points to a faulty O2 sensor, wiring issues, or exhaust leaks near the sensor...' },
  { id: 2, title: 'Free HOS Tracker for CDL Drivers', excerpt: 'How to stay FMCSA compliant with our free Hours of Service tracking tool.', platform: 'trucking', date: '2026-02-24', readTime: '4 min', featured: true, content: 'Hours of Service compliance is critical for CDL drivers. Our free HOS tracker helps you monitor drive time, on-duty time, and required breaks according to current FMCSA regulations...' },
  { id: 3, title: 'E-Bike Battery Health: How to Check & Maintain', excerpt: 'Everything you need to know about monitoring your e-bike battery condition.', platform: 'ebike', date: '2026-02-25', readTime: '6 min', content: 'Your e-bike battery is the most expensive component. Learn how to check voltage, capacity, and cell balance to maximize your battery lifespan...' },
  { id: 4, title: 'OBD-II Codes Explained for Beginners', excerpt: 'A plain-English guide to understanding what your check engine light is trying to tell you.', platform: 'auto', date: '2026-02-26', readTime: '7 min', content: 'OBD-II (On-Board Diagnostics) codes are standardized across all vehicles sold in the US since 1996. When your check engine light comes on, these codes help identify what system is having issues...' },
  { id: 5, title: 'The Complete Pre-Trip Inspection Checklist', excerpt: 'A step-by-step CDL pre-trip inspection guide that covers every DOT requirement.', platform: 'trucking', date: '2026-02-27', readTime: '8 min', content: 'A thorough pre-trip inspection is your first line of defense against breakdowns and DOT violations. This checklist covers every item required by federal regulations...' },
  { id: 6, title: 'Harley-Davidson Service Intervals by Model', excerpt: 'Complete maintenance schedule for Sportster, Softail, Touring, and more.', platform: 'harley', date: '2026-02-20', readTime: '5 min', content: 'Regular maintenance keeps your Harley running strong. Here are the recommended service intervals for each model family...' },
  { id: 7, title: 'Electric Scooter Tire Maintenance Guide', excerpt: 'When to replace tires, how to check pressure, and solid vs pneumatic options.', platform: 'scooter', date: '2026-02-19', readTime: '4 min', content: 'Tire maintenance is one of the most overlooked aspects of electric scooter ownership. Proper tire care improves safety, range, and ride quality...' },
  { id: 8, title: 'Understanding E-Bike Classifications', excerpt: 'Class 1, 2, and 3 explained — plus state-by-state legal differences.', platform: 'ebike', date: '2026-02-18', readTime: '5 min', content: 'E-bike classification determines where you can ride and how fast your bike can go. Understanding these classes is essential for legal compliance...' },
  { id: 9, title: 'Top 5 Most Common Check Engine Codes', excerpt: 'The five OBD-II codes mechanics see most often and what they really mean.', platform: 'auto', date: '2026-02-17', readTime: '6 min', content: 'Some check engine codes appear far more frequently than others. Here are the top five most common codes and practical guidance for each...' },
  { id: 10, title: 'IFTA Reporting Made Simple', excerpt: 'A trucker-friendly guide to International Fuel Tax Agreement reporting.', platform: 'trucking', date: '2026-02-16', readTime: '5 min', content: 'IFTA reporting doesn\'t have to be complicated. This guide breaks down exactly what you need to track and when to file...' },
];

export default function BlogPage() {
  const [search, setSearch] = useState('');
  const [platformFilter, setPlatformFilter] = useState('all');
  const [selectedArticle, setSelectedArticle] = useState(null);

  const filtered = ARTICLES.filter((a) => {
    const matchesSearch = !search || a.title.toLowerCase().includes(search.toLowerCase()) || a.excerpt.toLowerCase().includes(search.toLowerCase());
    const matchesPlatform = platformFilter === 'all' || a.platform === platformFilter;
    return matchesSearch && matchesPlatform;
  });

  if (selectedArticle) {
    return (
      <div className="min-h-screen bg-background">
        <header className="border-b border-border px-4 py-3">
          <div className="max-w-3xl mx-auto">
            <button onClick={() => setSelectedArticle(null)} className="text-text-muted hover:text-text-primary text-sm">
              ← Back to Blog
            </button>
          </div>
        </header>
        <article className="max-w-3xl mx-auto px-4 py-12">
          <div className="mb-6">
            <span className="mc-badge" style={{ backgroundColor: PLATFORMS[selectedArticle.platform]?.color + '20', color: PLATFORMS[selectedArticle.platform]?.color }}>
              {PLATFORMS[selectedArticle.platform]?.icon} {PLATFORMS[selectedArticle.platform]?.shortName}
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold mb-4">{selectedArticle.title}</h1>
          <div className="flex items-center gap-4 text-text-muted text-sm mb-8">
            <span>{selectedArticle.date}</span>
            <span>·</span>
            <span>{selectedArticle.readTime} read</span>
          </div>
          <div className="prose prose-invert max-w-none text-text-secondary leading-relaxed text-lg" style={{ fontFamily: 'Georgia, serif' }}>
            <p className="text-xl text-text-primary mb-6">{selectedArticle.excerpt}</p>
            <p>{selectedArticle.content}</p>
            <div className="mc-card p-6 my-8 bg-harley/5 border-harley/20">
              <h3 className="font-bold mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>🤖 Need more help?</h3>
              <p className="text-sm mb-3">Ask our AI Diagnostic Chat for personalized guidance.</p>
              <a href="/ai-chat" className="mc-btn-primary text-sm inline-block">Open AI Chat →</a>
            </div>
          </div>
        </article>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
            <span className="text-border">|</span>
            <h1 className="font-bold text-lg">📝 Blog</h1>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Search & Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search articles..." className="mc-input flex-1" />
          <div className="flex gap-2 flex-wrap">
            <button onClick={() => setPlatformFilter('all')} className={`px-3 py-1.5 rounded-full text-xs font-medium ${platformFilter === 'all' ? 'bg-text-primary text-background' : 'bg-surface text-text-muted border border-border'}`}>All</button>
            {PLATFORM_LIST.map((p) => (
              <button key={p.id} onClick={() => setPlatformFilter(p.id)} className={`px-3 py-1.5 rounded-full text-xs font-medium ${platformFilter === p.id ? 'text-white' : 'bg-surface text-text-muted border border-border'}`} style={platformFilter === p.id ? { backgroundColor: p.color } : {}}>
                {p.icon} {p.shortName}
              </button>
            ))}
          </div>
        </div>

        {/* Featured */}
        {platformFilter === 'all' && !search && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
            {ARTICLES.filter((a) => a.featured).map((article) => (
              <button key={article.id} onClick={() => setSelectedArticle(article)} className="mc-card-hover p-6 text-left">
                <span className="mc-badge mb-3" style={{ backgroundColor: PLATFORMS[article.platform]?.color + '20', color: PLATFORMS[article.platform]?.color }}>
                  {PLATFORMS[article.platform]?.shortName}
                </span>
                <h2 className="text-xl font-bold mb-2">{article.title}</h2>
                <p className="text-text-muted text-sm mb-3">{article.excerpt}</p>
                <div className="text-text-dim text-xs">{article.date} · {article.readTime}</div>
              </button>
            ))}
          </div>
        )}

        {/* All articles */}
        <div className="space-y-4">
          {filtered.map((article) => (
            <button key={article.id} onClick={() => setSelectedArticle(article)} className="mc-card-hover p-4 w-full text-left flex items-center gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs" style={{ color: PLATFORMS[article.platform]?.color }}>{PLATFORMS[article.platform]?.icon} {PLATFORMS[article.platform]?.shortName}</span>
                  <span className="text-text-faint text-xs">· {article.readTime}</span>
                </div>
                <h3 className="font-semibold mb-1">{article.title}</h3>
                <p className="text-text-muted text-sm">{article.excerpt}</p>
              </div>
              <span className="text-text-faint hidden sm:block">→</span>
            </button>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-16">
            <p className="text-text-muted">No articles found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  );
}
