'use client';

import { useState } from 'react';
import { useAuth } from '@/components/AuthProvider';
import { TIERS } from '@/lib/constants';
import { TierBadge } from '@/components/PlatformBadge';

export default function AccountPage() {
  const { user, profile, tier, signOut } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');

  const tierInfo = TIERS[tier] || TIERS.free;
  const aiUsed = 1; // Placeholder — would come from Supabase
  const aiLimit = tierInfo.aiLimit === Infinity ? '∞' : tierInfo.aiLimit;

  const tabs = [
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'subscription', label: 'Subscription', icon: '💳' },
    { id: 'vehicles', label: 'Vehicles', icon: '🏍️' },
    { id: 'preferences', label: 'Preferences', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
            <span className="text-border">|</span>
            <h1 className="font-bold text-lg">Account Settings</h1>
          </div>
          <TierBadge tier={tier} />
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-1 mb-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-mc text-sm font-medium whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? 'bg-harley text-white'
                  : 'text-text-muted hover:text-text-primary hover:bg-surface'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="space-y-6">
            <div className="mc-card p-6">
              <h2 className="text-lg font-bold mb-4">Profile Information</h2>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-full bg-harley/20 flex items-center justify-center text-harley text-2xl font-bold">
                  {user?.email?.charAt(0).toUpperCase() || '?'}
                </div>
                <div>
                  <p className="font-medium">{profile?.full_name || 'No name set'}</p>
                  <p className="text-text-muted text-sm">{user?.email}</p>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Full Name</label>
                  <input type="text" defaultValue={profile?.full_name || ''} className="mc-input" placeholder="Your name" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Email</label>
                  <input type="email" defaultValue={user?.email || ''} className="mc-input" disabled />
                  <p className="text-text-dim text-xs mt-1">Email changes require re-verification.</p>
                </div>
                <button className="mc-btn-primary">Save Changes</button>
              </div>
            </div>
          </div>
        )}

        {/* Subscription Tab */}
        {activeTab === 'subscription' && (
          <div className="space-y-6">
            <div className="mc-card p-6" style={{ borderColor: tierInfo.color || '#1E1E21' }}>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold">Current Plan</h2>
                <TierBadge tier={tier} size="lg" />
              </div>
              <p className="text-text-muted mb-4">
                {tier === 'free'
                  ? "You're on the free plan. Upgrade for more AI power and features."
                  : `You're on the ${tierInfo.name} plan.`}
              </p>
              {tier === 'free' && (
                <a href="/pricing" className="mc-btn-primary">Upgrade Now</a>
              )}
            </div>

            {/* AI Usage */}
            <div className="mc-card p-6">
              <h3 className="font-bold mb-3">AI Chat Usage Today</h3>
              <div className="flex items-center gap-4 mb-2">
                <div className="flex-1 h-3 bg-surface rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full bg-harley transition-all"
                    style={{ width: tierInfo.aiLimit === Infinity ? '5%' : `${(aiUsed / tierInfo.aiLimit) * 100}%` }}
                  />
                </div>
                <span className="text-sm text-text-muted">{aiUsed} / {aiLimit}</span>
              </div>
              <p className="text-text-dim text-xs">Resets daily at midnight.</p>
            </div>
          </div>
        )}

        {/* Vehicles Tab */}
        {activeTab === 'vehicles' && (
          <div className="space-y-6">
            <div className="mc-card p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold">My Vehicles</h2>
                <a href="/garage" className="mc-btn-primary text-sm">Manage in Garage →</a>
              </div>
              <p className="text-text-muted text-sm">
                {tier === 'free' ? '1 vehicle' : tier === 'premium' ? '3 vehicles' : 'Unlimited vehicles'} allowed on your plan.
              </p>
            </div>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="space-y-6">
            <div className="mc-card p-6">
              <h2 className="text-lg font-bold mb-4">Preferences</h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Units</label>
                  <select defaultValue={profile?.units || 'imperial'} className="mc-input">
                    <option value="imperial">Imperial (MPH, °F, gallons)</option>
                    <option value="metric">Metric (KPH, °C, liters)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Morning Brief Frequency</label>
                  <select defaultValue={profile?.brief_frequency || 'daily'} className="mc-input">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="never">Never</option>
                  </select>
                </div>
                <button className="mc-btn-primary">Save Preferences</button>
              </div>
            </div>

            {/* Danger Zone */}
            <div className="mc-card p-6 border-danger/30">
              <h3 className="font-bold text-danger mb-3">Danger Zone</h3>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Sign Out</p>
                  <p className="text-text-dim text-xs">End your current session.</p>
                </div>
                <button onClick={signOut} className="mc-btn text-danger border border-danger/30 hover:bg-danger/10">
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
