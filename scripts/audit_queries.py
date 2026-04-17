#!/usr/bin/env python3
"""
FLAME Detection Logic — Query Content Audit Script

Performs deep content-level validation of detection rule queries that
validate_rules.py does not cover:

  Phase 1 — Content checks:
    Check 1: Stub/placeholder detection in query strings
    Check 2: Detection block vs query field consistency
    Check 3: Cross-reference bidirectional consistency (DL<>TP)
    Check 4: Logsource naming consistency across rules
    Check 5: ATT&CK tag format validation
    Check 6: Inline TP rules drift detection
    Check 7: Cross-format threshold consistency

  Phase 2 — Language-specific validation:
    Check 8:  Duplicate UUID detection
    Check 9:  Sigma condition references valid selections
    Check 10: Sigma field modifier syntax
    Check 11: KQL syntax (tables, fields, datetime_diff)
    Check 12: SPL syntax (command ordering, bracket balance, eval)
    Check 13: CQL syntax (equality operator, groupBy, selfJoinFilter)

Outputs a JSON audit report and a human-readable summary.

Exit codes:
  0 = no critical issues
  1 = critical issues found
"""

import yaml
import os
import re
import sys
import json
import glob
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL_DIR = os.path.join(REPO_ROOT, "DetectionLogic")
TP_API_DIR = os.path.join(REPO_ROOT, "api", "v1", "threat-paths")
TP_CONTENT_DIR = os.path.join(REPO_ROOT, "database", "flame-content")
DL_RULES_JSON = os.path.join(REPO_ROOT, "database", "flame_detection_rules.json")
REPORT_PATH = os.path.join(REPO_ROOT, "database", "audit-report.json")

# ── Stub patterns ──────────────────────────────────────────────────────────

STUB_PATTERNS = [
    (r'selfJoinFilter\([^)]*where=\[\.\.\.\]', "Incomplete selfJoinFilter stub"),
    (r'\[\.\.\.\]', "Placeholder [...] found"),
    (r'\bTODO\b', "TODO marker in query"),
    (r'\bFIXME\b', "FIXME marker in query"),
    (r'\bXXX\b', "XXX marker in query"),
    (r'PLACEHOLDER', "PLACEHOLDER marker in query"),
]

# ── Valid ATT&CK tag pattern ──────────────────────────────────────────────

ATTACK_TAG_RE = re.compile(r'^attack\.t\d{4}(\.\d{3})?$')

# ── KQL known tables and fields ──────────────────────────────────────────

KQL_KNOWN_TABLES = {
    "SigninLogs", "AADNonInteractiveUserSignInLogs", "OfficeActivity",
    "CloudAppEvents", "IdentityLogonEvents", "AuditLogs",
    "SecurityAlert", "ThreatIntelligenceIndicator",
}

ENTRA_SIGNINLOGS_FIELDS = {
    "UserPrincipalName", "IPAddress", "UserAgent", "AppId", "AppDisplayName",
    "ResultType", "ResultDescription", "AuthenticationRequirement",
    "ConditionalAccessStatus", "RiskLevelDuringSignIn", "RiskLevelAggregated",
    "SessionId", "CorrelationId", "TimeGenerated", "Location",
    "DeviceDetail", "MfaDetail", "Status", "TokenIssuerType",
    "ResourceDisplayName", "ResourceId", "ClientAppUsed",
    "AuthenticationDetails", "AuthenticationMethodsUsed",
}

OFFICE_ACTIVITY_FIELDS = {
    "Operation", "UserId", "ClientIP", "Parameters", "CreationTime",
    "ResultStatus", "Workload", "RecordType", "TimeGenerated",
}


# ── Helpers ────────────────────────────────────────────────────────────────

def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_fields_from_detection(detection):
    """Extract field names from Sigma-style detection block."""
    fields = set()
    for key, val in detection.items():
        if key in ("condition", "timeframe", "correlation"):
            continue
        if isinstance(val, dict):
            for fk in val.keys():
                base = fk.split("|")[0]
                if base:
                    fields.add(base)
        elif isinstance(val, list):
            pass  # list values are values, not field names
    return fields


