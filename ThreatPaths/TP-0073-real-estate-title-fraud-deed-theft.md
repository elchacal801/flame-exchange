# TP-0073: Real Estate Title Fraud & Deed Theft

```yaml
---
id: TP-0073
title: "Real Estate Title Fraud & Deed Theft"
category: ThreatPath
date: 2026-03-29
last_reviewed: 2026-03-29
author: "FLAME Project"
source: "First American Title Fraud Report; HousingWire (2025); ALTA Best Practices; Virginia Deed Fraud Study (2025); NAR Fraud Advisory; CertifID Wire Fraud Report; Entrust Identity Fraud Report (2026)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - title-fraud
  - deed-theft
  - seller-impersonation
  - appraisal-fraud
sector:
  - real-estate
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "identity-synthetic"
primary_phase: "P3"
short_name: "Title/Deed Theft"
confidence_score: 80
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1656      # Impersonation
  - T1566.002  # Phishing: Spearphishing Link
  - T1078      # Valid Accounts
  - T1565      # Data Manipulation
  - T1136      # Create Account
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FT007.009", "FT011.001"]
mitre_f3: ["F1027", "F1031", "T1672"]
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
  act: "Level 4"
  monitor: "Level 3"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0006
    relationship: enables
  - id: TP-0029
    relationship: related-to
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-WCI-2024
tags:
  - title-fraud
  - deed-theft
  - seller-impersonation
  - appraisal-fraud
  - deepfake-notary
  - ai-forged-documents
  - vacant-property-fraud
  - wire-fraud-real-estate
  - remote-notarization-fraud
  - wci-geographic-attribution
---
```

## Summary

Real estate title fraud and deed theft represent a growing category of property-related fraud, with FBI data reporting $16.6 billion in total real estate fraud losses in 2024. The core scheme involves impersonating property owners -- primarily targeting vacant lots, unencumbered properties, and absentee-owner homes -- to fraudulently transfer titles or initiate sales, diverting proceeds to attacker-controlled accounts. The emergence of AI-forged documents (deeds, government IDs, notary stamps) and deepfake video notarization has dramatically lowered the barrier to executing these schemes, with Entrust reporting a 40% year-over-year increase in deepfake-related fraud attempts. Seller impersonation of vacant property owners is the most common vector, as these properties lack occupants who would notice unauthorized activity. Virginia's 2025 deed fraud legislation represents the first major legislative response, mandating enhanced identity verification for property transfers. This threat path intersects with wire fraud (TP-0006) at the monetization phase, where sale proceeds are redirected via business email compromise or fraudulent wire instructions.

## Threat Path Hypothesis

