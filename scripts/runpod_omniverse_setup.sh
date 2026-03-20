#!/bin/bash
# ============================================================
# ADC Mission Control — Omniverse DSX Blueprint on RunPod
# One-click setup script for RTX 6000 Ada / L40S / A6000 pods
# ============================================================
# USAGE:
#   1. Create a RunPod GPU pod (RTX 6000 Ada or better, 100GB volume)
#   2. SSH into the pod or use the web terminal
#   3. Set your NGC API key first:
#      export NGC_CLI_API_KEY='your-ngc-key'
#   4. curl this script and run it:
#      curl -sSL https://raw.githubusercontent.com/adhscott/gpu-learning-lab/main/scripts/runpod_omniverse_setup.sh | bash
#   OR copy-paste into the terminal
# ============================================================

set -euo pipefail

echo "============================================"
echo "  ADC Mission Control"
echo "  Omniverse DSX Blueprint -- RunPod Setup"
echo "============================================"
echo ""

# -----------------------------------------------------------
# 0. Detect GPU
# -----------------------------------------------------------
echo "[0/10] Detecting GPU..."
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
echo "[1/10] Installing system dependencies..."
apt-get update -qq
apt-get install -y -qq \
    git git-lfs curl wget unzip build-essential \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libxi6 libxkbcommon0 libxrandr2 libxss1 libxtst6 \
    > /dev/null 2>&1
echo "  Done."

# -----------------------------------------------------------
# 2. Node.js 20.x (for web frontend)
# -----------------------------------------------------------
echo "[2/10] Installing Node.js 20.x..."
if ! command -v node &> /dev/null || [[ $(node -v | cut -d. -f1 | tr -d 'v') -lt 20 ]]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null 2>&1
    apt-get install -y -qq nodejs > /dev/null 2>&1
fi
echo "  Node: $(node --version)"
echo "  npm:  $(npm --version)"

# -----------------------------------------------------------
# 3. Git LFS
# -----------------------------------------------------------
echo "[3/10] Configuring Git LFS..."
git lfs install > /dev/null 2>&1
echo "  Done."

# -----------------------------------------------------------
# 4. Install NGC CLI
# -----------------------------------------------------------
echo "[4/10] Installing NGC CLI..."
if ! command -v ngc &> /dev/null; then
    cd /tmp
    wget -q --content-disposition https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/3.55.0/files/ngcli_linux.zip -O ngc_cli.zip
    unzip -q -o ngc_cli.zip -d /usr/local/
    rm -f ngc_cli.zip
    # NGC CLI extracts to /usr/local/ngc-cli/
    if [ -f /usr/local/ngc-cli/ngc ]; then
        ln -sf /usr/local/ngc-cli/ngc /usr/local/bin/ngc
        chmod +x /usr/local/ngc-cli/ngc
    fi
    cd /workspace
fi
if command -v ngc &> /dev/null; then
    echo "  NGC CLI: $(ngc --version 2>/dev/null | head -1 || echo 'installed')"
else
    echo "  WARNING: NGC CLI install failed. Will need manual Content Pack download."
fi

# -----------------------------------------------------------
# 5. Configure NGC API Key
# -----------------------------------------------------------
echo "[5/10] NGC API Key..."
if [ -n "${NGC_CLI_API_KEY:-}" ]; then
    # Configure NGC CLI non-interactively
    mkdir -p ~/.ngc
    cat > ~/.ngc/config <<NGCEOF
[CURRENT]
apikey = ${NGC_CLI_API_KEY}
format_type = ascii
org = nvidia
NGCEOF
    echo "  NGC API key configured."
else
    echo ""
    echo "  +-----------------------------------------------------+"
    echo "  |  NGC API KEY NOT SET                                 |"
    echo "  |                                                      |"
    echo "  |  The DSX Content Pack (32.73 GB) requires NGC auth.  |"
    echo "  |                                                      |"
    echo "  |  1. Create account: https://ngc.nvidia.com           |"
    echo "  |  2. Get API key: NGC Portal -> Setup -> API Key      |"
    echo "  |  3. Set it:                                          |"
    echo "  |     export NGC_CLI_API_KEY='your-key'                |"
    echo "  |  4. Re-run this script                               |"
    echo "  +-----------------------------------------------------+"
    echo ""
