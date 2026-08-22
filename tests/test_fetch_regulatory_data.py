"""
test_fetch_regulatory_data.py -- Tests for the CLI orchestration script.

Covers: SOURCE_REGISTRY completeness, collect_alerts with mock/empty sources,
write_csv output correctness, and write_csv with empty alerts list.
"""

import csv
import sys
from datetime import date
from pathlib import Path
from typing import List
from unittest.mock import MagicMock

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from regulatory.models import RegulatoryAlert, CSV_COLUMNS
from regulatory.base import RegulatorySource

# Import the module under test
from fetch_regulatory_data import (
    SOURCE_REGISTRY,
    collect_alerts,
    load_existing_alerts,
    write_csv,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _MockSource(RegulatorySource):
    """A mock source that returns predetermined alerts without network I/O."""

    name = "mock"

    def __init__(self, alerts: List[RegulatoryAlert]):
        # Bypass parent __init__ which requires a config dict --
        # we just need .run() to work.
        self._alerts = alerts

    def fetch(self) -> str:
        return ""

    def parse(self, raw: str) -> List[RegulatoryAlert]:
        return self._alerts

    def run(self) -> List[RegulatoryAlert]:
        return self._alerts


class _EmptySource(RegulatorySource):
    """A source that succeeds with zero alerts (empty is NOT failure)."""

    name = "empty"

    def __init__(self):
        self._id_seen = {}

    def fetch(self) -> str:
        return ""

    def parse(self, raw: str) -> List[RegulatoryAlert]:
        return []


class _FailingSource(RegulatorySource):
    """A source whose fetch raises -- run() must report failure, not []."""

    name = "failing"

    def __init__(self):
        self._id_seen = {}

    def fetch(self) -> str:
        raise RuntimeError("simulated failure")

    def parse(self, raw: str) -> List[RegulatoryAlert]:
        return []


def _make_alert(**overrides) -> RegulatoryAlert:
    """Helper to create a RegulatoryAlert with sensible defaults."""
    defaults = dict(
        source="test",
        alert_id="T-001",
        title="Test Alert",
        date=date(2026, 2, 1),
        category="test-cat",
        mapped_tp_ids=["TP-0001"],
        url="https://example.com/alert",
        severity="high",
        summary="A test alert summary.",
    )
    defaults.update(overrides)
    return RegulatoryAlert(**defaults)


# ---------------------------------------------------------------------------
# SOURCE_REGISTRY tests
# ---------------------------------------------------------------------------

class TestSourceRegistry:
    def test_registry_has_all_six_sources(self):
        """SOURCE_REGISTRY should contain exactly the 6 expected source keys."""
        expected_keys = {"cfpb", "occ", "sec", "ofac", "fincen", "fbi_ic3"}
        assert set(SOURCE_REGISTRY.keys()) == expected_keys

    def test_registry_values_are_subclasses_of_regulatory_source(self):
        """Every registry value should be a subclass of RegulatorySource."""
        for name, cls in SOURCE_REGISTRY.items():
            assert issubclass(cls, RegulatorySource), (
                f"{name} -> {cls} is not a RegulatorySource subclass"
            )

    def test_registry_has_six_entries(self):
        """Registry should have exactly 6 entries."""
        assert len(SOURCE_REGISTRY) == 6


# ---------------------------------------------------------------------------
# collect_alerts tests
# ---------------------------------------------------------------------------

class TestCollectAlerts:
    def test_collect_alerts_merges_results(self):
        """collect_alerts should merge alerts from multiple sources."""
        alert_a = _make_alert(source="src_a", alert_id="A-001")
        alert_b = _make_alert(source="src_b", alert_id="B-001")
        alert_c = _make_alert(source="src_b", alert_id="B-002")

        sources = {
            "src_a": _MockSource([alert_a]),
            "src_b": _MockSource([alert_b, alert_c]),
        }

        result, failed = collect_alerts(sources)
        assert len(result) == 3
        assert failed == []
        ids = {a.alert_id for a in result}
        assert ids == {"A-001", "B-001", "B-002"}

    def test_collect_alerts_empty_source_is_not_failure(self):
        """A source that succeeds with zero alerts is not reported failed."""
        alert = _make_alert(source="good", alert_id="G-001")
        sources = {
            "good": _MockSource([alert]),
            "empty": _EmptySource(),
        }

        result, failed = collect_alerts(sources)
        assert len(result) == 1
        assert failed == []
        assert result[0].alert_id == "G-001"

    def test_collect_alerts_reports_failed_sources(self):
        """A raising source is reported by name, others still collected."""
        alert = _make_alert(source="good", alert_id="G-001")
        sources = {
            "good": _MockSource([alert]),
            "failing": _FailingSource(),
        }

        result, failed = collect_alerts(sources)
        assert len(result) == 1
        assert failed == ["failing"]

    def test_collect_alerts_empty_sources_dict(self):
        """An empty sources dict should return an empty list, no failures."""
        result, failed = collect_alerts({})
        assert result == []
        assert failed == []


# ---------------------------------------------------------------------------
# write_csv tests
# ---------------------------------------------------------------------------

class TestWriteCsv:
    def test_write_csv_produces_valid_csv(self, tmp_path):
        """write_csv should produce a valid CSV file with correct columns."""
        alerts = [
            _make_alert(
                source="fincen",
                alert_id="FIN-001",
                title="Advisory",
                date=date(2026, 2, 15),
                category="money-laundering",
                mapped_tp_ids=["TP-0001", "TP-0003"],
                url="https://fincen.gov/advisory/001",
                severity="high",
                summary="Advisory on AML.",
            ),
            _make_alert(
                source="cfpb",
                alert_id="CFPB-001",
                title="Complaint Alert",
                date=date(2026, 1, 10),
                category="elder-fraud",
                mapped_tp_ids=["TP-0005"],
                url="https://cfpb.gov/alert/001",
                severity="medium",
                summary="Elder fraud alert.",
            ),
        ]

        output = tmp_path / "output.csv"
        write_csv(alerts, output)

        assert output.exists()

        with open(output, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames == CSV_COLUMNS

            rows = list(reader)
            assert len(rows) == 2

            # Check first row
            assert rows[0]["source"] == "fincen"
            assert rows[0]["alert_id"] == "FIN-001"
            assert rows[0]["title"] == "Advisory"
            assert rows[0]["date"] == "2026-02-15"
            assert rows[0]["category"] == "money-laundering"
            assert rows[0]["mapped_tp_ids"] == "TP-0001|TP-0003"
            assert rows[0]["url"] == "https://fincen.gov/advisory/001"
            assert rows[0]["severity"] == "high"
            assert rows[0]["summary"] == "Advisory on AML."

            # Check second row
            assert rows[1]["source"] == "cfpb"
            assert rows[1]["mapped_tp_ids"] == "TP-0005"

    def test_write_csv_empty_alerts_writes_header_only(self, tmp_path):
        """write_csv with empty list should still write CSV header."""
        output = tmp_path / "empty.csv"
        write_csv([], output)

        assert output.exists()

        with open(output, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames == CSV_COLUMNS
            rows = list(reader)
            assert len(rows) == 0

    def test_write_csv_creates_parent_directories(self, tmp_path):
        """write_csv should create parent directories if they don't exist."""
        output = tmp_path / "nested" / "deep" / "output.csv"
        write_csv([], output)

        assert output.exists()
        assert output.parent.exists()

    def test_write_csv_mapped_tp_ids_serialization(self, tmp_path):
        """mapped_tp_ids should be pipe-delimited; empty list should be empty string."""
        alerts = [
            _make_alert(mapped_tp_ids=["TP-0001", "TP-0002", "TP-0003"]),
            _make_alert(alert_id="T-002", mapped_tp_ids=[]),
        ]
        output = tmp_path / "tp_test.csv"
        write_csv(alerts, output)

        with open(output, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            assert rows[0]["mapped_tp_ids"] == "TP-0001|TP-0002|TP-0003"
            assert rows[1]["mapped_tp_ids"] == ""

    def test_write_csv_date_serialization(self, tmp_path):
        """date fields should be serialized as ISO format strings."""
        alerts = [
            _make_alert(date=date(2026, 3, 15)),
            _make_alert(alert_id="T-002", date="January 2026"),
        ]
        output = tmp_path / "date_test.csv"
        write_csv(alerts, output)

        with open(output, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            assert rows[0]["date"] == "2026-03-15"
            assert rows[1]["date"] == "January 2026"


# ---------------------------------------------------------------------------
# Failure-preservation and stable-id tests
# ---------------------------------------------------------------------------

class TestLoadExistingAlerts:
    def test_carries_forward_failed_source_rows(self, tmp_path):
        """Rows from a failed source survive a rewrite via carry-forward."""
        csv_path = tmp_path / "alerts.csv"
        old_rows = [
            _make_alert(source="occ", alert_id="occ-aaaa"),
            _make_alert(source="sec", alert_id="sec-bbbb"),
        ]
        write_csv(old_rows, csv_path)

        carried = load_existing_alerts(csv_path, ["occ"])
        assert len(carried) == 1
        assert carried[0].source == "occ"
        assert carried[0].alert_id == "occ-aaaa"

    def test_missing_file_returns_empty(self, tmp_path):
        assert load_existing_alerts(tmp_path / "nope.csv", ["occ"]) == []

    def test_no_failed_sources_returns_empty(self, tmp_path):
        csv_path = tmp_path / "alerts.csv"
        write_csv([_make_alert(source="occ", alert_id="occ-aaaa")], csv_path)
        assert load_existing_alerts(csv_path, []) == []

    def test_round_trips_mapped_tp_ids(self, tmp_path):
        csv_path = tmp_path / "alerts.csv"
        write_csv(
            [_make_alert(source="occ", alert_id="occ-aaaa",
                         mapped_tp_ids=["TP-0001", "TP-0060"])],
            csv_path,
        )
        carried = load_existing_alerts(csv_path, ["occ"])
        assert carried[0].mapped_tp_ids == ["TP-0001", "TP-0060"]


class TestStableIds:
    def _source(self):
        class _S(RegulatorySource):
            name = "stub"

            def __init__(self):
                self._id_seen = {}

            def fetch(self):
                return ""

            def parse(self, raw):
                return []

        return _S()

    def test_same_input_same_id(self):
        a = self._source()
        b = self._source()
        id_a = a._stable_id("https://x/1.html", "Title", "2026-01-01")
        id_b = b._stable_id("https://x/1.html", "Title", "2026-01-01")
        assert id_a == id_b
        assert id_a.startswith("stub-")

    def test_different_input_different_id(self):
        s = self._source()
        assert (s._stable_id("https://x/1.html", "T", "2026-01-01")
                != s._stable_id("https://x/2.html", "T", "2026-01-01"))

    def test_duplicate_rows_get_suffix(self):
        s = self._source()
        first = s._stable_id("https://x/1.html", "T", "2026-01-01")
        second = s._stable_id("https://x/1.html", "T", "2026-01-01")
        assert second == first + "-1"

    def test_run_resets_duplicate_counter(self):
        s = self._source()
        first = s._stable_id("https://x/1.html", "T", "2026-01-01")
        s.run()
        again = s._stable_id("https://x/1.html", "T", "2026-01-01")
        assert again == first


class TestFailureSemantics:
    def test_run_returns_none_on_fetch_exception(self):
        src = _FailingSource()
        assert src.run() is None

    def test_run_returns_list_on_success(self):
        src = _EmptySource()
        assert src.run() == []
