'use client';

import { useState } from 'react';
import { useAuth } from '@/components/AuthProvider';
import { hasTierAccess } from '@/lib/supabase';

export default function ProGate({ requiredTier = 'pro', featureName = 'This feature', children }) {
  const { tier, user } = useAuth();
  const [showModal, setShowModal] = useState(false);

  // If user has access, render children normally
  if (hasTierAccess(tier, requiredTier)) {
    return children;
  }

  const tierLabel = requiredTier === 'pro' ? 'Pro' : 'Premium';
  const tierColor = requiredTier === 'pro' ? '#F59E0B' : '#8B5CF6';
  const price = requiredTier === 'pro' ? '$19.99' : '$9.99';

  return (
    <div className="relative">
      {/* Blurred preview of the actual content */}
      <div className="blur-sm pointer-events-none select-none opacity-50">
        {children}
      </div>

      {/* Lock overlay */}
      <div className="absolute inset-0 flex items-center justify-center bg-background/60 backdrop-blur-sm rounded-mc">
        <div className="text-center p-8 max-w-md">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            style={{ backgroundColor: `${tierColor}20` }}
          >
            <svg className="w-8 h-8" fill={tierColor} viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                clipRule="evenodd"
              />
            </svg>
          </div>

          <h3 className="text-xl font-bold text-text-primary mb-2">
            {tierLabel} Feature
          </h3>
          <p className="text-text-muted mb-6">
            {featureName} requires a {tierLabel} subscription. Upgrade to unlock this and more.
          </p>

          <button
            onClick={() => setShowModal(true)}
            className="mc-btn text-white font-semibold px-6 py-3"
            style={{ backgroundColor: tierColor }}
          >
            Upgrade to {tierLabel} — {price}/mo
          </button>

          {!user && (
            <p className="text-text-dim text-sm mt-4">
              <a href="/login" className="text-harley hover:underline">
                Sign in
              </a>{' '}
              to check your current plan.
            </p>
          )}
        </div>
      </div>

      {/* Upgrade Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
          <div className="mc-card max-w-lg w-full mx-4 p-8">
            <div className="flex justify-between items-start mb-6">
              <h2 className="text-2xl font-bold">
                Upgrade to <span style={{ color: tierColor }}>{tierLabel}</span>
              </h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-text-muted hover:text-text-primary text-2xl leading-none"
              >
                &times;
              </button>
            </div>

            <div className="space-y-3 mb-8">
              {requiredTier === 'pro' ? (
                <>
                  <Feature text="Unlimited AI Diagnostic Chat" />
                  <Feature text="Unlimited vehicles in garage" />
                  <Feature text="Wiring diagrams (Harley + E-Bike)" />
                  <Feature text="Torque sequences" />
                  <Feature text="Service history export" />
                  <Feature text="PRO forum badge" />
                </>
              ) : (
                <>
                  <Feature text="20 AI queries per day" />
                  <Feature text="3 vehicles in garage" />
                  <Feature text="Morning brief emails" />
                  <Feature text="PREMIUM forum badge" />
                  <Feature text="7-day free trial" />
                </>
              )}
            </div>

            <div className="flex gap-3">
              <a
                href="/pricing"
                className="mc-btn text-white font-semibold px-6 py-3 flex-1 text-center"
                style={{ backgroundColor: tierColor }}
              >
                View Pricing
              </a>
              <button
                onClick={() => setShowModal(false)}
                className="mc-btn-secondary flex-1"
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Feature({ text }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-ebike">✓</span>
      <span className="text-text-secondary">{text}</span>
    </div>
  );
}
