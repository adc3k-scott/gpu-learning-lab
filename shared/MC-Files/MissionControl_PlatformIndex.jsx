'use client';

import { usePathname } from 'next/navigation';
import { PLATFORMS, NAV_SECTIONS, GATED_ROUTES } from '@/lib/constants';

export default function PlatformIndexPage() {
  const pathname = usePathname();
  const platformId = pathname.split('/')[1];
  const platform = PLATFORMS[platformId];

  if (!platform) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-text-muted">Platform not found.</p>
      </div>
    );
  }

  const section = NAV_SECTIONS.find((s) => s.platform === platformId);
  const tools = section?.items || [];

  const stats = [
    { label: 'Tools', value: platform.toolCount },
    { label: 'Free', value: tools.filter((t) => !t.gate).length },
    { label: 'PRO', value: tools.filter((t) => t.gate === 'pro').length },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
          <span className="text-border">|</span>
          <span className="font-bold" style={{ color: platform.color }}>{platform.icon} {platform.name}</span>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero */}
        <div className="text-center mb-12">
          <span className="text-6xl block mb-4">{platform.icon}</span>
          <h1 className="text-3xl md:text-4xl font-bold mb-3">
            <span style={{ color: platform.color }}>{platform.name}</span> Tools
          </h1>
          <p className="text-text-muted max-w-lg mx-auto">{platform.description}</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-12 max-w-sm mx-auto">
          {stats.map((stat, i) => (
            <div key={i} className="mc-card p-4 text-center">
              <p className="text-2xl font-bold" style={{ color: platform.color }}>{stat.value}</p>
              <p className="text-text-dim text-xs">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Tool List */}
        <div className="space-y-3 mb-12">
          {tools.map((tool, i) => {
            const isGated = tool.gate === 'pro';
            return (
              <a
                key={i}
                href={tool.route}
                className="mc-card-hover p-4 flex items-center gap-4 group"
              >
                <span className="text-2xl w-10 text-center">{tool.icon}</span>
                <div className="flex-1">
                  <h3 className="font-semibold group-hover:text-harley transition-colors">{tool.name}</h3>
                </div>
                <div className="flex items-center gap-2">
                  {isGated ? (
                    <span className="text-[10px] font-bold text-pro bg-pro/15 px-2 py-0.5 rounded">PRO</span>
                  ) : (
                    <span className="text-[10px] font-bold text-ebike bg-ebike/15 px-2 py-0.5 rounded">FREE</span>
                  )}
                  <span className="text-text-faint group-hover:text-text-muted transition-colors">→</span>
                </div>
              </a>
            );
          })}
        </div>

        {/* AI Chat Promo */}
        <div className="mc-card p-8 text-center" style={{ borderColor: platform.color + '40' }}>
          <span className="text-4xl block mb-3">🤖</span>
          <h2 className="text-xl font-bold mb-2">
            Need help with your <span style={{ color: platform.color }}>{platform.shortName}</span>?
          </h2>
          <p className="text-text-muted mb-6 max-w-md mx-auto">
            Our AI diagnostic chat is trained specifically on {platform.name.toLowerCase()} issues.
            Describe your problem in plain English.
          </p>
          <a
            href="/ai-chat"
            className="mc-btn text-white inline-block"
            style={{ backgroundColor: platform.color }}
          >
            Open {platform.shortName} AI Chat →
          </a>
        </div>
      </div>
    </div>
  );
}
