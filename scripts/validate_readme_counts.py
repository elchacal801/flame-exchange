#!/usr/bin/env python3
"""Validate that README.md counts match ground-truth file counts.

Exits non-zero if any count in README.md drifts from the actual file counts.
Designed to run in CI to prevent stale documentation.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
STATS = ROOT / "database" / "flame-stats.json"


def count_files(pattern: str) -> int:
    """Count files matching a glob pattern relative to repo root."""
    return len(list(ROOT.glob(pattern)))


def get_ground_truth() -> dict[str, int]:
    """Derive ground-truth counts from actual files."""
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    return {
        "threat_paths": count_files("ThreatPaths/TP-*.md"),
        "detection_rules": count_files("DetectionLogic/DL-*.yml"),
        "baselines": count_files("Baselines/BL-*.md"),
        "emulation_playbooks": count_files("EmulationPlaybooks/EP-*.json"),
        "fraud_types": stats.get("fraudTypes", 0),
        "sectors": len(stats.get("sectorList", [])),
    }


def check_readme(counts: dict[str, int]) -> list[str]:
    """Check README.md for stale counts. Returns list of errors."""
    readme = README.read_text(encoding="utf-8")
    errors = []

    # Patterns to check: badge values, At a Glance table, and prose mentions.
    checks = [
        # Badges
        (
            rf"threat_paths-{counts['threat_paths']}-",
            f"Threat paths badge should show {counts['threat_paths']}",
            "threat_paths",
        ),
        # At a Glance table — threat paths row
        (
            rf"\*\*Threat Paths\*\*\s*\|\s*{counts['threat_paths']}",
            f"At a Glance: Threat Paths should be {counts['threat_paths']}",
            "threat_paths",
        ),
        # Threat Path Collection prose
        (
            rf"\*\*{counts['threat_paths']} threat paths\*\*",
            f"Threat Path Collection should say {counts['threat_paths']}",
            "threat_paths",
        ),
        # At a Glance — fraud types
        (
            rf"\*\*Fraud Types\*\*\s*\|\s*{counts['fraud_types']}",
            f"At a Glance: Fraud Types should be {counts['fraud_types']}",
            "fraud_types",
        ),
        # At a Glance — baselines
        (
            rf"\*\*Baselines\*\*\s*\|\s*{counts['baselines']}",
            f"At a Glance: Baselines should be {counts['baselines']}",
            "baselines",
        ),
        # At a Glance — emulation playbooks
        (
            rf"\*\*Emulation Playbooks\*\*\s*\|\s*{counts['emulation_playbooks']}",
            f"At a Glance: Emulation Playbooks should be {counts['emulation_playbooks']}",
            "emulation_playbooks",
        ),
        # At a Glance — sectors
        (
            rf"\*\*Sectors Covered\*\*\s*\|\s*{counts['sectors']}",
            f"At a Glance: Sectors should be {counts['sectors']}",
            "sectors",
        ),
    ]

    for pattern, message, key in checks:
        if not re.search(pattern, readme):
            errors.append(f"FAIL: {message} (actual: {counts[key]})")

    return errors


def main():
    counts = get_ground_truth()
    print("Ground-truth counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print()

    errors = check_readme(counts)
    if errors:
        print("README count validation FAILED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("README count validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
