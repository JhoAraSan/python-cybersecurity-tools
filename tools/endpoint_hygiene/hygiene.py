"""
hygiene.py

Endpoint Hygiene Orchestrator
Runs read-only hygiene checks and aggregates results into a single report.

Supported OS:
- Windows
- Linux (Kali, Debian-based)

Design principles:
- Safe by default
- Read-only checks
- Explicit execution
"""

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent
CHECKS_DIR = BASE_DIR / "checks"


# ----------------------------
# Utility helpers
# ----------------------------

def run_python_check(script: Path) -> dict | None:
    try:
        output = subprocess.check_output(
            [sys.executable, str(script)],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return json.loads(output)
    except Exception as e:
        return {
            "check": script.stem,
            "status": "error",
            "error": str(e)
        }


def run_powershell_check(script: Path) -> dict | None:
    try:
        output = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", str(script)
            ],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return json.loads(output)
    except Exception as e:
        return {
            "check": script.stem,
            "status": "error",
            "error": str(e)
        }


# ----------------------------
# Check registry
# ----------------------------

def get_checks_for_os() -> list[Path]:
    system = platform.system()

    checks = [
        CHECKS_DIR / "temp_files.py",
        CHECKS_DIR / "last_reboot.py",
    ]

    if system == "Windows":
        checks.extend([
            CHECKS_DIR / "disk.ps1",
            CHECKS_DIR / "startup_item.ps1",
            CHECKS_DIR / "services.ps1",
        ])
    else:
        checks.extend([
            CHECKS_DIR / "disk_linux.py",
            CHECKS_DIR / "startup_items_linux.py",
            CHECKS_DIR / "services_linux.py",
        ])

    return [c for c in checks if c.exists()]


# ----------------------------
# Main execution
# ----------------------------

def run_checks(selected: list[str] | None = None) -> dict:
    results = []
    system = platform.system()

    for check in get_checks_for_os():
        if selected and check.stem not in selected:
            continue

        if check.suffix == ".py":
            result = run_python_check(check)
        elif check.suffix == ".ps1" and system == "Windows":
            result = run_powershell_check(check)
        else:
            continue

        if result:
            results.append(result)

    return {
        "hostname": platform.node(),
        "os": system,
        "timestamp_utc": datetime.now().isoformat(timespec="seconds"),
        "checks_executed": len(results),
        "results": results
    }


# ----------------------------
# CLI
# ----------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Endpoint Hygiene Orchestrator (read-only)"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Run hygiene checks (default behavior)"
    )

    parser.add_argument(
        "--only",
        nargs="+",
        help="Run only specific checks (by name)"
    )

    parser.add_argument(
        "--output",
        help="Write output to file (JSON)"
    )

    args = parser.parse_args()

    report = run_checks(selected=args.only)

    output = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[+] Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
