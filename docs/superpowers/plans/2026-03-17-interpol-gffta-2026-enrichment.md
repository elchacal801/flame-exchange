# INTERPOL GFFTA 2026 — FLAME Enrichment Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the INTERPOL Global Financial Fraud Threat Assessment (2nd Edition, March 2026) into FLAME — 6 new TPs, 4 new fraud types, and enrichment of 8 existing TPs.

**Architecture:** Markdown-first content authoring in `ThreatPaths/` with YAML frontmatter, taxonomy updates in `data/flame_taxonomy.json`, then `scripts/build_database.py` regenerates all derived artifacts (SQLite, JSON APIs, search index, stats, INDEX.md).

**Tech Stack:** Markdown + YAML frontmatter, Python build pipeline, JSON static API

**Spec:** `docs/superpowers/specs/2026-03-17-interpol-gffta-2026-enrichment-design.md`

**Source:** `docs/docs_internal/INTERPOL_Global_Financial_Fraud_Threat_Assessment_2026.md`

---

## Chunk 1: Taxonomy and New Threat Paths

### Task 1: Add 4 new fraud types to taxonomy

**Files:**
- Modify: `data/flame_taxonomy.json` (fraud_types array — alphabetically sorted)

- [ ] **Step 1: Add new fraud types**

Insert these 4 entries into the `fraud_types` array in alphabetical position:

- `fraud-as-a-service` — between `first-party-fraud` and `fraudulent-claim`
- `quishing` — between `purchase-scam` and `rdga-infrastructure`
- `sextortion` — between `scam-compound-operations` and `social-engineering`
- `vehicle-export-fraud` — between `upcoding` and `vendor-impersonation`

- [ ] **Step 2: Verify taxonomy is valid JSON**

Run: `python -c "import json; json.load(open('data/flame_taxonomy.json')); print('Valid JSON')"`
Expected: `Valid JSON`

- [ ] **Step 3: Commit**

```bash
git add data/flame_taxonomy.json
git commit -m "feat: add 4 new fraud types from INTERPOL GFFTA 2026

Add quishing, sextortion, vehicle-export-fraud, fraud-as-a-service
to the FLAME taxonomy based on INTERPOL Global Financial Fraud
Threat Assessment (2nd Edition, March 2026)."
```

---

### Task 2: Create TP-0051 — QR Code Payment Fraud / Quishing

**Files:**
- Create: `ThreatPaths/TP-0051-qr-code-payment-fraud-quishing.md`

- [ ] **Step 1: Create the threat path markdown file**

Use TP-0050 as the structural template. The file must include:

**Frontmatter** (code-fenced YAML block):
```yaml
---
id: TP-0051
title: "QR Code Payment Fraud / Quishing"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - quishing
  - credential-stuffing
  - account-takeover
  - social-engineering
sector:
  - banking
  - payments
  - retail
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 82
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1566.002  # Phishing: Spearphishing Link
  - T1204.001  # User Execution: Malicious Link
  - T1056.003  # Input Capture: Web Portal Capture
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FTA009", "FT016"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0012
    relationship: related-to
  - id: TP-0037
    relationship: related-to
  - id: TP-0050
    relationship: enhances
regulatory_refs:
  - REG-CFPB-REGE
  - REG-UK-PSR-APP
  - REG-PSD3-SCA
geopolitical_timing: none
nation_state_nexus: none
tags:
  - qr-code-fraud
  - quishing
  - credential-harvesting
  - fake-bank-login
  - marketplace-fraud
  - 2fa-bypass
  - mobile-money
  - post-office-impersonation
---
```

**Required body sections** (following TP-0050 structure exactly):

1. **Summary** — QR code payment fraud where fraudsters impersonate buyers on online marketplaces, move conversation to messaging apps, send fake QR codes claiming payment at post office, leading to credential harvest via fake bank login pages. INTERPOL documented a European case where over USD 110,000 was stolen. After credential capture, fraudsters add a new 2FA device to block victim notifications and drain funds via mobile money transfer.

2. **Threat Path Hypothesis** — Actors exploit consumer trust in QR codes (normalized by COVID-era contactless payments) to redirect victims to credential-harvesting pages that impersonate legitimate banking or postal service portals. The attack chain moves off-platform quickly to avoid marketplace fraud detection.
   - Confidence: Medium-High (82)
   - Estimated Impact: USD 5,000–110,000+ per victim

3. **CFPF Phase Mapping** (P1 through P5) — table format with Technique, Description, Indicators columns:
   - P1: Target identification on marketplace platforms; infrastructure setup (fake bank/post office pages, local phone numbers)
   - P2: Initial contact as buyer; conversation migration to messaging app; QR code delivery
   - P3: Fake QR code leads to fraudulent website impersonating post office; "Receive Money" button + bank selection redirect
   - P4: Credential capture on fake bank login; 2FA device enrollment to block victim; fund transfer initiation
   - P5: Funds drained via mobile money transfer; possible further account exploitation

4. **Cross-Framework Mapping** — FT3, MITRE ATT&CK, Group-IB Fraud Matrix (same format as TP-0050)

5. **Look Left / Look Right Analysis** — Discovery at P3/P4. Look Left: marketplace off-platform conversation patterns, fake website registration. Look Right: additional account compromise, credential resale.

