# Phase 4: BEACON (v1.0) — Community & Production

> **Goal:** Transform FLAME from a single-developer platform into a community-governed fraud intelligence exchange with production-grade infrastructure, partnership integrations, and automated content pipelines.

## Current State

Phases 1-3 delivered a comprehensive fraud intelligence platform:

| Phase | Version | Key Deliverables |
|---|---|---|
| Phase 1: IGNITE | v0.3 | 33 Threat Paths, 67 Detection Logic rules, full-text search, taxonomy expansion |
| Phase 2: FORGE | v0.4 | REST API (106 endpoints), MCP server, coverage assessment, relationship graph, Sigma export |
| Phase 3: SIGNAL | v0.5 | STIX 2.1 fraud extension (4 SDOs, 5 relationship types), MISP galaxy & feed, framework navigator, regulatory mapping (15 regulations, 6 jurisdictions), TAXII 2.1 endpoints |

FLAME is now a standards-compliant, queryable intelligence platform with interoperable outputs. What it lacks is a community contribution pipeline, production hardening, and the partnership engagement needed to sustain long-term growth beyond a single maintainer.

---

## Priority Ordering

Work items are organized into 3 batches based on dependencies and downstream impact.

### Batch A: Quick Wins (Notifications & Feeds)

Low-dependency items that deliver immediate value and establish automated content distribution.

- **4.6:** RSS feed generation (3-4 hrs)
- **4.7:** Webhook notification integration — Slack/Discord/Teams (4-6 hrs)

### Batch B: Community Infrastructure

The core contribution pipeline. Items are sequenced by dependency: schema before content, forms before workflow, contributions before leaderboard.

- **4.5:** EP-XXXX JSON schema (3-4 hrs)
- **4.1:** Contributor submission interface (12-16 hrs)
- **4.2:** Peer review workflow (6-8 hrs)
- **4.4:** Author 5 adversary emulation playbooks (15-20 hrs)
- **4.3:** Contributor leaderboard (4-6 hrs)

### Batch C: Partnerships & Hardening

External engagement and production readiness. Depends on all implementation items being complete so that demos and documentation reflect the final state.

- **4.8:** MITRE CTID partnership (2-3 hrs)
- **4.9:** FS-ISAC presentation (6-8 hrs)
- **4.10:** Comprehensive test suite (8-12 hrs)
- **4.11:** Production documentation (8-10 hrs)

---

## Detailed Work Items

### 4.1 Contributor Submission Interface

**What it builds:** A streamlined path for external contributors to submit new Threat Paths, Detection Logic rules, Baselines, and Emulation Playbooks without requiring deep knowledge of FLAME's internal file formats.

**Key files/directories:**
- `.github/ISSUE_TEMPLATE/*.yml` (modify existing 3 templates + add new ones)
- `contribute.html` (create — web-based submission preview)

**Dependencies:** None (but should be completed before 4.2).

**Implementation:** Three GitHub Issue templates already exist (threat-path, detection-rule, evidence). These will be upgraded from basic markdown templates to the richer GitHub Issue Forms YAML schema, adding structured dropdowns for fraud type, CFPF phase, sector, and confidence level. New templates will be added for Baseline submissions and Emulation Playbook submissions.

A standalone `contribute.html` page will provide a browser-based form that mirrors the Issue template fields, renders a live markdown preview of the submission, and generates a pre-filled GitHub Issue URL. This lowers the barrier for contributors unfamiliar with GitHub's issue interface. The page will use the same Crimson Vector design language as the main FLAME UI and will be linked from the header navigation.

---

### 4.2 Peer Review Workflow

**What it builds:** An automated GitHub Actions pipeline that manages the full lifecycle of community submissions from initial triage through publication.

**Key files/directories:**
- `.github/workflows/peer-review.yml` (create)
- `.github/CODEOWNERS` (create or modify)

**Dependencies:** 4.1 (submission interface must exist so that issues arrive in the expected format).

