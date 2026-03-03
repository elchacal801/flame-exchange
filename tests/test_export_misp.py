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