6. **Controls & Mitigations** — table with Phase, Control, Type, Owner columns. Include: marketplace monitoring for off-platform conversation migration, QR code URL validation, 2FA device enrollment alerts, mobile money velocity checks.

7. **UCFF Alignment** — table format matching the frontmatter ucff_domains values

8. **Detection Approaches** — Include:
   - QR code URL destination analysis (domain age, reputation)
   - New 2FA device enrollment within minutes of credential entry
   - Mobile money transfer velocity post-authentication
   - Off-platform conversation migration patterns on marketplace

9. **References** — Cite INTERPOL GFFTA 2026 (European member country report). Include page/section reference.

10. **Analyst Notes** — Key differentiator: QR codes bypass URL preview that email/SMS links provide. Victims cannot inspect the destination before scanning. The post-office/bank impersonation chain is highly localized (language, institution). Cross-reference TP-0037 (digital wallet/NFC) for mobile payment vector overlap.

11. **Revision History** — table: 2026-03-17 | FLAME Project | Initial submission

- [ ] **Step 2: Verify frontmatter parses**

Run: `python -c "
import yaml, re
text = open('ThreatPaths/TP-0051-qr-code-payment-fraud-quishing.md').read()
m = re.search(r'\x60\x60\x60yaml\s*\n---\n(.*?)\n---\s*\n\x60\x60\x60', text, re.DOTALL)
data = yaml.safe_load(m.group(1))
print(f'ID: {data[\"id\"]}, Title: {data[\"title\"]}, Phases: {data[\"cfpf_phases\"]}')
"`
Expected: `ID: TP-0051, Title: QR Code Payment Fraud / Quishing, Phases: ['P1', 'P2', 'P3', 'P4', 'P5']`

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0051-qr-code-payment-fraud-quishing.md
git commit -m "feat: add TP-0051 QR Code Payment Fraud / Quishing

New threat path based on INTERPOL GFFTA 2026 European member
country report. Documents quishing kill chain from marketplace
contact through QR-based credential harvest to mobile money drain."
```

---

### Task 3: Create TP-0052 — Sextortion-Investment Hybrid Fraud

**Files:**
- Create: `ThreatPaths/TP-0052-sextortion-investment-hybrid.md`

- [ ] **Step 1: Create the threat path markdown file**

**Frontmatter**:
```yaml
---
id: TP-0052
title: "Sextortion-Investment Hybrid Fraud"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - sextortion
  - investment-scam
  - deepfake
  - social-engineering
  - romance-scam
sector:
  - banking
  - crypto
  - investment
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 78
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1566.003  # Phishing: Spearphishing via Service
  - T1589.001  # Gather Victim Identity: Credentials
  - T1656       # Impersonation
  - T1657       # Financial Theft
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FT016"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Social Engineering"
  - "Resource Development"
  - "Initial Access"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0011
    relationship: related-to
  - id: TP-0017
    relationship: enhances
  - id: TP-0025
    relationship: enhances
  - id: TP-0026
    relationship: enhances
regulatory_refs:
  - REG-CFPB-REGE
  - REG-FINCEN-AML
geopolitical_timing: none
nation_state_nexus: none
tags:
  - sextortion
  - investment-fraud
  - deepfake-imagery
  - romance-baiting
  - hybrid-fraud
  - crypto-laundering
  - teen-targeting
  - executive-targeting
---
```

**Required body sections** — same structure as Task 2. Key content:

1. **Summary** — Hybrid scheme combining deepfake sextortion with investment fraud. INTERPOL reports three regional variants: Americas (targeting teens 14-17), Asia-Pacific (hybrid investment-sextortion with deepfakes), Latin America (targeting business executives with high ransom demands in crypto). The attack pivots from blackmail to "investment opportunity" to recover losses, funneling victims into fraudulent crypto platforms.

2. **Threat Path Hypothesis** — Actors leverage AI-generated intimate imagery or coerced image sharing to create blackmail leverage, then pivot the relationship to investment fraud. The sextortion phase creates urgency and shame that suppresses reporting, while the investment pivot extracts additional funds under the guise of "recovery."
   - Confidence: Medium-High (78)
   - Estimated Impact: USD 5,000–500,000+ per victim (executive variant significantly higher)

3. **CFPF Phase Mapping**:
   - P1: Target identification via social media; AI deepfake tooling setup; fake crypto platform infrastructure
   - P2: Social media grooming via dating apps or social platforms; relationship building
   - P3: Escalation to intimate content exchange or deepfake generation; blackmail leverage established
   - P4: Blackmail demand (crypto payment); pivot to "investment opportunity" to recover/earn money; deposits into fraudulent platform
   - P5: Crypto laundering through mixing services; platform disappears; possible re-victimization cycle

4. **Detection Approaches**: Account age vs transaction velocity anomalies; crypto deposit patterns following new social media connections; rapid escalation from small to large deposits on investment platforms; victim demographic patterns (teen accounts, executive accounts with unusual crypto activity)

5. **References**: INTERPOL GFFTA 2026 — sections on hybrid fraud tactics, sextortion trends (Americas, Asia-Pacific, Latin America). FBI IC3 sextortion advisories.

6. **Analyst Notes**: The hybrid nature makes this scheme difficult to categorize for SAR/BSA reporting — recommend dual categorization under both extortion and investment fraud. The teen-targeting variant raises significant safeguarding concerns beyond financial loss. Cross-reference TP-0017 (pig butchering) for the investment fraud mechanics and TP-0025/TP-0026 for GenAI-enhanced variants.

- [ ] **Step 2: Verify frontmatter parses** (same verification pattern as Task 2)

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0052-sextortion-investment-hybrid.md
git commit -m "feat: add TP-0052 Sextortion-Investment Hybrid Fraud

New threat path based on INTERPOL GFFTA 2026 multi-regional
reporting. Documents hybrid sextortion-to-investment fraud
kill chain with three regional variants (teen, executive, general)."
```

