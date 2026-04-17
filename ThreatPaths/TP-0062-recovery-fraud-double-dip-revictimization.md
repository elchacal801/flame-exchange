# TP-0062: Recovery Fraud — Double-Dip Re-victimization

```yaml
---
id: TP-0062
title: "Recovery Fraud — Double-Dip Re-victimization"
category: ThreatPath
date: 2026-03-22
author: "FLAME Project"
source: "UNODC Organized Fraud Issue Paper (Vienna, 2024)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - recovery-fraud
  - impersonation
  - advance-fee-fraud
  - social-engineering
sector:
  - cross-sector
  - banking
  - investment
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 72
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1589.001  # Gather Victim Identity Information: Credentials
  - T1566.002  # Phishing: Spearphishing Link
  - T1656      # Impersonation
ft3_tactics: ["FTA001", "FT007.009", "FT016"]
mitre_f3: ["F1020.002", "F1031", "F1032", "F1025", "F1040", "T1598", "T1660"]
groupib_stages:
  - "Reconnaissance"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 4"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0011
    relationship: feeds-into
  - id: TP-0017
    relationship: feeds-into
  - id: TP-0027
    relationship: enhances
  - id: TP-0065
    relationship: shares-infrastructure
regulatory_refs:
  - REG-UNODC-ORGANIZED-FRAUD-2024
  - REG-FINCEN-AML
  - REG-FBI-IC3
baseline_ids:
  - BL-0031
geopolitical_timing: none
nation_state_nexus: none
tags:
  - unodc
  - unodc-organized-fraud-2024
  - recovery-fraud
  - double-victimization
  - lead-list
  - victim-database
  - advance-fee
  - organized-crime-group
---
```

## Summary

Recovery fraud is an organized crime model in which victims of prior fraud (investment scams, romance fraud, pig butchering) are systematically re-contacted by actors posing as asset recovery agents, lawyers, law enforcement officials, or government bodies who claim they can recover the victim's lost funds — for an upfront fee. The UNODC identifies this as a distinct organized fraud operation with separate infrastructure from the initial fraud, targeting an identifiable victim population using traded "lead lists" of prior fraud complainants. Recovery fraud exploits the emotional vulnerability and financial desperation of already-defrauded individuals, often resulting in substantial secondary losses.

**Distinction from upstream TPs**: TP-0011 (Romance Scam) and TP-0017 (Pig Butchering) document the initial fraud schemes. TP-0062 documents the distinct second-stage organized crime operation that re-targets those same victims through entirely separate infrastructure and impersonation narratives.

## Threat Path Hypothesis

> **Hypothesis**: Organized criminal groups acquire or compile databases of prior fraud victims ("suckers lists" / "lead lists") and systematically re-contact them posing as recovery agents, lawyers, regulatory officials, or law enforcement. The victim's known loss amount, fraud type, and emotional state are used to craft highly targeted recovery narratives. The operation runs from separate infrastructure — often different call centers, different OCGs, different jurisdictions — than the initial fraud. Victims pay upfront fees, retainer deposits, or "tax clearance" charges, none of which result in any recovery. Some victims are cycled through multiple recovery fraud operations, each claiming the previous recovery agent was fraudulent but that they represent the legitimate recovery path.

**Confidence**: Medium-High — UNODC documents this as a recognized organized fraud pattern. FBI IC3 and FTC have reported on recovery fraud targeting investment and romance scam victims. The pattern is well-established but quantitative data on organized crime group structures is limited.

**Estimated Impact**: $5,000–$500,000 per victim (secondary losses). Victims who lost $100K+ to initial fraud are prime targets and may pay $10K–$100K+ in recovery fees. Aggregate losses are difficult to separate from initial fraud reporting.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Lead list acquisition | OCG acquires databases of prior fraud victims from dark web markets, co-offender networks, or compiled from public complaint records, court filings, and social media posts about fraud victimization | Victim reports contact from unknown parties who know details of their prior fraud loss; trading of victim databases on dark web forums |
| Victim profiling | OCG researches individual victims to determine loss amount, fraud type, emotional vulnerability, and financial capacity for secondary extraction | Targeted outreach referencing specific details of the victim's prior fraud experience; contact timed to periods of peak frustration (post-complaint, post-failed-investigation) |
| Impersonation infrastructure setup | OCG creates spoofed websites, fake law firm websites, fake government agency portals, and spoofed caller ID infrastructure to impersonate recovery entities | Domain registrations mimicking regulatory bodies or law firms; caller ID spoofing from numbers associated with legitimate recovery services |

