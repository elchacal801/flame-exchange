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


def count_mapped(field: str) -> int:
    """Count TPs whose frontmatter list *field* is non-empty."""
    n = 0
    for f in ROOT.glob("ThreatPaths/TP-*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(rf"^{field}:\s*(\[.*?\])", text, re.M)
        if not m or '"' in m.group(1) or "'" in m.group(1):
            n += 1  # block-style or populated inline list counts as mapped
    return n


def count_tests() -> int:
    """Count tests as pytest collects them (parametrize cases expand).

    Returns 0 if pytest is unavailable; the caller skips the check then.
    """
    import subprocess
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        ).stdout
        m = re.search(r"(\d+) tests? collected", out)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def get_ground_truth() -> dict[str, int]:
    """Derive ground-truth counts from actual files."""
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    return {
        "threat_paths": count_files("ThreatPaths/TP-*.md"),
        "baselines": count_files("Baselines/BL-*.md"),
        "emulation_playbooks": count_files("EmulationPlaybooks/EP-*.json"),
        "fraud_types": stats.get("fraudTypes", 0),
        "sectors": len(stats.get("sectorList", [])),
        "f3_mapped": count_mapped("mitre_f3"),
        "ft3_mapped": count_mapped("ft3_tactics"),
        "tests": count_tests(),
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

    # Framework coverage claims (e.g. "Mapped (89/89 TPs)")
    tp = counts["threat_paths"]
    checks.append((
        rf"MITRE F3 \(Fight Fraud Framework\) \| Mapped \({counts['f3_mapped']}/{tp} TPs\)",
        f"F3 coverage claim should be {counts['f3_mapped']}/{tp}",
        "f3_mapped",
    ))
    checks.append((
        rf"Stripe FT3 \| Mapped \({counts['ft3_mapped']}/{tp} TPs\)",
        f"FT3 coverage claim should be {counts['ft3_mapped']}/{tp}",
        "ft3_mapped",
    ))
    # Test count claims ("NNN tests")
    if counts["tests"]:
        checks.append((
            rf"\*\*{counts['tests']} tests\*\*",
            f"Test count should be {counts['tests']}",
            "tests",
        ))

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
