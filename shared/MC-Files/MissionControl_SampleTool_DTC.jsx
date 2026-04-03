'use client';

import { useState } from 'react';

const DTC_CODES = [
  { code: 'P0131', title: 'O2 Sensor Circuit Low Voltage (Bank 1, Sensor 1)', severity: 'moderate', likelihood: 72, description: 'Indicates low voltage from the front oxygen sensor. Common on Twin Cam and Milwaukee-Eight engines.', causes: ['Faulty O2 sensor', 'Exhaust leak near sensor', 'Wiring damage/corrosion', 'ECM issue (rare)'], fixes: ['Inspect O2 sensor wiring and connector', 'Check for exhaust leaks at header gaskets', 'Replace O2 sensor if readings are out of range', 'Clear code and test ride — may be intermittent'] },
  { code: 'P0122', title: 'Throttle Position Sensor Circuit Low', severity: 'high', likelihood: 58, description: 'TPS sending lower-than-expected voltage to the ECM. Can cause poor throttle response or stalling.', causes: ['Faulty TPS', 'Loose TPS connector', 'Wiring short to ground', 'Corroded pins'], fixes: ['Inspect TPS connector for corrosion', 'Check wiring between TPS and ECM', 'Measure TPS voltage with multimeter (should be 0.5-4.5V)', 'Replace TPS if out of spec'] },
  { code: 'P0562', title: 'System Voltage Low', severity: 'moderate', likelihood: 65, description: 'Battery voltage dropping below 10V during operation. Common after long storage or with aging batteries.', causes: ['Weak or dying battery', 'Faulty voltage regulator', 'Loose battery terminals', 'Parasitic drain'], fixes: ['Load test the battery', 'Clean and tighten battery terminals', 'Test charging system output (should be 13.8-14.5V)', 'Check for parasitic draw with multimeter'] },
  { code: 'P1353', title: 'Front Cylinder Misfire', severity: 'high', likelihood: 45, description: 'Front cylinder is not firing consistently. Can cause rough idle, loss of power, and backfiring.', causes: ['Fouled spark plug', 'Weak ignition coil', 'Fuel injector clogged', 'Low compression'], fixes: ['Replace front spark plug', 'Swap ignition coils front/rear to isolate', 'Run fuel injector cleaner', 'Perform compression test if issue persists'] },
  { code: 'P0501', title: 'Vehicle Speed Sensor Range/Performance', severity: 'low', likelihood: 40, description: 'Speedometer reading is inconsistent or absent. Usually an electrical issue rather than mechanical.', causes: ['Faulty VSS', 'Damaged sensor wiring', 'Corroded connector', 'Aftermarket wheel/tire change'], fixes: ['Inspect VSS connector at transmission', 'Check for damaged wiring', 'Replace VSS if no signal detected', 'Recalibrate speedometer if wheels changed'] },
  { code: 'P2135', title: 'Throttle Position Correlation Error', severity: 'high', likelihood: 52, description: 'TPS 1 and TPS 2 readings don\'t match. May trigger reduced power mode for safety.', causes: ['Faulty throttle body', 'Wiring issue between dual TPS sensors', 'ECM calibration error', 'Aftermarket air cleaner interference'], fixes: ['Check both TPS sensor readings with scan tool', 'Inspect wiring harness for damage', 'Verify aftermarket parts aren\'t interfering', 'Replace throttle body assembly if needed'] },
  { code: 'P0106', title: 'MAP Sensor Performance', severity: 'moderate', likelihood: 48, description: 'Manifold Absolute Pressure sensor readings are outside expected range. Affects fuel mixture.', causes: ['Faulty MAP sensor', 'Vacuum leak at intake', 'Clogged vacuum line', 'Aftermarket intake without remap'], fixes: ['Check vacuum lines for cracks or disconnection', 'Inspect MAP sensor connector', 'Replace MAP sensor if readings erratic', 'Ensure ECM is tuned for aftermarket intake'] },
  { code: 'U1300', title: 'CAN Bus Communication Error', severity: 'low', likelihood: 35, description: 'Controller Area Network communication fault. Often caused by aftermarket accessories tapping into the CAN bus.', causes: ['Aftermarket accessory wiring issue', 'Corroded CAN bus connector', 'ECM communication fault', 'Loose ground connection'], fixes: ['Disconnect any recently added accessories', 'Inspect CAN bus connectors under seat', 'Check all ground connections', 'May require dealer scan tool for full diagnosis'] },
];