def extract_fields_from_query(query_str):
    """Extract likely field names from a KQL/SPL query string via heuristics."""
    fields = set()
    # KQL: where Field == / != / in / contains / has
    for m in re.finditer(r'\bwhere\s+(\w+)\s*(?:==|!=|in\b|contains\b|has\b|has_any\b)', query_str):
        fields.add(m.group(1))
    # KQL: project Field= or just Field
    for m in re.finditer(r'\bproject\s+(.+?)(?:\n|\|)', query_str, re.DOTALL):
        for part in m.group(1).split(","):
            part = part.strip()
            if "=" in part:
                src = part.split("=", 1)[1].strip()
                fields.add(src.split(".")[0].split("(")[0].strip())
            else:
                fields.add(part.split(".")[0].strip())
    # KQL: summarize ... by Field
    for m in re.finditer(r'\bby\s+(\w[\w,\s]*?)(?:\n|\||$)', query_str):
        for part in m.group(1).split(","):
            fields.add(part.strip())
    # SPL: rename Field AS / BY Field
    for m in re.finditer(r'\brename\s+(\w+)\s+AS\b', query_str, re.IGNORECASE):
        fields.add(m.group(1))
    for m in re.finditer(r'\bBY\s+(\w[\w,\s]*?)(?:\n|\||$|\[)', query_str):
        for part in m.group(1).split(","):
            fields.add(part.strip())
    # SPL/CQL: field="value" or field=value (implicit search terms)
    for m in re.finditer(r'\b(\w+)\s*=\s*"[^"]*"', query_str):
        fields.add(m.group(1))
    for m in re.finditer(r'\b(\w+)\s*=\s*(\w+)\b', query_str):
        candidate = m.group(1)
        # Exclude known SPL parameters and operators
        if candidate not in {"index", "sourcetype", "type", "max", "kind",
                             "earliest", "latest", "span", "as", "function",
                             "maxspan", "dc", "count", "values", "min",
                             "comment", "eval", "rename", "search", "OR", "AND"}:
            fields.add(candidate)
    # SPL: field IN ("val1", "val2")
    for m in re.finditer(r'\b(\w+)\s+IN\s*\(', query_str):
        fields.add(m.group(1))
    # SPL: | table field1, field2
    for m in re.finditer(r'\|\s*table\s+(.+?)(?:\n|\||$)', query_str):
        for part in m.group(1).split(","):
            part = part.strip()
            if part and not part.startswith("-"):
                fields.add(part)
    # SPL: | stats ... AS alias
    for m in re.finditer(r'\bAS\s+(\w+)', query_str):
        fields.add(m.group(1))
    # CQL: field>=N or field<=N
    for m in re.finditer(r'\b(\w+)\s*(?:>=|<=|>|<)\s*\d', query_str):
        fields.add(m.group(1))
    # Clean up
    fields.discard("")
    fields -= {"search", "index", "sourcetype", "where", "let", "and", "or",
               "not", "in", "kind", "inner", "type", "max", "on", "earliest",
               "latest", "now", "ago", "true", "false", "comment", "eval",
               "rename", "table", "stats", "values", "count", "dc", "min",
               "transaction", "sort", "head", "tail", "dedup", "fields",
               "round", "relative_time", "if", "case", "like", "match",
               "mvexpand", "spath", "rex", "replace", "split", "substr",
               "groupBy", "collect", "selfJoinFilter", "length",
               "summarize", "extend", "project", "join", "make_set",
               "dcount", "tostring", "datetime_diff",
               "select", "from", "left", "right", "inner", "outer",
               "having", "group", "order", "limit", "offset",
               "OfficeActivity", "SigninLogs", "TP"}
    return fields


def extract_numbers_from_query(query_str):
    """Extract numeric thresholds from query (e.g., >= 2, > 3, <= 4)."""
    thresholds = []
    for m in re.finditer(r'(>=|<=|>|<|==|!=)\s*(\d+\.?\d*)', query_str):
        thresholds.append((m.group(1), float(m.group(2))))
    return thresholds


def normalize_query_for_comparison(query_str):
    """Normalize a query string for drift comparison."""
    # Strip comments, collapse whitespace
    lines = []
    for line in query_str.split("\n"):
        line = re.sub(r'//.*$', '', line)  # KQL comments
        line = re.sub(r'--.*$', '', line)  # SQL comments
        line = line.strip()
        if line:
            lines.append(line)
    return " ".join(lines).lower()


# ── Check functions ────────────────────────────────────────────────────────

def check_stubs(dl_id, rule):
    """Check 1: Stub/placeholder detection."""
    issues = []
    queries = rule.get("queries", {})
    for lang, query_str in queries.items():
        if not isinstance(query_str, str):
            continue
        for pattern, desc in STUB_PATTERNS:
            if re.search(pattern, query_str, re.IGNORECASE):
                issues.append({
                    "check": "stub_detection",
                    "severity": "fail",
                    "lang": lang,
                    "message": f"{desc} in {lang} query",
                })
    # Also check detection condition for prose
    condition = str(rule.get("detection", {}).get("condition", ""))
    if condition and not re.search(r'\b(and|or|not|1 of|all of|selection|filter)\b', condition, re.IGNORECASE):
        # Condition has no Sigma keywords — likely prose
        if len(condition) > 40:
            issues.append({
                "check": "stub_detection",
                "severity": "warn",
                "message": f"Detection condition appears to be prose: {condition[:80]}...",
            })
    return issues


