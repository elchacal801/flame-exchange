# TP-0031: Refund-as-a-Service (FTID / RaaS)

```yaml
---
id: TP-0031
title: "Refund-as-a-Service (FTID / RaaS)"
category: ThreatPath
date: 2026-03-02
author: "FLAME Project"
source: "Original Research — aggregated from NRF, industry reporting, and underground market analysis"
tlp: WHITE
sector:
  - retail
fraud_types:
  - first-party-fraud
  - refunding-as-a-service
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "retail-ecommerce"
primary_phase: "P4"
short_name: "Refund-as-a-Service"
mitre_attack:
  - T1589.002  # Gather Victim Identity Information: Email Addresses
  - T1585.001  # Establish Accounts: Social Media Accounts
  - T1656      # Impersonation
  - T1657      # Financial Theft
ft3_tactics: ["FTA001", "FTA003", "FTA004", "FTA006", "FTA009", "FTA010", "FT003", "FT006.001", "FT016", "FT028", "FT031", "FT052.003"]
mitre_f3: ["F1015", "F1024", "F1043"]
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
confidence_score: 72
source_reliability: C
info_credibility: 2
related_tps:
  - id: TP-0016
    relationship: related-to
  - id: TP-0030
    relationship: shares-infrastructure
regulatory_refs:
  - REG-NRF-RFT-V1
baseline_ids:
  - BL-0008
tags:
  - refund-fraud
  - FTID
  - DNA
  - SNAD
  - e-commerce
  - return-abuse
  - social-engineering
  - organized-fraud
  - telegram
  - nrf-rft
---
```

---

## Summary

Organized Refund-as-a-Service (RaaS) operations monetize retailer return policies at industrial scale by filing fraudulent refund claims on behalf of paying customers. Professional "refunders" operating through Telegram channels and underground forums charge 15-40% commission per successful refund, employing techniques such as Fake Tracking ID (FTID), Did Not Arrive (DNA), and Significantly Not As Described (SNAD) claims. With return fraud contributing to an estimated $103B in annual losses across U.S. retail, and some RaaS operations processing over 1,000 refunds per month, this threat path represents a mature, professionalized fraud-as-a-service ecosystem operating in the gray zone between first-party fraud and organized crime.

---

## Threat Path Hypothesis

> **Hypothesis**: Organized fraud operators are running professionalized Refund-as-a-Service businesses that exploit retailer return and refund policies through FTID, DNA, and SNAD techniques at scale, targeting major e-commerce and omnichannel retailers in the retail sector, resulting in systemic refund losses, inventory shrinkage, and policy erosion.

**Confidence**: High — based on extensive industry reporting (NRF, Appriss Retail), law enforcement actions, and direct observation of underground RaaS marketplaces operating openly on Telegram.

**Estimated Impact**: $50 – $5,000 per individual refund claim. At scale, a single RaaS operation processing 1,000+ refunds/month generates $500K – $2M+ in fraudulent refunds monthly. Industry-wide return fraud totals an estimated $103B annually.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Return policy analysis | RaaS operators systematically study retailer return, refund, and shipping policies to identify exploitable gaps — weight-based vs. scan-based delivery confirmation, return window lengths, refund thresholds that bypass manual review, and carrier-specific tracking behaviors. | N/A (external research; not directly observable by retailers) |
| CFPF-P1-002: Carrier and logistics reconnaissance | Operators map carrier delivery confirmation methods (signature required thresholds, GPS delivery verification, photo-on-delivery) to identify which shipping methods are vulnerable to FTID or DNA claims. | Unusual pattern of delivery method inquiries on customer service channels; probing questions about carrier policies |
| CFPF-P1-003: Customer account acquisition | RaaS operators recruit customers (termed "clients") through Telegram channels, Discord servers, and underground forums. Clients provide their order details and account credentials to the refunder. | Telegram/Discord channels advertising refund services; recruitment posts on social media and forums |

