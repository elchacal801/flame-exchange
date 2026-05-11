# TP-0022: Government Program Fraud

```yaml
---
id: TP-0022
title: "Government Program Fraud (Unemployment/Tax)"
category: ThreatPath
date: 2026-02-20
author: "FLAME Project"
source: "Internal Knowledge Base"
tlp: WHITE
sector:
  - government
  - banking
fraud_types:
  - benefit-fraud
  - identity-theft
  - synthetic-identity
  - tax-fraud
cfpf_phases:
  - P1
  - P3
  - P4
  - P5
fraud_family: "identity-synthetic"
primary_phase: "P4"
short_name: "Gov Program Fraud"
mitre_attack: []
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT052.004", "FT026.004", "FT016.001", "FT020", "FT005.001", "FT011.002", "FT018", "FT025", "FT051.003", "FT006"]
mitre_f3: ["F1020.001", "F1006", "F1029", "T1585"]
groupib_stages:
  - "Resource Development"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 4"
  improve: "Level 3"
confidence_score: 82
source_reliability: A
info_credibility: 2
related_tps:
  - id: TP-0003
    relationship: feeds-into
  - id: TP-0011
    relationship: provides-mules-for
  - id: TP-0033
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-CDD
baseline_ids: []
tags:
  - benefits-scam
  - irs-fraud
  - targeted-demographics
---
```

---

## Summary

Government Program Fraud involves threat actors leveraging stolen Personally Identifiable Information (PII) to file fraudulent claims for government benefits (e.g., UI, SNAP, FEMA disaster relief) or tax refunds. The actor directs the government payout to a pre-paid debit card, a digitally opened neo-bank account, or an established mule account, depriving the legitimate citizen of their benefits and defrauding the state.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors source massive quantities of PII from data broker breaches, use automation to bulk-file claims with state workforce or tax agencies, and route the approved funds into networks of "drop" accounts or prepaid debit cards.

**Confidence**: High — Verified by the massive wave of unemployment fraud observed globally during the 2020-2022 pandemic, and ongoing persistent tax return fraud.

**Estimated Impact**: Micro-impacts of $1,000 to $20,000 per victimized identity, but macro-impacts totaling hundreds of billions of dollars across federal and state governments when executed via automated botnets.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Data Sourcing | Actors purchase bulk "Fullz" (full PII profiles) from dark web marketplaces, specifically targeting demographics likely to qualify for specific benefits or not actively filing taxes (e.g., the elderly, the incarcerated). | Large dark web data dumps involving SSNs, DOBs, and historical employment data. |

**Data Sources**: Cyber Threat Intelligence feeds.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: Account Setup (Benefits Portal) | Actor creates a portal account with the state agency using the victim's PII, often using variations of a single email domain (e.g., Gmail dot-trick) to manage thousands of profiles. | High volume of accounts registered from the same IP range; email addresses following patterned or alias structures. |
| CFPF-P3-002: Drop Account Creation | Actor opens accounts at fintechs or banks to receive the funds, or requests prepaid debit cards be mailed to compromised physical addresses. | New account opening velocity anomalies associated with specific IP or device clusters. |

**Data Sources**: State agency portal logs, financial institution onboarding logs.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Claim Submission | The actor submits the fraudulent UI claim or forged tax return, instructing the agency to deposit the money to the drop account. | High velocity of claims filed outside normal seasonal parameters; "bursts" of claims from similar IP blocks. |

**Data Sources**: Government system audit logs.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: ACH Deposit & Rapid Withdrawal | State agency originates the ACH deposit. Once it lands in the bank account, the actor immediately withdraws it via ATM, wire, or crypto purchase. | Multiple government ACH deposits (often in different names) hitting a single account, followed by immediate ATM cash-outs. |

**Data Sources**: Bank ACH monitoring, ATM transaction logs.

---

## Look Left / Look Right Analysis

**Discovery Phase**: Discovered at **Phase 5** by financial institutions when identifying suspicious volumes of inbound government ACHs, or later when the true citizen attempts to file their real tax return and is rejected.

**Look Left**:

- Financial institutions see the ACH deposit, but the state agency operates independently. Frictionless information sharing between the FI (which sees the anomalous bank account) and the State (which sees the anomalous login) is historically poor.

**Look Right**:

