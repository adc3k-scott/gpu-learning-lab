import os
from pathlib import Path

SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache', '.mypy_cache'}
TEXT_EXTENSIONS = {'.py', '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.cfg', '.env.example'}
MAX_FILE_SIZE = 50_000  # 50 KB


def scan_project(root: Path) -> dict:
    """Walk the project tree and return its structure and readable file contents."""
    structure_lines = []
    files = {}

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune directories we don't want to descend into
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith('.')
        )

        rel_dir = Path(dirpath).relative_to(root)
        depth = len(rel_dir.parts)
        indent = "  " * depth
        label = str(rel_dir) if str(rel_dir) != "." else "."
        structure_lines.append(f"{indent}{label}/")

        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            structure_lines.append(f"{indent}  {fname}")

            rel_path = str(fpath.relative_to(root))
            suffix = fpath.suffix.lower()
            try:
                size = fpath.stat().st_size
            except OSError:
                continue

            if suffix in TEXT_EXTENSIONS and size <= MAX_FILE_SIZE:
                try:
                    files[rel_path] = fpath.read_text(encoding='utf-8', errors='replace')
                except OSError:
                    pass

    return {'structure': '\n'.join(structure_lines), 'files': files}
