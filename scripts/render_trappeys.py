"""
Trappeys Ragin' Cajun Compute Campus — Renderings
Kontext edits on real photos — RESTORATION not futuristic
"""
import asyncio
import base64
import httpx
import os
import time
from pathlib import Path

API_KEY = os.environ.get("RUNPOD_API_KEY", "")
KONTEXT_ENDPOINT = "https://api.runpod.ai/v2/black-forest-labs-flux-1-kontext-dev"
OUTPUT_DIR = Path("adc3k-deploy/renders")
SOURCE_DIR = Path("adc3k-deploy/trappeys-photos")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


KONTEXT_JOBS = [
    {
        "name": "trappeys-front-restored",
        "source": "Front5.jpg",
        "prompt": (
            "Restore this historic brick building viewed from across a small brown Louisiana bayou. "
            "Keep the exact same brick building, same roof shape, same windows, same structure. "
            "Repair the seawall along the waterfront — clean concrete or stone seawall replacing the crumbling wooden pilings. "
            "Clean up the brick facade — repoint the mortar, make the bricks look maintained but still historic. "
            "Restore all the windows — clean glass, no broken panes. "
            "Remove the dead trees and overgrowth from in front of the building. Add a few healthy green trees. "
            "Keep the brown bayou water in front — this is a small bayou, not a river. Keep it calm and narrow. "
            "Add solar panels on the flat roof sections only — dark blue panels, not covering the whole roof. "
            "Keep the dramatic Louisiana sky with clouds. "
            "This is a restoration, not a redesign. Same building, just repaired and maintained. "
            "Realistic photography, natural afternoon lighting. Not futuristic. Not CGI."
        ),
    },
    {
        "name": "trappeys-front-wide",
        "source": "Front2.jpg",
        "prompt": (
            "Restore this wider view of the historic brick building from across the brown bayou. "
            "Keep the exact same brick buildings, same rooflines, same overall structure. "
            "Repair the seawall — clean concrete replacing the rotting wood pilings along the water edge. "
            "Clean up the brick — repointed mortar, maintained look, still historic red brick. "
            "Fix all windows — clean glass, intact frames. "
            "Remove dead branches and overgrown vegetation blocking the view. Keep a few healthy green trees. "
            "Keep the brown bayou water — small, calm, Louisiana bayou. Not a big river. "
            "Add subtle solar panels on the flat roof section. "
            "Keep the overcast Louisiana sky. "
            "Restoration only. Same buildings. Just cleaned up, repaired, and maintained. "
            "Realistic photography. Not futuristic."
        ),
    },
    {
        "name": "trappeys-watertower-restored",
        "source": "WT1.jpg",
        "prompt": (
            "Restore this scene showing a water tower next to a historic brick warehouse building. "
            "Keep the water tower exactly as it is — same shape, same size. Clean it up — fresh white paint, no graffiti. "
            "Keep the brick warehouse building — same structure, same roof pitch. Repair the brick, fix the windows, "
            "replace the damaged metal siding sections. Remove the debris and scrap metal on the ground. "
            "Clean green grass, maintained landscaping. Remove the small shed structures and clutter in front. "
            "Add a paved parking area or clean gravel where the debris was. "
            "Add solar panels on the roof of the warehouse — dark blue, flat mounted. "
            "Keep the dramatic cloudy Louisiana sky. "
            "This is a restoration of an abandoned industrial site. Same buildings, just repaired and cleaned up. "
            "Realistic photography, natural lighting. Not futuristic."
        ),
    },
    {
        "name": "trappeys-warehouse-interior",
        "source": "Rear_warehouse1.jpg",
        "prompt": (
            "Transform this empty industrial warehouse interior into a working AI compute facility. "
            "Keep the same steel beam structure, same ceiling height, same general space. "
            "Clean the concrete floor — patch and seal it, make it smooth and clean. "
            "Add rows of modern black server racks down the center of the space with green LED status lights. "
            "Add bright LED overhead lighting replacing the old fluorescent fixtures. "
            "Add blue cooling pipes running along the ceiling between the steel beams. "
            "Keep the skylights — clean the glass so natural light comes through. "
            "Add cable trays along the ceiling carrying fiber optic cables. "
            "This is a converted industrial warehouse, not a purpose-built facility. "
            "The original steel structure and skylights should still be visible. "
            "Realistic interior photography. Industrial conversion, not a sci-fi movie set."
        ),
    },
    {
        "name": "trappeys-entrance-restored",
        "source": "Middle1.jpg",
        "prompt": (
            "Restore this view of the front entrance and loading dock area of a historic brick cannery. "
            "Keep the same brick buildings with the hip roof on the left and the sawtooth roof on the right. "
            "Repair the brick on both buildings — clean, repointed mortar, maintained historic look. "
            "Replace the rusty roll-up doors with clean new ones. "
            "Repave the concrete loading area — clean, smooth concrete with painted parking lines. "
            "Add a few parked vehicles — work trucks or SUVs. "
            "Clean up the weeds growing through the concrete. "
            "Add a small sign near the entrance. "
            "Keep the power lines and utility poles — they're part of the setting. "
            "Keep the Louisiana overcast sky. "
            "This is a working industrial campus, not a corporate office park. Clean but industrial. "
            "Realistic photography, natural lighting."
        ),
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
    return {"name": job["name"], "job_id": job_id, "endpoint": KONTEXT_ENDPOINT}


async def poll_and_download(client: httpx.AsyncClient, job_info: dict) -> str:
    job_id = job_info["job_id"]
    endpoint = job_info["endpoint"]
    name = job_info["name"]

    for attempt in range(90):
        resp = await client.get(f"{endpoint}/status/{job_id}", headers=HEADERS, timeout=20)
        data = resp.json()
        status = data.get("status", "")

        if status == "COMPLETED":
            output = data.get("output", {})
            image_data = None

            if isinstance(output, dict):
                result = output.get("image_url") or output.get("image") or output.get("result")
                if isinstance(result, str):
                    if result.startswith("http"):
                        img_resp = await client.get(result, timeout=30, follow_redirects=True)
                        image_data = img_resp.content
                    elif len(result) > 1000:
                        import base64 as b64mod
                        image_data = b64mod.b64decode(result)

            if image_data:
                out_path = OUTPUT_DIR / f"{name}.jpg"
                out_path.write_bytes(image_data)
                cost = output.get("cost", 0) if isinstance(output, dict) else 0
                print(f"[DONE] {name} -> {out_path} ({len(image_data):,} bytes, ${cost})")
                return str(out_path)
            else:
                print(f"[WARN] {name} completed but no image found. Keys: {list(output.keys()) if isinstance(output, dict) else type(output)}")
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

    if not API_KEY:
        print("ERROR: RUNPOD_API_KEY not set")
        return

    async with httpx.AsyncClient() as client:
        tasks = [submit_kontext(client, job) for job in KONTEXT_JOBS]
        job_infos = await asyncio.gather(*tasks)

        print(f"\nSubmitted {len(job_infos)} jobs. Polling...\n")

        results = await asyncio.gather(*[poll_and_download(client, j) for j in job_infos])

        print(f"\nRESULTS:")
        for info, result in zip(job_infos, results):
            status = "OK" if result else "FAILED"
            print(f"  [{status}] {info['name']}")


if __name__ == "__main__":
    asyncio.run(main())
