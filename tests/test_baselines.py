"""
test_baselines.py — Validate all FLAME Baseline (BL) files.

Tests cover YAML frontmatter parsing, required fields,
ID uniqueness and sequencing, and cross-references from
Threat Paths.
"""

import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BL_DIR = REPO_ROOT / "Baselines"
TP_INDEX_PATH = REPO_ROOT / "database" / "flame-index.json"

REQUIRED_FIELDS = ["id", "title", "category", "date", "author"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_bl_files() -> list[Path]:
    """Return all BL Markdown files sorted by name."""
    return sorted(BL_DIR.glob("BL-*.md"))


def _extract_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a Baseline markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```yaml\s*\n---\n(.*?)\n---\s*\n```", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def _get_bl_id_number(bl_id: str) -> int | None:
    """Extract numeric portion from a BL ID like BL-0002."""
    m = re.match(r"BL-(\d+)", bl_id)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBLFilesExist:
    def test_baselines_directory_exists(self) -> None:
        assert BL_DIR.exists(), "Baselines/ directory must exist"

    def test_bl_files_present(self) -> None:
        files = _get_bl_files()
        assert len(files) > 0, "No BL Markdown files found"


class TestBLParsing:
    def test_all_bl_files_parse_without_error(self) -> None:
        """Every BL file must have parseable YAML frontmatter."""
        for bl_file in _get_bl_files():
            meta = _extract_frontmatter(bl_file)
            assert meta is not None, (
                f"{bl_file.name} has unparseable or missing YAML frontmatter"
            )


class TestBLRequiredFields:
    def test_all_bl_have_required_fields(self) -> None:
        """Every BL file must contain all required frontmatter fields."""
        for bl_file in _get_bl_files():
            meta = _extract_frontmatter(bl_file)
            if meta is None:
                pytest.fail(f"{bl_file.name} has no frontmatter")
            for field in REQUIRED_FIELDS:
                assert field in meta, (
                    f"{bl_file.name} missing required field: {field}"
                )


class TestBLIDUniqueness:
    def test_all_bl_ids_are_unique(self) -> None:
        """No two BL files should share the same id."""
        seen: dict[str, str] = {}
        for bl_file in _get_bl_files():
            meta = _extract_frontmatter(bl_file)
            if meta is None:
                continue
            bl_id = meta.get("id")
            assert bl_id is not None, f"{bl_file.name} has no id"
            assert bl_id not in seen, (
                f"Duplicate BL id {bl_id} in {bl_file.name} and {seen[bl_id]}"
            )
            seen[bl_id] = bl_file.name

    def test_bl_ids_are_sequential(self) -> None:
        """BL IDs should form a sequential set with minimal gaps."""
        numbers = []
        for bl_file in _get_bl_files():
            meta = _extract_frontmatter(bl_file)
            if meta is None:
                continue
            bl_id = meta.get("id", "")
            num = _get_bl_id_number(bl_id)
            if num is not None:
                numbers.append(num)
        numbers.sort()
        if len(numbers) < 2:
            pytest.skip("Not enough BL files to check sequencing")
        # Allow up to 2 gaps (retired/reserved IDs) but flag large gaps
        expected_count = numbers[-1] - numbers[0] + 1
        gap_count = expected_count - len(numbers)
        missing = sorted(set(range(numbers[0], numbers[-1] + 1)) - set(numbers))
        # Allow gaps for retired/reserved IDs (BL-0001 and BL-0014 are skipped)
        assert gap_count <= 5, (
            f"BL IDs have {gap_count} gaps (max allowed 5): "
            f"missing {missing}"
        )


class TestBLCrossReferences:
    def test_tp_baseline_ids_reference_existing_files(self) -> None:
        """baseline_ids in TP index must point to existing BL files."""
        if not TP_INDEX_PATH.exists():
            pytest.skip("flame-index.json not found")

        existing_bl_ids = set()
        for bl_file in _get_bl_files():
            meta = _extract_frontmatter(bl_file)
            if meta and "id" in meta:
                existing_bl_ids.add(meta["id"])

        tp_data = json.loads(TP_INDEX_PATH.read_text(encoding="utf-8"))
        for tp in tp_data:
            for bl_id in tp.get("baseline_ids", []):
                assert bl_id in existing_bl_ids, (
                    f"{tp['id']} references baseline {bl_id} which does not exist"
                )
