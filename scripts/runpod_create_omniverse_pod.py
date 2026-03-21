"""
ADC Mission Control — Create RunPod GPU Pod for Omniverse DSX Blueprint

Usage:
    python scripts/runpod_create_omniverse_pod.py

Requires:
    RUNPOD_API_KEY environment variable (from runpod.io -> Settings -> API Keys)

What it does:
    1. Checks your RunPod balance
    2. Finds available L40S / A6000 / RTX 4090 GPUs (in that preference order)
    3. Creates a GPU pod with Ubuntu 22.04, 100GB volume, exposed ports
    4. Prints SSH command and web terminal URL
    5. Prints the setup script command to run inside the pod
"""

import json
import os
import sys

import httpx

API_URL = "https://api.runpod.io/graphql"
API_KEY = os.environ.get("RUNPOD_API_KEY", "")

# Pod configuration
POD_CONFIG = {
    "name": "adc-omniverse-dsx",
    "imageName": "runpod/base:0.6.2-cuda12.2.0",  # Lightweight CUDA base — no PyTorch bloat
    "gpuCount": 1,
    "volumeInGb": 200,  # 74GB Content Pack + 50GB build artifacts + headroom
    "containerDiskInGb": 50,  # Packman cache (~15GB) + system + build tools
    "ports": "8888/http,8081/http,49100/http,22/tcp",
    "env": [],
    # GPU preference order: RTX PRO 6000 (Blackwell, meets official spec) > L40S > A6000 > RTX 4090
    "gpuPreference": [
        "RTX PRO 6000",
        "NVIDIA L40S",
        "NVIDIA RTX A6000",
        "NVIDIA GeForce RTX 4090",
        "NVIDIA L40",
        "RTX 6000 Ada",
        "NVIDIA RTX A5000",
    ],
}


