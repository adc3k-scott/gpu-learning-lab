'use client';

import { useState } from 'react';
import { UNIVERSAL_TOOLS } from '@/lib/constants';

export default function UniversalToolsPage() {
  const [search, setSearch] = useState('');

  const filtered = UNIVERSAL_TOOLS.filter((t) =>
    !search || t.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
          <span className="text-border">|</span>
          <h1 className="font-bold">🔧 Universal Tools</h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold mb-3">Universal Tools</h2>
          <p className="text-text-muted max-w-lg mx-auto">
            Tools that work across all vehicle types. Converters, calculators, guides, and more.
          </p>
        </div>

        <div className="max-w-md mx-auto mb-8">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search tools..."
            className="mc-input"
          />
        </div>

        <div className="space-y-3">
          {filtered.map((tool) => (
            <a
              key={tool.id}
              href={tool.route}
              className="mc-card-hover p-4 flex items-center gap-4 group"
            >
              <span className="text-2xl w-10 text-center">{tool.icon}</span>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold group-hover:text-harley transition-colors">{tool.name}</h3>
                  {tool.badge && (
                    <span className="text-[10px] font-bold text-auto bg-auto/15 px-2 py-0.5 rounded">{tool.badge}</span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {tool.gate === 'pro' ? (
                  <span className="text-[10px] font-bold text-pro bg-pro/15 px-2 py-0.5 rounded">PRO</span>
                ) : (
                  <span className="text-[10px] font-bold text-ebike bg-ebike/15 px-2 py-0.5 rounded">FREE</span>
                )}
                <span className="text-text-faint group-hover:text-text-muted transition-colors">→</span>
              </div>
            </a>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-12">
            <p className="text-text-muted">No tools match your search.</p>
          </div>
        )}
      </div>
    </div>
  );
}