**Data Sources**: Customer service interaction logs, social media monitoring, threat intelligence feeds monitoring underground fraud channels, delivery carrier policy documentation.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Client account handoff | The paying customer (client) provides their retailer account credentials, order numbers, and personal details to the RaaS operator, who then acts on their behalf. The operator may also use the client's email to intercept communications. | Multiple accounts accessed from shared IP ranges or device fingerprints; login location shifts coinciding with refund requests |
| CFPF-P2-002: Social engineering script deployment | RaaS operators use refined, retailer-specific social engineering scripts when contacting customer service. Scripts include emotional manipulation tactics, legal threats, and escalation procedures tailored to each retailer's support workflow. | Customer service contacts using scripted language patterns; unusually assertive or legally threatening refund requests; identical phrasing across multiple unrelated customer accounts |
| CFPF-P2-003: Contact channel selection | Operators choose the optimal contact channel (live chat, phone, email, social media) based on which channel has the most lenient refund approval authority or least experienced agents. | Disproportionate refund requests through specific channels; channel switching mid-claim |

**Target**: Institution (retailer customer service, returns processing)

**Data Sources**: Customer service CRM logs, chat transcripts, call recordings, email correspondence, account authentication logs, device fingerprinting systems.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: FTID (Fake Tracking ID) setup | Operator generates or obtains a valid tracking number that shows delivery to a different address or a carrier facility, then uses label manipulation (partial address, incorrect zip code routing) to ensure the return package is either lost in transit or delivered to an unmonitored location, while tracking shows "delivered." | Return tracking numbers that resolve to addresses different from the customer's; tracking showing delivery to carrier facilities rather than retailer warehouses; label anomalies (missing suite numbers, transposed zip codes) |
| CFPF-P3-002: Empty or partial return staging | For retailers requiring physical returns, operators send back empty boxes, boxes filled with weighted substitutes (sand, rocks, cheap items), or partial returns while claiming the full order was returned. | Return package weights inconsistent with expected product weight; return packages with correct dimensions but wrong weight profile; photo documentation showing non-matching contents |
| CFPF-P3-003: Documentation fabrication | Operators create falsified photo evidence (damaged products, wrong items received), fabricated delivery exception screenshots, or manipulated tracking status images to support SNAD or DNA claims. | Metadata inconsistencies in submitted photos (EXIF data, timestamps); reverse image search matches; photos reused across multiple claims from different accounts |

**Data Sources**: Returns processing systems, carrier tracking APIs, warehouse receiving logs, photo/document submission systems with metadata analysis, package weight verification records.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: DNA (Did Not Arrive) claim | Operator contacts retailer claiming the order was never received despite carrier tracking showing delivery. Exploits the gap between carrier delivery confirmation and retailer willingness to dispute with customers. | Refund claims on orders with confirmed delivery; disproportionate DNS claims from addresses with high delivery success rates; repeated DNA claims from same address or account |
| CFPF-P4-002: SNAD (Significantly Not As Described) claim | Operator claims received item was defective, wrong, or significantly different from the listing. Often paired with fabricated photo evidence. Retailer issues refund without requiring return for low-value items or when return shipping cost exceeds item value. | SNAD claims on items rarely reported as defective; SNAD claim rates exceeding product defect baselines; claims that precisely match refund-without-return thresholds |
| CFPF-P4-003: Refund method manipulation | Operator requests refund to a different payment method than the original purchase (gift card, store credit, alternative card) to complicate clawback and enable resale of credits. | Refund method change requests; refunds to payment methods added post-purchase; gift card refunds on high-value orders |
| CFPF-P4-004: Escalation and threat tactics | When initial claim is denied, operators escalate through supervisors, threaten chargebacks, invoke consumer protection regulations, or threaten negative social media exposure to pressure approval. | Claims with multiple escalation attempts; legal or regulatory language in customer communications; chargeback threats following denied refund requests |