fi

# -----------------------------------------------------------
# 6. Clone the Blueprint repo
# -----------------------------------------------------------
REPO_DIR="/workspace/omniverse-dsx-blueprint"
echo "[6/10] Cloning Omniverse DSX Blueprint..."
if [ -d "$REPO_DIR" ]; then
    echo "  Repo already exists at $REPO_DIR -- pulling latest..."
    cd "$REPO_DIR" && git pull > /dev/null 2>&1
else
    git clone https://github.com/NVIDIA-Omniverse-blueprints/omniverse-dsx-blueprint-for-ai-factories.git "$REPO_DIR" 2>&1 | tail -1
    cd "$REPO_DIR"
fi
echo "  Done. Directory: $REPO_DIR"

# -----------------------------------------------------------
# 7. Download DSX Content Pack from NGC (32.73 GB)
# -----------------------------------------------------------
DSX_DATA="/workspace/dsx-data"
echo "[7/10] DSX Content Pack (32.73 GB)..."
if [ -d "$DSX_DATA/DSX_BP" ] || [ -d "$DSX_DATA/dsx_dataset_v1.0" ]; then
    echo "  Content pack already exists at $DSX_DATA -- skipping download."
else
    mkdir -p "$DSX_DATA"
    if command -v ngc &> /dev/null && [ -n "${NGC_CLI_API_KEY:-}" ]; then
        echo "  Downloading from NGC (this will take 15-30 min on RunPod)..."
        echo "  Size: 32.73 GB compressed"
        ngc registry resource download-version \
            nvidia/omniverse/dsx_dataset \
            --dest "$DSX_DATA" \
            2>&1 | tail -5
        # The download creates a versioned subdirectory — find and note it
        echo "  Download complete. Contents:"
        ls -la "$DSX_DATA"/ 2>/dev/null || true
        echo ""
        echo "  If DSX_BP folder is inside a subdirectory, adjust the path in step 8."
    else
        echo ""
        echo "  +-----------------------------------------------------+"
        echo "  |  CANNOT AUTO-DOWNLOAD: NGC CLI or API key missing    |"
        echo "  |                                                      |"
        echo "  |  Manual download options:                            |"
        echo "  |                                                      |"
        echo "  |  Option A: Set NGC key and re-run this script        |"
        echo "  |    export NGC_CLI_API_KEY='your-key'                 |"
        echo "  |    bash /workspace/runpod_omniverse_setup.sh         |"
        echo "  |                                                      |"
        echo "  |  Option B: NGC CLI manual download                   |"
        echo "  |    ngc registry resource download-version \\          |"
        echo "  |      nvidia/omniverse/dsx_dataset \\                  |"
        echo "  |      --dest $DSX_DATA                                |"
        echo "  |                                                      |"
        echo "  |  Option C: Browser download from NGC catalog         |"
        echo "  |    https://catalog.ngc.nvidia.com (search DSX)       |"
        echo "  |    Upload to pod via RunPod file manager              |"
        echo "  +-----------------------------------------------------+"
        echo ""
    fi
fi

# -----------------------------------------------------------
# 8. Configure scene path
# -----------------------------------------------------------
echo "[8/10] Configuring scene path..."
KIT_CONFIG="$REPO_DIR/source/apps/dsx.kit"

# Find the actual DSX_BP directory (may be nested in versioned folder)
DSX_BP_PATH=""
if [ -d "$DSX_DATA/DSX_BP" ]; then
    DSX_BP_PATH="$DSX_DATA/DSX_BP"
elif [ -d "$DSX_DATA/dsx_dataset_v1.0/DSX_BP" ]; then
    DSX_BP_PATH="$DSX_DATA/dsx_dataset_v1.0/DSX_BP"
