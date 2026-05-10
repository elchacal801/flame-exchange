# Phase 1: Detection Rule Surface Area Inventory

**Date:** 2026-05-10
**Purpose:** Comprehensive inventory of all detection-rule touchpoints before decoupling to `flame-detections`.

---

## 1. Detection Rule Content Files

| Path | Count | Description |
|------|-------|-------------|
| `DetectionLogic/DL-*.yml` | 221 | Sigma-format detection rule YAML files |
| `DetectionLogic/pipelines/cql.yml` | 1 | CrowdStrike CQL pipeline config |
| `DetectionLogic/pipelines/splunk.yml` | 1 | Splunk SPL pipeline config |
| `database/sigma-exports/` | 1,632 | Exported rules: elastic/, sentinel/, splunk/, sigma/, pseudocode/, packs/ |
| `database/flame_detection_rules.json` | 1 (908K) | Aggregated detection rules JSON |
| `database/flame_stix_detection_rules.json` | 1 (144K) | STIX course-of-action SDOs for detection rules |
| `api/v1/detection-rules.json` | 1 | API index of all detection rules |
| `api/v1/detection-rules/DL-*.json` | 221 | Individual rule API endpoints |

**Total files to migrate/remove: ~1,870**

---

## 2. Python Scripts

### Scripts to migrate to flame-detections (6)

| Script | Lines | Purpose |
|--------|-------|---------|
| `scripts/export_sigma.py` | 452 | Reads DetectionLogic/, converts via pySigma backends, writes sigma-exports/ |
| `scripts/sigma_pipeline.py` | 79 | pySigma processing pipeline definition |
| `scripts/validate_rules.py` | 329 | Validates sigma_compatible flag, data_sources, native queries |
| `scripts/remediate_rules.py` | 813 | Auto-fixes DL files (reorders YAML, sets flags, adds query blocks) |
| `scripts/audit_queries.py` | 1,053 | Audits query content, validates Sigma modifiers, TP bidirectional refs |
| `scripts/sync_tp_rules.py` | 222 | Syncs detection rules between TPs and DetectionLogic/ |

### Scripts to modify in flame-fraud (3)

| Script | Lines | What to change |
|--------|-------|---------------|
| `scripts/build_database.py` | 1,906 | Remove: `find_dl_files()` L502, `load_detection_rule()` L510, `export_detection_rules_json()` L1005, `_fetch_detection_rule_ids()` L775, detection_rules schema L307-346, DL processing loop L1846-1902 |
| `scripts/export_flame_stix.py` | 867 | Remove: `build_course_of_action()` L547, DL->CoA block L744-783, `OUTPUT_RULES` L63, bundle assembly L818/821 |
| `scripts/validate_submission.py` | 647 | Remove: "DetectionLogic" from VALID_CATEGORIES, "DL-" from ID_PREFIX |

---

## 3. Test Files

### To remove (1)

| Test | Description |
|------|-------------|
| `tests/test_detection_rules.py` | Dedicated DL tests: required fields, UUID uniqueness, TP refs, query blocks, ATT&CK tags, fraud types, CFPF phases |

### To modify (6)

| Test | What to change |
|------|---------------|
| `tests/test_data_quality.py` | Remove `test_every_tp_has_at_least_one_detection_rule` (L89), remove bidirectional TP-DL consistency tests |
| `tests/test_build_database.py` | Remove assertions on `detection_rules` key in DB output (L378) |
| `tests/test_integration.py` | Remove `TestDetectionRulesJSON` class (L64-89+) |
| `tests/test_mcp_server.py` | Remove `test_get_detection_rules_tool` (L224), update `test_assess_coverage_tool` (L288) |
| `tests/test_export_stix.py` | Remove `extract_detection_rules` tests (L95+), update CoA count assertions |
| `tests/test_emulation_playbooks.py` | Skip DL filesystem validation (L160-169), keep detection_rule_ref as opaque cross-repo ref |

---

## 4. CI Workflows

