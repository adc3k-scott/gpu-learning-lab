'use client';

import { useEffect } from 'react';

export default function Error({ error, reset }) {
  useEffect(() => {
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="w-16 h-16 rounded-full bg-danger/10 flex items-center justify-center mx-auto mb-6">
          <span className="text-3xl">⚠️</span>
        </div>
        <h2 className="text-2xl font-bold mb-3">Something Went Wrong</h2>
        <p className="text-text-muted mb-8">
          An unexpected error occurred. This has been logged and we&apos;ll look into it.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button onClick={() => reset()} className="mc-btn-primary">
            Try Again
          </button>
          <a href="/dashboard" className="mc-btn-secondary">
            Go to Dashboard
          </a>
        </div>
      </div>
    </div>
  );
}