**Data Sources**: Refund processing systems, customer service case management, chargeback monitoring, gift card/store credit issuance logs, payment method modification logs.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Commission collection | RaaS operator collects 15-40% commission from the client, typically via cryptocurrency (BTC, USDT), peer-to-peer payment apps, or gift cards. Client retains the refunded item and the remaining refund value. | N/A (transaction occurs outside retailer visibility on P2P platforms) |
| CFPF-P5-002: Gift card and store credit resale | When refunds are issued as gift cards or store credits, operators resell them on secondary markets (gift card exchanges, underground forums) at 60-80% face value. | Gift cards redeemed from unusual geographic locations; rapid full-balance redemption of refund gift cards; gift cards appearing on resale platforms shortly after issuance |
| CFPF-P5-003: Repeat client monetization | Successful refunds drive repeat business — clients return to the same RaaS operator for future orders, creating ongoing revenue streams. Operators build client portfolios and track retailer-specific success rates. | Same accounts generating repeated refund claims across multiple orders; temporal patterns in refund activity suggesting scheduled/batched operations |

**Data Sources**: Gift card transaction monitoring, secondary market monitoring, payment platform analytics, customer lifetime refund analysis.

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001 (Account Compromise) — client account handoff to RaaS operator
- FTA003 (Social Engineering) — scripted social engineering of customer service agents
- FTA006 (Abuse of Functionality) — systematic exploitation of return policies and refund thresholds
- FTA009 (First-Party Fraud) — client colludes with operator; technically the account holder authorizes the fraud
- FT028 (Return/Refund Fraud) — core technique category
- FT031 (Policy Abuse) — systematic exploitation of lenient return policies

**MITRE ATT&CK:**

- T1589.002 (Gather Victim Identity Information: Email Addresses) — operators collect client account details and retailer employee identifiers for social engineering
- T1585.001 (Establish Accounts: Social Media Accounts) — RaaS operators maintain Telegram/Discord presence for client recruitment
- T1656 (Impersonation) — operators impersonate the customer when contacting retailer support
- T1657 (Financial Theft) — end goal of fraudulent refund extraction

**Group-IB Fraud Matrix:**

- Reconnaissance — return policy analysis, carrier logistics mapping
- Resource Development — social engineering script creation, FTID label generation tooling
- Trust Abuse — exploitation of retailer-customer trust relationship and lenient return policies
- End-user Interaction — social engineering of customer service agents
- Perform Fraud — filing fraudulent refund claims (DNA, SNAD, FTID)
- Monetization — commission collection, gift card resale

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 4 (Execution)** — when refund rates spike above baseline, when returns processing identifies empty/wrong-weight packages, or when pattern analysis flags serial refunders. Occasionally discovered at **Phase 3** when warehouse staff intercept suspicious return packages.

**Look Left** (what was missed before discovery):

- **P4 → P3**: The FTID label manipulation and empty box returns should have been caught at warehouse receiving with weight verification and package inspection protocols. Were return packages being weighed and compared to expected product weights?
- **P3 → P2**: The social engineering scripts used on customer service follow recognizable patterns. Were customer service interactions being analyzed for scripted language, unusual assertiveness, or cross-account phraseology matches?
- **P2 → P1**: Accounts accessed by RaaS operators show device/IP fingerprint anomalies compared to the customer's baseline. Was device intelligence being applied to accounts filing refund claims?
- **Cross-team gap**: Loss prevention teams see shrinkage numbers. Customer service sees individual claims. E-commerce fraud teams see chargeback patterns. Nobody correlates refund claims across channels (chat, phone, email) to identify the same operator working multiple client accounts.

**Look Right** (predicted next steps if uninterrupted):

- Successful operators expand client base and increase volume, potentially processing hundreds of refunds weekly
- RaaS operators who find a reliable method against a specific retailer will exploit it until the policy is patched, then pivot to alternative techniques
- Gift card refunds will appear on secondary markets within 24-48 hours
- Clients who successfully defraud one retailer will target others, creating cross-retailer fraud networks
- Escalation from individual refund fraud to organized retail crime (ORC) with warehouse-scale return fraud operations

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Refunder (Operator) | End-to-end refund claim processing | High | 15-40% commission per successful refund |
| FTID Specialist | Fake tracking ID generation and label manipulation | High | $20-50 per FTID label or bundled into refunder commission |
| Script Writer | Social engineering scripts tailored to specific retailers | Medium | $50-200 per retailer-specific script package |
| Account Provider | Aged retailer accounts with clean refund history | Medium | $10-50 per account depending on retailer and order history |
| Reshipping Mule | Receives and redirects FTID return packages | Medium | $15-30 per package handled |

