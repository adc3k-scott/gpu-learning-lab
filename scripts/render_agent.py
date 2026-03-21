"""
ADC Mission Control — Render Agent
FastAPI service that runs on RunPod pod, accepts render jobs, executes Kit SDK headless renders.

Runs on port 8001. Submit jobs via POST /submit_job, check status via GET /job_status/{id}.

Usage (on pod):
    python /workspace/render_agent.py &

Submit from anywhere:
    curl -X POST https://<pod_id>-8001.proxy.runpod.net/submit_job \
         -H 'Content-Type: application/json' \
         -d '{"prompt": "aerial overview of DSX facility", "style": "bright_daylight", "resolution": "1920x1080"}'
"""

import asyncio
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Optional

# --- FastAPI setup (pip install fastapi uvicorn) ---
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel

app = FastAPI(title="ADC Render Agent", version="1.0.0")

# --- Configuration ---
JOBS_DIR = Path("/workspace/jobs")
KIT_BINARY = "/workspace/omniverse-dsx-blueprint/_build/linux-x86_64/release/kit/kit"
KIT_APP = None  # Found at startup
EXT_FOLDERS = [
    "/workspace/omniverse-dsx-blueprint/_build/linux-x86_64/release/extscache",
    "/workspace/omniverse-dsx-blueprint/_build/linux-x86_64/release/kit/extscore",
    "/workspace/exts",
]
DSX_SCENE = "/workspace/dsx-data/DSX_BP/Assembly/DSX_Main_BP.usda"

# --- Camera presets ---
CAMERA_PRESETS = {
    "hero_front": {
        "description": "Elevated front perspective of facility",
        "eye_offset": [0.0, 0.35, 1.8],
        "focal_length": 28.0,
    },
    "hero_quarter": {
        "description": "Classic 3/4 angle showing depth and facade",
        "eye_offset": [1.4, 0.4, 1.4],
        "focal_length": 24.0,
    },
    "aerial_overview": {
        "description": "High aerial showing full facility and site",
        "eye_offset": [0.5, 3.0, 0.8],
        "focal_length": 14.0,
    },
    "side_elevation": {
        "description": "Side profile from ground level",
        "eye_offset": [2.0, 0.25, 0.0],
        "focal_length": 35.0,
    },
    "rear_three_quarter": {
        "description": "Rear 3/4 showing cooling and back facade",
        "eye_offset": [-1.3, 0.4, -1.3],
        "focal_length": 24.0,
    },
    "cooling_infrastructure": {
        "description": "Cooling systems from pulled-back angle",
        "eye_offset": [-1.8, 0.35, 0.5],
        "focal_length": 28.0,
    },
    "power_yard": {
        "description": "Power distribution yard and equipment",
        "eye_offset": [1.5, 0.3, -1.0],
        "focal_length": 28.0,
    },
    "bird_eye_full": {
        "description": "Bird eye view of entire site with terrain",
        "eye_offset": [0.3, 4.0, 0.3],
        "focal_length": 12.0,
    },
    "entry_approach": {
        "description": "Ground-level approach view of main entrance",
        "eye_offset": [0.3, 0.15, 2.2],
        "focal_length": 35.0,
    },
    "panoramic_site": {
        "description": "Wide panoramic showing facility in landscape",
        "eye_offset": [1.0, 1.8, 1.5],
        "focal_length": 14.0,
    },
    "diagonal_high": {
        "description": "Diagonal elevated showing roof and two facades",
        "eye_offset": [1.2, 1.0, 1.2],
        "focal_length": 20.0,
    },
    "equipment_closeup": {
        "description": "Equipment detail from medium distance",
        "eye_offset": [0.8, 0.2, 0.8],
        "focal_length": 50.0,
    },
}

