"""
AIDO Omniverse Headless Render
Runs NVIDIA Omniverse Kit in headless mode on RunPod to render frames.

This script is designed to run INSIDE the RunPod container.
On the local machine it validates inputs and prints the remote command.

Usage (on RunPod):
    OMNI_KIT_ALLOW_ROOT=1 python -m aido.render_episode \
        --master-usd output/EP001/usd/EP001_master.usda \
        --out-dir output/EP001/frames \
        --fps 24 \
        --width 1920 \
        --height 1080

Usage (local — just prints the RunPod command):
    python -m aido.render_episode --dry-run --master-usd output/EP001/usd/EP001_master.usda
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger("aido.render")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

# Kit App path — matches RunPod Omniverse pip install layout
_KIT_APP_DEFAULT = "/root/.local/lib/python3.10/site-packages/omni/kit/app/kit"
_KIT_APP_ENV = "OMNI_KIT_APP"

# Extension used for headless batch rendering
_RENDER_EXT = "omni.kit.render.offline"


def _find_kit() -> str | None:
    """Locate the kit executable."""
    env_path = os.environ.get(_KIT_APP_ENV, "")
    if env_path and Path(env_path).exists():
        return env_path
    if Path(_KIT_APP_DEFAULT).exists():
        return _KIT_APP_DEFAULT
    found = shutil.which("kit")
    return found


def render_headless(
    master_usd: str,
    out_dir: str,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    start_frame: int = 0,
    end_frame: int | None = None,
    dry_run: bool = False,
) -> int:
    """
    Invoke Omniverse Kit headless render.
    Returns subprocess returncode (or 0 for dry-run).
    """
    kit = _find_kit()
    if not kit and not dry_run:
        logger.error(
            "Omniverse Kit not found. Set %s or install via: "
            "pip install omniverse-kit",
            _KIT_APP_ENV,
        )
        return 1

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Build Kit command
    cmd = [
        kit or "kit",
        "--ext-folder", "/root/.local/lib/python3.10/site-packages/omni/kit",
        "--enable", _RENDER_EXT,
        "--/renderer/enabled=rtx",
        "--/app/window/width", str(width),
        "--/app/window/height", str(height),
        "--/app/file/path", str(Path(master_usd).resolve()),
        "--/app/renderer/resolution/width", str(width),
        "--/app/renderer/resolution/height", str(height),
        "--/app/render/frameStart", str(start_frame),
        "--/renderer/offline/outputDir", str(out.resolve()),
        "--/renderer/offline/frameNameFormat", "frame_{:06d}.png",
        "--/app/headless/enabled", "true",
        "--no-window",
    ]
    if end_frame is not None:
        cmd += ["--/app/render/frameEnd", str(end_frame)]

    env = os.environ.copy()
    env["OMNI_KIT_ALLOW_ROOT"] = "1"

    if dry_run:
        print("\nDry-run — would execute:")
        print("  " + " \\\n    ".join(cmd))
        print(f"\n  Frames -> {out.resolve()}")
        return 0

    logger.info("Starting Kit headless render...")
    logger.info("  Scene: %s", master_usd)
    logger.info("  Output: %s", out)
    logger.info("  Resolution: %dx%d @ %dfps", width, height, fps)

    result = subprocess.run(cmd, env=env)
    if result.returncode == 0:
        frames = list(out.glob("frame_*.png"))
        logger.info("Render complete. %d frames in %s", len(frames), out)
    else:
        logger.error("Kit exited with code %d", result.returncode)
    return result.returncode


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO Omniverse headless render")
    p.add_argument("--master-usd", required=True, help="Path to master .usda scene")
    p.add_argument("--out-dir", default="output/EP001/frames")
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--start-frame", type=int, default=0)
    p.add_argument("--end-frame", type=int, default=None)
    p.add_argument("--dry-run", action="store_true", help="Print command without running")
    args = p.parse_args()

    rc = render_headless(
        master_usd=args.master_usd,
        out_dir=args.out_dir,
        fps=args.fps,
        width=args.width,
        height=args.height,
        start_frame=args.start_frame,
        end_frame=args.end_frame,
        dry_run=args.dry_run,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
