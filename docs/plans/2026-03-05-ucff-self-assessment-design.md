# UCFF Maturity Self-Assessment Tool — Design

**Date:** March 5, 2026
**Issue:** #11
**Status:** Approved

---

## Overview

An interactive UCFF maturity self-assessment tool accessible from a new header toolbar button. Users set their organizational maturity across 7 UCFF domains, then see which threat paths they can/cannot effectively detect based on maturity gaps.

## Architecture

- New "UCFF Assessment" button in the header toolbar (alongside Heat Map, Coverage, Graph, etc.)
- Opens a fullscreen modal (matching existing widget pattern)
- Two-panel layout: slider inputs (left), results (right)
- Results update live as sliders move (no submit button)
- Data source: `ucff_domains` from `flame-index.json` (already loaded at page init)
- No new data files, no build pipeline changes, no backend — pure frontend addition

## Components

### 1. Slider Input Panel (Left)

Seven range sliders (1-5), one per UCFF domain: Commit, Assess, Plan, Act, Monitor, Report, Improve.

Each slider shows the current level and a one-line description that updates as the user slides:

| Level | Description |
|-------|-------------|
| 1 | Ad hoc, reactive fraud management |
| 2 | Basic fraud function with some defined processes |
| 3 | Formalized fraud program with proactive capabilities |
| 4 | Data-driven, continuously improving fraud program |
| 5 | Industry-leading, predictive fraud management |

Default position: Level 1 (shows all gaps — worst-case starting point).

### 2. Radar Chart (Right, Top)

D3 7-axis spider chart with two overlaid polygons:

- **Blue polygon**: User's self-assessed maturity (from sliders)
- **Red polygon**: Maximum required maturity across all TPs (the "threat landscape ceiling")

Shows instantly where the organization falls short of what the threat landscape demands.

### 3. TP Gap Grid (Right, Bottom)

Sortable table with columns:

| Column | Description |
|--------|-------------|
| TP ID | Threat path identifier |
| Title | Threat path title |
| Gap Score | Sum of maturity shortfalls across all 7 domains |
| Worst Gap Domain | The domain with the largest shortfall |
| Coverage Status | Covered / Partial / Blind |

Row color-coding: green (gap 0), yellow (gap 1-3), red (gap 4+).

### 4. Summary Stats

Shown above the grid:
- X of N TPs fully covered
- Y TPs with partial gaps
- Z TPs you're blind to
- Weakest domain: the domain with the largest aggregate gap

### 5. Save/Load (JSON)

- "Export" button downloads `flame-ucff-assessment.json` containing the 7 slider values + timestamp
- "Import" button loads it back via file picker
- Simple `JSON.stringify`/`parse` + download link

## Scoring Logic

### Maturity Extraction

Each TP's `ucff_domains` values are strings like `"Level 3"`. Parse: `parseInt(value.match(/\d/))`. Empty string or missing = Level 0 (no requirement).

### Per-TP Gap Calculation

```
for each domain in [commit, assess, plan, act, monitor, report, improve]:
    required = tp.ucff_domains[domain] parsed to int (0 if empty)
    gap[domain] = max(0, required - user_level[domain])
gap_score = sum(all gap values)
worst_gap_domain = domain with highest individual gap value
```

### Coverage Status Thresholds

- **Covered** (green): gap_score = 0
- **Partial** (yellow): gap_score 1-3
- **Blind** (red): gap_score >= 4

### Radar Chart Threat Ceiling

For each domain, `max(required_level)` across all 49 TPs. This single polygon represents the maximum maturity the full threat landscape demands.

## Files Modified

- `index.html` — add header button, modal markup
- `app.js` — add UCFF assessment logic, event handlers, scoring
- `viz.js` — add radar chart rendering function
- `style.css` — add UCFF modal styles, slider styles, grid styles

No new files. No build pipeline changes.

## Non-Goals

- PDF export (users can print-to-PDF from browser)
- Multi-user/team assessments
- Historical trend tracking
- Questionnaire-based input (sliders with descriptions are sufficient)
