"""
Condense the ROI section in index.html — tighten verbose paragraphs,
keep the comparison table, calculator, revenue cards, and Made in USA.
"""

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── Tighten opener paragraph ─────────────────────────────────────────────────
html = html.replace(
    """    <p style="font-size:14px;line-height:1.9;color:var(--text-muted);font-weight:300;">
      Legacy data centers were engineered for the internet era — HTTP traffic, email, CDN delivery.
      They are air-cooled energy hogs running mixed-generation hardware retrofitted with GPUs they
      were never designed to hold. Their operators claim &ldquo;renewable energy&rdquo; through paper
      RECs while burning 40&ndash;80% of their power bill on chillers and CRAC units.
      <strong style="color:var(--text-primary);">That era is over.</strong>
      MARLIE I is purpose-built for one thing: AI inference at the highest density, lowest energy cost,
      and fastest deployment possible. Every dollar of capital goes to compute — not cooling overhead.
      Every watt of power generates revenue — not conditioned air. The comparison is not close.
    </p>""",
    """    <p style="font-size:14px;line-height:1.9;color:var(--text-muted);font-weight:300;">
      Legacy data centers were built for the internet era. Air-cooled, energy-wasteful, retrofitted with GPUs
      they were never designed to hold. Their &ldquo;renewable energy&rdquo; is paper REC credits while
      40&ndash;80% of power burns on chillers. <strong style="color:var(--text-primary);">That era is over.</strong>
      MARLIE I is purpose-built for AI — highest density, lowest energy cost, fastest deployment.
      Every watt generates revenue. Every dollar goes to compute. The comparison is not close.
    </p>"""
)

# ── Tighten the rate basis note under revenue model ──────────────────────────
html = html.replace(
    """    <div style="background:#080e06;border:1px solid #2a4020;border-left:3px solid var(--gold);padding:18px 22px;font-size:12px;color:var(--text-muted);line-height:1.8;">
      <strong style="color:var(--gold);">Rate basis:</strong> $6/GPU/hr is a conservative 2026 market estimate for Vera Rubin-tier compute. Current H100 market rates run $2.50&ndash;$3.50/GPU/hr. Vera Rubin delivers 2.5&times; the FP4 compute density at higher memory bandwidth — a premium rate tier is justified and expected. At $8/GPU/hr (mid estimate), Year 3 gross revenue reaches <strong style="color:var(--gold);">$48.4M</strong>. Infrastructure OPEX remains the same. The upside is asymmetric.
    </div>""",
    """    <div style="background:#080e06;border:1px solid #2a4020;border-left:3px solid var(--gold);padding:14px 20px;font-size:11px;color:var(--text-muted);line-height:1.7;">
      <strong style="color:var(--gold);">Rate basis:</strong> $6/GPU/hr conservative (H100 market: $2.50&ndash;$3.50). Vera Rubin delivers 2.5&times; the FP4 density — premium rate tier justified. At $8/GPU/hr mid estimate, Year 3 gross reaches <strong style="color:var(--gold);">$48.4M</strong>. OPEX stays flat. Upside is asymmetric.
    </div>"""
)

# ── Tighten Natural Gas paragraph ────────────────────────────────────────────
html = html.replace(
    """        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          Lafayette sits 40 miles from <strong style="color:var(--text-primary);">Henry Hub</strong> — the global natural gas price benchmark.
          Gulf Coast gas infrastructure is the most redundant pipeline network in North America.
          Bloom Energy fuel cells convert natural gas at <strong style="color:var(--text-primary);">60%+ electrical efficiency</strong>
          — generating on-site power at an effective cost of <strong style="color:var(--gold);">$0.07&ndash;$0.09/kWh</strong>,
          independent of the utility grid. Every competitor paying grid rates is paying a premium
          that compounds annually. We locked in the cheapest, most reliable power source in the country
          before the first rack was ever installed.
        </p>""",
    """        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          Lafayette sits 40 miles from <strong style="color:var(--text-primary);">Henry Hub</strong> — the global gas price benchmark.
          Bloom Energy fuel cells convert Gulf Coast natural gas at <strong style="color:var(--text-primary);">60%+ efficiency</strong>,
          generating on-site power at <strong style="color:var(--gold);">$0.07&ndash;$0.09/kWh</strong> — independent of the grid.
          Every competitor on grid rates pays a premium that compounds annually. We locked in the cheapest,
          most reliable power source in the country before the first rack arrives.
        </p>"""
)