def check_field_consistency(dl_id, rule):
    """Check 2: Detection block vs query field consistency."""
    issues = []
    detection = rule.get("detection", {})
    data_sources = rule.get("data_sources", {})
    queries = rule.get("queries", {})

    det_fields = extract_fields_from_detection(detection)

    # Collect ALL documented fields: native_fields + enrichment_required + derived_fields
    ds_native = set(data_sources.get("native_fields", []))
    ds_enrichment = set()
    for entry in data_sources.get("enrichment_required", []):
        if isinstance(entry, dict):
            ds_enrichment.add(entry.get("field", ""))
    ds_derived = set(data_sources.get("derived_fields", []))
    # Also check cross_log_sources fields
    for xls in data_sources.get("cross_log_sources", []):
        if isinstance(xls, dict):
            ds_native.update(xls.get("fields", []))
    ds_all_fields = ds_native | ds_enrichment | ds_derived
    ds_all_fields.discard("")

    for lang, query_str in queries.items():
        if not isinstance(query_str, str):
            continue
        query_fields = extract_fields_from_query(query_str)

        # Check data_sources fields appear in queries
        if ds_native and query_fields:
            # Only check native fields (enrichment fields may be computed, not in query text)
            missing_in_query = ds_native - query_fields
            # Filter out common false positives (TimeGenerated is often implicit)
            missing_in_query -= {"TimeGenerated", "CreationTime"}
            if len(missing_in_query) > len(ds_native) * 0.5:
                issues.append({
                    "check": "field_consistency",
                    "severity": "warn",
                    "lang": lang,
                    "message": f"data_sources fields not found in {lang} query: {sorted(missing_in_query)}",
                })

    # Check detection block fields vs ALL data_sources fields (native + enrichment + derived)
    if det_fields and ds_all_fields:
        # Exclude Sigma syntax keywords that appear as detection block keys
        sigma_keywords = {"type", "description", "count", "groupby", "timeframe",
                          "near", "condition", "correlation"}
        det_not_in_ds = det_fields - ds_all_fields - sigma_keywords
        if det_not_in_ds:
            issues.append({
                "check": "field_consistency",
                "severity": "warn",
                "message": f"Detection block fields not in data_sources: {sorted(det_not_in_ds)}",
            })

    return issues


def check_cross_references(dl_rules, tp_api_dir):
    """Check 3: Bidirectional DL↔TP cross-reference consistency."""
    issues = []

    # Build DL → TP mapping from YAML
    dl_to_tp = {}
    for dl_id, rule in dl_rules.items():
        dl_to_tp[dl_id] = set(rule.get("threat_paths", []))

    # Build TP → DL mapping from API JSON
    tp_to_dl = {}
    tp_files = glob.glob(os.path.join(tp_api_dir, "TP-*.json"))
    for tp_file in tp_files:
        try:
            tp_data = load_json(tp_file)
            # Handle both {data: {...}} and flat structure
            inner = tp_data.get("data", tp_data)
            tp_id = inner.get("id", os.path.basename(tp_file).replace(".json", ""))
            dl_ids = set(inner.get("detection_rule_ids", []))
            tp_to_dl[tp_id] = dl_ids
        except Exception:
            continue

    # Check: DL says it maps to TP, but TP doesn't list the DL
    for dl_id, tp_ids in dl_to_tp.items():
        for tp_id in tp_ids:
            if tp_id in tp_to_dl and dl_id not in tp_to_dl[tp_id]:
                issues.append({
                    "check": "cross_reference",
                    "severity": "fail",
                    "rule": dl_id,
                    "message": f"{dl_id} claims {tp_id} but {tp_id} does not list {dl_id} in detection_rule_ids",
                })

    # Check: TP lists a DL, but that DL doesn't map back to the TP
    for tp_id, dl_ids in tp_to_dl.items():
        for dl_id in dl_ids:
            if dl_id in dl_to_tp and tp_id not in dl_to_tp[dl_id]:
                issues.append({
                    "check": "cross_reference",
                    "severity": "fail",
                    "rule": dl_id,
                    "message": f"{tp_id} lists {dl_id} but {dl_id} does not claim {tp_id} in threat_paths",
                })

    return issues


