# TP-0072: Telecom Subscription & Billing Fraud

```yaml
---
id: TP-0072
title: "Telecom Subscription & Billing Fraud"
category: ThreatPath
date: 2026-03-29
last_reviewed: 2026-03-29
author: "FLAME Project"
source: "Subex Telecom Fraud Intelligence (2025, 2026); TransUnion Consumer Pulse (2025); SEON Telecom Fraud Guide; Vonage Communications Fraud Report"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - subscription-fraud
  - telecom-billing-fraud
  - premium-sms-fraud
sector:
  - telecommunications
cfpf_phases:
  - P2
  - P3
  - P4
  - P5
fraud_family: "telecom-specialized"
primary_phase: "P3"
short_name: "Telecom Sub Fraud"
confidence_score: 75
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1078      # Valid Accounts
  - T1656      # Impersonation
  - T1136      # Create Account
  - T1098      # Account Manipulation
  - T1565      # Data Manipulation
ft3_tactics: ["FTA001", "FT007.003", "FT011.001"]
mitre_f3: ["F1003", "F1005", "F1015", "F1040", "T1451", "T1585"]
groupib_stages:
  - "Resource Development"
  - "Initial Access"
  - "Account Access"
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
  - id: TP-0003
    relationship: enables
  - id: TP-0008
    relationship: related-to
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-WCI-2024
tags:
  - subscription-fraud
  - telecom-billing-fraud
  - premium-sms-fraud
  - synthetic-identity-telecom
  - device-fraud
  - genai-kyc-bypass
  - cramming
  - wci-geographic-attribution
---
```

## Summary

Telecom subscription and billing fraud encompasses the use of stolen, synthetic, or manipulated identities to fraudulently obtain telecom services, devices, and credit -- combined with unauthorized billing manipulation that charges victims for premium services they never requested. TransUnion reports that 53% of telecom executives identify subscription fraud as their top concern, driven by the increasing sophistication of synthetic identity creation (TP-0003) and GenAI-powered KYC bypass techniques. The total telecom fraud ecosystem reaches $41.82B annually (CFCA/TNS 2026), with subscription fraud as a primary entry point that enables downstream fraud including device resale, SIM swap attacks (TP-0008), and premium SMS billing schemes (cramming). GenAI tools now generate convincing synthetic identity documents that pass automated KYC checks, enabling fraudsters to open multiple telecom accounts for device acquisition at industrial scale.

## Threat Path Hypothesis

> **Hypothesis**: Fraudsters exploit telecom onboarding processes by combining synthetic identities (TP-0003) with GenAI-generated KYC documents to fraudulently activate service subscriptions and acquire subsidized devices. The synthetic identity creation pipeline produces identities with legitimate-appearing credit histories sufficient to pass automated credit checks. Once accounts are established, fraudsters acquire high-value devices (smartphones, tablets) on installment plans with no intention of payment, reselling devices on secondary markets. In parallel, billing fraud operators manipulate account settings to add unauthorized premium SMS subscriptions (cramming), generating per-message revenue shared with premium content providers. The combination of subscription fraud for device acquisition and billing fraud for ongoing revenue extraction creates a dual-monetization model that maximizes per-identity returns.

**Confidence**: Medium-High -- TransUnion, Subex, and SEON document subscription fraud patterns and executive concern levels. GenAI KYC bypass is an emerging escalation documented across multiple sources.

**Estimated Impact**: $41.82B total telecom fraud annually. Subscription fraud contributes an estimated $3-5B in device acquisition losses alone. Premium SMS cramming generates additional billions in unauthorized charges to consumer accounts.

## CFPF Phase Mapping

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Synthetic identity onboarding | Fraudsters use synthetic identities with manufactured credit histories to pass telecom KYC and credit checks during account activation | New account applications with synthetic identity markers (valid SSN + mismatched name/DOB); credit files with limited or thin history; identity documents with GenAI artifacts |
| GenAI KYC document generation | AI tools generate realistic government IDs, utility bills, and proof-of-address documents that pass automated document verification | Documents with metadata indicating AI generation; pixel-level inconsistencies in security features; document serial numbers that fail validation |
| Stolen identity account opening | Fraudsters use compromised PII from data breaches to open accounts in victims' names | Multiple new account applications using the same identity within 30 days across carriers; account activation from device/location inconsistent with identity's established pattern |

**Target**: Telecom carriers, MVNOs (Mobile Virtual Network Operators), device retailers

