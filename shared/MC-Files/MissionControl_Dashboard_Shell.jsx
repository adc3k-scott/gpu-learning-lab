'use client';

import { useState, useMemo } from 'react';
import { useAuth } from '@/components/AuthProvider';
import { NAV_SECTIONS, PLATFORMS, PLATFORM_LIST, GATED_ROUTES } from '@/lib/constants';
import { TierBadge } from '@/components/PlatformBadge';

export default function DashboardPage() {
  const { user, tier } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [platformFilter, setPlatformFilter] = useState('all');

  // Flatten all tools for the grid
  const allTools = useMemo(() => {
    const tools = [];
    NAV_SECTIONS.forEach((section) => {
      section.items.forEach((item) => {
        tools.push({
          ...item,
          section: section.title,
          platform: section.platform || 'universal',
          color: section.platform ? PLATFORMS[section.platform]?.color : '#8E8E9A',
        });
      });
    });
    return tools;
  }, []);

  // Filter tools
  const filteredTools = useMemo(() => {
    return allTools.filter((tool) => {
      const matchesSearch = !search ||
        tool.name.toLowerCase().includes(search.toLowerCase()) ||
        tool.section.toLowerCase().includes(search.toLowerCase());
      const matchesPlatform = platformFilter === 'all' || tool.platform === platformFilter;
      return matchesSearch && matchesPlatform;
    });
  }, [allTools, search, platformFilter]);

  return (
    <div className="min-h-screen bg-background flex">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:sticky top-0 left-0 h-screen w-64 bg-surface border-r border-border z-50 overflow-y-auto transition-transform lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Sidebar header */}
        <div className="p-4 border-b border-border flex items-center justify-between">
          <a href="/" className="flex items-center gap-2">
            <span className="text-xl">🔧</span>
            <span className="font-mono font-bold text-sm">MISSION CONTROL</span>
          </a>
          <button onClick={() => setSidebarOpen(false)} className="lg:hidden text-text-muted hover:text-text-primary">
            ✕
          </button>
        </div>

        {/* Nav sections */}
        <nav className="p-3">
          {NAV_SECTIONS.map((section, i) => (
            <div key={i} className="mb-4">
              <h3
                className="text-xs font-bold uppercase tracking-wider mb-2 px-2"
                style={{ color: section.platform ? PLATFORMS[section.platform]?.color : '#6B6B76' }}
              >
                {section.title}
              </h3>
              <div className="space-y-0.5">
                {section.items.map((item, j) => (
                  <a
                    key={j}
                    href={item.route}
                    className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-text-muted hover:text-text-primary hover:bg-background transition-colors group"
                  >
                    <span className="text-base w-5 text-center">{item.icon}</span>
                    <span className="flex-1 truncate">{item.name}</span>
                    {item.gate === 'pro' && (
                      <span className="text-[10px] font-bold text-pro bg-pro/15 px-1.5 py-0.5 rounded">PRO</span>
                    )}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {/* Sidebar footer */}
        <div className="p-4 border-t border-border mt-auto">
          {user ? (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-harley/20 flex items-center justify-center text-harley text-sm font-bold">
                {user.email?.charAt(0).toUpperCase() || '?'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm truncate">{user.email}</p>
                <TierBadge tier={tier} size="sm" />
              </div>
            </div>
          ) : (
            <a href="/login" className="mc-btn-primary w-full text-center block text-sm">
              Sign In
            </a>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 min-w-0">
        {/* Top bar */}
        <header className="sticky top-0 bg-background/80 backdrop-blur-md border-b border-border z-30 px-4 lg:px-6 h-14 flex items-center gap-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden text-text-muted hover:text-text-primary"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Search */}
          <div className="flex-1 max-w-md relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-faint">🔍</span>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search 41 tools..."
              className="mc-input pl-9 py-1.5 text-sm"
            />
          </div>

          {/* Quick links */}
          <div className="hidden md:flex items-center gap-2">
            <a href="/ai-chat" className="mc-btn-ghost text-xs">🤖 AI Chat</a>
            <a href="/garage" className="mc-btn-ghost text-xs">🏠 Garage</a>
            <a href="/account" className="mc-btn-ghost text-xs">⚙️ Account</a>
          </div>
        </header>

        <div className="p-4 lg:p-6">
          {/* Welcome */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold mb-1">Dashboard</h1>
            <p className="text-text-muted text-sm">
              {filteredTools.length} tool{filteredTools.length !== 1 ? 's' : ''} available
              {search && ` matching "${search}"`}
              {platformFilter !== 'all' && ` in ${PLATFORMS[platformFilter]?.name || platformFilter}`}
            </p>
          </div>

          {/* Platform filter pills */}
          <div className="flex flex-wrap gap-2 mb-6">
            <button
              onClick={() => setPlatformFilter('all')}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                platformFilter === 'all'
                  ? 'bg-text-primary text-background'
                  : 'bg-surface text-text-muted border border-border hover:text-text-primary'
              }`}
            >
              All Platforms
            </button>
            {PLATFORM_LIST.map((p) => (
              <button
                key={p.id}
                onClick={() => setPlatformFilter(p.id)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                  platformFilter === p.id
                    ? 'text-white'
                    : 'bg-surface text-text-muted border border-border hover:text-text-primary'
                }`}
                style={platformFilter === p.id ? { backgroundColor: p.color } : {}}
              >
                {p.icon} {p.shortName}
              </button>
            ))}
          </div>

          {/* Tool Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredTools.map((tool, i) => {
              const isGated = GATED_ROUTES[tool.route];
              return (
                <a
                  key={i}
                  href={tool.route}
                  className="mc-card-hover p-4 group relative"
                  style={{ borderLeftColor: tool.color, borderLeftWidth: '3px' }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-2xl">{tool.icon}</span>
                    {isGated && (
                      <span className="text-[10px] font-bold text-pro bg-pro/15 px-1.5 py-0.5 rounded uppercase">
                        {isGated}
                      </span>
                    )}
                  </div>
                  <h3 className="font-semibold text-sm mb-1 group-hover:text-harley transition-colors">
                    {tool.name}
                  </h3>
                  <p className="text-text-dim text-xs">{tool.section}</p>
                </a>
              );
            })}
          </div>

          {filteredTools.length === 0 && (
            <div className="text-center py-16">
              <span className="text-4xl mb-4 block">🔍</span>
              <h3 className="text-lg font-bold mb-2">No tools found</h3>
              <p className="text-text-muted text-sm">Try a different search term or platform filter.</p>
            </div>
          )}

          {/* AI Chat Promo */}
          <div className="mt-8 mc-card p-6 bg-gradient-to-r from-surface to-harley/5 border-harley/20">
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="text-5xl">🤖</div>
              <div className="flex-1">
                <h3 className="text-lg font-bold mb-1">AI Diagnostic Chat</h3>
                <p className="text-text-muted text-sm">
                  Can&apos;t find what you need? Describe your issue in plain English and get expert guidance
                  from our AI — trained on all 5 platforms.
                </p>
              </div>
              <a href="/ai-chat" className="mc-btn-primary whitespace-nowrap">
                Open AI Chat →
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