| Workflow | DL references | Action |
|----------|--------------|--------|
| `build-and-deploy.yml` | Triggers on `DetectionLogic/**`; runs `export_sigma.py` | Remove DL trigger, remove sigma export step |
| `update-database.yml` | Triggers on `DetectionLogic/**` | Remove DL trigger |
| `validate-pr.yml` | Triggers on `DetectionLogic/**`; runs `validate_rules.py`, `audit_queries.py` | Remove DL trigger, remove validation steps |
| `ai-intake.yml` | No DL references | No change |
| `fetch-regulatory.yml` | No DL references | No change |
| `generate_threat_path.yml` | No DL references | No change |
| `peer-review.yml` | No DL references | No change |

---

## 5. MCP Server

| Tool | DL usage | Action |
|------|----------|--------|
| `get_detection_rules` (Tool 3) | Primary — filters and returns detection rules | **Remove entirely** |
| `get_threat_path` (Tool 2) | Returns `detection_rule_ids` field on TP objects | Drop field or leave as opaque ref |
| `assess_coverage` (Tool 5) | Calls `get_detection_rules()`, returns `recommended_detection_rules` count | Remove DL count from response |
| `search_threat_paths` (Tool 1) | No direct DL usage | No change |
| `map_framework` (Tool 4) | No DL usage | No change |
| `get_baseline` (Tool 6) | No DL usage | No change |
| `look_left_right` (Tool 7) | No DL usage | No change |

**Data loader:** `mcp_server/data_loader.py` loads `flame_detection_rules.json` (L26-28), exposes `get_detection_rules()` method (L153-177).

---

## 6. Frontend

| File | DL code | Action |
|------|---------|--------|
| `app.js` | `loadAndRenderDetectionRules()` L1005, `renderRulesGrid()` L2375, `renderRuleDetail()` L2417, `formatDetectionYaml()` L1068, `_buildTPSeverityMap()` L615, `#rules` hash routing | Remove ~550 lines |
| `index.html` | Detection Rules nav tab L155, `rules-view` section L269-297, severity filter chips L198-208 | Remove sections, replace tab with flame-detections link |
| `flame-data.js` | `DETECTION_RULES_URL` L24, `loadAllDetectionRules()` L191, `loadDetectionRules()` L227 | Remove functions and constant |
| `viz.js` | `updateAttackFlowRules()` — rule badges in CFPF attack flow | Remove function |
| `style.css` | `.rule-card`, `.dl-rule-*`, `.rules-view`, `.rules-grid`, `.rule-detail`, `.rule-level-*` classes | Remove all DL-related styles |

---

## 7. README.md References

**50+ lines reference detection logic.** Key locations:

- **Line 5:** Badge `detection_rules-217` (stale count)
- **Line 24:** At a Glance table: "Detection Logic Rules | 217"
- **Line 46:** Comparison table: "Structured detection logic | 217 rules"
- **Lines 88-122:** Mermaid architecture diagram includes `DL["DetectionLogic/*.yml"]` and sigma export flow
- **Line 150:** Repo structure: "DetectionLogic/ 217 Sigma-based detection rules"
- **Lines 291-305:** Detection Logic section (full section)
- **Lines 396-412:** Sigma Detection Packs section
- **Lines 438-453:** MCP server tool list includes `get_detection_rules`

---

## 8. Documentation References

14 docs files reference detection rules:

- `docs/TAXONOMY.md`
- `docs/ARCHITECTURE.md`
- `docs/COMPETITIVE-LANDSCAPE.md`
- `docs/openapi.yaml`
- `docs/MCP-TOOLS.md`
- 9 plan/design docs under `docs/plans/` and `docs/superpowers/`

---

## 9. Dependencies (requirements.txt)

```
pySigma>=1.3.3
pySigma-backend-splunk>=2.1.0
pySigma-backend-elasticsearch>=2.0.2
pySigma-backend-microsoft365defender>=0.3.2
```

These 4 lines move to flame-detections' requirements.txt.

---

## 10. Portability Summary

| Category | Count | % |
|----------|-------|---|
| Sigma-compatible (auto-convert to SPL/EQL/KQL) | 98 | 44% |
| Non-Sigma (native queries required) | 123 | 56% |
| **Total** | **221** | |

Of the 221 rules, the Sigma export pipeline produces:
- 107 fully converted (all 3 backends)
- 69 pseudocode-only (aggregation/correlation rules)
- 45 failed (parse errors in pySigma)

This 44/56 split is the primary motivation for decoupling detection rules — their inconsistent portability creates a misleading value proposition for the parent exchange product.
