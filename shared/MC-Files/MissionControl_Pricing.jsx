'use client';

import { useState } from 'react';
import { TIERS } from '@/lib/constants';

const COMPARISON = [
  { feature: 'All 41 diagnostic tools', free: true, premium: true, pro: true },
  { feature: 'AI Diagnostic Chat', free: '3/day', premium: '20/day', pro: 'Unlimited' },
  { feature: 'Vehicle Garage', free: '1 vehicle', premium: '3 vehicles', pro: 'Unlimited' },
  { feature: 'Community Forum', free: true, premium: true, pro: true },
  { feature: 'Blog Access', free: true, premium: true, pro: true },
  { feature: 'Morning Brief Emails', free: false, premium: true, pro: true },
  { feature: 'Wiring Diagrams', free: false, premium: false, pro: true },
  { feature: 'Torque Sequences', free: false, premium: false, pro: true },
  { feature: 'Service History Export', free: false, premium: false, pro: true },
  { feature: 'Forum Badge', free: '—', premium: 'PREMIUM', pro: 'PRO' },
  { feature: 'Free Trial', free: '—', premium: '7 days', pro: '—' },
];

const FAQ = [
  {
    q: 'Can I use Mission Control for free?',
    a: 'Yes! All 41 diagnostic tools are completely free. The free tier includes 3 AI chat queries per day, 1 vehicle in your garage, and full community access. No credit card required.',
  },
  {
    q: 'What does the 7-day free trial include?',
    a: 'The Premium free trial gives you full Premium access for 7 days — 20 AI queries/day, 3 vehicles, and morning brief emails. If you don\'t cancel before the trial ends, you\'ll be charged $9.99/mo.',
  },
  {
    q: 'Can I switch between plans?',
    a: 'Absolutely. You can upgrade, downgrade, or cancel at any time from your Account page. When you downgrade, you keep access until the end of your current billing period.',
  },
  {
    q: 'What payment methods do you accept?',
    a: 'We accept all major credit and debit cards through Stripe. All payments are securely processed.',
  },
  {
    q: 'Is there an annual discount?',
    a: 'Yes! Annual billing saves you 20%. Premium drops from $9.99/mo to $7.99/mo, and Pro drops from $19.99/mo to $15.99/mo.',
  },
  {
    q: 'What if I need help with something the AI can\'t answer?',
    a: 'Post your question in the community forum! Our community of riders and drivers is incredibly knowledgeable. You can also tag your post with a platform for targeted help.',
  },
];

