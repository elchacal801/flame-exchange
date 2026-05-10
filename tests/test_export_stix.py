"""
test_export_stix.py — Tests for FLAME export_flame_stix.py

Tests detection rule extraction, section parsing, phase mapping,
and deterministic ID generation.
"""

from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_flame_stix import (
    map_cfpf_phases,
    deterministic_id,
    build_relationship,
    build_fraud_scheme,
    build_financial_transaction,
    build_mule_network,
    build_fraud_actor_profile,
)


# ---------------------------------------------------------------------------
# map_cfpf_phases tests
# ---------------------------------------------------------------------------

class TestMapCfpfPhases:
    def test_all_phases(self):
        phases = map_cfpf_phases(["P1", "P2", "P3", "P4", "P5"])
        assert len(phases) == 5
        assert phases[0] == {"kill_chain_name": "cfpf", "phase_name": "P1-reconnaissance"}
        assert phases[4] == {"kill_chain_name": "cfpf", "phase_name": "P5-monetization"}

    def test_partial_phases(self):
        phases = map_cfpf_phases(["P2", "P4"])
        assert len(phases) == 2
        assert phases[0]["phase_name"] == "P2-initial-access"
        assert phases[1]["phase_name"] == "P4-execution"

    def test_invalid_phase_skipped(self):
        phases = map_cfpf_phases(["P1", "P99", "P5"])
        assert len(phases) == 2

    def test_empty_phases(self):
        phases = map_cfpf_phases([])
        assert phases == []


# ---------------------------------------------------------------------------
# deterministic_id tests
# ---------------------------------------------------------------------------

class TestDeterministicId:
    def test_idempotent(self):
        """Same inputs should produce same output."""
        id1 = deterministic_id("attack-pattern", "flame-TP-0001")
        id2 = deterministic_id("attack-pattern", "flame-TP-0001")
        assert id1 == id2

    def test_different_seeds_different_ids(self):
        id1 = deterministic_id("attack-pattern", "flame-TP-0001")
        id2 = deterministic_id("attack-pattern", "flame-TP-0002")
        assert id1 != id2

    def test_format(self):
        result = deterministic_id("attack-pattern", "test-seed")
        assert result.startswith("attack-pattern--")
        # UUID format: 8-4-4-4-12 hex chars
        uuid_part = result.split("--")[1]
        assert len(uuid_part) == 36


# ---------------------------------------------------------------------------
# build_fraud_scheme tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# build_financial_transaction tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# build_mule_network tests
# ---------------------------------------------------------------------------

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
        content = {"body": "Basic phishing scheme with no special involvement."}
        result = build_mule_network(tp, content)
        assert result is None


# ---------------------------------------------------------------------------
# build_fraud_actor_profile tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# New relationship types tests
# ---------------------------------------------------------------------------

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
