"""
last_reboot.py

Read-only check to determine last system reboot and current uptime.
Designed for endpoint hygiene and operational security monitoring.

Requires:
- psutil
"""

import psutil # pip install psutil
from datetime import datetime, timezone


def calculate_risk(uptime_days: float) -> str:
    """
    Classify risk level based on uptime.
    """
    if uptime_days < 7:
        return "low"
    elif uptime_days < 30:
        return "medium"
    return "high"


def run_check() -> dict:
    """
    Execute last reboot check.
    Returns structured, JSON-serializable output.
    """
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp, tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    uptime_seconds = (now - boot_time).total_seconds()
    uptime_days = round(uptime_seconds / 86400, 2)

    return {
        "check": "last_reboot",
        "status": "ok",
        "data": {
            "risk_level": calculate_risk(uptime_days),
            "last_boot_utc": boot_time.isoformat(timespec="seconds"),
            "uptime_days": uptime_days
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_check(), indent=2))
