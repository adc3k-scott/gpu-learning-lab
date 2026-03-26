"""
ADC Mission Control — NIM Proof of Concept on RunPod B200
Deploys a Blackwell GPU with NIM-ready container
"""
import os, json
from pathlib import Path

for line in Path('.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k,v = line.split('=',1)
        os.environ.setdefault(k.strip(),v.strip())

import httpx

key = os.environ.get('RUNPOD_API_KEY','')
VOLUME_ID = '55alwnycav'  # aido-workspace network volume

# B200 Blackwell — 180GB VRAM, NVFP4 native
GPU_ID = 'NVIDIA B200'
GPU_COUNT = 1
CONTAINER_DISK = 100  # GB — need space for model weights
VOLUME_MOUNT = '/workspace'

# Use NVIDIA PyTorch container as base (has CUDA, cuDNN, everything)
IMAGE = 'runpod/pytorch:2.8.0-py3.12-cuda12.8.1-devel-ubuntu22.04'

mutation = """
mutation {
  podFindAndDeployOnDemand(
    input: {
      name: "adc-nim-b200"
      gpuTypeId: "NVIDIA B200"
      gpuCount: 1
      cloudType: SECURE
      containerDiskInGb: 100
      networkVolumeId: "%s"
      volumeMountPath: "/workspace"
      imageName: "%s"
      startSsh: true
      dockerArgs: ""
      env: [
        {key: "JUPYTER_PASSWORD", value: "adc3k"}
      ]
      ports: "8888/http,8000/http,8501/http"
    }
  ) {
    id
    name
    desiredStatus
    imageName
    machineId
    machine {
      gpuDisplayName
    }
    runtime {
      uptimeInSeconds
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
""" % (VOLUME_ID, IMAGE)

print("Creating B200 Blackwell pod on RunPod...")
print(f"  GPU: NVIDIA B200 (180GB VRAM)")
print(f"  Image: {IMAGE}")
print(f"  Disk: {CONTAINER_DISK}GB + network volume")
print()

resp = httpx.post('https://api.runpod.io/graphql',
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    json={'query': mutation},
    timeout=60)

data = resp.json()

if 'errors' in data:
    print("ERROR:")
    for err in data['errors']:
        print(f"  {err.get('message','unknown error')}")

    # Try community cloud if secure fails
    print("\nTrying community cloud...")
    mutation2 = mutation.replace('SECURE', 'COMMUNITY')
    resp2 = httpx.post('https://api.runpod.io/graphql',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={'query': mutation2},
        timeout=60)
    data = resp2.json()

    if 'errors' in data:
        print("Community cloud also failed:")
        for err in data['errors']:
            print(f"  {err.get('message','unknown error')}")
        print("\nB200 may not be available right now. Try H100 SXM as fallback.")
    else:
        pod = data['data']['podFindAndDeployOnDemand']
        print(f"\nPOD CREATED (community):")
        print(f"  ID: {pod['id']}")
        print(f"  Name: {pod['name']}")
        print(f"  Status: {pod['desiredStatus']}")
        print(f"  GPU: {pod.get('machine',{}).get('gpuDisplayName','pending')}")
else:
    pod = data['data']['podFindAndDeployOnDemand']
    print(f"POD CREATED:")
    print(f"  ID: {pod['id']}")
    print(f"  Name: {pod['name']}")
    print(f"  Status: {pod['desiredStatus']}")
    print(f"  GPU: {pod.get('machine',{}).get('gpuDisplayName','pending')}")

print("\nNext steps:")
print("1. Wait for pod to start (1-3 minutes)")
print("2. SSH in or use Jupyter")
print("3. Install NIM and deploy model")
print("4. Test inference endpoint")
