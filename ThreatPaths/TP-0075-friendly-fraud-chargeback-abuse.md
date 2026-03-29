# TP-0075: Friendly Fraud & Chargeback Abuse

```yaml
---
id: TP-0075
title: "Friendly Fraud & Chargeback Abuse"
category: ThreatPath
date: 2026-03-27
author: "FLAME Project"
source: "Chargebacks911 (2026); Chargeflow (2025); Payscout (2025); Chargeback.io (2026); Alloy; Offenso Academy (2026)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - friendly-fraud
  - chargeback-abuse
  - first-party-misuse
  - dispute-fraud
sector:
  - payments
  - ecommerce
  - retail
cfpf_phases:
  - P4
  - P5
confidence_score: 85
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1657      # Financial Theft
ft3_tactics: []
mitre_f3: []
groupib_stages:
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 4"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0031
    relationship: related-to
  - id: TP-0016
    relationship: related-to
regulatory_refs: []
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - friendly-fraud
  - chargeback-abuse
  - first-party-fraud
  - dispute-fraud
  - visa-vamp
  - refund-hack
  - chargeback-velocity
  - delivery-confirmation
  - merchant-fraud
---
```

## Summary

Friendly fraud — where legitimate cardholders dispute genuine transactions to obtain refunds while retaining goods or services — has become the single largest fraud category in payment networks, representing 36% of all fraud and projected to reach 337 million chargebacks costing USD 15.3 billion in the US by 2026. Unlike third-party fraud, the identity is real and the transaction is legitimate, making detection fundamentally different. Chargeback abuse surged 233% between Q1 and Q3 2025, with 84% of consumers finding chargebacks simpler than contacting the merchant. The economic multiplier is severe: merchants lose USD 4.61 for every USD 1.00 of friendly fraud. Visa's VAMP (Visa Acquirer Monitoring Program) launched April 2025 to impose stricter thresholds on merchants and acquirers. Underground "refund hack" tutorials proliferate on forums and social platforms, teaching consumers systematic chargeback abuse techniques.

**Distinction from TP-0031**: TP-0031 covers Refund-as-a-Service (RaaS) — organized refund fraud where third-party services file refunds on behalf of consumers against merchants. TP-0075 covers first-party chargeback abuse where the cardholder directly files disputes through the payment network, bypassing the merchant entirely.

**Distinction from TP-0016**: TP-0016 covers first-party bust-out fraud (synthetic or real identity credit abuse). TP-0075 covers dispute-level abuse of the chargeback mechanism against individual transactions, not credit line bust-outs.

## Threat Path Hypothesis

> **Hypothesis**: Friendly fraud exploits the consumer-protective chargeback mechanism built into payment networks, weaponizing it as a cost-free return channel. The asymmetry is structural: payment networks default to consumer protection, merchants bear the burden of proof, and the dispute process is deliberately frictionless for cardholders. This creates a moral hazard where consumers learn that filing a chargeback is simpler than a legitimate return, and that false claims of non-delivery or unauthorized use are rarely challenged effectively. The 233% surge in 2025 reflects both economic pressure on consumers and the proliferation of "refund hack" tutorials that systematize abuse techniques. Detection must focus on behavioral patterns (chargeback velocity, delivery confirmation correlation, device fingerprint matching) rather than identity verification, since the identity is genuine.

**Confidence**: High — Chargebacks911, Chargeflow, and payment network data quantify the scale. Visa VAMP program confirms network-level recognition of the problem.

**Estimated Impact**: 337 million chargebacks projected for 2026 in US alone. USD 15.3 billion in direct losses. Merchants lose USD 4.61 per USD 1.00 of friendly fraud (including chargeback fees, operational costs, lost merchandise, and shipping).

## CFPF Phase Mapping

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Legitimate transaction completion | Cardholder makes a genuine purchase, receives goods/services, and then initiates a dispute through their card issuer | Transaction with successful delivery confirmation followed by chargeback filing; device fingerprint on dispute matches original purchase device |
| False claim filing | Cardholder files a chargeback claiming non-delivery, unauthorized use, or item-not-as-described despite having received the product | Chargeback reason codes inconsistent with delivery tracking data; repeated use of same reason codes by same cardholder across merchants |
| Merchant bypass | Cardholder files directly with card issuer without first contacting the merchant for resolution, exploiting the zero-liability consumer protection | Chargeback filed with no prior merchant contact; no return merchandise authorization (RMA) request preceding dispute |
| Tutorial-guided abuse | Consumers follow "refund hack" guides from underground forums that specify optimal timing, reason codes, and claim language for successful chargebacks | Chargeback language patterns matching known tutorial scripts; timing patterns consistent with published guides (e.g., waiting exactly 14-30 days post-delivery) |