> **Hypothesis**: Criminal networks identify vacant, unencumbered, or absentee-owner properties through public county records and real estate databases. They then impersonate the property owner using AI-generated identity documents (driver's licenses, passports) and forged notarized deeds to initiate property sales or title transfers. The impersonation is facilitated by deepfake video technology that enables fraudsters to pass remote online notarization (RON) sessions, and by AI tools that generate convincing forged documents including deeds, powers of attorney, and notary stamps. Once title is transferred or a sale is initiated, proceeds are diverted to attacker-controlled accounts via wire transfer (TP-0006). The scheme exploits the fact that county recording offices typically accept documents at face value without independent identity verification, and that vacant property owners may not discover the fraud for months or years.

**Confidence**: High -- FBI loss data, First American, ALTA, and Virginia's legislative response confirm the scale and mechanics. Deepfake notarization fraud is documented by CertifID and Entrust.

**Estimated Impact**: $16.6B in total real estate fraud (FBI 2024). Individual property losses range from $50K to $5M+ depending on property value. Average wire fraud loss in real estate transactions: $150K-$250K (CertifID).

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Vacant property identification | Fraudsters search county assessor records, tax databases, and real estate platforms to identify vacant lots, properties with no mortgage (unencumbered), and absentee owners | Bulk queries to county property records; scraping of real estate listing sites for vacant/unoccupied properties; USPS change-of-address lookups |
| Owner information harvesting | PII of target property owners gathered from public records, data breaches, and social media to support impersonation | Property owner name/address lookups; social media profiling of property owners; data broker queries for owner SSN/DOB |
| Notarization process reconnaissance | Fraudsters identify title companies, notaries, and county recording offices with weak identity verification processes, particularly those offering remote online notarization (RON) | Research into RON-accepting jurisdictions; identification of title companies with minimal in-person verification requirements |

**Data Sources**: County property records access logs, title search request monitoring, real estate platform analytics

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| AI-generated identity document creation | Fraudsters use AI tools to create convincing replicas of the property owner's government-issued ID (driver's license, passport) using harvested PII and either stolen or AI-generated photos | Identity documents with AI generation artifacts in security features; documents with valid PII but synthetic biometric photos; metadata inconsistencies in document images |
| Forged deed and power of attorney preparation | AI tools generate fraudulent deeds, powers of attorney, and other title transfer documents with forged signatures and notary stamps | Documents with font/formatting inconsistencies; notary stamps that don't match registered notaries; document serial numbers that fail county validation |
| Contact information manipulation | Fraudsters create new email addresses, phone numbers, and mailing addresses associated with the property owner's name to receive communications from title companies and buyers | New email accounts created using property owner's name; phone numbers registered shortly before transaction initiation; mail forwarding requests for the property address |

**Target**: Vacant property owners, absentee owners, elderly property owners, recently deceased property owners' estates

**Data Sources**: Identity verification platform logs, document forensics tools, email/phone registration databases, county recorder submissions

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Seller impersonation and listing initiation | Fraudster contacts a real estate agent or buyer directly, posing as the property owner, to initiate a sale often at below-market price for rapid closing (DL-0186) | Property sale initiated by non-resident owner; below-market listing price on unencumbered property; seller requesting all-cash transaction with expedited closing; seller unavailable for in-person meetings |
| Remote online notarization exploitation | Fraudster uses deepfake video technology to pass RON identity verification, appearing as the property owner during video notarization sessions | RON session with audio/video quality anomalies; notarization from IP address inconsistent with owner's known location; biometric verification flags during RON session |
| Title company engagement | Fraudster engages title company and escrow services, providing forged documents and directing wire instructions to attacker-controlled accounts | New client engagement with expedited closing request; wire instructions to recently opened accounts; title company unable to reach owner through previously known contact methods |

**Data Sources**: Real estate listing platforms, RON platform logs, title company transaction records, wire instruction databases

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Fraudulent deed recording | Forged deed or title transfer document recorded at county recorder's office, officially transferring property title (DL-0187) | Deed recording with document metadata anomalies; deed filed by party not matching historical ownership records; recording followed by immediate sale listing; deed with notary credentials that don't validate |
| Sale completion and wire diversion | Property sold to legitimate buyer (often unaware of fraud), with proceeds wired to attacker-controlled bank accounts | Wire transfer to newly opened account; proceeds directed to account in different jurisdiction than property; split wire instructions directing funds to multiple accounts |
| Appraisal manipulation | In cases involving mortgage fraud, inflated appraisals generated using manipulated comparable sales data to support fraudulent property valuations | Appraisal values significantly above recent comparable sales; appraiser with no geographic presence in property area; comparable sales that cannot be independently verified |

**Data Sources**: County recorder databases, wire transfer monitoring, appraisal review systems, title insurance claim databases

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Wire transfer cash-out | Sale proceeds received via wire transfer and rapidly moved through layered accounts to prevent recovery | Wire transfers immediately forwarded to secondary accounts; currency conversion to cryptocurrency; international wire transfers from domestic property sale proceeds |
| HELOC/mortgage fraud | Fraudulently transferred title used to obtain home equity lines of credit or mortgages against the stolen property | HELOC or mortgage applications on recently transferred properties; credit applications with identity inconsistencies; multiple financial products obtained against same property in short timeframe |
| Serial property targeting | Successful scheme repeated across multiple properties, often in different jurisdictions to avoid detection pattern recognition | Same fraud TTPs applied to multiple vacant properties; common elements (email domains, phone numbers, bank accounts) across multiple property transactions in different counties |

