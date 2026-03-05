# Changelog

All notable changes to the FLAME project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.6.0] — 2026-03-04

### Added

- **RSS 2.0 intelligence feed** — Auto-generated `database/feed.xml` with 108 items (34 TPs + 74 DL rules), category tags, and RFC 822 dates; auto-discovery link in `index.html`
- **Emulation Playbook schema** — `Templates/emulation-playbook-template.json` with CFPF phase-mapped steps, TP/DL cross-references, and full validation in `validate_submission.py`
- **5 adversary emulation playbooks** — EP-0001 (Synthetic Identity Bust-Out), EP-0002 (BEC Wire Fraud), EP-0003 (SIM Swap Crypto ATO), EP-0004 (APP Fraud), EP-0005 (A2A Payment Exploitation)
- **Contributor submission interface** — `contribute.html` with type selector, live preview, and pre-filled GitHub Issue URL generation; 2 new Issue Form templates (baseline, emulation playbook)
- **Peer review workflow** — `.github/workflows/peer-review.yml` with label-driven lifecycle (`submitted` → `under-review` → `approved` → `published`), auto-validation, and PR generation
- **Contributor leaderboard** — Build-time extraction from frontmatter authors, `database/flame-contributors.json`, and frontend modal with ranked table
- **CODEOWNERS** — Auto-assign reviewers for submissions to ThreatPaths, DetectionLogic, Baselines, EmulationPlaybooks

### Changed

- `build_database.py` — Added `generate_rss_feed()`, `extract_contributors()`, and `export_contributors_json()` to build pipeline
- `validate_submission.py` — Extended to validate `.json` emulation playbook files with cross-reference resolution
- `index.html` — Added Contribute button, Contributors button with leaderboard modal, RSS auto-discovery link
- `app.js` — Added Contributors modal with `renderContributorsModal()`
- `style.css` — Added leaderboard table styles
- Issue templates — Expanded to 18 sectors, added CFPF phase checkboxes, standardized `submission` label

---

## [0.2.0] — 2026-02-19

### Added

- **Search-driven discovery interface** — Card grid replaces sidebar list
- **Lazy content loading** — Individual TP content fetched on demand via `flame-content/TP-XXXX.json`
- **Pre-computed statistics** — `flame-stats.json` with aggregate counts and coverage matrix
- **Metadata-only index** — `flame-index.json` for fast initial load
- **Coverage heat map** — Modal showing fraud types × CFPF phases matrix
- **Taxonomy toggle** — Switch between CFPF, MITRE ATT&CK, and Group-IB views in detail
- **Copy-to-clipboard** — All code blocks in detail view have copy buttons
- **Look Left / Look Right** — Visual callouts in detail view
- **URL hash routing** — Direct links to threat paths via `#detail/TP-XXXX`
- **Filter panel** — CFPF phase, sector, and fraud type chip filters with clear-all
- **Mobile responsive** — Collapsible filter panel, stacked cards on narrow screens
- **`docs/TAXONOMY.md`** — Complete taxonomy reference
- **`CHANGELOG.md`** — This file

### Changed

- `build_database.py` — Generates three new export files alongside legacy `flame-data.json`
- `index.html` — Complete rewrite with new layout structure
- `app.js` — Complete rewrite with card grid, hash routing, and lazy loading
- `flame-data.js` — Rewritten for v2 data architecture
- `style.css` — Premium dark theme redesign with animations

### Fixed

- TP count corrected to 14 (TP-0015 not yet submitted)

---

## [0.1.0] — 2026-02-12

### Added

- Initial release with 14 seed threat paths (TP-0001 through TP-0014)
- Python build pipeline (`build_database.py`, `validate_submission.py`)
- AI-assisted intake pipeline (`ai_intake.py`)
- GitHub Actions for PR validation and database rebuild
- SQLite index + JSON export
- Vanilla HTML/CSS/JS frontend with sidebar list view
- FS-ISAC CFPF framework as primary mapping structure
- Cross-framework support: MITRE ATT&CK, Group-IB Fraud Matrix 2.0, Stripe FT3, MITRE F3
- Project documentation: `FLAME-project-design.md`, `COMPETITIVE-LANDSCAPE.md`
- GitHub Issue templates for AI-assisted and manual submissions
