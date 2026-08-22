"""
test_regulatory_sources_structured.py — Tests for structured regulatory sources.

Covers: CFPBSource, OCCSource, SECSource, OFACSource.
Each source is tested for correct .name attribute, proper alert parsing
from mock data, and TP mapping behaviour.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from regulatory.models import RegulatoryAlert
from regulatory.sources.cfpb import CFPBSource
from regulatory.sources.occ import OCCSource
from regulatory.sources.sec import SECSource
from regulatory.sources.ofac import OFACSource


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _make_config(extra=None):
    """Build a minimal config dict with optional overrides."""
    config = {
        "enabled": True,
        "category_mapping": {},
    }
    if extra:
        config.update(extra)
    return config


# ===========================================================================
# CFPBSource tests
# ===========================================================================

CFPB_API_RESPONSE = {
    "hits": {
        "hits": [
            {
                "_source": {
                    "complaint_id": "12345",
                    "product": "Credit reporting",
                    "date_received": "2026-02-01",
                    "issue": "Incorrect information on your report",
                    "complaint_what_happened": "My credit report shows an account that is not mine.",
                }
            },
            {
                "_source": {
                    "complaint_id": "67890",
                    "product": "Mortgage",
                    "date_received": "2026-02-10",
                    "issue": "Applying for a mortgage or refinancing an existing mortgage",
                    "complaint_what_happened": "",
                }
            },
        ]
    }
}


class TestCFPBSource:
    def test_name(self):
        """CFPBSource.name should be 'cfpb'."""
        src = CFPBSource(_make_config({"base_url": "https://api.example.com"}))
        assert src.name == "cfpb"

    @patch("regulatory.sources.cfpb.requests.get")
    def test_fetch_calls_api(self, mock_get):
        """fetch() should GET from base_url with expected params."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = CFPB_API_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        src = CFPBSource(_make_config({"base_url": "https://api.example.com/complaints"}))
        result = src.fetch()

        mock_get.assert_called_once_with(
            "https://api.example.com/complaints",
            params={"size": 100, "sort": "created_date_desc"},
            timeout=30,
        )
        assert result == CFPB_API_RESPONSE

    def test_parse_produces_correct_alerts(self):
        """parse() should produce one alert per hit with correct fields."""
        src = CFPBSource(_make_config({"base_url": "https://api.example.com"}))
        alerts = src.parse(CFPB_API_RESPONSE)

        assert len(alerts) == 2

        a0 = alerts[0]
        assert a0.source == "cfpb"
        assert a0.alert_id == "cfpb-12345"
        assert a0.title == "Incorrect information on your report"
        assert a0.date == "2026-02-01"
        assert a0.category == "credit-reporting"
        assert a0.severity == "medium"
        assert a0.summary == "My credit report shows an account that is not mine."

        a1 = alerts[1]
        assert a1.alert_id == "cfpb-67890"
        assert a1.category == "mortgage-fraud"

    def test_parse_maps_tp_ids(self):
        """parse() should map product to TP IDs via category_mapping."""
        config = _make_config({
            "base_url": "https://api.example.com",
            "category_mapping": {
                "credit-reporting": ["TP-0051"],
                "mortgage-fraud": ["TP-0002"],
            },
        })
        src = CFPBSource(config)
        alerts = src.parse(CFPB_API_RESPONSE)

        assert alerts[0].mapped_tp_ids == ["TP-0051"]
        assert alerts[1].mapped_tp_ids == ["TP-0002"]

    def test_parse_no_mapping(self):
        """When no category_mapping matches, mapped_tp_ids is empty."""
        src = CFPBSource(_make_config({"base_url": "https://api.example.com"}))
        alerts = src.parse(CFPB_API_RESPONSE)
        assert alerts[0].mapped_tp_ids == []


# ===========================================================================
# OCCSource tests
# ===========================================================================

# Shaped like the post-2026-restructure year-index pages:
# a table of Date | ID | Title rows.
OCC_HTML = '''
<table>
  <thead><tr><th>Date</th><th>ID</th><th>Title</th></tr></thead>
  <tbody>
    <tr>
      <td>01/15/2026</td>
      <td>OCC 2026-1</td>
      <td><a href="/news-issuances/bulletins/2026/bulletin-2026-1.html">BSA/AML Compliance: Updated Examination Procedures</a></td>
    </tr>
    <tr>
      <td>02/01/2026</td>
      <td>OCC 2026-2</td>
      <td><a href="/news-issuances/bulletins/2026/bulletin-2026-2.html">Enforcement Actions and Civil Money Penalties</a></td>
    </tr>
    <tr>
      <td>03/01/2026</td>
      <td>OCC 2026-3</td>
      <td><a href="/about/leadership.html">Not a bulletin link</a></td>
    </tr>
    <tr><td>only-two</td><td>cells</td></tr>
  </tbody>
</table>
'''