export default function PricingPage() {
  const [annual, setAnnual] = useState(false);
  const [expandedFAQ, setExpandedFAQ] = useState(null);
  const [showComparison, setShowComparison] = useState(false);

  const handleCheckout = async (tier) => {
    try {
      const res = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tier, interval: annual ? 'annual' : 'monthly' }),
      });
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      }
    } catch (error) {
      console.error('Checkout error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/" className="flex items-center gap-2">
              <span>🔧</span>
              <span className="font-mono font-bold text-sm">MISSION CONTROL</span>
            </a>
          </div>
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="mc-btn-ghost text-sm">Dashboard</a>
            <a href="/login" className="mc-btn-ghost text-sm">Log In</a>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Heading */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p className="text-text-muted text-lg max-w-xl mx-auto">
            Start free with all 41 tools. Upgrade for more AI power, vehicles, and exclusive features.
          </p>
        </div>

        {/* Annual toggle */}
        <div className="flex items-center justify-center gap-3 mb-12">
          <span className={`text-sm font-medium ${!annual ? 'text-text-primary' : 'text-text-muted'}`}>Monthly</span>
          <button
            onClick={() => setAnnual(!annual)}
            className={`w-12 h-6 rounded-full transition-colors relative ${annual ? 'bg-harley' : 'bg-border'}`}
          >
            <span className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${annual ? 'left-7' : 'left-1'}`} />
          </button>
          <span className={`text-sm font-medium ${annual ? 'text-text-primary' : 'text-text-muted'}`}>
            Annual <span className="text-ebike text-xs font-bold ml-1">SAVE 20%</span>
          </span>
        </div>

        {/* Pricing cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {Object.values(TIERS).map((tier) => {
            const isPopular = tier.id === 'premium';
            return (
              <div
                key={tier.id}
                className={`mc-card p-8 relative ${isPopular ? 'border-premium ring-2 ring-premium/20 scale-105' : ''}`}
              >
                {isPopular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="bg-premium text-white text-xs font-bold px-3 py-1 rounded-full">
                      MOST POPULAR
                    </span>
                  </div>
                )}

                <h3 className="text-xl font-bold mb-1">{tier.name}</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">
                    ${tier.id === 'free' ? '0' : annual ? tier.annualPrice : tier.monthlyPrice}
                  </span>
                  {tier.id !== 'free' && <span className="text-text-muted text-lg">/mo</span>}
                  {tier.id !== 'free' && annual && (
                    <p className="text-text-dim text-sm mt-1">
                      Billed annually (${tier.id === 'premium' ? '95.88' : '191.88'}/yr)
                    </p>
                  )}
                </div>

                <ul className="space-y-3 mb-8">
                  {tier.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                      <span className="text-ebike mt-0.5">✓</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>

                {tier.id === 'free' ? (
                  <a href="/dashboard" className="mc-btn-secondary w-full text-center block">
                    Get Started Free
                  </a>
                ) : (
                  <button
                    onClick={() => handleCheckout(tier.id)}
                    className={`mc-btn w-full text-center ${
                      tier.id === 'premium'
                        ? 'bg-premium text-white hover:brightness-110'
                        : 'bg-pro text-black hover:brightness-110'
                    }`}
                  >
                    {tier.id === 'premium' ? 'Start 7-Day Free Trial' : 'Upgrade to Pro'}
                  </button>
                )}
              </div>
            );
          })}
        </div>

        {/* Comparison Table Toggle */}
        <div className="text-center mb-8">
          <button
            onClick={() => setShowComparison(!showComparison)}
            className="mc-btn-secondary"
          >
            {showComparison ? 'Hide' : 'Show'} Feature Comparison ↓
          </button>
        </div>

        {/* Comparison Table */}
        {showComparison && (
          <div className="mc-card overflow-x-auto mb-16">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left p-4 text-text-muted text-sm font-medium">Feature</th>
                  <th className="text-center p-4 text-sm font-medium">Free</th>
                  <th className="text-center p-4 text-sm font-medium text-premium">Premium</th>
                  <th className="text-center p-4 text-sm font-medium text-pro">Pro</th>
                </tr>
              </thead>
              <tbody>
                {COMPARISON.map((row, i) => (
                  <tr key={i} className="border-b border-border last:border-0">
                    <td className="p-4 text-sm">{row.feature}</td>
                    {['free', 'premium', 'pro'].map((tier) => (
                      <td key={tier} className="text-center p-4 text-sm">
                        {row[tier] === true ? (
                          <span className="text-ebike">✓</span>
                        ) : row[tier] === false ? (
                          <span className="text-text-faint">—</span>
                        ) : (
                          <span className="text-text-secondary">{row[tier]}</span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* FAQ */}
        <div className="max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h2>
          <div className="space-y-3">
            {FAQ.map((item, i) => (
              <div key={i} className="mc-card overflow-hidden">
                <button
                  onClick={() => setExpandedFAQ(expandedFAQ === i ? null : i)}
                  className="w-full p-4 flex items-center justify-between text-left hover:bg-background/50 transition-colors"
                >
                  <span className="font-medium text-sm pr-4">{item.q}</span>
                  <span className="text-text-muted text-lg flex-shrink-0">
                    {expandedFAQ === i ? '−' : '+'}
                  </span>
                </button>
                {expandedFAQ === i && (
                  <div className="px-4 pb-4 text-sm text-text-muted animate-fade-in">
                    {item.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