const SEVERITY_CONFIG = {
  low: { label: 'Low', color: '#22C55E', bg: 'rgba(34, 197, 94, 0.15)' },
  moderate: { label: 'Moderate', color: '#F59E0B', bg: 'rgba(245, 158, 11, 0.15)' },
  high: { label: 'High', color: '#EF4444', bg: 'rgba(239, 68, 68, 0.15)' },
};

export default function HarleyDTCPage() {
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState(null);

  const filtered = DTC_CODES.filter((dtc) =>
    !search ||
    dtc.code.toLowerCase().includes(search.toLowerCase()) ||
    dtc.title.toLowerCase().includes(search.toLowerCase()) ||
    dtc.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <a href="/harley" className="text-text-muted hover:text-text-primary text-sm">← Harley-Davidson</a>
          <span className="text-border">|</span>
          <h1 className="font-bold" style={{ color: '#E8720E' }}>🔧 DTC Code Database</h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Harley-Davidson DTC Codes</h2>
          <p className="text-text-muted text-sm">Search {DTC_CODES.length} diagnostic trouble codes. Click any code for details.</p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by code (e.g. P0131) or keyword..."
            className="mc-input"
          />
        </div>

        {/* Results */}
        <div className="space-y-3">
          {filtered.map((dtc) => {
            const sev = SEVERITY_CONFIG[dtc.severity];
            const isExpanded = expanded === dtc.code;

            return (
              <div key={dtc.code} className="mc-card overflow-hidden">
                <button
                  onClick={() => setExpanded(isExpanded ? null : dtc.code)}
                  className="w-full p-4 text-left hover:bg-background/50 transition-colors"
                >
                  <div className="flex items-start gap-4">
                    {/* Code */}
                    <div className="font-mono font-bold text-lg text-harley flex-shrink-0 w-20">
                      {dtc.code}
                    </div>

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold mb-1">{dtc.title}</h3>
                      <p className="text-text-muted text-sm line-clamp-1">{dtc.description}</p>
                    </div>

                    {/* Severity badge */}
                    <span
                      className="text-xs font-bold px-2 py-1 rounded flex-shrink-0"
                      style={{ backgroundColor: sev.bg, color: sev.color }}
                    >
                      {sev.label}
                    </span>
                  </div>

                  {/* Likelihood bar */}
                  <div className="flex items-center gap-3 mt-3 ml-24">
                    <span className="text-text-dim text-xs w-16">Likelihood</span>
                    <div className="flex-1 h-2 bg-surface rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{ width: `${dtc.likelihood}%`, backgroundColor: sev.color }}
                      />
                    </div>
                    <span className="text-text-muted text-xs w-8">{dtc.likelihood}%</span>
                  </div>
                </button>

                {/* Expanded detail */}
                {isExpanded && (
                  <div className="border-t border-border p-4 animate-fade-in bg-surface/50">
                    <p className="text-text-secondary text-sm mb-4">{dtc.description}</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-bold text-sm mb-2 text-danger">Possible Causes</h4>
                        <ul className="space-y-1">
                          {dtc.causes.map((c, i) => (
                            <li key={i} className="text-sm text-text-muted flex items-start gap-2">
                              <span className="text-danger mt-0.5">•</span> {c}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-bold text-sm mb-2 text-ebike">Suggested Fixes</h4>
                        <ul className="space-y-1">
                          {dtc.fixes.map((f, i) => (
                            <li key={i} className="text-sm text-text-muted flex items-start gap-2">
                              <span className="text-ebike mt-0.5">{i + 1}.</span> {f}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-border">
                      <a href="/ai-chat" className="text-harley text-sm hover:underline">
                        🤖 Ask AI about {dtc.code} →
                      </a>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-12">
            <p className="text-text-muted">No codes match &quot;{search}&quot;. Try a different search term.</p>
          </div>
        )}
      </div>
    </div>
  );
}
