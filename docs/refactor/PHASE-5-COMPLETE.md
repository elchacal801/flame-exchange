# Phase 5: Refactor Complete

**Date:** 2026-05-10
**Baseline tag:** `pre-refactor-baseline`

## What Changed

FLAME was repositioned from a multi-purpose fraud platform to a **fraud intelligence exchange**. Detection rules (221 files) were decoupled into a sibling repo.

### Repos

| Repo | Role | URL |
|------|------|-----|
| flame-fraud | Fraud intelligence exchange: taxonomy, threat paths, frameworks, STIX/MISP/TAXII, MCP server | https://github.com/elchacal801/flame-fraud |
| flame-detections | Detection rule pack: 221 Sigma rules, native queries, sigma exports | https://github.com/elchacal801/flame-detections |

### Phases Executed

| Phase | PR | Summary |
|-------|-----|---------|
| 1 | #72 | Baseline tag + inventory (docs only) |
| 2 | #73 | README reframed as exchange, stale counts fixed, validate_readme_counts.py |
| 3 | N/A | flame-detections scaffolded (v0.1.0) + content migrated (v0.2.0) |
| 4 | #74 | Detection content removed from flame-fraud (~135K lines, 2,087 files) |
| 5 | #75 | Cross-linking, orphan cleanup, final polish |

### Metrics

| Metric | Before | After |
|--------|--------|-------|
| Detection rule files | 221 in flame-fraud | 221 in flame-detections |
| Sigma export files | 1,632 in flame-fraud | 1,632 in flame-detections |
| Tests | 258 | 217 (41 DL tests moved) |
| MCP tools | 7 | 6 (get_detection_rules removed) |
| pySigma dependencies | 4 in flame-fraud | 4 in flame-detections |
| README framing | "platform" | "exchange" |

### Remaining Action Item

- **GitHub repo rename:** `flame-fraud` -> `flame-exchange` approved but not executed. This requires manual GitHub action (Settings > General > Repository name). GitHub will set up redirects but remote URLs in local clones need updating.