def graphql(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL query against RunPod API."""
    resp = httpx.post(
        API_URL,
        json={"query": query, "variables": variables or {}},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        timeout=15.0,
    )
    if not resp.is_success:
        print(f"ERROR: HTTP {resp.status_code}: {resp.text[:500]}")
        sys.exit(1)
    body = resp.json()
    if "errors" in body:
        for e in body["errors"]:
            print(f"ERROR: {e.get('message', e)}")
        sys.exit(1)
    return body.get("data", {})


def check_balance():
    """Check RunPod account balance."""
    data = graphql("query { myself { currentSpendPerHr clientBalance } }")
    me = data.get("myself", {})
    balance = me.get("clientBalance", 0)
    spend = me.get("currentSpendPerHr", 0)
    print(f"  Balance:      ${balance:.2f}")
    print(f"  Current burn: ${spend:.4f}/hr")
    if balance < 1.0:
        print("  WARNING: Balance under $1.00. Add credits at runpod.io.")
    return balance


def find_gpu():
    """Find available GPU from preference list."""
    data = graphql("""
        query {
            gpuTypes {
                id
                displayName
                memoryInGb
                communityPrice
                securePrice
            }
        }
    """)
    gpu_types = data.get("gpuTypes", [])

    for preferred in POD_CONFIG["gpuPreference"]:
        for gpu in gpu_types:
            if preferred.lower() in gpu.get("displayName", "").lower():
                price = gpu.get("communityPrice") or gpu.get("securePrice") or 0
                if price > 0:
                    print(f"  Found: {gpu['displayName']} ({gpu['memoryInGb']}GB) — ${price:.2f}/hr")
                    return gpu["id"], price
    return None, None


def list_existing_pods():
    """Check if we already have an omniverse pod running."""
    data = graphql("query { myself { pods { id name desiredStatus } } }")
    pods = data.get("myself", {}).get("pods", [])
    for pod in pods:
        if "omniverse" in pod.get("name", "").lower() or "dsx" in pod.get("name", "").lower():
            print(f"  Existing pod found: {pod['name']} (ID: {pod['id']}, Status: {pod['desiredStatus']})")
            return pod
    return None


def create_pod(gpu_type_id: str):
    """Create a new GPU pod."""
    # Add API keys to pod env if available
    env_vars = []
    nvidia_key = os.environ.get("NVIDIA_API_KEY", "")
    if nvidia_key:
        env_vars.append({"key": "NVIDIA_API_KEY", "value": nvidia_key})
    ngc_key = os.environ.get("NGC_CLI_API_KEY", "")
    if ngc_key:
        env_vars.append({"key": "NGC_CLI_API_KEY", "value": ngc_key})

    query = """
        mutation CreatePod($input: PodFindAndDeployOnDemandInput!) {
            podFindAndDeployOnDemand(input: $input) {
                id
                name
                desiredStatus
                imageName
                machine { podHostId }
                runtime { ports { ip isIpPublic privatePort publicPort type } }
            }
        }
    """
    variables = {
        "input": {
            "name": POD_CONFIG["name"],
            "imageName": POD_CONFIG["imageName"],
            "gpuTypeId": gpu_type_id,
            "gpuCount": POD_CONFIG["gpuCount"],
            "volumeInGb": POD_CONFIG["volumeInGb"],
            "containerDiskInGb": POD_CONFIG["containerDiskInGb"],
            "volumeMountPath": "/workspace",
            "ports": POD_CONFIG["ports"],
            "env": env_vars,
            "cloudType": "COMMUNITY",  # Cheaper than SECURE
        }
    }

    data = graphql(query, variables)
    pod = data.get("podFindAndDeployOnDemand", {})
    return pod


def main():
    if not API_KEY:
        print("ERROR: RUNPOD_API_KEY not set.")
        print("  Get your key at: https://www.runpod.io/console/user/settings")
        print("  Then: export RUNPOD_API_KEY='rp_...'")
        sys.exit(1)

    print("=" * 52)
    print("  ADC Mission Control")
    print("  Omniverse DSX Blueprint — RunPod Deployment")
    print("=" * 52)
    print()

    # Step 1: Check balance
    print("[1/4] Checking RunPod balance...")
    balance = check_balance()
    print()

    # Step 2: Check for existing pod
    print("[2/4] Checking for existing Omniverse pod...")
    existing = list_existing_pods()
    if existing:
        print(f"  Pod already exists. Use RunPod console to manage it.")
        print(f"  Pod ID: {existing['id']}")
        print()
        if existing.get("desiredStatus") == "STOPPED":
            print("  Pod is stopped. Start it with:")
            print(f"    python -c \"import scripts.runpod_create_omniverse_pod as r; r.graphql('mutation {{ podResume(input: {{ podId: \\\"{existing['id']}\\\", gpuCount: 1 }}) {{ id }} }}')\"")
        return

    # Step 3: Find GPU
    print("[3/4] Finding available GPU...")
    gpu_id, price = find_gpu()
    if not gpu_id:
        print("  ERROR: No compatible GPU available right now.")
        print("  Try again in a few minutes, or check runpod.io for availability.")
        sys.exit(1)

    hours_available = balance / price if price > 0 else 0
    print(f"  ${balance:.2f} / ${price:.2f}/hr = ~{hours_available:.0f} hours available")
    print()

    # Step 4: Create pod
    print("[4/4] Creating pod...")
    pod = create_pod(gpu_id)
    pod_id = pod.get("id", "UNKNOWN")
    print(f"  Pod ID:   {pod_id}")
    print(f"  Status:   {pod.get('desiredStatus', 'UNKNOWN')}")
    print(f"  Image:    {pod.get('imageName', 'UNKNOWN')}")
    print()

    print("=" * 52)
    print("  POD CREATED SUCCESSFULLY")
    print("=" * 52)
    print()
    print("  1. Go to: https://www.runpod.io/console/pods")
    print(f"  2. Find pod: {POD_CONFIG['name']} (ID: {pod_id})")
    print("  3. Click 'Connect' -> Web Terminal")
    print("  4. Run the setup script:")
    print()
    print("     cd /workspace")
    print("     apt-get update && apt-get install -y curl")
    print("     curl -sSL https://raw.githubusercontent.com/adc3k-scott/gpu-learning-lab/main/scripts/runpod_omniverse_setup.sh | bash")
    print()
    print("  OR copy-paste the script manually from:")
    print("     scripts/runpod_omniverse_setup.sh")
    print()
    print("  5. After setup, launch:")
    print("     Terminal 1: cd /workspace/omniverse-dsx-blueprint && ./run_streaming.sh")
    print("     Terminal 2: cd /workspace/omniverse-dsx-blueprint && ./run_web.sh")
    print()
    print("  6. Access in browser:")
    print(f"     https://{pod_id}-8081.proxy.runpod.net/streaming.html")
    print()
    print(f"  RECOMMENDED: SSH Tunnel (bypasses RunPod UDP limitation)")
    print(f"     Get SSH details from RunPod Console -> Pod -> Connect -> SSH")
    print(f"     ssh -L 8081:localhost:8081 -L 49100:localhost:49100 root@<IP> -p <PORT>")
    print(f"     Then open: http://localhost:8081/streaming.html")
    print()
    print(f"  STOP when done (saves $$$):")
    print(f"     runpodctl stop pod {pod_id}")
    print(f"     OR: https://www.runpod.io/console/pods -> Stop")
    print()
    print("  Full prep kit: https://adc3k.com/trappeys-dsx-prep")
    print()
    print("=" * 52)
    print("  ADC Mission Control — Pod deployed.")
    print("=" * 52)


if __name__ == "__main__":
    main()
