# Phase 3: SIGNAL (v0.5) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform FLAME into an interoperable fraud intelligence node with STIX extensions, MISP galaxy/feed, static TAXII, regulatory mapping, and a framework mapping navigator.

**Architecture:** 6 batches: A (STIX extension), B (MISP galaxy/feed), C (Static TAXII), D (Regulatory mapping), E (Framework Navigator), F (Rebuild + CI). Batch A is the critical path. B/C depend on A. D and E are independent.

**Tech Stack:** Python 3.12, stix2>=3.0.0, pyyaml, vanilla JS/CSS frontend, GitHub Actions CI.

---

## Batch A: STIX 2.1 Fraud Extension (Items 3.1-3.2)

### Task 1: Write STIX Extension Spec Document

**Files:**
- `docs/STIX-FRAUD-EXTENSION.md` — Create

**Steps:**

1. Create `docs/STIX-FRAUD-EXTENSION.md` with the formal specification for the 4 new SDOs and 5 new relationship types. The document must follow the STIX 2.1 extension specification format and include:

   - **Header**: Title "FLAME STIX 2.1 Fraud Extension Specification", version (1.0.0), namespace (`x-flame`), and scope statement (SDOs only, no SCOs).

   - **x-flame-fraud-scheme** SDO definition:
     ```
     Type Name: x-flame-fraud-scheme
     Properties:
       - scheme_type (string, required) — enum: ato, bec, synthetic-identity, app-fraud, check-fraud, wire-fraud, insurance-fraud, investment-fraud, romance-scam, first-party, insider, mule-recruitment, credential-stuffing, deepfake, identity-theft, other
       - cfpf_phases (list of string) — P1 through P5
       - loss_estimate (object) — {low: int, high: int, currency: string}
       - affected_sectors (list of string) — from FLAME taxonomy
       - kill_chain_phases (list) — STIX kill_chain_phases format using "cfpf" kill chain
       - confidence_score (integer, 0-100)
     ```

   - **x-flame-financial-transaction** SDO definition:
     ```
     Type Name: x-flame-financial-transaction
     Properties:
       - transaction_type (string, required) — enum: wire, ACH, A2A, crypto, check, card, other
       - amount_range (object) — {low: int, high: int, currency: string}
       - rail (string) — enum: SWIFT, FedWire, ACH, blockchain, card-network, RTP, other
       - velocity_pattern (string) — free-text description
     ```

   - **x-flame-mule-network** SDO definition:
     ```
     Type Name: x-flame-mule-network
     Properties:
       - recruitment_method (string, required) — enum: romance, employment, social-media, crypto-job, other
       - geographic_spread (list of string) — ISO region codes or descriptions
       - estimated_throughput (string) — free-text
       - network_type (string) — enum: individual, organized, hybrid
     ```

   - **x-flame-fraud-actor-profile** SDO definition:
     ```
     Type Name: x-flame-fraud-actor-profile
     Properties:
       - fraud_specialization (list of string) — fraud type tags
       - monetization_methods (list of string) — e.g., wire, crypto, mule
       - sophistication_level (string) — enum: low, medium, high, expert
       - jurisdiction (list of string) — operating regions
     ```

   - **Relationship Types** table with source_type, target_type, and semantic description for: `monetizes`, `launders-through`, `impersonates`, `recruits`, `enables`.

   - **UUID Namespace** section explaining deterministic ID generation using `uuid5(NAMESPACE_DNS, "flame-{tp_id}-{sdo_suffix}")`.

   - **Backward Compatibility** note: existing `attack-pattern` SDOs remain in the bundle. New SDOs are additive.

2. Verify the document renders correctly in a markdown viewer.

**Commit:** `docs: add STIX 2.1 Fraud Extension specification`

---

### Task 2: Add Fraud Scheme SDO Builder

**Files:**
- `tests/test_export_stix.py` — Modify (add tests)
- `scripts/export_flame_stix.py` — Modify (add builder function)

**Steps:**

1. Add test class `TestBuildFraudScheme` in `tests/test_export_stix.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_flame_stix import build_fraud_scheme, deterministic_id

class TestBuildFraudScheme:
    def test_basic_scheme(self):
        tp = {
            "id": "TP-0001",
            "title": "Treasury Management ATO",
            "summary": "Test summary",
            "fraud_types": ["account-takeover", "wire-fraud"],
            "cfpf_phases": ["P1", "P2", "P3", "P4", "P5"],
            "sector": ["banking"],
            "confidence_score": 82,
            "mitre_attack": ["T1566.002"],
        }
        result = build_fraud_scheme(tp)
        assert result["type"] == "x-flame-fraud-scheme"
        assert result["scheme_type"] == "ato"
        assert "P1" in result["cfpf_phases"]
        assert result["confidence_score"] == 82

    def test_deterministic_id(self):
        tp = {"id": "TP-0001", "title": "Test", "fraud_types": ["bec"],
              "cfpf_phases": ["P1"], "sector": [], "confidence_score": 50}
        r1 = build_fraud_scheme(tp)
        r2 = build_fraud_scheme(tp)
        assert r1["id"] == r2["id"]

    def test_missing_optional_fields(self):
        tp = {"id": "TP-0099", "title": "Minimal", "fraud_types": [],
              "cfpf_phases": [], "sector": []}
        result = build_fraud_scheme(tp)
        assert result["type"] == "x-flame-fraud-scheme"
        assert result["scheme_type"] == "other"
```

2. Run `python -m pytest tests/test_export_stix.py::TestBuildFraudScheme -v` -- expect FAIL (function does not exist yet).

3. Add the `SCHEME_TYPE_MAP` constant and `build_fraud_scheme()` function in `scripts/export_flame_stix.py` after the existing `build_external_refs()` function (around line 138):

```python
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
    "romance-scam": "romance-scam",
    "first-party": "first-party",
    "insider": "insider",
    "mule-recruitment": "mule-recruitment",
    "credential-stuffing": "credential-stuffing",
    "deepfake": "deepfake",
    "identity-theft": "identity-theft",
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
        "id": deterministic_id("x-flame-fraud-scheme", f"flame-{tp_id}-fraud-scheme"),
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
    return obj
```

4. Run `python -m pytest tests/test_export_stix.py::TestBuildFraudScheme -v` -- expect PASS.

---

### Task 3: Add Financial Transaction SDO Builder

**Files:**
- `tests/test_export_stix.py` — Modify (add tests)
- `scripts/export_flame_stix.py` — Modify (add builder function)