### Tool Ecosystem
- FTID label generation tools and address manipulation utilities
- Carrier tracking lookup APIs for identifying exploitable delivery confirmation methods
- Customer service chatbot detection/bypass tools
- Photo/screenshot editing tools for fabricating damage evidence
- Bulk order management tools for tracking multiple client refunds simultaneously

### Underground Marketplace Presence
RaaS operations are highly visible on Telegram (dedicated channels with thousands of subscribers, vouched refunder directories, client testimonial systems), Discord servers (often disguised as "deals" or "savings" communities), and English-language fraud forums. Activity level is extremely high — RaaS is one of the most accessible and openly advertised fraud services in the underground economy, with low barriers to entry for both operators and clients.

### Intelligence Sources
- NRF (National Retail Federation) annual retail security surveys and return fraud estimates
- Appriss Retail Consumer Returns in the Retail Industry reports
- FBI IC3 reporting on organized retail crime
- Industry-specific threat intelligence from major e-commerce platform trust & safety teams

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor underground channels (Telegram, forums) for RaaS operators targeting your brand specifically | Detective | Threat Intelligence |
| P1 | Implement dynamic return policies that adjust based on customer risk scoring rather than static thresholds | Preventive | E-commerce / Policy |
| P2 | Deploy NLP analysis on customer service interactions to detect scripted social engineering patterns | Detective | Fraud Ops / Customer Service |
| P2 | Device fingerprinting and IP analysis on accounts initiating refund claims to detect operator-controlled sessions | Detective | Fraud Ops |
| P3 | Mandatory weight verification for all return packages at warehouse receiving with automated tolerance checks | Detective | Returns Processing / Logistics |
| P3 | Photo/document metadata analysis (EXIF data, reverse image search) for submitted damage evidence | Detective | Fraud Ops |
| P3 | FTID detection: validate return tracking delivers to an authorized returns facility, not an intermediate address | Detective | Logistics / Fraud Ops |
| P4 | Customer-level refund velocity monitoring: flag accounts exceeding refund rate baselines by product category | Detective | Fraud Ops |
| P4 | Cross-channel refund claim correlation: identify identical refund patterns across chat, phone, and email | Detective | Fraud Ops |
| P4 | Require video evidence for high-value SNAD claims rather than static photos | Preventive | Customer Service |
| P5 | Restrict refund method changes — refunds to original payment method only for orders above threshold | Preventive | E-commerce / Finance |
| P5 | Gift card velocity monitoring: flag rapid redemption or resale of refund-issued gift cards | Detective | Fraud Ops |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Executive recognition that refund fraud is an organized threat requiring dedicated fraud resources, not just a cost-of-doing-business shrinkage line item; cross-functional mandate connecting loss prevention, customer service, and fraud operations |
| ASSESS | Level 3 (Established) | Comprehensive refund fraud risk assessment including policy gap analysis, carrier vulnerability mapping, and customer service social engineering exposure evaluation; quantified refund fraud loss baseline by category and channel |
| PLAN | Level 3 (Established) | Documented refund fraud playbooks for customer service agents; FTID detection procedures for returns processing; dynamic return policy framework with risk-tiered thresholds; underground monitoring program for brand-specific RaaS activity |
| ACT | Level 3 (Established) | Automated refund velocity monitoring with customer-level risk scoring; weight verification systems at returns processing; NLP-based script detection on customer service channels; cross-channel claim correlation engine |
| MONITOR | Level 3 (Established) | KRIs for refund rate by category, DNA claim rate vs. carrier delivery confirmation rate, SNAD claim rate vs. product defect baselines, return package weight discrepancy rate, customer-level refund lifetime value tracking |
| REPORT | Level 2 (Developing) | Refund fraud loss reporting disaggregated by technique (DNA, SNAD, FTID, empty box); suspicious pattern reporting to law enforcement for organized operations; cross-retailer intelligence sharing through industry consortia |
| IMPROVE | Level 3 (Established) | Continuous return policy tuning based on fraud pattern analysis; post-incident reviews linking individual claims to organized RaaS campaigns; customer service script detection model retraining based on emerging social engineering patterns |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**SQL — Refund Velocity Anomaly Detection (Phase 4) — Detection Logic: DL-0062**