**Data Sources**: Dark web monitoring for lead list trading, domain registration monitoring, customer complaint database cross-referencing, call center inbound logs

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Unsolicited recovery outreach | OCG contacts victim via phone, email, or social media claiming to represent a recovery service, law firm, or government body that can recover their lost funds | Unsolicited contact referencing specific prior fraud loss details; caller claims affiliation with government agency, law firm, or international recovery body |
| Authority impersonation | Actors impersonate legitimate entities — FBI asset recovery units, FTC, SEC, INTERPOL, attorneys, or fintech companies — to establish credibility | Spoofed caller ID matching known government numbers; fake credentials or case numbers; professional-appearing websites with no verifiable registration |
| Urgency and scarcity pressure | Claims that a recovery window is closing, seized funds will be redistributed, or that the victim must act within a specific timeframe | Time-pressure language in communications; claims that recovered funds will be released to other victims if not claimed |

**Target**: Individual consumers who have previously reported fraud losses

**Data Sources**: Customer complaint databases, call center recordings, email security logs, social media monitoring

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Trust building with "evidence" | OCG provides fabricated case numbers, fake court documents, forged wire transfer confirmations, or screenshots of "recovered" funds to build victim confidence | Documents with formatting inconsistencies; case numbers that don't validate; recovery amounts that exactly match the victim's reported loss |
| Staged progress updates | OCG provides regular status updates on the "recovery process" to maintain engagement and justify incremental fee requests | Multiple small fee requests over weeks/months; escalating payment demands as "recovery progresses" |
| Fee justification narratives | OCG explains upfront fees as tax clearance, anti-money-laundering compliance, insurance bonding, legal retainers, or international wire transfer fees | Payment requests to personal accounts rather than business accounts; fees described using compliance terminology without verifiable regulatory basis |

**Data Sources**: Customer correspondence analysis, payment destination monitoring, document verification systems

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Advance fee extraction | Victim pays upfront fees via wire transfer, cryptocurrency, gift cards, or prepaid debit cards for purported recovery services | Payments to unfamiliar accounts, often international; requests for payment via gift cards or cryptocurrency; multiple sequential payments of increasing amounts |
| Cascading recovery fraud | After initial recovery fraud fails, victim is contacted by a second "recovery" operation claiming the first was fraudulent — perpetuating the cycle | Same victim receiving multiple recovery fraud approaches from different entities; victim reporting having paid multiple recovery agents |
| Information harvesting | OCG collects additional personal and financial information during the recovery process, enabling future identity theft or additional fraud targeting | Requests for bank account details, SSN, passport copies under the guise of verifying identity for fund release |

**Data Sources**: Transaction monitoring, wire transfer logs, cryptocurrency analytics, customer complaint patterns

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Mule account cashout | Fees collected through money mule accounts and rapidly withdrawn or converted to cryptocurrency | Payments flowing to accounts with mule-pattern activity; rapid withdrawal following receipt of victim payments |
| Lead list recycling | Victim information from the recovery fraud operation is sold or traded to other OCGs for additional re-targeting | Same victim appearing in multiple complaint records for recovery fraud from different entities over time |
| Cross-OCG revenue sharing | Lead list providers receive percentage of recovery fraud proceeds as commission, creating incentive to compile and sell higher-quality victim databases | Financial flows between initial fraud OCGs and recovery fraud OCGs; commission-style payments tied to successful extraction amounts |

**Data Sources**: Payment rail analytics, blockchain analysis, dark web monitoring, cross-institutional complaint correlation

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering
- FT007.009: Impersonation of authority
- FT016: Advance fee fraud