**Steps:**

1. Add test class `TestBuildFinancialTransaction` in `tests/test_export_stix.py`:

```python
from export_flame_stix import build_financial_transaction

class TestBuildFinancialTransaction:
    def test_wire_transaction(self):
        tp = {"id": "TP-0001", "title": "Test", "fraud_types": ["wire-fraud"],
              "cfpf_phases": ["P4", "P5"]}
        content = {"body": "## CFPF Phase Mapping\n### Phase 4: Execution\nWire transfer via SWIFT\n### Phase 5: Monetization\nFunds moved to mule accounts"}
        result = build_financial_transaction(tp, content)
        assert result is not None
        assert result["type"] == "x-flame-financial-transaction"

    def test_no_p4_p5_returns_none(self):
        tp = {"id": "TP-TEST", "title": "Test", "fraud_types": [],
              "cfpf_phases": ["P1", "P2"]}
        content = {"body": "## Summary\nNo execution phase"}
        result = build_financial_transaction(tp, content)
        assert result is None
```

2. Run tests -- expect FAIL.

3. Add `build_financial_transaction()` function in `scripts/export_flame_stix.py`:

```python
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
```

4. Run tests -- expect PASS.

---

### Task 4: Add Mule Network SDO Builder

**Files:**
- `tests/test_export_stix.py` — Modify (add tests)
- `scripts/export_flame_stix.py` — Modify (add builder function)

**Steps:**

1. Add test class `TestBuildMuleNetwork`:

```python
from export_flame_stix import build_mule_network

class TestBuildMuleNetwork:
    def test_mule_tp(self):
        tp = {"id": "TP-0011", "title": "Romance Scam Mule Pipeline",
              "fraud_types": ["romance-scam", "mule-recruitment"]}
        content = {"body": "Money mule recruitment via social media. Mule accounts used for laundering."}
        result = build_mule_network(tp, content)
        assert result is not None
        assert result["type"] == "x-flame-mule-network"

    def test_no_mule_reference_returns_none(self):
        tp = {"id": "TP-TEST", "title": "No Mules", "fraud_types": ["phishing"]}
        content = {"body": "Basic phishing scheme with no mule involvement."}
        result = build_mule_network(tp, content)
        assert result is None
```

2. Run tests -- expect FAIL.

3. Add `build_mule_network()`:

```python
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
```

4. Run tests -- expect PASS.

---

### Task 5: Add Fraud Actor Profile SDO Builder

**Files:**
- `tests/test_export_stix.py` — Modify (add tests)
- `scripts/export_flame_stix.py` — Modify (add builder function)

**Steps:**

1. Add test class `TestBuildFraudActorProfile`:

```python
from export_flame_stix import build_fraud_actor_profile

class TestBuildFraudActorProfile:
    def test_with_underground_context(self):
        tp = {"id": "TP-0001", "title": "Test", "fraud_types": ["account-takeover"]}
        content = {"body": "## Underground Ecosystem Context\n### Service Supply Chain\nInfostealer MaaS kits available"}
        result = build_fraud_actor_profile(tp, content)
        assert result is not None
        assert result["type"] == "x-flame-fraud-actor-profile"
        assert "account-takeover" in result["fraud_specialization"]

    def test_no_underground_section_returns_none(self):
        tp = {"id": "TP-TEST", "title": "No Underground", "fraud_types": []}
        content = {"body": "## Summary\nBasic scheme."}
        result = build_fraud_actor_profile(tp, content)
        assert result is None
```

2. Run tests -- expect FAIL.

3. Add `build_fraud_actor_profile()`:

```python
import re

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
```

4. Run tests -- expect PASS.

---

### Task 6: Add New Relationship Types and Integrate SDOs into Main Loop

**Files:**
- `tests/test_export_stix.py` — Modify (add integration tests)
- `scripts/export_flame_stix.py` — Modify (update `main()`)

**Steps:**

1. Add test class `TestNewRelationshipTypes`:

```python
from export_flame_stix import build_relationship, deterministic_id

class TestNewRelationshipTypes:
    def test_monetizes_relationship(self):
        src = deterministic_id("x-flame-fraud-scheme", "test-scheme")
        tgt = deterministic_id("x-flame-financial-transaction", "test-txn")
        rel = build_relationship(src, tgt, "monetizes")
        assert rel.relationship_type == "monetizes"

    def test_launders_through_relationship(self):
        src = deterministic_id("x-flame-financial-transaction", "test-txn")
        tgt = deterministic_id("x-flame-mule-network", "test-mule")
        rel = build_relationship(src, tgt, "launders-through")
        assert rel.relationship_type == "launders-through"

    def test_recruits_relationship(self):
        src = deterministic_id("x-flame-fraud-actor-profile", "test-actor")
        tgt = deterministic_id("x-flame-mule-network", "test-mule")
        rel = build_relationship(src, tgt, "recruits")
        assert rel.relationship_type == "recruits"
```

2. Run tests -- expect PASS (the existing `build_relationship()` function already accepts custom `rel_type` strings, so this validates that behavior).

3. Update the `main()` function in `scripts/export_flame_stix.py` to generate extended SDOs. In the main loop (around line 318), after `attack_patterns[tp_id] = ap`, add:

```python
    # Build extended SDOs
    fraud_schemes = {}    # tp_id -> dict
    fin_transactions = {} # tp_id -> dict
    mule_networks = {}    # tp_id -> dict
    actor_profiles = {}   # tp_id -> dict

    for tp in index:
        tp_id = tp["id"]
        # ... existing attack-pattern code ...

        content = load_tp_content(tp_id)
        body = content.get("body", "") if content else ""

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
```

4. After the main loop, add extended relationship generation:

```python
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
```

5. Update bundle assembly to include custom objects. Since stix2 `Bundle` requires stix2 objects or dicts with `allow_custom=True`, the custom SDO dicts can be appended directly:

```python
    # Assemble bundle
    all_objects = [identity]
    all_objects.extend(attack_patterns.values())
    all_objects.extend(mitre_patterns.values())
    all_objects.extend(fraud_schemes.values())       # NEW
    all_objects.extend(fin_transactions.values())     # NEW
    all_objects.extend(mule_networks.values())        # NEW
    all_objects.extend(actor_profiles.values())       # NEW
    all_objects.extend(stix_relationships)
```

6. Update the summary printout to include new SDO counts.

7. Run the full STIX export: `python scripts/export_flame_stix.py`

8. Verify `database/flame_stix_bundle.json` contains the new object types.

