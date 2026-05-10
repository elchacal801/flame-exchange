# Phase 1: Refactor Baseline

**Date:** 2026-05-10
**Tag:** `pre-refactor-baseline` (commit `4bb83e5`)
**Branch:** `main`

## Test Suite

```
pytest tests/ -v
258 passed in 19.61s
0 failed
0 errors
```

## Build

```
python scripts/build_database.py
Build complete: 123 loaded, 0 errors, 40 techniques, 221 DL rules (0 DL errors)
```

**Outputs:**
- 86 submissions to `database/flame-data.json`
- 86 submissions to `database/flame-index.json`
- 86 content files to `database/flame-content/`
- 154 evidence entries to `database/flame-evidence-index.json`
- 18,933 regulatory alerts to `database/regulatory-alerts.json`
- 221 detection rules to `database/flame_detection_rules.json`
- 344 search index entries to `database/flame-search-index.json`
- 313 API v1 files
- 307-item RSS feed
- 23 contributors

## Exporters

| Exporter | Status | Output |
|----------|--------|--------|
| `export_flame_stix.py` | PASS | 2,440 STIX objects (221 CoA SDOs, 352 CoA relationships, 163 detection rules JSON) |
| `export_sigma.py` | PASS | 221 total rules: 107 fully converted, 69 pseudocode-only, 45 failed (parse errors), 76 TP packs |
| `export_misp.py` | PASS | Galaxy + cluster (86 entries) + 86 feed events |
| `export_taxii.py` | PASS | 3 collections: threat-paths (2,182), detection-rules (221), baselines (37) |

## Ground-Truth Counts

| Metric | Count | Source |
|--------|-------|--------|
| Threat paths | 86 | `ls ThreatPaths/TP-*.md` |
| Detection rules | 221 | `ls DetectionLogic/DL-*.yml` |
| Sigma-compatible | 98 (44%) | `grep -l "sigma_compatible: true"` |
| Non-Sigma (native query) | 123 (56%) | `grep -l "sigma_compatible: false"` |
| Fraud types | 141 | `flame-stats.json` |
| Sectors | 22 | `flame-stats.json` |
| Frameworks | 6 | CFPF, ATT&CK, F3, FT3, Group-IB FM, UCFF |
| Baselines | 38 | `ls Baselines/BL-*.md` |
| MCP tools | 7 | `mcp_server/server.py` |
| CI workflows | 7 | `.github/workflows/` |

## Pre-Existing Issues

- README hardcodes detection rule count as **217** but actual count is **221** (4 rules added since last README update)
- Sigma export reports 45 parse failures (known: complex correlation rules that don't parse as standard Sigma)