---

### Task 4: Create TP-0053 — Vehicle Export Financing Fraud

**Files:**
- Create: `ThreatPaths/TP-0053-vehicle-export-financing-fraud.md`

- [ ] **Step 1: Create the threat path markdown file**

**Frontmatter**:
```yaml
---
id: TP-0053
title: "Vehicle Export Financing Fraud"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - vehicle-export-fraud
  - identity-theft
  - application-fraud
  - loan-fraud
sector:
  - banking
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 80
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1589.001  # Gather Victim Identity: Credentials
  - T1586.002  # Compromise Accounts: Email Accounts
  - T1656       # Impersonation
  - T1657       # Financial Theft
ft3_tactics: ["FTA001", "FTA003", "FTA004"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Social Engineering"
  - "Initial Access"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0018
    relationship: related-to
  - id: TP-0019
    relationship: related-to
  - id: TP-0029
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-AML
  - REG-CFPB-REGE
geopolitical_timing: none
nation_state_nexus: none
tags:
  - vehicle-fraud
  - straw-buyer
  - auto-lending
  - export-fraud
  - cross-border
  - identity-theft
  - forged-documents
  - loan-default
---
```

**Required body sections** — Key content:

1. **Summary** — Transnational fraud scheme first detected in North America in early 2024. Criminal networks use identity theft and "straw buyers" to obtain financed vehicles from car dealerships, then export them overseas before lenders can detect fraud. Perpetrators submit forged employment records and falsified income statements, making minimal initial payments to establish credibility before defaulting after export. INTERPOL notes the scheme exploits delays between loan default and fraud detection, and is spreading to other regions.

2. **CFPF Phase Mapping**:
   - P1: Recruit straw buyers; acquire stolen/synthetic identities; identify target dealerships with lax verification
   - P2: Submit fraudulent loan applications with forged employment/income documentation
   - P3: Make minimal initial payments to establish credibility; prepare export logistics
   - P4: Take possession of vehicles; arrange cross-border export before default window
   - P5: Vehicles sold overseas; loan defaults with unrecoverable losses for lenders

3. **Detection Approaches**: Loan application velocity by identity cluster; employment/income verification failures; vehicle GPS tracking discontinuity at borders; loan-to-first-default timing anomalies; cross-border shipping records correlated with recent auto loans.

4. **Analyst Notes**: The critical detection window is between vehicle delivery and export — typically days, not weeks. By the time vehicles are flagged as stolen, they have often bypassed national databases, making them untraceable in INTERPOL's systems. Recommend integration with customs/border protection data feeds for real-time cross-referencing. This TP has no direct MITRE ATT&CK cyber equivalents for the physical export phase — the mapping covers only the identity theft and application fraud components.

- [ ] **Step 2: Verify frontmatter parses**

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0053-vehicle-export-financing-fraud.md
git commit -m "feat: add TP-0053 Vehicle Export Financing Fraud

New threat path based on INTERPOL GFFTA 2026 Americas region
report. Documents straw buyer vehicle financing and cross-border
export scheme exploiting loan-to-default detection gaps."
```

---

### Task 5: Create TP-0054 — Fraud-as-a-Service (FaaS) Platforms

**Files:**
- Create: `ThreatPaths/TP-0054-fraud-as-a-service-platforms.md`

- [ ] **Step 1: Create the threat path markdown file**

**Frontmatter**:
```yaml
---
id: TP-0054
title: "Fraud-as-a-Service (FaaS) Platforms"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: ai-assisted
fraud_types:
  - fraud-as-a-service
  - ai-accelerated-fraud-infrastructure
  - phishing
  - brand-impersonation
sector:
  - cross-sector
  - banking
  - payments
  - crypto
  - technology
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 75
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1583.001  # Acquire Infrastructure: Domains
  - T1583.003  # Acquire Infrastructure: Virtual Private Server
  - T1588.002  # Obtain Capabilities: Tool
  - T1566.001  # Phishing: Spearphishing Attachment
  - T1566.002  # Phishing: Spearphishing Link
ft3_tactics: ["FTA001", "FTA009", "FTA010", "FT016"]
mitre_f3: []
groupib_stages:
  - "Resource Development"
  - "Initial Access"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
related_tps:
  - id: TP-0043
    relationship: enhances
  - id: TP-0041
    relationship: shares-infrastructure
  - id: TP-0042
    relationship: shares-infrastructure
regulatory_refs:
  - REG-CFPB-REGE
  - REG-DORA
  - REG-FINCEN-AML