LIGHTING_PRESETS = {
    "bright_daylight": {
        "dome_intensity": 8000,
        "distant_intensity": 5000,
        "distant_angle": 1.0,
        "distant_rotation": [-35, 45, 0],
    },
    "golden_hour": {
        "dome_intensity": 4000,
        "distant_intensity": 6000,
        "distant_angle": 0.5,
        "distant_rotation": [-15, -60, 0],
    },
    "overcast": {
        "dome_intensity": 10000,
        "distant_intensity": 1000,
        "distant_angle": 3.0,
        "distant_rotation": [-60, 0, 0],
    },
    "studio": {
        "dome_intensity": 6000,
        "distant_intensity": 4000,
        "distant_angle": 1.5,
        "distant_rotation": [-45, 30, 0],
    },
    "scene_default": {
        "dome_intensity": 0,
        "distant_intensity": 0,
        "use_scene_lights": True,
    },
}

# --- Job store (in-memory + disk) ---
jobs: dict = {}


class RenderRequest(BaseModel):
    prompt: str = "DSX facility overview"
    style: str = "bright_daylight"
    resolution: str = "1920x1080"
    num_outputs: int = 1
    cameras: Optional[list[str]] = None  # List of preset names, or None for auto-select
    custom_camera: Optional[dict] = None  # {"eye": [x,y,z], "target": [x,y,z], "focal_length": 24}
    lighting: Optional[str] = None  # Preset name, overrides style
    settle_frames: int = 200  # Frames to wait for render convergence
    scene_path: Optional[str] = None  # Override DSX scene


class JobStatus(BaseModel):
    job_id: str
    status: str  # pending, running, complete, failed
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    cameras: list[str] = []
    images: list[str] = []
    errors: list[str] = []
    progress: str = ""


def find_kit_app():
    """Find the omni.app.viewport.kit base app."""
    import glob
    patterns = [
        "/root/.cache/packman/chk/kit-kernel/*/apps/omni.app.viewport.kit",
        "/workspace/omniverse-dsx-blueprint/_build/**/apps/omni.app.viewport.kit",
    ]
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            return matches[0]
    return None


