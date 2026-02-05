"""
temp_files.py

Read-only check to measure temporary files usage on the system.
Designed for endpoint hygiene auditing (safe by default).

Supported OS:
- Windows
- Linux (Kali, Ubuntu, etc.)

This module does NOT delete any files.
"""

import os
import tempfile
import platform
from pathlib import Path


def get_dir_size(path: Path) -> int:
    """
    Calculate directory size in bytes.
    Silently skips files/directories without access.
    """
    total_size = 0

    if not path.exists():
        return 0

    for root, _, files in os.walk(path, onerror=lambda e: None):
        for name in files:
            try:
                file_path = Path(root) / name
                total_size += file_path.stat().st_size
            except (PermissionError, FileNotFoundError):
                continue

    return total_size


def collect_temp_paths() -> dict:
    """
    Collect relevant temporary directories based on OS.
    """
    paths = {}

    # Cross-platform temp directory
    paths["system_temp"] = Path(tempfile.gettempdir())

    if platform.system() == "Windows":
        paths["windows_temp"] = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Temp"
    else:
        paths["var_tmp"] = Path("/var/tmp")
        paths["tmp"] = Path("/tmp")

    return paths


def run_check() -> dict:
    """
    Execute temp files size check.
    Returns structured, JSON-serializable output.
    """
    temp_paths = collect_temp_paths()
    results = {}

    total_bytes = 0

    for name, path in temp_paths.items():
        size = get_dir_size(path)
        results[name] = {
            "path": str(path),
            "size_mb": round(size / (1024 * 1024), 2)
        }
        total_bytes += size

    return {
        "check": "temp_files",
        "status": "ok",
        "data": {
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "locations": results
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_check(), indent=2))