geopolitical_timing: none
nation_state_nexus: none
tags:
  - fraud-as-a-service
  - faas
  - genai-fraud
  - phishing-kits
  - fake-payment-gateways
  - deepfake-tools
  - bot-testimonials
  - affiliate-fraud
  - democratized-fraud
---
```

**Required body sections** — Key content:

1. **Summary** — GenAI-powered "Fraud-as-a-Service" platforms that provide subscription-based access to professional-grade fraud toolkits. INTERPOL reports these platforms offer automated phishing websites, fake payment gateways, deepfake generation tools, and bot-generated fake testimonials. Low-skill actors can now launch sophisticated BEC and phishing campaigns with minimal effort. The FaaS model operates on an affiliate structure where proceeds are split between platform operators and campaign operators. **Distinction from TP-0043**: TP-0043 covers AI-accelerated *generation* of fraud infrastructure; TP-0054 covers the *marketplace/subscription model* that packages and democratizes access to these tools.

2. **CFPF Phase Mapping**:
   - P1: FaaS operator develops platform; integrates GenAI tools for phishing kit generation, deepfake creation, payment gateway cloning
   - P2: Affiliate purchases subscription; selects campaign type (BEC, phishing, investment scam); receives turnkey toolkit
   - P3: Affiliate customizes templates; deploys infrastructure using FaaS-provided hosting and domains
   - P4: Campaign execution — automated phishing, fake payment capture, deepfake-enhanced social engineering
   - P5: Proceeds collected via crypto or money mules; revenue share between operator and affiliate

3. **Detection Approaches**: Shared infrastructure fingerprints across seemingly unrelated campaigns; template/kit reuse patterns (CSS fingerprinting, JavaScript similarity, page structure); payment gateway clone detection; identical phishing page deployments across multiple domains; affiliate payout patterns in crypto.

4. **Analyst Notes**: FaaS represents a structural shift — the barrier to entry for sophisticated fraud has dropped dramatically. Previously, BEC and phishing required technical skill; now GenAI-powered platforms abstract that away. Detection strategies must evolve from individual campaign analysis to platform-level infrastructure fingerprinting. The shared tooling creates a detection advantage: identify one campaign's infrastructure signatures and you can map the entire FaaS platform's affiliate network.

- [ ] **Step 2: Verify frontmatter parses**

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0054-fraud-as-a-service-platforms.md
git commit -m "feat: add TP-0054 Fraud-as-a-Service (FaaS) Platforms

New threat path based on INTERPOL GFFTA 2026 AI enablement
reporting. Documents GenAI-powered FaaS marketplace model that
democratizes access to professional-grade fraud toolkits."
```

---

### Task 6: Create TP-0055 — Crypto Fraud-Terrorism/Narco Financing Nexus

**Files:**
- Create: `ThreatPaths/TP-0055-crypto-fraud-narco-terror-nexus.md`

- [ ] **Step 1: Create the threat path markdown file**

**Frontmatter**:
```yaml
---
id: TP-0055
title: "Crypto Fraud–Terrorism/Narco Financing Nexus"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - crypto-laundering
  - investment-scam
  - state-criminal-convergence
  - money-mule
sector:
  - crypto
  - banking
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 78
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1657       # Financial Theft
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FTA003", "FTA007"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Social Engineering"
  - "Initial Access"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0044
    relationship: enhances
  - id: TP-0045
    relationship: related-to
  - id: TP-0049
    relationship: shares-infrastructure
regulatory_refs:
  - REG-FINCEN-AML
  - REG-FATF-R16
geopolitical_timing: none
nation_state_nexus: suspected
tags:
  - crypto-fraud
  - narco-financing
  - terrorism-financing
  - ponzi-scheme
  - tren-de-aragua
  - crypto-mixing
  - cross-border-laundering
  - organized-crime-convergence
---
```

**Required body sections** — Key content:

1. **Summary** — Criminal syndicates traditionally linked to drug trafficking and organized crime are establishing cryptocurrency Ponzi and investment schemes to launder proceeds and fund further operations. INTERPOL documents a Tren de Aragua-linked USD 150 million cryptocurrency fraud scheme used to launder proceeds from drug trafficking and extortion across Chile, Colombia, Venezuela, and the Iberian Peninsula. This represents a convergence of financial fraud and traditional organized crime where fraud is no longer ancillary but a primary revenue stream for narco-terror organizations.

2. **CFPF Phase Mapping**:
   - P1: Syndicate identifies crypto as laundering vehicle; establishes fraudulent investment platform or Ponzi scheme; recruits technical operators
   - P2: Victim recruitment via social media, community networks; promises of high crypto returns
   - P3: Initial small returns paid to build trust (Ponzi mechanics); victims encouraged to recruit others and increase deposits
   - P4: Large deposits collected; funds routed through crypto mixing services; cross-border transfers to shell entities
   - P5: Cleaned proceeds fund drug trafficking, extortion, arms procurement; platform eventually collapses or disappears

3. **Detection Approaches**: Ponzi structure indicators (returns funded by new deposits, not investment gains); crypto mixer usage patterns; geographic clustering analysis (investor deposit locations vs. withdrawal destinations); convergence indicators between fraud proceeds and wallets associated with known narco/terror entities; unusual cross-jurisdiction fund flows between Latin America and Iberian Peninsula.