**Data Sources**: Payment network dispute data, delivery tracking systems, customer contact logs, device fingerprint databases

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Refund retention | Cardholder retains both the refunded amount and the original goods/services | Chargeback approved with no return of merchandise; customer continues using digital services post-chargeback |
| Serial abuse across merchants | Cardholder repeats the pattern across multiple merchants and card issuers to avoid detection thresholds | Same cardholder identity appearing in chargeback filings across multiple merchants within 90 days; cross-merchant velocity exceeding normal consumer dispute rates |
| Resale of retained goods | Physical goods obtained via chargeback abuse are resold through secondary marketplaces | Goods from chargebacked orders appearing on resale platforms linked to the same cardholder address |

**Data Sources**: Cross-merchant chargeback databases, payment network consortium data, marketplace monitoring

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- Not directly mapped (first-party misuse of legitimate dispute mechanisms)

**MITRE ATT&CK:**
- T1657: Financial Theft — abuse of chargeback mechanism for financial gain

**Group-IB Fraud Matrix:**
- Perform Fraud → Monetization (no recon/initial access phases — the cardholder is the fraudster using their own identity and credentials)

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 5 (Monetization) when chargeback data is analyzed retrospectively, or at Phase 4 when real-time dispute monitoring flags velocity anomalies.

**Look Left**:
- Pre-P4: Limited look-left opportunity because the transaction itself is legitimate. Behavioral indicators at purchase time (e.g., customer with prior chargeback history) provide the only pre-dispute signal
- P4: Merchant contact absence — chargebacks filed without prior merchant communication are a strong indicator

**Look Right**:
- P5: Serial chargeback abuse across multiple merchants funds ongoing consumer enrichment
- P5: "Refund hack" tutorial communities create multiplier effect as techniques spread
- P5: Merchants exceeding Visa VAMP thresholds face program penalties, increased monitoring fees, and potential card acceptance revocation

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Refund hack tutorial creator | Publishing step-by-step chargeback abuse guides on forums and social media | High | Free to USD 50 per guide |
| Chargeback coaching service | One-on-one guidance for filing successful chargebacks | Medium | USD 20–100 per consultation |
| Dispute letter template seller | Pre-written dispute letters optimized for specific reason codes | Medium | USD 10–50 per template set |
| Cross-merchant abuse coordinator | Organizing sequential chargeback abuse across multiple merchants | Low | Commission-based (10–30% of refund value) |

### Intelligence Sources
- Chargebacks911, "State of Chargebacks 2026" — 337M chargeback projection, USD 15.3B impact
- Chargeflow, "Friendly Fraud Statistics 2025" — 233% surge Q1-Q3 2025, 84% simplicity preference
- Payscout, "Chargeback Economics" (2025) — USD 4.61 loss per USD 1.00 fraud
- Chargeback.io, "Chargeback Trends 2026" — 36% of all fraud attribution
- Alloy, "First-party fraud detection" — behavioral analytics approaches
- Offenso Academy, "Refund hack tutorial analysis" (2026) — underground tutorial ecosystem

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| Pre-P4 | Customer chargeback history scoring at purchase time | Detective | Fraud/Risk |
| P4 | Delivery confirmation integration with dispute response — automated compelling evidence submission | Preventive | Operations/Fraud |
| P4 | Device fingerprint matching between original purchase and dispute filing | Detective | Fraud Engineering |
| P4 | Mandatory merchant contact verification before chargeback acceptance | Preventive | Issuer/Network |
| P4 | Real-time chargeback velocity monitoring per cardholder across merchants | Detective | Payment Network/Fraud |
| P5 | Visa VAMP compliance monitoring — track merchant dispute ratios against thresholds | Preventive | Acquiring/Compliance |
| P5 | Cross-merchant chargeback consortium data sharing (e.g., Ethoca, Verifi) | Detective | Fraud Operations |
| P5 | Blacklisting of serial chargeback abusers at network level | Corrective | Payment Network |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive recognition of friendly fraud as a distinct fraud category requiring dedicated countermeasures |
| ASSESS | Level 3 (Established) | Risk assessment quantifying friendly fraud exposure separate from third-party fraud |
| PLAN | Level 3 (Established) | Chargeback management strategy; Visa VAMP compliance roadmap; compelling evidence automation plan |
| ACT | Level 4 (Advanced) | Real-time chargeback velocity monitoring; device fingerprint correlation; delivery confirmation integration |
| MONITOR | Level 4 (Advanced) | Continuous cross-merchant chargeback pattern analysis; VAMP threshold monitoring |
| REPORT | Level 3 (Established) | Chargeback analytics reporting; serial abuser identification; network-level reporting |
| IMPROVE | Level 3 (Established) | Post-dispute analysis feeding back into purchase-time risk scoring and dispute response optimization |

