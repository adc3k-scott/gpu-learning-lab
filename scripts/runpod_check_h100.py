import os, json
from pathlib import Path
for line in Path('.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k,v = line.split('=',1)
        os.environ.setdefault(k.strip(),v.strip())

import httpx
key = os.environ.get('RUNPOD_API_KEY','')

# Check H100 availability
resp = httpx.post('https://api.runpod.io/graphql',
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    json={'query': '{gpuTypes{id displayName memoryInGb secureCloud communityCloud lowestPrice{minimumBidPrice uninterruptablePrice}}}'},
    timeout=15)
data = resp.json()
for gpu in data.get('data',{}).get('gpuTypes',[]):
    name = gpu.get('displayName','')
    if 'H100' in name:
        price = gpu.get('lowestPrice',{}) or {}
        secure = gpu.get('secureCloud')
        community = gpu.get('communityCloud')
        on_demand = price.get('uninterruptablePrice','N/A')
        bid = price.get('minimumBidPrice','N/A')
        print(f"{name}: secure={secure}, community={community}, on-demand=${on_demand}/hr, bid=${bid}/hr")
