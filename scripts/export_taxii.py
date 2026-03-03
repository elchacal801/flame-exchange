#!/usr/bin/env python3
"""
export_taxii.py — FLAME Static TAXII 2.1 Endpoint Generator

Generates TAXII 2.1-compatible JSON files at build time in api/taxii/.
"""

import json
import uuid
import sys
from pathlib import Path
from datetime import datetime, timezone

NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
TAXII_BASE = "https://elchacal801.github.io/flame-fraud/api/taxii"
STIX_BUNDLE_PATH = Path("database/flame_stix_bundle.json")
OUTPUT_DIR = Path("api/taxii")

COLLECTION_DEFS = [
    {"seed": "flame-taxii-col-threat-paths", "title": "FLAME Threat Paths",
     "description": "Fraud scheme SDOs derived from FLAME threat paths"},
    {"seed": "flame-taxii-col-detection-rules", "title": "FLAME Detection Rules",
     "description": "Course-of-action SDOs for fraud detection"},
    {"seed": "flame-taxii-col-baselines", "title": "FLAME Baselines",
     "description": "Baseline control SDOs"},
]


def deterministic_uuid(seed: str) -> str:
    return str(uuid.uuid5(NAMESPACE, seed))


def build_discovery() -> dict:
    return {
        "title": "FLAME TAXII Server",
        "description": "Static TAXII 2.1 endpoint for FLAME fraud intelligence",
        "contact": "https://github.com/elchacal801/flame-fraud",
        "default": f"{TAXII_BASE}/default/",
        "api_roots": [f"{TAXII_BASE}/default/"],
    }


def build_collections() -> dict:
    collections = []
    for cdef in COLLECTION_DEFS:
        collections.append({
            "id": deterministic_uuid(cdef["seed"]),
            "title": cdef["title"],
            "description": cdef["description"],
            "can_read": True,
            "can_write": False,
            "media_types": ["application/stix+json;version=2.1"],
        })
    return {"collections": collections}


def build_manifest(objects: list) -> dict:
    entries = []
    for obj in objects:
        entries.append({
            "id": obj.get("id", ""),
            "date_added": obj.get("modified", datetime.now(timezone.utc).isoformat()),
            "version": obj.get("modified", datetime.now(timezone.utc).isoformat()),
            "media_type": "application/stix+json;version=2.1",
        })
    return {"objects": entries}


def build_collection_objects(objects: list) -> dict:
    """Wrap objects in a STIX bundle format for TAXII response."""
    return {
        "type": "bundle",
        "id": f"bundle--{deterministic_uuid('flame-taxii-bundle')}",
        "objects": objects,
    }


def main():
    print("[*] FLAME Static TAXII Generator")

    if not STIX_BUNDLE_PATH.exists():
        print(f"[!] STIX bundle not found: {STIX_BUNDLE_PATH}")
        sys.exit(1)

    with open(STIX_BUNDLE_PATH, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    all_objects = bundle.get("objects", [])
    print(f"[*] Loaded {len(all_objects)} STIX objects")

    # Split objects into collections by type
    threat_path_types = {"attack-pattern", "x-flame-fraud-scheme",
                         "x-flame-financial-transaction", "x-flame-mule-network",
                         "x-flame-fraud-actor-profile", "relationship"}
    detection_types = {"course-of-action"}
    baseline_types = {"x-flame-baseline"}

    tp_objects = [o for o in all_objects if o.get("type") in threat_path_types or o.get("type") == "identity"]
    dl_objects = [o for o in all_objects if o.get("type") in detection_types]
    bl_objects = [o for o in all_objects if o.get("type") in baseline_types]

    collections = build_collections()
    col_data = [
        (collections["collections"][0]["id"], "flame-threat-paths", tp_objects),
        (collections["collections"][1]["id"], "flame-detection-rules", dl_objects),
        (collections["collections"][2]["id"], "flame-baselines", bl_objects),
    ]

    # Write discovery
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    disc_path = OUTPUT_DIR / "discovery.json"
    disc_path.write_text(json.dumps(build_discovery(), indent=2), encoding="utf-8")
    print(f"[+] Discovery: {disc_path}")

    # Write collections
    default_dir = OUTPUT_DIR / "default"
    default_dir.mkdir(parents=True, exist_ok=True)
    col_path = default_dir / "collections.json"
    col_path.write_text(json.dumps({"collections": collections["collections"]}, indent=2), encoding="utf-8")
    print(f"[+] Collections: {col_path}")

    # Write per-collection data
    for col_id, col_slug, objects in col_data:
        col_dir = default_dir / "collections" / col_slug
        col_dir.mkdir(parents=True, exist_ok=True)

        manifest = build_manifest(objects)
        (col_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        bundle_data = build_collection_objects(objects)
        (col_dir / "objects.json").write_text(json.dumps(bundle_data, indent=2), encoding="utf-8")

        print(f"[+] Collection '{col_slug}': {len(objects)} objects")

    print("[*] Done.")


if __name__ == "__main__":
    main()