---

## Detection Approaches

### Queries / Rules

```sql
-- SQL: Chargeback Velocity Pattern Detection (DL-0190)
-- Customer with 3+ chargebacks in 90 days across different merchants with delivery confirmed
SELECT
  c.cardholder_id,
  c.cardholder_name,
  COUNT(DISTINCT d.dispute_id) AS dispute_count,
  COUNT(DISTINCT d.merchant_id) AS merchant_count,
  SUM(d.dispute_amount) AS total_disputed,
  COUNT(DISTINCT CASE WHEN t.delivery_confirmed = 1 THEN d.dispute_id END) AS confirmed_delivery_disputes,
  MIN(d.dispute_date) AS first_dispute,
  MAX(d.dispute_date) AS last_dispute
FROM chargebacks d
JOIN cardholders c ON d.cardholder_id = c.cardholder_id
JOIN transactions t ON d.original_transaction_id = t.transaction_id
WHERE d.dispute_date >= DATEADD(DAY, -90, CURRENT_DATE)
  AND t.delivery_confirmed = 1
GROUP BY c.cardholder_id, c.cardholder_name
HAVING COUNT(DISTINCT d.dispute_id) >= 3
  AND COUNT(DISTINCT d.merchant_id) >= 2
ORDER BY dispute_count DESC
```

```sql
-- SQL: First-Party Dispute Anomaly Detection (DL-0191)
-- Chargeback with delivery confirmation, matching device fingerprint, and no merchant contact
SELECT
  d.dispute_id,
  d.cardholder_id,
  d.merchant_id,
  d.dispute_amount,
  d.dispute_reason_code,
  d.dispute_date,
  t.transaction_date,
  t.delivery_confirmed,
  t.delivery_date,
  t.device_fingerprint AS purchase_device,
  d.device_fingerprint AS dispute_device,
  CASE WHEN t.device_fingerprint = d.device_fingerprint THEN 1 ELSE 0 END AS device_match,
  mc.last_contact_date AS merchant_contact_date
FROM chargebacks d
JOIN transactions t ON d.original_transaction_id = t.transaction_id
LEFT JOIN merchant_contacts mc ON d.cardholder_id = mc.customer_id
  AND d.merchant_id = mc.merchant_id
  AND mc.contact_date BETWEEN t.transaction_date AND d.dispute_date
WHERE t.delivery_confirmed = 1
  AND t.device_fingerprint = d.device_fingerprint
  AND mc.contact_id IS NULL
  AND d.dispute_date >= DATEADD(DAY, -30, CURRENT_DATE)
ORDER BY d.dispute_amount DESC
```

### Behavioral Analytics

- Chargeback velocity: 3+ disputes in 90 days across different merchants
- Delivery confirmation contradiction: chargeback filed on orders with confirmed delivery (signed, photographed, GPS-verified)
- Device fingerprint match: dispute filed from same device used for original purchase (strong indicator of first-party abuse vs. true unauthorized use)
- No merchant contact: chargeback filed without any prior attempt to contact merchant for resolution
- Reason code patterns: repeated use of "item not received" or "unauthorized" codes by same cardholder despite delivery/device evidence
- Timing patterns: disputes filed at consistent intervals post-delivery matching known tutorial recommendations

### Cross-Team Correlation

- **Fraud + Customer Service**: Absence of merchant contact pre-dispute is a strong friendly fraud signal
- **Fraud + Logistics**: Delivery confirmation data (GPS, signature, photo) correlated with dispute claims
- **Fraud + Payment Network**: Cross-merchant chargeback velocity shared through network consortiums (Ethoca, Verifi)

---

## Operational Evidence

### EV-TP0075-2026-001: Chargeback Volume and Cost Projections