```sql
SELECT
    customer_id,
    COUNT(*) AS refund_count_90d,
    SUM(refund_amount) AS total_refund_value_90d,
    COUNT(DISTINCT order_id) AS orders_with_refunds,
    ROUND(SUM(refund_amount) / NULLIF(SUM(order_total), 0) * 100, 2) AS refund_rate_pct,
    COUNT(CASE WHEN refund_reason = 'DNA' THEN 1 END) AS dna_claims,
    COUNT(CASE WHEN refund_reason = 'SNAD' THEN 1 END) AS snad_claims
FROM refunds r
JOIN orders o ON r.order_id = o.order_id
WHERE r.refund_date >= DATEADD(day, -90, GETDATE())
GROUP BY customer_id
HAVING COUNT(*) > 3
   AND SUM(refund_amount) > 500
ORDER BY total_refund_value_90d DESC;
```

**Sigma — Return Package Weight Discrepancy (Phase 3) — Detection Logic: DL-0064**

```yaml
title: Return Package Weight Discrepancy - Potential Empty Box or FTID
status: experimental
description: Detects return packages where received weight deviates significantly from expected product weight, indicating empty box returns or substitute-filled packages.
logsource:
    product: returns_processing
    service: warehouse
detection:
    selection:
        event_type: "return_received"
    filter_weight_mismatch:
        weight_delta_pct|gte: 30
    condition: selection and filter_weight_mismatch
level: high
tags:
    - fraud.refund
    - cfpf.phase3.positioning
```

**Splunk — Cross-Account Refund Operator Detection (Phase 2) — Detection Logic: DL-0065**

```spl
index=customer_service sourcetype=refund_claims
| stats count AS claim_count, dc(customer_id) AS unique_customers, values(customer_id) AS customers BY device_fingerprint, src_ip
| where unique_customers > 2 AND claim_count > 5
| eval suspicious_operator = if(unique_customers > 3 AND claim_count > 10, "HIGH", "MEDIUM")
| table device_fingerprint, src_ip, unique_customers, claim_count, customers, suspicious_operator
| sort - unique_customers
```

### Behavioral Analytics

- **Customer refund lifetime scoring**: Build per-customer refund profiles tracking refund frequency, value, technique (DNA vs. SNAD vs. return), and success rate. Flag accounts whose refund behavior deviates significantly from peer cohort baselines.
- **Serial refunder clustering**: Apply network analysis to identify clusters of accounts that share device fingerprints, IP addresses, payment methods, or shipping addresses — indicators of a single RaaS operator working multiple client accounts.
- **DNA claim vs. carrier confirmation correlation**: Cross-reference DNA claims with carrier GPS delivery confirmation and photo-on-delivery records. Accounts with high DNA claim rates but high carrier confirmation rates are strong FTID/DNA fraud indicators.
- **Social engineering script detection**: NLP models trained on known RaaS scripts to flag customer service interactions matching scripted language patterns, unusual formality, or cross-account phrase reuse.

### Cross-Team Correlation

- **Loss Prevention -> Fraud Ops**: Shrinkage data from returns processing (empty boxes, wrong items, weight discrepancies) should feed into fraud case management for correlation with refund claim patterns.
- **Customer Service -> Fraud Ops**: Scripted interaction patterns, escalation threats, and high-pressure refund requests should be flagged and correlated with account-level refund analytics.
- **Fraud Ops -> Threat Intelligence**: Identified RaaS operator device/IP fingerprints and techniques should feed into underground monitoring for attribution and campaign-level intelligence.
- **Fraud Ops -> Legal/Law Enforcement**: Organized RaaS operations processing high volumes should be packaged for law enforcement referral with evidence of interstate organized retail crime.

---

## Operational Evidence

### EV-TP0031-2026-001: NRF Retail Fraud Taxonomy — Checkout and Return Fraud Techniques

