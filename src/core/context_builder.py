from pathlib import Path
from .repo_scanner import scan_project

# Files to include first in the context prompt
PRIORITY_FILES = ['README.md', 'requirements.txt', 'main.py']


def build_system_context(project_root: Path) -> str:
    """Build a system prompt that gives Claude full project context."""
    scan = scan_project(project_root)
    files = scan['files']

    parts = [
        "You are an AI coding assistant with complete knowledge of this repository.",
        "",
        "## Project",
        "gpu-learning-lab — CUDA, GPU Computing, RunPod experiments, and Nvidia accelerated"
        " computing tutorials.",
        "",
        "## Directory Structure",
        "```",
        scan['structure'],
        "```",
        "",
        "## File Contents",
    ]

    # Emit priority files first, then everything else
    seen = set()
    for fname in PRIORITY_FILES:
        for rel_path, content in files.items():
            if rel_path == fname or rel_path.endswith(f"/{fname}") or rel_path.endswith(f"\\{fname}"):
                parts += [f"### {rel_path}", "```", content.rstrip(), "```", ""]
                seen.add(rel_path)
                break

    for rel_path, content in files.items():
        if rel_path not in seen:
            parts += [f"### {rel_path}", "```", content.rstrip(), "```", ""]

    parts += [
        "## Your Capabilities",
        "- Explain what this project does and how it is organised",
        "- Answer questions about specific files or code sections",
        "- Suggest code improvements, bug fixes, and best practices",
        "- Help the user understand GPU/CUDA and RunPod concepts shown in the project",
    ]

    return "\n".join(parts)