**Implementation:** A GitHub Actions workflow will trigger on new issues labeled `submission`. The workflow validates the submission body against the relevant schema (TP, DL, Baseline, or EP), auto-assigns reviewers based on CODEOWNERS rules (matched by fraud type or sector), and applies lifecycle labels: `submitted` -> `under-review` -> `approved` -> `published`. When a reviewer applies the `approved` label, a second workflow step auto-generates the properly formatted markdown or JSON file, creates a branch, commits the file, and opens a PR. Merging the PR triggers the standard build pipeline, which regenerates the database, STIX bundle, MISP feed, and API.

Validation failures will post a comment on the issue with specific errors and apply a `needs-revision` label. This creates a feedback loop that guides contributors toward well-formed submissions without requiring reviewer time on format issues.

---

### 4.3 Contributor Leaderboard

**What it builds:** A frontend component displaying top contributors ranked by Threat Paths authored, Detection Logic rules contributed, and reviews completed.

**Key files/directories:**
- `scripts/build_database.py` (modify — add contributor extraction)
- `database/flame-contributors.json` (generated)
- `app.js` (modify — add leaderboard UI component)
- `style.css` (modify — add leaderboard styles)

**Dependencies:** 4.1 and 4.2 (the contribution and review pipeline must exist so that contributor data accumulates meaningfully).

**Implementation:** The build pipeline will be extended to extract contributor data from two sources: git log (commit authors) and frontmatter `author` fields in TP/DL/BL/EP files. The script will generate `database/flame-contributors.json` containing per-contributor stats: TPs authored, DL rules contributed, reviews completed (from GitHub API — merged PRs with review labels), and total contributions. Review counts will be fetched from the GitHub API during CI builds and cached in the JSON output.

The frontend leaderboard will be rendered as a modal (consistent with the navigator and assessment modals) triggered by a "Contributors" button in the header stats area. It will display a ranked table with contributor name/handle, avatar (GitHub), contribution counts by category, and a link to their GitHub profile. The leaderboard encourages participation through visible recognition.

---

### 4.4 Adversary Emulation Playbooks

**What it builds:** Five structured playbooks that enable fraud teams to simulate real-world fraud scenarios against their detection stack, analogous to MITRE ATT&CK's adversary emulation plans but focused on financial fraud.

**Key files/directories:**
- `EmulationPlaybooks/` (create directory)
- `EmulationPlaybooks/EP-0001-synthetic-identity-bust-out.json`
- `EmulationPlaybooks/EP-0002-bec-wire-fraud.json`
- `EmulationPlaybooks/EP-0003-sim-swap-crypto-ato.json`
- `EmulationPlaybooks/EP-0004-app-fraud.json`
- `EmulationPlaybooks/EP-0005-a2a-payment-exploitation.json`

**Dependencies:** 4.5 (the EP-XXXX JSON schema must be defined first so playbooks conform to it).

**Implementation:** Each playbook is a JSON file following the EP-XXXX schema. The file contains a steps array where each step maps to a CFPF phase and includes: an `action` field with human-readable instructions for the tester, an `automation` field with optional script or API call references, an `expected_result` describing what the detection stack should produce, and a `detection_rule_ref` linking to the relevant DL-XXXX rule. Steps are ordered to follow the fraud lifecycle from reconnaissance through monetization.

The initial set of 5 playbooks covers high-impact fraud types that exercise different parts of the detection stack: synthetic identity bust-out (identity verification + credit lifecycle), BEC wire fraud (email compromise + payment authorization), SIM swap crypto ATO (telecom + crypto exchange), APP fraud (social engineering + real-time payments), and A2A payment exploitation (open banking + account linking). Each playbook will reference existing TPs and DL rules, creating cross-references that strengthen the overall intelligence graph.

---

### 4.5 EP-XXXX JSON Schema

**What it builds:** A formal JSON Schema defining the structure of Emulation Playbook files, plus a template for contributors.

