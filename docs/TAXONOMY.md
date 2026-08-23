# FLAME Taxonomy Reference

This document defines the taxonomy elements used across FLAME threat path submissions.

---

## CFPF Phases (Primary Framework)

Every threat path maps to the FS-ISAC **Cyber Fraud Prevention Framework (CFPF)** five-phase lifecycle:

| Phase | Name | Description |
|-------|------|-------------|
| **P1** | Recon | Target identification, OSINT, social engineering preparation |
| **P2** | Initial Access | Account compromise, credential theft, phishing entry |
| **P3** | Positioning | Establishing persistence, privilege escalation, internal movement |
| **P4** | Execution | Executing the fraudulent action (transfers, claims, diversions) |
| **P5** | Monetization | Cashing out, laundering, converting stolen value |

## Fraud Types

Standardized lowercase-hyphenated labels. Each threat path must have at least one.

| Fraud Type | Description |
|-----------|-------------|
| `ACH-fraud` | Fraudulent ACH transfer schemes |
| `account-takeover` | Unauthorized control of legitimate accounts |
| `advance-fee-fraud` | Schemes requiring upfront payment for promised returns |
| `ai-accelerated-fraud-infrastructure` | AI-assisted generation of fraud infrastructure at scale, including domain registration, content generation, and campaign orchestration |
| `ai-document-fraud` | AI-generated fraudulent documents for KYC bypass or claims |
| `application-fraud` | Fraudulent account/credit applications |
| `approval-phishing` | Smart contract approval manipulation (token approvals, permit signatures) |
| `authorized-push-payment` | Victim-authorized payments to fraudster-controlled accounts |
| `autonomous-ai-fraud` | Autonomous AI agents executing fraud without human intervention |
| `BEC` | Business email compromise schemes |
| `benefit-fraud` | Fraudulent claims for government or employer benefits |
| `billing-fraud` | Submission of false or inflated billing claims |
| `bph-migration` | Bulletproof hosting migration and rebranding patterns post-sanctions or post-takedown, including infrastructure relocation and cloud provider abuse |
| `brand-impersonation` | Fraudulent use of brand identity to deceive victims |
| `business-email-compromise` | Compromise of business email for fraudulent purposes |
| `bust-out` | Building credit then maxing out and disappearing |
| `check-fraud` | Check washing, counterfeiting, mobile deposit fraud |
| `cmln-operations` | Chinese Money Laundering Network operations using crypto rails |
| `collusion` | Coordinated fraud involving insiders or multiple actors |
| `credential-stuffing` | Automated credential reuse attacks |
| `crypto-laundering` | Money laundering via cryptocurrency |
| `crypto-laundering-infrastructure` | Cryptocurrency laundering infrastructure at the network level, including CMLN operations, no-KYC exchange off-ramping, and cross-chain bridge exploitation |
| `data-theft` | Exfiltration of PII or financial data |
| `deepfake` | AI-generated audio/video impersonation |
| `deepfake-fraud` | Deepfake-enabled fraud spanning voice, video, and document forgery |
| `disability-fraud` | Fraudulent disability insurance claims |
| `documentary-fraud` | Use of forged or altered documents to facilitate fraud |
| `dprk-it-worker-fraud` | North Korean IT workers using false identities for employment fraud |
| `employment-fraud` | Fraudulent employment schemes or misrepresentation |
| `esim-hijacking` | eSIM-based account takeover (distinct from physical SIM swap) |
| `first-party-fraud` | Fraud committed by the account holder themselves |
| `fraudulent-claim` | False or exaggerated insurance claims |
| `ghost-student-fraud` | Fabricated student identities to harvest financial aid |
| `healthcare-fraud` | Fraud targeting healthcare systems and insurance |
| `human-trafficking-facilitation` | Fraud infrastructure that directly supports human trafficking operations, including recruitment sites, compound control infrastructure, and cryptocurrency payment rails |
| `identity-theft` | Theft and misuse of personal identity information |
| `impersonation` | Identity impersonation (non-synthetic) |
| `insider-threat` | Employee or contractor abuse of access |
| `insurance-fraud` | Fraudulent insurance claims or policy manipulation |
| `investment-scam` | Fraudulent investment schemes and Ponzi operations |
| `invoice-fraud` | Fraudulent or manipulated invoices |
| `loan-fraud` | Fraudulent loan applications or misrepresentation |
| `loyalty-point-fraud` | Theft or abuse of loyalty program points and rewards |
| `malvertising` | Malicious advertising to redirect victims |
| `malware` | Malicious software used to facilitate fraud |
| `money-mule` | Use of intermediaries to move stolen funds |
| `new-account-fraud` | Fraud using newly opened accounts |
| `nfc-relay` | NFC contactless payment data capture and relay attacks |
| `payment-diversion` | Redirecting legitimate payments |
| `payroll-diversion` | Redirecting employee payroll deposits |
| `phantom-billing` | Billing for services or goods never provided |
| `phantom-hacker` | Three-actor impostor chain (tech support, bank, government) coercing safe-account transfers |
| `phishing` | Email/SMS/voice phishing campaigns |
| `premium-diversion` | Insurance premium payment redirection |
| `provider-fraud` | Healthcare or service provider collusion |
| `rdga-infrastructure` | Registered Domain Generation Algorithm campaigns where all generated domains are registered and the algorithm is secret |
| `refunding-as-a-service` | Industrialized refund fraud operations (FTID, RaaS) |
| `romance-scam` | Relationship-based social engineering fraud |
| `sanctions-evasion-infrastructure` | Infrastructure specifically built or repurposed to evade international sanctions (OFAC SDN, EU sanctions lists), including alternative payment rails, stablecoins, and BPH rebranding |
| `scam-compound-operations` | Organized scam compound operations with human trafficking nexus |
| `smishing` | SMS-based phishing and social engineering |
| `social-engineering` | Manipulation of individuals to divulge information or take action |
| `state-criminal-convergence` | Threat paths where nation-state actors and criminal organizations share infrastructure, tools, or operational relationships, crossing the traditional APT/criminal boundary |
| `synthetic-identity` | Fabricated identities using real + fake PII |
| `synthetic-medical-fraud` | AI-generated medical records for healthcare billing fraud |
| `tech-support-scam` | Fake technical support personas obtaining device access or payments |
| `tds-exploitation` | Traffic Distribution System exploitation as an infrastructure-layer threat, including multi-hop redirect chains with cloaking capabilities |
| `tax-fraud` | Fraudulent tax filings or refund claims |
| `unauthorized-transaction` | Transactions executed without account holder authorization |
| `upcoding` | Billing for more expensive services than provided |
| `vendor-impersonation` | Impersonation of legitimate vendors to divert payments |
| `vishing` | Voice-based phishing and social engineering |
| `wire-fraud` | Fraudulent wire transfer schemes |