def check_logsource_consistency(dl_rules):
    """Check 4: Logsource naming consistency.

    Only flags rules that query the same underlying table/index but use
    different logsource service names. Different services under the same
    product (e.g., banking/transaction_monitoring vs banking/voice_authentication)
    are legitimate and not flagged.
    """
    issues = []

    # Extract the primary table/index referenced in each rule's queries
    def get_query_tables(rule):
        tables = set()
        for lang, q in rule.get("queries", {}).items():
            if not isinstance(q, str):
                continue
            # KQL: table name is the first word after let blocks
            for m in re.finditer(r'(?:^|\n)\s*(\w+)\s*\n?\s*\|', q):
                t = m.group(1)
                if t not in ("let", "search", "index"):
                    tables.add(t)
            # SPL: index=X sourcetype=Y
            for m in re.finditer(r'index=(\w+)', q):
                tables.add(f"index:{m.group(1)}")
            for m in re.finditer(r'sourcetype[=:]"?([^"\s]+)"?', q):
                tables.add(f"sourcetype:{m.group(1)}")
        return frozenset(tables) if tables else None

    # Group by (product, table_set) to find rules with same table but diff service
    table_to_services = defaultdict(lambda: defaultdict(list))
    for dl_id, rule in dl_rules.items():
        ls = rule.get("logsource", {})
        product = ls.get("product", "")
        service = ls.get("service", "")
        tables = get_query_tables(rule)
        if product and service and tables:
            table_to_services[(product, tables)][service].append(dl_id)

    for (product, tables), services in table_to_services.items():
        if len(services) > 1:
            svc_summary = ", ".join(
                f"'{s}' ({len(ids)} rules: {', '.join(ids[:3])}{'...' if len(ids)>3 else ''})"
                for s, ids in services.items()
            )
            issues.append({
                "check": "logsource_consistency",
                "severity": "warn",
                "message": (
                    f"Same table(s) {set(tables)} under product '{product}' "
                    f"use different service names: {svc_summary}"
                ),
            })

    return issues


def check_attack_tags(dl_id, rule):
    """Check 5: ATT&CK tag format validation."""
    issues = []
    tags = rule.get("tags", [])
    attack_tags = [t for t in tags if str(t).startswith("attack.")]

    if not attack_tags:
        issues.append({
            "check": "attack_tags",
            "severity": "warn",
            "message": "No ATT&CK technique tags",
        })
    else:
        for tag in attack_tags:
            if not ATTACK_TAG_RE.match(str(tag)):
                issues.append({
                    "check": "attack_tags",
                    "severity": "fail",
                    "message": f"Invalid ATT&CK tag format: '{tag}' (expected attack.tXXXX or attack.tXXXX.XXX)",
                })

    return issues


def check_inline_tp_drift(dl_rules, tp_content_dir, dl_rules_json_path):
    """Check 6: Inline TP rules drift detection."""
    issues = []

    # Load compiled DL rules JSON
    compiled_rules = {}
    if os.path.exists(dl_rules_json_path):
        try:
            all_rules = load_json(dl_rules_json_path)
            for rule in all_rules:
                dl_id = rule.get("dl_id", "")
                if dl_id:
                    compiled_rules[dl_id] = rule
        except Exception:
            pass

    # Check each TP-XXXX-rules.json
    rules_files = glob.glob(os.path.join(tp_content_dir, "TP-*-rules.json"))
    for rules_file in rules_files:
        tp_id = os.path.basename(rules_file).replace("-rules.json", "")
        try:
            tp_rules = load_json(rules_file)
        except Exception:
            issues.append({
                "check": "inline_drift",
                "severity": "fail",
                "tp": tp_id,
                "message": f"Failed to parse {os.path.basename(rules_file)}",
            })
            continue

        inline_rules = tp_rules.get("rules", [])
        if not inline_rules:
            continue

        # Check if inline rules have source_rule traceability
        has_source = any(r.get("source_rule") for r in inline_rules)

        # Find DL rules that should map to this TP
        expected_dl_ids = set()
        for dl_id, rule in dl_rules.items():
            if tp_id in rule.get("threat_paths", []):
                expected_dl_ids.add(dl_id)

        if expected_dl_ids and not has_source:
            issues.append({
                "check": "inline_drift",
                "severity": "warn",
                "tp": tp_id,
                "message": (
                    f"Inline rules lack source_rule traceability. "
                    f"Expected DL rules: {sorted(expected_dl_ids)}"
                ),
            })

        # For rules with source_rule, check content drift
        for inline_rule in inline_rules:
            source_dl = inline_rule.get("source_rule", "")
            if not source_dl or source_dl not in compiled_rules:
                continue

            compiled = compiled_rules[source_dl]
            inline_content = inline_rule.get("content", "")
            inline_type = inline_rule.get("type", "")

            # Compare against compiled query of same type
            compiled_queries = compiled.get("queries", {})
            if inline_type in compiled_queries:
                compiled_content = compiled_queries[inline_type]
                norm_inline = normalize_query_for_comparison(inline_content)
                norm_compiled = normalize_query_for_comparison(compiled_content)
                if norm_inline != norm_compiled:
                    issues.append({
                        "check": "inline_drift",
                        "severity": "warn",
                        "tp": tp_id,
                        "rule": source_dl,
                        "message": f"Inline {inline_type} content drifted from compiled {source_dl}",
                    })

    return issues


