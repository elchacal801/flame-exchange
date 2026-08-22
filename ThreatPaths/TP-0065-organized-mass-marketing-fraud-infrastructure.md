# TP-0065: Organized Mass-Marketing Fraud Infrastructure (Boiler Rooms & Lead Lists)

```yaml
---
id: TP-0065
title: "Organized Mass-Marketing Fraud Infrastructure (Boiler Rooms & Lead Lists)"
category: ThreatPath
date: 2026-03-22
last_reviewed: 2026-03-29
author: "FLAME Project"
source: "UNODC Organized Fraud Issue Paper (Vienna, 2024)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - social-engineering
  - impersonation
  - vishing
  - robodialling-fraud
  - advance-fee-fraud
  - investment-scam
  - fraud-as-a-service
sector:
  - cross-sector
  - banking
  - investment
  - telecommunications
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "fraud-infrastructure"
primary_phase: "P1"
short_name: "Boiler Room Infra"
confidence_score: 78
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1589.001  # Gather Victim Identity Information: Credentials
  - T1566.003  # Phishing: Spearphishing via Service
  - T1656      # Impersonation
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FT007.009", "FT016", "FT031"]
mitre_f3: ["F1032", "F1020.002", "F1031", "F1034", "F1040.002", "F1018", "F1025", "T1598", "T1660"]
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
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
  - id: TP-0012
    relationship: shares-infrastructure
  - id: TP-0058
    relationship: related-to
  - id: TP-0054
    relationship: shares-infrastructure
  - id: TP-0062
    relationship: enables
regulatory_refs:
  - REG-UNODC-ORGANIZED-FRAUD-2024
  - REG-FINCEN-AML
  - REG-INTERPOL-GFFTA
  - REG-WCI-2024
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - unodc
  - unodc-organized-fraud-2024
  - boiler-room
  - lead-list
  - robodialling
  - mass-marketing-fraud
  - sim-farm
  - telemarketing-fraud
  - crime-as-a-service
  - organized-crime-group
  - wci-geographic-attribution
---
```

## Summary

Organized mass-marketing fraud infrastructure encompasses the boiler room operations, lead list ecosystems, robodialling infrastructure, and SIM farm devices that serve as the shared demand-generation engine feeding multiple downstream fraud types. The UNODC identifies mass-marketing as a cross-cutting facilitator of organized fraud, documenting call center operations (boiler rooms) that employ salaried agents, use "lead lists" of targeted victims (including "suckers lists" of previously defrauded individuals), and leverage telecommunications infrastructure (SIM farms, VoIP spoofing, robodialling) for high-volume victim contact. This infrastructure operates as a discrete business layer — separate from the fraud execution itself — and may serve multiple fraud types simultaneously (investment scams, impersonation, recovery fraud, tech support fraud).

**Distinction from TP-0058**: TP-0058 (Scam Compound Operations) covers the physical compound model in South-East Asia where trafficked individuals perpetrate fraud. TP-0065 documents the broader mass-marketing infrastructure layer that UNODC identifies as a cross-cutting facilitator across all regions — including virtual boiler rooms, offshore call centers, and the lead list/robodialling ecosystem that enables organized fraud at scale.

## Threat Path Hypothesis

> **Hypothesis**: A shared mass-marketing infrastructure layer — comprising boiler rooms, lead list brokers, caller ID spoofing services, SIM farm operators, and robodialling platforms — operates as the demand-generation engine for organized fraud. This infrastructure layer functions as a crime-as-a-service marketplace where fraud operators can procure victim contact capabilities without building their own telecommunications infrastructure. OCGs that control this infrastructure serve multiple fraud campaigns simultaneously, creating a high-value disruption target: dismantling a single boiler room or lead list broker can degrade multiple downstream fraud operations. UNODC documents that these operations adopt formal workforce structures with salaried employees, office space, and operational hierarchies.

**Confidence**: Medium-High — UNODC documents multiple case studies. INTERPOL operations have targeted mass-marketing fraud infrastructure. The iSpoof takedown (59,000 users, €3.7M revenue) demonstrates the scale.

