# Phase 4 BEACON — Batch A + B Implementation Design

**Date:** 2026-03-04
**Scope:** Items 4.6, 4.5, 4.4, 4.1, 4.2, 4.3 (skipping 4.7 webhooks)
**Parent design:** `2026-03-03-phase4-beacon-design.md`

---

## Items In Scope

| Item | Description | Est. Hours | Dependencies |
|------|-------------|------------|--------------|
| 4.6 | RSS feed generation | 3-4 | None |
| 4.5 | EP-XXXX JSON schema | 3-4 | None |
| 4.1 | Contributor submission interface | 12-16 | None |
| 4.4 | 5 adversary emulation playbooks | 15-20 | 4.5 |
| 4.2 | Peer review workflow | 6-8 | 4.1 |
| 4.3 | Contributor leaderboard | 4-6 | 4.1, 4.2 |

**Execution order (respecting dependencies):**
```
Track 1: 4.6 (RSS) ─ standalone, do first
Track 2: 4.5 (EP schema) → 4.4 (5 playbooks)
Track 3: 4.1 (submission UI) → 4.2 (peer review) → 4.3 (leaderboard)
```

---

## 4.6 RSS Feed Generation

**Files to modify:**
- `scripts/build_database.py` — add `generate_rss_feed()` after `export_api_v1()` (line ~1508)
- `index.html` — add `<link rel="alternate" type="application/rss+xml">` in `<head>`

**Files to create:**
- `database/feed.xml` (generated)
- `tests/test_rss_feed.py`

**Design:**
- RSS 2.0 format (wider tooling support than Atom)
- One `<item>` per Threat Path and Detection Logic rule
- Fields per item: `<title>`, `<link>` (GitHub Pages URL), `<description>` (first 200 chars of summary), `<pubDate>` (from frontmatter `date`), `<category>` tags (fraud types + CFPF phases)
- Channel metadata: title "FLAME Intelligence Feed", link to GitHub Pages, description
- Auto-regenerated on every build
- Feed URL referenced in `index.html` head for auto-discovery

**Integration point in build_database.py:**
```python
# After export_api_v1(conn, submissions, root)
generate_rss_feed(conn, submissions, dl_rules, root)
```

---

## 4.5 EP-XXXX JSON Schema

**Files to create:**
- `Templates/emulation-playbook-template.json`

**Files to modify:**
- `scripts/validate_submission.py` — add EP validation logic
- `flame_taxonomy.json` — add "EmulationPlaybook" if needed for category validation

**Schema structure:**
```json
{
  "id": "EP-XXXX",
  "title": "string",
  "description": "string",
  "author": "string",
  "date": "YYYY-MM-DD",
  "target_threat_paths": ["TP-XXXX"],
  "cfpf_phases": ["P1", "P2", ...],
  "fraud_types": ["wire-fraud", ...],
  "sectors": ["banking", ...],
  "prerequisites": {
    "environment": "string",
    "tools": ["string"],
    "access_required": "string"
  },
  "steps": [
    {
      "step_number": 1,
      "cfpf_phase": "P1",
      "title": "string",
      "action": "string (human instruction)",
      "automation": "string (optional script/API call)",
      "expected_result": "string",
      "detection_rule_ref": "DL-XXXX (optional)"
    }
  ],
  "expected_outcomes": {
    "detections_triggered": ["DL-XXXX"],
    "alerts_generated": "string",
    "coverage_validated": "string"
  }
}
```

**Validation additions to validate_submission.py:**
- Accept `.json` files with category "EmulationPlaybook"
- Validate required fields: id, title, description, target_threat_paths, steps
- Validate TP-XXXX and DL-XXXX cross-references resolve to existing files
- Validate CFPF phase values
- Validate step_number ordering is sequential
- Add `VALID_CATEGORIES` entry: "EmulationPlaybook" with prefix "EP-"

---

## 4.4 Adversary Emulation Playbooks

**Files to create:**
- `EmulationPlaybooks/EP-0001-synthetic-identity-bust-out.json`
- `EmulationPlaybooks/EP-0002-bec-wire-fraud.json`
- `EmulationPlaybooks/EP-0003-sim-swap-crypto-ato.json`
- `EmulationPlaybooks/EP-0004-app-fraud.json`
- `EmulationPlaybooks/EP-0005-a2a-payment-exploitation.json`

**Coverage matrix:**

| EP | Threat Paths | Fraud Types | CFPF Phases | Key DL Rules |
|----|-------------|-------------|-------------|--------------|
| EP-0001 | TP-0003, TP-0016 | Synthetic identity, bust-out | P1-P5 | DL-0001, DL-0028, DL-0038 |
| EP-0002 | TP-0002, TP-0006 | BEC, wire fraud | P1-P5 | DL-0019, DL-0024, DL-0030, DL-0031 |
| EP-0003 | TP-0008, TP-0013 | ATO, crypto laundering | P1-P5 | DL-0044, DL-0045, DL-0047 |
| EP-0004 | TP-0012, TP-0024 | APP, impersonation | P1-P5 | DL-0050, DL-0051, DL-0055, DL-0056 |
| EP-0005 | TP-0024 | A2A payment fraud | P1-P5 | DL-0055, DL-0056, DL-0057, DL-0058, DL-0059 |