def check_threshold_consistency(dl_id, rule):
    """Check 7: Cross-format threshold consistency."""
    issues = []
    queries = rule.get("queries", {})
    if len(queries) < 2:
        return issues

    # Extract thresholds from each query format
    lang_thresholds = {}
    for lang, query_str in queries.items():
        if not isinstance(query_str, str):
            continue
        thresholds = extract_numbers_from_query(query_str)
        if thresholds:
            lang_thresholds[lang] = thresholds

    if len(lang_thresholds) < 2:
        return issues

    # Compare threshold values across formats
    # Extract just the values for a rough comparison
    lang_values = {}
    for lang, thresholds in lang_thresholds.items():
        lang_values[lang] = set(v for _, v in thresholds)

    langs = list(lang_values.keys())
    for i, l1 in enumerate(langs):
        for l2 in langs[i+1:]:
            v1 = lang_values[l1]
            v2 = lang_values[l2]
            # Filter out common noise values (0, 1, 24, etc.)
            noise = {0, 1, 24, 48, 7}
            sig_v1 = v1 - noise
            sig_v2 = v2 - noise
            if sig_v1 and sig_v2:
                overlap = sig_v1 & sig_v2
                diff = sig_v1.symmetric_difference(sig_v2)
                if diff and not overlap:
                    issues.append({
                        "check": "threshold_consistency",
                        "severity": "warn",
                        "message": (
                            f"Threshold mismatch between {l1} and {l2}: "
                            f"{l1}={sorted(sig_v1)}, {l2}={sorted(sig_v2)}"
                        ),
                    })

    return issues


def check_kql_quality(dl_id, rule):
    """Additional KQL-specific quality checks."""
    issues = []
    queries = rule.get("queries", {})
    kql = queries.get("kql", "")
    if not kql:
        return issues

    # Check: let statements should end with ;
    let_stmts = re.findall(r'^(\s*let\s+\w+\s*=.*?)(?=\nlet\s|\n\w+\n|\Z)', kql, re.MULTILINE | re.DOTALL)
    for stmt in let_stmts:
        if not stmt.rstrip().endswith(";"):
            issues.append({
                "check": "kql_quality",
                "severity": "warn",
                "message": "KQL let statement may be missing trailing semicolon",
            })

    # Check: join without kind= specified
    joins_without_kind = re.findall(r'\|\s*join\s+(?!kind=)', kql)
    if joins_without_kind:
        issues.append({
            "check": "kql_quality",
            "severity": "warn",
            "message": "KQL join without explicit 'kind=' (defaults to innerunique, may lose rows)",
        })

    # Check: has operator on dynamic array (make_set result)
    if "make_set" in kql:
        # Look for `FieldFromMakeSet has "value"` without tostring
        make_set_fields = re.findall(r'(\w+)\s*=\s*make_set\(', kql)
        for field in make_set_fields:
            if re.search(rf'\b{field}\b\s+has\s+"', kql) and f"tostring({field})" not in kql:
                issues.append({
                    "check": "kql_quality",
                    "severity": "warn",
                    "message": f"KQL 'has' on dynamic array '{field}' — use tostring() first or set_has_element()",
                })

    return issues


def check_spl_quality(dl_id, rule):
    """Additional SPL-specific quality checks."""
    issues = []
    queries = rule.get("queries", {})
    spl = queries.get("splunk", queries.get("spl", ""))
    if not spl:
        return issues

    # Check: join without max= (defaults to max=1)
    join_no_max = re.findall(r'\|\s*join\s+(?!.*\bmax=)', spl)
    if join_no_max:
        issues.append({
            "check": "spl_quality",
            "severity": "warn",
            "message": "SPL join without 'max=' (defaults to max=1, likely loses results)",
        })

    # Check: join used at all (Splunk best practice: prefer stats)
    if re.search(r'\|\s*join\b', spl):
        issues.append({
            "check": "spl_quality",
            "severity": "info",
            "message": "SPL uses join command — consider stats-based approach for better performance",
        })

    return issues


# ── Phase 2: Language-specific validation ─────────────────────────────────

def check_duplicate_uuids(dl_rules):
    """Check 8: Duplicate UUIDs across detection rules."""
    issues = []
    uuid_to_rules = defaultdict(list)
    for dl_id, rule in dl_rules.items():
        rule_uuid = str(rule.get("id", ""))
        if rule_uuid:
            uuid_to_rules[rule_uuid].append(dl_id)
    for uuid_val, dl_ids in uuid_to_rules.items():
        if len(dl_ids) > 1:
            issues.append({
                "check": "duplicate_uuid",
                "severity": "fail",
                "rule": dl_ids[0],
                "message": (
                    f"Duplicate UUID '{uuid_val}' shared by: {', '.join(dl_ids)}. "
                    f"This causes database overwrites and cross-reference corruption."
                ),
            })
    return issues


