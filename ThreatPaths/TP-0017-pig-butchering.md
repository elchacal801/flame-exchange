# TP-0017: Pig Butchering (Investment Scam)

```yaml
---
id: TP-0017
title: "Pig Butchering (Investment Scam)"
category: ThreatPath
date: 2026-02-20
author: "FLAME Project"
source: "Internal Knowledge Base"
tlp: WHITE
sector:
  - banking
  - crypto
  - cross-sector
fraud_types:
  - investment-scam
  - social-engineering
  - authorized-push-payment
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "investment-romance"
primary_phase: "P3"
short_name: "Pig Butchering"
mitre_attack:
  - T1566.002 # Phishing: Spearphishing Link (often via messaging apps)
  - T1656     # Impersonation
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT028", "FT016", "FT007.009", "FT008.003", "FT021", "FT051.003", "FT052.003", "FT001", "FT011", "FT031"]
mitre_f3: ["F1020.002", "F1025.003", "F1018", "F1031", "F1032", "F1040", "F1047", "T1598", "T1660"]
groupib_stages:
  - "Reconnaissance"
  - "End-user Interaction"
  - "Trust Abuse"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 3"
  report: "Level 3"
  improve: "Level 3"
confidence_score: 88
source_reliability: A
info_credibility: 1
related_tps:
  - id: TP-0026
    relationship: related-to
  - id: TP-0032
    relationship: shares-infrastructure
regulatory_refs:
  - REG-AU-SPF
  - REG-FCA-APP
  - REG-MAS-SRF
  - REG-SEC-SAR
  - REG-UK-PSR-APP
  - REG-INTERPOL-GFFTA
  - REG-UNODC-EMERGING-THREATS
  - REG-UNODC-ORGANIZED-FRAUD-2024
  - REG-WCI-2024
baseline_ids:
  - BL-0004
  - BL-0031
  - BL-0034
tags:
  - pig-butchering
  - crypto-scam
  - romance-scam
  - app-fraud
  - interpol-gffta
  - unodc
  - unodc-organized-fraud-2024
  - 40b-annual
  - wci-geographic-attribution
---
```

---

## Summary

"Pig Butchering" (Sha Zhu Pan) is an orchestrated, long-term social engineering scheme where perpetrators build trust with targets over weeks or months (often via dating apps or misdirected text messages) before convincing them to invest in fraudulent cryptocurrency platforms. The scam is characterized by an extended "fattening" phase where the victim sees fake returns on small initial investments, prompting them to invest massive sums before the platform disappears.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors will use social media, dating apps, or SMS to initiate contact, cultivate a romantic or friendly relationship, and gradually introduce the victim to a fraudulent investment platform, culminating in the victim voluntarily authorizing large transfers of funds or cryptocurrency that are ultimately stolen.

**Confidence**: High — Widely documented by law enforcement globally, with billions of dollars in reported losses annually.

**Estimated Impact**: Extremely high per victim. Often results in the victim liquidating life savings, taking out loans, or mortgaging property. Average losses range from $50k to $1M+.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-003: Target identification | Actors source victim phone numbers or social media profiles from data brokers or breaches, initiating contact via "wrong number" texts or dating apps. | Inbound SMS from unknown international or VoIP numbers; rapid transition to encrypted messaging apps (WhatsApp, Telegram) |

**Data Sources**: Telecommunications providers, user-reported SMS spam.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-002: Vishing (voice phishing) / Texting | The actor establishes long-term rapport. No malicious links or overt requests for money are made initially. | (Not visible to financial institution, fully out-of-band social engineering) |

**Data Sources**: Victim mobile devices, messaging platform metadata.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: Add authorized user / Introduce platform | The actor introduces the victim to a fake trading platform (often a sophisticated clone of a real exchange). The victim creates an account and links their legitimate bank account. | User downloads unverified trading apps (TestFlight/sideloaded); victim connects bank account to new crypto on-ramps |

**Data Sources**: Mobile Device Management (MDM) if corporate, bank connection logs (Plaid/Yodlee).

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Unauthorized wire transfer | (Authorized Push Payment) The victim transfers funds from their bank to a legitimate crypto exchange, converts to crypto, and sends it to the fraudulent platform's wallet. | Wire transfers or ACH to crypto exchanges (Coinbase, Kraken); liquidation of legitimate investment accounts followed by immediate transfer out |

**Data Sources**: Bank wire logs, ACH monitoring, securities brokerage withdrawal logs.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-002: Rapid fund movement | The fraudulent platform shows fake profits. When the victim attempts a withdrawal, they are hit with "tax" or "fee" demands (further extortion). Eventually, the communications cease. | Blockchain transactions showing victim deposits flowing immediately to nested exchanges or mixers |