**Estimated Impact**: Individual boiler rooms can generate $1M–$50M+ in annual fraud revenue. The shared infrastructure layer collectively enables billions in annual organized fraud across all categories.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Lead list compilation | OCG compiles or acquires databases of potential victims from multiple sources: purchased marketing lists, scraped social media profiles, stolen CRM databases, public complaint records, and "suckers lists" of prior fraud victims | Trading of lead lists on dark web forums; lead lists containing institutional customer PII; lists segmented by demographics (age, income, prior fraud history) |
| Target market research | OCG researches demographic vulnerabilities, seasonal opportunities (tax season, investment cycles), and regional targeting effectiveness | Call campaigns coinciding with tax deadlines, investment product launches, or economic uncertainty events |
| Infrastructure procurement | OCG acquires SIM farm devices, VoIP accounts, caller ID spoofing services, and office space for call center operations | Bulk SIM card purchases; VoIP account registrations from anonymous payment methods; office space leased in areas with low-cost labor and weak telecom regulation |

**Data Sources**: Dark web monitoring, telecom CDR analysis, SIM registration databases, commercial real estate intelligence

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| High-volume outbound calling | Call center agents make hundreds of calls per day using scripts tailored to the specific fraud type (investment opportunity, tax authority impersonation, tech support, recovery service) | Burst calling patterns from sequential phone numbers; short average call duration (most calls rejected); geographic origin mismatch between caller and claimed identity |
| Robodialling and auto-dialing | Automated systems dial thousands of numbers per hour, playing pre-recorded messages or connecting answered calls to live agents | High-volume outbound calls with identical timing patterns; pre-recorded message content across multiple recipients; IVR-style interactions before live agent connection |
| Spam communications | Mass email, SMS, and social media messages containing fraudulent offers, impersonation narratives, or phishing links | Burst messaging from new or recently activated accounts; SMS from SIM farm-associated numbers; email campaigns with consistent formatting across different sender addresses |
| Caller ID spoofing | Spoofing services make outbound calls appear to originate from legitimate numbers — government agencies, banks, local numbers matching the victim's area code | Calls displaying legitimate institutional numbers that don't match actual call routing; high volume of calls from numbers registered to government agencies |

**Target**: Individual consumers and businesses targeted by demographic, geographic, or prior victimization profile

**Data Sources**: Telecom CDR, SMS gateway logs, email security platforms, caller ID verification services (STIR/SHAKEN)

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Script-driven social engineering | Call agents follow detailed scripts designed to establish authority, create urgency, and overcome objections; scripts are refined based on success rates | Consistent language patterns across calls from the same campaign; scripted escalation procedures when victim expresses doubt |
| Warm transfer to "closers" | Initial call agents qualify victims and transfer promising leads to senior agents ("closers") who specialize in extracting payments | Multi-stage call patterns: short initial call followed by longer call from different number; escalation to "supervisor" or "specialist" |
| Repeat contact and grooming | For investment and romance fraud, initial contact is followed by scheduled callbacks to build rapport and trust over days or weeks | Regular scheduled call patterns to the same victim; progressively longer call durations indicating relationship building |

**Data Sources**: Call center analytics, call recording analysis, customer complaint patterns

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Payment extraction | Victim directed to make payment via wire transfer, cryptocurrency, gift cards, or prepaid debit cards, depending on the fraud narrative | Payments directed to accounts controlled by the OCG or downstream mule networks; payment method matches known patterns for specific fraud types |
| Multi-victim campaigns | Boiler room operates continuous campaigns across multiple fraud types, cycling through lead lists and scripts based on success rates | Consistent payment destinations across multiple victims contacted from the same number ranges; fraud type diversity from the same infrastructure |
| Victim data harvesting | Personal and financial information provided by victims during the interaction is recorded for use in identity fraud or lead list re-sale | Victim PII appearing in subsequent dark web data sales; identity fraud attempts using information provided during fraudulent calls |

**Data Sources**: Transaction monitoring, payment rail analytics, customer complaint correlation, call center recordings

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Mule network cashout | Payments extracted from victims flow through money mule accounts before reaching OCG principals | Mule account activity patterns correlated with boiler room calling campaigns; payment timing aligned with call center operating hours |
| CaaS revenue model | Infrastructure operators charge downstream fraud operators per-call, per-lead, or as subscription fees for access to spoofing/robodialling platforms | Subscription payment patterns to VoIP and spoofing service providers; per-use billing models for caller ID spoofing services |
| Lead list recycling | Successful victim contacts and their details are compiled into higher-value lead lists for resale to other OCGs, including recovery fraud operators | Victim details from mass-marketing campaigns appearing in recovery fraud targeting; lead lists with enriched fields (amount paid, fraud type responded to) |

**Data Sources**: Payment rail analytics, dark web monitoring, telecom billing records, blockchain analysis

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering
- FT007.009: Impersonation of authority
- FT016: Advance fee fraud
- FT031: Telecom abuse