def check_sigma_condition(dl_id, rule):
    """Check 9: Sigma detection block condition references valid selections."""
    issues = []
    detection = rule.get("detection", {})
    condition = str(detection.get("condition", ""))
    if not condition:
        return issues

    # Only validate rules marked sigma_compatible
    if not rule.get("sigma_compatible"):
        return issues

    # Extract defined selection/filter names (keys that aren't condition/timeframe)
    defined_names = set()
    for key in detection.keys():
        if key not in ("condition", "timeframe", "correlation"):
            defined_names.add(key)

    # Extract names referenced in condition
    # Sigma condition uses: selection_xxx, filter_xxx, aggregation, correlation_xxx, etc.
    # Also supports: 1 of selection_*, all of filter_*, pipe syntax (selection | aggregation)
    referenced = set()

    # Match any defined name that appears as a word boundary in the condition
    for name in defined_names:
        if re.search(r'\b' + re.escape(name) + r'\b', condition):
            referenced.add(name)

    # "X of pattern*" references
    for m in re.finditer(r'(?:1|all)\s+of\s+(\w+)\*', condition):
        prefix = m.group(1)
        matching = {n for n in defined_names if n.startswith(prefix)}
        if not matching:
            issues.append({
                "check": "sigma_condition",
                "severity": "fail",
                "message": f"Condition references '{prefix}*' but no matching selections defined",
            })
        referenced.update(matching)

    # Check for unused definitions
    unused = defined_names - referenced
    if unused:
        issues.append({
            "check": "sigma_condition",
            "severity": "warn",
            "message": f"Defined selections not referenced in condition: {sorted(unused)}",
        })

    return issues


def check_sigma_modifiers(dl_id, rule):
    """Check 10: Sigma field modifier syntax validation."""
    issues = []
    detection = rule.get("detection", {})
    if not rule.get("sigma_compatible"):
        return issues

    VALID_MODIFIERS = {
        "contains", "endswith", "startswith", "cidr", "re", "all",
        "base64", "base64offset", "windash", "wide", "utf16le", "utf16be",
        "gte", "lte", "gt", "lt", "exists",
    }

    for key, val in detection.items():
        if key in ("condition", "timeframe", "correlation"):
            continue
        if not isinstance(val, dict):
            continue
        for field_key in val.keys():
            if "|" in field_key:
                parts = field_key.split("|")
                for mod in parts[1:]:
                    if mod and mod not in VALID_MODIFIERS:
                        issues.append({
                            "check": "sigma_modifiers",
                            "severity": "fail",
                            "message": f"Invalid Sigma modifier '|{mod}' on field '{parts[0]}'",
                        })

    return issues


def check_kql_syntax(dl_id, rule):
    """Check 11: KQL-specific syntax validation."""
    issues = []
    kql = rule.get("queries", {}).get("kql", "")
    if not kql:
        return issues

    # Validate table references
    # First non-comment, non-let line that starts a query should be a known table
    lines = [l.strip() for l in kql.split("\n") if l.strip() and not l.strip().startswith("//")]
    for line in lines:
        if line.startswith("let "):
            continue
        # First non-let line — check if it's a table reference
        table_match = re.match(r'^(\w+)\s*$|^(\w+)\s*\|', line)
        if table_match:
            table = table_match.group(1) or table_match.group(2)
            if table and table not in KQL_KNOWN_TABLES and table not in ("risky_signins", "inbox_changes",
                "mfa_events", "access_events", "new_ip_signins"):
                issues.append({
                    "check": "kql_syntax",
                    "severity": "info",
                    "lang": "kql",
                    "message": f"KQL references table '{table}' — not in known tables list",
                })
        break

    # Validate field references against known schemas
    logsource = rule.get("logsource", {})
    product = logsource.get("product", "")
    service = logsource.get("service", "")

    if product == "azure" and service == "signinlogs":
        # Check SigninLogs field names
        query_fields = extract_fields_from_query(kql)
        unknown = query_fields - ENTRA_SIGNINLOGS_FIELDS - {
            "TimeGenerated", "mfa_events", "access_events", "new_ip_signins",
            "risky_signins", "inbox_changes", "timeWindow",
            # Aliases and computed fields
            "MFATime", "MFA_IP", "MFA_UserAgent", "MFA_AppId",
            "AccessTime", "Access_IP", "Access_UserAgent", "Access_AppId",
            "IPCount", "IPs", "UserAgents", "AppIds", "MinTime", "MaxTime",
            "RiskLevels", "UACount", "UA_str", "SignInTime", "SignInIP",
            "RiskLevel", "RuleTime", "FirstSeen",
            "first_seen", "last_seen", "ip_count", "ua_count",
            "window_hours", "window_minutes",
        }
        if unknown:
            issues.append({
                "check": "kql_syntax",
                "severity": "warn",
                "lang": "kql",
                "message": f"Unknown SigninLogs fields in KQL: {sorted(unknown)}",
            })

    if product == "m365" and service == "exchange":
        query_fields = extract_fields_from_query(kql)
        unknown = query_fields - OFFICE_ACTIVITY_FIELDS - ENTRA_SIGNINLOGS_FIELDS - {
            "risky_signins", "inbox_changes", "new_ip_signins",
            "SignInTime", "SignInIP", "RiskLevel", "RuleTime", "FirstSeen",
            "hours_after_signin",
        }
        if unknown:
            issues.append({
                "check": "kql_syntax",
                "severity": "warn",
                "lang": "kql",
                "message": f"Unknown OfficeActivity/SigninLogs fields in KQL: {sorted(unknown)}",
            })

    # Check datetime_diff syntax — must use single quotes for unit
    for m in re.finditer(r'datetime_diff\s*\(\s*"(\w+)"', kql):
        issues.append({
            "check": "kql_syntax",
            "severity": "warn",
            "lang": "kql",
            "message": f"datetime_diff unit should use single quotes: datetime_diff('{m.group(1)}', ...) not \"{m.group(1)}\"",
        })

    return issues


