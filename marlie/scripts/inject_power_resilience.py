"""
Inject 5-Layer Power Resilience section into MARLIE I pitch deck.
Inserts before the INVESTOR BENEFITS section.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML_PATH = r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

SECTION = """
  <!-- ── POWER RESILIENCE ── -->
  <div style="margin-bottom:64px;">
    <div style="font-family:'Source Code Pro',monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:24px;">5-Layer Power Resilience &mdash; Hurricane-Rated Infrastructure</div>

    <p style="font-size:13px;line-height:1.85;color:var(--text-muted);font-weight:300;margin-bottom:32px;">
      Lafayette sits 60 miles inland from the Gulf Coast &mdash; FEMA Zone X, high ground, dry through Katrina, Rita, and Ida.
      But we are in Louisiana. We engineer for what <em>can</em> happen, not just what usually happens.
      MARLIE I is designed to <strong style="color:var(--text-primary);">keep running through a Category 4 landfall</strong> &mdash;
      five independent power layers, stored fuel for 96+ hours on-site, and zero dependence on any single utility or pipeline.
    </p>

    <div style="display:flex;flex-direction:column;gap:3px;margin-bottom:40px;">

      <div style="display:grid;grid-template-columns:48px 1fr;background:#0a0e0a;border:1px solid #1a2a1a;">
        <div style="background:#1a4a1a;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:#70e070;padding:20px 0;">1</div>
        <div style="padding:18px 22px;">
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;color:var(--text-primary);margin-bottom:4px;">LUS POWER &mdash; UTILITY GRID TIE</div>
          <div style="font-size:12px;color:var(--text-muted);line-height:1.7;">Lafayette Utilities System municipal grid. Primary power during commissioning, servicing windows, and low-draw periods. Cooperative interconnect agreement &mdash; municipal utility. MARLIE I draws minimally from the grid at operating capacity, but the tie-in is the legal and operational safety net required by lenders and by code.</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:48px 1fr;background:#0a0e0a;border:1px solid #2a1a3a;">
        <div style="background:#3a1a5a;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:#c070f0;padding:20px 0;">2</div>
        <div style="padding:18px 22px;">
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;color:var(--text-primary);margin-bottom:4px;">BLOOM ENERGY &mdash; ON-SITE FUEL CELLS</div>
          <div style="font-size:12px;color:var(--text-muted);line-height:1.7;">300 kW continuous (Phase 1), scalable in 300 kW increments. Converts Gulf Coast natural gas at 60%+ electrical efficiency &mdash; <strong style="color:var(--gold);">$0.07&ndash;$0.09/kWh</strong> effective cost, grid-independent. Runs 24/7/365 without interruption. Offsets 10.8% of Phase 1 facility load on an ongoing basis. Made in Newark, Delaware &mdash; 100% domestic.</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:48px 1fr;background:#0a0e0a;border:1px solid #1a2a3a;">
        <div style="background:#1a3a5a;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:#60b0f0;padding:20px 0;">3</div>
        <div style="padding:18px 22px;">
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;color:var(--text-primary);margin-bottom:4px;">CAT G3520H &mdash; NATURAL GAS PRIME POWER (N+1)</div>
          <div style="font-size:12px;color:var(--text-muted);line-height:1.7;">2&times; Caterpillar G3520H &mdash; 2.5 MW each, N+1 configuration. One runs continuously, one warm standby. EPA prime/continuous certified &mdash; not standby-restricted. 10-second full block load from cold start. Natural gas / up to 25% hydrogen blend. Manufactured: <strong style="color:var(--text-primary);">Caterpillar Large Engine Center, Lafayette, Indiana.</strong> 5,500 parts from 500+ U.S. suppliers across 33 states. OBBBA domestic content certified.</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:48px 1fr;background:#0a0e0a;border:1px solid #2a2a1a;">
        <div style="background:#4a3a10;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:#d4a843;padding:20px 0;">4</div>
        <div style="padding:18px 22px;">
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;color:var(--text-primary);margin-bottom:4px;">UPS &mdash; BATTERY RIDE-THROUGH</div>
          <div style="font-size:12px;color:var(--text-muted);line-height:1.7;">Uninterruptible power supply &mdash; millisecond switchover, seconds-to-minutes battery ride-through during any source transition. Protects compute hardware from power transients. Vertiv (Columbus, Ohio) or Eaton (Menomonee Falls, Wisconsin) &mdash; both American manufacturers. Standard Tier III data center requirement. Zero perceived downtime to hosted workloads during any power source switch.</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:48px 1fr;background:#0a0e0a;border:1px solid #3a1a1a;">
        <div style="background:#5a1a1a;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:#ff6060;padding:20px 0;">5</div>
        <div style="padding:18px 22px;">
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;color:var(--text-primary);margin-bottom:4px;">DIESEL EMERGENCY BACKUP &mdash; HURRICANE LAYER</div>
          <div style="font-size:12px;color:var(--text-muted);line-height:1.7;">
            Last-resort layer &mdash; independent of natural gas pipelines, utility grid, and all external infrastructure. Activates when gas supply is interrupted by hurricane, pipeline shutdown, or force majeure.
            <br><br>
            <strong style="color:var(--text-primary);">Phase 1:</strong> 1&times; Cat 3516 diesel emergency standby &mdash; 2.0 MW.
            On-site <strong style="color:var(--gold);">20,000-gallon double-wall UL 142 diesel storage tank</strong>.
            Runtime: <strong style="color:var(--gold);">96+ hours at full Phase 1 load</strong> &mdash; enough to outlast any Gulf Coast storm event without resupply.
            <br>
            <strong style="color:var(--text-primary);">Full Build:</strong> 2&times; Cat 3516 diesel (N+1) &mdash; full 6.5 MW emergency coverage. 30,000-gallon tank. 96-hour runtime at full two-floor load.
            <br><br>
            Manufactured: <strong style="color:var(--text-primary);">Caterpillar &mdash; Seguin, Texas / Lafayette, Indiana.</strong>
            Same parts family as our natural gas units. One dealer, one service contract, one relationship: Ring Power, Louisiana.
          </div>
        </div>
      </div>

    </div>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-bottom:32px;">
      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:6px;">5</div>
        <div style="font-size:11px;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase;">Independent Power Layers</div>
      </div>
      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:6px;">96h</div>
        <div style="font-size:11px;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase;">On-Site Diesel Fuel</div>
      </div>
      <div style="background:var(--bg-card);border:1px solid var(--card-border);padding:20px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:#70c070;line-height:1;margin-bottom:6px;">0</div>
        <div style="font-size:11px;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase;">Single Points of Failure</div>
      </div>
    </div>

    <div style="background:#080c08;border:1px solid #2a4020;border-left:4px solid #70e070;padding:20px 24px;font-size:12px;color:var(--text-muted);line-height:1.8;">
      <strong style="color:#70e070;">Hurricane Protocol:</strong>
      When a Gulf Coast storm threatens, MARLIE I switches to diesel + Bloom Energy island mode, disconnects from the grid, and runs self-contained.
      Natural gas generators remain on hot standby. Once the storm passes and pipeline pressure is restored &mdash; typically 24&ndash;72 hours for Lafayette inland &mdash;
      prime power transitions back to natural gas. Diesel tank is replenished via fuel delivery contract.
      <strong style="color:var(--text-primary);">Customer-facing downtime: zero.</strong>
    </div>

  </div>

"""

MARKER = "  <!-- ── INVESTOR BENEFITS ──"
idx = html.find(MARKER)
if idx < 0:
    print("ERROR: injection marker not found")
    # search alternatives
    for alt in ["INVESTOR BENEFITS", "investor benefits", "Investor Benefits"]:
        i2 = html.find(alt)
        if i2 > 0:
            print(f"  Found alternative: [{alt}] at {i2}: {repr(html[max(0,i2-40):i2+60])}")
else:
    html = html[:idx] + SECTION + html[idx:]
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Injected at position {idx} — saved.")