- **Source**: NRF Retail Fraud Taxonomy v1.0 (November 2024)
- **CFPF Phase Coverage**: P4–P5
- **Confidence**: High
- **Summary**: NRF RFT documents Checkout techniques (FT1303) covering POS, guest services, and online channels used to convert illicit resources into liquid funds. Mitigations include restocking fees (FM1009) and delayed reimbursement (FM1010). NRF and expanded partners are developing v2.0 specifically to address return and refund fraud — validating FLAME's early coverage of refund-as-a-service as a distinct threat path. The NRF RFT is one of three foundational inputs to MITRE F3, which will also model cash-out and monetization activities.

---

## References

- **NRF 2024 National Retail Security Survey**: Industry-wide return fraud loss estimates; documents the $103B annual return fraud figure and rising trend in organized refund abuse. [Link](https://nrf.com/research/national-retail-security-survey)

- **Appriss Retail — Consumer Returns in the Retail Industry (2024)**: Detailed breakdown of return fraud typologies including FTID, DNA, and SNAD, with retailer survey data on policy exploitation patterns.

- **FBI IC3 — Organized Retail Crime Reporting**: Federal law enforcement perspective on the intersection of online refund fraud and organized retail crime networks.

- **Related FLAME Threat Paths**: [TP-0016: First-Party Fraud](TP-0016-first-party-fraud.md) (foundational first-party fraud patterns); [TP-0030: E-Commerce Triangulation Fraud] (e-commerce fraud ecosystem overlap).

- NRF Retail Fraud Taxonomy v1.0 (November 2024) — FT1303 Checkout techniques; v2.0 in development adding return/refund fraud

---

## Analyst Notes

**The professionalization problem**: RaaS represents a maturation of what was once opportunistic individual refund abuse into a fully professionalized fraud-as-a-service ecosystem. Operators maintain client portfolios, track success rates by retailer, run customer satisfaction programs (client vouching systems), and operate with business-like structures. This professionalization makes the threat fundamentally different from individual first-party fraud (see TP-0016) — the operator brings expertise, tooling, and scale that individual fraudsters lack.

**Policy arbitrage is the core vulnerability**: RaaS operators exploit the tension between customer experience (fast, frictionless refunds) and fraud prevention (friction, verification, delays). Retailers who tighten policies risk losing legitimate customers; those who maintain lenient policies become preferred targets in the RaaS ecosystem. This creates a competitive dynamic where the most customer-friendly retailers absorb disproportionate fraud losses.

**The FTID technique is particularly difficult to detect**: Unlike DNA claims (which can be countered with carrier delivery confirmation) or SNAD claims (which can be countered with return inspection), FTID exploits the logistics system itself — the return appears to be in transit or delivered, but it never reaches the retailer's returns facility. Detection requires end-to-end tracking validation that many retailers lack.

**Loss quantification is challenging**: Because RaaS clients are also legitimate customers making legitimate purchases, isolating fraudulent refunds from legitimate returns requires sophisticated analytics. The $103B annual figure includes both organized RaaS and opportunistic individual abuse, making it difficult to quantify the organized component precisely.

**Cross-retailer intelligence sharing is nascent**: Unlike financial services (where FS-ISAC facilitates information sharing), the retail sector lacks a mature cross-company intelligence sharing mechanism for refund fraud. RaaS operators exploit this by rotating across retailers when one tightens controls.

---

## Distinction from Friendly Fraud & Chargeback Abuse

TP-0031 covers **merchant-level refund exploitation** — fraudsters abuse the merchant's return/refund process (fake tracking IDs, DNA claims, partial returns, refunder-as-a-service). The remediation pathway is between customer and merchant.

**TP-0075 (Friendly Fraud & Chargeback Abuse)** covers **payment-network-level dispute exploitation** — customers file chargebacks directly with their issuing bank after receiving goods/services, bypassing the merchant entirely. The remediation pathway involves the payment network (Visa, Mastercard) arbitration process.

These are distinct threat models:
- **TP-0031**: Customer → Merchant (refund process) → Value extraction
- **TP-0075**: Customer → Issuing Bank → Payment Network (chargeback process) → Merchant debited

Both may be used by the same actor but represent different operational pathways with different detection signals and different stakeholder impacts.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-02 | FLAME Project | Initial submission |