def generate_extension_script(job_id: str, request: RenderRequest) -> str:
    """Generate the Kit extension Python code for this render job."""
    job_dir = JOBS_DIR / job_id
    images_dir = job_dir / "images"

    # Determine cameras
    if request.cameras:
        cam_names = request.cameras
    elif request.custom_camera:
        cam_names = ["custom"]
    else:
        # Auto-select based on prompt keywords
        prompt_lower = request.prompt.lower()
        if "aerial" in prompt_lower or "overview" in prompt_lower or "bird" in prompt_lower:
            cam_names = ["aerial_overview", "bird_eye", "panoramic_wide"]
        elif "power" in prompt_lower or "electrical" in prompt_lower:
            cam_names = ["power_hall_wide", "close_equipment"]
        elif "cool" in prompt_lower or "thermal" in prompt_lower:
            cam_names = ["rear_cooling", "side_elevation"]
        elif "hero" in prompt_lower or "front" in prompt_lower:
            cam_names = ["hero_front", "hero_quarter"]
        elif "all" in prompt_lower or "every" in prompt_lower:
            cam_names = list(CAMERA_PRESETS.keys())
        else:
            cam_names = ["hero_front", "aerial_overview", "hero_quarter",
                         "rear_cooling", "power_hall_wide", "data_hall_interior"]

    # Limit to num_outputs if specified
    if request.num_outputs > 0 and len(cam_names) > request.num_outputs:
        cam_names = cam_names[:request.num_outputs]

    # Get lighting preset
    light_name = request.lighting or request.style
    lighting = LIGHTING_PRESETS.get(light_name, LIGHTING_PRESETS["bright_daylight"])

    # Resolution
    parts = request.resolution.split("x")
    width = int(parts[0]) if len(parts) == 2 else 1920
    height = int(parts[1]) if len(parts) == 2 else 1080

    # Build camera list for the extension
    cam_configs = []
    for name in cam_names:
        if name == "custom" and request.custom_camera:
            cam_configs.append({
                "name": "custom",
                "eye_offset": request.custom_camera.get("eye", [1, 1, 1]),
                "focal_length": request.custom_camera.get("focal_length", 24.0),
                "target_offset": request.custom_camera.get("target", None),
            })
        elif name in CAMERA_PRESETS:
            preset = CAMERA_PRESETS[name]
            cam_configs.append({
                "name": name,
                "eye_offset": preset["eye_offset"],
                "focal_length": preset["focal_length"],
            })

    scene = request.scene_path or DSX_SCENE

    # Generate extension code
    script = f'''import asyncio
import json
import os
import time
import carb
import omni.ext
import omni.usd
import omni.kit.app
import omni.kit.viewport.utility as viewport_util
from pxr import Gf, UsdGeom, UsdLux

SCENE = {scene!r}
OUTPUT_DIR = {str(images_dir)!r}
JOB_ID = {job_id!r}
JOB_DIR = {str(job_dir)!r}
SETTLE_FRAMES = {request.settle_frames}
CAMERAS = {json.dumps(cam_configs)}
LIGHTING = {json.dumps(lighting)}

class RenderJobExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        carb.log_warn(f'Render Agent job {{JOB_ID}} starting')
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self._update_status("running")
        asyncio.ensure_future(self._run())

    def on_shutdown(self):
        pass

    def _update_status(self, status, **kwargs):
        status_file = os.path.join(JOB_DIR, "status.json")
        data = {{"job_id": JOB_ID, "status": status, "updated_at": time.time()}}
        data.update(kwargs)
        if os.path.exists(status_file):
            with open(status_file) as f:
                old = json.load(f)
            old.update(data)
            data = old
        with open(status_file, "w") as f:
            json.dump(data, f)

    async def _run(self):
        kit_app = omni.kit.app.get_app()
        usd_ctx = omni.usd.get_context()

        carb.log_warn(f'Opening scene: {{SCENE}}')
        result, error = await usd_ctx.open_stage_async(SCENE)
        if not result:
            carb.log_error(f'Failed to open scene: {{error}}')
            self._update_status("failed", errors=[f"Scene load failed: {{error}}"])
            kit_app.post_quit()
            return

        carb.log_warn('Scene opened, waiting for hydra...')
        for i in range(SETTLE_FRAMES):
            await kit_app.next_update_async()

        stage = usd_ctx.get_stage()

        # Get building bounding box (NOT terrain root)
        building_prim = stage.GetPrimAtPath('/World/Building')
        if building_prim and building_prim.IsValid():
            bbox_cache = UsdGeom.BBoxCache(0, [UsdGeom.Tokens.default_])
            bbox = bbox_cache.ComputeWorldBound(building_prim)
        else:
            # Fallback: try internal assembly
            internal = stage.GetPrimAtPath('/World/Assembly_Building_Internal')
            if internal and internal.IsValid():
                bbox_cache = UsdGeom.BBoxCache(0, [UsdGeom.Tokens.default_])
                bbox = bbox_cache.ComputeWorldBound(internal)
            else:
                bbox_cache = UsdGeom.BBoxCache(0, [UsdGeom.Tokens.default_])
                bbox = bbox_cache.ComputeWorldBound(stage.GetPseudoRoot())

        bbox_range = bbox.ComputeAlignedRange()
        bbox_min = bbox_range.GetMin()
        bbox_max = bbox_range.GetMax()
        center = (bbox_min + bbox_max) / 2.0
        size = bbox_max - bbox_min
        max_dim = max(size[0], size[1], size[2])
        carb.log_warn(f'Building: center={{center}}, size={{size}}, maxdim={{max_dim}}')

        # Setup lighting
        use_scene = LIGHTING.get("use_scene_lights", False)
        if not use_scene:
            dome_int = LIGHTING.get("dome_intensity", 5000)
            if dome_int > 0:
                dl_path = '/RenderDomeLight'
                if stage.GetPrimAtPath(dl_path):
                    dl_prim = stage.GetPrimAtPath(dl_path)
                else:
                    dl_prim = stage.DefinePrim(dl_path, 'DomeLight')
                UsdLux.DomeLight(dl_prim).GetIntensityAttr().Set(float(dome_int))

            dist_int = LIGHTING.get("distant_intensity", 3000)
            if dist_int > 0:
                dl2_path = '/RenderDistantLight'
                if not stage.GetPrimAtPath(dl2_path):
                    dl2_prim = stage.DefinePrim(dl2_path, 'DistantLight')
                else:
                    dl2_prim = stage.GetPrimAtPath(dl2_path)
                UsdLux.DistantLight(dl2_prim).GetIntensityAttr().Set(float(dist_int))
                UsdLux.DistantLight(dl2_prim).GetAngleAttr().Set(float(LIGHTING.get("distant_angle", 1.0)))
                rot = LIGHTING.get("distant_rotation", [-45, 30, 0])
                xf = UsdGeom.Xformable(dl2_prim)
                xf.ClearXformOpOrder()
                xf.AddRotateXYZOp().Set(Gf.Vec3f(rot[0], rot[1], rot[2]))

        vp = viewport_util.get_active_viewport()
        if vp is None:
            carb.log_error('No viewport')
            self._update_status("failed", errors=["No viewport available"])
            kit_app.post_quit()
            return

        dist = max_dim * 1.0  # Base distance = building size
        completed = []
        errors = []

        for cam_cfg in CAMERAS:
            name = cam_cfg["name"]
            eye_off = cam_cfg["eye_offset"]
            focal = cam_cfg.get("focal_length", 24.0)

            # Compute eye position: offset * dist from center
            eye = center + Gf.Vec3d(eye_off[0] * dist, eye_off[1] * dist, eye_off[2] * dist)

            # Target: center of building (or custom)
            target_off = cam_cfg.get("target_offset")
            if target_off:
                target = center + Gf.Vec3d(target_off[0] * dist, target_off[1] * dist, target_off[2] * dist)
            else:
                target = Gf.Vec3d(center[0], center[1], center[2])

            cam_path = f'/RenderCam_{{name}}'
            if stage.GetPrimAtPath(cam_path):
                cam_prim = stage.GetPrimAtPath(cam_path)
            else:
                cam_prim = stage.DefinePrim(cam_path, 'Camera')
            cam = UsdGeom.Camera(cam_prim)
            cam.GetFocalLengthAttr().Set(float(focal))
            cam.GetClippingRangeAttr().Set(Gf.Vec2f(0.1, max_dim * 50))

            forward = (target - eye).GetNormalized()
            right = Gf.Cross(forward, Gf.Vec3d(0, 1, 0)).GetNormalized()
            up = Gf.Cross(right, forward).GetNormalized()

            mat = Gf.Matrix4d()
            mat.SetRow(0, Gf.Vec4d(right[0], right[1], right[2], 0))
            mat.SetRow(1, Gf.Vec4d(up[0], up[1], up[2], 0))
            mat.SetRow(2, Gf.Vec4d(-forward[0], -forward[1], -forward[2], 0))
            mat.SetRow(3, Gf.Vec4d(eye[0], eye[1], eye[2], 1))

            xf = UsdGeom.Xformable(cam_prim)
            xf.ClearXformOpOrder()
            xf.AddTransformOp().Set(mat)
            vp.set_active_camera(cam_path)

            carb.log_warn(f'Camera {{name}}: eye={{eye}}, focal={{focal}}')

            # Wait for render to converge
            for i in range(SETTLE_FRAMES):
                await kit_app.next_update_async()

            out_path = f'{{OUTPUT_DIR}}/{{name}}.png'
            try:
                viewport_util.capture_viewport_to_file(vp, out_path)
                carb.log_warn(f'Capture requested: {{out_path}}')
            except Exception as e:
                carb.log_error(f'Capture failed for {{name}}: {{e}}')
                errors.append(f'{{name}}: {{str(e)}}')
                continue

            # Wait for async file write
            for i in range(120):
                await kit_app.next_update_async()

            if os.path.exists(out_path):
                sz = os.path.getsize(out_path)
                carb.log_warn(f'VERIFIED: {{out_path}} ({{sz}} bytes)')
                completed.append(name)
            else:
                carb.log_error(f'FILE NOT FOUND: {{out_path}}')
                errors.append(f'{{name}}: file not written')

            self._update_status("running", progress=f'{{len(completed)}}/{{len(CAMERAS)}} cameras done',
                              images=[f'{{name}}.png' for name in completed])

        self._update_status("complete",
                          images=[f'{{name}}.png' for name in completed],
                          errors=errors,
                          completed_at=time.time())
        carb.log_warn(f'Job {{JOB_ID}} complete: {{len(completed)}} images, {{len(errors)}} errors')

        for i in range(150):
            await kit_app.next_update_async()
        kit_app.post_quit()
'''
    return script