Each playbook: 5-8 steps following the CFPF lifecycle (P1 through P5), with human-readable instructions, optional automation references, expected detection outcomes, and DL rule cross-references.

---

## 4.1 Contributor Submission Interface

**Files to modify:**
- `.github/ISSUE_TEMPLATE/intel_submission_template.yml` — upgrade to Issue Forms
- `.github/ISSUE_TEMPLATE/manual_submission.yml` — upgrade to Issue Forms
- `.github/ISSUE_TEMPLATE/new_threat_path.yml` — upgrade to Issue Forms
- `index.html` — add "Contribute" button to header-actions

**Files to create:**
- `.github/ISSUE_TEMPLATE/baseline_submission.yml` — new template
- `.github/ISSUE_TEMPLATE/emulation_playbook_submission.yml` — new template
- `contribute.html` — browser-based submission form

**Existing template patterns (from intel_submission_template.yml):**
- Already uses Issue Forms YAML with `type: input`, `type: dropdown`, `type: checkboxes`
- Has sector dropdown (10 options) and fraud_types checkboxes (13 types)
- Includes `crafter_name` for contributor credit
- Labels: `["intel-submission", "ai-generation"]`

**Upgrade approach:**
- Keep existing structure, add missing fields from taxonomy (16 sectors, expanded fraud types)
- Add `confidence_level` dropdown (low/medium/high)
- Add `cfpf_phases` checkboxes
- Standardize labels: `["submission", "<type>"]` for peer review workflow compatibility

**contribute.html design:**
- Same Crimson Vector dark theme as main UI
- Form fields mirror Issue template: title, type (TP/DL/BL/EP), sector, fraud types, CFPF phases, content textarea
- Live markdown preview panel (right side)
- "Submit via GitHub" button generates pre-filled GitHub Issue URL
- No backend required — purely client-side

---

## 4.2 Peer Review Workflow

**Files to create:**
- `.github/workflows/peer-review.yml`
- `.github/CODEOWNERS` (if not exists)

**Workflow triggers:**
- `issues: [labeled]` — when `submission` label is applied
- `issue_comment: [created]` — when reviewer posts approval comment

**Lifecycle labels:**
`submitted` → `under-review` → `approved` → `published`

**Workflow steps:**
1. On `submission` label: validate issue body against schema, post validation result as comment
2. On validation pass: apply `under-review` label, auto-assign reviewer from CODEOWNERS
3. On validation fail: apply `needs-revision` label, post specific errors as comment
4. On `approved` label: generate markdown/JSON file, create branch, open PR
5. PR merge triggers existing build pipeline

**CODEOWNERS mapping:**
- `ThreatPaths/` → maintainer
- `DetectionLogic/` → maintainer
- `Baselines/` → maintainer
- `EmulationPlaybooks/` → maintainer

---

## 4.3 Contributor Leaderboard

**Files to modify:**
- `scripts/build_database.py` — add `extract_contributors()` and `export_contributors_json()`
- `app.js` — add leaderboard modal component
- `style.css` — add leaderboard styles
- `index.html` — add "Contributors" button to header-stats

**Files to create:**
- `database/flame-contributors.json` (generated)

**Contributor data sources:**
1. Frontmatter `author` fields in TP/DL/BL/EP files
2. Git log commit authors (fallback)

**Generated JSON structure:**
```json
{
  "contributors": [
    {
      "name": "string",
      "github": "string (optional)",
      "threat_paths": 5,
      "detection_rules": 12,
      "baselines": 2,
      "emulation_playbooks": 1,
      "total": 20
    }
  ],
  "generated_at": "ISO timestamp"
}
```

**Frontend modal:**
- Triggered by "Contributors" button in header-stats area
- Ranked table: avatar, name, TP count, DL count, BL count, EP count, total
- Consistent with existing modal patterns (navigator, assessment, about)

---

## Testing Strategy

New test files:
- `tests/test_rss_feed.py` — RSS XML structure, item count, required fields
- `tests/test_emulation_playbooks.py` — EP schema validation, cross-reference resolution

Extended test files:
- `tests/test_validate_submission.py` — EP validation rules
- `tests/test_build_database.py` — contributor extraction, RSS generation

Target: add 30-40 new test cases (bringing total from 176 to ~210+).

## Verification After Each Item

- `python scripts/build_database.py` succeeds
- `python -m pytest tests/ -v` passes with zero failures
- Frontend dev server: new features render correctly, zero console errors
