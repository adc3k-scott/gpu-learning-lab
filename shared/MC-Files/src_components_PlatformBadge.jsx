'use client';

import { PLATFORMS } from '@/lib/constants';

const sizeClasses = {
  sm: 'text-xs px-1.5 py-0.5',
  md: 'text-xs px-2 py-0.5',
  lg: 'text-sm px-2.5 py-1',
};

export function PlatformBadge({ platform, size = 'md' }) {
  const p = PLATFORMS[platform];
  if (!p) return null;

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full font-medium ${sizeClasses[size]}`}
      style={{
        backgroundColor: `${p.color}15`,
        color: p.color,
      }}
    >
      <span>{p.icon}</span>
      <span>{p.shortName}</span>
    </span>
  );
}

export function TierBadge({ tier, size = 'md' }) {
  const config = {
    free: { label: 'FREE', color: '#8E8E9A', bg: 'rgba(142, 142, 154, 0.15)' },
    premium: { label: 'PREMIUM', color: '#8B5CF6', bg: 'rgba(139, 92, 246, 0.15)' },
    pro: { label: 'PRO', color: '#F59E0B', bg: 'rgba(245, 158, 11, 0.15)' },
  };

  const t = config[tier] || config.free;

  return (
    <span
      className={`inline-flex items-center rounded-full font-bold tracking-wider ${sizeClasses[size]}`}
      style={{ backgroundColor: t.bg, color: t.color }}
    >
      {t.label}
    </span>
  );
}
