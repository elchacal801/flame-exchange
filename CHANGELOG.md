# Changelog

All notable changes to the FLAME project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.9.0] — 2026-03-20

### Added

- **Phase 7 SIGNAL: Multi-Source Intelligence Integration** — 5 external reports integrated: INTERPOL GFFTA 2026, UNODC Emerging Threats Sept 2025, Flare/IBM X-Force DPRK March 2026, Infoblox TDS/DNS Intelligence, Recorded Future CTA-2026-0319 Malicious Infrastructure Year-in-Review
- **TP-0057: Deepfake-as-a-Service Marketplace Ecosystem** — DaaS platforms on dark web/Telegram, 600% deepfake surge (UNODC), 10+ vendor ecosystem, voice clones from 10s audio, AI face/voice changers for DPRK interviews
- **TP-0058: Scam Compound Operational Infrastructure** — Boiler room mechanics, multilingual chatbots, $40B annual profits (UNODC), 80 nationalities trafficked (INTERPOL), scripted sextortion fallback, CRM-driven victim management
- **TP-0059: Automated Mule Account Infrastructure** — Bot-driven mule creation at scale, GAN liveness bypass, KYC circumvention, account aging simulation, automated transaction splitting
- **TP-0060: Investment Scam TDS Integrated Pipeline** — Named actors (Reckless Rabbit, Ruthless Rabbit, Savvy Seahorse), Keitaro/Binom TDS abuse, geo-routing evasion (US→eToro), 500K TDS domains/year, CNAME-as-TDS technique
- **TP-0061: Threat Activity Enabler (TAE) Bulletproof Hosting Infrastructure** — Named TAEs (Virtualine, CrazyRDP, Stark/THE.Hosting, Aeza), aurologic GmbH upstream concentration (70%), sanctions evasion via corporate rebranding, IP prefix transfers
- **9 new detection rules** (DL-0115 through DL-0123) — DaaS transaction patterns, real-time face/voice changer detection, multilingual chatbot scam patterns, automated mule account velocity, KYC bot circumvention, investment TDS geo-routing evasion, DPRK internal platform connection, Keitaro/Binom TDS abuse, TAE infrastructure rotation
- **3 new baselines** (BL-0028 through BL-0030) — deepfake service procurement norms, automated account opening velocity norms, investment TDS routing norms
- **5 new fraud types** in taxonomy: `deepfake-as-a-service`, `ai-face-voice-changer`, `automated-mule-infrastructure`, `chatbot-enabled-fraud`, `investment-tds-pipeline`
- **1 new infrastructure generation method**: `tds-routing`
- **6 new regulatory/intelligence references**: REG-INTERPOL-GFFTA, REG-INTERPOL-SHADOW-STORM, REG-INTERPOL-HAECHI, REG-INTERPOL-REDCARD, REG-UNODC-EMERGING-THREATS, REG-RF-CTA-2026-0319

### Changed

- **TP-0034** (DPRK IT Worker Fraud) — Major enrichment: RB Site/NetkeyRegister platforms, Western collaborator recruitment, OConnect/NetKey VPN, BeaverTail/InvisibleFerret malware, PurpleBravo/PurpleDelta infrastructure overlap, 100K+ operatives/$500M year (Flare/IBM, Recorded Future)
- **TP-0042** (TDS Chain Exploitation) — Added named actors (Reckless/Ruthless Rabbit, Savvy Seahorse), GrayCharlie/TAG-124 TDS actors, ClickFix technique, Keitaro/Binom platforms, 500K domains/year (Infoblox, Recorded Future)
- **TP-0041** (RDGA Infrastructure) — Added named actor RDGA patterns and wildcard DNS cloaking (Infoblox)
- **TP-0047** (Human Trafficking-Linked Fraud) — Added multilingual chatbots, sextortion fallback, 80 nationalities, MENA expansion, $18-37B/$40B loss estimates (INTERPOL, UNODC)
- **TP-0007** (Deepfake Voice Authorization) — Added DaaS ecosystem, 600% surge, 10+ vendors, voice clones from 10s audio (INTERPOL, UNODC)
- **TP-0039** (Agentic Commerce Fraud) — Added INTERPOL confirmation of autonomous AI campaign execution
- **TP-0052** (Sextortion-Investment Hybrid) — Added formalized sextortion in compound operating procedures (INTERPOL)
- **TP-0054** (Fraud-as-a-Service) — Added $442B losses, 4.5x AI profitability, MaaS/PhaaS professionalization, TAG-161 premium tooling, bulletproof hosting enablers (INTERPOL, UNODC, Recorded Future)
- **TP-0055** (Crypto Fraud–Terror/Narco Nexus) — Added terrorist financing via crypto in Africa (INTERPOL)
- **TP-0044** (State-Criminal Convergence) — Added TAE infrastructure as convergence mechanism, Stark/Aeza sanctions evasion, aurologic GmbH systemic enabler, Kaopu Cloud shared infra (INTERPOL, Recorded Future)
- **TP-0049** (Crypto Laundering Infrastructure) — Added AI-enabled laundering detection evasion (INTERPOL, UNODC)
- **TP-0017** (Pig Butchering) — Added $18-37B E/SE Asia losses, $40B annual compound profits (INTERPOL, UNODC)
- **REG-OFAC-SDN** — Added `deepfake-as-a-service` and `scam-compound-operations` to relevant fraud types
- `flame_taxonomy.json` — Added 5 new fraud types + 1 infrastructure method (total: 76 fraud types)
- `ThreatPaths/INDEX.md` — Updated all coverage tables for 61 TPs, 81 fraud types

### Source Intelligence

