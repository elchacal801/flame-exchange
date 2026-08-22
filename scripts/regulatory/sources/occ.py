"""
occ.py — OCC Bulletins year-index source.

Fetches the OCC bulletins year-index pages (current and previous year)
and normalises each bulletin row into a ``RegulatoryAlert``.

OCC restructured its site in mid-2026; the old
``news-issuances/bulletins/index-bulletin-issuances.html`` index now
returns 404. The current listing lives at
``news-events/newsroom/news-issuances-by-year/bulletins/{year}-bulletins.html``
as a table of ``Date | ID | Title`` rows.
"""

import logging
from datetime import date
from typing import List

import requests

from regulatory.base import RegulatorySource
from regulatory.models import RegulatoryAlert

logger = logging.getLogger(__name__)

DEFAULT_URL_TEMPLATE = (
    "https://www.occ.gov/news-events/newsroom/news-issuances-by-year/"
    "bulletins/{year}-bulletins.html"
)


class OCCSource(RegulatorySource):
    """Office of the Comptroller of the Currency — Bulletins year index."""

    name = "occ"

    def fetch(self):
        """Fetch the OCC bulletins year-index page(s).

        The configured ``url`` may contain a ``{year}`` placeholder; it is
        expanded for the current and previous year so the feed stays
        complete across the year boundary. A URL without the placeholder
        is fetched as-is.
        """
        template = self.config.get("url", DEFAULT_URL_TEMPLATE)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        if "{year}" in template:
            year = date.today().year
            urls = [template.format(year=year), template.format(year=year - 1)]
        else:
            urls = [template]

        pages = []
        for url in urls:
            res = requests.get(url, headers=headers, timeout=60)
            # The previous-year page may not exist early in a rollout;
            # only the first (current) URL is required to succeed.
            if res.status_code == 404 and url != urls[0]:
                logger.warning("OCC year page not found, skipping: %s", url)
                continue
            res.raise_for_status()
            pages.append(res.text)
        return "\n".join(pages)

    def parse(self, raw_data) -> List[RegulatoryAlert]:
        """Parse year-index HTML into a list of RegulatoryAlert objects.

        The year-index pages use a table with columns:
        Date (col 0, mm/dd/yyyy) | ID (col 1, e.g. "OCC 2026-2") | Title (col 2, linked).
        """
        alerts: List[RegulatoryAlert] = []
        if not raw_data:
            return []

        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(raw_data, "html.parser")

            for tr in soup.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 3:
                    continue

                a = tds[2].find("a", href=True)
                if not a:
                    continue
                title = a.text.strip()
                if len(title) < 5:
                    continue
                if len(title) > 150:
                    title = title[:147] + "..."

                href = a["href"]
                if "bulletin" not in href.lower():
                    continue
                if href.startswith("/"):
                    href = "https://www.occ.gov" + href

                alert_date = tds[0].text.strip()
                bulletin_id = tds[1].text.strip()

                category = "Bulletin"
                if "enforcement" in title.lower():
                    category = "Enforcement Action"

                tp_ids = self.map_category_to_tps(category)
                severity = "medium" if tp_ids else "low"

                alerts.append(
                    RegulatoryAlert(
                        source=self.name,
                        alert_id=f"occ-{len(alerts):04d}",
                        title=title,
                        date=alert_date,
                        category=category,
                        mapped_tp_ids=tp_ids,
                        url=href,
                        severity=severity,
                        summary=f"OCC Regulatory Bulletin {bulletin_id}".strip(),
                    )
                )
        except Exception as e:
            logger.error(f"Failed to parse OCC alerts: {e}")

        # Dedupe by URL (year pages could overlap after a redesign)
        seen = set()
        unique = []
        for x in alerts:
            if x.url not in seen:
                seen.add(x.url)
                unique.append(x)

        return unique