def write_extension_package(job_id: str, script: str):
    """Write the Kit extension package for this job."""
    ext_dir = JOBS_DIR / job_id / "ext" / "omni.render.job" / "omni" / "render" / "job"
    ext_dir.mkdir(parents=True, exist_ok=True)

    # __init__.py with the render script
    (ext_dir / "__init__.py").write_text(script)

    # Namespace packages
    (ext_dir.parent / "__init__.py").write_text("")
    (ext_dir.parent.parent / "__init__.py").write_text("")

    # extension.toml
    toml_dir = ext_dir.parent.parent.parent
    (toml_dir / "extension.toml").write_text("""[package]
version = "1.0.0"
title = "Render Job"

[dependencies]
"omni.usd" = {}
"omni.kit.viewport.utility" = {}
"omni.kit.commands" = {}

[[python.module]]
name = "omni.render.job"
""")

    return str(toml_dir.parent)  # Return ext folder path


async def run_kit_job(job_id: str, request: RenderRequest):
    """Launch Kit SDK to execute a render job."""
    global KIT_APP

    job_dir = JOBS_DIR / job_id
    log_file = job_dir / "kit.log"

    # Generate and write extension
    script = generate_extension_script(job_id, request)
    ext_folder = write_extension_package(job_id, script)

    # Find Kit app if not cached
    if not KIT_APP:
        KIT_APP = find_kit_app()
    if not KIT_APP:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["errors"] = ["Kit app (omni.app.viewport.kit) not found"]
        return

    # Build Kit command
    cmd = [
        KIT_BINARY,
        *[arg for folder in EXT_FOLDERS for arg in ["--ext-folder", folder]],
        "--ext-folder", ext_folder,
        "--enable", "omni.hydra.rtx",
        "--enable", "omni.kit.renderer.capture",
        "--enable", "omni.render.job",
        "--enable", "omni.mdl",
        "--enable", "omni.mdl.neuraylib",
        "--enable", "omni.kit.viewport.window",
        KIT_APP,
    ]

    env = os.environ.copy()
    env["DISPLAY"] = ":99"
    env["OMNI_KIT_ALLOW_ROOT"] = "1"
    env["OMNI_KIT_ACCEPT_EULA"] = "yes"

    jobs[job_id]["status"] = "running"
    jobs[job_id]["started_at"] = time.time()

    # Write job metadata
    with open(job_dir / "request.json", "w") as f:
        json.dump(request.model_dump(), f, indent=2)

    # Launch Kit as subprocess
    with open(log_file, "w") as lf:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=lf,
            stderr=asyncio.subprocess.STDOUT,
            env=env,
        )
        await proc.wait()

    # Read status from disk (written by extension)
    status_file = job_dir / "status.json"
    if status_file.exists():
        with open(status_file) as f:
            disk_status = json.load(f)
        jobs[job_id].update(disk_status)
    else:
        # Kit crashed or didn't write status
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["errors"] = ["Kit process exited without writing status"]

    jobs[job_id]["completed_at"] = time.time()

    # List actual output images
    images_dir = job_dir / "images"
    if images_dir.exists():
        jobs[job_id]["images"] = [f.name for f in images_dir.iterdir() if f.suffix == ".png"]