- INTERPOL: Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 ($442B global losses, FaaS proliferation, scam compound globalization)
- UNODC: Emerging Threats — AI & Automation in Cybercrime, September 2025 (600% deepfake surge, $40B compound profits, automated mule systems)
- Flare/IBM X-Force: Inside the North Korean Infiltrator Threat, March 2026 (RB Site, NetkeyRegister, 100K+ operatives, $500M/year)
- Infoblox: DNS Intelligence — Keitaro TDS & Investment Scams (Reckless/Ruthless Rabbit, Savvy Seahorse, 500K TDS domains)
- Recorded Future CTA-2026-0319: 2025 Malicious Infrastructure Year in Review, March 2026 (TAE ecosystem, DPRK malware families, sanctions evasion patterns, as-a-service professionalization)

---

## [0.8.0] — 2026-03-04

### Added

- **Phase 6 SIGNAL-LNRS: LexisNexis Risk Solutions Global State of Fraud 2026 Integration + BNPL Fraud**
- **TP-0040: BNPL Multi-Provider Fraud** — Synthetic stacking, ATO & friendly fraud across Klarna, Afterpay, Affirm, Clearpay, Zip; STYX marketplace; Klarna Method/Glitch; $3.2B synthetic exposure
- **DL-0087 through DL-0091**: 5 BNPL fraud detection rules (onboarding risk signals, multi-provider stacking, spending step-up bust-out, INR claim velocity, device clustering)
- **BL-0020**: BNPL Account & Transaction Patterns baseline
- `bnpl-fraud` fraud type added to taxonomy

### Changed

- **TP-0016** (First-Party Fraud) — Enhanced with LNRS 2026 scale data: 36% of all fraud ($3.9B losses), viral fraud cohorts, consortium intelligence uplift (43%)
- **TP-0024** (A2A Instant Payment) — Enhanced with mule laundering speed data: 30-min cycle, UK Banking Consortium results (£508M, 377K mule payments)
- **TP-0011** (Romance Scam Mule Pipeline) — Enhanced with mule network operational scale: 15 avg mules, 3.4 banks, £10B UK annual volume, Gen Z recruitment stats
- **TP-0003** (Synthetic Identity Bust-Out) — Enhanced with synthetic identity projections: $23B by 2030, 85% GenAI involvement, thin-file exploitation
- **TP-0029** (AI Synthetic Identity & Document Forgery) — Enhanced with AI arms race data: 20% deepfake detection rate, 57% AI-generated forgeries, $20M Brazilian deepfake scam
- `flame_taxonomy.json` — Added 1 new fraud type (total: 71)
- `ThreatPaths/INDEX.md` — Updated all coverage tables for 40 TPs, 60 fraud types

### Source Intelligence

- LexisNexis Risk Solutions: Global State of Fraud and Identity Report 2026
- Supplementary BNPL fraud research (Experian, ACI Worldwide, MRC, CFPB, FCA, ASIC, Resecurity, SEON, Fingerprint.com, DataVisor)

---

## [0.7.0] — 2026-03-04

### Added

- **Phase 5 SIGNAL: Recorded Future Payment Fraud Report 2025 Integration** — 5 new threat paths sourced from the Recorded Future Annual Payment Fraud Intelligence Report 2025, covering major 2025 fraud themes absent from FLAME
- **TP-0035: Magecart E-Skimmer Data Compromise** — MaaS kits (Sniffer by Fleras, AcceptCar), blockchain smart contract C2, 10,500+ infections compromising 23.4M transactions
- **TP-0036: Purchase Scam Merchant Networks** — 3,600+ scam merchant accounts, victim-authorized fraud, subscription traps, AI-powered ad targeting across 40+ countries
- **TP-0037: Digital Wallet Fraud & NFC Relay Attacks** — OTP interception to wallet provisioning to "ghost tapping" contactless fraud, SuperCardX MaaS, 7 dark web tool offerings documented
- **TP-0038: Card Testing Infrastructure Abuse** — 1,350+ tester merchants (94% new), 27M card records via Telegram, BIN enumeration attacks
- **TP-0039: Agentic Commerce Fraud** — AI agent intent spoofing, Amazon Buy for Me / Visa Intelligent Commerce / Mastercard Agent Pay attack surface, open banking structural parallel
- **12 new detection rules** (DL-0075 through DL-0086) — e-skimmer script injection, blockchain C2 exfiltration, checkout page modification, scam merchant velocity, subscription trap, wallet provisioning anomaly, NFC relay geographic anomaly, ghost-tap velocity, card testing micro-authorization, BIN enumeration, agent intent manipulation, agent velocity anomaly
- **5 new baselines** (BL-0015 through BL-0019) — e-commerce payment page integrity, merchant account transaction patterns, digital wallet contactless activity, card authorization velocity, AI agent commerce activity
- **4 new fraud types** in taxonomy: `card-testing`, `digital-wallet-fraud`, `e-skimmer`, `purchase-scam`

### Changed

- **TP-0008** (SIM Swap) — Enhanced with OTP interception techniques beyond SIM swap (EvilginX, PhantomOS, xl-hook RAT, SS7 exploitation); added TP-0037 cross-reference
- **TP-0009** (Check Fraud) — Enhanced with deurbanization and Midwest geographic shift intelligence from Recorded Future 2025
- **TP-0030** (E-Commerce Triangulation) — Enhanced with purchase scam ecosystem convergence analysis; added TP-0035, TP-0036, TP-0038 cross-references
- `flame_taxonomy.json` — Added 4 new fraud types (total: 70)
- `ThreatPaths/INDEX.md` — Updated all coverage tables for 39 TPs, 56 fraud types, 18 sectors

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
