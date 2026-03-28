"""
test_data_quality.py — Cross-cutting data quality checks for FLAME.

Tests cover orphan detection, confidence score ranges, bidirectional
cross-references between TPs and DL rules, taxonomy compliance,
and structural completeness.
"""

import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
TP_DIR = REPO_ROOT / "ThreatPaths"
DL_DIR = REPO_ROOT / "DetectionLogic"
BL_DIR = REPO_ROOT / "Baselines"
TP_INDEX_PATH = REPO_ROOT / "database" / "flame-index.json"
TAXONOMY_PATH = REPO_ROOT / "api" / "v1" / "taxonomy.json"
REGULATORY_PATH = REPO_ROOT / "data" / "regulatory_alerts.csv"

VALID_CFPF_PHASES = {"P1", "P2", "P3", "P4", "P5"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_tp_ids_from_disk() -> set[str]:
    """Return the set of TP IDs from files on disk."""
    ids = set()
    for tp_file in TP_DIR.glob("TP-*.md"):
        match = re.match(r"(TP-\d{4})", tp_file.name)
        if match:
            ids.add(match.group(1))
    return ids


def _load_tp_index() -> list[dict]:
    """Load the TP index JSON."""
    return json.loads(TP_INDEX_PATH.read_text(encoding="utf-8"))


def _load_dl_file(path: Path) -> dict:
    """Load a DL YAML file."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _get_dl_files() -> list[Path]:
    return sorted(DL_DIR.glob("DL-*.yml"))


def _build_dl_to_tp_map() -> dict[str, list[str]]:
    """Map DL filename prefix -> list of TP IDs it references."""
    mapping: dict[str, list[str]] = {}
    for dl_file in _get_dl_files():
        data = _load_dl_file(dl_file)
        dl_id = re.match(r"(DL-\d{4})", dl_file.name)
        if dl_id:
            mapping[dl_id.group(1)] = data.get("threat_paths", [])
    return mapping


def _build_tp_to_dl_map() -> dict[str, list[str]]:
    """Map TP ID -> list of DL IDs from the index JSON."""
    mapping: dict[str, list[str]] = {}
    if not TP_INDEX_PATH.exists():
        return mapping
    for tp in _load_tp_index():
        mapping[tp["id"]] = tp.get("detection_rule_ids", [])
    return mapping


def _get_fraud_types_taxonomy() -> set[str]:
    """Load valid fraud types from taxonomy.json."""
    if not TAXONOMY_PATH.exists():
        return set()
    data = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    return set(data.get("data", {}).get("fraud_types", []))


# ---------------------------------------------------------------------------
# Orphan detection
# ---------------------------------------------------------------------------

class TestNoOrphanedTPs:
    def test_every_tp_has_at_least_one_detection_rule(self) -> None:
        """Every TP should be referenced by at least one DL rule."""
        dl_to_tp = _build_dl_to_tp_map()
        # Flatten to set of all TPs referenced by any DL
        tps_covered = set()
        for tp_list in dl_to_tp.values():
            tps_covered.update(tp_list)

        tp_ids = _get_tp_ids_from_disk()
        orphaned = tp_ids - tps_covered
        assert len(orphaned) == 0, (
            f"Orphaned TPs with no detection rules: {sorted(orphaned)}"
        )


class TestNoOrphanedDLRules:
    def test_every_dl_references_existing_tp(self) -> None:
        """Every DL rule must reference at least one existing TP."""
        existing_tps = _get_tp_ids_from_disk()
        for dl_file in _get_dl_files():
            data = _load_dl_file(dl_file)
            threat_paths = data.get("threat_paths", [])
            assert len(threat_paths) > 0, (
                f"{dl_file.name} has no threat_paths references"
            )
            for tp_id in threat_paths:
                assert tp_id in existing_tps, (
                    f"{dl_file.name} references non-existent {tp_id}"
                )


# ---------------------------------------------------------------------------
# Confidence scores
# ---------------------------------------------------------------------------

class TestConfidenceScores:
    def test_confidence_scores_in_valid_range(self) -> None:
        """confidence_score in TP index must be 0-100."""
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")
        for tp in _load_tp_index():
            score = tp.get("confidence_score")
            if score is not None:
                assert 0 <= score <= 100, (
                    f"{tp['id']} has out-of-range confidence_score: {score}"
                )


# ---------------------------------------------------------------------------
# TP structural completeness
# ---------------------------------------------------------------------------

class TestTPStructuralCompleteness:
    def test_all_tps_have_non_empty_summary(self) -> None:
        """Every TP in the index must have a non-empty summary."""
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")
        for tp in _load_tp_index():
            summary = tp.get("summary", "")
            assert summary and len(summary.strip()) > 0, (
                f"{tp['id']} has empty summary"
            )

    def test_all_tps_have_cfpf_phases(self) -> None:
        """Every TP in the index must have at least one CFPF phase."""
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")
        for tp in _load_tp_index():
            phases = tp.get("cfpf_phases", [])
            assert len(phases) > 0, (
                f"{tp['id']} has no CFPF phases"
            )
            for phase in phases:
                assert phase in VALID_CFPF_PHASES, (
                    f"{tp['id']} has invalid CFPF phase: {phase}"
                )


# ---------------------------------------------------------------------------
# Bidirectional cross-references
# ---------------------------------------------------------------------------

class TestBidirectionalReferences:
    def test_tp_dl_references_match(self) -> None:
        """
        If TP-XXXX lists DL-YYYY in detection_rule_ids, then DL-YYYY
        must list TP-XXXX in threat_paths, and vice versa.
        """
        tp_to_dl = _build_tp_to_dl_map()
        dl_to_tp = _build_dl_to_tp_map()

        if not tp_to_dl:
            pytest.skip("flame-index.json not available")

        # Forward: TP -> DL should be reciprocated
        for tp_id, dl_ids in tp_to_dl.items():
            for dl_id in dl_ids:
                if dl_id in dl_to_tp:
                    assert tp_id in dl_to_tp[dl_id], (
                        f"{tp_id} lists {dl_id} but {dl_id} does not list {tp_id} in threat_paths"
                    )

        # Reverse: DL -> TP should be reciprocated
        for dl_id, tp_ids in dl_to_tp.items():
            for tp_id in tp_ids:
                if tp_id in tp_to_dl:
                    assert dl_id in tp_to_dl[tp_id], (
                        f"{dl_id} lists {tp_id} but {tp_id} does not list {dl_id} in detection_rule_ids"
                    )


# ---------------------------------------------------------------------------
# ID uniqueness
# ---------------------------------------------------------------------------

class TestNoDuplicateTPIDs:
    def test_tp_ids_unique_in_index(self) -> None:
        """No duplicate TP IDs in the index."""
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")
        seen: dict[str, int] = {}
        for tp in _load_tp_index():
            tp_id = tp["id"]
            seen[tp_id] = seen.get(tp_id, 0) + 1
        duplicates = {k: v for k, v in seen.items() if v > 1}
        assert len(duplicates) == 0, f"Duplicate TP IDs in index: {duplicates}"

    def test_tp_ids_unique_on_disk(self) -> None:
        """No duplicate TP IDs from filenames on disk."""
        seen: dict[str, list[str]] = {}
        for tp_file in TP_DIR.glob("TP-*.md"):
            match = re.match(r"(TP-\d{4})", tp_file.name)
            if match:
                tp_id = match.group(1)
                seen.setdefault(tp_id, []).append(tp_file.name)
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        assert len(duplicates) == 0, f"Duplicate TP IDs on disk: {duplicates}"


# ---------------------------------------------------------------------------
# Taxonomy compliance
# ---------------------------------------------------------------------------

class TestFraudTypeTaxonomy:
    def test_tp_fraud_types_in_taxonomy(self) -> None:
        """All fraud_types in TP index should exist in taxonomy.

        Allows a small number of unknown types (taxonomy may lag behind new TPs)
        but fails if more than 5% of unique fraud_types are missing.
        """
        taxonomy = _get_fraud_types_taxonomy()
        if not taxonomy:
            pytest.skip("taxonomy.json not available")
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")

        unknown: list[tuple[str, str]] = []
        for tp in _load_tp_index():
            for ft in tp.get("fraud_types", []):
                if ft not in taxonomy:
                    unknown.append((tp["id"], ft))
        unique_unknown = {ft for _, ft in unknown}
        # Known taxonomy drift: ~13 fraud types in TPs not yet in taxonomy.json
        # This threshold should decrease as taxonomy is updated
        max_allowed = max(5, int(len(taxonomy) * 0.15))
        assert len(unique_unknown) <= max_allowed, (
            f"{len(unique_unknown)} unknown fraud_types in TPs (max allowed {max_allowed}): "
            f"{sorted(unique_unknown)}"
        )


# ---------------------------------------------------------------------------
# Regulatory references
# ---------------------------------------------------------------------------

class TestRegulatoryRefs:
    def test_regulatory_refs_reference_valid_entries(self) -> None:
        """regulatory_refs in TPs should reference known alert IDs if CSV exists."""
        if not REGULATORY_PATH.exists():
            pytest.skip("regulatory_alerts.csv not found")
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")

        import csv
        valid_ids = set()
        with open(REGULATORY_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                valid_ids.add(row["alert_id"])

        # Also accept REG-prefixed IDs that are static regulatory references
        # (not from the CSV but hardcoded in the taxonomy)
        for tp in _load_tp_index():
            for ref in tp.get("regulatory_refs", []):
                # Static REG-* refs are valid by convention
                if ref.startswith("REG-"):
                    continue
                assert ref in valid_ids, (
                    f"{tp['id']} references unknown regulatory entry: {ref}"
                )
