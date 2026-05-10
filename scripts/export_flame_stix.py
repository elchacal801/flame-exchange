#!/usr/bin/env python3
"""
export_flame_stix.py — FLAME STIX 2.1 Exporter

Reads threat path content from database/flame-content/TP-XXXX.json and
produces:
  1. database/flame_stix_bundle.json   — STIX 2.1 bundle with attack-patterns

All STIX IDs are deterministic (uuid5) so repeated builds produce identical
output.  The bundle validates against the stix2 Python library before writing.
"""

import json
import re
import uuid
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import stix2
except ImportError:
    print("[!] stix2 library required: pip install stix2>=3.0.0")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # NAMESPACE_DNS

FLAME_IDENTITY_UUID = uuid.uuid5(NAMESPACE, "flame-fraud-project")
FLAME_IDENTITY_ID = f"identity--{FLAME_IDENTITY_UUID}"

TLP_CLEAR = stix2.TLP_WHITE  # stix2 uses TLP_WHITE for TLP:CLEAR
TLP_CLEAR_ID = TLP_CLEAR.id

CFPF_KILL_CHAIN = [
    {"kill_chain_name": "cfpf", "phase_name": "P1-reconnaissance"},
    {"kill_chain_name": "cfpf", "phase_name": "P2-initial-access"},
    {"kill_chain_name": "cfpf", "phase_name": "P3-positioning"},
    {"kill_chain_name": "cfpf", "phase_name": "P4-execution"},
    {"kill_chain_name": "cfpf", "phase_name": "P5-monetization"},
]

PHASE_MAP = {
    "P1": "P1-reconnaissance",
    "P2": "P2-initial-access",
    "P3": "P3-positioning",
    "P4": "P4-execution",
    "P5": "P5-monetization",
}

FLAME_PAGES_BASE = "https://flameintel.org"

# Paths
CONTENT_DIR = Path("database/flame-content")
INDEX_FILE = Path("database/flame-index.json")
OUTPUT_BUNDLE = Path("database/flame_stix_bundle.json")
# Regex to find TP cross-references in body text
TP_REF_RE = re.compile(r"\bTP-(\d{4})\b")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def deterministic_id(stix_type: str, seed: str) -> str:
    """Generate a deterministic STIX ID from a seed string."""
    return f"{stix_type}--{uuid.uuid5(NAMESPACE, seed)}"


def load_index() -> List[Dict[str, Any]]:
    """Load flame-index.json."""
    if not INDEX_FILE.exists():
        print(f"[!] Index not found: {INDEX_FILE}")
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tp_content(tp_id: str) -> Optional[Dict[str, Any]]:
    """Load individual TP-XXXX.json content file."""
    path = CONTENT_DIR / f"{tp_id}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def map_cfpf_phases(phases: List[str]) -> List[Dict[str, str]]:
    """Map short phase codes (P1, P2...) to STIX kill_chain_phases."""
    result = []
    for p in phases:
        phase_name = PHASE_MAP.get(p)
        if phase_name:
            result.append({
                "kill_chain_name": "cfpf",
                "phase_name": phase_name,
            })
    return result


def build_external_refs(tp: Dict[str, Any]) -> List[Dict[str, str]]:
    """Build external_references for a threat path."""
    refs = [
        {
            "source_name": "FLAME Project",
            "description": f"Threat Path {tp['id']}",
            "url": f"{FLAME_PAGES_BASE}/?tp={tp['id']}",
        }
    ]
    # Add MITRE ATT&CK references
    for tech_id in tp.get("mitre_attack", []):
        refs.append({
            "source_name": "mitre-attack",
            "external_id": tech_id,
            "url": f"https://attack.mitre.org/techniques/{tech_id.replace('.', '/')}/",
        })
    # Add MITRE F3 references
    for tech_id in tp.get("mitre_f3", []):
        ref = {
            "source_name": "mitre-f3",
            "external_id": tech_id,
        }
        if tech_id.startswith("F"):
            ref["url"] = f"https://ctid.mitre.org/fraud#/techniques/{tech_id}/"
        else:
            ref["url"] = f"https://attack.mitre.org/techniques/{tech_id.replace('.', '/')}/"
        refs.append(ref)
    # Add source reference if available
    source = tp.get("source", "")
    if source and source.startswith("http"):
        refs.append({
            "source_name": "Reference",
            "url": source,
        })
    return refs