4. **Analyst Notes**: This TP requires elevated SAR/BSA treatment — dual filing under both fraud and terrorism/narco financing categories. The Tren de Aragua case demonstrates that traditional narco syndicates are adopting fraud as a core competency, not just a sideline. AML teams should cross-reference crypto fraud reports with OFAC SDN lists and FinCEN advisories on Venezuelan criminal organizations. The `nation_state_nexus: suspected` reflects the involvement of organizations with alleged state protection in origin countries.

- [ ] **Step 2: Verify frontmatter parses**

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0055-crypto-fraud-narco-terror-nexus.md
git commit -m "feat: add TP-0055 Crypto Fraud-Narco/Terror Financing Nexus

New threat path based on INTERPOL GFFTA 2026 Americas organized
crime reporting. Documents narco-syndicate crypto Ponzi schemes
with Tren de Aragua USD 150M case study."
```

---

### Task 7: Create TP-0056 — Insurance Claims Fraud (Motor/Medical)

**Files:**
- Create: `ThreatPaths/TP-0056-insurance-claims-fraud.md`

- [ ] **Step 1: Create the threat path markdown file**

**Frontmatter**:
```yaml
---
id: TP-0056
title: "Insurance Claims Fraud (Motor/Medical)"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 / FLAME gap analysis"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - insurance-fraud
  - fraudulent-claim
  - identity-theft
  - documentary-fraud
sector:
  - insurance
  - healthcare
  - banking
  - government
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 72
source_reliability: C
info_credibility: 3
mitre_attack:
  - T1589.001  # Gather Victim Identity: Credentials
  - T1656       # Impersonation