**Data Sources**: Financial transaction monitoring, mortgage application databases, county recorder cross-jurisdiction analysis, title insurance claims

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering (seller impersonation of property owners)
- FT007.009: Impersonation of authority (forged notary stamps, government IDs)
- FT011.001: Identity theft for property transfer

**MITRE ATT&CK:**
- T1656: Impersonation -- seller impersonation of property owners
- T1566.002: Phishing: Spearphishing Link -- communication with title companies/buyers using fraudulent identity
- T1078: Valid Accounts -- use of stolen owner PII to pass verification
- T1565: Data Manipulation -- forged deeds and title documents
- T1136: Create Account -- fraudulent bank accounts for wire receipt
- T1583.001: Acquire Infrastructure: Domains -- email infrastructure for owner impersonation

**Group-IB Fraud Matrix:**
- Reconnaissance -> Resource Development -> Initial Access -> Perform Fraud -> Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4-5 (Execution/Monetization) when the legitimate property owner discovers the title transfer, or when a title insurance claim is filed.

**Look Left**:
- P1: Property owner alerting services (county recorder notifications) would detect unauthorized document filings
- P2: AI document forensics during notarization would identify forged IDs and deeds (DL-0187)
- P3: Seller impersonation pattern detection would flag non-resident owners selling vacant unencumbered properties (DL-0186)

**Look Right**:
- P4: Wire fraud (TP-0006) as the primary monetization channel for property sale proceeds
- P5: HELOC/mortgage fraud against stolen titles creates secondary financial losses
- P5: Serial property targeting across jurisdictions compounds losses and complicates investigation

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| AI document forger | Forged government IDs, deeds, notary stamps, powers of attorney | Medium | $200-$2,000 per document package |
| Deepfake video provider | Real-time deepfake video for RON sessions | Low-Medium | $500-$5,000 per session |
| Property data researcher | Identification of vacant/unencumbered target properties | High | $50-$200 per property profile |
| Wire mule network | Bank accounts for receiving and layering property sale proceeds | Medium | 5-15% of wire amount |
| Corrupt notary/insider | Complicit notaries who authenticate forged documents | Low | $1,000-$10,000 per transaction |

### Intelligence Sources
- First American, "Title Fraud: Emerging Threats and Prevention Strategies" -- seller impersonation patterns
- HousingWire, "Deed Fraud on the Rise: AI-Powered Property Theft" (2025) -- AI-generated document analysis
- ALTA, "Best Practices for Title Insurance and Settlement" -- identity verification standards
- Virginia Deed Fraud Study (2025) -- legislative response and jurisdictional analysis
- CertifID, "Wire Fraud Report: Real Estate Transaction Security" -- wire fraud intersection
- Entrust, "Identity Fraud Report" (2026) -- 40% YoY deepfake increase

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Property owner notification services for any document filings against their properties | Detective | County Recorder/Title Company |
| P1 | Title lock/freeze services preventing unauthorized title transfers without owner verification | Preventive | Title Insurance |
| P2 | AI document forensics for government IDs presented during notarization and title transfer | Detective | Title Company/Notary |
| P2 | Multi-factor identity verification for property sellers beyond document presentation | Preventive | Title Company |
| P3 | Seller impersonation pattern detection for vacant/unencumbered property sales (DL-0186) | Detective | Title Company/Fraud Analytics |
| P3 | Enhanced RON identity verification with liveness detection and deepfake detection | Preventive | RON Platform |
| P4 | Deed recording anomaly detection for AI generation indicators and metadata inconsistencies (DL-0187) | Detective | County Recorder |
| P4 | Wire verification callbacks to property owners through independently verified contact methods | Preventive | Title Company/Escrow |
| P5 | Cross-jurisdictional deed recording monitoring for serial property targeting patterns | Detective | Law Enforcement/Title Insurance |
| P5 | HELOC/mortgage application verification against recent title transfer activity | Detective | Financial Institutions |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate for enhanced identity verification in property transfers and investment in AI document forensics |
| ASSESS | Level 3 (Established) | Risk assessment identifying exposure to seller impersonation, deepfake notarization, and AI-forged documents |
| PLAN | Level 3 (Established) | Enhanced KYC roadmap for property transfers; RON security standards; cross-jurisdictional monitoring plan |
| ACT | Level 4 (Advanced) | Real-time document forensics; seller impersonation pattern detection; deepfake detection in RON sessions |
| MONITOR | Level 3 (Established) | Continuous monitoring of deed recordings, title transfer patterns, and property owner notification systems |
| REPORT | Level 3 (Established) | Incident reporting to FBI IC3, state real estate commissions, and title insurance industry databases |
| IMPROVE | Level 3 (Established) | Post-incident analysis feeding back into document verification models and seller impersonation detection rules |

