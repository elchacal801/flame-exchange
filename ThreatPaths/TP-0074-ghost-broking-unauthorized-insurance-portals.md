# TP-0074: Ghost Broking & Unauthorized Insurance Portals

```yaml
---
id: TP-0074
title: "Ghost Broking & Unauthorized Insurance Portals"
category: ThreatPath
date: 2026-03-27
last_reviewed: 2026-03-29
author: "FLAME Project"
source: "Aviva ghost broking intelligence (Nov 2025); City of London Police (2025); Insurance Times (2025); ABI (2025); FraudOps (2026); NICB"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - ghost-broking
  - ghost-portal
  - insurance-policy-fraud
  - unlicensed-insurance
sector:
  - insurance
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "insurance-healthcare"
primary_phase: "P3"
short_name: "Ghost Broking"
confidence_score: 82
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1583.001  # Acquire Infrastructure: Domains
  - T1566.002  # Phishing: Spearphishing Link
  - T1078      # Valid Accounts
  - T1589      # Gather Victim Identity Information
  - T1656      # Impersonation
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT019", "FT026", "FT041", "FT049", "FT052", "FT054", "FT055", "FT043"]
mitre_f3: ["F1021", "F1027", "F1032"]
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
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
  - id: TP-0056
    relationship: related-to
  - id: TP-0066
    relationship: related-to
regulatory_refs: []
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - ghost-broking
  - ghost-portal
  - fake-insurance
  - unlicensed-intermediary
  - insurance-fraud
  - organized-crime
  - uk-insurance
  - ifed
---
```

## Summary

Ghost broking is a rapidly growing insurance fraud typology where unlicensed individuals or organized crime groups sell fraudulent, forged, or illegitimately obtained motor insurance policies to unsuspecting consumers. Victims increased 93% in 2025, driven by cost-of-living pressures that make below-market premiums attractive. An emerging evolution is the "ghost portal" — fraudsters now build and sell entire fake insurance verification platforms to other criminals, creating a fraud-as-a-service layer within the insurance ecosystem. City of London Police made significant arrests in May 2025, and the Insurance Fraud Enforcement Department (IFED) designated February 2026 as a ghost broking intensification month. UK fraud losses topped GBP 1 billion in 2024, with ghost broking contributing a material share of motor insurance fraud.

**Distinction from TP-0056**: TP-0056 covers claims fraud (filing false or inflated claims against legitimate policies). TP-0074 covers the upstream fraud of selling fake or unauthorized policies themselves, where the victim believes they have legitimate coverage but does not.

## Threat Path Hypothesis

> **Hypothesis**: Ghost brokers exploit the complexity and opacity of insurance distribution channels to sell fraudulent policies at below-market premiums, targeting price-sensitive consumers through social media, community groups, and messaging platforms. The threat has evolved from individual opportunists to organized operations that build entire fake insurance portal ecosystems — selling platform access to other fraudsters. Detection is complicated by the use of genuine insurer branding, real-looking policy documentation, and sophisticated verification portals on recently registered domains that return valid-appearing but unverifiable policy numbers. The connection to organized crime networks means ghost broking revenue funds other criminal enterprises including crash-for-cash rings (TP-0066).

**Confidence**: High — Aviva, ABI, City of London Police, and IFED have published detailed intelligence. Victim increase figures are quantified.

**Estimated Impact**: Individual victims face uninsured driving penalties (up to GBP 5,000 fine, 6-8 penalty points, vehicle seizure) and no coverage for accidents. Aggregate: UK motor insurance fraud exceeds GBP 1 billion annually, with ghost broking a significant and growing contributor.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Target market identification | Ghost brokers identify demographics most susceptible to below-market insurance offers — young drivers, newly qualified drivers, high-risk postcodes, migrant communities | Social media monitoring of insurance complaint groups; analysis of price comparison site demographics |
| Insurer brand research | Operators study legitimate insurer branding, policy document formats, and verification processes to create convincing forgeries | Downloads of insurer branding assets; reconnaissance of insurer portal URLs and verification workflows |
| Distribution channel setup | Ghost brokers establish social media profiles, community group presence, and messaging platform accounts to advertise services | New social media accounts advertising insurance services; WhatsApp/Telegram groups offering cheap car insurance |

