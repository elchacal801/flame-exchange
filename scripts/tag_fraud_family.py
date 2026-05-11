#!/usr/bin/env python3
"""Tag all 89 threat paths with fraud_family and primary_phase frontmatter."""

import re
import os

# Classification mapping: TP-ID -> (fraud_family, primary_phase)
CLASSIFICATIONS = {
    "TP-0001": ("account-takeover", "P3"),
    "TP-0002": ("payment-wire", "P4"),
    "TP-0003": ("identity-synthetic", "P3"),
    "TP-0004": ("payment-wire", "P4"),
    "TP-0005": ("insurance-healthcare", "P3"),
    "TP-0006": ("payment-wire", "P4"),
    "TP-0007": ("payment-wire", "P4"),
    "TP-0008": ("account-takeover", "P2"),
    "TP-0009": ("payment-wire", "P4"),
    "TP-0010": ("insurance-healthcare", "P4"),
    "TP-0011": ("investment-romance", "P3"),
    "TP-0012": ("social-engineering", "P4"),
    "TP-0013": ("account-takeover", "P2"),
    "TP-0014": ("account-takeover", "P3"),
    "TP-0015": ("social-engineering", "P3"),
    "TP-0016": ("identity-synthetic", "P4"),
    "TP-0017": ("investment-romance", "P3"),
    "TP-0018": ("identity-synthetic", "P2"),
    "TP-0019": ("identity-synthetic", "P2"),
    "TP-0020": ("payment-wire", "P4"),
    "TP-0021": ("insurance-healthcare", "P4"),
    "TP-0022": ("identity-synthetic", "P4"),
    "TP-0023": ("account-takeover", "P2"),
    "TP-0024": ("payment-wire", "P4"),
    "TP-0025": ("social-engineering", "P3"),
    "TP-0026": ("investment-romance", "P3"),
    "TP-0027": ("social-engineering", "P4"),
    "TP-0028": ("insurance-healthcare", "P4"),
    "TP-0029": ("identity-synthetic", "P2"),
    "TP-0030": ("retail-ecommerce", "P3"),
    "TP-0031": ("retail-ecommerce", "P4"),
    "TP-0032": ("crypto-laundering", "P4"),
    "TP-0033": ("identity-synthetic", "P3"),
    "TP-0034": ("state-geopolitical", "P2"),
    "TP-0035": ("fraud-infrastructure", "P2"),
    "TP-0036": ("retail-ecommerce", "P3"),
    "TP-0037": ("account-takeover", "P4"),
    "TP-0038": ("fraud-infrastructure", "P3"),
    "TP-0039": ("retail-ecommerce", "P4"),
    "TP-0040": ("retail-ecommerce", "P3"),
    "TP-0041": ("fraud-infrastructure", "P1"),
    "TP-0042": ("fraud-infrastructure", "P1"),
    "TP-0043": ("fraud-infrastructure", "P1"),
    "TP-0044": ("state-geopolitical", "P1"),
    "TP-0045": ("state-geopolitical", "P3"),
    "TP-0046": ("state-geopolitical", "P1"),
    "TP-0047": ("state-geopolitical", "P1"),
    "TP-0048": ("fraud-infrastructure", "P1"),
    "TP-0049": ("crypto-laundering", "P5"),
    "TP-0050": ("social-engineering", "P2"),
    "TP-0051": ("social-engineering", "P2"),
    "TP-0052": ("investment-romance", "P3"),
    "TP-0053": ("identity-synthetic", "P4"),
    "TP-0054": ("fraud-infrastructure", "P1"),
    "TP-0055": ("crypto-laundering", "P5"),
    "TP-0056": ("insurance-healthcare", "P4"),
    "TP-0057": ("fraud-infrastructure", "P1"),
    "TP-0058": ("fraud-infrastructure", "P1"),
    "TP-0059": ("fraud-infrastructure", "P2"),
    "TP-0060": ("fraud-infrastructure", "P1"),
    "TP-0061": ("fraud-infrastructure", "P1"),
    "TP-0062": ("social-engineering", "P3"),
    "TP-0063": ("retail-ecommerce", "P3"),
    "TP-0064": ("identity-synthetic", "P3"),
    "TP-0065": ("fraud-infrastructure", "P1"),
    "TP-0066": ("insurance-healthcare", "P4"),
    "TP-0067": ("account-takeover", "P2"),
    "TP-0068": ("retail-ecommerce", "P4"),
    "TP-0069": ("fraud-infrastructure", "P2"),
    "TP-0070": ("retail-ecommerce", "P3"),
    "TP-0071": ("telecom-specialized", "P4"),
    "TP-0072": ("telecom-specialized", "P3"),
    "TP-0073": ("identity-synthetic", "P3"),
    "TP-0074": ("insurance-healthcare", "P3"),
    "TP-0075": ("retail-ecommerce", "P4"),
    "TP-0076": ("retail-ecommerce", "P3"),
    "TP-0077": ("insurance-healthcare", "P3"),
    "TP-0078": ("crypto-laundering", "P5"),
    "TP-0079": ("fraud-infrastructure", "P1"),
    "TP-0080": ("crypto-laundering", "P5"),
    "TP-0081": ("account-takeover", "P2"),
    "TP-0082": ("social-engineering", "P4"),
    "TP-0083": ("investment-romance", "P3"),
    "TP-0084": ("social-engineering", "P4"),
    "TP-0085": ("crypto-laundering", "P5"),
    "TP-0086": ("state-geopolitical", "P1"),
    "TP-0087": ("account-takeover", "P2"),
    "TP-0088": ("social-engineering", "P2"),
    "TP-0089": ("fraud-infrastructure", "P1"),
}