9. Run full test suite: `python -m pytest tests/test_export_stix.py -v`

**Commit:** `feat(stix): add 4 fraud SDO builders and 5 relationship types for STIX extension`

---

## Batch B: MISP Galaxy & Feed (Items 3.3-3.5)

### Task 7: Create MISP Export Script with Galaxy and Cluster Generation

**Files:**
- `scripts/export_misp.py` — Create
- `tests/test_export_misp.py` — Create

**Steps:**

1. Create `tests/test_export_misp.py` with tests:

```python
"""Tests for FLAME MISP export pipeline."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_misp import build_galaxy, build_cluster_entry, build_feed_event


class TestBuildGalaxy:
    def test_galaxy_structure(self):
        galaxy = build_galaxy()
        assert galaxy["type"] == "flame-fraud"
        assert galaxy["name"] == "FLAME Fraud Threat Paths"
        assert galaxy["namespace"] == "flame"
        assert "uuid" in galaxy
        assert galaxy["version"] == 1

    def test_galaxy_deterministic_uuid(self):
        g1 = build_galaxy()
        g2 = build_galaxy()
        assert g1["uuid"] == g2["uuid"]


class TestBuildClusterEntry:
    def test_cluster_entry(self):
        tp = {
            "id": "TP-0001",
            "title": "Treasury Management ATO",
            "summary": "Test summary",
            "fraud_types": ["account-takeover"],
            "sector": ["banking"],
            "cfpf_phases": ["P1", "P2"],
            "mitre_attack": ["T1566.002"],
            "confidence_score": 82,
        }
        entry = build_cluster_entry(tp)
        assert entry["value"] == "Treasury Management ATO"
        assert "uuid" in entry
        assert entry["meta"]["fraud_types"] == ["account-takeover"]
        assert len(entry["related"]) >= 1  # MITRE ATT&CK relation

    def test_deterministic_uuid(self):
        tp = {"id": "TP-0001", "title": "Test", "summary": "",
              "fraud_types": [], "sector": [], "cfpf_phases": [],
              "mitre_attack": [], "confidence_score": 0}
        e1 = build_cluster_entry(tp)
        e2 = build_cluster_entry(tp)
        assert e1["uuid"] == e2["uuid"]


class TestBuildFeedEvent:
    def test_event_structure(self):
        tp = {"id": "TP-0001", "title": "Test TP", "summary": "Summary",
              "fraud_types": ["ato"], "sector": ["banking"],
              "cfpf_phases": ["P1"], "mitre_attack": [], "date": "2026-01-01",
              "confidence_score": 80}
        event = build_feed_event(tp)
        assert "Event" in event
        assert event["Event"]["info"] == "FLAME: Test TP"
        assert "Attribute" in event["Event"]
        assert "uuid" in event["Event"]
```

2. Run tests -- expect FAIL.

3. Create `scripts/export_misp.py`:

```python
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
        "refs": [f"https://elchacal801.github.io/flame-fraud/?tp={tp_id}"],
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
```

4. Run tests: `python -m pytest tests/test_export_misp.py -v` -- expect PASS.

5. Run the export: `python scripts/export_misp.py` -- verify output files exist.

**Commit:** `feat(misp): add MISP galaxy, cluster, and feed export pipeline`

---

## Batch C: Static TAXII Endpoints (Item 3.9)

### Task 8: Create Static TAXII Export Script

**Files:**
- `scripts/export_taxii.py` — Create
- `tests/test_export_taxii.py` — Create

**Steps:**

1. Create `tests/test_export_taxii.py`:

```python
"""Tests for FLAME TAXII static endpoint generator."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_taxii import build_discovery, build_collections, build_manifest


class TestBuildDiscovery:
    def test_discovery_structure(self):
        disc = build_discovery()
        assert disc["title"] == "FLAME TAXII Server"
        assert "default" in disc["default"]
        assert "api_roots" in disc

class TestBuildCollections:
    def test_collections_count(self):
        result = build_collections()
        assert "collections" in result
        assert len(result["collections"]) == 3

    def test_collection_ids_deterministic(self):
        c1 = build_collections()
        c2 = build_collections()
        for i in range(3):
            assert c1["collections"][i]["id"] == c2["collections"][i]["id"]

class TestBuildManifest:
    def test_manifest_structure(self):
        objects = [
            {"type": "x-flame-fraud-scheme", "id": "x-flame-fraud-scheme--abc",
             "modified": "2026-01-01T00:00:00Z", "spec_version": "2.1"}
        ]
        manifest = build_manifest(objects)
        assert "objects" in manifest
        assert len(manifest["objects"]) == 1
        assert manifest["objects"][0]["id"] == "x-flame-fraud-scheme--abc"
```

2. Run tests -- expect FAIL.

3. Create `scripts/export_taxii.py`:

```python
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
```

4. Run tests: `python -m pytest tests/test_export_taxii.py -v` -- expect PASS.

5. Run the export: `python scripts/export_taxii.py` -- verify `api/taxii/discovery.json` and collection directories exist.

**Commit:** `feat(taxii): add static TAXII 2.1 endpoint generator`

---

## Batch D: Regulatory Compliance Mapping (Items 3.7-3.8)

### Task 9: Create Regulatory Requirements Config

**Files:**
- `config/regulatory_requirements.yaml` — Create

**Steps:**

1. Create `config/regulatory_requirements.yaml` with ~15 key regulations. Structure each entry as:

```yaml
regulations:
  - id: REG-PSD3-SCA
    name: "PSD3 Strong Customer Authentication"
    jurisdiction: EU
    category: authentication
    description: "Requires multi-factor authentication for electronic payments"
    relevant_fraud_types:
      - account-takeover
      - unauthorized-transaction
      - phishing

  - id: REG-UK-PSR-APP
    name: "UK PSR APP Reimbursement"
    jurisdiction: UK
    category: reimbursement
    description: "Mandatory reimbursement for APP fraud victims"
    relevant_fraud_types:
      - authorized-push-payment
      - impersonation
      - social-engineering

  - id: REG-FINCEN-AML
    name: "FinCEN AML/BSA"
    jurisdiction: US
    category: anti-money-laundering
    description: "Bank Secrecy Act anti-money laundering requirements"
    relevant_fraud_types:
      - money-laundering
      - mule-recruitment
      - wire-fraud

  - id: REG-FATF-R16
    name: "FATF Recommendation 16 (Travel Rule)"
    jurisdiction: International
    category: wire-transfer
    description: "Originator and beneficiary information for wire transfers"
    relevant_fraud_types:
      - wire-fraud
      - money-laundering

  - id: REG-MAS-SRF
    name: "MAS Shared Responsibility Framework"
    jurisdiction: Singapore
    category: shared-responsibility
    description: "Framework for sharing losses from authorized push payment scams"
    relevant_fraud_types:
      - authorized-push-payment
      - phishing

  - id: REG-AU-SPF
    name: "Australia Scam Prevention Framework"
    jurisdiction: Australia
    category: scam-prevention
    description: "Obligations for banks, telcos, and platforms to prevent scams"
    relevant_fraud_types:
      - authorized-push-payment
      - romance-scam
      - investment-fraud

  - id: REG-FFIEC-AUTH
    name: "FFIEC Authentication Guidance"
    jurisdiction: US
    category: authentication
    description: "Federal guidance on authentication and access risk management"
    relevant_fraud_types:
      - account-takeover
      - credential-stuffing

  - id: REG-CFPB-REGE
    name: "CFPB Regulation E"
    jurisdiction: US
    category: consumer-protection
    description: "Electronic fund transfer consumer protection, unauthorized transaction liability"
    relevant_fraud_types:
      - unauthorized-transaction
      - account-takeover
      - ACH-fraud

  - id: REG-DORA
    name: "EU DORA"
    jurisdiction: EU
    category: operational-resilience
    description: "Digital Operational Resilience Act for financial entities"
    relevant_fraud_types:
      - account-takeover
      - deepfake

  - id: REG-FCA-APP
    name: "FCA Confirmation of Payee"
    jurisdiction: UK
    category: payment-verification
    description: "Name-checking for faster payment recipients"
    relevant_fraud_types:
      - authorized-push-payment
      - wire-fraud

  - id: REG-FINCEN-CDD
    name: "FinCEN CDD Rule"
    jurisdiction: US
    category: customer-due-diligence
    description: "Customer Due Diligence requirements for financial institutions"
    relevant_fraud_types:
      - synthetic-identity
      - identity-theft
      - application-fraud

  - id: REG-SEC-SAR
    name: "SEC Suspicious Activity Reporting"
    jurisdiction: US
    category: reporting
    description: "Broker-dealer SAR filing requirements"
    relevant_fraud_types:
      - investment-fraud
      - insider
      - money-laundering

  - id: REG-OCC-FRAUD
    name: "OCC Fraud Risk Management"
    jurisdiction: US
    category: risk-management
    description: "OCC guidance on fraud risk management for national banks"
    relevant_fraud_types:
      - account-takeover
      - check-fraud
      - wire-fraud

  - id: REG-EU-AMLD6
    name: "EU 6th Anti-Money Laundering Directive"
    jurisdiction: EU
    category: anti-money-laundering
    description: "Enhanced AML requirements including corporate criminal liability"
    relevant_fraud_types:
      - money-laundering
      - mule-recruitment

  - id: REG-FBI-IC3
    name: "FBI IC3 Recovery Asset Team"
    jurisdiction: US
    category: recovery
    description: "Financial Fraud Kill Chain for wire transfer recovery"
    relevant_fraud_types:
      - wire-fraud
      - BEC
```

**Commit:** `feat(regulatory): add regulatory requirements configuration`

---

### Task 10: Update Validation Script for regulatory_refs

**Files:**
- `tests/test_validate_submission.py` — Modify (add tests)
- `scripts/validate_submission.py` — Modify (add validation)

**Steps:**

1. Add test cases in `tests/test_validate_submission.py` for regulatory_refs validation. Follow the existing test patterns (there are no test classes in the current file, check actual pattern):

```python
# In the test file, add tests for the new field
class TestRegulatoryRefs:
    def test_valid_regulatory_refs(self, tmp_path):
        """Valid regulatory_refs should pass."""
        # Create a TP file with regulatory_refs
        content = VALID_TP_WITH_REG_REFS  # fixture with regulatory_refs: [REG-PSD3-SCA]
        fp = tmp_path / "TP-9990-test-reg.md"
        fp.write_text(content, encoding="utf-8")
        result = validate_file(fp)
        assert result.passed

    def test_invalid_regulatory_ref_id(self, tmp_path):
        """Invalid regulatory ref ID should produce error."""
        content = VALID_TP_WITH_BAD_REG_REFS  # fixture with regulatory_refs: [INVALID-REG]
        fp = tmp_path / "TP-9991-test-bad-reg.md"
        fp.write_text(content, encoding="utf-8")
        result = validate_file(fp)
        assert any("regulatory_refs" in e.lower() or "INVALID-REG" in e for e in result.errors)
```

2. Run tests -- expect FAIL.

3. In `scripts/validate_submission.py`, add after the taxonomy loading block (around line 56):

```python
# Load regulatory requirements config for validation
REGULATORY_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "regulatory_requirements.yaml"
VALID_REGULATORY_IDS = set()
try:
    with open(REGULATORY_CONFIG_FILE, "r", encoding="utf-8") as _f:
        _reg_config = yaml.safe_load(_f)
        if _reg_config and "regulations" in _reg_config:
            VALID_REGULATORY_IDS = {r["id"] for r in _reg_config["regulations"] if "id" in r}
except Exception as _e:
    print(f"WARNING: Failed to load regulatory config from {REGULATORY_CONFIG_FILE}: {_e}", file=sys.stderr)
```

4. In the `validate_file()` function, add after the `related_tps` validation block (around line 391):

```python
    # --- Regulatory references (optional) ---
    regulatory_refs = meta.get("regulatory_refs")
    if regulatory_refs is not None:
        if not isinstance(regulatory_refs, list):
            result.error("regulatory_refs must be a list")
        else:
            for ref in regulatory_refs:
                if ref not in VALID_REGULATORY_IDS:
                    result.error(f"Unrecognized regulatory_refs entry '{ref}' (not in config/regulatory_requirements.yaml)")
```

5. Run tests -- expect PASS.

**Commit:** `feat(validate): add regulatory_refs validation against config`

---

### Task 11: Update Build Pipeline for regulatory_refs

**Files:**
- `tests/test_build_database.py` — Modify (add tests)
- `scripts/build_database.py` — Modify (schema + parsing)

**Steps:**

1. Add test for regulatory_refs in `tests/test_build_database.py`:

```python
class TestRegulatoryRefs:
    def test_regulatory_refs_stored(self, test_db):
        """regulatory_refs should be inserted into submission_regulatory_refs table."""
        _insert_multi(test_db, "submission_regulatory_refs", "TP-REG-TEST", "reg_id",
                      ["REG-PSD3-SCA", "REG-FFIEC-AUTH"])
        result = _fetch_list(test_db, "submission_regulatory_refs", "reg_id", "TP-REG-TEST")
        assert "REG-PSD3-SCA" in result
        assert "REG-FFIEC-AUTH" in result
```

2. Run tests -- expect FAIL.

3. Update `scripts/build_database.py`:

   a. Add to SCHEMA (after `submission_groupib_stages` table, around line 234):
   ```sql
   CREATE TABLE IF NOT EXISTS submission_regulatory_refs (
       submission_id TEXT NOT NULL,
       reg_id TEXT NOT NULL,
       FOREIGN KEY (submission_id) REFERENCES submissions(id)
   );
   CREATE INDEX IF NOT EXISTS idx_regulatory_refs ON submission_regulatory_refs(reg_id);
   ```

   b. Add to `_VALID_MULTI_TABLES` set (line 400):
   ```python
   ("submission_regulatory_refs", "reg_id"),
   ```

   c. Add to `load_submission()` (after line 377):
   ```python
   _insert_multi(conn, "submission_regulatory_refs", sub_id, "reg_id", meta.get("regulatory_refs", []))
   ```

   d. Add to `_build_full_entry()` function to include regulatory_refs in JSON exports:
   ```python
   entry["regulatory_refs"] = _fetch_list(conn, "submission_regulatory_refs", "reg_id", sub_id)
   ```

4. Run tests -- expect PASS.

5. Run full build: `python scripts/build_database.py` -- verify `database/flame-index.json` entries now include `regulatory_refs` field (empty arrays for now, until TP files are updated).

**Commit:** `feat(build): add regulatory_refs to schema, parsing, and JSON exports`

---

### Task 12: Add regulatory_refs to TP Frontmatter Files

**Files:**
- 33 `ThreatPaths/TP-*.md` files — Modify
- `Templates/threat-path-template.md` — Modify

**Steps:**

1. First, update `Templates/threat-path-template.md` to add the `regulatory_refs` field in the frontmatter block, after `related_tps` and before `tags`:

```yaml
# Regulatory compliance mapping
regulatory_refs: []               # IDs from config/regulatory_requirements.yaml
                                  # e.g., REG-PSD3-SCA, REG-FFIEC-AUTH
```

2. For each of the 33 TP files, add `regulatory_refs` to the frontmatter based on the TP's fraud_types and sectors matched against the config's `relevant_fraud_types`. Use the following mapping logic:

   - TPs with `account-takeover` fraud type: `REG-PSD3-SCA`, `REG-FFIEC-AUTH`, `REG-CFPB-REGE`, `REG-OCC-FRAUD`
   - TPs with `wire-fraud` / `BEC`: `REG-FATF-R16`, `REG-FBI-IC3`, `REG-OCC-FRAUD`
   - TPs with `authorized-push-payment`: `REG-UK-PSR-APP`, `REG-MAS-SRF`, `REG-AU-SPF`, `REG-FCA-APP`
   - TPs with `mule-recruitment` or `money-laundering`: `REG-FINCEN-AML`, `REG-EU-AMLD6`
   - TPs with `synthetic-identity` or `identity-theft` or `application-fraud`: `REG-FINCEN-CDD`
   - TPs with `investment-fraud`: `REG-SEC-SAR`
   - TPs with `check-fraud`: `REG-OCC-FRAUD`
   - TPs with `credential-stuffing`: `REG-FFIEC-AUTH`
   - TPs with `deepfake`: `REG-DORA`

   The field should be added in the YAML frontmatter, after `related_tps` and before `tags`, e.g.:

   ```yaml
   regulatory_refs:
     - REG-PSD3-SCA
     - REG-FFIEC-AUTH
   ```

3. Run validation on all modified files:
   ```
   for f in ThreatPaths/TP-*.md; do python scripts/validate_submission.py "$f"; done
   ```

4. Run full build: `python scripts/build_database.py`

**Commit:** `feat(regulatory): add regulatory_refs to all 33 TP files and template`

---

### Task 13: Add Regulatory Badges to Frontend

**Files:**
- `index.html` — Modify (no changes needed -- badges render in JS-populated detail-content)
- `app.js` — Modify (add regulatory section to `renderDetailView`)
- `style.css` — Modify (add regulatory badge styles)

**Steps:**

1. In `app.js`, in the `renderDetailView()` function, add a new tag group for regulatory refs. Insert after the existing tags section (around line 606, after the `tags.length > 0` block and before `html += '</div>';` that closes `detail-taxonomy`):

```javascript
        // Regulatory refs
        const regRefs = item.regulatory_refs || [];
        if (regRefs.length > 0) {
            html += '<div class="tag-group"><h4>Regulatory Coverage</h4><div class="tag-list">';
            regRefs.forEach(function (ref) {
                // Extract jurisdiction from the ref ID pattern
                var jurisdiction = '';
                if (ref.indexOf('EU-') !== -1 || ref.indexOf('PSD') !== -1 || ref.indexOf('DORA') !== -1 || ref.indexOf('AMLD') !== -1) jurisdiction = 'EU';
                else if (ref.indexOf('UK-') !== -1 || ref.indexOf('FCA') !== -1) jurisdiction = 'UK';
                else if (ref.indexOf('MAS') !== -1) jurisdiction = 'SG';
                else if (ref.indexOf('AU-') !== -1) jurisdiction = 'AU';
                else if (ref.indexOf('FINCEN') !== -1 || ref.indexOf('FFIEC') !== -1 || ref.indexOf('CFPB') !== -1 || ref.indexOf('SEC') !== -1 || ref.indexOf('OCC') !== -1 || ref.indexOf('FBI') !== -1) jurisdiction = 'US';
                else if (ref.indexOf('FATF') !== -1) jurisdiction = 'INTL';

                var jurisdictionClass = jurisdiction ? ' reg-' + jurisdiction.toLowerCase() : '';
                html += '<span class="detail-tag regulatory-tag' + jurisdictionClass + '" title="' + escapeHtml(ref) + '">';
                if (jurisdiction) html += '<span class="reg-jurisdiction">' + jurisdiction + '</span> ';
                html += escapeHtml(ref.replace('REG-', ''));
                html += '</span>';
            });
            html += '</div></div>';
        }
```

