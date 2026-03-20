#!/bin/bash
# ============================================================
# ADC Mission Control — Omniverse DSX Blueprint on RunPod
# One-click setup script for L40S / A6000 / RTX 4090 pods
# ============================================================
# USAGE:
#   1. Create a RunPod GPU pod (L40S recommended, Ubuntu 22.04)
#   2. SSH into the pod or use the web terminal
#   3. curl this script and run it:
#      curl -sSL https://raw.githubusercontent.com/<your-repo>/main/scripts/runpod_omniverse_setup.sh | bash
#   OR copy-paste into the terminal
# ============================================================

set -euo pipefail

echo "============================================"
echo "  ADC Mission Control"
echo "  Omniverse DSX Blueprint — RunPod Setup"
echo "============================================"
echo ""

# -----------------------------------------------------------
# 0. Detect GPU
# -----------------------------------------------------------
echo "[0/8] Detecting GPU..."
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "UNKNOWN")
DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "UNKNOWN")
VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "UNKNOWN")
echo "  GPU:    $GPU_NAME"
echo "  Driver: $DRIVER"
echo "  VRAM:   ${VRAM} MiB"
echo ""

# -----------------------------------------------------------
# 1. System packages
# -----------------------------------------------------------
echo "[1/8] Installing system dependencies..."
apt-get update -qq
apt-get install -y -qq \
    git git-lfs curl wget build-essential \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libxi6 libxkbcommon0 libxrandr2 libxss1 libxtst6 \
    > /dev/null 2>&1
echo "  Done."

# -----------------------------------------------------------
# 2. Node.js 20.x (for web frontend)
# -----------------------------------------------------------
echo "[2/8] Installing Node.js 20.x..."
if ! command -v node &> /dev/null || [[ $(node -v | cut -d. -f1 | tr -d 'v') -lt 20 ]]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null 2>&1
    apt-get install -y -qq nodejs > /dev/null 2>&1
fi
echo "  Node: $(node --version)"
echo "  npm:  $(npm --version)"

# -----------------------------------------------------------
# 3. Git LFS
# -----------------------------------------------------------
echo "[3/8] Configuring Git LFS..."
git lfs install > /dev/null 2>&1
echo "  Done."

# -----------------------------------------------------------
# 4. Clone the Blueprint repo
# -----------------------------------------------------------
REPO_DIR="/workspace/omniverse-dsx-blueprint"
echo "[4/8] Cloning Omniverse DSX Blueprint..."
if [ -d "$REPO_DIR" ]; then
    echo "  Repo already exists at $REPO_DIR — pulling latest..."
    cd "$REPO_DIR" && git pull > /dev/null 2>&1
else
    git clone https://github.com/NVIDIA-Omniverse-blueprints/omniverse-dsx-blueprint-for-ai-factories.git "$REPO_DIR" 2>&1 | tail -1
    cd "$REPO_DIR"
fi
echo "  Done. Directory: $REPO_DIR"

# -----------------------------------------------------------
# 5. Download DSX Content Pack from NGC
# -----------------------------------------------------------
DSX_DATA="/workspace/dsx-data"
echo "[5/8] DSX Content Pack..."
if [ -d "$DSX_DATA/DSX_BP" ]; then
    echo "  Content pack already exists at $DSX_DATA — skipping download."
else
    echo ""
    echo "  ┌─────────────────────────────────────────────────────┐"
    echo "  │  MANUAL STEP: Download DSX Content Pack from NGC    │"
    echo "  │                                                     │"
    echo "  │  1. Go to: https://catalog.ngc.nvidia.com           │"
    echo "  │  2. Search: 'DSX Content Pack'                      │"
    echo "  │  3. Download the archive                            │"
    echo "  │  4. Upload to RunPod or download directly:          │"
    echo "  │     mkdir -p $DSX_DATA                              │"
    echo "  │     # Extract archive to $DSX_DATA                  │"
    echo "  │                                                     │"
    echo "  │  OR if you have the NGC CLI:                        │"
    echo "  │     ngc registry resource download-version           │"
    echo "  │       nvidia/omniverse-dsx-content-pack             │"
    echo "  │       --dest $DSX_DATA                              │"
    echo "  └─────────────────────────────────────────────────────┘"
    echo ""
    mkdir -p "$DSX_DATA"
fi

# -----------------------------------------------------------
# 6. Configure scene path
# -----------------------------------------------------------
echo "[6/8] Configuring scene path..."
KIT_CONFIG="$REPO_DIR/source/apps/dsx.kit"
if [ -f "$KIT_CONFIG" ]; then
    # Set the auto_load_usd path to the content pack location
    if grep -q 'auto_load_usd' "$KIT_CONFIG"; then
        sed -i "s|auto_load_usd = .*|auto_load_usd = \"$DSX_DATA/DSX_BP/Assembly/DSX_Main_BP.usda\"|" "$KIT_CONFIG"
        echo "  Updated auto_load_usd in dsx.kit"
    else
        echo "  WARNING: Could not find auto_load_usd in dsx.kit — set it manually."
    fi