**Key files/directories:**
- `Templates/emulation-playbook-template.json` (create)
- `scripts/validate_submission.py` (modify — add EP schema validation)

**Dependencies:** None.

**Implementation:** The template file will serve dual purpose: a JSON Schema definition for automated validation and a human-readable starting point for contributors. The schema defines required fields: `id` (EP-XXXX format), `title`, `description`, `target_threat_paths` (array of TP-XXXX references), `cfpf_phases` (array of P1-P5), `prerequisites` (environment setup needed), `steps` (ordered array), and `expected_outcomes` (summary of what successful detection looks like).

Each step object within the `steps` array requires: `step_number`, `cfpf_phase`, `action` (human instruction text), `automation` (optional script/API call), `expected_result`, and `detection_rule_ref` (DL-XXXX reference, optional). The `validate_submission.py` script will be extended to validate EP files against this schema, checking that all TP and DL cross-references resolve to existing files and that CFPF phase values are valid.

---

### 4.6 RSS Feed Generation

**What it builds:** An Atom/RSS 2.0 feed file that allows analysts and platforms to subscribe to FLAME content updates.

**Key files/directories:**
- `scripts/build_database.py` (modify — add RSS generation step)
- `database/feed.xml` (generated)

**Dependencies:** None (Batch A — no prerequisites).

**Implementation:** The build pipeline will be extended to generate `database/feed.xml` as the final step of the database build. The feed will be RSS 2.0 format (wider tooling support than Atom) and will contain one `<item>` entry per Threat Path and Detection Logic rule. Each entry includes: `<title>` (TP/DL title), `<link>` (GitHub Pages URL to the detail view), `<description>` (first 200 characters of the summary), `<pubDate>` (derived from frontmatter `date` field, falling back to git commit date), and `<category>` tags for fraud type and CFPF phase.

The feed will be auto-regenerated on every build, ensuring subscribers always see the latest content. A `<link>` element in the main `index.html` `<head>` will advertise the feed for auto-discovery by feed readers. The feed URL will also be included in the MISP feed manifest and the TAXII discovery document for cross-format discoverability.

---

### 4.7 Webhook Notification Integration

**What it builds:** A GitHub Actions workflow that posts notifications to Slack, Discord, and Microsoft Teams channels when FLAME content is updated.

**Key files/directories:**
- `.github/workflows/notify-updates.yml` (create)

**Dependencies:** None (Batch A — no prerequisites).

**Implementation:** A GitHub Actions workflow will trigger on pushes to `main` that modify files in `ThreatPaths/`, `DetectionLogic/`, `Baselines/`, or `EmulationPlaybooks/`. The workflow detects which files changed via `git diff`, extracts the title and fraud types from frontmatter, and constructs a notification payload. Three parallel notification steps will post to webhook URLs stored as repository secrets: `SLACK_WEBHOOK_URL`, `DISCORD_WEBHOOK_URL`, and `TEAMS_WEBHOOK_URL`. Each step is conditional on its respective secret being configured, so repositories can opt into whichever channels they use.

The notification message will include: the content type (TP, DL, BL, or EP), title, a direct link to the file on GitHub Pages, key fraud types as tags, and whether it is a new addition or an update to existing content. Discord and Slack messages will use embed formatting for rich display; Teams messages will use Adaptive Card format.

---

### 4.8 MITRE CTID Partnership

**What it builds:** A formal partnership proposal for MITRE's Center for Threat-Informed Defense, positioning FLAME as a community data source for fraud-specific extensions to ATT&CK.

**Key files/directories:**
- `docs/partnerships/mitre-ctid-proposal.md` (create)

**Dependencies:** All implementation items should be complete so the proposal reflects the full v1.0 platform.