2. In `style.css`, add regulatory badge styles (after the existing tag styles):

```css
/* Regulatory Tags */
.regulatory-tag {
    background: rgba(251, 191, 36, 0.10);
    color: #fbbf24;
    border: 1px solid rgba(251, 191, 36, 0.20);
}

.reg-jurisdiction {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    opacity: 0.7;
    margin-right: 2px;
}

.reg-us { border-color: rgba(59, 130, 246, 0.30); color: #60a5fa; background: rgba(59, 130, 246, 0.08); }
.reg-eu { border-color: rgba(168, 85, 247, 0.30); color: #c084fc; background: rgba(168, 85, 247, 0.08); }
.reg-uk { border-color: rgba(244, 63, 94, 0.30); color: #fb7185; background: rgba(244, 63, 94, 0.08); }
.reg-sg { border-color: rgba(34, 197, 94, 0.30); color: #4ade80; background: rgba(34, 197, 94, 0.08); }
.reg-au { border-color: rgba(251, 191, 36, 0.30); color: #fbbf24; background: rgba(251, 191, 36, 0.08); }
.reg-intl { border-color: rgba(14, 165, 233, 0.30); color: #38bdf8; background: rgba(14, 165, 233, 0.08); }
```

3. Start a local dev server, open a TP detail view (e.g., `#tp=TP-0001`), and verify regulatory badges appear with correct jurisdiction colors.

**Commit:** `feat(frontend): add regulatory compliance badges to detail view`

---

## Batch E: Framework Mapping Navigator (Item 3.6)

### Task 14: Add Navigator Modal HTML

**Files:**
- `index.html` — Modify (add modal)

**Steps:**

1. In `index.html`, add a new Navigator icon button in the `header-stats` div (after the graph button, before the closing `</div>` of `header-stats`, around line 68):

```html
                <button class="heat-map-btn" id="navigator-btn" title="Framework Navigator">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <line x1="3" y1="9" x2="21" y2="9"/>
                        <line x1="3" y1="15" x2="21" y2="15"/>
                        <line x1="9" y1="3" x2="9" y2="21"/>
                        <line x1="15" y1="3" x2="15" y2="21"/>
                    </svg>
                </button>
```

2. Add the Navigator modal (after the Graph modal, around line 271):

```html
    <!-- ================================================================ -->
    <!-- Framework Navigator Modal                                        -->
    <!-- ================================================================ -->
    <div class="modal-overlay" id="navigator-modal" style="display:none;">
        <div class="modal-content modal-wide modal-navigator">
            <div class="modal-header">
                <h2>Framework Mapping Navigator</h2>
                <div class="navigator-actions">
                    <button class="nav-export-btn" id="nav-export-svg" title="Export SVG">SVG</button>
                    <button class="nav-export-btn" id="nav-export-json" title="Export ATT&CK Navigator JSON" style="display:none;">JSON</button>
                    <button class="modal-close" id="navigator-close">&times;</button>
                </div>
            </div>
            <div class="navigator-tabs" id="navigator-tabs">
                <button class="nav-tab active" data-framework="cfpf">CFPF</button>
                <button class="nav-tab" data-framework="ft3">FT3</button>
                <button class="nav-tab" data-framework="groupib">Group-IB</button>
                <button class="nav-tab" data-framework="attack">ATT&CK</button>
            </div>
            <div class="navigator-legend">
                <span class="nav-legend-item"><span class="nav-legend-cell nav-cell-high"></span> 3+ rules</span>
                <span class="nav-legend-item"><span class="nav-legend-cell nav-cell-med"></span> 1-2 rules</span>
                <span class="nav-legend-item"><span class="nav-legend-cell nav-cell-low"></span> Mapped, no rules</span>
                <span class="nav-legend-item"><span class="nav-legend-cell nav-cell-empty"></span> Not mapped</span>
            </div>
            <div class="modal-body navigator-body" id="navigator-body">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>
```

**Commit:** (combined with Task 15)

---

### Task 15: Implement renderNavigator() in app.js

**Files:**
- `app.js` — Modify (add function, DOM refs, event bindings)

**Steps:**

1. In `cacheDom()`, add:
```javascript
        dom.navigatorBtn = document.getElementById('navigator-btn');
        dom.navigatorModal = document.getElementById('navigator-modal');
        dom.navigatorClose = document.getElementById('navigator-close');
        dom.navigatorBody = document.getElementById('navigator-body');
        dom.navigatorTabs = document.getElementById('navigator-tabs');
```

2. In `bindEvents()`, add after the graph modal bindings (around line 214):
```javascript
        // Framework Navigator
        dom.navigatorBtn.addEventListener('click', function () {
            dom.navigatorModal.style.display = 'flex';
            renderNavigator('cfpf');
        });
        dom.navigatorClose.addEventListener('click', function () { dom.navigatorModal.style.display = 'none'; });
        dom.navigatorModal.addEventListener('click', function (e) { if (e.target === dom.navigatorModal) dom.navigatorModal.style.display = 'none'; });

        // Navigator tab switching
        dom.navigatorTabs.addEventListener('click', function (e) {
            var tab = e.target.closest('.nav-tab');
            if (!tab) return;
            dom.navigatorTabs.querySelectorAll('.nav-tab').forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');
            var framework = tab.getAttribute('data-framework');
            renderNavigator(framework);
            // Show/hide JSON export button (only for ATT&CK)
            document.getElementById('nav-export-json').style.display = framework === 'attack' ? 'inline-block' : 'none';
        });

        // Navigator exports
        document.getElementById('nav-export-svg').addEventListener('click', exportNavigatorSVG);
        document.getElementById('nav-export-json').addEventListener('click', exportNavigatorATTCKJSON);
```

3. Add the `renderNavigator()` function (after `renderHeatMap()`, around line 1071):

