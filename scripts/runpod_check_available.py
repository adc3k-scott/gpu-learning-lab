import os, json
from pathlib import Path
for line in Path('.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k,v = line.split('=',1)
        os.environ.setdefault(k.strip(),v.strip())

import httpx
key = os.environ.get('RUNPOD_API_KEY','')

# Check all available GPUs with pricing
resp = httpx.post('https://api.runpod.io/graphql',
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    json={'query': '{gpuTypes{id displayName memoryInGb secureCloud communityCloud securePrice communityPrice lowestPrice{minimumBidPrice uninterruptablePrice stockStatus}}}'},
    timeout=15)
data = resp.json()

if 'errors' in data:
    # Try simpler query
    resp = httpx.post('https://api.runpod.io/graphql',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={'query': '{gpuTypes{id displayName memoryInGb secureCloud communityCloud securePrice communityPrice}}'},
        timeout=15)
    data = resp.json()

gpus = data.get('data',{}).get('gpuTypes',[])
print(f"{'GPU':<30} {'VRAM':>6} {'Secure':>8} {'Community':>10} {'Secure$/hr':>12} {'Community$/hr':>14}")
print("-" * 85)
for gpu in sorted(gpus, key=lambda x: x.get('securePrice') or 999):
    name = gpu.get('displayName','')
    mem = gpu.get('memoryInGb','')
    secure = gpu.get('secureCloud', False)
    community = gpu.get('communityCloud', False)
    sp = gpu.get('securePrice')
    cp = gpu.get('communityPrice')
    if secure or community:
        sp_str = f"${sp:.2f}" if sp else "N/A"
        cp_str = f"${cp:.2f}" if cp else "N/A"
        print(f"{name:<30} {mem:>4}GB {'Yes' if secure else 'No':>8} {'Yes' if community else 'No':>10} {sp_str:>12} {cp_str:>14}")
