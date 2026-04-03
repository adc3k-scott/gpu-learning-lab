'use client';

export function PageSkeleton() {
  return (
    <div className="min-h-screen bg-background p-6 animate-fade-in">
      {/* Header */}
      <div className="mc-skeleton h-8 w-64 mb-2" />
      <div className="mc-skeleton h-4 w-96 mb-8" />

      {/* Content grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="mc-card p-6 space-y-4">
            <div className="mc-skeleton h-6 w-3/4" />
            <div className="mc-skeleton h-4 w-full" />
            <div className="mc-skeleton h-4 w-5/6" />
            <div className="mc-skeleton h-10 w-32 rounded-mc" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function CardsSkeleton({ count = 4 }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="mc-card p-6 space-y-3">
          <div className="flex items-center gap-3">
            <div className="mc-skeleton h-10 w-10 rounded-full" />
            <div className="space-y-2 flex-1">
              <div className="mc-skeleton h-4 w-1/2" />
              <div className="mc-skeleton h-3 w-1/3" />
            </div>
          </div>
          <div className="mc-skeleton h-4 w-full" />
          <div className="mc-skeleton h-4 w-4/5" />
        </div>
      ))}
    </div>
  );
}

export function TableSkeleton({ rows = 5 }) {
  return (
    <div className="mc-card overflow-hidden">
      {/* Table header */}
      <div className="flex gap-4 p-4 border-b border-border">
        <div className="mc-skeleton h-4 w-1/4" />
        <div className="mc-skeleton h-4 w-1/4" />
        <div className="mc-skeleton h-4 w-1/4" />
        <div className="mc-skeleton h-4 w-1/4" />
      </div>
      {/* Table rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 p-4 border-b border-border last:border-0">
          <div className="mc-skeleton h-4 w-1/4" />
          <div className="mc-skeleton h-4 w-1/4" />
          <div className="mc-skeleton h-4 w-1/4" />
          <div className="mc-skeleton h-4 w-1/4" />
        </div>
      ))}
    </div>
  );
}

export function LineSkeleton({ lines = 4 }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="mc-skeleton h-4"
          style={{ width: `${70 + Math.random() * 30}%` }}
        />
      ))}
    </div>
  );
}

export default function LoadingSkeleton({ variant = 'page', ...props }) {
  switch (variant) {
    case 'cards':
      return <CardsSkeleton {...props} />;
    case 'table':
      return <TableSkeleton {...props} />;
    case 'lines':
      return <LineSkeleton {...props} />;
    default:
      return <PageSkeleton {...props} />;
  }
}
