"""
Inject the Financial Architecture & ROI section into index.html
before the Contact & CTA section (section 08).
"""

ROI_SECTION = r"""
<div class="section-divider"></div>

<!-- ============================================================ -->
<!-- SECTION: FINANCIAL ARCHITECTURE & ROI                        -->
<!-- ============================================================ -->
<section class="section" id="roi">

  <div class="section-header">
    <span class="section-label">Financial Architecture &mdash; Return on Investment</span>
  </div>

  <div class="section-rule"></div>

  <!-- ── OPENER ── -->
  <div style="max-width:900px;margin-bottom:56px;">
    <div style="font-family:'Oswald',sans-serif;font-size:clamp(22px,3vw,40px);font-weight:700;letter-spacing:3px;color:var(--text-primary);line-height:1.1;margin-bottom:24px;">
      THIS IS NOT A DATA CENTER.<br>
      <span style="color:var(--gold);">THIS IS A MONEY MACHINE.</span>
    </div>
    <p style="font-size:14px;line-height:1.9;color:var(--text-muted);font-weight:300;">
      Legacy data centers were engineered for the internet era — HTTP traffic, email, CDN delivery.
      They are air-cooled energy hogs running mixed-generation hardware retrofitted with GPUs they
      were never designed to hold. Their operators claim &ldquo;renewable energy&rdquo; through paper
      RECs while burning 40&ndash;80% of their power bill on chillers and CRAC units.
      <strong style="color:var(--text-primary);">That era is over.</strong>
      MARLIE I is purpose-built for one thing: AI inference at the highest density, lowest energy cost,
      and fastest deployment possible. Every dollar of capital goes to compute — not cooling overhead.
      Every watt of power generates revenue — not conditioned air. The comparison is not close.
    </p>
  </div>

  <!-- ── COMPARISON TABLE ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">The Comparison Nobody Wants to Make Public</div>
    <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead>
          <tr>
            <th style="text-align:left;padding:12px 16px;background:#0d1117;color:var(--text-muted);font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:2px;border-bottom:1px solid var(--card-border);font-weight:400;">METRIC</th>
            <th style="text-align:center;padding:12px 16px;background:#130808;color:#c04040;font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:2px;border-bottom:1px solid #3a1010;font-weight:400;">LEGACY DATA CENTER<br><span style="font-size:7px;color:#6a2020;">2010s Air-Cooled Infrastructure</span></th>
            <th style="text-align:center;padding:12px 16px;background:#081308;color:var(--gold);font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:2px;border-bottom:1px solid #3a3010;font-weight:400;">MARLIE I — AI FACTORY<br><span style="font-size:7px;color:#8a7020;">Lafayette, Louisiana — 2026</span></th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">Design Purpose</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">Internet traffic, email, CDN</td>
            <td style="padding:11px 16px;text-align:center;color:#70c070;font-weight:500;">AI inference — purpose-built</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;background:#0d1117;">
            <td style="padding:11px 16px;color:var(--text-muted);">Power Efficiency (PUE)</td>
            <td style="padding:11px 16px;text-align:center;color:#c04040;font-weight:600;">1.4 &ndash; 1.8 &nbsp;<span style="font-size:10px;color:#6a2020;">(40&ndash;80% wasted)</span></td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:600;">1.03 &nbsp;<span style="font-size:10px;color:#8a7020;">(&lt;3% overhead)</span></td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">Cooling Method</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">Air (CRAC units, chillers)</td>
            <td style="padding:11px 16px;text-align:center;color:#70c070;font-weight:500;">100% direct-to-chip liquid</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;background:#0d1117;">
            <td style="padding:11px 16px;color:var(--text-muted);">Energy Cost / kWh</td>
            <td style="padding:11px 16px;text-align:center;color:#c04040;font-weight:600;">$0.10 &ndash; $0.18 <span style="font-size:10px;color:#6a2020;">(national avg)</span></td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:600;">$0.065 <span style="font-size:10px;color:#8a7020;">(Louisiana industrial)</span></td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">On-Site Generation</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">None — grid dependent</td>
            <td style="padding:11px 16px;text-align:center;color:#70c070;font-weight:500;">Bloom Energy fuel cells + gas generators</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;background:#0d1117;">
            <td style="padding:11px 16px;color:var(--text-muted);">&ldquo;Renewable&rdquo; Claim</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">REC paper credits — not actual generation</td>
            <td style="padding:11px 16px;text-align:center;color:#70c070;font-weight:500;">Actual on-site fuel cell generation</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">Compute Hardware</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">Mixed-gen, retrofitted GPUs</td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:500;">NVIDIA Vera Rubin NVL72 — latest only</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;background:#0d1117;">
            <td style="padding:11px 16px;color:var(--text-muted);">AI Compute Density</td>
            <td style="padding:11px 16px;text-align:center;color:#c04040;font-weight:600;">Low — not purpose-built</td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:600;">3.6 ExaFLOPS per rack (NVFP4)</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">Revenue / Rack / Year</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">$200K &ndash; $500K <span style="font-size:10px;">(colo/hosting)</span></td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:600;">$3M &ndash; $5M+ <span style="font-size:10px;">(AI compute)</span></td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;background:#0d1117;">
            <td style="padding:11px 16px;color:var(--text-muted);">Operations Model</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">20&ndash;50 FTE — manual ops</td>
            <td style="padding:11px 16px;text-align:center;color:#70c070;font-weight:500;">3&ndash;5 FTE — Mission Control AI</td>
          </tr>
          <tr style="border-bottom:1px solid #1a1a20;">
            <td style="padding:11px 16px;color:var(--text-muted);">Domestic Content</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">Mixed — overseas components</td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:500;">100% USA &mdash; OBBBA compliant</td>
          </tr>
          <tr>
            <td style="padding:11px 16px;color:var(--text-muted);">CHIPS Act Eligible</td>
            <td style="padding:11px 16px;text-align:center;color:#8a4040;">No</td>
            <td style="padding:11px 16px;text-align:center;color:var(--gold);font-weight:600;">Yes &mdash; designed from day one</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ── PHASE 1 CAPITAL BREAKDOWN ── -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-bottom:64px;">

    <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:32px;">
      <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:20px;">Phase 1 — Infrastructure Capital</div>
      <div style="font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:1px;color:var(--text-muted);margin-bottom:12px;">ALREADY OWNED — ZERO COST TO INVESTORS</div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Building Structure (owner-built)</span>
        <span style="color:#70c070;font-weight:600;">$0</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Land (owned, $15K remaining debt)</span>
        <span style="color:#70c070;font-weight:600;">$15,000</span>
      </div>
      <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:1px;color:var(--text-muted);margin-top:16px;margin-bottom:12px;">INFRASTRUCTURE BUILDOUT — PHASE 1 EST.</div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Electrical service upgrade (3-phase heavy)</span>
        <span style="color:var(--text-primary);">$150,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Liquid cooling plant (CDU ×2, dry coolers, piping)</span>
        <span style="color:var(--text-primary);">$350,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Power distribution (switchgear, UPS, bus)</span>
        <span style="color:var(--text-primary);">$250,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Network infrastructure (LUS fiber, spine, patch)</span>
        <span style="color:var(--text-primary);">$120,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Security, monitoring, Mission Control integration</span>
        <span style="color:var(--text-primary);">$80,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Permits, engineering, inspections</span>
        <span style="color:var(--text-primary);">$100,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Contingency (10%)</span>
        <span style="color:var(--text-primary);">$105,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:14px 0 0 0;">
        <span style="color:var(--text-primary);font-weight:600;">Total Infrastructure Est.</span>
        <span style="color:var(--gold);font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;">~$1.17M</span>
      </div>
      <div style="margin-top:16px;padding:12px;background:#080e06;border-left:3px solid #40a040;font-size:11px;color:var(--text-muted);line-height:1.7;">
        GPU hardware (NVIDIA NVL72) priced separately via NVIDIA Enterprise Sales &mdash; available through equipment financing, NVIDIA Capital, and SBA programs. Infrastructure above is bankable as commercial real estate improvement.
      </div>
    </div>

    <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:32px;">
      <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:20px;">Annual Operating Cost — Full Build (16 Racks)</div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Energy (est. 2.4 MW @ $0.065/kWh)</span>
        <span style="color:var(--text-primary);">$1,370,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;"><em>Same load, national avg $0.122/kWh</em></span>
        <span style="color:#c04040;font-size:12px;">$2,570,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:#70c070;font-size:12px;font-weight:500;">Louisiana Energy Savings / Year</span>
        <span style="color:#70c070;font-weight:700;">+ $1,200,000</span>
      </div>
      <div style="margin:12px 0;border-top:1px solid var(--card-border);"></div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Staffing — Mission Control AI (3&ndash;5 FTE)</span>
        <span style="color:var(--text-primary);">$500,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;"><em>Legacy DC staffing same scale (25 FTE)</em></span>
        <span style="color:#c04040;font-size:12px;">$3,000,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:#70c070;font-size:12px;font-weight:500;">AI-Managed Staffing Savings / Year</span>
        <span style="color:#70c070;font-weight:700;">+ $2,500,000</span>
      </div>
      <div style="margin:12px 0;border-top:1px solid var(--card-border);"></div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Connectivity &amp; bandwidth</span>
        <span style="color:var(--text-primary);">$150,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a20;">
        <span style="color:var(--text-muted);font-size:12px;">Insurance, maintenance, misc.</span>
        <span style="color:var(--text-primary);">$300,000</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:14px 0 0 0;">
        <span style="color:var(--text-primary);font-weight:600;">Total Annual OPEX Est.</span>
        <span style="color:var(--gold);font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;">~$2.32M</span>
      </div>
      <div style="margin-top:12px;padding:12px;background:#080e06;border-left:3px solid #40a040;font-size:11px;color:var(--text-muted);line-height:1.7;">
        Combined advantage vs. equivalent operation nationally: <strong style="color:#70c070;">$3.7M+/year</strong> in energy + staffing savings — before a single dollar of revenue.
      </div>
    </div>

  </div>

  <!-- ── REVENUE MODEL ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">Revenue Model — AI Compute Rental (Conservative Basis)</div>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-bottom:32px;">

      <div style="background:#0a0e12;border:1px solid var(--card-border);padding:28px;position:relative;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);margin-bottom:12px;">YEAR 1 — 4 RACKS LIVE · 40% UTIL</div>
        <div style="font-family:'Oswald',sans-serif;font-size:36px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:4px;">$12.1M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:16px;">Gross annual revenue</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.8;">
          288 GPUs online<br>
          @&nbsp;$6/GPU/hr conservative<br>
          40% utilization ramp<br>
          OPEX: ~$1.2M (4-rack scale)<br>
          <strong style="color:#70c070;">EBITDA: ~$10.9M</strong>
        </div>
      </div>

      <div style="background:#0a0e12;border:1px solid var(--gold);padding:28px;position:relative;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--gold);margin-bottom:12px;">YEAR 2 — 8 RACKS LIVE · 65% UTIL</div>
        <div style="font-family:'Oswald',sans-serif;font-size:36px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:4px;">$19.6M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:16px;">Gross annual revenue</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.8;">
          576 GPUs online<br>
          @&nbsp;$6/GPU/hr conservative<br>
          65% stabilized utilization<br>
          OPEX: ~$1.8M (8-rack scale)<br>
          <strong style="color:#70c070;">EBITDA: ~$17.8M</strong>
        </div>
      </div>

      <div style="background:#0a0e12;border:1px solid var(--card-border);padding:28px;position:relative;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);margin-bottom:12px;">YEAR 3 — 16 RACKS LIVE · 75% UTIL</div>
        <div style="font-family:'Oswald',sans-serif;font-size:36px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:4px;">$36.3M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:16px;">Gross annual revenue</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.8;">
          1,152 GPUs online<br>
          @&nbsp;$6/GPU/hr conservative<br>
          75% target utilization<br>
          OPEX: ~$2.32M (full scale)<br>
          <strong style="color:#70c070;">EBITDA: ~$34.0M</strong>
        </div>
      </div>

    </div>

    <div style="background:#080e06;border:1px solid #2a4020;border-left:3px solid var(--gold);padding:18px 22px;font-size:12px;color:var(--text-muted);line-height:1.8;">
      <strong style="color:var(--gold);">Rate basis:</strong> $6/GPU/hr is a conservative 2026 market estimate for Vera Rubin-tier compute. Current H100 market rates run $2.50&ndash;$3.50/GPU/hr. Vera Rubin delivers 2.5&times; the FP4 compute density at higher memory bandwidth — a premium rate tier is justified and expected. At $8/GPU/hr (mid estimate), Year 3 gross revenue reaches <strong style="color:var(--gold);">$48.4M</strong>. Infrastructure OPEX remains the same. The upside is asymmetric.
    </div>
  </div>

  <!-- ── INTERACTIVE CALCULATOR ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">Revenue Calculator — Build Your Own Scenario</div>
    <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:36px;">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;margin-bottom:32px;">

        <div>
          <label style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);display:block;margin-bottom:10px;">RACKS ONLINE: <span id="rack-val" style="color:var(--gold);">8</span></label>
          <input type="range" id="racks" min="1" max="16" value="8" style="width:100%;accent-color:#d4a843;" oninput="calcROI()">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:4px;"><span>1</span><span>16</span></div>
        </div>

        <div>
          <label style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);display:block;margin-bottom:10px;">UTILIZATION: <span id="util-val" style="color:var(--gold);">65%</span></label>
          <input type="range" id="util" min="10" max="100" value="65" style="width:100%;accent-color:#d4a843;" oninput="calcROI()">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:4px;"><span>10%</span><span>100%</span></div>
        </div>

        <div>
          <label style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);display:block;margin-bottom:10px;">GPU RATE: $<span id="rate-val" style="color:var(--gold);">6</span>/hr</label>
          <input type="range" id="rate" min="4" max="15" value="6" style="width:100%;accent-color:#d4a843;" oninput="calcROI()">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:4px;"><span>$4</span><span>$15</span></div>
        </div>

      </div>

      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
        <div style="background:#0a0e12;border:1px solid var(--card-border);padding:20px;text-align:center;">
          <div style="font-family:'Source Code Pro',monospace;font-size:7px;letter-spacing:1.5px;color:var(--text-muted);margin-bottom:8px;">MONTHLY REVENUE</div>
          <div id="monthly" style="font-family:'Oswald',sans-serif;font-size:26px;font-weight:700;color:var(--gold);">$8.2M</div>
        </div>
        <div style="background:#0a0e12;border:1px solid var(--card-border);padding:20px;text-align:center;">
          <div style="font-family:'Source Code Pro',monospace;font-size:7px;letter-spacing:1.5px;color:var(--text-muted);margin-bottom:8px;">ANNUAL REVENUE</div>
          <div id="annual" style="font-family:'Oswald',sans-serif;font-size:26px;font-weight:700;color:var(--gold);">$98.9M</div>
        </div>
        <div style="background:#0a0e12;border:1px solid var(--card-border);padding:20px;text-align:center;">
          <div style="font-family:'Source Code Pro',monospace;font-size:7px;letter-spacing:1.5px;color:var(--text-muted);margin-bottom:8px;">ANNUAL ENERGY COST</div>
          <div id="energy" style="font-family:'Oswald',sans-serif;font-size:26px;font-weight:700;color:#70c070;">$685K</div>
        </div>
        <div style="background:#081308;border:1px solid #2a5020;padding:20px;text-align:center;">
          <div style="font-family:'Source Code Pro',monospace;font-size:7px;letter-spacing:1.5px;color:var(--text-muted);margin-bottom:8px;">EST. EBITDA</div>
          <div id="ebitda" style="font-family:'Oswald',sans-serif;font-size:26px;font-weight:700;color:#80e080;">$97.1M</div>
        </div>
      </div>

      <div style="margin-top:12px;font-size:10px;color:var(--text-muted);text-align:right;">
        Energy est: racks &times; 150 kW &times; $0.065/kWh. OPEX est: energy + $500K staffing + $450K misc. All figures are estimates for modeling purposes.
      </div>
    </div>
  </div>

  <!-- ── ENERGY ARBITRAGE ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">The Louisiana Energy Arbitrage — In Dollars</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-bottom:24px;">

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:24px;text-align:center;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--text-muted);margin-bottom:12px;">MARLIE I — LOUISIANA</div>
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:var(--gold);">$1.37M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">Annual energy cost (full 16 racks)</div>
        <div style="font-size:10px;color:#70c070;margin-top:4px;">$0.065/kWh industrial rate</div>
      </div>

      <div style="background:#13080a;border:1px solid #3a1015;padding:24px;text-align:center;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:#8a4040;margin-bottom:12px;">SAME LOAD — NATIONAL AVERAGE</div>
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:#c04040;">$2.57M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">Same 2.4 MW load</div>
        <div style="font-size:10px;color:#8a4040;margin-top:4px;">$0.122/kWh national average</div>
      </div>

      <div style="background:#13080a;border:1px solid #5a1015;padding:24px;text-align:center;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:#8a4040;margin-bottom:12px;">SAME LOAD — CALIFORNIA</div>
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:#e04040;">$3.86M</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">Same 2.4 MW load</div>
        <div style="font-size:10px;color:#a04040;margin-top:4px;">$0.185/kWh CA industrial avg</div>
      </div>

    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
      <div style="background:#080e06;border:1px solid #2a4020;padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--gold);margin-bottom:12px;">NATURAL GAS — THE HENRY HUB ADVANTAGE</div>
        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          Lafayette sits 40 miles from <strong style="color:var(--text-primary);">Henry Hub</strong> — the global natural gas price benchmark.
          Gulf Coast gas infrastructure is the most redundant pipeline network in North America.
          Bloom Energy fuel cells convert natural gas at <strong style="color:var(--text-primary);">60%+ electrical efficiency</strong>
          — generating on-site power at an effective cost of <strong style="color:var(--gold);">$0.07&ndash;$0.09/kWh</strong>,
          independent of the utility grid. Every competitor paying grid rates is paying a premium
          that compounds annually. We locked in the cheapest, most reliable power source in the country
          before the first rack was ever installed.
        </p>
      </div>
      <div style="background:#080a10;border:1px solid #20204a;padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:2px;color:var(--gold);margin-bottom:12px;">AI-MANAGED OPERATIONS — MISSION CONTROL</div>
        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          MARLIE I runs on <strong style="color:var(--text-primary);">Mission Control</strong> — an AI multi-agent platform
          built in-house that handles thermal monitoring, load balancing, predictive maintenance alerts,
          customer provisioning, and infrastructure health in real time. What used to require
          <strong style="color:var(--text-primary);">20&ndash;50 data center staff</strong> runs with
          <strong style="color:var(--gold);">3&ndash;5 people</strong>. The AI does not sleep, does not take
          vacation, and responds in milliseconds. Annual staffing savings versus a legacy operation:
          <strong style="color:var(--gold);">$2.5M+/year</strong>. This is not a future feature —
          Mission Control is operational today.
        </p>
      </div>
    </div>
  </div>

  <!-- ── TIMELINE TO REVENUE ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">Timeline — Capital In, Revenue Out</div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2px;">

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:1.5px;color:var(--gold);margin-bottom:8px;">Q1&ndash;Q2 2026</div>
        <div style="font-size:12px;font-weight:600;color:var(--text-primary);margin-bottom:8px;">Capital &amp; Build</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.7;">Financing close. Site prep. Electrical upgrade. CDU installation. LUS fiber activation.</div>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:1.5px;color:var(--gold);margin-bottom:8px;">Q3 2026</div>
        <div style="font-size:12px;font-weight:600;color:var(--text-primary);margin-bottom:8px;">First Racks Live</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.7;">NVIDIA Vera Rubin NVL72 delivery. Racks 1&ndash;4 commissioned. Mission Control online.</div>
      </div>

      <div style="background:#081308;border:1px solid #2a5020;padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:1.5px;color:#70d070;margin-bottom:8px;">Q4 2026</div>
        <div style="font-size:12px;font-weight:600;color:#70d070;margin-bottom:8px;">Revenue Begins</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.7;"><strong style="color:#70d070;">First dollar of AI compute revenue.</strong> Racks 5&ndash;8 commissioned. Bloom Energy fuel cells operational.</div>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:1.5px;color:var(--gold);margin-bottom:8px;">2027</div>
        <div style="font-size:12px;font-weight:600;color:var(--text-primary);margin-bottom:8px;">Full Phase 1</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.7;">All 16 racks live. 57.6 ExaFLOPS online. $19&ndash;36M+ annual revenue range at target utilization.</div>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;">
        <div style="font-family:'Source Code Pro',monospace;font-size:8px;letter-spacing:1.5px;color:var(--gold);margin-bottom:8px;">2027&ndash;2028</div>
        <div style="font-size:12px;font-weight:600;color:var(--text-primary);margin-bottom:8px;">Phase 2 &amp; Beyond</div>
        <div style="font-size:11px;color:var(--text-muted);line-height:1.7;">2nd floor expansion. Phase 2 site. Louisiana AI Network buildout. Cash flow funds next node.</div>
      </div>

    </div>
  </div>

  <!-- ── INVESTOR BENEFITS ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">What Investors Get — Beyond the Return</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:28px;">
        <div style="font-size:28px;margin-bottom:12px;">&#9889;</div>
        <div style="font-family:'Oswald',sans-serif;font-size:16px;letter-spacing:1px;color:var(--text-primary);margin-bottom:12px;">RESERVED BANDWIDTH</div>
        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          Investors receive <strong style="color:var(--gold);">reserved GPU compute access during off-peak hours</strong>
          — proportional to investment tier. Run your own AI workloads, inference jobs, or LLM fine-tuning
          at no marginal cost. Estimated compute credit value: <strong style="color:var(--gold);">$50K&ndash;$500K/month</strong>
          depending on tier. This is not a perk. It is a second revenue stream.
        </p>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:28px;">
        <div style="font-size:28px;margin-bottom:12px;">&#128200;</div>
        <div style="font-family:'Oswald',sans-serif;font-size:16px;letter-spacing:1px;color:var(--text-primary);margin-bottom:12px;">EARLY MOVER RATE LOCK</div>
        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          Investors who commit before the first rack goes live receive
          <strong style="color:var(--gold);">locked GPU rental rates below market for 24 months</strong>
          on their reserved bandwidth. As Vera Rubin compute demand increases through 2026&ndash;2027,
          the rate gap widens. Early capital = early advantage, compounding monthly.
        </p>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:28px;">
        <div style="font-size:28px;margin-bottom:12px;">&#127759;</div>
        <div style="font-family:'Oswald',sans-serif;font-size:16px;letter-spacing:1px;color:var(--text-primary);margin-bottom:12px;">NETWORK EQUITY</div>
        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          MARLIE I is Phase 1 of the Louisiana AI Network — a multi-site regional infrastructure play.
          <strong style="color:var(--gold);">Early investors in MARLIE I receive preferred participation rights</strong>
          in Phase 2 and Phase 3 sites. Owning a stake in the first node means owning the template
          for every node that follows. The network effect is real and it starts here.
        </p>
      </div>

    </div>
  </div>

  <!-- ── CITY & GOVERNMENT ── -->
  <div style="margin-bottom:64px;">
    <div style="background:#08080e;border:1px solid #2a2a4a;border-left:4px solid var(--gold);padding:32px;">
      <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:16px;">For the City of Lafayette &amp; the State of Louisiana</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;">
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:var(--gold);">$20M+</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">Estimated 5-year local economic impact (Phase 1 operations, vendor spend, employee wages)</div>
        </div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:var(--gold);">First</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">AI factory in Louisiana — Lafayette becomes the AI infrastructure hub of the Gulf Coast before any other city claims the position</div>
        </div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:var(--gold);">Federal $</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">CHIPS Act, EDA Tech Hub designation, DOE grid programs — ADC3K is the anchor tenant that unlocks federal funding for the entire region</div>
        </div>
      </div>
      <p style="font-size:12px;line-height:1.8;color:var(--text-muted);margin-top:20px;margin-bottom:0;">
        Every northern city retrofitting old internet infrastructure with band-aid GPU clusters is falling behind. Lafayette goes straight to the front of the line — purpose-built, liquid-cooled, AI-native infrastructure that every major tech company will want access to. The cities that win the AI infrastructure race in 2026 will lead the regional economy for the next 20 years.
        <strong style="color:var(--text-primary);">Lafayette is not on the backline. MARLIE I puts it at the front.</strong>
      </p>
    </div>
  </div>

  <!-- ── MADE IN USA ── -->
  <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:36px;">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:24px;">
      <div style="font-size:32px;">&#127482;&#127480;</div>
      <div>
        <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;letter-spacing:2px;color:var(--text-primary);">100% MADE IN AMERICA</div>
        <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:2px;color:var(--gold);">EVERY COMPONENT. EVERY SUPPLIER. EVERY DOLLAR.</div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">NVIDIA GPUs</strong><br>
        Manufactured in Texas — Houston &amp; Dallas area facilities. CHIPS Act domestic production. Zero foreign semiconductor dependency.
      </div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">Bloom Energy Fuel Cells</strong><br>
        Assembled in Newark, Delaware. US-manufactured solid oxide fuel cell stacks. American clean energy technology.
      </div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">Vertiv Cooling Systems</strong><br>
        Columbus, Ohio. CDUs and thermal management built in the American heartland.
      </div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">LUS Fiber Network</strong><br>
        Lafayette, Louisiana. City-owned municipal infrastructure. Every fiber mile is local.
      </div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">Building &amp; Construction</strong><br>
        Built by Louisiana General Contractor (ADC3K). Lafayette labor, Louisiana materials, zero foreign GC markup.
      </div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.8;">
        <strong style="color:var(--text-primary);">Mission Control Platform</strong><br>
        Designed and built in Lafayette, Louisiana. Open-source AI operations platform — American software, American infrastructure, American owned.
      </div>
    </div>
    <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--card-border);font-size:13px;color:var(--text-muted);line-height:1.8;">
      We are not importing AI infrastructure. We are <strong style="color:var(--text-primary);">building America&rsquo;s AI infrastructure</strong> — from the ground up, with American hands, American companies, and American capital. MARLIE I satisfies every OBBBA domestic content requirement and qualifies for the full federal incentive stack. This is what rebuilding American technological leadership looks like.
    </div>
  </div>

</section>

<script>
function calcROI() {
  const racks = parseInt(document.getElementById('racks').value);
  const util = parseInt(document.getElementById('util').value) / 100;
  const rate = parseInt(document.getElementById('rate').value);
  const gpusPerRack = 72;
  const hoursPerYear = 8760;
  const kWperRack = 150; // estimated
  const energyRate = 0.065;
  const baseOpex = 950000; // staffing + connectivity + insurance

  document.getElementById('rack-val').textContent = racks;
  document.getElementById('util-val').textContent = Math.round(util * 100) + '%';
  document.getElementById('rate-val').textContent = rate;

  const annualRev = racks * gpusPerRack * rate * util * hoursPerYear;
  const annualEnergy = racks * kWperRack * hoursPerYear * energyRate;
  const annualOpex = annualEnergy + baseOpex;
  const ebitda = annualRev - annualOpex;
  const monthly = annualRev / 12;

  const fmt = (n) => {
    if (n >= 1e9) return '$' + (n/1e9).toFixed(1) + 'B';
    if (n >= 1e6) return '$' + (n/1e6).toFixed(1) + 'M';
    if (n >= 1e3) return '$' + Math.round(n/1000) + 'K';
    return '$' + Math.round(n);
  };

  document.getElementById('monthly').textContent = fmt(monthly);
  document.getElementById('annual').textContent = fmt(annualRev);
  document.getElementById('energy').textContent = fmt(annualEnergy);
  document.getElementById('ebitda').textContent = fmt(ebitda);
}
calcROI();
</script>
"""

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the section 08 divider and inject before it
TARGET = '<div class="section-divider"></div>\n\n<!-- ============================================================ -->\n<!-- SECTION 8'

# Try alternate spacing
if TARGET not in html:
    import re
    # Find section 08 comment
    match = re.search(r'<div class="section-divider"></div>\s*\n\s*<!-- ={10,}.*?SECTION 8', html)
    if match:
        pos = match.start()
        html = html[:pos] + ROI_SECTION + '\n' + html[pos:]
        print(f"Injected at position {pos}")
    else:
        # Find Contact & CTA section by id
        match2 = re.search(r'<section class="section" id="contact"', html)
        if match2:
            pos = match2.start()
            html = html[:pos] + ROI_SECTION + '\n' + html[pos:]
            print(f"Injected before contact section at {pos}")
        else:
            print("ERROR: Could not find injection point")
            print("Looking for patterns...")
            for pattern in ['SECTION 8', 'section-8', 'id="contact"', 'CONTACT', 'Get In Touch']:
                if pattern in html:
                    print(f"  Found: {pattern}")
else:
    pos = html.index(TARGET)
    html = html[:pos] + ROI_SECTION + '\n' + html[pos:]
    print(f"Injected at position {pos}")

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done.")