**MITRE ATT&CK:**
- T1589.001: Gather Victim Identity Information — lead list compilation
- T1566.003: Phishing via Service — mass communication channels
- T1656: Impersonation — caller ID spoofing and authority impersonation
- T1583.001: Acquire Infrastructure — VoIP, SIM farms, spoofing services

**Group-IB Fraud Matrix:**
- Reconnaissance → Resource Development → Trust Abuse → End-user Interaction → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 2 (Initial Access) through telecom fraud detection or at Phase 4 (Execution) through victim complaints.

**Look Left**:
- P1: Dark web monitoring for lead list trading and boiler room recruitment ads
- P1: Telecom monitoring for bulk SIM registrations and VoIP account creation patterns
- P1: Intelligence sharing with telecom providers on SIM farm detection

**Look Right**:
- P5: Mule networks receiving payments from boiler room campaigns serve multiple fraud types
- Lead lists generated from this infrastructure feed recovery fraud operations (TP-0062)
- Victim PII harvested during calls enables downstream identity fraud campaigns

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Lead list broker | Victim/target databases segmented by demographics, net worth, prior fraud history | High | $0.10–$5.00 per record |
| Caller ID spoofing provider | CaaS platforms for spoofing outbound caller ID to match legitimate institutions | High | $50–$200/month subscription (iSpoof model: €150/month) |
| SIM farm operator | Bulk SIM card infrastructure for mass outbound SMS and voice calls | Medium | $1,000–$5,000 for hardware; $50–$200/month for SIM cards |
| Call center agent | Salaried or commission-based callers following fraud scripts | High | $500–$2,000/month salary + commission |
| Script developer | Fraud call scripts and objection-handling playbooks | Medium | $200–$1,000 per script set |

### Tool Ecosystem
- VoIP platforms with minimal identity verification
- Auto-dialer and robodialling software
- SIM farm hardware (multi-SIM devices)
- CRM systems repurposed for victim tracking and lead management
- Call recording and quality monitoring tools (mirroring legitimate call center operations)

### Underground Marketplace Presence
- Dark web forums: lead list trading, boiler room setup guides, spoofing service advertisements
- Telegram channels: recruitment of call center agents ("vacancy" posts for customer service roles in "financial companies")
- Criminal forums: script sharing, success rate optimization discussions

### Intelligence Sources
- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Cross-cutting facilitators: Mass-marketing
- Europol, "Action against criminal website that offered 'spoofing' services to fraudsters: 142 arrests", 24 November 2022 (iSpoof takedown)
- Jienan Liu et al., "Understanding, measuring, and detecting modern technical support scams", IEEE, 2023

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Dark web monitoring for lead list trading and boiler room recruitment | Detective | Threat Intel |
| P2 | STIR/SHAKEN caller ID verification to detect spoofed calls | Preventive | Telecommunications |
| P2 | Customer education campaigns on recognizing unsolicited calls from spoofed numbers | Preventive | Customer Protection |
| P3 | Behavioral analytics on inbound call patterns to customer accounts following mass-marketing campaigns | Detective | Fraud Operations |
| P4 | Transaction holds on payments to unfamiliar recipients initiated during or shortly after inbound call contact | Preventive | Fraud/Payments |
| P5 | Cross-institutional intelligence sharing on boiler room campaigns and associated payment destinations | Detective | Industry Partnerships |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive recognition of mass-marketing fraud as enabling infrastructure, not just individual incidents |
| ASSESS | Level 3 (Established) | Risk assessment incorporating telecom abuse vectors and lead list exposure |
| PLAN | Level 3 (Established) | Cross-sector response plan spanning financial institution, telecom provider, and law enforcement |
| ACT | Level 3 (Established) | Caller ID verification, inbound contact monitoring, and payment hold capabilities |
| MONITOR | Level 4 (Advanced) | Real-time telecom intelligence sharing; dark web lead list monitoring |
| REPORT | Level 3 (Established) | Consolidated reporting linking mass-marketing contact patterns to fraud outcomes |
| IMPROVE | Level 3 (Established) | Feedback from mass-marketing fraud cases to telecom providers for infrastructure disruption |

---

## Wangiri & SIM Box Fraud — Distinct Telecom Infrastructure Threats

### Wangiri (One-Ring) Fraud

Wangiri fraud operates on a fundamentally different model than outbound boiler room calling. Rather than initiating calls to victims, fraudsters use automated systems to make short calls terminated after one ring, enticing recipients to return the call to premium-rate numbers. The fraudster shares revenue with the premium-rate number operator. AI-powered auto-dialing now enables Wangiri at industrial scale.

