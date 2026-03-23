"""
Willow Glen AI Factory Renderings
Kontext edits on real helicopter photos + Schnell concept art
"""
import asyncio
import base64
import httpx
import os
import time
from pathlib import Path

API_KEY = os.environ.get("RUNPOD_API_KEY", "")
KONTEXT_ENDPOINT = "https://api.runpod.ai/v2/black-forest-labs-flux-1-kontext-dev"
SCHNELL_ENDPOINT = "https://api.runpod.ai/v2/black-forest-labs-flux-1-schnell"
OUTPUT_DIR = Path("adc3k-deploy/renders")
SOURCE_DIR = Path("adc3k-deploy")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ── KONTEXT JOBS (edit real photos) ──────────────────────────────

KONTEXT_JOBS = [
    {
        "name": "wg-aerial-solar-campus",
        "source": "willow-glen-heli-51.jpg",
        "prompt": (
            "Transform this aerial view of the former power plant into a modern AI factory campus. "
            "Keep the two existing smokestacks as landmarks. Keep the existing electrical substation structures. "
            "On the large open green areas, add rows of ground-mounted solar panel arrays with blue-black photovoltaic panels. "
            "Replace the demolished plant structures in the center with two large modern industrial warehouse buildings with "
            "white metal roofing and solar panels on top. Add a paved road network connecting the buildings. "
            "Keep the Mississippi River visible in the background. Keep the sky realistic with white clouds. "
            "Make it look like a real industrial site under active development, not futuristic. "
            "Realistic professional aerial photography style."
        ),
    },
    {
        "name": "wg-campus-overview-angle2",
        "source": "willow-glen-1.jpg",
        "prompt": (
            "Transform this aerial view of the decommissioned power plant site into an active AI compute campus. "
            "Keep the two tall smokestacks as heritage landmarks. Keep all electrical substation structures exactly as they are. "
            "On the cleared central area where the old plant was, add two large clean modern industrial buildings with "
            "flat white metal roofs and solar panels. Add ground-mounted solar arrays on the open grass areas. "
            "Add a few Cat natural gas generators in a small fenced equipment yard near the buildings. "
            "Keep the existing roads and operational buildings in the foreground. "
            "Everything should look realistic, like real industrial construction. No futuristic elements. "
            "Professional aerial drone photography."
        ),
    },
    {
        "name": "wg-before-after-ground",
        "source": "willow-glen-historical.jpg",
        "prompt": (
            "Update this ground-level photo of the old power plant to show it being converted into a modern AI factory campus. "
            "Remove the old rusted boiler structures and piping. Keep the tallest concrete smokestack as a landmark. "
            "Replace the industrial plant buildings with a clean modern warehouse-style building with white metal cladding "
            "and a flat roof with solar panels. Add some ground-mounted solar panels in the green field in the foreground. "
            "Keep the power lines and transmission towers in the background exactly as they are. "
            "Keep the Louisiana green grass, the realistic sky, and the general rural industrial feel. "
            "Make it look like a real facility under construction, not a CGI rendering. "
            "Realistic photography, natural lighting."
        ),
    },
    {
        "name": "wg-river-dock-vision",
        "source": "willow-glen-river.jpg",
        "prompt": (
            "Keep this aerial view of the Mississippi River dock mostly the same. "
            "On the land to the right of the dock, add a few large clean modern industrial buildings "
            "with white metal roofing visible in the tree line. Add rows of ground-mounted solar panels "
            "on any visible open land. Keep the river, the dock, the ship, and the transmission towers exactly as they are. "
            "This should look like a realistic active industrial campus along the Mississippi River. "
            "Professional aerial photography."
        ),
    },
]


# ── SCHNELL JOBS (concept art from scratch) ──────────────────────

SCHNELL_JOBS = [
    {
        "name": "wg-gpu-hall-interior",
        "prompt": (
            "Interior of a modern AI compute facility. Long rows of NVIDIA liquid-cooled server racks "
            "with bright green LED status lights. Blue overhead lighting. Clean polished concrete floor. "
            "Visible orange coolant pipes running along the ceiling. Cable trays overhead. "
            "A technician in a hard hat and safety vest walking down the aisle. "
            "Industrial warehouse converted to high-tech use, with exposed steel beams and high ceilings. "
            "Realistic professional interior photography, natural mixed lighting. Not futuristic."
        ),
        "width": 1344,
        "height": 768,
    },
    {
        "name": "wg-solar-farm-louisiana",
        "prompt": (
            "Large ground-mounted solar farm on flat green Louisiana land. Rows of dark blue photovoltaic panels "
            "on metal racking, stretching into the distance. A gravel service road between rows. "
            "In the background, a tall concrete smokestack and some industrial buildings. "
            "Puffy white cumulus clouds in a blue Louisiana sky. Flat terrain, green grass between rows. "
            "A chain-link fence with a gate in the foreground. This is a real industrial solar installation, "
            "not a rendering. Professional photography, afternoon sunlight casting shadows."
        ),
        "width": 1344,
        "height": 768,
    },
    {
        "name": "wg-control-room",
        "prompt": (
            "Modern network operations center inside a converted industrial building. "
            "A wall of large LED monitors showing GPU cluster status, power monitoring, and network maps. "
            "Two engineers seated at workstations with multiple screens. "
            "The room has exposed brick walls and steel beams from the original building. "
            "Clean, professional workspace. Blue and green lighting from the screens. "
            "NVIDIA branding visible on one monitor. Realistic office photography."
        ),
        "width": 1344,
        "height": 768,
    },
    {
        "name": "wg-cooling-infrastructure",
        "prompt": (
            "Industrial cooling water system at a power facility on the Mississippi River. "
            "Large blue cooling pipes running from a pump house to a modern industrial building. "
            "A concrete water intake structure at the river edge with steel grating. "
            "In the background, a large brown muddy river (Mississippi) with a barge passing. "
            "Steel pipe supports, concrete foundations, chain-link fencing. "
            "This is real industrial infrastructure, not a rendering. Louisiana afternoon light. "
            "Professional industrial photography."
        ),
        "width": 1344,
        "height": 768,
    },
    {
        "name": "wg-university-ai-lab",
        "prompt": (
            "University AI research lab with students working at GPU workstations. "
            "Five diverse college students seated at desks with large monitors showing code, "
            "neural network visualizations, and medical imaging scans. "
            "A professor standing at a whiteboard. Modern lab with good lighting. "
            "A window showing green trees outside. LSU purple and gold pennant on the wall. "
            "Realistic university interior photography."
        ),
        "width": 1344,
        "height": 768,
    },
]


