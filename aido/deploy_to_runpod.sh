#!/usr/bin/env bash
# AIDO RunPod Deployment Script
# Syncs pipeline code to RunPod network volume and runs TTS + render remotely.
#
# Usage:
#   ./aido/deploy_to_runpod.sh <pod_ip> <episode_id>
#   ./aido/deploy_to_runpod.sh 12.34.56.78 EP001
#
# Prerequisites:
#   - RunPod pod running with SSH access (TCP port exposed)
#   - Network volume mounted at /workspace (aido-workspace, 50GB, US-TX-3)
#   - SSH key added to RunPod pod
#   - ELEVENLABS_API_KEY in local .env

set -euo pipefail

POD_IP="${1:?Usage: $0 <pod_ip> [episode_id]}"
EPISODE="${2:-EP001}"
REMOTE_USER="root"
REMOTE_DIR="/workspace/aido"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=15"

echo "=== AIDO RunPod Deploy ==="
echo "Pod:     ${REMOTE_USER}@${POD_IP}"
echo "Episode: ${EPISODE}"
echo "Remote:  ${REMOTE_DIR}"
echo ""

# Load .env for ELEVENLABS_API_KEY
if [ -f .env ]; then
    set -a && source .env && set +a
fi

if [ -z "${ELEVENLABS_API_KEY:-}" ]; then
    echo "ERROR: ELEVENLABS_API_KEY not set in .env"
    exit 1
fi

# -----------------------------------------------------------------------
# 1. Sync pipeline code
# -----------------------------------------------------------------------
echo "--- Syncing code to RunPod ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" "mkdir -p ${REMOTE_DIR}"

rsync -avz --progress \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env' \
    --exclude 'output/' \
    aido/ "${REMOTE_USER}@${POD_IP}:${REMOTE_DIR}/"

# Sync workspace scenes
rsync -avz --progress \
    workspace/ "${REMOTE_USER}@${POD_IP}:/workspace/scenes/"

echo "Code synced."

# -----------------------------------------------------------------------
# 2. Install dependencies on pod
# -----------------------------------------------------------------------
echo "--- Installing dependencies ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" bash << 'REMOTE_SETUP'
    pip install -q httpx python-dotenv 2>&1 | tail -3
    # Omniverse Kit (headless)
    pip install -q omniverse-kit 2>&1 | tail -3 || echo "omniverse-kit install skipped (may already be installed)"
    # ffmpeg check
    ffmpeg -version 2>&1 | head -1 || apt-get install -y ffmpeg -q
REMOTE_SETUP
echo "Dependencies ready."

# -----------------------------------------------------------------------
# 3. Write .env on pod (secrets only — no commit risk)
# -----------------------------------------------------------------------
echo "--- Writing secrets to pod ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" "cat > ${REMOTE_DIR}/.env" << REMOTE_ENV
ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
NOTION_API_KEY=${NOTION_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
REMOTE_ENV
echo "Secrets written."

# -----------------------------------------------------------------------
# 4. Run TTS generation
# -----------------------------------------------------------------------
echo "--- Running TTS (${EPISODE}) ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" bash << REMOTE_TTS
    cd /workspace
    export \$(cat ${REMOTE_DIR}/.env | xargs)
    python -m aido.tts_generate --episode ${EPISODE} --out-dir /workspace/output/${EPISODE}
    echo "TTS done."
REMOTE_TTS

# -----------------------------------------------------------------------
# 5. Run USD content injection
# -----------------------------------------------------------------------
echo "--- Injecting USD content ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" bash << REMOTE_USD
    cd /workspace
    python -m aido.inject_content \
        --manifest /workspace/output/${EPISODE}/manifest.json \
        --out-dir /workspace/output/${EPISODE}
    echo "USD injection done."
REMOTE_USD

# -----------------------------------------------------------------------
# 6. Run Omniverse render
# -----------------------------------------------------------------------
echo "--- Running Omniverse headless render ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" bash << REMOTE_RENDER
    cd /workspace
    export OMNI_KIT_ALLOW_ROOT=1
    python -m aido.render_episode \
        --master-usd /workspace/output/${EPISODE}/usd/${EPISODE}_master.usda \
        --out-dir /workspace/output/${EPISODE}/frames \
        --fps 24 --width 1920 --height 1080
    echo "Render done."
REMOTE_RENDER

# -----------------------------------------------------------------------
# 7. Assemble final MP4
# -----------------------------------------------------------------------
echo "--- Assembling final MP4 ---"
ssh $SSH_OPTS "${REMOTE_USER}@${POD_IP}" bash << REMOTE_ASSEMBLE
    cd /workspace
    python -m aido.assemble \
        --manifest /workspace/output/${EPISODE}/manifest.json \
        --frames-dir /workspace/output/${EPISODE}/frames \
        --out-dir /workspace/output/${EPISODE}
    echo "Assembly done."
REMOTE_ASSEMBLE

# -----------------------------------------------------------------------
# 8. Download final MP4 to local
# -----------------------------------------------------------------------
echo "--- Downloading final MP4 ---"
mkdir -p "output/${EPISODE}"
rsync -avz --progress \
    "${REMOTE_USER}@${POD_IP}:/workspace/output/${EPISODE}/${EPISODE}_final.mp4" \
    "output/${EPISODE}/"

rsync -avz --progress \
    "${REMOTE_USER}@${POD_IP}:/workspace/output/${EPISODE}/manifest.json" \
    "output/${EPISODE}/"

echo ""
echo "=== DONE ==="
echo "Final MP4: output/${EPISODE}/${EPISODE}_final.mp4"
echo ""
echo "Next step: python -m aido.upload_youtube --manifest output/${EPISODE}/manifest.json --privacy private"
