'use client';

import { useState } from 'react';
import { PLATFORM_LIST } from '@/lib/constants';

const STEPS = ['Platform', 'Vehicle', 'Preferences', 'Launch'];

export default function OnboardingPage() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState({
    platforms: [],
    vehicle: { year: '', make: '', model: '', nickname: '' },
    preferences: { units: 'imperial', briefFrequency: 'daily' },
  });

  const togglePlatform = (id) => {
    setData((prev) => ({
      ...prev,
      platforms: prev.platforms.includes(id)
        ? prev.platforms.filter((p) => p !== id)
        : [...prev.platforms, id],
    }));
  };

  const updateVehicle = (field, value) => {
    setData((prev) => ({ ...prev, vehicle: { ...prev.vehicle, [field]: value } }));
  };

  const updatePreferences = (field, value) => {
    setData((prev) => ({ ...prev, preferences: { ...prev.preferences, [field]: value } }));
  };

  const canProceed = () => {
    if (step === 0) return data.platforms.length > 0;
    if (step === 1) return true; // Vehicle is optional
    return true;
  };

  const handleFinish = async () => {
    // Save to Supabase profile (would happen here)
    window.location.href = '/dashboard';
  };

  const primaryColor = data.platforms[0]
    ? PLATFORM_LIST.find((p) => p.id === data.platforms[0])?.color || '#E8720E'
    : '#E8720E';

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-lg">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {STEPS.map((s, i) => (
              <div key={i} className="flex items-center gap-2">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    i <= step ? 'text-white' : 'bg-surface text-text-muted border border-border'
                  }`}
                  style={i <= step ? { backgroundColor: primaryColor } : {}}
                >
                  {i < step ? '✓' : i + 1}
                </div>
                {i < STEPS.length - 1 && (
                  <div className={`hidden sm:block w-12 h-0.5 ${i < step ? 'bg-harley' : 'bg-border'}`} />
                )}
              </div>
            ))}
          </div>
          <p className="text-text-muted text-sm text-center">
            Step {step + 1} of {STEPS.length}: {STEPS[step]}
          </p>
        </div>

        <div className="mc-card p-8">
          {/* Step 0: Platform Selection */}
          {step === 0 && (
            <div>
              <h2 className="text-2xl font-bold mb-2">What do you ride or drive?</h2>
              <p className="text-text-muted mb-6">Pick all that apply. This customizes your dashboard.</p>

              <div className="grid grid-cols-1 gap-3">
                {PLATFORM_LIST.map((p) => {
                  const selected = data.platforms.includes(p.id);
                  return (
                    <button
                      key={p.id}
                      onClick={() => togglePlatform(p.id)}
                      className={`flex items-center gap-4 p-4 rounded-mc border-2 transition-all text-left ${
                        selected ? 'border-current bg-current/5' : 'border-border hover:border-text-faint'
                      }`}
                      style={selected ? { borderColor: p.color, color: p.color } : {}}
                    >
                      <span className="text-3xl">{p.icon}</span>
                      <div>
                        <p className={`font-bold ${selected ? '' : 'text-text-primary'}`}>{p.name}</p>
                        <p className="text-text-muted text-xs">{p.toolCount} tools</p>
                      </div>
                      {selected && <span className="ml-auto text-xl">✓</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Step 1: Add Vehicle */}
          {step === 1 && (
            <div>
              <h2 className="text-2xl font-bold mb-2">Add your first vehicle</h2>
              <p className="text-text-muted mb-6">Optional — you can skip this and add vehicles later.</p>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1.5">Year</label>
                    <input
                      type="number"
                      value={data.vehicle.year}
                      onChange={(e) => updateVehicle('year', e.target.value)}
                      placeholder="2022"
                      className="mc-input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1.5">Nickname</label>
                    <input
                      type="text"
                      value={data.vehicle.nickname}
                      onChange={(e) => updateVehicle('nickname', e.target.value)}
                      placeholder="My Ride"
                      className="mc-input"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Make</label>
                  <input
                    type="text"
                    value={data.vehicle.make}
                    onChange={(e) => updateVehicle('make', e.target.value)}
                    placeholder="Harley-Davidson"
                    className="mc-input"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Model</label>
                  <input
                    type="text"
                    value={data.vehicle.model}
                    onChange={(e) => updateVehicle('model', e.target.value)}
                    placeholder="Street Glide"
                    className="mc-input"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Preferences */}
          {step === 2 && (
            <div>
              <h2 className="text-2xl font-bold mb-2">Your preferences</h2>
              <p className="text-text-muted mb-6">You can change these anytime in Settings.</p>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-3">Units</label>
                  <div className="flex gap-3">
                    {['imperial', 'metric'].map((unit) => (
                      <button
                        key={unit}
                        onClick={() => updatePreferences('units', unit)}
                        className={`flex-1 p-3 rounded-mc border-2 text-center capitalize font-medium ${
                          data.preferences.units === unit
                            ? 'border-harley text-harley bg-harley/5'
                            : 'border-border text-text-muted hover:border-text-faint'
                        }`}
                      >
                        {unit}
                        <p className="text-xs text-text-dim mt-0.5">
                          {unit === 'imperial' ? 'MPH, °F, gallons' : 'KPH, °C, liters'}
                        </p>
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-3">Morning Brief Emails</label>
                  <div className="flex gap-3">
                    {[
                      { id: 'daily', label: 'Daily' },
                      { id: 'weekly', label: 'Weekly' },
                      { id: 'never', label: 'Never' },
                    ].map((opt) => (
                      <button
                        key={opt.id}
                        onClick={() => updatePreferences('briefFrequency', opt.id)}
                        className={`flex-1 p-3 rounded-mc border-2 text-center font-medium ${
                          data.preferences.briefFrequency === opt.id
                            ? 'border-harley text-harley bg-harley/5'
                            : 'border-border text-text-muted hover:border-text-faint'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Launch */}
          {step === 3 && (
            <div className="text-center py-4">
              <div className="text-6xl mb-4">🚀</div>
              <h2 className="text-2xl font-bold mb-2">You&apos;re all set!</h2>
              <p className="text-text-muted mb-6">
                Your dashboard is customized for{' '}
                {data.platforms.map((id) => PLATFORM_LIST.find((p) => p.id === id)?.shortName).join(', ')}.
              </p>

              <div className="mc-card p-4 text-left mb-6">
                <h3 className="font-medium mb-3 text-sm">What&apos;s waiting for you:</h3>
                <ul className="space-y-2 text-sm text-text-secondary">
                  <li className="flex items-center gap-2"><span className="text-ebike">✓</span> 41 free diagnostic tools</li>
                  <li className="flex items-center gap-2"><span className="text-ebike">✓</span> AI Diagnostic Chat (3 queries/day)</li>
                  <li className="flex items-center gap-2"><span className="text-ebike">✓</span> Vehicle Garage</li>
                  <li className="flex items-center gap-2"><span className="text-ebike">✓</span> Community Forum</li>
                </ul>
              </div>
            </div>
          )}

          {/* Navigation buttons */}
          <div className="flex gap-3 mt-8">
            {step > 0 && (
              <button onClick={() => setStep(step - 1)} className="mc-btn-secondary flex-1">
                Back
              </button>
            )}
            {step < 3 ? (
              <button
                onClick={() => setStep(step + 1)}
                disabled={!canProceed()}
                className="mc-btn-primary flex-1"
                style={canProceed() ? { backgroundColor: primaryColor } : {}}
              >
                {step === 1 && !data.vehicle.make ? 'Skip' : 'Continue'}
              </button>
            ) : (
              <button onClick={handleFinish} className="mc-btn-primary flex-1" style={{ backgroundColor: primaryColor }}>
                Open My Dashboard →
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