else
    echo "  WARNING: dsx.kit not found at $KIT_CONFIG"
fi

# -----------------------------------------------------------
# 7. Set NVIDIA API Key
# -----------------------------------------------------------
echo "[7/8] NVIDIA API Key..."
if [ -z "${NVIDIA_API_KEY:-}" ]; then
    echo ""
    echo "  ┌─────────────────────────────────────────────────────┐"
    echo "  │  Set your NVIDIA API Key for the AI Agent:          │"
    echo "  │                                                     │"
    echo "  │  export NVIDIA_API_KEY='nvapi-...'                  │"
    echo "  │                                                     │"
    echo "  │  Get one at: https://build.nvidia.com               │"
    echo "  │  (Account → API Keys)                               │"
    echo "  │                                                     │"
    echo "  │  The 3D viewer works without it.                    │"
    echo "  │  The AI Agent requires it.                          │"
    echo "  └─────────────────────────────────────────────────────┘"
    echo ""
else
    echo "  NVIDIA_API_KEY is set."
fi

# -----------------------------------------------------------
# 8. Configure for RunPod networking
# -----------------------------------------------------------
echo "[8/9] Configuring for RunPod networking..."

# RunPod does NOT support UDP — WebRTC needs a TCP transport workaround.
# The Omniverse Kit streaming uses WebRTC for video, signaling on port 49100.
# Two options:
#   A) SSH tunnel from local machine (recommended — bypasses all RunPod proxy limits)
#   B) RunPod HTTP proxy (may hit 100-second Cloudflare timeout)

# Ensure services bind to 0.0.0.0 (required for RunPod — not 127.0.0.1)
# The web frontend Vite server needs --host flag
if [ -f "$REPO_DIR/run_web.sh" ]; then
    # Patch Vite to bind to all interfaces if not already
    if ! grep -q '0.0.0.0' "$REPO_DIR/run_web.sh" 2>/dev/null; then
        sed -i 's/npm run dev/npm run dev -- --host 0.0.0.0/g' "$REPO_DIR/run_web.sh" 2>/dev/null || true
    fi
fi
echo "  Network bindings configured for RunPod."

# Get RunPod pod ID for proxy URLs
RUNPOD_POD_ID="${RUNPOD_POD_ID:-$(hostname)}"

# -----------------------------------------------------------
# 9. Print launch instructions
# -----------------------------------------------------------
echo "[9/9] Setup complete!"
echo ""
echo "============================================"
echo "  LAUNCH INSTRUCTIONS"
echo "============================================"
echo ""
echo "  Terminal 1 — Kit Streaming Server:"
echo "    cd $REPO_DIR"
echo "    ./run_streaming.sh"
echo "    (First launch: 5-8 min shader compile)"
echo ""
echo "  Terminal 2 — Web Frontend:"
echo "    cd $REPO_DIR"
echo "    ./run_web.sh"
echo ""
echo "============================================"
echo "  ACCESS METHOD A: SSH TUNNEL (Recommended)"
echo "============================================"
echo ""
echo "  RunPod doesn't support UDP, and WebRTC needs it."
echo "  SSH tunneling bypasses this completely."
echo ""
echo "  From YOUR LOCAL machine (not the pod):"
echo "    ssh -L 8081:localhost:8081 -L 49100:localhost:49100 root@<RUNPOD_SSH_IP> -p <RUNPOD_SSH_PORT>"
echo ""
echo "  Then open in YOUR local browser:"
echo "    http://localhost:8081/streaming.html"
echo ""
echo "  Get SSH details from: RunPod Console → Pod → Connect → SSH"
echo ""
echo "============================================"
echo "  ACCESS METHOD B: RunPod HTTP Proxy"
echo "============================================"
echo ""
echo "  Direct proxy (may timeout after 100s due to Cloudflare):"
echo "    https://${RUNPOD_POD_ID}-8081.proxy.runpod.net/streaming.html"
echo ""
echo "  This works for quick checks but WebRTC streaming may"
echo "  be unstable due to UDP limitation. Use SSH tunnel for"
echo "  sustained simulation sessions."
echo ""
echo "============================================"
echo "  TRAPPEYS QUICK START"
echo "============================================"
echo ""
echo "  Once the Blueprint loads:"
echo "  1. Configurator → Site tab → select a site"
echo "  2. GPU tab → switch to GB300 NVL72"
echo "  3. Save config, switch to GB200, save again"
echo "  4. Compare side-by-side (Document icon)"
echo "  5. Simulations → Thermal → Begin Test"
echo "  6. Simulations → Electrical → Fail RPPs"
echo "  7. AI Agent: 'Run power failure test'"
echo ""
echo "  Full prep kit: https://adc3k.com/trappeys-dsx-prep"
echo ""
echo "============================================"
echo "  ADC Mission Control — Ready to simulate."
echo "============================================"
