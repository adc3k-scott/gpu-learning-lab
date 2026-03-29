#!/bin/bash
# =============================================================================
# DSX Blueprint — ONE-TIME SETUP on aido-workspace network volume
# Run this ONCE on a pod that has the volume mounted at /workspace
# All future pods just mount the volume and run start.sh
#
# Network Volume: aido-workspace | ID: 55alwnycav | 250GB | US-TX-3 SECURE
# =============================================================================

set -e

VOLUME="/workspace"
DSX_DIR="$VOLUME/omniverse-dsx-blueprint-for-ai-factories"
NGC_API_KEY="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"
CONTENT_DIR="$VOLUME/dsx-content"

echo "=== DSX Blueprint One-Time Volume Setup ==="
echo "Volume: $VOLUME"
echo ""

# --- 1. System deps ---
echo "[1/6] Installing system dependencies..."
apt-get update -q && apt-get install -y -q \
    git git-lfs build-essential curl nodejs npm \
    docker.io nvidia-container-toolkit 2>/dev/null || true

git lfs install

# --- 2. Clone repo ---
if [ ! -d "$DSX_DIR" ]; then
    echo "[2/6] Cloning DSX Blueprint repo..."
    cd "$VOLUME"
    git clone https://github.com/NVIDIA-Omniverse-blueprints/omniverse-dsx-blueprint-for-ai-factories.git
    cd "$DSX_DIR"
    git submodule update --init --recursive
else
    echo "[2/6] Repo already cloned — pulling latest..."
    cd "$DSX_DIR"
    git pull
    git submodule update --recursive
fi

# --- 3. Build ---
echo "[3/6] Building Kit application (first build takes 10-20 min)..."
cd "$DSX_DIR"
chmod +x repo.sh run_streaming.sh run_web.sh
./repo.sh build

echo "[3/6] Build complete."

# --- 4. Download USD Content Pack from NGC ---
if [ ! -f "$CONTENT_DIR/DSX_BP/Assembly/DSX_Main_BP.usda" ]; then
    echo "[4/6] Downloading DSX USD Content Pack from NGC..."
    mkdir -p "$CONTENT_DIR"

    # Install NGC CLI if needed
    if ! command -v ngc &> /dev/null; then
        wget -q https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/3.41.4/files/ngccli_linux.zip -O /tmp/ngccli.zip
        unzip -q /tmp/ngccli.zip -d /tmp/ngccli
        chmod +x /tmp/ngccli/ngc-cli/ngc
        mv /tmp/ngccli/ngc-cli/ngc /usr/local/bin/ngc
    fi

    ngc config set --api-key "$NGC_API_KEY" --org nvidia --format_type ascii
    ngc registry resource download-version \
        "nvidia/omniverse/dsx-usd-content-pack:latest" \
        --dest "$CONTENT_DIR"

    echo "[4/6] Content pack downloaded."
else
    echo "[4/6] USD Content Pack already present — skipping."
fi

# --- 5. Patch dsx.kit with USD scene path ---
echo "[5/6] Patching dsx.kit with USD scene path..."
KIT_FILE="$DSX_DIR/source/apps/dsx.kit"
USD_PATH="$CONTENT_DIR/DSX_BP/Assembly/DSX_Main_BP.usda"

if grep -q 'auto_load_usd = ""' "$KIT_FILE" || grep -q 'auto_load_usd = "<your_extract_path>' "$KIT_FILE"; then
    sed -i "s|auto_load_usd = \".*\"|auto_load_usd = \"$USD_PATH\"|g" "$KIT_FILE"
    echo "[5/6] Patched: auto_load_usd = $USD_PATH"
else
    echo "[5/6] dsx.kit already patched or path already set."
fi

# --- 6. Set NGC API key in environment ---
echo "[6/6] Persisting NVIDIA_API_KEY for AI agent..."
echo "export NVIDIA_API_KEY=\"$NGC_API_KEY\"" >> "$VOLUME/.dsx_env"

# --- Write startup script ---
cat > "$VOLUME/start.sh" << 'STARTSCRIPT'
#!/bin/bash
# DSX Blueprint startup — run this every time a new pod mounts the volume
# Usage: bash /workspace/start.sh

VOLUME="/workspace"
DSX_DIR="$VOLUME/omniverse-dsx-blueprint-for-ai-factories"

source "$VOLUME/.dsx_env" 2>/dev/null || true

echo "=== DSX Blueprint Startup ==="
echo "Repo: $DSX_DIR"
echo "NVIDIA_API_KEY: ${NVIDIA_API_KEY:0:20}..."
echo ""
echo "Starting Kit streaming server on port 49100..."
echo "Starting web frontend on port 8080..."
echo ""
echo "Open browser to: http://<POD_IP>:8080"
echo ""

# Terminal 1: Kit streaming server (background)
cd "$DSX_DIR"
./run_streaming.sh &
KIT_PID=$!

# Wait for Kit to be ready (~60s first launch after volume warmup)
echo "Waiting 60s for Kit to initialize..."
sleep 60

# Terminal 2: Web frontend
./run_web.sh &
WEB_PID=$!

echo ""
echo "Kit PID: $KIT_PID | Web PID: $WEB_PID"
echo "Both services running. Ctrl+C to stop."

wait
STARTSCRIPT

chmod +x "$VOLUME/start.sh"

echo ""
echo "=== SETUP COMPLETE ==="
echo ""
echo "Volume contents:"
echo "  $DSX_DIR        — Kit application (built)"
echo "  $CONTENT_DIR    — USD Content Pack"
echo "  $VOLUME/.dsx_env — API keys"
echo "  $VOLUME/start.sh — Startup script"
echo ""
echo "Next time: mount this volume and run:"
echo "  bash /workspace/start.sh"