- Uncaught botnets will iterate through databases, finding vulnerabilities across different state systems, migrating from high-security states to those with weaker controls.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P3 | Identity Verification (NIST IAL2) at government portals prior to account creation | Preventive | Government Agency |
| P4 | Analytics to identify highly coordinated claim submissions (IP pooling, device fingerprints) | Detective | Government Agency |
| P5 | FI AML rules flagging Name Mismatches: Inbound ACH name doesn't match the Bank Account holder name | Preventive | Bank AML/Fraud |
| P5 | Rules flagging >1 distinct government benefit deposits hitting a single consumer account | Detective | Bank Fraud |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Organizational commitment to detecting government benefit fraud at the financial institution level; investment in ACH monitoring capabilities and cross-agency information sharing |
| ASSESS | Level 3 (Established) | Risk assessment of deposit account portfolio for government benefit fraud exposure; evaluation of onboarding controls for accounts likely to serve as drop accounts (fintech, prepaid, neo-bank); analysis of inbound ACH patterns for government-originated deposits |
| PLAN | Level 3 (Established) | Detection strategy combining ACH name-mismatch analysis, government deposit velocity monitoring, and rapid withdrawal pattern detection; coordination plan with state workforce agencies and IRS for fraud intelligence sharing |
| ACT | Level 3 (Established) | Automated ACH receiver name vs. KYC account holder fuzzy matching for government-originated deposits; velocity rules flagging multiple distinct government benefit deposits to a single consumer account; device fingerprinting and IP clustering analysis at account opening to detect botnet-driven drop account creation |
| MONITOR | Level 3 (Established) | Continuous monitoring for government ACH deposits followed by immediate ATM cash-outs, wire transfers, or crypto purchases; tracking of account opening velocity from shared IP ranges or device clusters; seasonal anomaly detection for unemployment claims outside normal filing patterns |
| REPORT | Level 4 (Advanced) | SAR filing for suspected government benefit fraud with enriched typology codes; real-time reporting to state agencies when drop accounts are identified; coordination with Secret Service and FBI for large-scale botnet-driven benefit fraud networks |
| IMPROVE | Level 3 (Established) | Post-investigation review incorporating state agency feedback on confirmed fraud cases; recalibration of name-mismatch thresholds and deposit velocity triggers; integration of new PII breach data into proactive drop account identification models |

## Detection Approaches

### Queries / Rules

**SQL — Multiple UI/Tax Deposits to Single Account (Mule Indicator)**

```sql
SELECT 
    a.account_id,
    COUNT(DISTINCT t.originator_name) as distinct_state_agencies,
    SUM(t.amount) as total_government_deposits,
    MAX(t.transaction_date) as latest_deposit
FROM ach_inbound t
JOIN accounts a ON t.account_id = a.account_id
WHERE t.sec_code = 'PPD' 
  AND t.originator_name SIMILAR TO '%(UI|UNEMPLOYMENT|TREAS 310|TAX REF)% '
  AND t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1
HAVING COUNT(*) > 2 -- More than 2 distinct benefit deposits
   AND COUNT(DISTINCT t.receiver_name) > 1; -- For different individuals
```

### Behavioral Analytics

- **Name Mismatch Analysis**: Utilize fuzzy matching (Levenshtein distance) between the ACH Receiver Name and the KYC Account Holder Name. Wide divergence in consumer accounts receiving government funds indicates a "drop" account for stolen UI/Tax refunds.

---

## Analyst Notes

**IC3 2025 Data:** The FBI IC3 2025 Internet Crime Report reported $797.9 million in government impersonation fraud losses from 32,424 complaints — an 87% increase in complaints and 97% increase in losses from 2024. Transaction type breakdown: Cryptocurrency 40%, Wire Transfer/ACH 21%, Prepaid card/Gift card 15%, Cash 14%, Check/Cashier's Check 10%. Elder victims (60+) accounted for 8,628 complaints and $413.2M in losses. Note: Government impersonation APP fraud (using government authority to socially engineer payments) is distinct from the government program exploitation covered by this TP. See TP-0084 for the impersonation-based attack path.

**IC3 2024 Data:** The FBI IC3 2024 Internet Crime Report (covering 2024 incidents, released April 2025) reported $405M in government impersonation losses. This figure captures cases where actors impersonate government agencies to extract payments from victims, which overlaps with this threat path's use of stolen identities to file fraudulent government benefit claims. IC3 also recorded over 108,000 identity theft complaints in 2024, representing the PII theft pipeline that fuels bulk fraudulent benefit filings.

---

## References

- FBI IC3: "2024 Internet Crime Report" (April 2025) — annual loss and complaint statistics. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)
- FBI IC3: "2025 Internet Crime Report" — Government impersonation fraud: $797.9M in losses, 32,424 complaints (87% increase in complaints, 97% increase in losses from 2024). Transaction type breakdown: Cryptocurrency 40%, Wire Transfer/ACH 21%, Prepaid card/Gift card 15%, Cash 14%, Check/Cashier's Check 10%. Elder targeting: 8,628 complaints, $413.2M in losses from 60+ victims. [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)
- FLAME Project Internal Knowledge Base.
- U.S. Secret Service Advisories on Pandemic Fraud Networks.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-20 | FLAME Project | Initial creation |
| 2026-02-28 | FLAME Project | v1.5 enrichment: added Stripe FT3 tactic mappings, IC3 2024 loss figures |
| 2026-04-06 | FLAME Project | FBI IC3 2025 enrichment — government impersonation $797.9M losses (97% increase), elder targeting $413.2M, TP-0084 cross-reference |