# --- API Endpoints ---

@app.get("/")
async def root():
    return {
        "service": "ADC Render Agent",
        "version": "1.0.0",
        "endpoints": ["/submit_job", "/job_status/{id}", "/results/{id}", "/presets", "/jobs"],
        "kit_binary": os.path.exists(KIT_BINARY),
        "scene": os.path.exists(DSX_SCENE),
    }


@app.get("/presets")
async def get_presets():
    return {
        "cameras": {k: v["description"] for k, v in CAMERA_PRESETS.items()},
        "lighting": list(LIGHTING_PRESETS.keys()),
    }


@app.post("/submit_job")
async def submit_job(request: RenderRequest):
    job_id = str(uuid.uuid4())[:8]
    job_dir = JOBS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "images").mkdir(exist_ok=True)

    # Determine cameras that will be used
    if request.cameras:
        cam_names = request.cameras
    elif request.custom_camera:
        cam_names = ["custom"]
    else:
        prompt_lower = request.prompt.lower()
        if "aerial" in prompt_lower or "overview" in prompt_lower:
            cam_names = ["aerial_overview", "bird_eye", "panoramic_wide"]
        elif "power" in prompt_lower or "electrical" in prompt_lower:
            cam_names = ["power_hall_wide", "close_equipment"]
        elif "cool" in prompt_lower or "thermal" in prompt_lower:
            cam_names = ["rear_cooling", "side_elevation"]
        elif "hero" in prompt_lower or "front" in prompt_lower:
            cam_names = ["hero_front", "hero_quarter"]
        elif "all" in prompt_lower:
            cam_names = list(CAMERA_PRESETS.keys())
        else:
            cam_names = ["hero_front", "aerial_overview", "hero_quarter",
                         "rear_cooling", "power_hall_wide", "data_hall_interior"]

    if request.num_outputs > 0 and len(cam_names) > request.num_outputs:
        cam_names = cam_names[:request.num_outputs]

    job_data = {
        "job_id": job_id,
        "status": "pending",
        "created_at": time.time(),
        "cameras": cam_names,
        "images": [],
        "errors": [],
        "progress": "queued",
    }
    jobs[job_id] = job_data

    # Launch Kit in background
    asyncio.create_task(run_kit_job(job_id, request))

    return {"job_id": job_id, "status": "pending", "cameras": cam_names,
            "message": f"Render job submitted. {len(cam_names)} cameras queued."}


