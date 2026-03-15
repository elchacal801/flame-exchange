"""Tests for the FLAME MCP server data loader and tool logic."""

from __future__ import annotations

import json

import pytest

from mcp_server.data_loader import FlameDataLoader


@pytest.fixture
def loader() -> FlameDataLoader:
    return FlameDataLoader()


# -----------------------------------------------------------------------
# DataLoader — loading
# -----------------------------------------------------------------------

class TestDataLoaderLoading:
    def test_loads_threat_paths(self, loader: FlameDataLoader) -> None:
        assert len(loader.threat_paths) == 50

    def test_loads_detection_rules(self, loader: FlameDataLoader) -> None:
        assert len(loader.detection_rules) == 114

    def test_loads_stats(self, loader: FlameDataLoader) -> None:
        assert loader.stats["total"] == 50

    def test_loads_baselines(self, loader: FlameDataLoader) -> None:
        assert len(loader.baselines) == 26


# -----------------------------------------------------------------------
# DataLoader — get_threat_path
# -----------------------------------------------------------------------

class TestGetThreatPath:
    def test_get_existing_tp(self, loader: FlameDataLoader) -> None:
        tp = loader.get_threat_path("TP-0001")
        assert tp is not None
        assert tp["id"] == "TP-0001"
        assert "body" in tp

    def test_tp_has_expected_fields(self, loader: FlameDataLoader) -> None:
        tp = loader.get_threat_path("TP-0001")
        assert tp is not None
        assert "title" in tp
        assert "cfpf_phases" in tp
        assert "mitre_attack" in tp
        assert "fraud_types" in tp
        assert "sectors" in tp

    def test_get_nonexistent_tp(self, loader: FlameDataLoader) -> None:
        assert loader.get_threat_path("TP-9999") is None

    def test_get_tp_merges_index_and_content(self, loader: FlameDataLoader) -> None:
        tp = loader.get_threat_path("TP-0001")
        assert tp is not None
        # Body comes from content file
        assert "body" in tp
        # These come from the index
        assert "confidence_score" in tp


# -----------------------------------------------------------------------
# DataLoader — search_threat_paths
# -----------------------------------------------------------------------