else
    # Search one level deep
    for d in "$DSX_DATA"/*/DSX_BP; do
        if [ -d "$d" ]; then
            DSX_BP_PATH="$d"
            break
        fi
    done
fi

if [ -n "$DSX_BP_PATH" ] && [ -f "$KIT_CONFIG" ]; then
    if grep -q 'auto_load_usd' "$KIT_CONFIG"; then
        sed -i "s|auto_load_usd = .*|auto_load_usd = \"${DSX_BP_PATH}/Assembly/DSX_Main_BP.usda\"|" "$KIT_CONFIG"
        echo "  Updated auto_load_usd -> ${DSX_BP_PATH}/Assembly/DSX_Main_BP.usda"
    else
        echo "  WARNING: Could not find auto_load_usd in dsx.kit -- set it manually."
    fi
elif [ -z "$DSX_BP_PATH" ]; then
    echo "  WARNING: DSX_BP directory not found. Content Pack may still be downloading."
    echo "  After download, manually update $KIT_CONFIG:"
    echo "    auto_load_usd = \"/workspace/dsx-data/<path>/DSX_BP/Assembly/DSX_Main_BP.usda\""
else
    echo "  WARNING: dsx.kit not found at $KIT_CONFIG"
fi

# -----------------------------------------------------------
# 9. Set NVIDIA API Key (for AI Agent feature)
# -----------------------------------------------------------
echo "[9/10] NVIDIA API Key..."
if [ -z "${NVIDIA_API_KEY:-}" ]; then
    echo ""
    echo "  +-----------------------------------------------------+"
    echo "  |  Set your NVIDIA API Key for the AI Agent:           |"
    echo "  |                                                      |"
    echo "  |  export NVIDIA_API_KEY='nvapi-...'                   |"
    echo "  |                                                      |"
    echo "  |  Get one at: https://build.nvidia.com                |"
    echo "  |  (Account -> API Keys)                               |"
    echo "  |                                                      |"
    echo "  |  The 3D viewer works without it.                     |"
    echo "  |  The AI Agent requires it.                           |"
    echo "  +-----------------------------------------------------+"
    echo ""
else
    echo "  NVIDIA_API_KEY is set."
fi

# -----------------------------------------------------------
# 10. Configure for RunPod networking
# -----------------------------------------------------------
echo "[10/10] Configuring for RunPod networking..."

# RunPod does NOT support UDP -- WebRTC needs a TCP transport workaround.
# The Omniverse Kit streaming uses WebRTC for video, signaling on port 49100.
# Two options:
#   A) SSH tunnel from local machine (recommended -- bypasses all RunPod proxy limits)
#   B) RunPod HTTP proxy (may hit 100-second Cloudflare timeout)

# Ensure services bind to 0.0.0.0 (required for RunPod -- not 127.0.0.1)
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
# Print launch instructions
# -----------------------------------------------------------
echo ""
echo "============================================"
echo "  SETUP COMPLETE"
echo "============================================"
echo ""

# Check if Content Pack is ready
if [ -n "$DSX_BP_PATH" ]; then
    echo "  [OK] Content Pack found at: $DSX_BP_PATH"
else
    echo "  [!!] Content Pack NOT found -- 3D scene will be empty"
    echo "       Download it first (see step 7 above)"
fi

echo ""
echo "============================================"
echo "  LAUNCH INSTRUCTIONS"
echo "============================================"
echo ""
echo "  Terminal 1 -- Kit Streaming Server:"
echo "    cd $REPO_DIR"
echo "    ./run_streaming.sh"
echo "    (First launch: 5-8 min shader compile)"
echo ""
echo "  Terminal 2 -- Web Frontend:"
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
echo "  Get SSH details from: RunPod Console -> Pod -> Connect -> SSH"
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
echo "  1. Configurator -> Site tab -> select a site"
echo "  2. GPU tab -> switch to GB300 NVL72"
echo "  3. Save config, switch to GB200, save again"
echo "  4. Compare side-by-side (Document icon)"
echo "  5. Simulations -> Thermal -> Begin Test"
echo "  6. Simulations -> Electrical -> Fail RPPs"
echo "  7. AI Agent: 'Run power failure test'"
echo ""
echo "  Full prep kit: https://adc3k.com/trappeys-dsx-prep"
echo ""
echo "============================================"
echo "  ADC Mission Control -- Ready to simulate."
echo "============================================"
