"""
startup_items_linux.py

Read-only inventory of startup mechanisms on Linux systems.
Checks systemd services and autostart desktop entries.

Designed for endpoint hygiene auditing.
"""

import json
import subprocess
from pathlib import Path


def run_cmd(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return ""


def systemd_services() -> list[dict]:
    output = run_cmd(["systemctl", "list-unit-files", "--type=service", "--state=enabled"])
    services = []

    for line in output.splitlines():
        if line.endswith("enabled"):
            services.append({
                "source": "systemd",
                "name": line.split()[0]
            })

    return services


def autostart_files() -> list[dict]:
    entries = []
    paths = [
        Path("/etc/xdg/autostart"),
        Path.home() / ".config/autostart"
    ]

    for path in paths:
        if path.exists():
            for file in path.glob("*.desktop"):
                entries.append({
                    "source": "autostart",
                    "name": file.name,
                    "path": str(file)
                })

    return entries


def run_check() -> dict:
    items = systemd_services() + autostart_files()

    risk = "low"
    if len(items) > 15:
        risk = "medium"
    if len(items) > 30:
        risk = "high"

    return {
        "check": "startup_items",
        "status": "ok",
        "data": {
            "count": len(items),
            "items": items,
            "risk_level": risk
        }
    }


if __name__ == "__main__":
    print(json.dumps(run_check(), indent=2))
