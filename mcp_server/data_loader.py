"""FLAME data loader — reads and caches JSON files from the database/ directory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FlameDataLoader:
    """Load and cache FLAME intelligence data from JSON files."""

    def __init__(self, data_dir: str | None = None):
        if data_dir is not None:
            self._root = Path(data_dir)
        else:
            # Default: database/ relative to repository root
            self._root = Path(__file__).resolve().parent.parent / "database"

        self._repo_root = Path(__file__).resolve().parent.parent

        # Eagerly load core indices
        self.threat_paths: list[dict[str, Any]] = self._load_json(
            self._root / "flame-index.json"
        )
        self.detection_rules: list[dict[str, Any]] = self._load_json(
            self._root / "flame_detection_rules.json"
        )
        self.stats: dict[str, Any] = self._load_json(
            self._root / "flame-stats.json"
        )

        # Baselines come from api/v1/baselines.json
        baselines_path = self._repo_root / "api" / "v1" / "baselines.json"
        baselines_raw = self._load_json(baselines_path)
        if isinstance(baselines_raw, dict):
            self.baselines: list[dict[str, Any]] = baselines_raw.get("data", [])
        else:
            self.baselines = baselines_raw

        # Content directory for lazy-loaded TP bodies
        self._content_dir = self._root / "flame-content"

        # Cache for loaded TP content files (lazy)
        self._content_cache: dict[str, dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_json(path: Path) -> Any:
        """Load a JSON file and return its parsed content."""
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def _load_content(self, tp_id: str) -> dict[str, Any] | None:
        """Lazy-load a TP content file from flame-content/."""
        if tp_id in self._content_cache:
            return self._content_cache[tp_id]

        content_path = self._content_dir / f"{tp_id}.json"
        if not content_path.exists():
            return None

        data = self._load_json(content_path)
        self._content_cache[tp_id] = data
        return data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_threat_path(self, tp_id: str) -> dict[str, Any] | None:
        """Get full TP content including body (lazy-load from flame-content/).

        Merges the index metadata with the content file so the returned dict
        has every field from both sources.
        """
        # Find the index entry first
        index_entry = None
        for tp in self.threat_paths:
            if tp["id"] == tp_id:
                index_entry = tp
                break

        if index_entry is None:
            return None

        # Try to load the full content file
        content = self._load_content(tp_id)
        if content is not None:
            # Content file is the superset — merge any index-only fields in
            merged = dict(content)
            for key, value in index_entry.items():
                if key not in merged:
                    merged[key] = value
            return merged

        # Fall back to index-only data
        return dict(index_entry)

    def search_threat_paths(
        self,
        query: str = "",
        sector: str = "",
        fraud_type: str = "",
        cfpf_phase: str = "",
        infrastructure_generation_method: str = "",
        geopolitical_timing: str = "",
        nation_state_nexus: str = "",
    ) -> list[dict[str, Any]]:
        """Filter TPs by query, sector, fraud_type, cfpf_phase, infrastructure_generation_method, geopolitical_timing, or nation_state_nexus."""
        results: list[dict[str, Any]] = []
        query_lower = query.lower()

        for tp in self.threat_paths:
            # Query filter — substring match in title or summary
            if query_lower:
                title = tp.get("title", "").lower()
                summary = tp.get("summary", "").lower()
                if query_lower not in title and query_lower not in summary:
                    continue

            # Sector filter
            if sector and sector not in tp.get("sectors", []):
                continue

            # Fraud type filter
            if fraud_type and fraud_type not in tp.get("fraud_types", []):
                continue

            # CFPF phase filter
            if cfpf_phase and cfpf_phase not in tp.get("cfpf_phases", []):
                continue

            # Infrastructure generation method filter
            if infrastructure_generation_method and tp.get("infrastructure_generation_method") != infrastructure_generation_method:
                continue

            # Geopolitical timing filter
            if geopolitical_timing and tp.get("geopolitical_timing") != geopolitical_timing:
                continue

            # Nation-state nexus filter
            if nation_state_nexus and tp.get("nation_state_nexus") != nation_state_nexus:
                continue

            results.append(tp)

        return results

    def get_detection_rules(
        self,
        tp_id: str = "",
        fraud_type: str = "",
        level: str = "",
    ) -> list[dict[str, Any]]:
        """Filter detection rules by tp_id, fraud_type, level."""
        results: list[dict[str, Any]] = []

        for rule in self.detection_rules:
            # Filter by threat path ID
            if tp_id and tp_id not in rule.get("threat_path_ids", []):
                continue

            # Filter by fraud type
            if fraud_type and fraud_type not in rule.get("fraud_types", []):
                continue

            # Filter by severity level
            if level and rule.get("level", "") != level:
                continue

            results.append(rule)

        return results

    def get_baseline(
        self,
        baseline_id: str = "",
        tp_id: str = "",
    ) -> list[dict[str, Any]]:
        """Get baselines, optionally filtered by baseline_id or tp_id.

        If tp_id is provided, returns baselines whose related_tps include
        that TP (or whose threat_path_ids include it, for forward compat).
        """
        results: list[dict[str, Any]] = []

        for bl in self.baselines:
            # Filter by baseline ID
            if baseline_id and bl.get("id", "") != baseline_id:
                continue

            # Filter by threat path association
            if tp_id:
                # Check related_tps list
                related_ids = [r["id"] if isinstance(r, dict) else r
                               for r in bl.get("related_tps", [])]
                # Also check threat_path_ids if it exists
                tp_ids = bl.get("threat_path_ids", [])
                if tp_id not in related_ids and tp_id not in tp_ids:
                    continue

            results.append(bl)

        return results

    def get_stats(self) -> dict[str, Any]:
        """Return pre-computed stats."""
        return self.stats

    def get_coverage_matrix(self) -> list[dict[str, Any]]:
        """Return coverage matrix from stats."""
        return self.stats.get("coverageMatrix", [])
