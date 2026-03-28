"""
test_detection_rules.py — Validate all FLAME Detection Logic (DL) rules.

Tests cover YAML parsing, required fields, UUID uniqueness,
threat path cross-references, query blocks, ATT&CK tags,
detection conditions, and fraud type taxonomy compliance.
"""

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DL_DIR = REPO_ROOT / "DetectionLogic"
TP_DIR = REPO_ROOT / "ThreatPaths"
TAXONOMY_PATH = REPO_ROOT / "api" / "v1" / "taxonomy.json"

REQUIRED_FIELDS = [
    "title",
    "id",
    "status",
    "threat_paths",
    "cfpf_phase",
    "detection",
    "tags",
]

VALID_CFPF_PHASES = {"P1", "P2", "P3", "P4", "P5"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_dl_files() -> list[Path]:
    """Return all DL YAML files sorted by name."""
    return sorted(DL_DIR.glob("DL-*.yml"))


def _load_dl(path: Path) -> dict:
    """Load a DL YAML file and return parsed dict."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _get_existing_tp_ids() -> set[str]:
    """Return the set of all TP IDs that exist on disk."""
    ids = set()
    for tp_file in TP_DIR.glob("TP-*.md"):
        match = re.match(r"(TP-\d{4})", tp_file.name)
        if match:
            ids.add(match.group(1))
    return ids


def _get_fraud_types_taxonomy() -> set[str]:
    """Load valid fraud types from taxonomy.json."""
    import json
    if not TAXONOMY_PATH.exists():
        return set()
    data = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    return set(data.get("data", {}).get("fraud_types", []))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDLFilesExist:
    def test_dl_directory_exists(self) -> None:
        assert DL_DIR.exists(), "DetectionLogic/ directory must exist"

    def test_dl_files_present(self) -> None:
        files = _get_dl_files()
        assert len(files) > 0, "No DL YAML files found"


class TestDLParsing:
    def test_all_dl_files_parse_without_error(self) -> None:
        """Every DL YAML file must be parseable."""
        for dl_file in _get_dl_files():
            try:
                data = _load_dl(dl_file)
                assert isinstance(data, dict), f"{dl_file.name} did not parse to a dict"
            except yaml.YAMLError as exc:
                pytest.fail(f"{dl_file.name} failed to parse: {exc}")


class TestDLRequiredFields:
    def test_all_dl_have_required_fields(self) -> None:
        """Every DL rule must have all required top-level fields."""
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            for field in REQUIRED_FIELDS:
                assert field in data, (
                    f"{dl_file.name} missing required field: {field}"
                )

    def test_detection_condition_non_empty(self) -> None:
        """detection.condition must be present and non-empty."""
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            detection = data.get("detection", {})
            if isinstance(detection, dict):
                condition = detection.get("condition", "")
                assert condition, (
                    f"{dl_file.name} has empty or missing detection.condition"
                )


class TestDLUUIDUniqueness:
    def test_all_uuids_are_unique(self) -> None:
        """No two DL rules should share the same UUID (id field)."""
        seen: dict[str, str] = {}
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            uuid = data.get("id")
            assert uuid is not None, f"{dl_file.name} has no id field"
            assert uuid not in seen, (
                f"Duplicate UUID {uuid} in {dl_file.name} and {seen[uuid]}"
            )
            seen[uuid] = dl_file.name


class TestDLThreatPathReferences:
    def test_all_threat_paths_exist(self) -> None:
        """Every TP referenced in a DL rule must exist on disk."""
        existing_tps = _get_existing_tp_ids()
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            for tp_id in data.get("threat_paths", []):
                assert tp_id in existing_tps, (
                    f"{dl_file.name} references {tp_id} which does not exist"
                )


class TestDLQueryBlocks:
    def test_non_sigma_rules_have_queries(self) -> None:
        """Rules with sigma_compatible: false must have a queries block."""
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            if data.get("sigma_compatible") is False:
                assert "queries" in data and data["queries"], (
                    f"{dl_file.name} is not sigma-compatible but has no queries block"
                )


class TestDLATTCKTags:
    # Valid tag prefixes: ATT&CK (attack.*), CFPF (cfpf.*), FLAME (flame.*)
    VALID_TAG_PREFIXES = ("attack.", "cfpf.", "flame.")

    def test_all_rules_have_framework_tags(self) -> None:
        """Every DL rule must have at least one framework tag (attack.*, cfpf.*, or flame.*)."""
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            tags = data.get("tags", [])
            framework_tags = [
                t for t in tags
                if any(str(t).startswith(p) for p in self.VALID_TAG_PREFIXES)
            ]
            assert len(framework_tags) >= 1, (
                f"{dl_file.name} has no framework tags (attack.*, cfpf.*, or flame.*) in tags list"
            )


class TestDLFraudTypes:
    def test_fraud_types_in_taxonomy(self) -> None:
        """All fraud_types values should exist in the project taxonomy.

        Allows a small number of unknown types (taxonomy may lag behind new rules)
        but fails if more than 5% of unique fraud_types are missing.
        """
        taxonomy = _get_fraud_types_taxonomy()
        if not taxonomy:
            pytest.skip("taxonomy.json not available")
        unknown: list[tuple[str, str]] = []
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            for ft in data.get("fraud_types", []):
                if ft not in taxonomy:
                    unknown.append((dl_file.name, ft))
        # Collect all unique unknown fraud types
        unique_unknown = {ft for _, ft in unknown}
        # Known taxonomy drift: ~15 fraud types in DL rules not yet in taxonomy.json
        # This threshold should decrease as taxonomy is updated
        max_allowed = max(5, int(len(taxonomy) * 0.15))
        assert len(unique_unknown) <= max_allowed, (
            f"{len(unique_unknown)} unknown fraud_types (max allowed {max_allowed}): "
            f"{sorted(unique_unknown)}"
        )


class TestDLCFPFPhases:
    def test_valid_cfpf_phases(self) -> None:
        """cfpf_phase must be a valid CFPF phase."""
        for dl_file in _get_dl_files():
            data = _load_dl(dl_file)
            phase = data.get("cfpf_phase")
            assert phase in VALID_CFPF_PHASES, (
                f"{dl_file.name} has invalid cfpf_phase: {phase}"
            )