**Data Sources**: KYC/CDD verification logs, credit bureau inquiry records, identity verification platform telemetry, account application databases

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Multi-account establishment | Fraudsters activate multiple accounts across different carriers using variations of synthetic or stolen identities | Same device IMEI used across multiple carrier activations (DL-0184); identity variations (name spelling, address) linked by common attributes; rapid sequential account activations |
| Device acquisition on installment | High-value devices obtained on 24-36 month installment plans with no intention of payment | New accounts immediately selecting highest-value device options; preference for flagship devices with highest resale value; multiple device upgrades within first billing cycle |
| Premium SMS subscription injection | Unauthorized premium SMS services added to accounts through compromised billing APIs, social engineering of carrier support, or malware-initiated WAP billing | Premium SMS shortcode subscriptions appearing without customer opt-in; billing API calls from unauthorized sources; WAP billing triggers from suspicious URLs |

**Data Sources**: Account activation logs, device inventory systems, billing system audit trails, premium SMS subscription records

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Device resale and liquidation | Acquired devices immediately unlocked and resold on secondary markets (eBay, Swappa, local marketplaces, overseas export) | Devices reported as active on carrier network for < 30 days then going inactive; device unlock requests within days of activation; IMEI appearing on secondary market listings |
| Subscription service exploitation | Fraudulently opened accounts used to consume services (data, international calling) at maximum capacity with no payment intent | Maximum plan utilization from day one; no payment on first bill; account churning pattern across carriers |
| Premium SMS billing accumulation (DL-0185) | Unauthorized premium SMS subscriptions generate ongoing per-message charges on victim accounts | Sudden appearance of premium SMS charges on established accounts; multiple premium shortcode subscriptions added within short timeframe; charges from premium content providers with no corresponding customer opt-in |

**Data Sources**: Device management platforms, billing systems, secondary market monitoring, premium SMS aggregator logs

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Device resale proceeds | Stolen devices sold at 60-80% of retail value on secondary markets | Cash or cryptocurrency transactions correlated with device serial numbers; bulk device listings from same seller profiles |
| Premium SMS revenue sharing | Per-message charges from cramming shared between premium content providers and fraud operators | Revenue share payments to entities associated with known cramming operations; disproportionate premium SMS revenue from specific shortcodes |
| Account default and write-off | Fraudulent subscription accounts default after 60-90 days, with carriers writing off device installment balances and service charges | Accounts following consistent pattern: activation -> device acquisition -> maximum utilization -> non-payment -> write-off; correlation of write-off accounts with synthetic identity markers |

**Data Sources**: Carrier bad debt and write-off databases, secondary market transaction monitoring, premium SMS revenue sharing records, collections data

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering (impersonation during account activation)
- FT007.003: Synthetic identity creation for account opening
- FT011.001: Credential and identity theft for subscription fraud

**MITRE ATT&CK:**
- T1078: Valid Accounts -- use of stolen/synthetic identities to create valid accounts
- T1656: Impersonation -- impersonation of legitimate customers during onboarding
- T1136: Create Account -- fraudulent account creation at scale
- T1098: Account Manipulation -- unauthorized premium service additions
- T1565: Data Manipulation -- billing record manipulation for cramming

**Group-IB Fraud Matrix:**
- Resource Development -> Initial Access -> Account Access -> Perform Fraud -> Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4-5 (Execution/Monetization) when accounts default on payments or customers report unauthorized premium SMS charges.

**Look Left**:
- P2: Enhanced identity verification with liveness detection and document forensics would catch GenAI-generated KYC documents
- P2: Cross-carrier identity sharing would identify synthetic identities applying across multiple carriers
- P3: Device acquisition velocity monitoring would flag multi-account device accumulation patterns (DL-0184)

**Look Right**:
- P4: Devices acquired through subscription fraud fund secondary market operations and potentially burner phone supply chains
- P5: Subscription fraud accounts repurposed for SIM swap attacks (TP-0008) and money mule operations
- P5: Premium SMS revenue used to fund other fraud operations

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Synthetic identity provider | Complete identity packages with credit file for telecom onboarding | High | $50-$500 per identity |
| GenAI document forge | AI-generated government IDs, utility bills, proof of address | Medium | $20-$200 per document set |
| Device reseller | Secondary market liquidation of fraudulently acquired devices | High | 60-80% of device retail value |
| Premium SMS aggregator | Complicit or compromised premium SMS content providers enabling cramming | Medium | Revenue share (30-60% of charges) |
| Account activation mule | Individuals who visit stores to activate accounts using provided identities | High | $50-$200 per account activation |

