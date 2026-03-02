"""FLAME MCP Server — exposes 7 fraud-intelligence tools via Model Context Protocol."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from mcp_server.data_loader import FlameDataLoader

mcp = FastMCP("FLAME Fraud Intelligence")
loader = FlameDataLoader()


# ---------------------------------------------------------------------------
# Tool 1: search_threat_paths
# ---------------------------------------------------------------------------

@mcp.tool()
def search_threat_paths(
    query: str = "",
    sector: str = "",
    fraud_type: str = "",
    cfpf_phase: str = "",
) -> str:
    """Search FLAME threat paths by keyword, sector, fraud type, or CFPF phase.

    Args:
        query: Search text to match against TP title and summary
        sector: Filter by sector (e.g., 'banking', 'insurance', 'crypto')
        fraud_type: Filter by fraud type (e.g., 'account-takeover', 'wire-fraud')
        cfpf_phase: Filter by CFPF phase (P1-P5)

    Returns matching threat paths with id, title, summary, confidence_score, cfpf_phases, and fraud_types.
    """
    results = loader.search_threat_paths(query, sector, fraud_type, cfpf_phase)
    return json.dumps(
        [
            {
                "id": tp["id"],
                "title": tp["title"],
                "summary": tp.get("summary", ""),
                "confidence_score": tp.get("confidence_score"),
                "cfpf_phases": tp.get("cfpf_phases", []),
                "fraud_types": tp.get("fraud_types", []),
            }
            for tp in results
        ],
        indent=2,
    )


# ---------------------------------------------------------------------------
# Tool 2: get_threat_path
# ---------------------------------------------------------------------------

@mcp.tool()
def get_threat_path(tp_id: str) -> str:
    """Get full details of a specific FLAME threat path including body text, detection rules, and relationships.

    Args:
        tp_id: Threat path ID (e.g., 'TP-0001')
    """
    tp = loader.get_threat_path(tp_id)
    if not tp:
        return json.dumps({"error": f"Threat path {tp_id} not found"})
    return json.dumps(tp, indent=2)


# ---------------------------------------------------------------------------
# Tool 3: get_detection_rules
# ---------------------------------------------------------------------------

@mcp.tool()
def get_detection_rules(
    tp_id: str = "",
    fraud_type: str = "",
    level: str = "",
) -> str:
    """Get FLAME detection logic rules, optionally filtered by threat path, fraud type, or severity level.

    Args:
        tp_id: Filter by threat path ID (e.g., 'TP-0001')
        fraud_type: Filter by fraud type (e.g., 'wire-fraud')
        level: Filter by severity level ('informational', 'low', 'medium', 'high', 'critical')
    """
    rules = loader.get_detection_rules(tp_id, fraud_type, level)
    return json.dumps(rules, indent=2)


# ---------------------------------------------------------------------------
# Tool 4: map_framework
# ---------------------------------------------------------------------------

@mcp.tool()
def map_framework(tp_id: str, framework: str) -> str:
    """Get framework-specific mappings for a FLAME threat path.

    Args:
        tp_id: Threat path ID (e.g., 'TP-0001')
        framework: Framework to map ('cfpf', 'mitre', 'groupib', 'ft3', 'ucff')
    """
    tp = loader.get_threat_path(tp_id)
    if not tp:
        return json.dumps({"error": f"Threat path {tp_id} not found"})

    mapping: dict = {"tp_id": tp_id, "framework": framework}

    if framework == "cfpf":
        mapping["phases"] = tp.get("cfpf_phases", [])
    elif framework == "mitre":
        mapping["techniques"] = tp.get("mitre_attack", [])
    elif framework == "groupib":
        mapping["stages"] = tp.get("groupib_stages", [])
    elif framework == "ft3":
        mapping["tactics"] = tp.get("ft3_tactics", [])
    elif framework == "ucff":
        mapping["domains"] = tp.get("ucff_domains", {})
    else:
        return json.dumps(
            {
                "error": (
                    f"Unknown framework '{framework}'. "
                    "Use: cfpf, mitre, groupib, ft3, ucff"
                )
            }
        )

    return json.dumps(mapping, indent=2)


# ---------------------------------------------------------------------------
# Tool 5: assess_coverage
# ---------------------------------------------------------------------------

@mcp.tool()
def assess_coverage(sectors: list[str], fraud_types: list[str]) -> str:
    """Assess your organization's fraud detection coverage based on selected sectors and fraud types.

    Args:
        sectors: List of sectors to assess (e.g., ['banking', 'insurance'])
        fraud_types: List of fraud types to assess (e.g., ['account-takeover', 'wire-fraud'])
    """
    # Get all TPs matching ANY of the selected sectors
    matching_tps = [
        tp
        for tp in loader.threat_paths
        if any(s in tp.get("sectors", []) for s in sectors)
    ]

    # Further filter by fraud types — keep TPs matching ANY of the given fraud types
    relevant_tps = [
        tp
        for tp in matching_tps
        if any(ft in tp.get("fraud_types", []) for ft in fraud_types)
    ]

    # Calculate coverage per fraud type
    coverage: dict[str, dict] = {}
    for ft in fraud_types:
        ft_tps = [tp for tp in relevant_tps if ft in tp.get("fraud_types", [])]
        covered_phases: set[str] = set()
        for tp in ft_tps:
            covered_phases.update(tp.get("cfpf_phases", []))
        coverage[ft] = {
            "threat_path_count": len(ft_tps),
            "covered_phases": sorted(covered_phases),
            "gap_phases": sorted(
                {"P1", "P2", "P3", "P4", "P5"} - covered_phases
            ),
        }

    # Find fraud types with no coverage
    gaps = [ft for ft, cov in coverage.items() if cov["threat_path_count"] == 0]

    # Get recommended detection rules
    relevant_tp_ids = {tp["id"] for tp in relevant_tps}
    all_rules = loader.get_detection_rules()
    recommended = [
        r
        for r in all_rules
        if any(
            tp_id in relevant_tp_ids for tp_id in r.get("threat_path_ids", [])
        )
    ]

    # Average confidence
    conf_scores = [
        tp["confidence_score"]
        for tp in relevant_tps
        if tp.get("confidence_score")
    ]
    avg_confidence = (
        round(sum(conf_scores) / len(conf_scores), 1) if conf_scores else None
    )

    covered_count = len(
        [ft for ft, c in coverage.items() if c["threat_path_count"] > 0]
    )
    coverage_score = (
        round(covered_count / len(fraud_types) * 100, 1) if fraud_types else 0
    )

    result = {
        "sectors": sectors,
        "fraud_types_assessed": fraud_types,
        "total_matching_tps": len(relevant_tps),
        "coverage_score": coverage_score,
        "coverage_by_fraud_type": coverage,
        "uncovered_fraud_types": gaps,
        "recommended_detection_rules": len(recommended),
        "average_confidence": avg_confidence,
        "phase_weakness": _find_phase_weakness(relevant_tps),
    }
    return json.dumps(result, indent=2)


def _find_phase_weakness(tps: list[dict]) -> dict[str, int]:
    """Count how many TPs cover each CFPF phase."""
    phase_counts = {"P1": 0, "P2": 0, "P3": 0, "P4": 0, "P5": 0}
    for tp in tps:
        for p in tp.get("cfpf_phases", []):
            if p in phase_counts:
                phase_counts[p] += 1
    return phase_counts


# ---------------------------------------------------------------------------
# Tool 6: get_baseline
# ---------------------------------------------------------------------------

@mcp.tool()
def get_baseline(baseline_id: str = "", tp_id: str = "") -> str:
    """Get fraud baseline measurements for benchmarking.

    Args:
        baseline_id: Specific baseline ID (e.g., 'BASE-001')
        tp_id: Get baselines related to a threat path ID
    """
    results = loader.get_baseline(baseline_id, tp_id)
    return json.dumps(results, indent=2)


# ---------------------------------------------------------------------------
# Tool 7: look_left_right
# ---------------------------------------------------------------------------

@mcp.tool()
def look_left_right(tp_id: str) -> str:
    """Analyze upstream and downstream relationships for a threat path (CFPF Look Left/Right methodology).

    Args:
        tp_id: Threat path ID to analyze (e.g., 'TP-0001')
    """
    tp = None
    for t in loader.threat_paths:
        if t["id"] == tp_id:
            tp = t
            break
    if not tp:
        return json.dumps({"error": f"Threat path {tp_id} not found"})

    related = tp.get("related_tps", [])

    # Classify relationships
    upstream: list[dict] = []   # Things that feed into or enable this TP
    downstream: list[dict] = []  # Things this TP feeds into or enables
    lateral: list[dict] = []    # Shared infrastructure, enhancements, related

    for rel in related:
        rel_id = rel["id"]
        rel_type = rel["relationship"]
        # Find the related TP's title
        rel_tp = next(
            (t for t in loader.threat_paths if t["id"] == rel_id), None
        )
        rel_title = rel_tp["title"] if rel_tp else rel_id

        entry = {"id": rel_id, "title": rel_title, "relationship": rel_type}

        if rel_type in ("feeds-into", "enables", "provides-mules-for"):
            downstream.append(entry)
        elif rel_type in ("escalates-from",):
            upstream.append(entry)
        else:
            lateral.append(entry)

    # Also check reverse relationships (other TPs that reference this one)
    for other_tp in loader.threat_paths:
        if other_tp["id"] == tp_id:
            continue
        for rel in other_tp.get("related_tps", []):
            if rel["id"] == tp_id:
                other_title = other_tp["title"]
                entry = {
                    "id": other_tp["id"],
                    "title": other_title,
                    "relationship": rel["relationship"],
                }
                if rel["relationship"] in (
                    "feeds-into",
                    "enables",
                    "provides-mules-for",
                ):
                    upstream.append(entry)
                elif rel["relationship"] in ("escalates-from",):
                    downstream.append(entry)
                else:
                    lateral.append(entry)

    result = {
        "tp_id": tp_id,
        "title": tp["title"],
        "cfpf_phases": tp.get("cfpf_phases", []),
        "look_left": {
            "description": "Upstream threat paths that feed into or enable this one",
            "threat_paths": upstream,
        },
        "look_right": {
            "description": "Downstream threat paths enabled or fed by this one",
            "threat_paths": downstream,
        },
        "lateral": {
            "description": "Related threat paths sharing infrastructure or enhancing each other",
            "threat_paths": lateral,
        },
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