# Mapping from fraud_types keywords to scheme_type enum
SCHEME_TYPE_MAP = {
    "account-takeover": "ato",
    "BEC": "bec",
    "business-email-compromise": "bec",
    "synthetic-identity": "synthetic-identity",
    "authorized-push-payment": "app-fraud",
    "check-fraud": "check-fraud",
    "wire-fraud": "wire-fraud",
    "insurance-fraud": "insurance-fraud",
    "investment-fraud": "investment-fraud",
    "investment-scam": "investment-fraud",
    "romance-scam": "romance-scam",
    "first-party": "first-party",
    "first-party-fraud": "first-party",
    "insider": "insider",
    "insider-threat": "insider",
    "mule-recruitment": "mule-recruitment",
    "money-mule": "mule-recruitment",
    "credential-stuffing": "credential-stuffing",
    "deepfake": "deepfake",
    "deepfake-fraud": "deepfake",
    "identity-theft": "identity-theft",
    "rdga-infrastructure": "infrastructure-generation",
    "tds-exploitation": "infrastructure-generation",
    "ai-accelerated-fraud-infrastructure": "infrastructure-generation",
    "sanctions-evasion-infrastructure": "sanctions-evasion",
    "state-criminal-convergence": "state-criminal-convergence",
    "human-trafficking-facilitation": "human-trafficking",
    "bph-migration": "infrastructure-migration",
    "crypto-laundering-infrastructure": "crypto-laundering",
}


def _infer_scheme_type(fraud_types: list) -> str:
    """Infer the primary scheme_type from a TP's fraud_types list."""
    for ft in fraud_types:
        if ft in SCHEME_TYPE_MAP:
            return SCHEME_TYPE_MAP[ft]
    return "other"


def build_fraud_scheme(tp: dict) -> dict:
    """Build an x-flame-fraud-scheme custom STIX object from TP data."""
    tp_id = tp["id"]
    phases = tp.get("cfpf_phases", [])
    fraud_types = tp.get("fraud_types", [])

    obj = {
        "type": "x-flame-fraud-scheme",
        "spec_version": "2.1",
        "id": deterministic_id("x-flame-fraud-scheme", f"flame-{tp_id}-scheme"),
        "created_by_ref": FLAME_IDENTITY_ID,
        "name": tp.get("title", tp_id),
        "description": tp.get("summary", ""),
        "scheme_type": _infer_scheme_type(fraud_types),
        "cfpf_phases": phases,
        "affected_sectors": tp.get("sector", []),
        "kill_chain_phases": map_cfpf_phases(phases),
        "confidence_score": tp.get("confidence_score", 0) or 0,
        "labels": fraud_types,
        "external_references": build_external_refs(tp),
        "object_marking_refs": [TLP_CLEAR_ID],
    }

    # Custom properties for new frontmatter fields
    infra_gen = tp.get("infrastructure_generation_method")
    if infra_gen:
        obj["x_flame_infrastructure_generation_method"] = infra_gen

    geo_timing = tp.get("geopolitical_timing")
    if geo_timing:
        obj["x_flame_geopolitical_timing"] = geo_timing

    ns_nexus = tp.get("nation_state_nexus")
    if ns_nexus:
        obj["x_flame_nation_state_nexus"] = ns_nexus

    return obj


# Transaction type inference from body text keywords
TRANSACTION_KEYWORDS = {
    "wire": "wire", "SWIFT": "wire", "FedWire": "wire",
    "ACH": "ACH", "direct deposit": "ACH",
    "crypto": "crypto", "bitcoin": "crypto", "blockchain": "crypto",
    "check": "check", "cheque": "check",
    "A2A": "A2A", "instant payment": "A2A", "RTP": "A2A", "Zelle": "A2A",
    "card": "card", "credit card": "card", "debit card": "card",
}

RAIL_KEYWORDS = {
    "SWIFT": "SWIFT", "FedWire": "FedWire", "ACH": "ACH",
    "blockchain": "blockchain", "card network": "card-network",
    "RTP": "RTP", "Zelle": "RTP",
}


def _infer_transaction_type(body: str) -> str:
    body_lower = body.lower()
    for keyword, ttype in TRANSACTION_KEYWORDS.items():
        if keyword.lower() in body_lower:
            return ttype
    return "other"