---

## Detection Approaches

### Queries / Rules

```sql
-- SQL for Seller Impersonation Pattern Detection — DL-0186
-- Property sale initiated by non-resident owner of vacant/unencumbered property
-- with recent contact info changes
SELECT
  p.property_id,
  p.property_address,
  p.property_type,
  p.assessed_value,
  p.mortgage_balance,
  o.owner_name,
  o.owner_mailing_address,
  o.contact_last_updated,
  t.transaction_type,
  t.listing_price,
  t.listing_date,
  t.seller_contact_email,
  t.seller_contact_phone,
  CASE WHEN p.property_address != o.owner_mailing_address THEN 1 ELSE 0 END AS non_resident_owner,
  CASE WHEN p.mortgage_balance = 0 OR p.mortgage_balance IS NULL THEN 1 ELSE 0 END AS unencumbered,
  CASE WHEN p.occupancy_status = 'vacant' THEN 1 ELSE 0 END AS vacant_property,
  CASE WHEN o.contact_last_updated >= DATEADD(DAY, -90, CURRENT_DATE) THEN 1 ELSE 0 END AS recent_contact_change,
  (CASE WHEN p.property_address != o.owner_mailing_address THEN 1 ELSE 0 END
   + CASE WHEN p.mortgage_balance = 0 OR p.mortgage_balance IS NULL THEN 1 ELSE 0 END
   + CASE WHEN p.occupancy_status = 'vacant' THEN 1 ELSE 0 END
   + CASE WHEN o.contact_last_updated >= DATEADD(DAY, -90, CURRENT_DATE) THEN 1 ELSE 0 END
   + CASE WHEN t.listing_price < p.assessed_value * 0.85 THEN 1 ELSE 0 END) AS risk_score
FROM properties p
JOIN property_owners o ON p.property_id = o.property_id
JOIN property_transactions t ON p.property_id = t.property_id
WHERE t.transaction_type IN ('sale_listing', 'title_transfer')
  AND t.listing_date >= DATEADD(DAY, -30, CURRENT_DATE)
  AND (p.occupancy_status = 'vacant' OR p.property_address != o.owner_mailing_address)
  AND (p.mortgage_balance = 0 OR p.mortgage_balance IS NULL)
HAVING risk_score >= 3
ORDER BY risk_score DESC, t.listing_date DESC
```

