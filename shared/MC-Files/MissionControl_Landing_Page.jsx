'use client';

import { useState } from 'react';
import { PLATFORMS, PLATFORM_LIST, TIERS } from '@/lib/constants';

export default function LandingPage() {
  const [email, setEmail] = useState('');
  const [emailStatus, setEmailStatus] = useState(null);
  const [activePlatform, setActivePlatform] = useState('harley');
  const [annual, setAnnual] = useState(false);

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setEmailStatus('loading');
    try {
      const res = await fetch('/api/email-signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, platform: activePlatform, source: 'landing' }),
      });
      const data = await res.json();
      if (res.ok) {
        setEmailStatus('success');
        setEmail('');
      } else {
        setEmailStatus(data.error || 'Something went wrong');
      }
    } catch {
      setEmailStatus('Network error. Please try again.');
    }
  };

  const features = [
    { icon: '🔧', title: '41 Free Tools', desc: 'DTC codes, flowcharts, calculators, trackers — all free, no login required.' },
    { icon: '🤖', title: 'AI Diagnostic Chat', desc: 'Describe your issue in plain English. Get expert-level guidance instantly.' },
    { icon: '🏠', title: 'Vehicle Garage', desc: 'Track your vehicles, service history, fuel logs, and maintenance schedules.' },
    { icon: '📊', title: '5 Platforms', desc: 'Harley-Davidson, Automotive, Trucking, E-Bike, and Scooter — all in one place.' },
    { icon: '💬', title: 'Community Forum', desc: 'Ask questions, share knowledge, and connect with other riders and drivers.' },
    { icon: '📧', title: 'Morning Briefs', desc: 'Daily tips, seasonal reminders, and maintenance nudges delivered to your inbox.' },
  ];

  const testimonials = [
    { name: 'Jake M.', vehicle: '2019 Street Glide', platform: 'harley', text: 'Found the exact DTC code for my check engine light in seconds. Saved me a $150 dealer diagnostic fee.' },
    { name: 'Sarah K.', vehicle: '2022 RAV4', platform: 'auto', text: 'The AI chat explained my P0420 code better than the forums. Turns out it was just a loose gas cap.' },
    { name: 'Mike T.', vehicle: 'CDL Class A', platform: 'trucking', text: 'The HOS tracker is cleaner than my ELD. Great for planning my routes and keeping compliant.' },
    { name: 'Lisa R.', vehicle: 'RadPower RadRunner', platform: 'ebike', text: 'Battery health calculator helped me understand why my range was dropping. Needed a BMS reset.' },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="border-b border-border sticky top-0 bg-background/80 backdrop-blur-md z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🔧</span>
            <span className="font-bold text-lg text-text-primary font-mono">MISSION CONTROL</span>
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm text-text-muted">
            <a href="#features" className="hover:text-text-primary transition-colors">Features</a>
            <a href="#platforms" className="hover:text-text-primary transition-colors">Platforms</a>
            <a href="#pricing" className="hover:text-text-primary transition-colors">Pricing</a>
            <a href="/blog" className="hover:text-text-primary transition-colors">Blog</a>
          </div>
          <div className="flex items-center gap-3">
            <a href="/login" className="mc-btn-ghost text-sm">Log In</a>
            <a href="/dashboard" className="mc-btn-primary text-sm">Open Dashboard</a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface border border-border text-sm text-text-muted mb-6">
            <span className="w-2 h-2 rounded-full bg-ebike animate-pulse" />
            41 free tools across 5 platforms
          </div>

          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            <span className="text-gradient-brand">AI-Powered</span> Vehicle Intelligence
            <br />for Every Rider & Driver
          </h1>

          <p className="text-lg md:text-xl text-text-secondary max-w-2xl mx-auto mb-10">
            Free diagnostic tools, AI chat, vehicle garage, and community — for Harley riders,
            car owners, truckers, e-bike riders, and scooter owners.
          </p>

          {/* Email capture */}
          <form onSubmit={handleEmailSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto mb-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email for early access"
              className="mc-input flex-1"
              required
            />
            <button
              type="submit"
              disabled={emailStatus === 'loading'}
              className="mc-btn-primary whitespace-nowrap"
            >
              {emailStatus === 'loading' ? 'Joining...' : 'Get Started Free'}
            </button>
          </form>

          {emailStatus === 'success' && (
            <p className="text-ebike text-sm">You&apos;re in! Check your email for a welcome message.</p>
          )}
          {emailStatus && emailStatus !== 'loading' && emailStatus !== 'success' && (
            <p className="text-danger text-sm">{emailStatus}</p>
          )}

          <p className="text-text-dim text-sm">Free forever. No credit card required.</p>
        </div>
      </section>

      {/* Platform Tabs */}
      <section id="platforms" className="py-16 px-4 bg-surface/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">One Dashboard. Five Platforms.</h2>
          <p className="text-text-muted text-center mb-10 max-w-xl mx-auto">
            Pick your ride. Get tools built specifically for your vehicle type.
          </p>

          <div className="flex flex-wrap justify-center gap-2 mb-10">
            {PLATFORM_LIST.map((p) => (
              <button
                key={p.id}
                onClick={() => setActivePlatform(p.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  activePlatform === p.id
                    ? 'text-white shadow-lg'
                    : 'bg-surface text-text-muted border border-border hover:text-text-primary'
                }`}
                style={activePlatform === p.id ? { backgroundColor: p.color } : {}}
              >
                {p.icon} {p.shortName}
              </button>
            ))}
          </div>

          <div className="mc-card p-8 max-w-2xl mx-auto" style={{ borderColor: PLATFORMS[activePlatform]?.color + '40' }}>
            <div className="flex items-center gap-3 mb-4">
              <span className="text-4xl">{PLATFORMS[activePlatform]?.icon}</span>
              <div>
                <h3 className="text-xl font-bold">{PLATFORMS[activePlatform]?.name}</h3>
                <p className="text-text-muted text-sm">{PLATFORMS[activePlatform]?.toolCount} specialized tools</p>
              </div>
            </div>
            <p className="text-text-secondary mb-6">{PLATFORMS[activePlatform]?.description}</p>
            <a
              href={PLATFORMS[activePlatform]?.route}
              className="mc-btn text-white inline-block"
              style={{ backgroundColor: PLATFORMS[activePlatform]?.color }}
            >
              Explore {PLATFORMS[activePlatform]?.shortName} Tools →
            </a>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Everything You Need</h2>
          <p className="text-text-muted text-center mb-12 max-w-xl mx-auto">
            Built by riders for riders. Every tool is free to use — upgrade for AI power and extra features.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <div key={i} className="mc-card-hover p-6">
                <span className="text-3xl mb-4 block">{f.icon}</span>
                <h3 className="font-bold text-lg mb-2">{f.title}</h3>
                <p className="text-text-muted text-sm">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-4 bg-surface/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">What Riders Are Saying</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {testimonials.map((t, i) => (
              <div key={i} className="mc-card p-6">
                <div className="flex items-center gap-1 mb-3">
                  {Array.from({ length: 5 }).map((_, j) => (
                    <span key={j} className="text-yellow-500 text-sm">★</span>
                  ))}
                </div>
                <p className="text-text-secondary mb-4 italic">&quot;{t.text}&quot;</p>
                <div className="flex items-center gap-3">
                  <div
                    className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
                    style={{ backgroundColor: PLATFORMS[t.platform]?.color }}
                  >
                    {t.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-medium text-sm">{t.name}</p>
                    <p className="text-text-dim text-xs">{t.vehicle}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Simple Pricing</h2>
          <p className="text-text-muted text-center mb-6">Start free. Upgrade when you need more power.</p>

          <div className="flex items-center justify-center gap-3 mb-10">
            <span className={`text-sm ${!annual ? 'text-text-primary' : 'text-text-muted'}`}>Monthly</span>
            <button
              onClick={() => setAnnual(!annual)}
              className={`w-12 h-6 rounded-full transition-colors relative ${annual ? 'bg-harley' : 'bg-border'}`}
            >
              <span className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${annual ? 'left-7' : 'left-1'}`} />
            </button>
            <span className={`text-sm ${annual ? 'text-text-primary' : 'text-text-muted'}`}>
              Annual <span className="text-ebike text-xs font-medium">Save 20%</span>
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {Object.values(TIERS).map((tier) => (
              <div
                key={tier.id}
                className={`mc-card p-6 ${tier.id === 'premium' ? 'border-premium ring-1 ring-premium/30' : ''}`}
              >
                {tier.id === 'premium' && (
                  <span className="mc-badge mc-badge-premium mb-3">MOST POPULAR</span>
                )}
                <h3 className="text-xl font-bold mb-1">{tier.name}</h3>
                <div className="mb-4">
                  <span className="text-3xl font-bold">
                    ${tier.id === 'free' ? '0' : annual ? tier.annualPrice : tier.monthlyPrice}
                  </span>
                  {tier.id !== 'free' && <span className="text-text-muted">/mo</span>}
                </div>
                <ul className="space-y-2 mb-6">
                  {tier.features.map((f, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-text-secondary">
                      <span className="text-ebike">✓</span> {f}
                    </li>
                  ))}
                </ul>
                <a
                  href={tier.id === 'free' ? '/dashboard' : '/pricing'}
                  className={`mc-btn w-full text-center block ${
                    tier.id === 'premium'
                      ? 'bg-premium text-white hover:brightness-110'
                      : tier.id === 'pro'
                      ? 'bg-pro text-black hover:brightness-110'
                      : 'mc-btn-secondary'
                  }`}
                >
                  {tier.id === 'free' ? 'Get Started' : tier.id === 'premium' ? 'Start Free Trial' : 'Go Pro'}
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 bg-surface/50">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Take Control?</h2>
          <p className="text-text-muted mb-8">
            41 free tools. 5 platforms. Zero excuses. Start diagnosing smarter today.
          </p>
          <a href="/dashboard" className="mc-btn-primary text-lg px-8 py-3">
            Open Dashboard — It&apos;s Free
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12 px-4">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h4 className="font-bold text-sm mb-3">Platforms</h4>
            <div className="space-y-2">
              {PLATFORM_LIST.map((p) => (
                <a key={p.id} href={p.route} className="block text-sm text-text-muted hover:text-text-primary">
                  {p.icon} {p.shortName}
                </a>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-bold text-sm mb-3">Product</h4>
            <div className="space-y-2 text-sm text-text-muted">
              <a href="/dashboard" className="block hover:text-text-primary">Dashboard</a>
              <a href="/ai-chat" className="block hover:text-text-primary">AI Chat</a>
              <a href="/tools" className="block hover:text-text-primary">Universal Tools</a>
              <a href="/pricing" className="block hover:text-text-primary">Pricing</a>
            </div>
          </div>
          <div>
            <h4 className="font-bold text-sm mb-3">Community</h4>
            <div className="space-y-2 text-sm text-text-muted">
              <a href="/blog" className="block hover:text-text-primary">Blog</a>
              <a href="/community" className="block hover:text-text-primary">Forum</a>
            </div>
          </div>
          <div>
            <h4 className="font-bold text-sm mb-3">Account</h4>
            <div className="space-y-2 text-sm text-text-muted">
              <a href="/login" className="block hover:text-text-primary">Log In</a>
              <a href="/garage" className="block hover:text-text-primary">My Garage</a>
              <a href="/account" className="block hover:text-text-primary">Settings</a>
            </div>
          </div>
        </div>
        <div className="max-w-6xl mx-auto mt-10 pt-6 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 text-text-dim text-sm">
            <span>🔧</span>
            <span className="font-mono">MISSION CONTROL</span>
            <span>· Built in Baton Rouge, LA</span>
          </div>
          <p className="text-text-dim text-sm">© 2026 Mission Control. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
