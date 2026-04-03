'use client';

import { PLATFORM_LIST } from '@/lib/constants';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="text-center max-w-lg">
        <h1 className="text-8xl font-bold mb-4 text-gradient-brand">404</h1>
        <h2 className="text-2xl font-bold mb-3">Page Not Found</h2>
        <p className="text-text-muted mb-8">
          The page you&apos;re looking for doesn&apos;t exist or has been moved. 
          Let&apos;s get you back on track.
        </p>

        <div className="flex flex-col sm:flex-row gap-3 justify-center mb-10">
          <a href="/" className="mc-btn-primary">Go Home</a>
          <a href="/dashboard" className="mc-btn-secondary">Open Dashboard</a>
        </div>

        <div>
          <p className="text-text-dim text-sm mb-4">Or jump to a platform:</p>
          <div className="flex flex-wrap justify-center gap-2">
            {PLATFORM_LIST.map((p) => (
              <a
                key={p.id}
                href={p.route}
                className="px-3 py-1.5 rounded-full text-xs font-medium bg-surface border border-border text-text-muted hover:text-white transition-all"
                style={{ '--hover-bg': p.color }}
                onMouseEnter={(e) => { e.target.style.backgroundColor = p.color; e.target.style.borderColor = p.color; }}
                onMouseLeave={(e) => { e.target.style.backgroundColor = ''; e.target.style.borderColor = ''; }}
              >
                {p.icon} {p.shortName}
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