# ── Tighten Mission Control paragraph ────────────────────────────────────────
html = html.replace(
    """        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          MARLIE I runs on <strong style="color:var(--text-primary);">Mission Control</strong> — an AI multi-agent platform
          built in-house that handles thermal monitoring, load balancing, predictive maintenance alerts,
          customer provisioning, and infrastructure health in real time. What used to require
          <strong style="color:var(--text-primary);">20&ndash;50 data center staff</strong> runs with
          <strong style="color:var(--gold);">3&ndash;5 people</strong>. The AI does not sleep, does not take
          vacation, and responds in milliseconds. Annual staffing savings versus a legacy operation:
          <strong style="color:var(--gold);">$2.5M+/year</strong>. This is not a future feature —
          Mission Control is operational today.
        </p>""",
    """        <p style="font-size:12px;line-height:1.8;color:var(--text-muted);">
          MARLIE I runs on <strong style="color:var(--text-primary);">Mission Control</strong> — an AI multi-agent platform
          built in-house managing thermal, load balancing, maintenance, and provisioning in real time.
          What used to take <strong style="color:var(--text-primary);">20&ndash;50 staff</strong> runs with
          <strong style="color:var(--gold);">3&ndash;5 people</strong>. Annual staffing savings vs legacy ops:
          <strong style="color:var(--gold);">$2.5M+/year</strong>. Not a future feature — operational today.
        </p>"""
)

# ── Tighten City/Government paragraph ────────────────────────────────────────
html = html.replace(
    """      <p style="font-size:12px;line-height:1.8;color:var(--text-muted);margin-top:20px;margin-bottom:0;">
        Every northern city retrofitting old internet infrastructure with band-aid GPU clusters is falling behind. Lafayette goes straight to the front of the line — purpose-built, liquid-cooled, AI-native infrastructure that every major tech company will want access to. The cities that win the AI infrastructure race in 2026 will lead the regional economy for the next 20 years.
        <strong style="color:var(--text-primary);">Lafayette is not on the backline. MARLIE I puts it at the front.</strong>
      </p>""",
    """      <p style="font-size:12px;line-height:1.8;color:var(--text-muted);margin-top:20px;margin-bottom:0;">
        Northern cities are retrofitting old internet infrastructure with band-aid GPU clusters. Lafayette goes straight to the front — purpose-built, liquid-cooled, AI-native. Cities that win the infrastructure race in 2026 lead the regional economy for 20 years.
        <strong style="color:var(--text-primary);">Lafayette is not on the backline. MARLIE I puts it at the front.</strong>
      </p>"""
)

# ── Tighten Made in USA closing paragraph ────────────────────────────────────
html = html.replace(
    """    <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--card-border);font-size:13px;color:var(--text-muted);line-height:1.8;">
      We are not importing AI infrastructure. We are <strong style="color:var(--text-primary);">building America&rsquo;s AI infrastructure</strong> — from the ground up, with American hands, American companies, and American capital. MARLIE I satisfies every OBBBA domestic content requirement and qualifies for the full federal incentive stack. This is what rebuilding American technological leadership looks like.
    </div>""",
    """    <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--card-border);font-size:12px;color:var(--text-muted);line-height:1.8;">
      We are not importing AI infrastructure. We are <strong style="color:var(--text-primary);">building America&rsquo;s AI infrastructure</strong> — American hands, American companies, American capital. 100% OBBBA compliant. Full federal incentive stack qualified. This is what rebuilding American technological leadership looks like.
    </div>"""
)

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("ROI section condensed.")