class TestSearchThreatPaths:
    def test_search_by_sector(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(sector="banking")
        assert len(results) > 0
        for tp in results:
            assert "banking" in tp.get("sectors", [])

    def test_search_by_fraud_type(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(fraud_type="wire-fraud")
        assert len(results) > 0
        for tp in results:
            assert "wire-fraud" in tp.get("fraud_types", [])

    def test_search_by_query(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(query="wire")
        assert len(results) > 0

    def test_search_by_cfpf_phase(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(cfpf_phase="P1")
        assert len(results) > 0
        for tp in results:
            assert "P1" in tp.get("cfpf_phases", [])

    def test_search_no_filters_returns_all(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths()
        assert len(results) == 50

    def test_search_combined_filters(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(sector="banking", fraud_type="wire-fraud")
        assert len(results) > 0
        for tp in results:
            assert "banking" in tp.get("sectors", [])
            assert "wire-fraud" in tp.get("fraud_types", [])

    def test_search_no_match(self, loader: FlameDataLoader) -> None:
        results = loader.search_threat_paths(query="xyznonexistent")
        assert len(results) == 0

    def test_search_case_insensitive(self, loader: FlameDataLoader) -> None:
        upper = loader.search_threat_paths(query="WIRE")
        lower = loader.search_threat_paths(query="wire")
        assert len(upper) == len(lower)


# -----------------------------------------------------------------------
# DataLoader — get_detection_rules
# -----------------------------------------------------------------------

class TestGetDetectionRules:
    def test_get_all_rules(self, loader: FlameDataLoader) -> None:
        rules = loader.get_detection_rules()
        assert len(rules) == 114

    def test_filter_by_tp_id(self, loader: FlameDataLoader) -> None:
        rules = loader.get_detection_rules(tp_id="TP-0001")
        assert len(rules) > 0
        for rule in rules:
            assert "TP-0001" in rule.get("threat_path_ids", [])

    def test_filter_by_level(self, loader: FlameDataLoader) -> None:
        rules = loader.get_detection_rules(level="high")
        assert len(rules) > 0
        for rule in rules:
            assert rule["level"] == "high"

    def test_filter_by_fraud_type(self, loader: FlameDataLoader) -> None:
        rules = loader.get_detection_rules(fraud_type="wire-fraud")
        assert len(rules) > 0
        for rule in rules:
            assert "wire-fraud" in rule.get("fraud_types", [])

    def test_combined_filters(self, loader: FlameDataLoader) -> None:
        rules = loader.get_detection_rules(tp_id="TP-0001", level="high")
        assert len(rules) > 0
        for rule in rules:
            assert "TP-0001" in rule.get("threat_path_ids", [])
            assert rule["level"] == "high"


# -----------------------------------------------------------------------
# DataLoader — get_baseline
# -----------------------------------------------------------------------

class TestGetBaseline:
    def test_get_all_baselines(self, loader: FlameDataLoader) -> None:
        results = loader.get_baseline()
        assert len(results) == 26

    def test_get_by_id(self, loader: FlameDataLoader) -> None:
        results = loader.get_baseline(baseline_id="BASE-001")
        assert len(results) == 1
        assert results[0]["id"] == "BASE-001"

    def test_get_nonexistent_baseline(self, loader: FlameDataLoader) -> None:
        results = loader.get_baseline(baseline_id="NOPE-999")
        assert len(results) == 0


# -----------------------------------------------------------------------
# DataLoader — stats / coverage matrix
# -----------------------------------------------------------------------

class TestStatsAndCoverage:
    def test_get_stats(self, loader: FlameDataLoader) -> None:
        stats = loader.get_stats()
        assert stats["total"] == 50
        assert "phaseCoverage" in stats
        assert "coverageMatrix" in stats

    def test_get_coverage_matrix(self, loader: FlameDataLoader) -> None:
        matrix = loader.get_coverage_matrix()
        assert len(matrix) > 0
        first = matrix[0]
        assert "fraud_type" in first
        assert "phases" in first
        assert "total_tps" in first


# -----------------------------------------------------------------------
# Tool wrappers — test via the server module functions
# -----------------------------------------------------------------------

class TestToolFunctions:
    """Test the MCP tool functions directly (they return JSON strings)."""

    def test_search_threat_paths_tool(self, loader: FlameDataLoader) -> None:
        from mcp_server.server import search_threat_paths as stp

        result = json.loads(stp(query="wire"))
        assert isinstance(result, list)
        assert len(result) > 0
        # Check simplified fields
        first = result[0]
        assert "id" in first
        assert "title" in first
        assert "summary" in first
        assert "confidence_score" in first
        assert "cfpf_phases" in first
        assert "fraud_types" in first

    def test_get_threat_path_tool(self) -> None:
        from mcp_server.server import get_threat_path as gtp

        result = json.loads(gtp("TP-0001"))
        assert result["id"] == "TP-0001"
        assert "body" in result

    def test_get_threat_path_tool_not_found(self) -> None:
        from mcp_server.server import get_threat_path as gtp

        result = json.loads(gtp("TP-9999"))
        assert "error" in result

    def test_get_detection_rules_tool(self) -> None:
        from mcp_server.server import get_detection_rules as gdr

        result = json.loads(gdr(tp_id="TP-0001"))
        assert isinstance(result, list)
        assert len(result) > 0

    def test_map_framework_cfpf(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "cfpf"))
        assert result["tp_id"] == "TP-0001"
        assert result["framework"] == "cfpf"
        assert "phases" in result
        assert "P1" in result["phases"]

    def test_map_framework_mitre(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "mitre"))
        assert "techniques" in result
        assert len(result["techniques"]) > 0

    def test_map_framework_groupib(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "groupib"))
        assert "stages" in result

    def test_map_framework_ft3(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "ft3"))
        assert "tactics" in result

    def test_map_framework_ucff(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "ucff"))
        assert "domains" in result

    def test_map_framework_unknown(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-0001", "nope"))
        assert "error" in result

    def test_map_framework_tp_not_found(self) -> None:
        from mcp_server.server import map_framework

        result = json.loads(map_framework("TP-9999", "cfpf"))
        assert "error" in result

    def test_assess_coverage_tool(self) -> None:
        from mcp_server.server import assess_coverage

        result = json.loads(
            assess_coverage(["banking"], ["account-takeover", "wire-fraud"])
        )
        assert result["sectors"] == ["banking"]
        assert result["total_matching_tps"] > 0
        assert "coverage_score" in result
        assert "coverage_by_fraud_type" in result
        assert "phase_weakness" in result
        assert "recommended_detection_rules" in result

    def test_assess_coverage_empty(self) -> None:
        from mcp_server.server import assess_coverage

        result = json.loads(
            assess_coverage(["nonexistent-sector"], ["nonexistent-type"])
        )
        assert result["total_matching_tps"] == 0

    def test_get_baseline_tool(self) -> None:
        from mcp_server.server import get_baseline

        result = json.loads(get_baseline(baseline_id="BASE-001"))
        assert isinstance(result, list)
        assert len(result) == 1

    def test_look_left_right_tool(self) -> None:
        from mcp_server.server import look_left_right

        result = json.loads(look_left_right("TP-0001"))
        assert result["tp_id"] == "TP-0001"
        assert "look_left" in result
        assert "look_right" in result
        assert "lateral" in result
        assert "description" in result["look_left"]
        assert "threat_paths" in result["look_left"]

    def test_look_left_right_not_found(self) -> None:
        from mcp_server.server import look_left_right

        result = json.loads(look_left_right("TP-9999"))
        assert "error" in result

    def test_look_left_right_has_relationships(self) -> None:
        from mcp_server.server import look_left_right

        result = json.loads(look_left_right("TP-0001"))
        # TP-0001 has related_tps so at least one category should be non-empty
        all_rels = (
            result["look_left"]["threat_paths"]
            + result["look_right"]["threat_paths"]
            + result["lateral"]["threat_paths"]
        )
        assert len(all_rels) > 0