**MITRE ATT&CK:**
- T1589.001: Gather Victim Identity Information — harvesting prior fraud victim details
- T1566.002: Spearphishing Link — targeted outreach with recovery fraud links
- T1656: Impersonation — posing as law enforcement, attorneys, regulators

**Group-IB Fraud Matrix:**
- Reconnaissance → Trust Abuse → End-user Interaction → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4 (Execution) when victim realizes no recovery is forthcoming and reports the secondary fraud.

**Look Left** (what did you miss before discovery?):
- P1: Dark web monitoring for lead list trading would identify victim databases being compiled and sold
- P2: Proactive monitoring of inbound contact to customers who recently filed fraud complaints could catch recovery fraud outreach early
- P3: Document verification on purported recovery paperwork would reveal fabrication

**Look Right** (what comes next after discovery?):
- Victim information from recovery fraud may be sold again for tertiary targeting
- Personal/financial information harvested during recovery fraud process enables identity theft
- Lead list providers adjust and re-sell updated victim databases to new OCGs

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Lead list broker | Compiled databases of fraud victims with loss amounts, contact details, fraud type | Medium | $0.50–$5.00 per record depending on data richness |
| Call center operator | Telephone outreach impersonating recovery agents | High | Salaried or commission-based (10–20% of extracted fees) |
| Document forger | Fabricated court orders, government letters, wire confirmations | High | $50–$500 per document |
| Caller ID spoofer | Infrastructure to spoof legitimate government/law firm numbers | High | $50–$200/month subscription (e.g., iSpoof model) |

### Tool Ecosystem
- Caller ID spoofing services (CaaS model)
- Document template generators for fake legal/government correspondence
- CRM-style victim tracking systems for managing multi-victim campaigns
- Lead list aggregation tools scraping complaint databases and social media

### Underground Marketplace Presence
- Dark web forums: victim lead lists traded alongside other PII datasets
- Telegram fraud channels: recovery fraud "scripts" and playbooks shared
- Criminal forums: co-offender recruitment for call center and mule roles

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor dark web for lead list trading mentioning institutional customers | Detective | Cyber/Threat Intel |
| P2 | Proactive outreach to recent fraud victims warning about recovery fraud | Preventive | Fraud/Customer Protection |
| P2 | Detect and flag inbound contact to recently-defrauded customers from unfamiliar sources | Detective | Fraud Operations |
| P3 | Provide customers with verification channels to confirm legitimacy of recovery contacts | Preventive | Customer Service |
| P4 | Transaction monitoring rules for payments from known fraud victims to new unfamiliar recipients | Detective | Fraud/AML |
| P5 | Cross-institutional complaint correlation to identify recovery fraud campaigns targeting multiple victims | Detective | Industry Partnerships |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive recognition that fraud victim protection extends beyond initial fraud recovery |
| ASSESS | Level 3 (Established) | Risk assessment incorporating recovery fraud as distinct threat to prior fraud victims |
| PLAN | Level 3 (Established) | Recovery fraud prevention integrated into victim support protocols |
| ACT | Level 3 (Established) | Monitoring of inbound contact patterns to recently-defrauded customers |
| MONITOR | Level 4 (Advanced) | Cross-institutional correlation of recovery fraud complaints; dark web lead list monitoring |
| REPORT | Level 3 (Established) | Recovery fraud reported as distinct category from initial fraud in SAR filings |
| IMPROVE | Level 3 (Established) | Feedback loop from recovery fraud cases to improve initial fraud victim warning protocols |

---

## Detection Approaches

### Queries / Rules

```sql
-- Detect potential recovery fraud contact: payments from customers
-- who filed fraud complaints in preceding 90 days to new unfamiliar recipients
SELECT
    t.customer_id,
    t.transaction_date,
    t.amount,
    t.recipient_account,
    c.complaint_date,
    c.original_loss_amount,
    c.fraud_type AS original_fraud_type
FROM transactions t
JOIN fraud_complaints c ON t.customer_id = c.customer_id
WHERE c.complaint_date >= DATEADD(day, -90, t.transaction_date)
  AND t.recipient_account NOT IN (
    SELECT DISTINCT recipient_account
    FROM transactions
    WHERE customer_id = t.customer_id
      AND transaction_date < c.complaint_date
  )
  AND t.amount > 500
ORDER BY t.transaction_date DESC;
```