**Data Sources**: Blockchain analytics platforms (Chainalysis, TRM), crypto exchange SARs.

---

## Evasion Techniques

| Technique | Description | Detection Signal |
|-----------|-------------|------------------|
| Domain Sale Page Camouflage | Fraudulent investment platform domain shows "for sale" or "coming soon" page to automated scanners, evading blocklists while remaining operational for victims directed via messaging apps | FP-0007: `http_title` matches parked/sale pattern in domain_intel |
| Geo-Targeted Content | Platform serves legitimate-looking content or blocks access from regions where law enforcement or researchers are likely based | Manual verification required; inconsistent scan results |

**Source**: CrowdStrike Counter Adversary Operations — typosquatting evasion research.

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 5** when the victim reports the fraud because they cannot withdraw their purported "profits."

**Look Left**:

- Financial institutions lack visibility into Phase 1-3.
- The primary indicator at **Phase 4** is highly anomalous fund movements: e.g., an elderly customer who has never traded crypto suddenly wiring $100k to a crypto exchange.

**Look Right**:

- If untracked, victims will often apply for personal loans or home equity lines of credit (HELOCs) to fund "fees" to release their funds, compounding their financial ruin.

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Scam Compound Operator | Industrial-scale fraud facilities (Cambodia, Myanmar, Laos, Philippines) using coerced and trafficked labor | High | Operational cost borne by TCOs; victims/workers are trafficked |
| AI Script Generator | Malicious LLM tools for generating convincing social engineering messages (successors to WormGPT/FraudGPT) | High | $50-$500/month subscription |
| Target Lead Provider | Victim targeting data — social media profiles, dating app users, investment forum members | High | $0.01-$1.00 per lead |
| Crypto Laundering Service | OTC desks, mixing services, cross-chain bridges for converting stolen crypto | High | 5-15% commission |
| Telecommunications Infrastructure | VOIP, virtual numbers, messaging platform accounts for sustained victim engagement | High | $10-$50/month per line |
| Money Mule Network | Bank accounts and crypto wallets for layering transactions | High | 10-20% of laundered value |
| Fraud Tool Marketplace | Platforms providing bundled fraud tools, tutorials, and operational support (Huione Guarantee model) | Medium | Variable — marketplace commissions |

### Tool Ecosystem
Malicious AI chatbot tools (Nytheon AI, Xanthorox AI, GhostGPT and successors replacing earlier WormGPT/FraudGPT), social media profile automation tools, cryptocurrency wallet management and multi-chain transfer tools, victim relationship management systems (CRM-like tools adapted for scam operations), translation tools for multi-language targeting, ghost-tapping tools for contactless payment fraud using pre-loaded stolen payment credentials on NFC-enabled devices.

### Underground Marketplace Presence
Pig butchering operations are orchestrated through industrial-scale scam compounds primarily in Southeast Asia (Cambodia, Myanmar, Laos, Philippines), many operated by Chinese-linked transnational criminal organizations (TCOs) using trafficked and coerced labor. Supporting infrastructure — fraud tools, scripts, laundering services, and target lists — is traded on Telegram-based marketplaces. The Huione Guarantee platform (Telegram marketplace for fraud tools and laundering services) was disrupted but quickly replaced by successors like Tudou, demonstrating the resilience and rapid reconstitution capability of these marketplace ecosystems. The operational model has industrialized to the point where individual scam operators work from scripts with AI assistance, dramatically lowering the skill barrier to entry.

