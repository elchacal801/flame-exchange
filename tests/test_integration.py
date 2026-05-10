"""
test_integration.py — End-to-end integration tests for FLAME.

Tests cover build output validation, API JSON file integrity,
and structural checks on all generated JSON artifacts.
"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = REPO_ROOT / "database"
API_V1_DIR = REPO_ROOT / "api" / "v1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> dict | list:
    """Load and return parsed JSON from a file."""
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# flame-index.json (build_database.py output)
# ---------------------------------------------------------------------------

class TestFlameIndex:
    INDEX_PATH = DATABASE_DIR / "flame-index.json"

    def test_flame_index_exists(self) -> None:
        assert self.INDEX_PATH.exists(), "database/flame-index.json must exist"

    def test_flame_index_is_valid_json(self) -> None:
        data = _load_json(self.INDEX_PATH)
        assert isinstance(data, list), "flame-index.json should be a list"

    def test_flame_index_has_entries(self) -> None:
        data = _load_json(self.INDEX_PATH)
        assert len(data) > 0, "flame-index.json should not be empty"

    def test_tp_json_entries_have_expected_fields(self) -> None:
        """Every TP entry must have the core fields."""
        required_fields = [
            "id", "title", "sectors", "fraud_types",
            "baseline_ids",
        ]
        data = _load_json(self.INDEX_PATH)
        for tp in data:
            for field in required_fields:
                assert field in tp, (
                    f"{tp.get('id', 'UNKNOWN')} missing field: {field}"
                )


# ---------------------------------------------------------------------------
# API v1 JSON files
# ---------------------------------------------------------------------------

class TestAPIV1JSON:
    EXPECTED_FILES = [
        "threat-paths.json",
        "taxonomy.json",
        "stats.json",
        "baselines.json",
        "coverage-matrix.json",
    ]

    def test_api_v1_directory_exists(self) -> None:
        assert API_V1_DIR.exists(), "api/v1/ directory must exist"

    def test_expected_api_files_exist(self) -> None:
        for filename in self.EXPECTED_FILES:
            path = API_V1_DIR / filename
            assert path.exists(), f"api/v1/{filename} must exist"

    def test_all_api_files_are_valid_json(self) -> None:
        """Every JSON file in api/v1/ must parse without error."""
        for json_file in API_V1_DIR.glob("*.json"):
            try:
                _load_json(json_file)
            except json.JSONDecodeError as exc:
                pytest.fail(f"{json_file.name} is invalid JSON: {exc}")

    def test_individual_tp_json_files_valid(self) -> None:
        """All TP-XXXX.json files in api/v1/threat-paths/ must be valid JSON."""
        tp_json_dir = API_V1_DIR / "threat-paths"
        if not tp_json_dir.exists():
            pytest.skip("api/v1/threat-paths/ not found")
        for tp_file in sorted(tp_json_dir.glob("TP-*.json")):
            try:
                data = _load_json(tp_file)
                assert isinstance(data, dict), f"{tp_file.name} is not a JSON object"
                # Individual TP files are wrapped in {meta, data}
                if "data" in data:
                    inner = data["data"]
                else:
                    inner = data
                assert "id" in inner, (
                    f"{tp_file.name} missing 'id' field in data envelope"
                )
            except json.JSONDecodeError as exc:
                pytest.fail(f"{tp_file.name} is invalid JSON: {exc}")



# ---------------------------------------------------------------------------
# Search index
# ---------------------------------------------------------------------------

class TestSearchIndex:
    SEARCH_INDEX_PATH = DATABASE_DIR / "flame-search-index.json"

    def test_search_index_exists(self) -> None:
        assert self.SEARCH_INDEX_PATH.exists(), "flame-search-index.json must exist"

    def test_search_index_is_valid_json(self) -> None:
        data = _load_json(self.SEARCH_INDEX_PATH)
        assert isinstance(data, list), "flame-search-index.json should be a list"

    def test_search_index_has_entries_for_all_tps(self) -> None:
        """Search index should have at least one entry per TP."""
        index_path = DATABASE_DIR / "flame-index.json"
        if not index_path.exists():
            pytest.skip("flame-index.json not found")

        tp_data = _load_json(index_path)
        tp_ids = {tp["id"] for tp in tp_data}

        search_data = _load_json(self.SEARCH_INDEX_PATH)
        search_ids = set()
        for entry in search_data:
            entry_id = entry.get("id", "")
            if entry_id.startswith("TP-"):
                search_ids.add(entry_id)

        missing = tp_ids - search_ids
        assert len(missing) == 0, (
            f"TPs missing from search index: {sorted(missing)}"
        )


# ---------------------------------------------------------------------------
# Threat-paths.json structure
# ---------------------------------------------------------------------------

class TestThreatPathsJSON:
    TP_PATH = API_V1_DIR / "threat-paths.json"

    def test_threat_paths_json_exists(self) -> None:
        assert self.TP_PATH.exists()

    def test_threat_paths_has_meta_and_data(self) -> None:
        data = _load_json(self.TP_PATH)
        assert "meta" in data, "threat-paths.json must have 'meta' key"
        assert "data" in data, "threat-paths.json must have 'data' key"

    def test_threat_paths_count_matches_index(self) -> None:
        """threat-paths.json data count should match flame-index.json."""
        index_path = DATABASE_DIR / "flame-index.json"
        if not index_path.exists():
            pytest.skip("flame-index.json not found")
        tp_json = _load_json(self.TP_PATH)
        index_data = _load_json(index_path)
        assert len(tp_json["data"]) == len(index_data), (
            f"threat-paths.json has {len(tp_json['data'])} entries but "
            f"flame-index.json has {len(index_data)}"
        )