### Behavioral Analytics

- Customers who filed fraud complaints within 90 days initiating new wire transfers to previously unseen recipients
- Payment patterns showing escalating amounts to the same recipient over 2–4 weeks (staged fee extraction)
- Multiple customers from the same original fraud complaint sending payments to the same recovery fraud recipient

### Cross-Team Correlation

- **Fraud + Customer Service**: Correlate complaint records with subsequent outbound payment activity
- **Fraud + AML**: Recovery fraud fees flowing to mule accounts with layering patterns
- **Fraud + Threat Intel**: Dark web monitoring for lead lists containing institutional customer PII

---

## Operational Evidence

### EV-TP0062-2026-001: UNODC Organized Fraud Typology — Recovery Fraud

- **Source**: UNODC Organized Fraud Issue Paper (Vienna, 2024), Chapter II — Consumer Investment Fraud
- **Key Finding**: "the victim may be targeted again by the same or other offenders, who in some cases claim to have an affiliation to a legitimate body that is able to trace and recover the lost money, but the victim is asked to pay an upfront fee"
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: Medium-High
- **Summary**: UNODC identifies recovery fraud as a distinct organized crime pattern within the consumer investment fraud category. The paper documents that recovery fraud operators may be from the same OCG that perpetrated the initial fraud or from separate OCGs that acquire victim databases. This confirms recovery fraud as a standalone organized crime operation with its own infrastructure, not merely a continuation of the initial scheme.

---

## References

- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Chapter II, Consumer Investment Fraud section on recovery fraud
- FBI IC3, "2023 Internet Crime Report" — recovery fraud statistics and victim patterns
- FTC, "Consumer Sentinel Network Data Book 2023" — recovery/refund fraud complaint trends
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) — organized fraud re-victimization patterns
- FBI IC3, "2025 Internet Crime Report" — recovery fraud statistics and loss data. [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)
- FBI IC3, PSA250813 (August 13, 2025) — fictitious law firms targeting cryptocurrency scam victims. [Link](https://www.ic3.gov/PSA/2025/PSA250813)
- FBI IC3, PSA250418 (April 18, 2025) — scammers impersonating the IC3 as a recovery fraud vector. [Link](https://www.ic3.gov/PSA/2025/PSA250418)

---

## Analyst Notes

Recovery fraud represents one of the most operationally distinctive UNODC findings for FLAME enrichment because it documents a self-reinforcing fraud ecosystem: initial fraud creates the victim pool, which is then monetized again through recovery fraud. The existence of traded "lead lists" or "suckers lists" (UNODC terminology) means that a single victim's data may pass through multiple OCGs over time.

Key operational insight: the separation between initial fraud OCGs and recovery fraud OCGs means that disrupting the initial scheme does not necessarily disrupt the recovery fraud pipeline. Separate disruption strategies are needed for the lead list ecosystem and the recovery fraud call center infrastructure.

Regional patterns: UNODC documents recovery fraud operations in West Africa (targeting romance scam victims), South-East Asia (targeting pig butchering victims), and Eastern Europe (targeting investment scam victims).

**FBI IC3 2025 Annual Report:** Recovery scams generated 10,516 complaints and $1.4 billion in losses, making it one of the largest IC3 loss categories. Losses may also include losses from the original scam that prompted contact with the recovery entity.

**PSA250813 (August 13, 2025):** Fictitious law firms targeting cryptocurrency scam victims combine multiple exploitation tactics while offering to recover funds. [Link](https://www.ic3.gov/PSA/2025/PSA250813)

**PSA250418 (April 18, 2025):** FBI warns of scammers impersonating the IC3 itself as a recovery fraud vector. [Link](https://www.ic3.gov/PSA/2025/PSA250418)

Recovery scams show increasing government impersonation variants, where actors pose as federal agencies to add authority to recovery claims.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-22 | FLAME Project | Initial submission — sourced from UNODC Organized Fraud Issue Paper (Vienna, 2024) |