**Implementation:** The proposal document will be structured as a formal participation request letter addressing MITRE CTID leadership. It will package FLAME's contributions in three areas: (1) the 50+ Threat Paths and 150+ Detection Logic rules as structured source data for F3 (Fraud, Forgery & Falsification) framework development, (2) the STIX 2.1 fraud extension (4 custom SDOs, 5 relationship types) as a contribution to the STIX ecosystem that fills the gap in fraud-specific object types, and (3) the CFPF lifecycle model as a complementary kill chain to ATT&CK's existing cyber kill chain, specifically designed for financial fraud workflows.

The proposal will include a technical appendix with data format examples, API access instructions, and a mapping between FLAME TPs and existing ATT&CK techniques to demonstrate interoperability. The document will follow MITRE CTID's published participation model and reference their existing collaborative projects as precedent.

---

### 4.9 FS-ISAC Presentation

**What it builds:** A presentation package for FS-ISAC (Financial Services Information Sharing and Analysis Center) audiences, including an outline and a live demo script.

**Key files/directories:**
- `docs/partnerships/fsisac-presentation-outline.md` (create)

**Dependencies:** All implementation items should be complete for the live demo to showcase the full platform.

**Implementation:** The presentation outline will cover five segments: (1) the problem statement — fragmented fraud intelligence across institutions, (2) FLAME's architecture — CFPF lifecycle model, static-first design, detection-as-code approach, (3) community model — contributor pipeline, peer review, leaderboard, (4) integration points — STIX export, MISP galaxy, TAXII feed, REST API, MCP server, and (5) call to action — how FS-ISAC members can contribute TPs from their institution's fraud patterns.

The live demo script will provide step-by-step instructions for demonstrating: full-text search across TPs, the API's filtering and relationship endpoints, the MCP server responding to natural language fraud queries, the framework navigator showing cross-framework coverage, STIX bundle export and TAXII consumption, and the contributor submission flow. Each demo step will include fallback screenshots in case of connectivity issues during live presentation.

---

### 4.10 Comprehensive Test Suite

**What it builds:** Expanded automated test coverage targeting all Phase 1-4 features, with a goal of 250+ test cases (up from 176).

**Key files/directories:**
- `tests/test_stix_export.py` (create or expand)
- `tests/test_taxii.py` (create or expand)
- `tests/test_sigma.py` (create or expand)
- `tests/test_api.py` (create or expand)
- `tests/test_emulation_playbooks.py` (create)
- `tests/test_rss_feed.py` (create)
- `tests/test_contributor_pipeline.py` (create)

**Dependencies:** All implementation items (4.1-4.9) must be complete so that tests can exercise the full feature set.

**Implementation:** The test suite will be organized into four tiers. Unit tests will validate individual functions: STIX SDO generation, MISP cluster formatting, RSS XML structure, EP schema validation, and contributor data extraction. Integration tests will validate the end-to-end build pipeline: `build_database.py` produces valid index JSON, STIX export generates a valid bundle, MISP export creates spec-compliant galaxy and feed files, TAXII endpoints serve valid discovery and collection documents, and RSS feed contains entries for all TPs.

API endpoint tests will verify all 106+ endpoints return correct status codes, content types, and response structures. Sigma conversion tests will validate that every DL rule with a Sigma mapping produces a syntactically valid Sigma rule. A new Emulation Playbook test module will validate all EP files against the JSON schema, verify that TP and DL cross-references resolve, and confirm that CFPF phase coverage is complete for each playbook. Target: 250+ test cases with zero failures.

---

### 4.11 Production Documentation

**What it builds:** A complete documentation set for users, contributors, and integrators of the FLAME platform.

**Key files/directories:**
- `docs/API-REFERENCE.md` (create)
- `docs/MCP-GUIDE.md` (create)
- `docs/CONTRIBUTOR-HANDBOOK.md` (create)
- `docs/DEPLOYMENT.md` (create)

**Dependencies:** All implementation items (4.1-4.9) must be complete so that documentation reflects the final state.

**Implementation:** Four documents will be authored. The **API Reference** will be auto-generated from the endpoint directory structure, documenting every endpoint path, HTTP method, query parameters, response format, and example responses. The **MCP Server Guide** will cover setup instructions, available tool descriptions, example natural language queries, and integration with Claude Desktop and other MCP clients.

