#!/usr/bin/env python3
"""
FLAME Detection Logic — TP Inline Rules Sync Script

Regenerates all TP-XXXX-rules.json files from the canonical DL-XXXX YAML
sources. This ensures inline rules shown on the detail page stay in sync
with the Detection Logic source of truth.

Each DL rule's queries are emitted as individual entries in the TP rules
file, with a `source_rule` field for traceability.

Usage:
    python scripts/sync_tp_rules.py          # regenerate all
    python scripts/sync_tp_rules.py TP-0067  # regenerate one
"""

import yaml
import os
import re
import sys
import json
import glob
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL_DIR = os.path.join(REPO_ROOT, "DetectionLogic")
TP_CONTENT_DIR = os.path.join(REPO_ROOT, "database", "flame-content")

# Priority order for which query types to include
QUERY_PRIORITY = ["kql", "sigma", "splunk", "cql", "sql", "python"]


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def build_tp_to_dl_map():
    """Build mapping of TP-ID -> list of (dl_id, rule_data) from YAML sources."""
    tp_map = defaultdict(list)
    yaml_files = sorted(glob.glob(os.path.join(DL_DIR, "DL-*.yml")))

    for path in yaml_files:
        fname = os.path.basename(path)
        dl_id_match = re.match(r"^(DL-\d{4})", fname)
        if not dl_id_match:
            continue
        dl_id = dl_id_match.group(1)

        try:
            rule = load_yaml(path)
            if not isinstance(rule, dict):
                continue
        except Exception:
            continue

        for tp_id in (rule.get("threat_paths") or []):
            if tp_id:
                tp_map[str(tp_id)].append((dl_id, rule))

    return tp_map


def generate_tp_rules(tp_id, dl_rules):
    """Generate the rules list for a TP from its mapped DL rules."""
    rules = []

    for dl_id, rule in sorted(dl_rules, key=lambda x: x[0]):
        title = rule.get("title", dl_id)
        queries = rule.get("queries", {})

        if not queries:
            # Sigma-compatible rules without explicit queries block:
            # emit the detection block as a Sigma rule
            detection = rule.get("detection", {})
            logsource = rule.get("logsource", {})
            level = rule.get("level", "medium")
            if detection:
                sigma_content = build_sigma_from_detection(rule, dl_id)
                if sigma_content:
                    rules.append({
                        "type": "sigma",
                        "content": sigma_content,
                        "title": f"{dl_id}: {title} (Sigma)",
                        "source_rule": dl_id,
                    })
            continue

        # Emit each query type in priority order
        for lang in QUERY_PRIORITY:
            if lang not in queries:
                continue
            content = queries[lang]
            if not isinstance(content, str) or not content.strip():
                continue

            # Determine display type
            type_map = {
                "kql": "kql",
                "sigma": "sigma",
                "splunk": "spl",
                "cql": "cql",
                "sql": "sql",
                "python": "python",
            }
            display_type = type_map.get(lang, lang)

            # Use first available query as the primary, others as alternatives
            rules.append({
                "type": display_type,
                "content": content,
                "title": f"{dl_id}: {title} ({lang.upper()})",
                "source_rule": dl_id,
            })
            # Only emit the first (highest priority) query per DL rule
            # to keep the inline rules concise
            break

    return rules


def build_sigma_from_detection(rule, dl_id):
    """Build a minimal Sigma YAML string from a rule's detection block."""
    detection = rule.get("detection", {})
    logsource = rule.get("logsource", {})
    title = rule.get("title", dl_id)
    level = rule.get("level", "medium")
    description = rule.get("description", "")
    if isinstance(description, str):
        description = description.strip()[:200]

    if not detection.get("condition"):
        return None

    lines = []
    lines.append(f"title: {title}")
    lines.append("status: experimental")
    if description:
        lines.append(f"description: {description}")
    lines.append("logsource:")
    for k, v in logsource.items():
        lines.append(f"    {k}: {v}")
    lines.append("detection:")

    for key, val in detection.items():
        if key == "condition":
            continue
        if isinstance(val, dict):
            lines.append(f"    {key}:")
            for fk, fv in val.items():
                if isinstance(fv, list):
                    lines.append(f"        {fk}:")
                    for item in fv:
                        lines.append(f"            - {json.dumps(item)}")
                else:
                    lines.append(f"        {fk}: {json.dumps(fv)}")
        elif isinstance(val, str):
            lines.append(f"    {key}: {val}")

    condition = str(detection.get("condition", ""))
    lines.append(f"    condition: {condition}")
    lines.append(f"level: {level}")

    return "\n".join(lines)


def main():
    target_tp = sys.argv[1] if len(sys.argv) > 1 else None

    tp_map = build_tp_to_dl_map()
    print(f"[INFO] Mapped {sum(len(v) for v in tp_map.values())} DL->TP relationships "
          f"across {len(tp_map)} threat paths")

    # Also discover existing TP-XXXX-rules.json files
    existing = set()
    for f in glob.glob(os.path.join(TP_CONTENT_DIR, "TP-*-rules.json")):
        tp_id = os.path.basename(f).replace("-rules.json", "")
        existing.add(tp_id)

    updated = 0
    skipped = 0
    created = 0

    tp_ids = [target_tp] if target_tp else sorted(set(list(tp_map.keys()) + list(existing)))

    for tp_id in tp_ids:
        if not tp_id.startswith("TP-"):
            continue

        output_path = os.path.join(TP_CONTENT_DIR, f"{tp_id}-rules.json")
        dl_rules = tp_map.get(tp_id, [])

        if not dl_rules:
            # No DL rules map to this TP — write empty rules
            data = {"tp_id": tp_id, "rules": []}
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            skipped += 1
            continue

        rules = generate_tp_rules(tp_id, dl_rules)
        data = {"tp_id": tp_id, "rules": rules}

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        if tp_id in existing:
            updated += 1
        else:
            created += 1

        if len(dl_rules) > 0:
            dl_ids = ", ".join(dl_id for dl_id, _ in sorted(dl_rules, key=lambda x: x[0]))
            print(f"  {tp_id}: {len(rules)} inline rules from {len(dl_rules)} DL rules ({dl_ids})")

    print(f"\n[INFO] Sync complete: {updated} updated, {created} created, {skipped} empty")


if __name__ == "__main__":
    main()