def _infer_rail(body: str) -> str:
    for keyword, rail in RAIL_KEYWORDS.items():
        if keyword in body:
            return rail
    return "other"


def build_financial_transaction(tp: dict, content: dict | None = None) -> dict | None:
    """Build x-flame-financial-transaction from P4/P5 content. Returns None if no P4/P5."""
    phases = tp.get("cfpf_phases", [])
    if "P4" not in phases and "P5" not in phases:
        return None

    body = content.get("body", "") if content else ""
    tp_id = tp["id"]

    return {
        "type": "x-flame-financial-transaction",
        "spec_version": "2.1",
        "id": deterministic_id("x-flame-financial-transaction", f"flame-{tp_id}-fin-txn"),
        "created_by_ref": FLAME_IDENTITY_ID,
        "name": f"{tp.get('title', tp_id)} - Financial Transaction Pattern",
        "transaction_type": _infer_transaction_type(body),
        "rail": _infer_rail(body),
        "velocity_pattern": "",
        "object_marking_refs": [TLP_CLEAR_ID],
    }


MULE_KEYWORDS = ["mule", "money mule", "mule account", "mule network", "mule-recruitment",
                 "mule pipeline", "mule ring"]

RECRUITMENT_KEYWORDS = {
    "romance": "romance", "love": "romance",
    "employment": "employment", "job": "employment", "work-from-home": "employment",
    "social media": "social-media", "telegram": "social-media",
    "crypto": "crypto-job",
}


def _has_mule_reference(tp: dict, body: str) -> bool:
    fraud_types = tp.get("fraud_types", [])
    if "mule-recruitment" in fraud_types:
        return True
    body_lower = body.lower()
    return any(kw in body_lower for kw in MULE_KEYWORDS)


def _infer_recruitment_method(body: str) -> str:
    body_lower = body.lower()
    for keyword, method in RECRUITMENT_KEYWORDS.items():
        if keyword in body_lower:
            return method
    return "other"


def build_mule_network(tp: dict, content: dict | None = None) -> dict | None:
    """Build x-flame-mule-network. Only for TPs with mule references."""
    body = content.get("body", "") if content else ""
    if not _has_mule_reference(tp, body):
        return None

    tp_id = tp["id"]
    return {
        "type": "x-flame-mule-network",
        "spec_version": "2.1",
        "id": deterministic_id("x-flame-mule-network", f"flame-{tp_id}-mule-net"),
        "created_by_ref": FLAME_IDENTITY_ID,
        "name": f"{tp.get('title', tp_id)} - Mule Network",
        "recruitment_method": _infer_recruitment_method(body),
        "network_type": "hybrid",
        "geographic_spread": [],
        "estimated_throughput": "",
        "object_marking_refs": [TLP_CLEAR_ID],
    }


def _has_underground_section(body: str) -> bool:
    return bool(re.search(r"^## Underground Ecosystem Context", body, re.MULTILINE))


SOPHISTICATION_KEYWORDS = {
    "expert": ["nation-state", "APT", "advanced persistent"],
    "high": ["organized crime", "sophisticated", "complex infrastructure"],
    "medium": ["toolkit", "MaaS", "service", "marketplace"],
    "low": ["script", "tutorial", "copy-paste"],
}


def _infer_sophistication(body: str) -> str:
    body_lower = body.lower()
    for level, keywords in SOPHISTICATION_KEYWORDS.items():
        if any(kw.lower() in body_lower for kw in keywords):
            return level
    return "medium"


def build_fraud_actor_profile(tp: dict, content: dict | None = None) -> dict | None:
    """Build x-flame-fraud-actor-profile from Underground Ecosystem Context."""
    body = content.get("body", "") if content else ""
    if not _has_underground_section(body):
        return None

    tp_id = tp["id"]
    fraud_types = tp.get("fraud_types", [])

    return {
        "type": "x-flame-fraud-actor-profile",
        "spec_version": "2.1",
        "id": deterministic_id("x-flame-fraud-actor-profile", f"flame-{tp_id}-actor"),
        "created_by_ref": FLAME_IDENTITY_ID,
        "name": f"{tp.get('title', tp_id)} - Actor Profile",
        "fraud_specialization": fraud_types,
        "monetization_methods": [],
        "sophistication_level": _infer_sophistication(body),
        "jurisdiction": [],
        "object_marking_refs": [TLP_CLEAR_ID],
    }