- **Source**: Chargebacks911 (2026); Chargeback.io (2026)
- **Key Findings**: 337 million chargebacks projected for 2026 in the US, representing USD 15.3 billion in losses. Friendly fraud accounts for 36% of all fraud. Merchants lose USD 4.61 for every USD 1.00 of friendly fraud when factoring chargeback fees, operational costs, lost merchandise, and shipping.
- **CFPF Phase Coverage**: P4–P5
- **Confidence**: High

### EV-TP0075-2026-002: Chargeback Abuse Surge 2025

- **Source**: Chargeflow (2025); Payscout (2025)
- **Key Findings**: Chargeback abuse surged 233% between Q1 and Q3 2025. 84% of consumers surveyed found filing a chargeback simpler than contacting the merchant directly. Cost-of-living pressures and awareness of chargeback processes through social media contributed to the acceleration.
- **CFPF Phase Coverage**: P4
- **Confidence**: High

### EV-TP0075-2026-003: Visa VAMP Program Launch

- **Source**: Visa (April 2025); Alloy
- **Key Findings**: Visa launched the VAMP (Visa Acquirer Monitoring Program) in April 2025, replacing previous monitoring programs with stricter dispute ratio thresholds for merchants and acquirers. Merchants exceeding thresholds face escalating fees (USD 50–200 per excess dispute), enhanced monitoring requirements, and potential card acceptance revocation. The program reflects network-level recognition that chargeback abuse has become systemic.
- **CFPF Phase Coverage**: P5
- **Confidence**: High

### EV-TP0075-2026-004: Refund Hack Tutorial Ecosystem

- **Source**: Offenso Academy (2026); underground forum analysis
- **Key Findings**: "Refund hack" tutorials have proliferated across underground forums, Reddit communities, TikTok, and Telegram channels. Guides provide step-by-step instructions for filing successful chargebacks, including recommended timing (14-30 days post-delivery), optimal reason codes, and scripted dispute language. Some guides are specific to individual merchants (e.g., Amazon, eBay) and payment processors.
- **CFPF Phase Coverage**: P4
- **Confidence**: Medium-High

---

## References

- Chargebacks911, "State of Chargebacks 2026" — 337M projection, USD 15.3B US impact
- Chargeflow, "Friendly Fraud Statistics and Trends 2025" — 233% surge, 84% simplicity preference
- Payscout, "The True Cost of Chargebacks" (2025) — USD 4.61 multiplier per USD 1.00 fraud
- Chargeback.io, "Chargeback Industry Trends 2026" — 36% of all fraud attribution
- Alloy, "First-party fraud: detection and prevention strategies" — behavioral analytics approaches
- Offenso Academy, "The refund hack economy" (2026) — underground tutorial ecosystem analysis
- Visa, "Visa Acquirer Monitoring Program (VAMP)" (April 2025) — program thresholds and enforcement

---

## Analyst Notes

Friendly fraud is structurally different from every other fraud typology in the FLAME taxonomy because the identity is real, the transaction is legitimate, and the payment method belongs to the person filing the dispute. Traditional fraud detection — identity verification, device anomaly detection, behavioral biometrics — is largely irrelevant because there is nothing anomalous about the transaction itself.

Detection must instead focus on post-transaction behavioral patterns: chargeback velocity across merchants, contradiction between delivery evidence and dispute claims, device fingerprint matching between purchase and dispute sessions, and absence of merchant contact. These signals require data sources and correlation logic that most fraud teams are not accustomed to building.

The USD 4.61 multiplier is the critical business case metric: friendly fraud is not merely the disputed transaction amount. It includes chargeback fees (USD 20-100 per dispute), operational cost of dispute response, lost merchandise, shipping costs, and Visa VAMP penalty exposure. For high-volume merchants, the aggregate cost can exceed third-party fraud losses.

The Visa VAMP program represents a structural shift in accountability. Previously, merchants bore the fraud loss but faced limited network consequences. VAMP creates escalating penalties that can ultimately revoke card acceptance, making chargeback management an existential business concern for high-dispute-ratio merchants.

The proliferation of "refund hack" tutorials is a demand-side accelerant. As awareness spreads that chargebacks are easy and consequence-free, the behavior normalizes. Payment networks and merchants should consider consequences for proven friendly fraud (network-level dispute flags, future transaction risk scoring) to create deterrence.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-27 | FLAME Project | Initial submission — sourced from Chargebacks911, Chargeflow, Payscout, Chargeback.io, Alloy, Offenso Academy intelligence |