async def submit_kontext(client: httpx.AsyncClient, job: dict) -> dict:
    source_path = SOURCE_DIR / job["source"]
    image_b64 = encode_image(source_path)
    payload = {"input": {"prompt": job["prompt"], "image": image_b64}}

    print(f"[KONTEXT] Submitting: {job['name']} (source: {job['source']})")
    resp = await client.post(f"{KONTEXT_ENDPOINT}/run", json=payload, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    job_id = data.get("id", "")
    print(f"[KONTEXT] {job['name']} -> job {job_id}")
    return {"name": job["name"], "job_id": job_id, "endpoint": KONTEXT_ENDPOINT, "type": "kontext"}


async def submit_schnell(client: httpx.AsyncClient, job: dict) -> dict:
    payload = {
        "input": {
            "prompt": job["prompt"],
            "width": job.get("width", 1024),
            "height": job.get("height", 1024),
        }
    }

    print(f"[SCHNELL] Submitting: {job['name']}")
    resp = await client.post(f"{SCHNELL_ENDPOINT}/run", json=payload, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    job_id = data.get("id", "")
    print(f"[SCHNELL] {job['name']} -> job {job_id}")
    return {"name": job["name"], "job_id": job_id, "endpoint": SCHNELL_ENDPOINT, "type": "schnell"}


async def poll_and_download(client: httpx.AsyncClient, job_info: dict) -> str:
    job_id = job_info["job_id"]
    endpoint = job_info["endpoint"]
    name = job_info["name"]

    for attempt in range(90):  # 3 minutes max
        resp = await client.get(f"{endpoint}/status/{job_id}", headers=HEADERS, timeout=20)
        data = resp.json()
        status = data.get("status", "")

        if status == "COMPLETED":
            output = data.get("output", {})
            image_url = None

            if isinstance(output, dict):
                image_url = output.get("image_url") or output.get("image") or output.get("result")
                if isinstance(image_url, list):
                    image_url = image_url[0]
                # Handle base64 result
                if isinstance(image_url, str) and not image_url.startswith("http") and len(image_url) > 1000:
                    import base64 as b64mod
                    img_bytes = b64mod.b64decode(image_url)
                    out_path = OUTPUT_DIR / f"{name}.png"
                    out_path.write_bytes(img_bytes)
                    cost = output.get("cost", 0)
                    print(f"[DONE] {name} -> {out_path} ({len(img_bytes):,} bytes, ${cost})")
                    return str(out_path)
            elif isinstance(output, str) and output.startswith("http"):
                image_url = output

            if not image_url:
                # Try nested
                for key in ("images", "output", "result"):
                    val = output.get(key) if isinstance(output, dict) else None
                    if isinstance(val, list) and val:
                        first = val[0]
                        if isinstance(first, str) and first.startswith("http"):
                            image_url = first
                        elif isinstance(first, dict):
                            image_url = first.get("image_url") or first.get("url")

            if image_url:
                img_resp = await client.get(image_url, timeout=30, follow_redirects=True)
                ext = ".jpg" if "jpeg" in img_resp.headers.get("content-type", "") else ".png"
                out_path = OUTPUT_DIR / f"{name}{ext}"
                out_path.write_bytes(img_resp.content)
                cost = output.get("cost", 0) if isinstance(output, dict) else 0
                print(f"[DONE] {name} -> {out_path} ({len(img_resp.content):,} bytes, ${cost})")
                return str(out_path)
            else:
                print(f"[WARN] {name} completed but no image URL found. Output keys: {list(output.keys()) if isinstance(output, dict) else type(output)}")
                return ""

        elif status == "FAILED":
            error = data.get("error", "unknown")
            print(f"[FAIL] {name}: {error}")
            return ""

        await asyncio.sleep(2)

    print(f"[TIMEOUT] {name}")
    return ""


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as client:
        # Submit all jobs in parallel
        tasks = []
        for job in KONTEXT_JOBS:
            tasks.append(submit_kontext(client, job))
        for job in SCHNELL_JOBS:
            tasks.append(submit_schnell(client, job))

        job_infos = await asyncio.gather(*tasks)

        print(f"\n{'='*60}")
        print(f"Submitted {len(job_infos)} jobs. Polling for results...")
        print(f"{'='*60}\n")

        # Poll all jobs in parallel
        results = await asyncio.gather(*[poll_and_download(client, j) for j in job_infos])

        print(f"\n{'='*60}")
        print("RESULTS:")
        for info, result in zip(job_infos, results):
            status = "OK" if result else "FAILED"
            print(f"  [{status}] {info['name']} ({info['type']})")
        print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