```python
# Python pseudocode for Fraudulent Deed Transfer Anomaly Detection — DL-0187
# Detects deed recording with document metadata anomalies (AI generation indicators)
# on properties with no prior recent activity

import hashlib
from datetime import datetime, timedelta

def detect_fraudulent_deed_transfer(deed_record):
    """
    Analyze deed recording for fraud indicators including:
    - AI generation metadata artifacts
    - Properties with no prior activity
    - Document inconsistencies
    """
    risk_indicators = []
    risk_score = 0

    # Check 1: Document metadata anomalies (AI generation indicators)
    if deed_record.get('document_metadata'):
        metadata = deed_record['document_metadata']
        # Check for AI generation tool signatures in PDF metadata
        ai_tool_signatures = ['stable-diffusion', 'midjourney', 'dall-e',
                              'adobe-firefly', 'generative', 'ai-generated']
        creator_tool = metadata.get('creator', '').lower()
        producer_tool = metadata.get('producer', '').lower()
        for sig in ai_tool_signatures:
            if sig in creator_tool or sig in producer_tool:
                risk_indicators.append('ai_tool_in_metadata')
                risk_score += 30

        # Check for suspicious creation/modification timestamps
        if metadata.get('creation_date') and metadata.get('modification_date'):
            creation = metadata['creation_date']
            modification = metadata['modification_date']
            if (modification - creation).total_seconds() < 60:
                risk_indicators.append('rapid_document_creation')
                risk_score += 15

    # Check 2: No prior property activity in last 5 years
    if deed_record.get('prior_recordings_5yr', 0) == 0:
        risk_indicators.append('no_prior_activity')
        risk_score += 20

    # Check 3: Notary validation
    if deed_record.get('notary_commission_number'):
        if not validate_notary_commission(deed_record['notary_commission_number'],
                                          deed_record.get('notary_state')):
            risk_indicators.append('invalid_notary_commission')
            risk_score += 40

    # Check 4: Property is vacant and unencumbered
    if deed_record.get('occupancy_status') == 'vacant':
        risk_score += 15
        risk_indicators.append('vacant_property')
    if deed_record.get('mortgage_balance', 0) == 0:
        risk_score += 10
        risk_indicators.append('unencumbered')

    # Check 5: Grantor contact info recently changed
    if deed_record.get('grantor_contact_updated'):
        days_since_update = (datetime.now() - deed_record['grantor_contact_updated']).days
        if days_since_update < 90:
            risk_score += 20
            risk_indicators.append('recent_contact_change')

    return {
        'property_id': deed_record.get('property_id'),
        'risk_score': risk_score,
        'risk_level': 'critical' if risk_score >= 60 else 'high' if risk_score >= 40 else 'medium',
        'risk_indicators': risk_indicators,
        'recommendation': 'HOLD_RECORDING' if risk_score >= 60 else 'MANUAL_REVIEW'
    }
```

### Behavioral Analytics

- Property sale initiated by non-resident owner of vacant, unencumbered property with below-market listing price
- Contact information (email, phone, mailing address) for property owner changed within 90 days of sale initiation
- Deed recording with document metadata indicating AI-generated content or recently created documents
- Remote online notarization session with video quality anomalies or biometric verification flags
- Wire instructions directing property sale proceeds to recently opened accounts in different jurisdictions

### Cross-Team Correlation

- **Title Company + County Recorder**: Deed recording anomalies correlated with title search patterns indicating seller impersonation research
- **Financial Institutions + Title Insurance**: Wire transfer monitoring correlated with property transactions flagged for seller impersonation (TP-0006)
- **Law Enforcement + Real Estate Regulators**: Serial property targeting patterns shared across jurisdictions for coordinated investigation

---

## Operational Evidence

### EV-TP0073-2026-001: FBI Real Estate Fraud Scale

- **Source**: FBI Internet Crime Complaint Center (IC3); First American Title Fraud Report
- **Key Findings**: FBI reported $16.6 billion in total real estate fraud losses in 2024. Seller impersonation of vacant property owners is the fastest-growing subcategory, with losses doubling year-over-year. Vacant lots and unencumbered properties are the primary targets because they lack mortgage servicers who might otherwise notice unauthorized activity. The average per-incident loss for seller impersonation cases is $150K-$350K.
- **CFPF Phase Coverage**: P1-P5
- **Confidence**: High

### EV-TP0073-2026-002: AI-Forged Documents and Deepfake Notarization