### Intelligence Sources
- Subex, "Telecom Fraud Intelligence Report" (2025, 2026) -- subscription fraud patterns and detection
- TransUnion, "Consumer Pulse Report" (2025) -- 53% executive concern metric and synthetic identity trends
- SEON, "Telecom Fraud Prevention Guide" -- KYC bypass techniques and device fraud
- Vonage, "Communications Fraud Report" -- premium SMS and billing fraud analysis

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P2 | AI-powered document verification with deepfake/GenAI detection | Preventive | Identity Verification |
| P2 | Liveness detection during remote onboarding to prevent synthetic identity bypass | Preventive | KYC Operations |
| P2 | Cross-carrier identity verification consortium to detect multi-carrier synthetic identity applications | Detective | Industry Collaboration |
| P3 | Device acquisition velocity monitoring per identity and per device (DL-0184) | Detective | Fraud Operations |
| P3 | IMEI cross-referencing across carrier activations | Detective | Network Security |
| P4 | Premium SMS opt-in verification and consumer consent management (DL-0185) | Preventive | Billing Operations |
| P4 | Real-time billing anomaly detection for unauthorized premium service additions | Detective | Fraud Management |
| P5 | Early payment default prediction models for new accounts | Detective | Credit Risk |
| P5 | Device blacklisting for accounts in fraud-confirmed default | Preventive | Device Management |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Recognition of subscription fraud and billing manipulation as priority fraud vectors |
| ASSESS | Level 3 (Established) | Risk assessment quantifying exposure to synthetic identity onboarding and premium SMS cramming |
| PLAN | Level 3 (Established) | KYC enhancement roadmap; premium SMS consent framework; cross-carrier collaboration plan |
| ACT | Level 3 (Established) | Real-time identity verification with GenAI detection; billing anomaly monitoring; device velocity tracking |
| MONITOR | Level 3 (Established) | Continuous monitoring of account activation patterns, device acquisition velocity, and premium SMS subscriptions |
| REPORT | Level 2 (Developing) | Incident reporting capturing synthetic identity indicators and billing fraud patterns for industry sharing |
| IMPROVE | Level 2 (Developing) | Post-incident analysis feeding back into KYC models and billing fraud detection thresholds |

---

## Detection Approaches

### Queries / Rules

```splunk
`comment("Splunk SPL for Telecom Subscription Velocity — DL-0184")`
`comment("Detects multiple new service activations from same identity/device within 30 days")`
index=flame_telecom sourcetype=flame:account_activations
  activation_type="new_account"
| bin _time span=30d
| stats count as activation_count,
        dc(carrier_id) as unique_carriers,
        dc(device_imei) as unique_devices,
        values(carrier_id) as carriers,
        values(device_imei) as devices,
        values(plan_type) as plan_types,
        sum(device_value) as total_device_value,
        earliest(_time) as first_activation,
        latest(_time) as last_activation
  by identity_hash, _time
| where activation_count >= 3 OR unique_carriers >= 2
| eval risk_score = case(
    activation_count >= 5 AND unique_carriers >= 3, "critical",
    activation_count >= 4 AND total_device_value > 5000, "high",
    activation_count >= 3 OR unique_carriers >= 2, "medium")
| table identity_hash, activation_count, unique_carriers, unique_devices,
        carriers, devices, plan_types, total_device_value,
        first_activation, last_activation, risk_score
| sort - activation_count
```

```sql
-- SQL for Premium SMS Billing Anomaly Detection — DL-0185
-- Detects unauthorized premium SMS subscriptions appearing on accounts
SELECT
  a.account_id,
  a.customer_name,
  a.account_open_date,
  COUNT(DISTINCT s.shortcode) AS premium_sms_subscriptions,
  SUM(s.charge_amount) AS total_premium_charges,
  MIN(s.subscription_start_date) AS first_subscription,
  MAX(s.subscription_start_date) AS last_subscription,
  DATEDIFF(DAY, MIN(s.subscription_start_date), MAX(s.subscription_start_date)) AS subscription_window_days,
  STRING_AGG(s.shortcode, ', ') AS shortcodes
FROM customer_accounts a
JOIN premium_sms_subscriptions s ON a.account_id = s.account_id
LEFT JOIN premium_sms_opt_in o ON a.account_id = o.account_id AND s.shortcode = o.shortcode
WHERE s.subscription_start_date >= DATEADD(DAY, -30, CURRENT_DATE)
  AND o.opt_in_id IS NULL  -- No corresponding opt-in record
GROUP BY a.account_id, a.customer_name, a.account_open_date
HAVING COUNT(DISTINCT s.shortcode) >= 2
ORDER BY total_premium_charges DESC
```