### Intelligence Sources
- Recorded Future 2026 State of Security Report (CTA-2026-0212) — TCO operations, marketplace resilience, AI tool evolution
- FBI IC3 2024 Internet Crime Report — $6.5B investment fraud losses, $9.3B crypto losses
- INTERPOL operations targeting SE Asian scam compounds
- FinCEN advisories on pig butchering / investment fraud schemes
- United Nations Office on Drugs and Crime (UNODC) reports on forced labor in cyber scam operations

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Telco-level SMS spam filtering for "wrong number" lures | Preventive | Telecommunications |
| P4 | Dynamic friction/warnings on wires to crypto exchanges for vulnerable demographics | Preventive | Fraud Ops |
| P4 | Flagging rapid loan origination followed immediately by wire out | Detective | Credit Risk / Fraud |
| P5 | Blockchain monitoring to identify withdrawal addresses linked to known scam syndicates | Detective | Crypto Exchange AML |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive commitment to authorized push payment (APP) fraud prevention, including willingness to introduce customer friction (delays, warnings) that may impact customer experience |
| ASSESS | Level 3 (Established) | Assessment of customer vulnerability segments (elderly, isolated), crypto on-ramp exposure across wire and ACH channels, APP fraud trend analysis by demographic |
| PLAN | Level 3 (Established) | Multi-layered intervention strategy combining real-time warnings, mandatory cooling-off delays for first-time crypto transfers, customer education campaigns, and intelligence sharing with crypto exchanges |
| ACT | Level 4 (Advanced) | Real-time payment intervention for high-risk wire/ACH patterns, behavioral anomaly detection (e.g., elderly customer with no crypto history initiating large transfers), crypto address screening against known scam wallets, dynamic customer warning systems |
| MONITOR | Level 3 (Established) | APP fraud KRIs tracked by customer segment, customer complaint analysis for scam indicators, crypto flow monitoring for on-ramp velocity and destination wallet risk scoring |
| REPORT | Level 3 (Established) | Cross-border reporting to international law enforcement, intelligence sharing with cryptocurrency exchanges on scam wallet addresses, participation in industry consortiums (e.g., Global Anti-Scam Alliance) |
| IMPROVE | Level 3 (Established) | Structured feedback loop from victim interviews and complaint narratives into warning trigger calibration and intervention threshold tuning |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**SQL — High-Value Outbound to Crypto Exchange (Elder Financial Exploitation Indicator)**

```sql
SELECT 
    c.customer_id,
    c.age,
    w.wire_amount,
    w.beneficiary_name,
    w.wire_date
FROM customers c
JOIN wire_outbound w ON c.account_id = w.account_id
WHERE c.age >= 60
  AND w.wire_amount > 25000
  AND w.beneficiary_name SIMILAR TO '%(coinbase|kraken|binance|gemini)%'
  AND NOT EXISTS (
      -- Detect if this is their first time wiring to crypto
      SELECT 1 FROM wire_outbound w_old 
      WHERE w_old.account_id = c.account_id 
        AND w_old.wire_date < CURRENT_DATE - INTERVAL '30 days'
        AND w_old.beneficiary_name SIMILAR TO '%(coinbase|kraken|binance|gemini)%'
  );
```

### Behavioral Analytics

- **Loan-to-Wire Velocity**: Analyze the latency between a customer taking out a new loan, HELOC, or liquidating a CD, and subsequently wiring those funds out. Rapid sequence (< 48 hours) highly indicative of Pig Butchering or other APP fraud.

---

## Analyst Notes

**2024-2026 Intelligence Update (RF CTA-2026-0212):** The pig butchering threat landscape has industrialized dramatically. Nearly $10B in crypto-based scam losses were reported in 2024, with investment fraud accounting for $6.5B per IC3. Southeast Asian transnational criminal organizations (TCOs) operate industrial-scale scam compounds in Cambodia and Myanmar, increasingly using coerced and trafficked labor alongside AI automation. The underground marketplace supporting these operations shows remarkable resilience — when Huione Guarantee (a Telegram-based fraud tool marketplace) was disrupted, successors like Tudou emerged rapidly. An emerging technique variant, "ghost-tapping," uses pre-loaded stolen payment credentials on NFC-enabled devices for contactless payment fraud at physical POS terminals. Malicious AI models (Nytheon AI, Xanthorox AI, GhostGPT) have replaced earlier tools like WormGPT and FraudGPT, offering more sophisticated social engineering capabilities. The infostealer-as-a-service (MaaS) pipeline continues to lower the barrier to entry for less technically skilled operators.

**FBI IC3 2025 Annual Report:** Investment fraud reached $8.65 billion in losses from 72,984 complaints — up 32% from $6.57B in 2024 and the single largest IC3 fraud category for the third consecutive year. Transaction type breakdown (IC3 2025): Cryptocurrency 72%, Wire Transfer/ACH 19%, Peer-to-Peer 4%, Debit/Credit Card 3%, Other 2%. The 72% crypto dominance is directly actionable for detection rule calibration. Crypto investment sub-category: 61,559 complaints, $7.228 billion in losses (48% increase in complaints from 2024). Investment club sub-trend: ~1,600 complaints, $160 million in losses. Accessed via social media and messaging apps — a group-based variant distinct from 1:1 pig butchering grooming. Operation Level Up (FBI): 3,780 victims notified in 2025, 78% unaware they were being scammed, $225.9M in estimated prevented losses. SE Asia scam compound nexus confirmed: IC3 2025 documents organized criminal enterprises in Southeast Asia using human trafficking victims as forced labor to operate crypto investment scams.