THREAT_PATHS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ThreatPaths")


def tag_file(filepath, fraud_family, primary_phase):
    """Insert fraud_family and primary_phase after cfpf_phases block."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already tagged
    if "fraud_family:" in content:
        print(f"  SKIP (already tagged): {os.path.basename(filepath)}")
        return False

    # Find the end of cfpf_phases block.
    # Handles both multi-line and inline array formats.
    lines = content.split("\n")
    insert_idx = None
    in_cfpf = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("cfpf_phases:"):
            # Check if inline array format: cfpf_phases: [P1, P2, ...]
            if "[" in line:
                insert_idx = i
                break
            else:
                in_cfpf = True
                continue
        if in_cfpf:
            if stripped.startswith("- P"):
                insert_idx = i  # keep updating to find the last P* line
            else:
                # We've exited cfpf_phases block
                break

    if insert_idx is None:
        print(f"  ERROR (no cfpf_phases found): {os.path.basename(filepath)}")
        return False

    # Insert the two new fields after cfpf_phases block
    new_lines = [
        f'fraud_family: "{fraud_family}"',
        f'primary_phase: "{primary_phase}"',
    ]
    lines = lines[: insert_idx + 1] + new_lines + lines[insert_idx + 1 :]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  OK: {os.path.basename(filepath)} -> {fraud_family} / {primary_phase}")
    return True


def main():
    import glob

    files = glob.glob(os.path.join(THREAT_PATHS_DIR, "TP-*.md"))
    print(f"Found {len(files)} threat path files")

    tagged = 0
    skipped = 0
    errors = 0

    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        # Extract TP ID from filename (e.g., TP-0001 from TP-0001-treasury-mgmt-ato-malvertising.md)
        tp_id = basename[:7]  # "TP-XXXX"

        if tp_id not in CLASSIFICATIONS:
            print(f"  WARN (no classification): {basename}")
            errors += 1
            continue

        fraud_family, primary_phase = CLASSIFICATIONS[tp_id]
        result = tag_file(filepath, fraud_family, primary_phase)
        if result:
            tagged += 1
        elif result is False:
            skipped += 1

    print(f"\nDone: {tagged} tagged, {skipped} skipped, {errors} errors")

    # Print distribution summary
    from collections import Counter

    family_counts = Counter(f for f, _ in CLASSIFICATIONS.values())
    phase_counts = Counter(p for _, p in CLASSIFICATIONS.values())

    print("\nFraud family distribution:")
    for family, count in sorted(family_counts.items(), key=lambda x: -x[1]):
        print(f"  {family}: {count}")

    print("\nPrimary phase distribution:")
    for phase, count in sorted(phase_counts.items()):
        print(f"  {phase}: {count}")


if __name__ == "__main__":
    main()