### Behavioral Analytics

- Multiple new account activations from the same identity or device IMEI across carriers within 30 days
- New accounts immediately selecting highest-value device options on installment plans
- Premium SMS subscriptions appearing on accounts with no corresponding opt-in or consent record
- Account activation followed by no usage within 48 hours (device removed for resale)
- Identity documents with metadata anomalies indicating AI generation during onboarding KYC

### Cross-Team Correlation

- **Fraud Operations + Identity Verification**: Synthetic identity markers from KYC correlated with account default patterns
- **Billing Operations + Fraud Analytics**: Premium SMS subscription anomalies correlated with account compromise indicators
- **Credit Risk + Fraud Management**: Early payment default models enriched with fraud-specific features (activation velocity, device selection patterns)

---

## Operational Evidence

### EV-TP0072-2026-001: Executive Concern and Synthetic Identity Scale

- **Source**: TransUnion Consumer Pulse Report (2025)
- **Key Findings**: 53% of telecom executives identify subscription fraud as their top fraud concern. Synthetic identity fraud in telecom has grown 40% year-over-year, driven by GenAI tools that generate convincing identity documents at scale. The average synthetic identity telecom fraud loss is $3,500 per account (device value + unpaid service charges).
- **CFPF Phase Coverage**: P2-P5
- **Confidence**: High

### EV-TP0072-2026-002: GenAI KYC Bypass Capabilities

- **Source**: Subex (2026); SEON Telecom Fraud Guide
- **Key Findings**: GenAI tools can generate government-issued ID replicas that pass automated document verification systems in 72% of tested scenarios. Liveness detection bypass using pre-recorded deepfake videos succeeds against 31% of remote onboarding systems. Combined synthetic identity + GenAI document packages cost $50-$200 on underground markets and enable fraudulent account activation at carriers with purely digital onboarding.
- **CFPF Phase Coverage**: P2
- **Confidence**: Medium-High

### EV-TP0072-2026-003: Total Telecom Fraud Scale

- **Source**: Subex (2025, 2026); TNS/CFCA (2026)
- **Key Findings**: Total global telecom fraud reaches $41.82B annually, with subscription fraud, IRSF (TP-0071), and billing fraud as the three largest categories. Premium SMS cramming alone generates an estimated $1.5B in unauthorized consumer charges annually. Carrier-side losses from subscription fraud device defaults contribute an additional $3-5B.
- **CFPF Phase Coverage**: P2-P5
- **Confidence**: High

---

## References

- Subex, "Global Telecom Fraud Intelligence Report" (2025, 2026) -- subscription fraud patterns, GenAI impact
- TransUnion, "Consumer Pulse Report" (2025) -- 53% executive concern, synthetic identity trends
- SEON, "Telecom Fraud Prevention Guide" -- KYC bypass techniques, device fraud patterns
- Vonage, "Communications Fraud Report" -- premium SMS billing fraud and cramming analysis
- TNS/CFCA, "Global Fraud Loss Survey" (2026) -- $41.82B total telecom fraud quantification
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) -- telecom fraud cross-border trends

---

## Analyst Notes

Telecom subscription fraud is a gateway crime -- the accounts and devices obtained through fraudulent onboarding fuel downstream fraud operations including SIM swap attacks (TP-0008), money mule communications, and burner phone supply chains for organized crime. Disrupting subscription fraud at the onboarding stage has outsized impact on multiple downstream threat paths.

The 53% executive concern rate (TransUnion) reflects a market awareness that is not yet matched by deployed controls. Many carriers still rely on credit bureau checks as the primary onboarding gate, which synthetic identities are specifically designed to pass. The shift to GenAI document generation means that document verification alone is no longer sufficient -- multi-modal verification combining document analysis, liveness detection, behavioral biometrics, and cross-carrier intelligence sharing is required.

Premium SMS cramming (DL-0185) remains profitable because detection typically occurs only when customers manually review their bills and dispute charges. Many consumers never notice small recurring charges ($9.99/month). Carrier-side detection must proactively identify premium SMS subscriptions without corresponding opt-in records rather than relying on customer complaints.

Cross-carrier collaboration is the most impactful structural improvement. Fraudsters exploit the siloed nature of carrier identity verification by applying across multiple carriers with variations of the same synthetic identity. A shared identity verification consortium would dramatically increase detection rates for multi-carrier subscription fraud (DL-0184).

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-29 | FLAME Project | Initial submission -- sourced from Subex, TransUnion, SEON, Vonage, and TNS/CFCA intelligence |
