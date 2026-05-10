#!/usr/bin/env python3
"""
validate_submission.py - FLAME Submission Validator

Validates the structure and frontmatter of FLAME submission
markdown files, YAML detection-logic files, and JSON emulation playbook files. Designed to run
in CI (GitHub Actions) on PRs that modify ThreatPaths/,
Baselines/, or EmulationPlaybooks/.

Usage:
    python scripts/validate_submission.py <file.md|file.yml|file.json> [...]

Exit codes:
    0 - All files pass validation
    1 - One or more files failed validation
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

VALID_CFPF_PHASES = {"P1", "P2", "P3", "P4", "P5"}

VALID_CATEGORIES = {"ThreatPath", "Baseline", "EmulationPlaybook"}

VALID_ID_PREFIXES = {
    "ThreatPath": "TP-",
    "Baseline": "BL-",
    "EmulationPlaybook": "EP-",
}

VALID_TLP = {"WHITE", "GREEN", "AMBER", "RED"}

TAXONOMY_FILE = Path(__file__).resolve().parent.parent / "data" / "flame_taxonomy.json"
try:
    with open(TAXONOMY_FILE, "r", encoding="utf-8") as _f:
        _tax = json.load(_f)
        VALID_SECTORS = set(_tax.get("sectors", []))
        VALID_FRAUD_TYPES = set(_tax.get("fraud_types", []))
        VALID_INFRA_GEN_METHODS = set(_tax.get("infrastructure_generation_method", []))
        VALID_GEO_TIMING = set(_tax.get("geopolitical_timing", []))
        VALID_NATION_STATE_NEXUS = set(_tax.get("nation_state_nexus", []))
except Exception as _e:
    print(f"WARNING: Failed to load taxonomy from {TAXONOMY_FILE}: {_e}", file=sys.stderr)
    VALID_SECTORS = set()
    VALID_FRAUD_TYPES = set()
    VALID_INFRA_GEN_METHODS = set()
    VALID_GEO_TIMING = set()
    VALID_NATION_STATE_NEXUS = set()

# Load regulatory requirements config for validation
REGULATORY_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "regulatory_requirements.yaml"
VALID_REGULATORY_IDS = set()
try:
    with open(REGULATORY_CONFIG_FILE, "r", encoding="utf-8") as _f:
        _reg_config = yaml.safe_load(_f)
        if _reg_config and "regulations" in _reg_config:
            VALID_REGULATORY_IDS = {r["id"] for r in _reg_config["regulations"] if "id" in r}
except Exception as _e:
    print(f"WARNING: Failed to load regulatory config from {REGULATORY_CONFIG_FILE}: {_e}", file=sys.stderr)

REQUIRED_FRONTMATTER_FIELDS = [
    "id", "title", "category", "date", "author", "source",
    "tlp", "sector", "fraud_types", "cfpf_phases",
]

# Category-aware required fields for markdown submissions
REQUIRED_TP_FIELDS = [
    "id", "title", "category", "date", "author", "source",
    "tlp", "sector", "fraud_types", "cfpf_phases",
]

REQUIRED_BASELINE_FIELDS = [
    "id", "title", "category", "date", "author",
]

# ---------------------------------------------------------------------------
# Detection Logic (YAML) constants
# ---------------------------------------------------------------------------

VALID_DL_STATUSES = {"experimental", "test", "stable", "deprecated"}
VALID_DL_LEVELS = {"informational", "low", "medium", "high", "critical"}
VALID_DL_PRODUCTS = {"banking", "insurance", "ecommerce", "crypto", "healthcare", "government", "telecom", "dns_intelligence"}
REQUIRED_DL_FIELDS = [
    "title", "id", "status", "description", "threat_paths",
    "cfpf_phase", "fraud_types", "logsource", "detection",
    "falsepositives", "level", "tags",
]

# ---------------------------------------------------------------------------
# Confidence scoring & relationship constants
# ---------------------------------------------------------------------------

VALID_SOURCE_RELIABILITY = {"A", "B", "C", "D", "E", "F"}
VALID_INFO_CREDIBILITY = {1, 2, 3, 4, 5, 6}
VALID_RELATIONSHIP_TYPES = {
    "feeds-into", "shares-infrastructure", "escalates-from",
    "provides-mules-for", "enables", "enhances", "related-to",
    "variant-of",
}

REQUIRED_BODY_SECTIONS = [
    "Summary",
    "CFPF Phase Mapping",
    "Detection Approaches",
    "Controls & Mitigations",
    "References",
]

# Matches code-fenced YAML blocks
FRONTMATTER_PATTERN = re.compile(
    r"```ya?ml\s*\n---\s*\n(.*?)\n---\s*\n```",
    re.DOTALL
)


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def report(self) -> str:
        lines = [f"--- {self.filepath} ---"]
        if self.passed:
            lines.append("  PASS")
        else:
            lines.append(f"  FAIL ({len(self.errors)} error(s))")
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)


def validate_dl_file(filepath: Path) -> ValidationResult:
    """Validate a Detection Logic YAML file."""
    result = ValidationResult(str(filepath))

    text = filepath.read_text(encoding="utf-8")

    try:
        meta = yaml.safe_load(text)
    except yaml.YAMLError as e:
        result.error(f"YAML parse error: {e}")
        return result

    if not isinstance(meta, dict):
        result.error("YAML file is not a mapping")
        return result

    # --- Required fields ---
    for field in REQUIRED_DL_FIELDS:
        if field not in meta or meta[field] is None:
            result.error(f"Missing required field: {field}")

    # --- ID: must be UUID v4 ---
    dl_id = meta.get("id", "")
    if dl_id:
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
        if not re.match(uuid_pattern, str(dl_id)):
            result.error(f"ID '{dl_id}' is not a valid UUID v4")

    # --- Status ---
    status = meta.get("status", "")
    if status and status not in VALID_DL_STATUSES:
        result.error(f"Invalid status '{status}'. Must be one of: {', '.join(sorted(VALID_DL_STATUSES))}")

    # --- CFPF phase (single value, not list) ---
    cfpf_phase = meta.get("cfpf_phase", "")
    if cfpf_phase and str(cfpf_phase) not in VALID_CFPF_PHASES:
        result.error(f"Invalid cfpf_phase '{cfpf_phase}'. Must be one of: {', '.join(sorted(VALID_CFPF_PHASES))}")

    # --- Fraud types ---
    fraud_types = meta.get("fraud_types", [])
    if isinstance(fraud_types, list):
        for ft in fraud_types:
            if ft not in VALID_FRAUD_TYPES:
                result.error(f"Unrecognized fraud type '{ft}' (not in taxonomy)")
    elif fraud_types is not None:
        result.error("fraud_types must be a list")

    # --- Logsource ---
    logsource = meta.get("logsource")
    if logsource is not None:
        if not isinstance(logsource, dict):
            result.error("logsource must be a mapping")
        else:
            product = logsource.get("product", "")
            if not product:
                result.error("logsource must have a 'product' key")
            elif product not in VALID_DL_PRODUCTS:
                result.error(f"Invalid logsource product '{product}'. Must be one of: {', '.join(sorted(VALID_DL_PRODUCTS))}")

    # --- Threat paths ---
    threat_paths = meta.get("threat_paths", [])
    if isinstance(threat_paths, list):
        for tp in threat_paths:
            if not re.match(r"^TP-\d{4}$", str(tp)):
                result.error(f"Invalid threat_paths entry '{tp}'. Must match TP-XXXX format")
            else:
                # Warn if the referenced TP file does not exist
                repo_root = filepath.resolve().parent.parent
                tp_pattern = f"{tp}-*.md"
                tp_matches = list((repo_root / "ThreatPaths").glob(tp_pattern))
                if not tp_matches:
                    result.warn(f"threat_paths reference '{tp}' does not match any file in ThreatPaths/")
    elif threat_paths is not None:
        result.error("threat_paths must be a list")

    # --- Detection ---
    detection = meta.get("detection")
    if detection is not None:
        if not isinstance(detection, dict):
            result.error("detection must be a mapping")
        elif "condition" not in detection:
            result.error("detection must have a 'condition' key")

    # --- Level ---
    level = meta.get("level", "")
    if level and level not in VALID_DL_LEVELS:
        result.error(f"Invalid level '{level}'. Must be one of: {', '.join(sorted(VALID_DL_LEVELS))}")

    return result


# ---------------------------------------------------------------------------
# Emulation Playbook (JSON) constants
# ---------------------------------------------------------------------------

REQUIRED_EP_FIELDS = [
    "id", "title", "description", "author", "date",
    "target_threat_paths", "cfpf_phases", "fraud_types",
    "sectors", "prerequisites", "steps", "expected_outcomes",
]

REQUIRED_EP_STEP_FIELDS = [
    "step_number", "cfpf_phase", "title", "action", "expected_result",
]


def validate_ep_file(filepath: Path) -> ValidationResult:
    """Validate an Emulation Playbook JSON file."""
    result = ValidationResult(str(filepath))
    repo_root = Path(__file__).resolve().parent.parent

    text = filepath.read_text(encoding="utf-8")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        result.error(f"JSON parse error: {e}")
        return result

    if not isinstance(data, dict):
        result.error("JSON file is not an object")
        return result

    # --- Required top-level fields ---
    for field in REQUIRED_EP_FIELDS:
        if field not in data or data[field] is None:
            result.error(f"Missing required field: {field}")

    # --- ID: must start with EP- ---
    ep_id = data.get("id", "")
    if ep_id and not str(ep_id).startswith("EP-"):
        result.error(f"ID '{ep_id}' must start with 'EP-'")

    # --- target_threat_paths: list of TP-XXXX that exist ---
    target_tps = data.get("target_threat_paths", [])
    if isinstance(target_tps, list):
        tp_dir = repo_root / "ThreatPaths"
        for tp_id in target_tps:
            if not re.match(r"^TP-\d{4}$", str(tp_id)):
                result.error(f"Invalid target_threat_paths entry '{tp_id}'. Must match TP-XXXX format")
            else:
                tp_matches = list(tp_dir.glob(f"{tp_id}-*.md"))
                if not tp_matches:
                    result.warn(f"target_threat_paths reference '{tp_id}' does not match any file in ThreatPaths/")
    elif target_tps is not None:
        result.error("target_threat_paths must be a list")

    # --- cfpf_phases ---
    phases = data.get("cfpf_phases", [])
    if isinstance(phases, list):
        for p in phases:
            if str(p) not in VALID_CFPF_PHASES:
                result.error(f"Invalid CFPF phase '{p}'. Must be one of: {', '.join(sorted(VALID_CFPF_PHASES))}")
    elif phases is not None:
        result.error("cfpf_phases must be a list")

    # --- fraud_types ---
    fraud_types = data.get("fraud_types", [])
    if isinstance(fraud_types, list):
        for ft in fraud_types:
            if ft not in VALID_FRAUD_TYPES:
                result.error(f"Unrecognized fraud type '{ft}' (not in taxonomy)")
    elif fraud_types is not None:
        result.error("fraud_types must be a list")

    # --- sectors ---
    sectors = data.get("sectors", [])
    if isinstance(sectors, list):
        for s in sectors:
            if s not in VALID_SECTORS:
                result.error(f"Unrecognized sector '{s}' (not in taxonomy)")
    elif sectors is not None:
        result.error("sectors must be a list")

    # --- steps: non-empty list ---
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        result.error("steps must be a list")
        steps = []
    elif len(steps) == 0:
        result.error("steps must not be empty")

    # --- Validate each step ---
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            result.error(f"steps[{i}] must be an object")
            continue

        # Required step fields
        for field in REQUIRED_EP_STEP_FIELDS:
            if field not in step or step[field] is None:
                result.error(f"steps[{i}] missing required field: {field}")

        # Sequential step numbers (1-based)
        step_num = step.get("step_number")
        if step_num is not None and step_num != i + 1:
            result.error(
                f"steps[{i}] has step_number {step_num}, expected {i + 1} (must be sequential)"
            )

        # Step cfpf_phase
        step_phase = step.get("cfpf_phase", "")
        if step_phase and str(step_phase) not in VALID_CFPF_PHASES:
            result.error(
                f"steps[{i}] invalid cfpf_phase '{step_phase}'. "
                f"Must be one of: {', '.join(sorted(VALID_CFPF_PHASES))}"
            )

        # detection_rule_ref (optional) — opaque cross-repo ref to flame-detections
        dl_ref = step.get("detection_rule_ref")
        if dl_ref is not None:
            if not re.match(r"^DL-\d{4}$", str(dl_ref)):
                result.error(f"steps[{i}] detection_rule_ref '{dl_ref}' must match DL-XXXX format")

    return result



def validate_file(filepath: Path) -> ValidationResult:
    """Validate a single submission file (.md or .yml)."""
    result = ValidationResult(str(filepath))

    if not filepath.exists():
        result.error(f"File not found: {filepath}")
        return result

    # Dispatch based on file extension
    if filepath.suffix == ".yml" or filepath.suffix == ".yaml":
        return validate_dl_file(filepath)

    if filepath.suffix == ".json":
        return validate_ep_file(filepath)

    if filepath.suffix != ".md":
        result.error("File must be a .md markdown file, .yml detection logic file, or .json emulation playbook file")
        return result

    text = filepath.read_text(encoding="utf-8")

    # --- Extract frontmatter ---
    match = FRONTMATTER_PATTERN.search(text)
    if not match:
        result.error("No YAML frontmatter block found (expected ```yaml ... ``` with --- delimiters)")
        return result

    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        result.error(f"YAML parse error: {e}")
        return result

    if not isinstance(meta, dict):
        result.error("Frontmatter is not a YAML mapping")
        return result

    # --- Determine category-aware required fields ---
    category = meta.get("category", "")
    if category == "Baseline":
        required_fields = REQUIRED_BASELINE_FIELDS
    else:
        required_fields = REQUIRED_TP_FIELDS

    # --- Required fields ---
    for field in required_fields:
        if field not in meta or meta[field] is None:
            result.error(f"Missing required field: {field}")

    # --- Field-specific validation ---
    # Category
    if category and category not in VALID_CATEGORIES:
        result.error(f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}")

    # ID format
    sub_id = meta.get("id", "")
    if sub_id and category:
        expected_prefix = VALID_ID_PREFIXES.get(category, "")
        if expected_prefix and not str(sub_id).startswith(expected_prefix):
            result.error(f"ID '{sub_id}' does not match expected prefix '{expected_prefix}' for category '{category}'")

    # TLP
    tlp = meta.get("tlp", "")
    if tlp and str(tlp).upper() not in VALID_TLP:
        result.error(f"Invalid TLP value '{tlp}'. Must be one of: {', '.join(sorted(VALID_TLP))}")

    # CFPF phases
    phases = meta.get("cfpf_phases", [])
    if isinstance(phases, list):
        for p in phases:
            if str(p) not in VALID_CFPF_PHASES:
                result.error(f"Invalid CFPF phase '{p}'. Must be one of: {', '.join(sorted(VALID_CFPF_PHASES))}")
    elif phases is not None:
        result.error("cfpf_phases must be a list")

    # Sectors
    sectors = meta.get("sector", [])
    if isinstance(sectors, list):
        for s in sectors:
            if s not in VALID_SECTORS:
                result.warn(f"Unrecognized sector '{s}' (not in standard list)")
    elif sectors is not None:
        result.error("sector must be a list")

    # Fraud types
    fraud_types = meta.get("fraud_types", [])
    if isinstance(fraud_types, list):
        for ft in fraud_types:
            if ft not in VALID_FRAUD_TYPES:
                result.warn(f"Unrecognized fraud type '{ft}' (not in standard list)")
    elif fraud_types is not None:
        result.error("fraud_types must be a list")

    # List fields that should be lists
    list_fields = ["tags", "mitre_attack", "ft3_tactics", "mitre_f3", "groupib_stages"]
    for field in list_fields:
        val = meta.get(field)
        if val is not None and not isinstance(val, list):
            result.error(f"Field '{field}' must be a list")

    # Validate MITRE F3 IDs against known patterns
    f3_ids = meta.get("mitre_f3", [])
    if isinstance(f3_ids, list):
        for fid in f3_ids:
            if not isinstance(fid, str):
                result.warn(f"mitre_f3 entry must be a string, got {type(fid).__name__}")
            elif not (fid.startswith("F1") or fid.startswith("T1") or fid.startswith("FA") or fid.startswith("TA")):
                result.warn(f"mitre_f3 entry '{fid}' does not match expected F3 ID pattern (F1xxx, T1xxx, FAxxx, TAxxx)")

    # UCFF domains (optional, must be a mapping if present)
    ucff = meta.get("ucff_domains")
    if ucff is not None:
        if not isinstance(ucff, dict):
            result.error("Field 'ucff_domains' must be a mapping (object), not a list or scalar")
        else:
            valid_ucff_keys = {"commit", "assess", "plan", "act", "monitor", "report", "improve"}
            for key in ucff:
                if key not in valid_ucff_keys:
                    result.warn(f"Unrecognized UCFF domain '{key}'. Expected: {', '.join(sorted(valid_ucff_keys))}")

    # Infrastructure generation method (optional, must match allowed values)
    infra_gen = meta.get("infrastructure_generation_method")
    if infra_gen is not None:
        if infra_gen not in VALID_INFRA_GEN_METHODS:
            result.error(
                f"Invalid infrastructure_generation_method '{infra_gen}'. "
                f"Must be one of: {', '.join(sorted(VALID_INFRA_GEN_METHODS))}"
            )

    # Geopolitical timing (optional, must match allowed values)
    geo_timing = meta.get("geopolitical_timing")
    if geo_timing is not None:
        if geo_timing not in VALID_GEO_TIMING:
            result.error(
                f"Invalid geopolitical_timing '{geo_timing}'. "
                f"Must be one of: {', '.join(sorted(VALID_GEO_TIMING))}"
            )

    # Nation-state nexus (optional, must match allowed values)
    ns_nexus = meta.get("nation_state_nexus")
    if ns_nexus is not None:
        if ns_nexus not in VALID_NATION_STATE_NEXUS:
            result.error(
                f"Invalid nation_state_nexus '{ns_nexus}'. "
                f"Must be one of: {', '.join(sorted(VALID_NATION_STATE_NEXUS))}"
            )

    # MITRE ATT&CK format validation
    mitre = meta.get("mitre_attack", [])
    if isinstance(mitre, list):
        for t in mitre:
            t_str = str(t)
            if t_str and not re.match(r"^T\d{4}(\.\d{3})?$", t_str):
                result.warn(f"MITRE ATT&CK ID '{t_str}' may not match expected format (T####[.###])")

    # --- Confidence scoring (optional, Admiralty Code) ---
    confidence_score = meta.get("confidence_score")
    if confidence_score is not None:
        if not isinstance(confidence_score, (int, float)) or not (0 <= confidence_score <= 100):
            result.error(f"confidence_score must be an integer 0-100, got '{confidence_score}'")

    source_reliability = meta.get("source_reliability")
    if source_reliability is not None:
        if str(source_reliability) not in VALID_SOURCE_RELIABILITY:
            result.error(f"source_reliability must be A-F, got '{source_reliability}'")

    info_credibility = meta.get("info_credibility")
    if info_credibility is not None:
        if info_credibility not in VALID_INFO_CREDIBILITY:
            result.error(f"info_credibility must be 1-6, got '{info_credibility}'")

    # --- Cross-TP relationships (optional) ---
    related_tps = meta.get("related_tps")
    if related_tps is not None:
        if not isinstance(related_tps, list):
            result.error("related_tps must be a list")
        else:
            repo_root = filepath.resolve().parent.parent
            for i, rel in enumerate(related_tps):
                if not isinstance(rel, dict):
                    result.error(f"related_tps[{i}] must be a mapping with 'id' and 'relationship' keys")
                    continue
                rel_id = rel.get("id", "")
                if not rel_id or not re.match(r"^TP-\d{4}$", str(rel_id)):
                    result.error(f"related_tps[{i}].id must match TP-XXXX format, got '{rel_id}'")
                else:
                    tp_matches = list((repo_root / "ThreatPaths").glob(f"{rel_id}-*.md"))
                    if not tp_matches:
                        result.warn(f"related_tps reference '{rel_id}' does not match any file in ThreatPaths/")
                rel_type = rel.get("relationship", "")
                if not rel_type or rel_type not in VALID_RELATIONSHIP_TYPES:
                    result.error(
                        f"related_tps[{i}].relationship must be one of "
                        f"{', '.join(sorted(VALID_RELATIONSHIP_TYPES))}, got '{rel_type}'"
                    )

    # --- Regulatory references (optional) ---
    regulatory_refs = meta.get("regulatory_refs")
    if regulatory_refs is not None:
        if not isinstance(regulatory_refs, list):
            result.error("regulatory_refs must be a list")
        else:
            for ref in regulatory_refs:
                if ref not in VALID_REGULATORY_IDS:
                    result.error(f"Unrecognized regulatory_refs entry '{ref}' (not in config/regulatory_requirements.yaml)")

    # --- Baseline references (optional, ThreatPath only) ---
    baseline_ids = meta.get("baseline_ids")
    if baseline_ids is not None:
        if not isinstance(baseline_ids, list):
            result.error("baseline_ids must be a list")
        else:
            repo_root = filepath.resolve().parent.parent
            for bl_id in baseline_ids:
                if not re.match(r"^BL-\d{4}$", str(bl_id)):
                    result.error(f"baseline_ids entry must match BL-XXXX format, got '{bl_id}'")
                else:
                    bl_matches = list((repo_root / "Baselines").glob(f"{bl_id}-*.md"))
                    if not bl_matches:
                        result.warn(f"baseline_ids reference '{bl_id}' does not match any file in Baselines/")

    # --- Body section validation (only for ThreatPath) ---
    if category != "Baseline":
        body_after_frontmatter = text[match.end():]
        for section in REQUIRED_BODY_SECTIONS:
            pattern = rf"^##\s+{re.escape(section)}"
            if not re.search(pattern, body_after_frontmatter, re.MULTILINE):
                result.error(f"Missing required section: ## {section}")

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py <file.md|file.yml|file.json> [...]", file=sys.stderr)
        sys.exit(2)

    files = [Path(f) for f in sys.argv[1:]]
    results = [validate_file(f) for f in files]

    all_passed = True
    for r in results:
        print(r.report())
        if not r.passed:
            all_passed = False

    print()
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print(f"Results: {passed} passed, {failed} failed out of {len(results)} file(s)")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