# ---------------------------------------------------------------------------
# STIX Object Construction
# ---------------------------------------------------------------------------

def build_identity() -> stix2.Identity:
    """Build the FLAME project identity object."""
    return stix2.Identity(
        id=FLAME_IDENTITY_ID,
        name="FLAME Project",
        identity_class="organization",
        description="Fraud Lifecycle Attack Map & Encyclopedia — open-source "
                    "framework for structured fraud threat intelligence.",
        external_references=[{
            "source_name": "FLAME GitHub",
            "url": "https://github.com/elchacal801/flame-fraud",
        }],
        object_marking_refs=[TLP_CLEAR.id],
        allow_custom=True,
    )


def build_attack_pattern(tp: Dict[str, Any]) -> stix2.AttackPattern:
    """Build a STIX attack-pattern from a FLAME threat path."""
    tp_id = tp["id"]
    phases = map_cfpf_phases(tp.get("cfpf_phases", []))
    ext_refs = build_external_refs(tp)

    return stix2.AttackPattern(
        id=deterministic_id("attack-pattern", f"flame-{tp_id}"),
        created_by_ref=FLAME_IDENTITY_ID,
        name=tp.get("title", tp_id),
        description=tp.get("summary", ""),
        kill_chain_phases=phases if phases else None,
        external_references=ext_refs,
        labels=tp.get("fraud_types", []),
        object_marking_refs=[TLP_CLEAR.id],
        allow_custom=True,
    )


def build_mitre_attack_pattern(tech_id: str) -> stix2.AttackPattern:
    """Build a stub STIX attack-pattern for a MITRE ATT&CK technique."""
    return stix2.AttackPattern(
        id=deterministic_id("attack-pattern", f"mitre-{tech_id}"),
        created_by_ref=FLAME_IDENTITY_ID,
        name=f"MITRE ATT&CK {tech_id}",
        external_references=[{
            "source_name": "mitre-attack",
            "external_id": tech_id,
            "url": f"https://attack.mitre.org/techniques/{tech_id.replace('.', '/')}/",
        }],
        allow_custom=True,
    )


def build_f3_attack_pattern(tech_id: str) -> stix2.AttackPattern:
    """Build a stub STIX attack-pattern for a MITRE F3 technique."""
    url = (f"https://ctid.mitre.org/fraud#/techniques/{tech_id}/"
           if tech_id.startswith("F")
           else f"https://attack.mitre.org/techniques/{tech_id.replace('.', '/')}/")
    return stix2.AttackPattern(
        id=deterministic_id("attack-pattern", f"f3-{tech_id}"),
        created_by_ref=FLAME_IDENTITY_ID,
        name=f"MITRE F3 {tech_id}",
        external_references=[{
            "source_name": "mitre-f3",
            "external_id": tech_id,
            "url": url,
        }],
        allow_custom=True,
    )


def find_tp_cross_refs(body: str, own_id: str, known_ids: set) -> List[str]:
    """Find cross-references to other TPs in the body text."""
    refs = set()
    for match in TP_REF_RE.finditer(body):
        ref_id = f"TP-{match.group(1)}"
        if ref_id != own_id and ref_id in known_ids:
            refs.add(ref_id)
    return sorted(refs)


def build_relationship(source_id: str, target_id: str,
                       rel_type: str = "related-to") -> stix2.Relationship:
    """Build a STIX relationship between two objects."""
    seed = f"rel-{source_id}-{rel_type}-{target_id}"
    return stix2.Relationship(
        id=deterministic_id("relationship", seed),
        relationship_type=rel_type,
        source_ref=source_id,
        target_ref=target_id,
        created_by_ref=FLAME_IDENTITY_ID,
        object_marking_refs=[TLP_CLEAR.id],
        allow_custom=True,
    )


