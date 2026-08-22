"""
test_regulatory_dates.py --- Tests for shared date normalization at ingest.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from regulatory.dates import normalize_date_to_iso
from regulatory.models import RegulatoryAlert


class TestNormalizeDateToIso:
    @pytest.mark.parametrize("raw,expected", [
        # already ISO
        ("2026-01-15", "2026-01-15"),
        # ISO timestamps (CFPB API) -- previously fell through untouched
        ("2026-08-21T01:49:20.000Z", "2026-08-21"),
        ("2026-03-25T12:00:00-05:00", "2026-03-25"),
        # US slash (OFAC, FinCEN, OCC year-index)
        ("08/20/2026", "2026-08-20"),
        ("3/5/2026", "2026-03-05"),
        # abbreviated month with period (SEC)
        ("Aug. 21, 2026", "2026-08-21"),
        ("Sept. 30, 2025", "2025-09-30"),
        # informal full month
        ("January 6, 2026", "2026-01-06"),
        # RFC 2822 with and without time (FBI IC3)
        ("Wed, 14 Jan 2026", "2026-01-14"),
        ("Wed, 29 Jul 2026 12:00:00 GMT", "2026-07-29"),
    ])
    def test_known_formats(self, raw, expected):
        assert normalize_date_to_iso(raw) == expected

    @pytest.mark.parametrize("raw", ["", "January 2026", "unknown", "Q1 2026"])
    def test_unparseable_passthrough(self, raw):
        assert normalize_date_to_iso(raw) == raw


class TestCsvRowNormalization:
    def _alert(self, raw_date):
        return RegulatoryAlert(
            source="test", alert_id="test-0001", title="T", date=raw_date,
            category="c", mapped_tp_ids=[], url="https://x", severity="low",
            summary="s",
        )

    def test_raw_string_date_normalized_in_csv_row(self):
        row = self._alert("08/20/2026").to_csv_row()
        assert row[3] == "2026-08-20"

    def test_iso_timestamp_normalized_in_csv_row(self):
        row = self._alert("2026-08-21T01:49:20.000Z").to_csv_row()
        assert row[3] == "2026-08-21"
