"""
Create a RunPod pod for DSX Blueprint sessions.
Mounts aido-workspace network volume (all builds already done).
Just mount and run /workspace/start.sh — done.

Usage:
    python scripts/runpod_create_dsx_pod.py

Requirements:
    RUNPOD_API_KEY in .env (already there)
"""

import os, sys, json
from pathlib import Path

# Load .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY")
if not RUNPOD_API_KEY:
    print("ERROR: RUNPOD_API_KEY not found in .env")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

MUTATION = """
mutation CreatePod($input: PodFindAndDeployOnDemandInput!) {
  podFindAndDeployOnDemand(input: $input) {
    id
    name
    runtime {
      ports {
        ip
        isIpPublic
        privatePort
        publicPort
        type
      }
    }
  }
}
"""

pod_input = {
    "name": "dsx-blueprint",
    "imageName": "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04",
    "gpuTypeId": "NVIDIA RTX 6000 Ada Generation",   # RTX 6000 Ada (closest to RTX Pro 6000 Blackwell on RunPod)
    "cloudType": "SECURE",
    "networkVolumeId": "55alwnycav",                  # aido-workspace 250GB US-TX-3
    "volumeMountPath": "/workspace",
    "containerDiskInGb": 50,
    "minVcpuCount": 8,
    "minMemoryInGb": 64,
    "ports": "8888/http,8080/http,49100/http,22/tcp",
    "startSsh": True,
    "supportPublicIp": True,
    "env": [
        {"key": "JUPYTER_PASSWORD", "value": "adc3k"},
        {"key": "NVIDIA_API_KEY",   "value": "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"},
    ],
}

print("Creating DSX Blueprint pod...")
print(f"  GPU: {pod_input['gpuTypeId']}")
print(f"  Network Volume: {pod_input['networkVolumeId']} → /workspace")
print(f"  Ports: {pod_input['ports']}")
print()

resp = requests.post(
    "https://api.runpod.io/graphql",
    headers={"Authorization": f"Bearer {RUNPOD_API_KEY}", "Content-Type": "application/json"},
    json={"query": MUTATION, "variables": {"input": pod_input}},
    timeout=30,
)

data = resp.json()

if "errors" in data:
    print("ERROR:", json.dumps(data["errors"], indent=2))
    sys.exit(1)

pod = data["data"]["podFindAndDeployOnDemand"]
pod_id = pod["id"]
print(f"Pod created: {pod_id}")
print(f"Name: {pod['name']}")

ports = pod.get("runtime", {}).get("ports", [])
if ports:
    print("\nPublic ports:")
    for p in ports:
        if p.get("isIpPublic"):
            print(f"  :{p['publicPort']} → {p['type']} (internal {p['privatePort']})")

print(f"\nOnce pod is RUNNING:")
print(f"  SSH: ssh root@<public_ip> -p <ssh_port>")
print(f"  Then: bash /workspace/start.sh")
print(f"\n  OR if first-time setup needed:")
print(f"  bash /workspace/  (no start.sh yet)")
print(f"  Copy dsx_volume_setup.sh to pod and run it once.")
print(f"\nPod ID: {pod_id}  (save this)")