**Data Sources**: Social media monitoring, brand protection services, community intelligence

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Below-market advertising | Fraudsters advertise insurance at 30-60% below market rates through social media, community noticeboards, and word-of-mouth referrals | Insurance advertisements at prices significantly below actuarial norms; unsolicited insurance offers via messaging platforms |
| Victim onboarding | Victims provide personal details, vehicle information, and payment to the ghost broker, believing they are purchasing legitimate insurance | Personal data collection via unofficial channels; payment to personal bank accounts or cryptocurrency rather than insurer accounts |
| Document forgery | Ghost broker produces forged policy documents, certificates of insurance, and welcome packs using stolen insurer branding | Policy documents with formatting inconsistencies; certificate numbers that fail MID (Motor Insurance Database) verification |

**Target**: Price-sensitive consumers, young drivers, newly qualified drivers, migrant communities

**Data Sources**: Social media monitoring, payment transaction analysis, MID verification queries

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| MID manipulation | Some ghost brokers obtain genuine policies (using stolen identities or false information) then cancel or alter them after providing documentation to the victim | Policies cancelled within days of issuance; multiple policies issued and cancelled through same intermediary |
| Ghost portal deployment | Fraudsters create fake insurance verification websites that return seemingly valid policy confirmations when queried | Recently registered domains mimicking insurer verification portals; SSL certificates issued to domains resembling legitimate insurance brands |
| Intermediary layering | Organized groups use multiple intermediary identities and disposable contact details to obscure the operation's true scale | Multiple policies traced to same intermediary using different aliases; disposable email addresses and prepaid phone numbers on policy applications |

**Data Sources**: MID query logs, domain registration monitoring, intermediary vetting records

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Policy distribution at scale | Ghost broker distributes forged or fraudulently obtained policies to dozens or hundreds of victims simultaneously | Clusters of policies with similar characteristics (submission timing, intermediary patterns, contact details) |
| Victim exploitation | When victims attempt to make claims, they discover their policy is invalid — the ghost broker has disappeared with premiums collected | Claims rejected due to policy non-existence; victims reporting unresponsive brokers to insurers |
| Platform-as-a-service | Ghost portal operators sell access to their fake verification platforms to other ghost brokers, creating a layered criminal ecosystem | Multiple ghost brokers using the same verification portal infrastructure; dark web advertisements for "insurance portal solutions" |

**Data Sources**: Claims processing systems, customer complaints, dark web monitoring

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Premium theft | Ghost brokers pocket 100% of premiums collected from victims, with no corresponding policy underwritten | Premium payments to non-insurer accounts; revenue patterns inconsistent with legitimate intermediary commissions |
| Identity data monetization | Personal information collected during the fake application process is sold or used for additional fraud schemes | Victim PII appearing in subsequent identity fraud cases; data listed on dark web markets linked to ghost broking operations |
| Portal licensing revenue | Ghost portal operators charge subscription fees to other ghost brokers for access to fake verification infrastructure | Recurring payments between criminal actors for portal access; advertisements for insurance platform rental on underground forums |

**Data Sources**: Financial transaction monitoring, dark web monitoring, identity fraud correlation

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- Not directly mapped (insurance-specific fraud type outside payment card taxonomy)

**MITRE ATT&CK:**
- T1583.001: Acquire Infrastructure: Domains — registration of ghost portal domains
- T1566.002: Phishing: Spearphishing Link — directing victims to fraudulent insurance portals
- T1078: Valid Accounts — use of stolen identities to obtain genuine policies for resale
- T1589: Gather Victim Identity Information — collecting PII during fake application process
- T1656: Impersonation — impersonating licensed insurance intermediaries

**Group-IB Fraud Matrix:**
- Reconnaissance → Resource Development → Initial Access → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4 (Execution) when victims attempt to make claims and discover their policy is invalid, or when MID checks reveal uninsured vehicles.

**Look Left**:
- P1: Social media monitoring would detect below-market insurance advertisements
- P2: MID real-time verification at point of sale would catch forged policy numbers
- P3: Domain monitoring would identify ghost portal infrastructure during setup

**Look Right**:
- P4: Victims driving uninsured create liability for accident counterparties
- P5: Stolen personal data used for downstream identity fraud
- P5: Ghost portal infrastructure reused for other insurance fraud schemes including crash-for-cash (TP-0066)

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Ghost broker operator | Direct policy fraud — selling fake/forged insurance to consumers | High | Premiums collected: GBP 200–800 per victim |
| Ghost portal developer | Building fake insurance verification websites | Medium | GBP 2,000–10,000 per portal build |
| Portal-as-a-Service operator | Licensing ghost portal access to other brokers | Medium | GBP 500–2,000/month subscription |
| Document forger | Creating convincing policy documents, certificates, and welcome packs | High | GBP 50–200 per document set |
| Identity supplier | Providing stolen identities for policy applications | High | GBP 20–100 per identity |
| Money mule network | Receiving and laundering premium payments | High | 10–20% of collected premiums |

