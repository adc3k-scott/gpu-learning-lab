'use client';

import { useState } from 'react';
import { PLATFORM_LIST, PLATFORMS } from '@/lib/constants';
import { PlatformBadge } from '@/components/PlatformBadge';
import { useAuth } from '@/components/AuthProvider';

const MOCK_VEHICLES = [
  { id: '1', nickname: 'Black Betty', platform: 'harley', year: 2019, make: 'Harley-Davidson', model: 'Street Glide', mileage: 22450, services: [
    { id: 's1', type: 'Oil Change', date: '2026-01-15', mileage: 22000, cost: 45.00, notes: 'Synthetic 20W-50' },
    { id: 's2', type: 'Tire Replacement', date: '2025-11-20', mileage: 20500, cost: 280.00, notes: 'Rear Dunlop D407' },
    { id: 's3', type: 'Brake Pads', date: '2025-09-10', mileage: 18000, cost: 120.00, notes: 'Front pads only' },
  ]},
];

export default function GaragePage() {
  const { tier } = useAuth();
  const [vehicles, setVehicles] = useState(MOCK_VEHICLES);
  const [selectedVehicle, setSelectedVehicle] = useState(vehicles[0] || null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newVehicle, setNewVehicle] = useState({ platform: 'harley', nickname: '', year: '', make: '', model: '' });

  const addVehicle = () => {
    if (!newVehicle.make || !newVehicle.model) return;
    const vehicle = { ...newVehicle, id: Date.now().toString(), mileage: 0, services: [] };
    setVehicles([...vehicles, vehicle]);
    setSelectedVehicle(vehicle);
    setShowAddForm(false);
    setNewVehicle({ platform: 'harley', nickname: '', year: '', make: '', model: '' });
  };

  const totalCost = selectedVehicle?.services?.reduce((sum, s) => sum + (s.cost || 0), 0) || 0;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
            <span className="text-border">|</span>
            <h1 className="font-bold text-lg">🏠 My Garage</h1>
          </div>
          <button onClick={() => setShowAddForm(true)} className="mc-btn-primary text-sm">+ Add Vehicle</button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Vehicle selector */}
        {vehicles.length > 0 && (
          <div className="flex gap-3 overflow-x-auto mb-8 pb-2">
            {vehicles.map((v) => (
              <button
                key={v.id}
                onClick={() => setSelectedVehicle(v)}
                className={`mc-card p-4 min-w-[200px] flex-shrink-0 text-left transition-all ${
                  selectedVehicle?.id === v.id ? 'ring-2' : 'opacity-70 hover:opacity-100'
                }`}
                style={selectedVehicle?.id === v.id ? { borderColor: PLATFORMS[v.platform]?.color, ringColor: PLATFORMS[v.platform]?.color } : {}}
              >
                <PlatformBadge platform={v.platform} size="sm" />
                <h3 className="font-bold mt-2">{v.nickname || `${v.year} ${v.model}`}</h3>
                <p className="text-text-dim text-xs">{v.year} {v.make} {v.model}</p>
                <p className="text-text-muted text-xs mt-1">{v.mileage?.toLocaleString()} miles</p>
              </button>
            ))}
          </div>
        )}

        {/* Add vehicle form */}
        {showAddForm && (
          <div className="mc-card p-6 mb-8 animate-slide-down">
            <h3 className="font-bold mb-4">Add a Vehicle</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1.5">Platform</label>
                <select value={newVehicle.platform} onChange={(e) => setNewVehicle({ ...newVehicle, platform: e.target.value })} className="mc-input">
                  {PLATFORM_LIST.map((p) => (<option key={p.id} value={p.id}>{p.icon} {p.name}</option>))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">Nickname</label>
                <input type="text" value={newVehicle.nickname} onChange={(e) => setNewVehicle({ ...newVehicle, nickname: e.target.value })} placeholder="Black Betty" className="mc-input" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">Year</label>
                <input type="number" value={newVehicle.year} onChange={(e) => setNewVehicle({ ...newVehicle, year: e.target.value })} placeholder="2022" className="mc-input" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">Make</label>
                <input type="text" value={newVehicle.make} onChange={(e) => setNewVehicle({ ...newVehicle, make: e.target.value })} placeholder="Harley-Davidson" className="mc-input" required />
              </div>
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium mb-1.5">Model</label>
                <input type="text" value={newVehicle.model} onChange={(e) => setNewVehicle({ ...newVehicle, model: e.target.value })} placeholder="Street Glide" className="mc-input" required />
              </div>
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={addVehicle} className="mc-btn-primary">Add Vehicle</button>
              <button onClick={() => setShowAddForm(false)} className="mc-btn-ghost">Cancel</button>
            </div>
          </div>
        )}

        {/* Selected vehicle details */}
        {selectedVehicle && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Stats */}
            <div className="lg:col-span-3 grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="mc-card p-4 text-center">
                <p className="text-2xl font-bold">{selectedVehicle.mileage?.toLocaleString()}</p>
                <p className="text-text-dim text-xs">Miles</p>
              </div>
              <div className="mc-card p-4 text-center">
                <p className="text-2xl font-bold">{selectedVehicle.services?.length || 0}</p>
                <p className="text-text-dim text-xs">Services</p>
              </div>
              <div className="mc-card p-4 text-center">
                <p className="text-2xl font-bold">${totalCost.toFixed(0)}</p>
                <p className="text-text-dim text-xs">Total Cost</p>
              </div>
              <div className="mc-card p-4 text-center">
                <p className="text-2xl font-bold" style={{ color: PLATFORMS[selectedVehicle.platform]?.color }}>
                  {PLATFORMS[selectedVehicle.platform]?.icon}
                </p>
                <p className="text-text-dim text-xs">{PLATFORMS[selectedVehicle.platform]?.shortName}</p>
              </div>
            </div>

            {/* Service History */}
            <div className="lg:col-span-3">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold">Service History</h2>
                <button className="mc-btn-primary text-sm">+ Add Service</button>
              </div>

              {selectedVehicle.services?.length > 0 ? (
                <div className="space-y-3">
                  {selectedVehicle.services.map((service) => (
                    <div key={service.id} className="mc-card p-4 flex items-start gap-4">
                      <div className="w-3 h-3 rounded-full mt-1.5 flex-shrink-0" style={{ backgroundColor: PLATFORMS[selectedVehicle.platform]?.color }} />
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h3 className="font-medium">{service.type}</h3>
                          <span className="text-harley font-bold">${service.cost?.toFixed(2)}</span>
                        </div>
                        <div className="flex items-center gap-3 text-text-dim text-xs">
                          <span>{service.date}</span>
                          <span>{service.mileage?.toLocaleString()} mi</span>
                        </div>
                        {service.notes && <p className="text-text-muted text-sm mt-1">{service.notes}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="mc-card p-8 text-center">
                  <p className="text-text-muted">No service records yet. Add your first service above.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Empty state */}
        {vehicles.length === 0 && !showAddForm && (
          <div className="text-center py-16">
            <span className="text-5xl block mb-4">🏠</span>
            <h2 className="text-2xl font-bold mb-2">Your garage is empty</h2>
            <p className="text-text-muted mb-6">Add your first vehicle to start tracking service history and more.</p>
            <button onClick={() => setShowAddForm(true)} className="mc-btn-primary">+ Add Your First Vehicle</button>
          </div>
        )}
      </div>
    </div>
  );
}