- **Source**: Entrust Identity Fraud Report (2026); CertifID Wire Fraud Report; HousingWire (2025)
- **Key Findings**: Entrust reports a 40% year-over-year increase in deepfake-related fraud attempts across all sectors, with real estate title fraud as a primary growth area. Deepfake video technology enables fraudsters to pass remote online notarization (RON) identity verification by appearing as the property owner during video sessions. AI tools generate convincing forged deeds, government IDs, and notary stamps that pass visual inspection. Document forensics tools can detect AI artifacts in 85% of cases, but many county recording offices and notaries lack access to such tools.
- **CFPF Phase Coverage**: P2-P4
- **Confidence**: High

### EV-TP0073-2026-003: Virginia Legislative Response

- **Source**: Virginia Deed Fraud Study (2025); ALTA Best Practices
- **Key Findings**: Virginia enacted the first major state-level deed fraud legislation in 2025, mandating enhanced identity verification for property transfers including: (1) independent verification of owner identity through non-document means, (2) mandatory waiting period for deed recordings on recently listed vacant properties, and (3) property owner notification requirements for any document filings. ALTA updated its best practices to recommend similar measures nationwide. The legislation was prompted by a documented surge in deed theft targeting vacant lots in Northern Virginia.
- **CFPF Phase Coverage**: P2-P4
- **Confidence**: High

---

## References

- FBI, "Internet Crime Complaint Center (IC3) Annual Report" (2024) -- $16.6B real estate fraud losses
- First American, "Title Fraud: Emerging Threats and Prevention Strategies" -- seller impersonation patterns and vacant property targeting
- HousingWire, "Deed Fraud on the Rise: AI-Powered Property Theft" (2025) -- AI-forged documents and deepfake notarization
- ALTA, "Best Practices for Title Insurance and Settlement Services" -- identity verification standards for property transfers
- Virginia Deed Fraud Study (2025) -- legislative response, enhanced verification mandates
- NAR (National Association of Realtors), "Wire Fraud and Title Theft Advisory" -- realtor awareness and prevention guidance
- CertifID, "Wire Fraud Report: Real Estate Transaction Security" -- wire fraud intersection with title fraud
- Entrust, "Identity Fraud Report" (2026) -- 40% YoY deepfake increase, document forgery trends

---

## Analyst Notes

Real estate title fraud exploits a fundamental weakness in the property recording system: county recorder offices are ministerial in nature, meaning they are required to record documents presented to them without independently verifying the identity of the parties or the authenticity of the documents. This creates a systemic vulnerability where a single forged deed, once recorded, becomes the official record of title.

The shift to remote online notarization (RON) during and after the COVID-19 pandemic expanded the attack surface significantly. While RON provides convenience and access benefits, it also eliminates the in-person identity verification that previously served as a friction point for deed fraud. Deepfake video technology capable of passing RON identity checks means that the video component of RON is no longer a reliable authentication factor.

Vacant property targeting is the dominant pattern because these properties lack the natural surveillance mechanisms of occupied properties -- no resident to notice unfamiliar activity, no mortgage servicer monitoring the title, and owners who may only check on the property periodically. Detection systems (DL-0186) should prioritize monitoring transactions involving vacant, unencumbered properties with non-resident owners.

The intersection with wire fraud (TP-0006) is critical. Even when title fraud is detected before recording, if the sale proceeds have already been wired, the financial loss may be unrecoverable. Wire verification callbacks to independently verified owner contact information (not the contact info provided by the person initiating the sale) are the most effective control at the monetization phase.

Virginia's 2025 legislation is a model for other jurisdictions, but adoption is slow. Title companies and county recorders should implement enhanced verification proactively rather than waiting for legislative mandates.

AI document forensics (DL-0187) should be deployed at both the notarization stage and the county recording stage. The 85% detection rate for AI-generated documents is encouraging but means 15% of forged documents will pass automated screening -- manual review for high-risk transactions (vacant property, non-resident owner, recent contact changes) remains necessary.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-29 | FLAME Project | Initial submission -- sourced from FBI IC3, First American, ALTA, Virginia Deed Fraud Study, CertifID, and Entrust intelligence |