ft3_tactics: ["FTA003", "FTA004"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Social Engineering"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0005
    relationship: related-to
  - id: TP-0010
    relationship: related-to
  - id: TP-0018
    relationship: related-to
  - id: TP-0028
    relationship: related-to
regulatory_refs:
  - REG-CFPB-REGE
  - REG-FINCEN-AML
geopolitical_timing: none
nation_state_nexus: none
tags:
  - insurance-fraud
  - motor-fraud
  - medical-fraud
  - staged-accident
  - false-claims
  - forged-documentation
  - policy-identity-theft
---
```

**Required body sections** — Key content:

1. **Summary** — Motor and medical insurance claims fraud involving staged accidents, fabricated medical events, and forged documentation. Perpetrators file fraudulent claims with insurers, often using stolen identities to submit claims under others' policies. This TP fills a gap in FLAME — existing insurance TPs cover premium diversion (TP-0005) and disability fraud (TP-0010) but not the core motor/medical false claims pattern that represents the highest-volume insurance fraud globally.

2. **CFPF Phase Mapping**:
   - P1: Identify target insurance companies with weak claims verification; acquire stolen identities and policy information; recruit accomplices for staged events
   - P2: Establish relationship with target insurer (purchase policy or access existing via stolen identity)
   - P3: Stage accident or fabricate medical event; obtain or forge supporting documentation (police reports, medical records, witness statements)
   - P4: File fraudulent claim; provide forged documentation to claims adjuster; manage investigator interactions
   - P5: Claim payout received via diverted payment channels; proceeds distributed among fraud ring members

3. **Detection Approaches**: Claims frequency analysis per provider/patient/vehicle; provider network graph anomalies; document authenticity verification (metadata analysis, template matching); staged accident pattern recognition (low-speed impacts, recurring participants, geographic clustering); cross-insurer claim correlation.

4. **Analyst Notes**: Insurance claims fraud is the highest-volume insurance fraud type globally but has been underrepresented in FLAME. Unlike premium diversion (TP-0005) or disability fraud (TP-0010), this TP covers the full false claims lifecycle. Organizations at UCFF Level 2 should prioritize claims analytics and cross-insurer data sharing. The government sector inclusion reflects that Medicare/Medicaid fraud follows the same pattern (see TP-0028 for the DME-specific variant).

- [ ] **Step 2: Verify frontmatter parses**

- [ ] **Step 3: Commit**

```bash
git add ThreatPaths/TP-0056-insurance-claims-fraud.md
git commit -m "feat: add TP-0056 Insurance Claims Fraud (Motor/Medical)

New threat path filling FLAME insurance coverage gap.
Documents staged accident and false claims kill chain
with motor and medical variants."
```

---

## Chunk 2: Existing TP Enrichments

### Task 8: Enrich TP-0007 — Deepfake Voice Authorization

**Files:**
- Modify: `ThreatPaths/TP-0007-deepfake-voice-wire-authorization.md`

- [ ] **Step 1: Add INTERPOL intelligence to References section**

Add to the `## References` section:

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents deepfake audio CEO/CFO impersonation during live BEC calls across Asia-Pacific region; notes FaaS platforms now offering deepfake voice generation tools
```

- [ ] **Step 2: Add INTERPOL intelligence to Analyst Notes section**

Add a new paragraph to `## Analyst Notes`:

```markdown
**INTERPOL 2026 Update**: The INTERPOL GFFTA 2026 confirms that BEC fraud across Asia-Pacific has evolved to include real-time deepfake audio impersonation of CEOs and CFOs during live phone calls, bypassing traditional voice-based verification protocols. This represents an escalation from pre-recorded deepfake audio to interactive, real-time voice synthesis. Fraud-as-a-Service platforms (TP-0054) are now offering deepfake voice generation as a subscription service, lowering the barrier to entry for this attack vector.
```

- [ ] **Step 3: Update Revision History table**

Add row: `| 2026-03-17 | FLAME Project | INTERPOL GFFTA 2026 enrichment — Asia-Pacific deepfake BEC intelligence |`

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0007-deepfake-voice-wire-authorization.md
git commit -m "enrich: TP-0007 with INTERPOL GFFTA 2026 deepfake BEC intelligence"
```

---

### Task 9: Enrich TP-0011 — Romance Scam to Money Mule Pipeline

**Files:**
- Modify: `ThreatPaths/TP-0011-romance-scam-mule-pipeline.md`

- [ ] **Step 1: Add to References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents MENA region victims coerced into money mule roles via investment fraud schemes; European re-victimization patterns where fraud victims are recruited as mules through "recovery" scams
```

- [ ] **Step 2: Add to Analyst Notes section**

```markdown
**INTERPOL 2026 Update — MENA and European Patterns**: INTERPOL reports that in the MENA region, investment fraud victims are being coerced into acting as money mules, allowing their bank accounts to serve as transit hubs for funds stolen from other victims. This represents a convergence of investment fraud and mule recruitment that differs from the traditional romance-to-mule pipeline. In Europe, INTERPOL documents re-victimization patterns where initial fraud victims are subsequently recruited as mules through fraudsters posing as "recovery agents" or law enforcement — a secondary exploitation cycle that extends the mule pipeline beyond the romance vector.
```

- [ ] **Step 3: Update Revision History**

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0011-romance-scam-mule-pipeline.md
git commit -m "enrich: TP-0011 with INTERPOL GFFTA 2026 MENA/European mule patterns"
```

---

### Task 10: Enrich TP-0012 — APP Fraud Tech Support Impersonation

**Files:**
- Modify: `ThreatPaths/TP-0012-app-fraud-tech-support-impersonation.md`

- [ ] **Step 1: Add to References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents evolution of impersonation fraud from remote calls to physical theft in Eastern Asia (doorstep cash collection by accomplices); reports surge in "grandparent scams" / "shock calls" across Caribbean and Europe involving fabricated family emergencies
```

- [ ] **Step 2: Add to Analyst Notes section**

```markdown
**INTERPOL 2026 Update — Physical Impersonation Evolution**: INTERPOL has documented a significant shift in impersonation fraud in Eastern Asia: criminals posing as law enforcement or bank representatives now instruct victims to leave cash at their doorsteps, where physical accomplices collect it. This bridges virtual deception and real-world crime, creating a hybrid threat that requires coordination between cyber fraud and physical security teams. Additionally, "grandparent scams" (fabricated family emergencies demanding immediate payment) have surged across the Caribbean and Europe, exploiting emotional vulnerability rather than technical sophistication. These variants expand the TP-0012 threat surface beyond tech support impersonation to broader authority/family impersonation vectors.
```

- [ ] **Step 3: Update Revision History**

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0012-app-fraud-tech-support-impersonation.md
git commit -m "enrich: TP-0012 with INTERPOL GFFTA 2026 physical impersonation and grandparent scam intelligence"
```

---

### Task 11: Enrich TP-0017 — Pig Butchering

**Files:**
- Modify: `ThreatPaths/TP-0017-pig-butchering.md`

- [ ] **Step 1: Add to References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — reports investment fraud as the most financially damaging fraud type globally; documents hybrid investment-sextortion schemes using deepfakes; notes AI-generated dashboards showing fabricated returns
- FBI Internet Crime Complaint Center (IC3), *2024 Internet Crime Report*, April 2025 — USD 5.6 billion in investment fraud losses reported in the United States alone (2023)
```

- [ ] **Step 2: Add to Analyst Notes section**

```markdown
**INTERPOL 2026 Update — Scale and Evolution**: The INTERPOL GFFTA 2026 confirms investment fraud (including pig butchering) as the costliest fraud type globally. FBI IC3 data shows USD 5.6 billion in US investment fraud losses in 2023 alone. Key evolutions: (1) AI-generated dashboards now show victims fabricated portfolio returns, making the deception harder to detect; (2) hybrid investment-sextortion schemes use deepfakes to blackmail victims who attempt to withdraw, adding a coercion layer to the pig butchering model (see TP-0052); (3) fraudsters tailor pitches to exploit religious, ethnic, or national identities in victims' native languages, indicating sophisticated audience segmentation. Defrauded funds are frequently laundered through cryptocurrencies across Southeast Asia, South Asia, MENA, Europe, and Africa.
```

- [ ] **Step 3: Update Revision History**

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0017-pig-butchering.md
git commit -m "enrich: TP-0017 with INTERPOL GFFTA 2026 investment fraud scale and AI dashboard intelligence"
```

---

### Task 12: Enrich TP-0025 and TP-0026 — GenAI APP Fraud variants

**Files:**
- Modify: `ThreatPaths/TP-0025-genai-app-fraud-romance.md`
- Modify: `ThreatPaths/TP-0026-genai-app-fraud-investment.md`

- [ ] **Step 1: Add to TP-0025 References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents Fraud-as-a-Service platforms powered by generative AI and LLMs enabling widespread adoption of cybercrime; platforms provide automated phishing websites, fake payment gateways, and bot-generated fake testimonials
```

- [ ] **Step 2: Add to TP-0025 Analyst Notes section**

```markdown
**INTERPOL 2026 Update — FaaS Enablement**: INTERPOL confirms that "Fraud-as-a-Service" platforms powered by generative AI and large language models have enabled low-skill actors to launch professional-grade romance-variant APP campaigns with minimal effort. These platforms provide ready-made tools including automated phishing websites, fake payment gateways, and bot-generated fake testimonials that mimic legitimate communications. See TP-0054 for the full FaaS platform threat path. The democratization of these tools means that romance APP campaigns are no longer limited to sophisticated criminal organizations — individual actors with subscription access can now execute campaigns previously requiring teams.
```

- [ ] **Step 3: Update TP-0025 Revision History**

- [ ] **Step 4: Add to TP-0026 References section**

Same INTERPOL reference as Step 1.

- [ ] **Step 5: Add to TP-0026 Analyst Notes section**

```markdown
**INTERPOL 2026 Update — FaaS Enablement**: INTERPOL reports that Fraud-as-a-Service platforms now provide investment-variant APP campaign toolkits including AI-generated crypto trading dashboards, fake exchange interfaces with manipulated return displays, and bot-generated testimonials from fake "successful investors." These platforms (see TP-0054) have enabled an explosion of investment fraud campaigns across Asia-Pacific and Europe, with criminals promoting deceptive platforms offering unrealistic returns on cryptocurrencies, renewable energy, or luxury assets. The FaaS model enables campaign operators to focus on victim engagement while the platform handles infrastructure.
```

- [ ] **Step 6: Update TP-0026 Revision History**

- [ ] **Step 7: Commit both files**

```bash
git add ThreatPaths/TP-0025-genai-app-fraud-romance.md ThreatPaths/TP-0026-genai-app-fraud-investment.md
git commit -m "enrich: TP-0025 and TP-0026 with INTERPOL GFFTA 2026 FaaS platform intelligence"
```

---

### Task 13: Enrich TP-0044 — State-Criminal Infrastructure Convergence

**Files:**
- Modify: `ThreatPaths/TP-0044-state-criminal-infrastructure-convergence.md`

- [ ] **Step 1: Add to References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents arrest of suspect linked to Tren de Aragua in connection with USD 150 million cryptocurrency fraud scheme used to launder proceeds from drug trafficking and extortion across Chile, Colombia, Venezuela and the Iberian Peninsula; highlights convergence of financial fraud and organized crime in South America
```

- [ ] **Step 2: Add to Analyst Notes section**

```markdown
**INTERPOL 2026 Update — South American Narco-Fraud Convergence**: INTERPOL documents a significant case: a suspect with alleged links to Tren de Aragua was arrested in connection with a USD 150 million cryptocurrency fraud scheme used to launder drug trafficking and extortion proceeds across Chile, Colombia, Venezuela, and the Iberian Peninsula. This represents a concrete instance of state-criminal convergence where South American crime syndicates — traditionally linked to drug trafficking, arms trafficking, and money laundering — are now actively operating financial fraud as a primary revenue stream, not merely using fraud infrastructure incidentally. See TP-0055 for the dedicated crypto-narco nexus threat path.
```

- [ ] **Step 3: Update Revision History**

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0044-state-criminal-infrastructure-convergence.md
git commit -m "enrich: TP-0044 with INTERPOL GFFTA 2026 Tren de Aragua narco-crypto convergence"
```

---

### Task 14: Enrich TP-0047 — Human Trafficking-Linked Fraud Infrastructure

**Files:**
- Modify: `ThreatPaths/TP-0047-human-trafficking-linked-fraud-infrastructure.md`

- [ ] **Step 1: Add to References section**

```markdown
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents scam centre expansion to South America (Spanish/Portuguese-speaking labour demand), Pacific Island nations, and MENA region; reports China-Myanmar-Thailand coordinated operations leading to demolition of 635 buildings in KK Park and full evacuation of Yatai New City with 14,000 foreign nationals from 54 countries detained; notes MENA scam centres targeting Syrian refugees with false promises of safe passage to Europe
- UNODC, *Inflection Point: Global Implications of Scam Centres, Underground Banking and Illicit Online Marketplaces in Southeast Asia*, April 2025
- INTERPOL, *Crime Trend Update: Human Trafficking-Fueled Scam Centres*, June 2025
```

- [ ] **Step 2: Add to Analyst Notes section**

```markdown
**INTERPOL 2026 Update — Global Scam Centre Expansion**: The INTERPOL GFFTA 2026 documents major developments in scam centre operations:

1. **Geographic expansion**: Scam centres have expanded beyond Southeast Asia into South America, Pacific Island nations, and the MENA region. Transnational organized crime groups from East Asia are increasingly targeting South America, driving demand for Spanish- and Portuguese-speaking labour.
2. **Myanmar crackdown**: Between February and December 2025, China, Myanmar, and Thailand conducted coordinated operations against scam compounds in Myanmar, leading to the demolition of 635 buildings in KK Park and the full evacuation of Yatai New City, with 14,000 foreign nationals from 54 countries detained.
3. **MENA trafficking nexus**: Criminal networks in the MENA region target Syrian refugees via social media, luring them with false promises of safe passage to Europe, extracting up to USD 5,000 per victim in smuggling fees. Victims are transported via Lebanon or Türkiye to Cyprus and Italy, where they are forced into labour or abandoned — a hybrid digital-physical enterprise where fraud directly funds human exploitation.
4. **Pacific exploitation**: Scam operations are exploiting weak regulatory oversight in Pacific Island nations, abusing Special Economic Zones, shell companies, and citizenship-by-investment programmes.

These developments confirm the global metastasis of the scam centre model beyond its Southeast Asian origins.
```

- [ ] **Step 3: Update Revision History**

- [ ] **Step 4: Commit**

```bash
git add ThreatPaths/TP-0047-human-trafficking-linked-fraud-infrastructure.md
git commit -m "enrich: TP-0047 with INTERPOL GFFTA 2026 global scam centre expansion intelligence"
```

---

### Task 15: Verify enriched TPs still parse correctly

- [ ] **Step 1: Batch verify all modified TPs parse valid YAML**

Run: `python -c "
import yaml, re, glob
enriched = ['TP-0007', 'TP-0011', 'TP-0012', 'TP-0017', 'TP-0025', 'TP-0026', 'TP-0044', 'TP-0047']
for tp in enriched:
    matches = glob.glob(f'ThreatPaths/{tp}-*.md')
    for f in matches:
        text = open(f).read()
        m = re.search(r'\x60\x60\x60yaml\s*\n---\n(.*?)\n---\s*\n\x60\x60\x60', text, re.DOTALL)
        if m:
            data = yaml.safe_load(m.group(1))
            print(f'{data[\"id\"]}: OK ({data[\"title\"][:50]})')
        else:
            print(f'{f}: FAILED - no frontmatter found')
"`

Expected: All 8 enriched TPs print OK with their titles.

- [ ] **Step 2: Commit if any fixups were needed**

---

## Chunk 3: Build, Verify, and Final Commit

### Task 16: Run database rebuild (was Task 15)

**Files:**
- All generated artifacts in `database/` and `api/v1/`

- [ ] **Step 1: Run the build script**

Run: `cd C:/Users/anon/Documents/anon/repos/flame-fraud && python scripts/build_database.py`

Expected output should show:
- 56 threat paths processed (was 50)
- Updated stats showing 81 fraud types (was 77)
- All JSON, SQLite, search index artifacts regenerated
- INDEX.md auto-updated with new TPs

- [ ] **Step 2: Verify TP count in generated stats**

Run: `python -c "import json; d=json.load(open('database/flame-stats.json')); print(f'TPs: {d[\"total\"]}, Fraud types: {d[\"fraudTypes\"]}, Sectors: {d[\"sectors\"]}')"`

Expected: `TPs: 56, Fraud types: 81, Sectors: 16` (or higher if taxonomy had more than 77)

- [ ] **Step 3: Verify new TPs appear in API**

Run: `python -c "
import json
for tp_id in ['TP-0051','TP-0052','TP-0053','TP-0054','TP-0055','TP-0056']:
    try:
        d = json.load(open(f'api/v1/threat-paths/{tp_id}.json'))
        print(f'{tp_id}: {d[\"data\"][\"title\"]}')
    except Exception as e:
        print(f'{tp_id}: MISSING - {e}')
"`

Expected: All 6 new TPs listed with correct titles.

- [ ] **Step 4: Verify INDEX.md updated**

Run: `grep -c "^| TP-" ThreatPaths/INDEX.md`

Expected: `56`

- [ ] **Step 5: Verify new TPs appear in search index**

Run: `python -c "
import json
idx = json.load(open('database/flame-search-index.json'))
# Search index is a Lunr.js serialized index — verify file size increased
import os
size = os.path.getsize('database/flame-search-index.json')
print(f'Search index size: {size:,} bytes (should be larger than ~141KB baseline)')
"`

- [ ] **Step 6: Commit all generated artifacts**

```bash
git add database/ api/v1/ ThreatPaths/INDEX.md
git commit -m "build: rebuild database with 6 new TPs and 4 new fraud types

56 threat paths, 81 fraud types, 16 sectors.
New: TP-0051 through TP-0056 from INTERPOL GFFTA 2026.
Enriched: TP-0007, TP-0011, TP-0012, TP-0017, TP-0025, TP-0026, TP-0044, TP-0047."
```

---

### Task 17: Final verification

- [ ] **Step 1: Run tests if available**

Run: `cd C:/Users/anon/Documents/anon/repos/flame-fraud && python -m pytest tests/ -v --tb=short 2>&1 | tail -30`

Fix any failing tests (likely test assertions on TP count or fraud type count need updating).

- [ ] **Step 2: Verify no broken JSON**

Run: `python -c "
import json, glob
errors = []
for f in glob.glob('api/v1/**/*.json', recursive=True):
    try: json.load(open(f))
    except Exception as e: errors.append(f'{f}: {e}')
print(f'Checked {len(glob.glob(\"api/v1/**/*.json\", recursive=True))} files, {len(errors)} errors')
for e in errors: print(e)
"`

Expected: 0 errors.

- [ ] **Step 3: Commit any test fixes**

```bash
git add tests/
git commit -m "fix: update test assertions for new TP count (50 -> 56)"
```