The **Contributor Handbook** will walk new contributors through writing each content type: Threat Paths (CFPF mapping, frontmatter fields, evidence requirements), Detection Logic rules (Sigma format, confidence scoring, false positive guidance), Baselines (peer institution data, threshold calibration), and Emulation Playbooks (step authoring, cross-referencing). The **Deployment Guide** will cover GitHub Pages hosting, MISP feed subscription configuration, TAXII client setup, RSS reader configuration, and webhook integration for Slack/Discord/Teams.

---

## Dependencies

```
Batch A (no dependencies — start immediately)
├── 4.6: RSS feed generation
└── 4.7: Webhook notifications

Batch B (sequential internal dependencies)
├── 4.5: EP-XXXX JSON schema          ← no dependencies
│   └── 4.4: Emulation playbooks      ← needs 4.5
├── 4.1: Contributor submission UI     ← no dependencies
│   └── 4.2: Peer review workflow     ← needs 4.1
│       └── 4.3: Contributor leaderboard  ← needs 4.1 + 4.2
│
│   (4.5 and 4.1 can run in parallel)

Batch C (depends on all implementation items)
├── 4.8: MITRE CTID partnership        ← needs 4.1-4.7 complete
├── 4.9: FS-ISAC presentation          ← needs 4.1-4.7 complete
├── 4.10: Comprehensive test suite     ← needs 4.1-4.7 complete
└── 4.11: Production documentation     ← needs 4.1-4.7 complete
```

**Critical path:** 4.1 -> 4.2 -> 4.3 (community infrastructure chain)

**Parallelism opportunities:**
- Batch A (4.6, 4.7) runs fully in parallel with Batch B
- Within Batch B, the 4.5 -> 4.4 chain runs in parallel with the 4.1 -> 4.2 -> 4.3 chain
- Within Batch C, all four items (4.8, 4.9, 4.10, 4.11) can run in parallel once Batch B is complete

---

## Success Metrics

| Metric | Current (v0.5) | Target (v1.0) |
|---|---|---|
| Threat Paths | 33 | 50+ |
| Detection Logic Rules | 67 | 150+ |
| GitHub Stars | TBD | 1,000 |
| Contributors | 1 | 25+ |
| Test Cases | 176 | 250+ |
| Emulation Playbooks | 0 | 5+ |
| API Endpoints | 106 | 106+ |
| Supported Frameworks | 4 | 4 |
| Regulatory Mappings | 15 | 15+ |
| Partnership Proposals | 0 | 2 (MITRE CTID, FS-ISAC) |

---

## Estimated Effort

| Batch | Items | Hours |
|---|---|---|
| A: Quick Wins | 4.6, 4.7 | 7-10 |
| B: Community Infrastructure | 4.1, 4.2, 4.3, 4.4, 4.5 | 40-54 |
| C: Partnerships & Hardening | 4.8, 4.9, 4.10, 4.11 | 24-33 |
| **Total** | **4.1-4.11** | **70-96** |

---

## Verification Strategy

After each batch:
- `python scripts/validate_submission.py` on all modified and new content files
- `python scripts/build_database.py` succeeds and produces valid outputs
- `python -m pytest tests/ -v` passes with zero failures
- Frontend: start dev server, verify new features render correctly, check browser console for errors

Final integration checks:
- RSS feed validates against RSS 2.0 XML schema
- Webhook notifications deliver to test channels for all three platforms
- Contributor submission flow works end-to-end: form -> issue -> review -> PR -> merge -> published
- Leaderboard reflects accurate contributor data from git history and frontmatter
- All 5 emulation playbooks validate against EP-XXXX schema
- All EP cross-references (TP-XXXX, DL-XXXX) resolve to existing content
- Test suite passes 250+ test cases
- Documentation covers all v1.0 features without stale references