**INTERPOL 2026 Update — Scale and Evolution**: The INTERPOL GFFTA 2026 confirms investment fraud (including pig butchering) as the costliest fraud type globally. FBI IC3 data shows USD 5.6 billion in US investment fraud losses in 2023 alone. Key evolutions: (1) AI-generated dashboards now show victims fabricated portfolio returns, making the deception harder to detect; (2) hybrid investment-sextortion schemes use deepfakes to blackmail victims who attempt to withdraw, adding a coercion layer to the pig butchering model (see TP-0052); (3) fraudsters tailor pitches to exploit religious, ethnic, or national identities in victims' native languages, indicating sophisticated audience segmentation. Defrauded funds are frequently laundered through cryptocurrencies across Southeast Asia, South Asia, MENA, Europe, and Africa.

---

## Operational Evidence

### EV-TP0017-2026-003: INTERPOL/UNODC Scale and Loss Estimates

- **Source**: INTERPOL GFFTA 2026; UNODC — Emerging Threats (September 2025)
- **Key Findings**:
  - East and Southeast Asia pig butchering losses estimated at $18-37B for 2023 alone (UNODC)
  - Annual scam centre profits estimated at $40B across the region (UNODC)
  - Pig butchering identified as the single largest fraud type by victim financial loss in INTERPOL's assessment
- **CFPF Phase Coverage**: Full lifecycle (P1-P5) — scale data applies across all phases
- **Confidence**: Very High — multi-source from international organizations

### EV-TP0017-2026-003: UNODC Organized Investment Fraud Typology

- **Source**: UNODC Organized Fraud Issue Paper (Vienna, 2024)
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: UNODC Category 3 (Consumer Investment Fraud) documents organized investment fraud including fraudulent cryptocurrency platforms, exit scams/rug pulls, and Ponzi/pyramid operating models. Key findings: investment fraud victims experience the largest losses compared to other fraud types; OCGs cultivate a veneer of legitimacy with formal organizational structures, division of labor, and designated personnel; recovery fraud operators subsequently re-target investment fraud victims (see TP-0062).

### EV-TP0017-2026-004: 2026 Technical Landscape — Pig Butchering Scale and Rug Pull Detection

- **Source**: Organized fraud detection in 2026: a technical landscape report
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: FBI IC3 reports $6.57B in US investment scam losses in 2024. Documented scam lifecycle: wrong-number contact initiation → weeks-to-months trust building → introduction to fake crypto platform → small initial investment → escalation with artificial gains → "slaughter" (withdrawals blocked). Detection indicators include scripted conversation patterns (from seized scam compound training manuals), migration from dating apps to WhatsApp/Telegram, and DeFi smart contract approval exploitation. Sophos X-Ops documents as-a-service scam kit models on dark web. Crypto rug pulls constitute 68% of all crypto scams in 2025 (350+ cases 2024). Detection methods: Uniswap trading/liquidity feature engineering, EVM bytecode balance-flow heuristics, OSINT signals precede on-chain anomalies by days/weeks.

---

## References

- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Chapter II, Consumer Investment Fraud
- FinCEN Advisory on Pig Butchering (FIN-2023-A002). [Link](https://www.fincen.gov/sites/default/files/shared/FinCEN_Advisory_Pig_Butchering_FINAL_508c.pdf)
- FBI IC3 2023-2024 Cryptocurrency Fraud Reports. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)
- Recorded Future: "2026 State of Security" (CTA-2026-0212) — SE Asian TCO fraud operations, marketplace resilience, AI tool evolution. [Link](https://www.recordedfuture.com/research/)
- FBI IC3 2024 Internet Crime Report — investment fraud and crypto loss figures. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — reports investment fraud as the most financially damaging fraud type globally; documents hybrid investment-sextortion schemes using deepfakes; notes AI-generated dashboards showing fabricated returns
- FBI Internet Crime Complaint Center (IC3), *2024 Internet Crime Report*, April 2025 — USD 5.6 billion in investment fraud losses reported in the United States alone (2023)

- "Organized fraud detection in 2026: a technical landscape report" — Specific fraud category detection: Pig butchering; Crypto rug pulls
- FBI IC3, "2025 Internet Crime Report" — investment fraud and crypto loss figures. [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-20 | FLAME Project | Initial creation |
| 2026-02-28 | FLAME Project | Enriched with RF 2026 TCO intelligence, Underground Ecosystem Context, ghost-tapping variant |
| 2026-03-17 | FLAME Project | INTERPOL GFFTA 2026 enrichment — investment fraud scale, AI dashboard intelligence, sextortion-hybrid convergence |
| 2026-03-20 | FLAME Project | Enriched with INTERPOL/UNODC loss estimates: $18-37B East/SE Asia losses, $40B annual scam centre profits |