## Sectors

Standardized sector labels for targeting context:

| Sector | Description |
|--------|-------------|
| `banking` | Commercial and retail banking |
| `credit-union` | Credit unions and member-owned FIs |
| `cross-sector` | Schemes targeting multiple sectors |
| `crypto` | Cryptocurrency exchanges and DeFi |
| `education` | Educational institutions and student financial aid |
| `employment` | Employment services and workforce platforms |
| `fintech` | Financial technology platforms |
| `government` | Government agencies and public sector programs |
| `healthcare` | Healthcare providers and health insurance |
| `insurance` | Insurance carriers and agents |
| `investment` | Investment firms and asset management |
| `payments` | Payment processors and money transfer services |
| `real-estate` | Real estate transactions and title services |
| `retail` | Retail and e-commerce platforms |
| `staffing` | Staffing agencies and temporary workforce |
| `trade` | International trade and trade finance |
| `travel` | Travel and hospitality industry |
| `web3` | Web3, DeFi, and decentralized infrastructure |

## Geopolitical Timing

Optional field linking threat paths to geopolitical event categories that influence campaign timing and targeting:

| Value | Description |
|-------|-------------|
| `none` | No observed geopolitical timing correlation |
| `election-cycle` | Campaigns timed to election periods |
| `sanctions-response` | Infrastructure changes triggered by sanctions announcements |
| `conflict-triggered` | Activity spikes correlated with military conflicts |
| `seasonal-political` | Campaigns timed to political budget cycles, legislative sessions, or diplomatic summits |

Existing threat paths are not required to retroactively populate this field.

## Nation-State Nexus

Optional field classifying the degree of nation-state involvement in a threat path:

| Value | Description | Evidentiary Standard |
|-------|-------------|---------------------|
| `none` | No nation-state involvement | Default assumption |
| `suspected` | Circumstantial evidence of state involvement | Documented infrastructure overlap or timing correlation |
| `confirmed` | Attribution by government agencies or multiple independent CTI firms | At least one government attribution or two independent CTI firm attributions |
| `hybrid` | Documented convergence of state and criminal actors | E.g., Moonstone Sleet deploying Qilin ransomware; DPRK using criminal RaaS |

Existing threat paths are not required to retroactively populate this field.

## Infrastructure Generation Method