def check_spl_syntax(dl_id, rule):
    """Check 12: SPL-specific syntax validation."""
    issues = []
    spl = rule.get("queries", {}).get("splunk", "")
    if not spl:
        return issues

    # Check command ordering: search context should come before transforming commands
    transforming_commands = {"stats", "chart", "timechart", "top", "rare", "eventstats"}
    found_transforming = False
    for line in spl.split("\n"):
        line = line.strip()
        if line.startswith("`comment"):
            continue
        cmd_match = re.match(r'\|\s*(\w+)', line)
        if cmd_match:
            cmd = cmd_match.group(1).lower()
            if cmd in transforming_commands:
                found_transforming = True
            elif found_transforming and cmd == "search":
                issues.append({
                    "check": "spl_syntax",
                    "severity": "warn",
                    "lang": "splunk",
                    "message": "SPL 'search' command after transforming command — may not work as expected",
                })

    # Check for common SPL syntax errors
    # Unbalanced subsearch brackets
    open_brackets = spl.count("[")
    close_brackets = spl.count("]")
    if open_brackets != close_brackets:
        issues.append({
            "check": "spl_syntax",
            "severity": "fail",
            "lang": "splunk",
            "message": f"Unbalanced subsearch brackets: {open_brackets} '[' vs {close_brackets} ']'",
        })

    # Check for eval with = instead of == in comparison
    for m in re.finditer(r'\|\s*eval\s+\w+\s*=\s*if\s*\(([^)]+)\)', spl):
        expr = m.group(1)
        # Look for single = in comparison context (not ==)
        if re.search(r'[^!=<>]=[^=]', expr):
            issues.append({
                "check": "spl_syntax",
                "severity": "warn",
                "lang": "splunk",
                "message": "SPL eval may use '=' (assignment) instead of '==' (comparison) in if()",
            })

    return issues


