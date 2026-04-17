#!/usr/bin/env python3
"""
export_misp.py — FLAME MISP Galaxy & Feed Exporter

Generates:
  1. data/misp/flame-galaxy.json     — MISP galaxy definition
  2. data/misp/flame-cluster.json    — MISP cluster entries (all TPs)
  3. database/misp-feed/manifest.json — MISP feed manifest
  4. database/misp-feed/{uuid}.json  — Per-TP MISP event files
"""

import json
import uuid
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
INDEX_FILE = Path("database/flame-index.json")
CONTENT_DIR = Path("database/flame-content")


def deterministic_uuid(seed: str) -> str:
    return str(uuid.uuid5(NAMESPACE, seed))


def build_galaxy() -> dict:
    """Generate MISP galaxy JSON."""
    return {
        "description": "FLAME Fraud Threat Paths - fraud schemes mapped across CFPF lifecycle",
        "icon": "fire",
        "name": "FLAME Fraud Threat Paths",
        "namespace": "flame",
        "type": "flame-fraud",
        "uuid": deterministic_uuid("flame-misp-galaxy"),
        "version": 1,
    }


def build_cluster_entry(tp: dict) -> dict:
    """Generate a single MISP cluster entry for a TP."""
    tp_id = tp["id"]
    entry_uuid = deterministic_uuid(f"flame-{tp_id}")

    meta = {
        "fraud_types": tp.get("fraud_types", []),
        "sectors": tp.get("sector", []),
        "cfpf_phases": tp.get("cfpf_phases", []),
        "confidence_score": tp.get("confidence_score", 0),
        "refs": [f"https://flameintel.org/?tp={tp_id}"],
    }

    # Build MITRE ATT&CK relations
    related = []
    for tech_id in tp.get("mitre_attack", []):
        related.append({
            "dest-uuid": deterministic_uuid(f"mitre-{tech_id}"),
            "tags": ["estimative-language:likelihood-probability=\"likely\""],
            "type": "uses",
        })

    return {
        "value": tp.get("title", tp_id),
        "description": tp.get("summary", ""),
        "uuid": entry_uuid,
        "meta": meta,
        "related": related,
    }


def build_cluster(index: list) -> dict:
    """Generate full MISP cluster JSON."""
    values = [build_cluster_entry(tp) for tp in index]
    return {
        "authors": ["FLAME Project"],
        "category": "fraud",
        "description": "FLAME Fraud Threat Paths cluster",
        "name": "FLAME Fraud Threat Paths",
        "source": "FLAME Project - https://github.com/elchacal801/flame-fraud",
        "type": "flame-fraud",
        "uuid": deterministic_uuid("flame-misp-cluster"),
        "version": 1,
        "values": values,
    }


def build_feed_event(tp: dict) -> dict:
    """Generate a MISP feed event for a single TP."""
    tp_id = tp["id"]
    event_uuid = deterministic_uuid(f"flame-event-{tp_id}")
    timestamp = tp.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))

    attributes = []
    for ft in tp.get("fraud_types", []):
        attr_uuid = deterministic_uuid(f"flame-attr-{tp_id}-ft-{ft}")
        attributes.append({
            "uuid": attr_uuid,
            "type": "text",
            "category": "Other",
            "value": ft,
            "comment": f"Fraud type for {tp_id}",
        })
    for phase in tp.get("cfpf_phases", []):
        attr_uuid = deterministic_uuid(f"flame-attr-{tp_id}-phase-{phase}")
        attributes.append({
            "uuid": attr_uuid,
            "type": "text",
            "category": "Other",
            "value": f"CFPF-{phase}",
            "comment": f"CFPF phase for {tp_id}",
        })

    return {
        "Event": {
            "uuid": event_uuid,
            "info": f"FLAME: {tp.get('title', tp_id)}",
            "date": timestamp,
            "analysis": "2",  # completed
            "threat_level_id": "2",  # medium
            "published": True,
            "Orgc": {"name": "FLAME Project", "uuid": deterministic_uuid("flame-org")},
            "Tag": [{"name": "flame:type=\"threat-path\""}],
            "Attribute": attributes,
        }
    }


def build_feed(index: list) -> dict:
    """Generate MISP feed manifest."""
    manifest = {}
    for tp in index:
        event = build_feed_event(tp)
        event_uuid = event["Event"]["uuid"]
        manifest[event_uuid] = {
            "Orgc": event["Event"]["Orgc"],
            "Tag": event["Event"]["Tag"],
            "info": event["Event"]["info"],
            "date": event["Event"]["date"],
            "analysis": event["Event"]["analysis"],
            "threat_level_id": event["Event"]["threat_level_id"],
            "timestamp": str(int(datetime.now(timezone.utc).timestamp())),
        }
    return manifest


def main():
    print("[*] FLAME MISP Exporter")

    if not INDEX_FILE.exists():
        print(f"[!] Index not found: {INDEX_FILE}")
        sys.exit(1)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    print(f"[*] Found {len(index)} threat paths.")

    # Galaxy
    galaxy = build_galaxy()
    galaxy_path = Path("data/misp/flame-galaxy.json")
    galaxy_path.parent.mkdir(parents=True, exist_ok=True)
    galaxy_path.write_text(json.dumps(galaxy, indent=2), encoding="utf-8")
    print(f"[+] Galaxy: {galaxy_path}")

    # Cluster
    cluster = build_cluster(index)
    cluster_path = Path("data/misp/flame-cluster.json")
    cluster_path.write_text(json.dumps(cluster, indent=2), encoding="utf-8")
    print(f"[+] Cluster: {cluster_path} ({len(cluster['values'])} entries)")

    # Feed
    feed_dir = Path("database/misp-feed")
    feed_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_feed(index)
    manifest_path = feed_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[+] Feed manifest: {manifest_path}")

    for tp in index:
        event = build_feed_event(tp)
        event_uuid = event["Event"]["uuid"]
        event_path = feed_dir / f"{event_uuid}.json"
        event_path.write_text(json.dumps(event, indent=2), encoding="utf-8")

    print(f"[+] Feed events: {len(index)} files in {feed_dir}")
    print("[*] Done.")


if __name__ == "__main__":
    main()