**Distinction from TP-0065**: TP-0065 covers outbound calling infrastructure (boiler rooms, lead lists, robodialling). Wangiri is inbound-lure fraud — the victim initiates the revenue-generating call. See TP-0071 for comprehensive IRSF/Wangiri coverage.

### SIM Box Fraud

SIM box fraud uses devices containing multiple prepaid SIM cards to convert international calls into local traffic, bypassing international termination rates. This deprives telecom operators of interconnect revenue. SIM boxes are distinct from SIM swap attacks (TP-0008) — SIM swap targets individual account takeover; SIM box targets carrier revenue at scale.

**Global telecom fraud context**: Total losses reached $41.82 billion by 2025, nearly a $3 billion increase in just two years (CFCA).

## Detection Approaches

### Queries / Rules

```sigma
title: Mass-Marketing Fraud Burst Calling Pattern
status: experimental
description: Detects burst patterns from potential SIM farm or robodialling infrastructure
logsource:
    product: telecom
    service: cdr
detection:
    selection:
        call_direction: inbound
        call_duration|lt: 30
    timeframe: 1h
    condition: selection | count(source_number) by destination_number > 3
        AND selection | count(distinct destination_number) by source_number_prefix > 50
fields:
    - source_number
    - destination_number
    - call_duration
    - caller_id_verification_status
level: medium
```

### Behavioral Analytics

- Burst inbound calling patterns: high volume of short-duration calls from sequential numbers to customer base
- Caller ID verification failures (STIR/SHAKEN attestation level C or unattested)
- Customer payment activity correlated with inbound call timing from unknown numbers
- Geographic mismatch between caller ID display and actual call origination

### Cross-Team Correlation

- **Fraud + Telecom**: Caller ID spoofing detection correlated with subsequent fraudulent payment activity
- **Fraud + AML**: Payment destinations from mass-marketing fraud campaigns linked to mule network patterns
- **Fraud + Threat Intel**: Dark web lead list intelligence correlated with customer complaint patterns

---

## Operational Evidence

### EV-TP0065-2026-001: UNODC Mass-Marketing Facilitator Analysis and Case Studies

- **Source**: UNODC Organized Fraud Issue Paper (Vienna, 2024), Chapter IV — Cross-cutting Facilitators: Mass-marketing; Chapter II case studies
- **Key Findings**: (1) Technical support scam case study: India-based call centers operating as discrete sub-businesses within underground economy — separate entities for calls, money laundering, and website development, all coordinated via mainstream social media. (2) iSpoof CaaS platform: 59,000 users, €3.7M revenue, caller ID spoofing service enabling mass impersonation fraud. (3) UNODC documents "lead lists" and "suckers lists" as critical infrastructure — prior victim databases traded and reused across multiple OCGs.
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: UNODC identifies mass-marketing as one of four cross-cutting facilitators of organized fraud. The infrastructure layer operates as a shared service across fraud types — investment, impersonation, tech support, recovery — making it a high-value disruption target. The iSpoof takedown demonstrates that CaaS infrastructure providers can be targeted to degrade capabilities across hundreds of downstream fraud operations simultaneously.

---

## References

- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Chapter IV, Mass-marketing
- Europol, "Action against criminal website that offered 'spoofing' services to fraudsters: 142 arrests", 24 November 2022 (iSpoof)
- Jienan Liu et al., "Understanding, measuring, and detecting modern technical support scams", IEEE European Symposium on Security and Privacy, 2023
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) — mass-marketing and telecom abuse trends
- TNS/CFCA, "The Telecom Fraud Landscape in 2026" (2026)

---

## Analyst Notes

The UNODC's identification of mass-marketing infrastructure as a cross-cutting facilitator is operationally significant for FLAME because it reframes individual fraud types (tech support, investment, impersonation) as downstream consumers of shared infrastructure. This has major implications for disruption strategy: targeting the infrastructure layer (boiler rooms, lead list brokers, spoofing services) can degrade multiple fraud types simultaneously.

The tech support scam case study from UNODC is particularly instructive: discrete sub-businesses operated as a vibrant underground economy on mainstream social media platforms, with call center operators, money launderers, and website builders operating as independent contractors. This mirrors the crime-as-a-service model documented in TP-0054 but at the mass-marketing infrastructure layer.

STIR/SHAKEN implementation varies significantly across jurisdictions, creating regulatory arbitrage opportunities for OCGs to originate spoofed calls from jurisdictions with weaker telecom regulation.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-22 | FLAME Project | Initial submission — sourced from UNODC Organized Fraud Issue Paper (Vienna, 2024) |
