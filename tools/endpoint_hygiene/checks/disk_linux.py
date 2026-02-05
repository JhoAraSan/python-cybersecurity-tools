"""
disk_type_linux.py

Read-only check to detect disk type (SSD / HDD) on Linux systems.
Uses kernel-provided information from /sys/block.

Designed for endpoint hygiene auditing.
"""

import json
from pathlib import Path


SYS_BLOCK = Path("/sys/block")


def is_rotational(device: str) -> bool | None:
    """
    Returns True if disk is rotational (HDD),
    False if non-rotational (SSD/NVMe),
    None if information is unavailable.
    """
    rotational_file = SYS_BLOCK / device / "queue" / "rotational"
    try:
        return rotational_file.read_text().strip() == "1"
    except FileNotFoundError:
        return None


def get_disks() -> list[dict]:
    disks = []

    for dev in SYS_BLOCK.iterdir():
        # Skip loop devices and RAM disks
        if dev.name.startswith(("loop", "ram")):
            continue

        rotational = is_rotational(dev.name)

        disks.append({
            "device": dev.name,
            "type": (
                "HDD" if rotational
                else "SSD/NVMe" if rotational is False
                else "unknown"
            )
        })

    return disks


def calculate_risk(disks: list[dict]) -> str:
    if any(d["type"] == "HDD" for d in disks):
        return "medium"
    return "low"


def run_check() -> dict:
    disks = get_disks()

    return {
        "check": "disk_type",
        "status": "ok",
        "data": {
            "disks": disks,
            "risk_level": calculate_risk(disks)
        }
    }


if __name__ == "__main__":
    print(json.dumps(run_check(), indent=2))