def parse_baseline_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a baseline markdown file."""
    # Frontmatter is inside a ```yaml block
    match = re.search(r"```yaml\s*\n---\s*\n(.*?)---\s*\n```", text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_baseline_description(text: str) -> str:
    """Extract the Description section from a baseline markdown file."""
    match = re.search(r"## Description\s*\n\n(.+?)(?:\n## |\Z)", text, re.DOTALL)
    if match:
        return match.group(1).strip()[:500]
    return ""


def build_baseline_sdo(bl_id: str, title: str, description: str,
                        tags: list) -> dict:
    """Build an x-flame-baseline custom STIX SDO."""
    return {
        "type": "x-flame-baseline",
        "spec_version": "2.1",
        "id": deterministic_id("x-flame-baseline", f"flame-{bl_id}"),
        "created_by_ref": FLAME_IDENTITY_ID,
        "name": title,
        "description": description,
        "labels": tags if tags else ["baseline"],
        "object_marking_refs": [TLP_CLEAR_ID],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("[*] FLAME STIX 2.1 Exporter")
    print(f"    Content dir: {CONTENT_DIR}")
    print(f"    Index: {INDEX_FILE}")

    # Load index
    index = load_index()
    if not index:
        print("[!] No threat paths found. Exiting.")
        sys.exit(1)

    print(f"[*] Found {len(index)} threat paths in index.")

    known_tp_ids = {tp["id"] for tp in index}

    # Build STIX objects
    identity = build_identity()
    attack_patterns = {}  # tp_id -> AttackPattern
    mitre_patterns = {}   # tech_id -> AttackPattern
    f3_patterns = {}      # tech_id -> AttackPattern (MITRE F3)
    relationships = []
    stix_relationships = []
    fraud_schemes = {}    # tp_id -> dict
    fin_transactions = {} # tp_id -> dict
    mule_networks = {}    # tp_id -> dict
    actor_profiles = {}   # tp_id -> dict

    for tp in index:
        tp_id = tp["id"]

        # Build attack-pattern
        ap = build_attack_pattern(tp)
        attack_patterns[tp_id] = ap
        print(f"    [+] {tp_id}: {tp.get('title', '?')}")

        # Load full content for cross-refs and extended SDOs
        content = load_tp_content(tp_id)
        body = content.get("body", "") if content else ""

        # Find cross-references for relationships
        # Prefer structured related_tps from frontmatter; fall back to regex body scan
        related_tps_meta = tp.get("related_tps", [])
        if related_tps_meta:
            for rel in related_tps_meta:
                ref_id = rel.get("id", "") if isinstance(rel, dict) else ""
                rel_type = rel.get("relationship", "related-to") if isinstance(rel, dict) else "related-to"
                if ref_id and ref_id != tp_id and ref_id in known_tp_ids:
                    relationships.append((tp_id, ref_id, rel_type))
        else:
            cross_refs = find_tp_cross_refs(body, tp_id, known_tp_ids)
            for ref_id in cross_refs:
                relationships.append((tp_id, ref_id, "related-to"))

        # Add MITRE relationships
        for tech_id in tp.get("mitre_attack", []):
            if tech_id not in mitre_patterns:
                mitre_patterns[tech_id] = build_mitre_attack_pattern(tech_id)
            mitre_ap = mitre_patterns[tech_id]
            rel = build_relationship(ap.id, mitre_ap.id, rel_type="uses")
            stix_relationships.append(rel)
            print(f"    [~] {tp_id} uses {tech_id}")

        # Add MITRE F3 relationships
        for tech_id in tp.get("mitre_f3", []):
            if tech_id not in f3_patterns:
                f3_patterns[tech_id] = build_f3_attack_pattern(tech_id)
            f3_ap = f3_patterns[tech_id]
            rel = build_relationship(ap.id, f3_ap.id, rel_type="uses")
            stix_relationships.append(rel)

        # Extended SDOs
        fs = build_fraud_scheme(tp)
        fraud_schemes[tp_id] = fs

        ft = build_financial_transaction(tp, content)
        if ft:
            fin_transactions[tp_id] = ft

        mn = build_mule_network(tp, content)
        if mn:
            mule_networks[tp_id] = mn

        ap_profile = build_fraud_actor_profile(tp, content)
        if ap_profile:
            actor_profiles[tp_id] = ap_profile

    # Build relationship objects (deduplicate bidirectional)
    seen_rels = set()
    for src_id, tgt_id, rel_type in relationships:
        # Normalize to avoid A->B and B->A duplicates
        pair = tuple(sorted([src_id, tgt_id]))
        if pair in seen_rels:
            continue
        seen_rels.add(pair)

        src_ap = attack_patterns.get(src_id)
        tgt_ap = attack_patterns.get(tgt_id)
        if src_ap and tgt_ap:
            rel = build_relationship(src_ap.id, tgt_ap.id, rel_type=rel_type)
            stix_relationships.append(rel)
            print(f"    [~] {src_id} --{rel_type}--> {tgt_id}")

    # Extended relationships
    for tp_id, fs in fraud_schemes.items():
        # monetizes: fraud-scheme -> financial-transaction
        if tp_id in fin_transactions:
            ft = fin_transactions[tp_id]
            rel = build_relationship(fs["id"], ft["id"], "monetizes")
            stix_relationships.append(rel)

        # launders-through: financial-transaction -> mule-network
        if tp_id in fin_transactions and tp_id in mule_networks:
            ft = fin_transactions[tp_id]
            mn = mule_networks[tp_id]
            rel = build_relationship(ft["id"], mn["id"], "launders-through")
            stix_relationships.append(rel)

        # recruits: actor-profile -> mule-network
        if tp_id in actor_profiles and tp_id in mule_networks:
            actor = actor_profiles[tp_id]
            mn = mule_networks[tp_id]
            rel = build_relationship(actor["id"], mn["id"], "recruits")
            stix_relationships.append(rel)

        # enables: attack-pattern -> fraud-scheme
        ap = attack_patterns.get(tp_id)
        if ap:
            rel = build_relationship(ap.id, fs["id"], "enables")
            stix_relationships.append(rel)

    # Detection rule SDOs removed — see github.com/elchacal801/flame-detections

    # ----- Baselines -> x-flame-baseline SDOs -----
    BL_DIR = Path("Baselines")
    baseline_sdos = {}

    if BL_DIR.is_dir():
        bl_files = sorted(BL_DIR.glob("*.md"))
        print(f"\n[*] Processing {len(bl_files)} baseline profiles for STIX SDOs...")

        for bl_path in bl_files:
            try:
                bl_text = bl_path.read_text(encoding="utf-8")
                meta = parse_baseline_frontmatter(bl_text)

                bl_id = meta.get("id", bl_path.stem)
                title = meta.get("title", bl_path.stem)
                tags = meta.get("tags", [])
                description = extract_baseline_description(bl_text)

                sdo = build_baseline_sdo(bl_id, title, description, tags)
                baseline_sdos[bl_id] = sdo
                print(f"    [+] {bl_id}: {title}")

            except Exception as exc:
                print(f"    [!] Error processing {bl_path.name}: {exc}")

    # Assemble bundle
    all_objects = [identity]
    all_objects.extend(attack_patterns.values())
    all_objects.extend(mitre_patterns.values())
    all_objects.extend(f3_patterns.values())
    all_objects.extend(fraud_schemes.values())
    all_objects.extend(fin_transactions.values())
    all_objects.extend(mule_networks.values())
    all_objects.extend(actor_profiles.values())
    all_objects.extend(baseline_sdos.values())
    all_objects.extend(stix_relationships)

    print(f"\n[*] Bundle summary:")
    print(f"    - Identity: 1")
    print(f"    - Threat Path attack patterns: {len(attack_patterns)}")
    print(f"    - MITRE ATT&CK patterns (stubs): {len(mitre_patterns)}")
    print(f"    - Fraud scheme SDOs: {len(fraud_schemes)}")
    print(f"    - Financial transaction SDOs: {len(fin_transactions)}")
    print(f"    - Mule network SDOs: {len(mule_networks)}")
    print(f"    - Actor profile SDOs: {len(actor_profiles)}")
    print(f"    - Baseline SDOs: {len(baseline_sdos)}")
    print(f"    - Relationships: {len(stix_relationships)}")

    # Build and validate bundle
    bundle = stix2.Bundle(
        objects=all_objects,
        id=deterministic_id("bundle", "flame-stix-bundle"),
        allow_custom=True,
    )

    # Validate by parsing back
    try:
        stix2.parse(bundle.serialize(), allow_custom=True)
        print("[+] STIX validation passed.")
    except Exception as e:
        print(f"[!] STIX validation failed: {e}")
        sys.exit(1)

    # Write STIX bundle
    OUTPUT_BUNDLE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_BUNDLE, "w", encoding="utf-8") as f:
        f.write(bundle.serialize(pretty=True))
    print(f"[+] STIX bundle written to {OUTPUT_BUNDLE}")

    print("[*] Done.")


if __name__ == "__main__":
    main()