```javascript
    // -----------------------------------------------------------------------
    // Framework Navigator
    // -----------------------------------------------------------------------

    const FT3_STAGES = [
        'FTA001', 'FTA002', 'FTA003', 'FTA004', 'FTA005',
        'FTA006', 'FTA007', 'FTA008', 'FTA009', 'FTA010', 'FTA011', 'FTA012'
    ];

    function renderNavigator(framework) {
        var data = FlameData.getData();
        if (!data || data.length === 0) {
            dom.navigatorBody.innerHTML = '<p>No data available.</p>';
            return;
        }

        // Determine columns based on framework
        var columns = [];
        var getMapping = null;

        switch (framework) {
            case 'cfpf':
                columns = PHASE_ORDER;  // ['P1','P2','P3','P4','P5']
                getMapping = function (item) { return item.cfpf_phases || []; };
                break;
            case 'ft3':
                // Collect all unique FT3 tactic IDs across all TPs
                var ft3Set = new Set();
                data.forEach(function (item) {
                    (item.ft3_tactics || []).forEach(function (t) { ft3Set.add(t); });
                });
                columns = Array.from(ft3Set).sort();
                getMapping = function (item) { return item.ft3_tactics || []; };
                break;
            case 'groupib':
                columns = GROUPIB_STAGES;
                getMapping = function (item) { return item.groupib_stages || []; };
                break;
            case 'attack':
                var attackSet = new Set();
                data.forEach(function (item) {
                    (item.mitre_attack || []).forEach(function (t) { attackSet.add(t); });
                });
                columns = Array.from(attackSet).sort();
                getMapping = function (item) { return item.mitre_attack || []; };
                break;
        }

        if (columns.length === 0) {
            dom.navigatorBody.innerHTML = '<p>No mapping data available for this framework.</p>';
            return;
        }

        // Build the CSS Grid matrix
        var gridCols = columns.length + 1;  // +1 for the TP label column
        var html = '<div class="navigator-grid" style="grid-template-columns: 180px repeat(' + columns.length + ', minmax(60px, 1fr));" id="navigator-grid">';

        // Header row
        html += '<div class="nav-cell nav-corner"></div>';
        columns.forEach(function (col) {
            html += '<div class="nav-cell nav-col-header" title="' + escapeHtml(col) + '">' + escapeHtml(col) + '</div>';
        });

        // Data rows (one per TP)
        data.forEach(function (item) {
            var mapping = getMapping(item);
            html += '<div class="nav-cell nav-row-label" title="' + escapeHtml(item.title) + '">';
            html += '<a href="#tp=' + escapeHtml(item.id) + '" class="nav-tp-link">' + escapeHtml(item.id) + '</a>';
            html += '</div>';

            columns.forEach(function (col) {
                var isMapped = mapping.indexOf(col) !== -1;
                var dlCount = (item.detection_rule_ids || []).length; // approximate
                var cellClass = 'nav-cell nav-data';
                if (isMapped) {
                    if (dlCount >= 3) cellClass += ' nav-cell-high';
                    else if (dlCount >= 1) cellClass += ' nav-cell-med';
                    else cellClass += ' nav-cell-low';
                } else {
                    cellClass += ' nav-cell-empty';
                }
                html += '<div class="' + cellClass + '" title="' + escapeHtml(item.title) + ' × ' + escapeHtml(col) + '" data-tp="' + escapeHtml(item.id) + '">';
                html += '</div>';
            });
        });

        html += '</div>';
        dom.navigatorBody.innerHTML = html;

        // Click-to-navigate
        dom.navigatorBody.querySelectorAll('.nav-data').forEach(function (cell) {
            cell.addEventListener('click', function () {
                var tpId = cell.getAttribute('data-tp');
                if (tpId) {
                    dom.navigatorModal.style.display = 'none';
                    window.location.hash = '#tp=' + tpId;
                }
            });
        });
    }

    function exportNavigatorSVG() {
        var grid = document.getElementById('navigator-grid');
        if (!grid) return;
        // Use html2canvas-style approach: create SVG from grid DOM
        // Simplified: serialize to SVG foreignObject
        var rect = grid.getBoundingClientRect();
        var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + rect.width + '" height="' + rect.height + '">';
        svg += '<foreignObject width="100%" height="100%">';
        svg += '<div xmlns="http://www.w3.org/1999/xhtml">';
        svg += grid.outerHTML;
        svg += '</div></foreignObject></svg>';

        var blob = new Blob([svg], { type: 'image/svg+xml' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'flame-navigator.svg';
        a.click();
        URL.revokeObjectURL(url);
    }

    function exportNavigatorATTCKJSON() {
        var data = FlameData.getData();
        if (!data) return;
        // Build ATT&CK Navigator layer format
        var techniques = [];
        data.forEach(function (item) {
            (item.mitre_attack || []).forEach(function (techId) {
                techniques.push({
                    techniqueID: techId,
                    score: (item.detection_rule_ids || []).length,
                    comment: item.title + ' (' + item.id + ')',
                    color: '',
                    enabled: true,
                });
            });
        });

        var layer = {
            name: 'FLAME Fraud Coverage',
            versions: { layer: '4.5', navigator: '4.9.1', attack: '14' },
            domain: 'enterprise-attack',
            description: 'FLAME fraud threat path coverage mapped to ATT&CK techniques',
            techniques: techniques,
            gradient: { colors: ['#ffffff', '#fbbf24', '#22c55e'], minValue: 0, maxValue: 5 },
        };

        var blob = new Blob([JSON.stringify(layer, null, 2)], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'flame-attack-navigator.json';
        a.click();
        URL.revokeObjectURL(url);
    }
```

---

### Task 16: Add Navigator Styles to style.css

**Files:**
- `style.css` — Modify

**Steps:**

1. Add navigator-specific styles (after the heat map styles section):