class TestOCCSource:
    def test_name(self):
        src = OCCSource(_make_config())
        assert src.name == "occ"

    @patch("regulatory.sources.occ.requests.get")
    def test_fetch_uses_configured_url(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = OCC_HTML
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp

        src = OCCSource(_make_config({"url": "https://occ.test/bulletins.html"}))
        result = src.fetch()
        # A plain URL (no {year} placeholder) is fetched exactly once, as-is.
        mock_get.assert_called_once()
        assert mock_get.call_args[0][0] == "https://occ.test/bulletins.html"
        assert result == OCC_HTML

    @patch("regulatory.sources.occ.requests.get")
    def test_fetch_expands_year_template(self, mock_get):
        from datetime import date as _date
        mock_resp = MagicMock()
        mock_resp.text = OCC_HTML
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp

        src = OCCSource(_make_config({"url": "https://occ.test/{year}-bulletins.html"}))
        src.fetch()
        year = _date.today().year
        called = [c.args[0] for c in mock_get.call_args_list]
        assert called == [
            f"https://occ.test/{year}-bulletins.html",
            f"https://occ.test/{year - 1}-bulletins.html",
        ]

    def test_parse_produces_correct_alerts(self):
        src = OCCSource(_make_config())
        alerts = src.parse(OCC_HTML)

        # Row 3 links outside bulletins, row 4 has too few cells.
        assert len(alerts) == 2

        a0 = alerts[0]
        assert a0.source == "occ"
        assert a0.alert_id.startswith("occ-")
        assert a0.title == "BSA/AML Compliance: Updated Examination Procedures"
        assert a0.date == "01/15/2026"
        assert a0.url == "https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-1.html"
        assert "OCC 2026-1" in a0.summary

        assert alerts[1].category == "Enforcement Action"

    def test_severity_with_tp_mapping(self):
        config = _make_config({
            "category_mapping": {
                "Bulletin": ["TP-0001"],
            },
        })
        src = OCCSource(config)
        alerts = src.parse(OCC_HTML)

        # First row has category "Bulletin" which maps to TP-0001
        assert alerts[0].severity == "medium"
        assert alerts[0].mapped_tp_ids == ["TP-0001"]


# ===========================================================================
# SECSource tests
# ===========================================================================

SEC_HTML = '''
<table>
  <tr>
    <td>2026-01-20</td>
    <td><a href="/litigation/lr/2026-001.htm">Release No. LR-26495</a></td>
    <td>SEC Charges XYZ Corp with Securities Fraud</td>
  </tr>
  <tr>
    <td>2026-02-05</td>
    <td><a href="/litigation/ap/2026-002.htm">Release No. 34-12345</a></td>
    <td>Administrative Proceeding Against ABC Fund</td>
  </tr>
  <tr>
    <td>Irrelevant Row</td>
  </tr>
</table>
'''

class TestSECSource:
    def test_name(self):
        src = SECSource(_make_config())
        assert src.name == "sec"

    @patch("regulatory.sources.sec.requests.get")
    def test_fetch_downloads_html(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SEC_HTML
        mock_get.return_value = mock_resp

        src = SECSource(_make_config({"url": "https://sec.test"}))
        result = src.fetch()
        mock_get.assert_called_once()
        assert result == SEC_HTML

    def test_parse_produces_correct_alerts(self):
        src = SECSource(_make_config())
        alerts = src.parse(SEC_HTML)

        assert len(alerts) == 2

        a0 = alerts[0]
        assert a0.source == "sec"
        assert a0.alert_id.startswith("sec-")
        assert a0.title == "SEC Litigation: SEC Charges XYZ Corp with Securities Fraud"
        assert a0.date == "2026-01-20"
        assert a0.category == "Litigation Release"
        assert a0.url == "https://www.sec.gov/litigation/lr/2026-001.htm"

        a1 = alerts[1]
        assert a1.category == "Litigation Release"

    def test_severity_with_tp_mapping(self):
        config = _make_config({
            "category_mapping": {
                "Litigation Release": ["TP-0031"],
            },
        })
        src = SECSource(config)
        alerts = src.parse(SEC_HTML)

        assert alerts[0].severity == "high"
        assert alerts[0].mapped_tp_ids == ["TP-0031"]

        assert alerts[1].severity == "high"
        assert alerts[1].mapped_tp_ids == ["TP-0031"]



# ===========================================================================
# OFACSource tests
# ===========================================================================

OFAC_SDN_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<sdnList xmlns="https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.XML">
  <publshInformation>
    <Publish_Date>02/20/2026</Publish_Date>
  </publshInformation>
  <sdnEntry>
    <uid>12345</uid>
    <firstName>John</firstName>
    <lastName>DOE</lastName>
    <sdnType>Individual</sdnType>
    <programList>
      <program>SDGT</program>
    </programList>
  </sdnEntry>
  <sdnEntry>
    <uid>67890</uid>
    <firstName>ACME</firstName>
    <lastName>CORP</lastName>
    <sdnType>Entity</sdnType>
    <programList>
      <program>CYBER2</program>
    </programList>
  </sdnEntry>
</sdnList>
"""

OFAC_SDN_XML_NO_NS = b"""<?xml version="1.0" encoding="utf-8"?>
<sdnList>
  <sdnEntry>
    <uid>99999</uid>
    <firstName>Jane</firstName>
    <lastName>SMITH</lastName>
    <sdnType>Individual</sdnType>
    <programList>
      <program>IRAN</program>
    </programList>
  </sdnEntry>
</sdnList>
"""


class TestOFACSource:
    def test_name(self):
        """OFACSource.name should be 'ofac'."""
        src = OFACSource(_make_config({"sdn_url": "https://ofac.example.com/SDN.XML"}))
        assert src.name == "ofac"

    @patch("regulatory.sources.ofac.requests.get")
    def test_fetch_returns_bytes(self, mock_get):
        """fetch() should GET from sdn_url and return raw bytes."""
        mock_resp = MagicMock()
        mock_resp.content = OFAC_SDN_XML
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        src = OFACSource(_make_config({"sdn_url": "https://ofac.example.com/SDN.XML"}))
        result = src.fetch()

        mock_get.assert_called_once_with(
            "https://ofac.example.com/SDN.XML",
            timeout=60,
        )
        assert result == OFAC_SDN_XML

    def test_parse_namespaced_xml(self):
        """parse() should correctly handle namespaced XML."""
        src = OFACSource(_make_config({"sdn_url": "https://ofac.example.com/SDN.XML"}))
        alerts = src.parse(OFAC_SDN_XML)

        assert len(alerts) == 2

        a0 = alerts[0]
        assert a0.source == "ofac"
        assert a0.alert_id == "ofac-12345"
        assert a0.title == "OFAC SDN: John DOE (Individual)"
        assert a0.severity == "high"
        assert a0.category == "terrorism-financing"

        a1 = alerts[1]
        assert a1.alert_id == "ofac-67890"
        assert a1.title == "OFAC SDN: ACME CORP (Entity)"

    def test_parse_non_namespaced_xml(self):
        """parse() should handle XML without namespace prefix."""
        src = OFACSource(_make_config({"sdn_url": "https://ofac.example.com/SDN.XML"}))
        alerts = src.parse(OFAC_SDN_XML_NO_NS)

        assert len(alerts) == 1
        assert alerts[0].alert_id == "ofac-99999"
        assert alerts[0].title == "OFAC SDN: Jane SMITH (Individual)"

    def test_parse_maps_tp_ids(self):
        """parse() should map SDN programs via category_mapping."""
        config = _make_config({
            "sdn_url": "https://ofac.example.com/SDN.XML",
            "category_mapping": {
                "terrorism-financing": ["TP-0001", "TP-0080"],
                "cyber-sanctions": ["TP-0020", "TP-0084"],
            },
        })
        src = OFACSource(config)
        alerts = src.parse(OFAC_SDN_XML)

        assert alerts[0].mapped_tp_ids == ["TP-0001", "TP-0080"]  # SDGT → terrorism-financing
        assert alerts[1].mapped_tp_ids == ["TP-0020", "TP-0084"]  # CYBER2 → cyber-sanctions

    def test_parse_summary_contains_programs(self):
        """Summary should contain program list information."""
        src = OFACSource(_make_config({"sdn_url": "https://ofac.example.com/SDN.XML"}))
        alerts = src.parse(OFAC_SDN_XML)

        assert "SDGT" in alerts[0].summary
        assert "CYBER2" in alerts[1].summary
