"""
base.py — Abstract base class for FLAME regulatory feed sources.

Each concrete source (FinCEN, CFPB, etc.) subclasses ``RegulatorySource``
and implements ``fetch()`` and ``parse()``.  The concrete ``run()`` method
orchestrates both steps with error handling.
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from regulatory.models import RegulatoryAlert

logger = logging.getLogger(__name__)


class RegulatorySource(ABC):
    """Abstract base class for a regulatory alert source.

    Subclasses must set the ``name`` class attribute and implement
    ``fetch()`` and ``parse()``.
    """

    name: str = ""

    def __init__(self, config: dict) -> None:
        """Initialise the source from a per-source config block.

        Parameters
        ----------
        config : dict
            The source-specific section from ``regulatory_sources.yaml``,
            e.g. ``{"enabled": true, "url": "...", "category_mapping": {...}}``.
        """
        self.config = config
        self._id_seen = {}
        self.enabled: bool = config.get("enabled", False)
        self.category_mapping: Dict[str, List[str]] = config.get("category_mapping", {})

    def map_category_to_tps(self, category: str) -> List[str]:
        """Map a regulatory category string to FLAME TP IDs.

        Returns an empty list when the category has no mapping configured.
        """
        return self.category_mapping.get(category, [])

    @abstractmethod
    def fetch(self) -> str:
        """Fetch raw content from the regulatory source.

        Returns
        -------
        str
            Raw content (HTML, XML, JSON, etc.) to be parsed.
        """

    @abstractmethod
    def parse(self, raw: str) -> List[RegulatoryAlert]:
        """Parse raw content into a list of ``RegulatoryAlert`` objects.

        Parameters
        ----------
        raw : str
            The raw content returned by ``fetch()``.

        Returns
        -------
        list[RegulatoryAlert]
            Parsed alerts.
        """

    def _stable_id(self, url: str = "", title: str = "", date: str = "") -> str:
        """Return a deterministic alert id derived from row content.

        Index-based ids (``occ-0000``) renumbered whenever the upstream
        page changed, so the same alert got a new identity every run.
        Hashing url|title|date gives the same id for the same row across
        runs; a numeric suffix disambiguates exact duplicates within one
        parse.
        """
        key = f"{url}|{title}|{date}".encode("utf-8", "replace")
        digest = hashlib.sha1(key, usedforsecurity=False).hexdigest()[:10]
        n = self._id_seen.get(digest, 0)
        self._id_seen[digest] = n + 1
        return f"{self.name}-{digest}" if n == 0 else f"{self.name}-{digest}-{n}"

    def run(self) -> Optional[List[RegulatoryAlert]]:
        """Execute the full fetch-and-parse pipeline.

        Returns ``None`` on failure (fetch or parse raised) so callers can
        distinguish a broken source from one that genuinely had nothing --
        conflating the two is how a 404ing source went unnoticed for
        months.
        """
        self._id_seen = {}
        try:
            raw = self.fetch()
            return self.parse(raw)
        except Exception:
            logger.exception("Error running source %s", self.name)
            return None
