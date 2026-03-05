# Phase 6: LNRS Integration + BNPL Fraud TP — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate quantitative intelligence from the LexisNexis Global State of Fraud 2026 report into 5 existing threat paths, add a new BNPL multi-provider fraud threat path (TP-0040) with 5 detection rules and 1 baseline, and rebuild all artifacts.

**Architecture:** Content-first approach — write YAML/markdown content files following existing templates, validate with `validate_submission.py`, rebuild database and exports. All new content follows the conventions established in Phase 5 (TP-0035 through TP-0039).

**Tech Stack:** Markdown (TPs, BLs), YAML (DLs), Python build scripts, SQLite, JSON APIs, STIX/MISP/Sigma exports

**Key files for reference:**
- Template TP: `ThreatPaths/TP-0035-magecart-eskimmer-data-compromise.md`
- Template DL: `DetectionLogic/DL-0075-eskimmer-script-injection.yml`
- Template BL: `Baselines/BL-0015-ecommerce-payment-page-integrity.md`
- Taxonomy: `flame_taxonomy.json`
- Design doc: `docs/plans/2026-03-04-phase6-lnrs-bnpl-design.md`
- LNRS report: `docs/docs_internal/lnrs_global-state-of-fraud_2026.md`

---

## Task 1: Taxonomy Update

**Files:**
- Modify: `flame_taxonomy.json`

**Step 1: Add `bnpl-fraud` to fraud_types array**

Insert alphabetically after `brand-impersonation`:

```json
"bnpl-fraud",
```

**Step 2: Verify taxonomy is valid JSON**

Run: `python -c "import json; json.load(open('flame_taxonomy.json'))"`
Expected: No output (valid JSON)

**Step 3: Commit**

```bash
git add flame_taxonomy.json
git commit -m "feat(6.0): add bnpl-fraud to taxonomy"
```

---

## Task 2: Create TP-0040 (BNPL Multi-Provider Fraud)

**Files:**
- Create: `ThreatPaths/TP-0040-bnpl-multi-provider-fraud.md`

**Step 1: Write the threat path**

Use `ThreatPaths/TP-0035-magecart-eskimmer-data-compromise.md` as the structural template. Required sections:

1. **YAML frontmatter** (inside ```yaml block):
   - title: "BNPL Multi-Provider Fraud — Synthetic Stacking, ATO & Friendly Fraud"
   - id: TP-0040
   - date: 2026-03-04
   - confidence_score: 78
   - source_reliability: B
   - info_credibility: 2
   - sectors: [retail, payments, fintech, banking]
   - fraud_types: [bnpl-fraud, first-party-fraud, identity-theft, account-takeover, social-engineering]
   - cfpf_phases: [P1, P2, P3, P4, P5]
   - mitre_attack: [T1586, T1589.001, T1657, T1583.001]
   - related_tps: TP-0003 (synthetic-identity-parent), TP-0016 (bust-out-variant), TP-0029 (ai-doc-forgery-for-kyc), TP-0030 (triangulation-via-bnpl), TP-0031 (inr-refund-overlap), TP-0013 (credential-stuffing-ato)
   - regulatory_refs: [REG-CFPB-REGE, REG-FCA-APP, REG-AU-SPF]
   - tags: [bnpl, klarna-method, synthetic-stacking, friendly-fraud, buy-now-pay-never, multi-provider]

2. **Summary**: BNPL as growing fraud surface ($3.2B synthetic exposure H1 2024, 3-4% fraud rate, 79% merchants hit by friendly fraud). Three attack variants. Multi-provider stacking enabled by lack of cross-bureau BNPL loan reporting. Regulatory landscape in flux (CFPB rescission, FCA full regulation 2026, ASIC licensing June 2025).

3. **CFPF Phase Mapping** (P1-P5):
   - P1 Recon: Fullz acquisition, BNPL provider KYC gap reconnaissance, dark web tutorials (Klarna Method on TikTok/Telegram)
   - P2 Initial Access: Synthetic account creation (soft-check-only approval), ATO via credential stuffing (45% password reuse), OTP/MFA bypass (EvilginX, SIM swap), emulator-based mass account opening
   - P3 Positioning: Credit grooming (small purchases repaid over weeks), multi-provider stacking (3+ providers in 72h), address preparation (reshipping services), spending limit probing
   - P4 Execution: Simultaneous bust-out across providers, phantom delivery (INR claims), friendly fraud disputes, address diversion post-purchase, coordinated ring stacking (50-1000+ synthetic IDs)
   - P5 Monetization: Physical goods resale/fencing (Facebook Marketplace, OfferUp), gift card liquidation, drop shipping/triangulation layer (combines with TP-0030), debt abandonment

4. **Cross-Framework Mapping**: FT3, MITRE ATT&CK (T1586, T1589.001, T1657, T1583.001), Group-IB Fraud Matrix

5. **Look Left / Look Right Analysis**:
   - Look Left: Dark web fullz markets, credential breach databases, BNPL provider vulnerability assessment forums
   - Look Right: Goods fencing networks, reshipping services, mule account cashout, triangulation fraud

6. **Underground Ecosystem Context**:
   - Telegram channels (53% activity surge), TikTok tutorials (Klarna Method viral), STYX marketplace
   - Fullz packages ($5-$50), pre-warmed synthetic accounts, reshipping service networks, emulator kits, OTP interception kits
   - FaaS generates ~$520M annually from $3.2B dark web revenue

7. **Controls & Mitigations**: Cross-provider application velocity monitoring (consortium data), digital footprint scoring at onboarding, behavioral biometrics during session, mandatory credit bureau BNPL loan reporting, device fingerprinting (emulator detection), shipping address risk scoring

8. **UCFF Alignment**: Map to Commit, Assess, Plan, Act, Monitor domains

9. **Detection Approaches**: Reference DL-0087 through DL-0091. Also reference existing linkable rules: DL-0012 (login velocity), DL-0014 (device fingerprint), DL-0015/DL-0016 (credential stuffing), DL-0063 (refund velocity), DL-0066 (INR high-value)

10. **References**: Include all sources from the BNPL research (Experian, ACI Worldwide, MRC, CentoLaw, FrankOnFraud, TechCrunch, SEON, Fingerprint.com, Fraud.net, DataVisor, Ocrolus, NoFraud, Resecurity, ASIC, PaymentsDive, GlobeNewswire, CFPB, Juniper Research, LNRS report)

11. **Provider-Specific Intelligence**: Table of Klarna, Afterpay, Affirm, Clearpay, Zip with known fraud patterns and distinctive factors

12. **Analyst Notes**: Regulatory divergence analysis (CFPB vs FCA vs ASIC), stacking invisibility problem (no cross-bureau reporting), Klarna Glitch case study (Detroit, Christmas 2024)

13. **Revision History**: Initial publication 2026-03-04

**Step 2: Validate**

Run: `python scripts/validate_submission.py ThreatPaths/TP-0040-bnpl-multi-provider-fraud.md`
Expected: PASS

---

## Task 3: Create 5 Detection Rules (DL-0087 through DL-0091)

**Files:**
- Create: `DetectionLogic/DL-0087-bnpl-onboarding-risk-signals.yml`
- Create: `DetectionLogic/DL-0088-bnpl-multi-provider-stacking.yml`
- Create: `DetectionLogic/DL-0089-bnpl-spending-stepup-bustout.yml`
- Create: `DetectionLogic/DL-0090-bnpl-inr-claim-velocity.yml`
- Create: `DetectionLogic/DL-0091-bnpl-device-clustering.yml`

Use `DetectionLogic/DL-0083-card-testing-micro-auth.yml` as structural template. Each rule needs:
- title, id (UUID v4), status: experimental, description, references, threat_paths, cfpf_phase, fraud_types, logsource, detection (with selection + aggregation/filter sections + condition), falsepositives, level, tags

**DL-0087**: BNPL Account Opening Risk Signal Cluster
- Phase: P2, Level: high, Product: ecommerce, Service: bnpl_onboarding
- Detection: email_domain_age_days|lte: 30 AND account_type = 'bnpl' AND digital_footprint_score|lte: 0.2
- False positives: Young consumers with limited digital history, new email adopters

**DL-0088**: BNPL Multi-Provider Application Velocity
- Phase: P3, Level: critical, Product: ecommerce, Service: credit_application
- Detection: count applications >= 3, groupby: identity_hash, timeframe: 72h, distinct BNPL providers >= 3
- False positives: Consumers comparison shopping across BNPL providers, corporate purchasing agents

**DL-0089**: BNPL Spending Step-Up to Limit Bust-Out Pattern
- Phase: P4, Level: critical, Product: ecommerce, Service: bnpl_transactions
- Detection: first_order_value|lte: 50 AND subsequent orders escalating AND final_order_value >= 85% of account limit AND time span <= 14 days
- False positives: Legitimate consumers building confidence with a new BNPL provider

**DL-0090**: BNPL Item-Not-Received Claim Velocity
- Phase: P4, Level: high, Product: ecommerce, Service: bnpl_disputes
- Detection: INR claims >= 3, groupby: account_id, timeframe: 90d, AND avg disputed order value >= 300
- False positives: Legitimate delivery failures in areas with known courier issues

**DL-0091**: BNPL Cross-Account Device Clustering
- Phase: P3, Level: high, Product: ecommerce, Service: bnpl_onboarding
- Detection: distinct accounts per device >= 4, timeframe: 30d, AND accounts created within window
- False positives: Shared household devices, retail kiosk devices

**Step 2: Validate all 5**

Run: `python scripts/validate_submission.py DetectionLogic/DL-008[7-9]*.yml DetectionLogic/DL-009[0-1]*.yml`
Expected: 5 passed, 0 failed

---

## Task 4: Create Baseline BL-0020

**Files:**
- Create: `Baselines/BL-0020-bnpl-account-transaction-patterns.md`

Use `Baselines/BL-0015-ecommerce-payment-page-integrity.md` as structural template.

**Content:**
- Description: Normal BNPL account and transaction behavior patterns
- Normal Patterns:
  - Email domain age at onboarding: >180 days (median)
  - Time from account creation to first order: 2-7 days (median)
  - Payment completion rate: 95%+ for legitimate users
  - BNPL providers used simultaneously: 1-2 over 12 months
  - INR dispute rate: <1% of orders
  - Shipping address change pre-dispatch: <1% of orders
  - Device reuse across accounts: 1 device per 1-2 accounts
  - First order as percentage of limit: 20-40%
  - Digital footprint score: Active profiles on 3+ platforms >6 months old
- Application to Detection: Reference DL-0087 through DL-0091, explain thresholds

**Step 2: Validate**

Run: `python scripts/validate_submission.py Baselines/BL-0020-bnpl-account-transaction-patterns.md`
Expected: PASS

---

## Task 5: Enhance TP-0016 (First-Party Fraud / Bust-Out)

**Files:**
- Modify: `ThreatPaths/TP-0016-first-party-fraud.md`

**Step 1: Add LNRS analyst notes**

Add new subsection under `## Analyst Notes`:

```markdown
### First-Party Fraud Scale — LexisNexis Global State of Fraud 2026

First-party fraud now represents 36% of all detected fraud events globally (up from 15% prior year), with losses of $3.9B in 2025 projected to reach $4.8B by 2028. Regional rates vary sharply: EMEA leads at 51% (up from 18%), North America at 30% (up from 8%), LATAM at 11%, and APAC at 6%. By industry, ecommerce (42%, up from 9%) and financial services (37%, up from 19%) are most affected.

A novel "viral fraud" phenomenon has emerged where consumer cohorts coordinate via social media to simultaneously exploit the same vulnerabilities. These cohorts exhibit distinctive characteristics: 2x more inquiries, 3x more likely to have a previously tagged fraud, 7.4x more likely to have a felony record, and average 12 years younger than baseline. Generational breakdown: Older Millennials 18%, Younger Millennials 16%, Gen Z 13%, Gen X 7%.

Consortium intelligence (cross-institutional data sharing) lifts fraud capture rates 43% over isolated approaches — a critical defense given that first-party fraud actors ARE the legitimate account holders.
```

**Step 2: Add related_tps entry for TP-0040**

Add to frontmatter `related_tps`:
```yaml
  - id: TP-0040
    relationship: variant-of
```

**Step 3: Add tags**

Add to frontmatter tags: `viral-fraud`, `lnrs-2026`

**Step 4: Add reference**

Add to References section:
```markdown
- LexisNexis Risk Solutions: "Global State of Fraud and Identity Report 2026"
```

**Step 5: Update date to 2026-03-04**

---

## Task 6: Enhance TP-0024 (A2A Instant Payment Fraud)

**Files:**
- Modify: `ThreatPaths/TP-0024-a2a-instant-payment-fraud.md`

**Step 1: Add LNRS analyst notes subsection**

```markdown
### Mule Laundering Speed & Consortium Intelligence — LNRS 2026

Network retro analysis documented a complete laundering cycle in just 30 minutes — stolen funds from two separate scam victims washed through multiple banks and ultimately through gaming and retail websites. The UK Banking Consortium (Jan-Sep 2025) tagged 377,000 mule payments representing £100M in stolen funds (65% YoY surge), identifying 22K digital identities, 80K devices, and 17K beneficiaries. Total consortium-detected fraudulent payments reached £508M across 1.4M payments in 8 months.

Combining CNP risk data with Digital Identity Network and Internet Banking intelligence lifted fraud detection from 43% to 75% (at 1.0% false positive rate), representing a $28.2M annualized increase in detected fraud value for a single major banking client. Consortium intelligence lifts fraud capture 43% over isolated approaches.
```

**Step 2: Add reference and update date**

---

## Task 7: Enhance TP-0011 (Romance Scam Mule Pipeline)

**Files:**
- Modify: `ThreatPaths/TP-0011-romance-scam-mule-pipeline.md`

**Step 1: Add LNRS analyst notes subsection**

```markdown
### Mule Network Operational Scale — LNRS 2026

The average mule network consists of 15 mules moving money among 3.4 banks. The largest documented network involved 543 mules and moved more than £130 million. In the UK alone, mules launder an estimated £10 billion annually.

Global enforcement actions are escalating: Europol supported operations against two networks that profited over $10M from cryptocurrency scams; the U.S. DOJ took action against 3,000+ money mules in its 2024 initiative; Hong Kong police dismantled a HK$118M crypto laundering ring with 500+ mule accounts.

Mule recruitment increasingly targets youth: 35% of Gen Z say they would consider moving money for a stranger for a fee, 14% "very likely." Among 18-24 year olds, 30% say they or someone they know has been approached, and 27% would be open to it. Three mule typologies are now recognized: complicit (willing participants), recruited (persuaded, paid, or forced), and exploited (unwitting participants whose accounts are misused).
```

**Step 2: Add reference and update date**

---

## Task 8: Enhance TP-0003 (Synthetic Identity Bust-Out)

**Files:**
- Modify: `ThreatPaths/TP-0003-synthetic-identity-bust-out.md`

**Step 1: Add LNRS analyst notes subsection**

```markdown
### Synthetic Identity Intelligence Update — LNRS 2026

Synthetic fraud is projected to generate $23 billion in losses by 2030. An estimated 85% of identity fraud cases now involve generative AI tools, dramatically lowering the barrier to creating convincing synthetic identities. Digital wallets — expected to account for 61% of ecommerce transactions by 2027 — represent an expanding synthetic identity vector, while 5 billion digital IDs have already been issued globally.

Thin-file exploitation is a growing concern: digitally fluent young people and new-to-country immigrants lack traditional credit histories, and fraudsters deploy synthetic identities that mirror these "acceptable" thin-file profiles while simultaneously targeting these vulnerable populations as money mule recruits. FinCEN's policy allowing banks to collect TIN from third parties (rather than directly from customers) may open a new attack vector.
```

**Step 2: Add related_tps entry for TP-0040, add reference, update date**

---

## Task 9: Enhance TP-0029 (AI Synthetic Identity & Document Forgery)

**Files:**
- Modify: `ThreatPaths/TP-0029-ai-synthetic-identity-document-forgery.md`

**Step 1: Add LNRS analyst notes subsection**

```markdown
### AI Fraud Arms Race Escalation — LNRS 2026

The arms race between "good AI" and "bad AI" is accelerating. An estimated 85% of identity fraud cases involve generative AI tools, while a study revealed that people correctly spot deepfakes only 20% of the time. In 2021, virtually no forged documents were AI-generated; by 2024, AI-generated forgeries were involved in 57% of attacks.

A fraudster recently scammed $20 million from Brazilian financial institutions using multiple deepfake accounts. On the dark web, 4.6 million users accessed it daily in 2025 (up from 3M in 2024), with KYC-as-a-service packages available for $500-$800.

Enterprise awareness is rising: 72% of S&P 500 companies disclosed material AI risk in 2025, up from just 12% in 2023. Meanwhile, 88% of senior executives plan to increase AI budgets specifically for agentic AI, signaling both defensive investment and recognition of the AI agent attack surface.
```

**Step 2: Add reference and update date**

---

## Task 10: Update INDEX.md and Documentation

**Files:**
- Modify: `ThreatPaths/INDEX.md`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `app.js`

**Step 1: Update INDEX.md**

- Update header count: 39 → 40 TPs, 59 → 60 fraud types
- Add TP-0040 row to Coverage Summary table
- Add `bnpl-fraud` entry to Coverage by Fraud Type table
- Update Banking, Fintech, Payments, Retail sector counts in Coverage by Sector
- Add cross-TP connection lines for TP-0040

**Step 2: Update CHANGELOG.md**

Add v0.8.0 entry above v0.7.0:

```markdown
## v0.8.0 — Phase 6: SIGNAL-LNRS (2026-03-04)

### Added
- **TP-0040**: BNPL Multi-Provider Fraud — Synthetic Stacking, ATO & Friendly Fraud
- **DL-0087 through DL-0091**: 5 BNPL fraud detection rules
- **BL-0020**: BNPL Account & Transaction Patterns baseline
- `bnpl-fraud` fraud type added to taxonomy

### Enhanced
- **TP-0016**: First-party fraud scale data (36% of all fraud, $3.9B losses, viral fraud cohorts)
- **TP-0024**: Mule laundering speed data (30-min window, £508M consortium results)
- **TP-0011**: Mule network operational scale (15 avg mules, Gen Z recruitment stats)
- **TP-0003**: Synthetic identity projections ($23B by 2030, 85% GenAI involvement)
- **TP-0029**: AI fraud arms race data (20% deepfake detection rate, $20M Brazilian scam)

### Source Intelligence
- LexisNexis Risk Solutions: Global State of Fraud and Identity Report 2026
- Supplementary BNPL fraud research (Experian, ACI Worldwide, MRC, CFPB, FCA, ASIC)
```

**Step 3: Update README.md**

- Update TP count: 39 → 40
- Update DL count: 86 → 91
- Update TP table: add TP-0040 row
- Update fraud type count if displayed

**Step 4: Update app.js About modal**

- Add Phase 6 to roadmap section
- Add Phase 6 changelog entry
- Update MISP cluster count: 39 → 40

---

## Task 11: Build and Export

**Step 1: Run validation on all new files**

```bash
python scripts/validate_submission.py ThreatPaths/TP-0040-bnpl-multi-provider-fraud.md
python scripts/validate_submission.py DetectionLogic/DL-008[7-9]*.yml DetectionLogic/DL-009[0-1]*.yml
python scripts/validate_submission.py Baselines/BL-0020-bnpl-account-transaction-patterns.md
```
Expected: All pass

**Step 2: Rebuild database**

```bash
python scripts/build_database.py
```
Expected: 40 TPs loaded, 91 DL rules, 0 errors

**Step 3: Run exports**

```bash
python scripts/export_flame_stix.py
python scripts/export_misp.py
python scripts/export_taxii.py
python scripts/export_sigma.py
```
Expected: All succeed

---

## Task 12: Verify and Commit

**Step 1: Start dev server and verify TP-0040 loads**

Use preview tools to verify the frontend renders TP-0040 correctly with proper tags, phases, and sector badges.

**Step 2: Final commit**

```bash
git add -A  # (review staged files first)
git commit -m "feat(6.0): Phase 6 SIGNAL-LNRS — BNPL fraud TP, LNRS enhancements, rebuilt artifacts"
git push
```

---

## Parallelization Notes

Tasks 2, 3, 4 (new TP, DLs, BL) can be parallelized via subagents after Task 1 completes.
Tasks 5-9 (TP enhancements) can all be parallelized.
Task 10 depends on Tasks 2-9.
Tasks 11-12 are sequential and last.