@app.get("/job_status/{job_id}")
async def job_status(job_id: str):
    if job_id not in jobs:
        # Try loading from disk
        status_file = JOBS_DIR / job_id / "status.json"
        if status_file.exists():
            with open(status_file) as f:
                return json.load(f)
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    # Merge with disk status if available
    status_file = JOBS_DIR / job_id / "status.json"
    if status_file.exists():
        with open(status_file) as f:
            disk = json.load(f)
        job.update(disk)

    return job


@app.get("/results/{job_id}")
async def get_results(job_id: str):
    images_dir = JOBS_DIR / job_id / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    images = [f.name for f in images_dir.iterdir() if f.suffix == ".png"]
    return {
        "job_id": job_id,
        "images": images,
        "urls": [f"/image/{job_id}/{img}" for img in images],
    }


@app.get("/image/{job_id}/{filename}")
async def get_image(job_id: str, filename: str):
    filepath = JOBS_DIR / job_id / "images" / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(str(filepath), media_type="image/png")


@app.get("/jobs")
async def list_jobs():
    result = []
    for jid, data in sorted(jobs.items(), key=lambda x: x[1].get("created_at", 0), reverse=True):
        result.append({
            "job_id": jid,
            "status": data.get("status", "unknown"),
            "cameras": len(data.get("cameras", [])),
            "images": len(data.get("images", [])),
            "created_at": data.get("created_at"),
        })
    return result


@app.get("/log/{job_id}")
async def get_log(job_id: str):
    log_file = JOBS_DIR / job_id / "kit.log"
    if not log_file.exists():
        raise HTTPException(status_code=404, detail="Log not found")
    # Return last 100 lines
    lines = log_file.read_text().split("\n")
    return {"job_id": job_id, "log_lines": lines[-100:]}


if __name__ == "__main__":
    import uvicorn

    # Find Kit app at startup
    KIT_APP = find_kit_app()
    print(f"Kit binary: {KIT_BINARY} ({'OK' if os.path.exists(KIT_BINARY) else 'MISSING'})")
    print(f"Kit app: {KIT_APP or 'NOT FOUND'}")
    print(f"DSX scene: {DSX_SCENE} ({'OK' if os.path.exists(DSX_SCENE) else 'MISSING'})")
    print(f"Jobs dir: {JOBS_DIR}")
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    uvicorn.run(app, host="0.0.0.0", port=8501)