def check_cql_syntax(dl_id, rule):
    """Check 13: CrowdStrike CQL-specific syntax validation."""
    issues = []
    lql = rule.get("queries", {}).get("cql", "")
    if not lql:
        return issues

    # Check: == used instead of = for equality (CQL uses = not ==)
    # But skip inside comments
    for line in lql.split("\n"):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        # CQL filter equality uses = not ==
        if "==" in stripped and "!=" not in stripped.replace("==", ""):
            issues.append({
                "check": "cql_syntax",
                "severity": "warn",
                "lang": "cql",
                "message": f"CQL uses '=' not '==' for equality: {stripped[:80]}",
            })
            break  # One warning per rule is enough

    # Check: groupBy syntax — function= should be a list
    for m in re.finditer(r'groupBy\s*\(([^)]+)\)', lql, re.DOTALL):
        body = m.group(1)
        if "function=" in body and "function=[" not in body:
            issues.append({
                "check": "cql_syntax",
                "severity": "warn",
                "lang": "cql",
                "message": "groupBy function= should use list syntax: function=[...]",
            })

    # Check: selfJoinFilter where= should have at least 2 conditions in {}
    for m in re.finditer(r'selfJoinFilter\s*\([^)]*where=\[([^\]]*)\]', lql, re.DOTALL):
        where_body = m.group(1)
        condition_count = len(re.findall(r'\{[^}]+\}', where_body))
        if condition_count < 2:
            issues.append({
                "check": "cql_syntax",
                "severity": "warn",
                "lang": "cql",
                "message": f"selfJoinFilter where= has {condition_count} conditions (need >= 2 for correlation)",
            })

    return issues


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    # Load all DL rules from YAML
    dl_rules = {}
    yaml_files = sorted(glob.glob(os.path.join(DL_DIR, "DL-*.yml")))
    for path in yaml_files:
        fname = os.path.basename(path)
        dl_id = fname.split(".")[0][:7]
        try:
            rule = load_yaml(path)
            if isinstance(rule, dict):
                dl_rules[dl_id] = rule
        except Exception as e:
            print(f"  ERROR: Failed to parse {fname}: {e}")

    print(f"[INFO] Loaded {len(dl_rules)} detection rules from YAML")
    print(f"[INFO] Running query content audit...\n")

    # Per-rule checks
    all_issues = []
    rule_reports = {}

    for dl_id, rule in dl_rules.items():
        rule_issues = []
        # Phase 1 checks
        rule_issues.extend(check_stubs(dl_id, rule))
        rule_issues.extend(check_field_consistency(dl_id, rule))
        rule_issues.extend(check_attack_tags(dl_id, rule))
        rule_issues.extend(check_threshold_consistency(dl_id, rule))
        rule_issues.extend(check_kql_quality(dl_id, rule))
        rule_issues.extend(check_spl_quality(dl_id, rule))
        # Phase 2 checks — language-specific validation
        rule_issues.extend(check_sigma_condition(dl_id, rule))
        rule_issues.extend(check_sigma_modifiers(dl_id, rule))
        rule_issues.extend(check_kql_syntax(dl_id, rule))
        rule_issues.extend(check_spl_syntax(dl_id, rule))
        rule_issues.extend(check_cql_syntax(dl_id, rule))

        for issue in rule_issues:
            issue["rule"] = issue.get("rule", dl_id)
        all_issues.extend(rule_issues)
        if rule_issues:
            rule_reports[dl_id] = rule_issues

    # Cross-rule checks
    uuid_issues = check_duplicate_uuids(dl_rules)
    all_issues.extend(uuid_issues)

    xref_issues = check_cross_references(dl_rules, TP_API_DIR)
    all_issues.extend(xref_issues)

    logsource_issues = check_logsource_consistency(dl_rules)
    all_issues.extend(logsource_issues)

    drift_issues = check_inline_tp_drift(dl_rules, TP_CONTENT_DIR, DL_RULES_JSON)
    all_issues.extend(drift_issues)

    # -- Summary --

    fail_count = sum(1 for i in all_issues if i.get("severity") == "fail")
    warn_count = sum(1 for i in all_issues if i.get("severity") == "warn")
    info_count = sum(1 for i in all_issues if i.get("severity") == "info")

    # Count rules with issues
    rules_with_issues = set()
    for issue in all_issues:
        r = issue.get("rule", issue.get("tp", ""))
        if r:
            rules_with_issues.add(r)

    # Group by check type
    by_check = defaultdict(int)
    for issue in all_issues:
        by_check[issue["check"]] += 1

    print("=" * 60)
    print("FLAME Detection Logic — Query Content Audit Report")
    print("=" * 60)
    print(f"Rules audited:       {len(dl_rules)}")
    print(f"Rules with issues:   {len(rules_with_issues)}")
    print(f"Total issues:        {len(all_issues)}")
    print(f"  Critical (fail):   {fail_count}")
    print(f"  Warning:           {warn_count}")
    print(f"  Info:              {info_count}")
    print()

    print("Issues by check:")
    for check, count in sorted(by_check.items()):
        print(f"  {check}: {count}")
    print()

    # Print all issues grouped by severity
    for severity, label in [("fail", "CRITICAL"), ("warn", "WARNING"), ("info", "INFO")]:
        sev_issues = [i for i in all_issues if i.get("severity") == severity]
        if sev_issues:
            print(f"-- {label} ({len(sev_issues)}) -------------------------")
            for issue in sorted(sev_issues, key=lambda x: x.get("rule", x.get("tp", ""))):
                rule = issue.get("rule", issue.get("tp", "???"))
                lang = issue.get("lang", "")
                lang_str = f" [{lang}]" if lang else ""
                print(f"  [{rule}]{lang_str} {issue['message']}")
            print()

    # -- Write JSON report --

    report = {
        "summary": {
            "rules_audited": len(dl_rules),
            "rules_with_issues": len(rules_with_issues),
            "total_issues": len(all_issues),
            "fail_count": fail_count,
            "warn_count": warn_count,
            "info_count": info_count,
            "by_check": dict(by_check),
        },
        "issues": all_issues,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Full report written to: {REPORT_PATH}")

    if fail_count > 0:
        print(f"\nRESULT: FAILED ({fail_count} critical issues)")
        sys.exit(1)
    elif warn_count > 0:
        print(f"\nRESULT: PASSED with {warn_count} warnings")
        sys.exit(0)
    else:
        print("\nRESULT: PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
