"""
services_linux.py

Read-only inventory of running services on Linux systems.
Uses systemd to collect active services.

Designed for endpoint hygiene auditing.
"""

import json
import subprocess


def run_cmd(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return ""


def get_running_services() -> list[dict]:
    output = run_cmd([
        "systemctl",
        "list-units",
        "--type=service",
        "--state=running",
        "--no-pager"
    ])

    services = []

    for line in output.splitlines():
        if ".service" in line:
            parts = line.split()
            services.append({
                "name": parts[0],
                "load": parts[1],
                "active": parts[2],
                "sub": parts[3]
            })

    return services


def run_check() -> dict:
    services = get_running_services()

    risk = "low"
    if len(services) > 80:
        risk = "medium"
    if len(services) > 120:
        risk = "high"

    return {
        "check": "services",
        "status": "ok",
        "data": {
            "running_services": len(services),
            "services": services,
            "risk_level": risk
        }
    }


if __name__ == "__main__":
    print(json.dumps(run_check(), indent=2))