### Intelligence Sources
- Aviva, "Ghost broking: the emerging threat" (November 2025) — victim increase and operational patterns
- City of London Police / IFED — May 2025 arrests, February 2026 intensification month
- ABI, "Annual Fraud Report" (2025) — UK fraud topped GBP 1B in 2024
- Insurance Times (2025) — ghost portal evolution and organized crime links
- FraudOps (2026) — ghost-portal-as-a-service model intelligence
- NICB — cross-border insurance fraud patterns

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Social media monitoring for below-market insurance advertisements | Detective | Fraud Intelligence |
| P2 | Real-time MID verification at point of sale and policy issuance | Preventive | Underwriting |
| P2 | Intermediary licensing verification against FCA register | Preventive | Compliance |
| P3 | Domain monitoring for insurer brand impersonation in recently registered domains | Detective | Cyber/Brand Protection |
| P3 | Intermediary due diligence — verify disposable contact details and multiple alias patterns | Detective | Compliance |
| P4 | Pattern detection: multiple policies with same intermediary using different disposable contact details | Detective | Fraud Operations |
| P4 | Below-market premium anomaly detection | Detective | Underwriting/Fraud |
| P5 | IFED reporting and law enforcement liaison for organized ghost broking networks | Corrective | Fraud/Legal |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate for intermediary vetting and ghost broking countermeasures |
| ASSESS | Level 3 (Established) | Risk assessment incorporating ghost broking as a distinct fraud typology |
| PLAN | Level 3 (Established) | Ghost broking detection playbook; MID verification integration plan |
| ACT | Level 3 (Established) | Intermediary pattern analysis; below-market premium flagging |
| MONITOR | Level 3 (Established) | Continuous monitoring of intermediary behavior patterns and MID query anomalies |
| REPORT | Level 3 (Established) | IFED reporting protocols; victim notification procedures |
| IMPROVE | Level 3 (Established) | Post-incident analysis feeding back into intermediary vetting and social media monitoring |

---

## Detection Approaches

### Queries / Rules

```sql
-- SQL: Ghost Broker Policy Pattern Detection (DL-0188)
-- Multiple policies with same intermediary using disposable contact details and below-market premiums
SELECT
  p.intermediary_id,
  p.intermediary_name,
  COUNT(DISTINCT p.policy_id) AS policy_count,
  COUNT(DISTINCT p.contact_email) AS distinct_emails,
  COUNT(DISTINCT p.contact_phone) AS distinct_phones,
  AVG(p.premium_amount) AS avg_premium,
  m.market_avg_premium,
  (AVG(p.premium_amount) / m.market_avg_premium * 100) AS premium_pct_of_market,
  COUNT(DISTINCT CASE WHEN p.contact_email LIKE '%@protonmail%'
    OR p.contact_email LIKE '%@guerrillamail%'
    OR p.contact_email LIKE '%@tempmail%' THEN p.policy_id END) AS disposable_email_policies
FROM insurance_policies p
JOIN market_premium_benchmarks m ON p.risk_category = m.risk_category
WHERE p.issue_date >= DATEADD(DAY, -90, CURRENT_DATE)
  AND p.premium_amount < (m.market_avg_premium * 0.70)
GROUP BY p.intermediary_id, p.intermediary_name, m.market_avg_premium
HAVING COUNT(DISTINCT p.policy_id) >= 5
  AND (COUNT(DISTINCT p.contact_email) > COUNT(DISTINCT p.policy_id) * 0.8
       OR disposable_email_policies >= 3)
ORDER BY policy_count DESC
```

```splunk
`comment("Splunk SPL: Ghost Portal Infrastructure Detection — DL-0189")`
`comment("Insurance verification portals on recently registered domains")`
index=flame_web sourcetype=flame:dns_proxy
  (query="*insurance*verify*" OR query="*policy*check*" OR query="*insurance*confirm*")
| lookup domain_age_lookup domain AS query OUTPUT domain_registered_date
| eval domain_age_days = round((now() - strptime(domain_registered_date, "%Y-%m-%d")) / 86400)
| where domain_age_days < 90
| stats count AS query_count, dc(src_ip) AS unique_requestors,
        values(query) AS domains BY domain_registered_date
| where query_count >= 10
| sort - query_count
```

