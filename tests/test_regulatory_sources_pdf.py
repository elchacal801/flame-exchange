"""
test_regulatory_sources_pdf.py --- Tests for FinCEN and FBI IC3 sources.

Covers: FinCENSource, FBIC3Source.
Tests focus on parse() with pre-extracted HTML strings.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from regulatory.models import RegulatoryAlert
from regulatory.sources.fincen import FinCENSource
from regulatory.sources.fbi_ic3 import FBIC3Source


def _make_config(extra=None):
    config = {"enabled": True, "category_mapping": {}}
    if extra:
        config.update(extra)
    return config


FINCEN_HTML = """
<table>
  <tr><th>Title</th><th>Date</th><th>Description</th></tr>
  <tr>
    <td><a href="/advisory/fake.pdf">FinCEN Advisory on Money Laundering</a></td>
    <td><time>2026-02-15</time></td>
    <td>Advisory on the Use of Money Laundering Networks</td>
  </tr>
  <tr>
    <td><a href="/advisory/fake2.pdf">FinCEN Advisory on Ransomware</a></td>
    <td>2026-02-10</td>
    <td>Advisory on Ransomware and the Financial System</td>
  </tr>
  <tr>
    <td>No Link Here</td>
    <td><time>Invalid Date</time></td>
    <td>Should be skipped</td>
  </tr>
</table>
"""

# Shaped like the Alerts table on the hub page: the link text is the
# FIN identifier and the human-readable title sits in the description.
FINCEN_ALERTS_HTML = """
<table class="usa-table">
  <thead><tr><th>Title</th><th>Date</th><th>Description</th></tr></thead>
  <tbody>
    <tr>
      <td><a href="/system/files/2026-07/FinCEN-Alert-Student-Aid.pdf">FIN-2026-Alert004</a></td>
      <td>07/24/2026</td>
      <td>FinCEN Alert on Fraud Schemes Targeting Federal Student Aid</td>
    </tr>
    <tr>
      <td><a href="/advisory/fake.pdf">FinCEN Advisory on Money Laundering</a></td>
      <td><time>2026-02-15</time></td>
      <td>Duplicate of the advisories listing entry</td>
    </tr>
  </tbody>
</table>
"""


class TestFinCENSource:
    def test_name(self):
        src = FinCENSource(_make_config())
        assert src.name == "fincen"

    def test_parse_produces_correct_alerts(self):
        src = FinCENSource(_make_config())
        alerts = src.parse(FINCEN_HTML)
        assert len(alerts) == 2
        
        assert alerts[0].title == "FinCEN Advisory on Money Laundering"
        assert alerts[0].date == "2026-02-15"
        assert alerts[0].url == "https://www.fincen.gov/advisory/fake.pdf"
        assert alerts[0].category == "money-laundering"
        assert alerts[0].severity == "medium"

        assert alerts[1].title == "FinCEN Advisory on Ransomware"
        assert alerts[1].date == "2026-02-10"
        assert alerts[1].url == "https://www.fincen.gov/advisory/fake2.pdf"
        assert alerts[1].category == "ransomware"

    def test_parse_severity_high_when_tp_mapped(self):
        config = _make_config({"category_mapping": {"money-laundering": ["TP-0001"]}})
        src = FinCENSource(config)
        alerts = src.parse(FINCEN_HTML)
        assert alerts[0].severity == "high"
        assert alerts[0].mapped_tp_ids == ["TP-0001"]

    def test_parse_empty_html(self):
        src = FinCENSource(_make_config())
        assert src.parse("") == []

    @patch("regulatory.sources.fincen.requests.get")
    def test_fetch_downloads_both_listings(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = FINCEN_HTML
        mock_get.return_value = mock_resp

        src = FinCENSource(_make_config({
            "url": "https://test.gov/advisories",
            "alerts_url": "https://test.gov/hub",
        }))
        result = src.fetch()

        called = [c.args[0] for c in mock_get.call_args_list]
        assert called == ["https://test.gov/advisories", "https://test.gov/hub"]
        assert FINCEN_HTML in result

    def test_parse_alerts_hub_rows(self):
        src = FinCENSource(_make_config())
        alerts = src.parse(FINCEN_ALERTS_HTML)
        assert len(alerts) == 2

        # FIN-id link text is replaced by the description-column title
        a0 = alerts[0]
        assert a0.title == "FinCEN Alert on Fraud Schemes Targeting Federal Student Aid"
        assert a0.date == "07/24/2026"
        assert a0.category == "benefits-fraud"
        assert a0.url == "https://www.fincen.gov/system/files/2026-07/FinCEN-Alert-Student-Aid.pdf"

    def test_parse_dedupes_by_url_across_pages(self):
        src = FinCENSource(_make_config())
        alerts = src.parse(FINCEN_HTML + FINCEN_ALERTS_HTML)
        urls = [a.url for a in alerts]
        assert len(urls) == len(set(urls))
        # fake.pdf appears in both fixtures but survives only once
        assert urls.count("https://www.fincen.gov/advisory/fake.pdf") == 1


FBI_IC3_HTML = """
<div>
  <ul>
    <li>
      Thu, 19 Feb 2026
      <a href="/CSA/2026/260219.pdf">FBI Alert on BEC</a>
    </li>
    <li>
      Wed, 18 Feb 2026
      <a href="/Media/2026/non-csa.pdf">Should be ignored</a>
    </li>
  </ul>
</div>
"""

class TestFBIC3Source:
    def test_name(self):
        src = FBIC3Source(_make_config())
        assert src.name == "fbi_ic3"

    def test_parse_produces_correct_alerts(self):
        src = FBIC3Source(_make_config())
        alerts = src.parse(FBI_IC3_HTML)
        assert len(alerts) == 1
        
        a = alerts[0]
        assert a.title == "FBI Alert on BEC"
        assert a.date == "Thu, 19 Feb 2026"
        assert a.url == "https://www.ic3.gov/CSA/2026/260219.pdf"
        assert a.category == "Industry Alert"
        assert a.severity == "medium"

    def test_parse_severity_high_when_tp_mapped(self):
        config = _make_config({"category_mapping": {"Industry Alert": ["TP-0010"]}})
        src = FBIC3Source(config)
        alerts = src.parse(FBI_IC3_HTML)
        assert alerts[0].severity == "high"
        assert alerts[0].mapped_tp_ids == ["TP-0010"]

    def test_parse_empty_html(self):
        src = FBIC3Source(_make_config())
        assert src.parse("") == []

    @patch("regulatory.sources.fbi_ic3.requests.get")
    def test_fetch_downloads_html(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = FBI_IC3_HTML
        mock_get.return_value = mock_resp

        src = FBIC3Source(_make_config({"url": "https://test.gov"}))
        result = src.fetch()

        mock_get.assert_called_once()
        assert result == FBI_IC3_HTML