Optional field classifying how fraud infrastructure (domains, hosting, certificates) was generated:

| Value | Description |
|-------|-------------|
| `manual` | Domains registered individually or in small batches by human operators |
| `dga-embedded` | Domain Generation Algorithm embedded in malware; algorithm is discoverable through reverse engineering |
| `rdga-registered` | Registered Domain Generation Algorithm; all domains are registered, algorithm is secret, detection requires cluster analysis |
| `ai-assisted` | AI tools used to generate domain names, content, or infrastructure configurations at scale |

Existing threat paths are not required to retroactively populate this field.

## Cross-Framework Mappings

FLAME supports mapping to supplementary frameworks:

### MITRE ATT&CK

Technique IDs in `TXXXX` or `TXXXX.XXX` format. Links resolve to [attack.mitre.org](https://attack.mitre.org/).

### Group-IB Fraud Matrix 2.0

Ten-stage lifecycle providing an alternative perspective to CFPF:

| # | Stage |
|---|-------|
| 1 | Reconnaissance |
| 2 | Resource Development |
| 3 | Trust Abuse |
| 4 | End-user Interaction |
| 5 | Credential Access |
| 6 | Account Access |
| 7 | Defence Evasion |
| 8 | Perform Fraud |
| 9 | Monetization |
| 10 | Laundering |

### Stripe FT3

MIT-licensed fraud taxonomy. Mapped to all 23 TPs via `ft3_mapper.py`. Tactic and technique IDs per TP.

### Group-IB UCFF (Unified Cyber Fraud Framework)

Seven-domain defense governance model. Mapped to 7 of 23 priority TPs as `ucff_domains` in frontmatter. Each mapped TP includes per-domain maturity levels and key deliverables required for effective detection. Domains: Commit, Assess, Prevent, Detect, Respond, Investigate, Manage.

### MITRE F3 (Fight Fraud Framework)

MITRE F3 was released April 9, 2026, as a behavior-based model of fraud actor tactics and techniques. Developed collaboratively by MITRE CTID with FS-ISAC, CrowdStrike, Citigroup, JPMorganChase, Standard Chartered, Lloyds Banking Group, and others.

**Structure**: 7 tactics, 74 top-level techniques (48 F3-native + 26 ATT&CK-reused), 49 sub-techniques.

**Tactics** (kill chain order):
- `TA0043` Reconnaissance (ATT&CK-derived)
- `TA0042` Resource Development (ATT&CK-derived)
- `TA0001` Initial Access (ATT&CK-derived)
- `FA0001` **Positioning** (F3-native) — fraud actor's actions to collect/manipulate data or prepare for execution after initial access
- `TA0002` Execution (ATT&CK-derived)
- `TA0005` Defense Evasion (ATT&CK-derived)
- `FA0002` **Monetization** (F3-native) — fraud actor's actions to convert assets into usable funds or value

**ID format**: F3-native techniques use `F1xxx` (e.g., `F1005` Account Manipulation). Sub-techniques use `F1xxx.yyy` (e.g., `F1005.003` Add Beneficiary). ATT&CK-reused techniques retain their `Txxx` IDs.

**CFPF alignment**: FA0001 (Positioning) maps to CFPF P3; FA0002 (Monetization) maps to CFPF P5.

**Vendored data**: `data/f3/F3_Tactics.json`, `data/f3/F3_Techniques.json`

**Auto-mapper**: `scripts/f3_mapper.py` uses 3-signal mapping (CFPF phase alignment, Group-IB stage matching, fraud type keyword matching) to generate and apply F3 technique suggestions.

**Source**: https://ctid.mitre.org/fraud

## Frontmatter Schema

Every threat path markdown file uses this YAML frontmatter:

```yaml
---
id: TP-XXXX
title: "Descriptive title"
category: ThreatPath
date: YYYY-MM-DD
last_reviewed: YYYY-MM-DD          # date content was last reviewed for currency
author: "Name or Handle"
source: "URL or 'Original Research'"
tlp: WHITE
sector:
  - banking
fraud_types:
  - account-takeover
cfpf_phases: [P1, P2, P3, P4, P5]
mitre_attack: []
ft3_tactics: []
mitre_f3: []
groupib_stages: []
ucff_domains: {}
infrastructure_generation_method: manual  # optional: manual | dga-embedded | rdga-registered | ai-assisted
geopolitical_timing: none                # optional: none | election-cycle | sanctions-response | conflict-triggered | seasonal-political
nation_state_nexus: none                 # optional: none | suspected | confirmed | hybrid
tags:
  - descriptive-tag
---
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full field guidelines.