```css
/* ---------------------------------------------------------------
   Framework Navigator
   --------------------------------------------------------------- */
.modal-navigator {
    max-width: 95vw;
    max-height: 90vh;
}

.navigator-tabs {
    display: flex;
    gap: var(--space-sm);
    padding: 0 var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.nav-tab {
    background: none;
    border: none;
    color: var(--color-text-dim);
    padding: var(--space-sm) var(--space-md);
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    transition: color var(--duration), border-color var(--duration);
}

.nav-tab:hover { color: var(--color-text); }
.nav-tab.active {
    color: var(--color-accent);
    border-bottom-color: var(--color-accent);
}

.navigator-legend {
    display: flex;
    gap: var(--space-lg);
    padding: var(--space-sm) var(--space-lg);
    font-size: 0.8rem;
    color: var(--color-text-dim);
}

.nav-legend-item { display: flex; align-items: center; gap: 6px; }

.nav-legend-cell {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid var(--color-border);
}

.nav-cell-high, .nav-legend-cell.nav-cell-high { background: rgba(34, 197, 94, 0.5); }
.nav-cell-med, .nav-legend-cell.nav-cell-med { background: rgba(251, 191, 36, 0.4); }
.nav-cell-low, .nav-legend-cell.nav-cell-low { background: rgba(161, 161, 170, 0.2); }
.nav-cell-empty, .nav-legend-cell.nav-cell-empty { background: transparent; }

.navigator-body {
    overflow: auto;
    max-height: calc(90vh - 180px);
    padding: var(--space-md);
}

.navigator-grid {
    display: grid;
    gap: 1px;
    background: var(--color-border);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    overflow: hidden;
}

.nav-cell {
    background: var(--color-surface-1);
    padding: 4px 8px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 32px;
}

.nav-corner { background: var(--color-surface-2); }

.nav-col-header {
    background: var(--color-surface-2);
    font-weight: 600;
    color: var(--color-text);
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    min-height: 80px;
    font-size: 0.7rem;
    white-space: nowrap;
}

.nav-row-label {
    background: var(--color-surface-2);
    justify-content: flex-start;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.nav-tp-link {
    color: var(--color-text);
    text-decoration: none;
    font-size: 0.75rem;
}

.nav-tp-link:hover { color: var(--color-accent); }

.nav-data {
    cursor: pointer;
    transition: opacity var(--duration);
}

.nav-data:hover { opacity: 0.7; }

.navigator-actions {
    display: flex;
    gap: var(--space-sm);
    align-items: center;
}

.nav-export-btn {
    background: var(--color-surface-3);
    border: 1px solid var(--color-border);
    color: var(--color-text-dim);
    padding: 4px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    cursor: pointer;
    transition: background var(--duration), color var(--duration);
}

.nav-export-btn:hover {
    background: var(--color-accent);
    color: white;
}
```

2. Start local dev server, click Navigator button, verify:
   - CFPF tab shows 5 columns (P1-P5) x 33 rows
   - FT3 tab shows dynamic columns
   - Group-IB tab shows 10 columns
   - ATT&CK tab shows technique columns + JSON export button appears
   - Cell colors reflect detection rule coverage
   - Click a cell navigates to TP detail
   - SVG export downloads a file

**Commit:** `feat(frontend): add Framework Mapping Navigator with 4 framework views and export`

---

## Batch F: Rebuild + CI

### Task 17: Update CI Workflow

**Files:**
- `.github/workflows/build-and-deploy.yml` — Modify

**Steps:**

1. In the `build` job, add MISP and TAXII export steps after the existing Sigma export step (after line 86):

```yaml
      - name: Export MISP galaxy and feed
        run: python scripts/export_misp.py

      - name: Export static TAXII endpoints
        run: python scripts/export_taxii.py
```

2. Update the `git add` line (line 93) to include the new output directories:

```yaml
          git add -A database/ api/ data/ flame-stix-bundle.json flame-stats.json docs/ 2>/dev/null || true
```

   (This already includes `data/` and `api/`, so the new MISP galaxy files in `data/misp/` and TAXII files in `api/taxii/` will be picked up automatically.)

3. Update the paths trigger to include the new config directory:

```yaml
    paths:
      - 'ThreatPaths/**'
      - 'scripts/**'
      - 'tests/**'
      - 'Baselines/**'
      - 'DetectionLogic/**'
      - 'config/**'
```

**Commit:** `ci: add MISP and TAXII export steps to build workflow`

---

### Task 18: Full Rebuild and Verification

**Files:**
- No file changes -- verification only

**Steps:**

1. Run the full test suite:
   ```
   python -m pytest tests/ -v --tb=short
   ```
   All tests must pass.

2. Run the full build pipeline:
   ```
   python scripts/build_database.py
   python scripts/export_flame_stix.py
   python scripts/export_misp.py
   python scripts/export_taxii.py
   python scripts/export_sigma.py
   ```
   All scripts must exit 0.

3. Verify artifacts exist:
   - `database/flame_stix_bundle.json` -- contains `x-flame-fraud-scheme` objects
   - `data/misp/flame-galaxy.json` -- valid galaxy
   - `data/misp/flame-cluster.json` -- 33 cluster values
   - `database/misp-feed/manifest.json` -- 33 feed entries
   - `api/taxii/discovery.json` -- valid TAXII discovery
   - `api/taxii/default/collections.json` -- 3 collections
   - `database/flame-index.json` -- entries have `regulatory_refs` arrays

4. Start a local dev server and verify frontend:
   - TP detail views show regulatory badges
   - Navigator modal opens, shows 4 framework tabs
   - All existing features (heat map, assessment, graph) still work
   - No console errors

5. Run validation on all TPs:
   ```
   for f in ThreatPaths/TP-*.md; do python scripts/validate_submission.py "$f"; done
   ```

**Commit:** `chore: rebuild all artifacts for Phase 3 SIGNAL release`

---

## Summary

| Batch | Tasks | New Files | Modified Files | Estimated Effort |
|-------|-------|-----------|----------------|------------------|
| A | 1-6 | `docs/STIX-FRAUD-EXTENSION.md` | `scripts/export_flame_stix.py`, `tests/test_export_stix.py` | Large |
| B | 7 | `scripts/export_misp.py`, `tests/test_export_misp.py` | None | Medium |
| C | 8 | `scripts/export_taxii.py`, `tests/test_export_taxii.py` | None |  Medium |
| D | 9-13 | `config/regulatory_requirements.yaml` | `scripts/validate_submission.py`, `scripts/build_database.py`, 33 TP files, `Templates/threat-path-template.md`, `app.js`, `style.css`, `tests/test_validate_submission.py`, `tests/test_build_database.py` | Large |
| E | 14-16 | None | `index.html`, `app.js`, `style.css` | Medium |
| F | 17-18 | None | `.github/workflows/build-and-deploy.yml` | Small |

---

### Critical Files for Implementation
- `C:\Users\anon\Documents\anon\repos\flame-fraud\scripts\export_flame_stix.py` - Core STIX exporter to extend with 4 new SDO builders and 5 relationship types (Batch A critical path)
- `C:\Users\anon\Documents\anon\repos\flame-fraud\scripts\build_database.py` - Build pipeline requiring schema changes, regulatory_refs parsing, and JSON export updates (Batch D)
- `C:\Users\anon\Documents\anon\repos\flame-fraud\app.js` - Frontend application requiring renderNavigator() function and regulatory badges in renderDetailView() (Batches D and E)
- `C:\Users\anon\Documents\anon\repos\flame-fraud\scripts\validate_submission.py` - Validation script requiring regulatory_refs validation against config (Batch D)
- `C:\Users\anon\Documents\anon\repos\flame-fraud\.github\workflows\build-and-deploy.yml` - CI workflow requiring MISP and TAXII export step additions (Batch F)