### Behavioral Analytics

- Intermediary submitting multiple policies with rotating disposable contact details (email, phone)
- Premiums consistently 30-60% below market average for the risk category
- Policies cancelled or lapsed within days of issuance
- MID queries from recently registered domains mimicking insurer verification portals
- Clusters of policies from same intermediary with different customer identities but similar submission patterns

### Cross-Team Correlation

- **Fraud Operations + Underwriting**: Below-market premium patterns correlated with intermediary behavior anomalies
- **Cyber/Brand Protection + Fraud**: Ghost portal domain registration correlated with policy fraud patterns
- **Fraud + Law Enforcement (IFED)**: Pattern intelligence shared for organized crime network disruption

---

## Operational Evidence

### EV-TP0074-2026-001: Ghost Broking Victim Surge 2025

- **Source**: Aviva (November 2025); ABI (2025)
- **Key Findings**: Ghost broking victims increased 93% in 2025 compared to prior year, driven by cost-of-living pressures making below-market premiums attractive. UK fraud losses topped GBP 1 billion in 2024. Young drivers and newly qualified drivers are disproportionately targeted through social media channels.
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High

### EV-TP0074-2026-002: City of London Police Ghost Broking Arrests

- **Source**: City of London Police / IFED (May 2025)
- **Key Findings**: City of London Police arrested multiple individuals involved in organized ghost broking operations in May 2025. Arrests followed intelligence-led operations targeting networks selling fake motor insurance through social media platforms. IFED designated February 2026 as a ghost broking intensification month with increased enforcement activity.
- **CFPF Phase Coverage**: P4–P5
- **Confidence**: High

### EV-TP0074-2026-003: Ghost Portal Evolution

- **Source**: Insurance Times (2025); FraudOps (2026)
- **Key Findings**: Ghost broking has evolved beyond individual operators forging documents to include organized groups building and selling entire fake insurance verification portal platforms. These "ghost portals" enable other fraudsters to verify fake policies against convincing but fraudulent databases, adding a fraud-as-a-service layer to insurance fraud. This mirrors the platform-as-a-service evolution seen in other fraud typologies (PhaaS, RaaS).
- **CFPF Phase Coverage**: P3–P5
- **Confidence**: Medium-High

---

## References

- Aviva, "Ghost broking: the scale and impact of fake insurance" (November 2025) — victim statistics and operational patterns
- City of London Police / IFED, "Ghost broking arrests and enforcement activity" (May 2025) — law enforcement operations
- Insurance Times, "Ghost portals: the next evolution in insurance fraud" (2025) — ghost-portal-as-a-service model
- ABI, "Annual Fraud Report 2024" (2025) — UK fraud losses exceeding GBP 1 billion
- FraudOps, "Insurance fraud threat landscape" (2026) — ghost portal FaaS intelligence
- NICB, "Insurance fraud indicators and red flags" — cross-border insurance fraud patterns

---

## Analyst Notes

Ghost broking represents a unique fraud typology where the primary victim is the consumer, not the insurer — victims believe they have legitimate insurance coverage until they need to make a claim or are stopped by police. This creates a dual harm: financial loss from the stolen premium and legal jeopardy from driving uninsured.

The evolution toward ghost-portal-as-a-service mirrors platform-as-a-service trends across the fraud ecosystem. When fraudsters begin selling tools and infrastructure to other fraudsters rather than directly defrauding consumers, it signals maturation of the typology and exponential scaling potential.

Detection is challenging because ghost broking operates largely outside insurer systems until a claim is filed. The most effective detection points are: (1) intermediary behavior analysis at policy submission, (2) MID verification at multiple touchpoints, and (3) social media monitoring for below-market advertising. Insurers should consider real-time MID checking APIs that consumers can use independently to verify their coverage.

The connection to organized crime networks means ghost broking should not be treated as a standalone insurance fraud problem. Intelligence sharing between insurers, IFED, and the broader financial crime community is essential for network disruption. The February 2026 IFED intensification month model provides a template for coordinated enforcement.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-27 | FLAME Project | Initial submission — sourced from Aviva, City of London Police, Insurance Times, ABI, FraudOps, NICB intelligence |
