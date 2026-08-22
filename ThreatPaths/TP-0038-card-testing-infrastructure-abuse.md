# TP-0038: Card Testing Infrastructure Abuse

```yaml
---
id: TP-0038
title: "Card Testing Infrastructure Abuse"
category: ThreatPath
date: 2026-03-04
last_reviewed: 2026-03-04
author: "FLAME Project (sourced from Recorded Future Payment Fraud Intelligence Report 2025)"
source: "https://www.recordedfuture.com/research/annual-payment-fraud-intelligence-report-2025"
tlp: WHITE
sector:
  - payments
  - retail
  - fintech
fraud_types:
  - card-testing
  - identity-theft
  - data-theft
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "fraud-infrastructure"
primary_phase: "P3"
short_name: "Card Testing"
mitre_attack:
  - T1110.001  # Brute Force: Password Guessing (BIN enumeration)
  - T1583.001  # Acquire Infrastructure: Domains
  - T1059       # Command and Scripting Interpreter
  - T1657       # Financial Theft
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA005", "FTA007", "FTA009", "FTA010", "FT003", "FT007.009", "FT017"]
mitre_f3: ["F1038", "F1006", "F1012", "F1029", "F1046", "T1585"]
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Execution"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
confidence_score: 72
source_reliability: B
info_credibility: 2
related_tps:
  - id: TP-0035
    relationship: shares-infrastructure
  - id: TP-0030
    relationship: feeds-into
  - id: TP-0013
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-CDD
  - REG-OCC-FRAUD
baseline_ids:
  - BL-0016
  - BL-0018
tags:
  - card-testing
  - BIN-attack
  - tester-merchant
  - telegram-carding
  - enumeration-attack
  - payment-gateway-abuse
  - card-validation
---
```

---

## Summary

Card testing infrastructure abuse is a foundational enabler for payment card fraud at scale. In this threat path, threat actors use automated tools to validate stolen or enumerated card numbers against live merchant payment infrastructure, separating "live" cards (those that return successful authorization responses) from dead or canceled cards. Recorded Future's 2025 Annual Payment Fraud Intelligence Report identified over 1,350 tester merchant accounts engaged in card testing activity, with 94% of tester merchants not previously observed (an increase of 4 percentage points from 2024), demonstrating that threat actors consistently prefer newly registered merchants to evade detection controls that rely on historical reputation. The report further documented 27 million card data records exposed on Telegram during card validation attempts, representing 38% of all cards observed on the Telegram platform.

The infrastructure supporting card testing has become increasingly sophisticated and commercialized. Threat actors abuse legitimate merchants' payment infrastructure for card validation, with abused merchants ranging from a school e-commerce platform to a U.S. state court payment system. Seven new tester services joined the trend in 2025, reflecting growing commercialization of the card testing function. BIN attacks, where threat actors generate valid card numbers using specific Bank Identification Numbers (BINs) through enumeration, feed directly into the testing pipeline to produce fully validated card credentials suitable for downstream fraud. The card testing ecosystem serves as the upstream supply chain for virtually all card-not-present fraud, triangulation fraud (TP-0030), digital wallet provisioning fraud (TP-0037), and credential-stuffing-based account takeover (TP-0013). Blanket fraud controls are often ineffective for large merchants with high transaction volumes, and Recorded Future assesses that tester merchant intelligence will likely remain effective for detection and remediation into 2026. The key detection opportunity lies in identifying the distinctive transaction patterns of testing activity: high-velocity sub-dollar authorizations, elevated decline rates, and sequential card number patterns from the same BIN prefix.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors are systematically abusing legitimate and purpose-registered merchant payment infrastructure to validate stolen and BIN-enumerated card data at scale, creating a reliable upstream supply chain for card-not-present fraud, digital wallet provisioning fraud, and triangulation fraud through automated sub-dollar authorization testing that exploits gaps in merchant and acquirer velocity controls.

**Confidence**: High (72%) — confirmed by Recorded Future 2025 Annual Payment Fraud Intelligence Report documenting 1,350+ tester merchant accounts, 27M card records on Telegram linked to validation activity, and 94% new merchant preference among testers. Lower confidence than TP-0037 due to the inherently distributed and ephemeral nature of tester merchants, which makes comprehensive enumeration difficult. Intelligence on the full scope of BIN enumeration activity is limited to what is observable through payment network data.

**Estimated Impact**: $1B - $5B annually in enabled downstream fraud (card testing is an enabler, not the final fraud event); direct merchant losses from authorization fees and chargeback costs estimated at $50M - $200M; payment processor and acquirer costs from infrastructure abuse, fraud monitoring, and merchant remediation estimated at $100M - $500M. Verified cards command a 3-10x price premium over unverified cards on carding markets, making card testing a high-margin criminal enterprise.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Stolen card data acquisition | Threat actors acquire bulk stolen card data from dark web carding forums, Telegram channels, Magecart e-skimmer operations, and data breach dumps. Card data may include full track data, card-not-present data (number, expiration, CVV), or partial data requiring enrichment through BIN enumeration. | Bulk card data listings on carding forums; Telegram channels advertising fresh card dumps; data breach notifications affecting payment card databases; Magecart skimmer detections on merchant websites |
| CFPF-P1-002: Vulnerable merchant identification | Threat actors identify merchants with weak velocity controls, minimal fraud monitoring, and low-friction payment flows suitable for automated testing. Small merchants, nonprofit payment portals, school e-commerce platforms, and government payment systems are preferred due to minimal fraud infrastructure. | Automated scanning of merchant checkout flows for minimal fraud controls; reconnaissance of payment form implementations lacking CAPTCHA or device fingerprinting; identification of merchants using older payment gateway integrations with permissive authorization policies |
| CFPF-P1-003: BIN intelligence gathering | Threat actors compile BIN databases mapping Bank Identification Numbers to issuer, card type, country, and card product tier. This intelligence enables targeted BIN enumeration attacks and allows testers to prioritize high-value card products (platinum, business, corporate) that have higher credit limits and lower monitoring. | BIN database purchases on carding forums; BIN lookup tool subscriptions; sharing of BIN-to-issuer mapping data in underground channels |

**Data Sources**: Dark web monitoring, Telegram channel surveillance, carding forum intelligence, payment network BIN databases, merchant security assessment data, threat intelligence feeds.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Tester merchant account registration | Threat actors register new merchant accounts with payment processors using fabricated or stolen business identities. These purpose-registered "tester merchants" exist solely to process card validation transactions. The 94% new merchant rate indicates a deliberate strategy to use fresh accounts that lack historical fraud indicators. | Merchant account applications with newly formed business entities; merchant registrations with minimal online business presence; merchant accounts that begin processing transactions immediately upon approval with atypical transaction profiles |
| CFPF-P2-002: Legitimate merchant infrastructure abuse | Threat actors abuse payment forms on legitimate merchants' websites by submitting automated authorization requests through the merchant's existing payment infrastructure. The merchant unknowingly processes validation transactions on behalf of the tester. Abused merchants have ranged from school e-commerce platforms to U.S. state court payment systems. | Sudden spikes in authorization volume on previously low-activity merchant accounts; high volumes of sub-dollar transactions from merchant accounts with historically larger average transaction amounts; authorization requests from IP addresses or geographic regions inconsistent with the merchant's customer base |
| CFPF-P2-003: Automated testing infrastructure setup | Threat actors deploy automated scripts, bots, and API-level integrations to submit card validation requests at scale. Testing infrastructure may leverage residential proxies to distribute requests across multiple IP addresses and avoid IP-based rate limiting. | Bot traffic patterns on merchant checkout pages; automated form submission signatures (consistent timing, missing browser telemetry, headless browser indicators); high-frequency API calls to payment gateway authorization endpoints |

**Data Sources**: Payment processor merchant onboarding systems, merchant account activity monitoring, web application firewall logs, bot detection platforms, payment gateway API logs.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: BIN enumeration attack configuration | Threat actors configure BIN attack tools to systematically generate valid card numbers from specific BIN prefixes. The tools apply Luhn algorithm validation to produce card numbers that pass basic checksum verification, then test these against payment infrastructure to identify numbers associated with active accounts. | Sequential card number patterns sharing the same first 6-8 digits (BIN prefix) with incremental variation in the remaining digits; Luhn-valid card numbers that have never been issued appearing in authorization requests; high volumes of authorization requests from the same BIN prefix in short timeframes |
| CFPF-P3-002: Automated low-value transaction testing | Threat actors configure testing infrastructure for sub-dollar authorization amounts ($0.01 - $0.99) to minimize costs and avoid fraud alert thresholds. Some testers use authorization-only requests (no capture) to avoid settlement costs entirely. Testing is often conducted in off-peak hours to reduce visibility. | Sub-dollar authorization volumes exceeding normal merchant patterns; authorization-only requests without subsequent capture at rates far exceeding normal merchant behavior; testing activity concentrated in off-peak hours (midnight to 6 AM local time) |
| CFPF-P3-003: Proxy and distribution infrastructure | Residential proxy networks and rotating IP infrastructure distribute testing requests across thousands of IP addresses to avoid velocity-based blocking. Each IP may submit only a small number of requests, staying below per-IP rate limits while achieving massive aggregate volume. | Authorization requests from IP addresses associated with residential proxy networks; geographically distributed authorization sources inconsistent with merchant customer base; IP rotation patterns where sequential card tests originate from different IP addresses |

**Data Sources**: Payment gateway authorization logs, card network authorization data, IP reputation services, residential proxy detection platforms, merchant transaction monitoring.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Automated card validation at scale | Testing infrastructure submits thousands to millions of sub-dollar authorization requests against the target merchant or tester merchant account. Each request tests whether a card number is associated with an active, funded account. Successful authorizations identify "live" cards; declines identify dead, canceled, or unfunded cards. | Authorization velocity exceeding 50 transactions per minute from a single source; decline rates exceeding 70% (compared to under 15% for legitimate merchants); sub-dollar transactions comprising more than 5% of total merchant authorizations; unique card numbers per source IP per hour exceeding normal shopping patterns |
| CFPF-P4-002: BIN enumeration execution | BIN attack tools systematically test sequential card numbers within a BIN range. Starting from a known valid BIN prefix, the tool generates candidate card numbers, validates them via Luhn checksum, and submits authorization requests. Valid cards are identified by the authorization response code. | Strictly sequential card number patterns from the same BIN prefix (e.g., 4532 0100 0001 0001, 4532 0100 0001 0002, ...); very high decline rates (90%+) interspersed with occasional approvals; authorization requests with expiration dates cycling through months/years to find valid combinations |
| CFPF-P4-003: Card enrichment and verification | Cards that pass initial validation are subjected to additional testing to confirm available balance, credit limits, and address verification status. These enrichment tests may use slightly higher authorization amounts ($1-$5) and include AVS/CVV verification to build a complete card profile for premium resale. | Follow-up authorization attempts on previously validated card numbers with increasing amounts; AVS verification requests following initial sub-dollar approvals; multiple authorization attempts on the same card with different expiration dates or CVV values |

**Data Sources**: Payment network authorization data, acquirer authorization monitoring, issuer authorization and decline logs, card network fraud analytics, merchant account monitoring systems.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Verified card premium resale | Validated ("live") cards are sold at premium prices on carding markets, Telegram channels, and underground forums. Verified cards command 3-10x the price of unverified dumps. Cards enriched with balance and CVV confirmation command the highest premiums. | Carding market listings advertising "tested" or "verified" cards with specific BIN prefixes; Telegram channels offering cards with guarantee policies based on recent verification; price premiums for cards identified as recently validated |
| CFPF-P5-002: Direct card-not-present fraud | Verified cards are used directly for card-not-present (CNP) fraud — unauthorized online purchases, subscription fraud, or digital goods purchases. The testing step ensures high success rates for downstream fraud attempts, reducing the attacker's operational waste. | CNP fraud attempts using card numbers that were recently subjected to sub-dollar test authorizations; fraud clusters where all compromised cards were tested through the same tester merchant within the preceding 48 hours |
| CFPF-P5-003: Supply chain to downstream fraud operations | Verified card data feeds into multiple downstream fraud operations: digital wallet provisioning (TP-0037), triangulation fraud (TP-0030), account creation fraud, and gift card laundering. Card testing serves as the quality assurance step in the broader payment fraud supply chain. | Correlation between cards tested at known tester merchants and subsequent digital wallet provisioning fraud, triangulation fraud, or CNP fraud events; common card numbers appearing across multiple fraud types within days of testing |

**Data Sources**: Carding market intelligence, Telegram channel monitoring, payment network fraud analytics, issuer fraud case management, cross-merchant card fraud correlation, chargeback analytics.

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001 (Account Compromise) — compromised card credentials entering the testing pipeline
- FTA002 (Fraud Ring) — organized testing operations with division of labor
- FTA003 (Financial Loss) — direct and downstream financial losses from validated cards
- FTA005 (Social Engineering) — merchant social engineering for payment infrastructure access
- FTA009 (Automated Attack) — bot-driven mass card validation
- FT003 (Card Testing) — core fraud type: automated validation of stolen card credentials
- FT007.009 (BIN Attack) — systematic enumeration of card numbers by BIN prefix
- FT017 (Payment Gateway Abuse) — exploitation of merchant payment infrastructure for testing

**MITRE ATT&CK:**

- T1110.001 (Brute Force: Password Guessing) — BIN enumeration analogous to credential brute forcing
- T1583.001 (Acquire Infrastructure: Domains) — registration of tester merchant accounts and supporting infrastructure
- T1059 (Command and Scripting Interpreter) — automated testing scripts and bot infrastructure
- T1657 (Financial Theft) — downstream financial theft enabled by validated cards

**Group-IB Fraud Matrix:**

- Reconnaissance — identification of vulnerable merchants and compilation of BIN intelligence
- Resource Development — tester merchant registration, bot infrastructure deployment, proxy network setup
- Execution — automated card validation and BIN enumeration at scale
- Perform Fraud — downstream CNP fraud, digital wallet provisioning, triangulation fraud using validated cards
- Monetization — premium resale of verified cards, direct fraud, supply chain to downstream operations

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 4 (Execution)** — when merchants, acquirers, or issuers detect anomalous authorization patterns including high-velocity sub-dollar transactions, elevated decline rates, or BIN enumeration signatures. Some cases are discovered at **Phase 5** when downstream fraud events (CNP fraud, wallet provisioning fraud) are traced back to cards that were recently tested through a specific merchant. Discovery at **Phase 2** occurs when payment processors identify tester merchant accounts during onboarding review or early-life monitoring.

**Look Left** (what was missed before discovery):

- **P4 -> P3**: Were there BIN enumeration patterns (sequential card numbers from the same prefix) that should have triggered automated blocking? Were sub-dollar authorization spikes detectable in the merchant's transaction profile deviation from baseline?
- **P3 -> P2**: Was the tester merchant account flagged during onboarding as high-risk based on business age, minimal web presence, or fabricated identity elements? Were there bot signatures on the merchant's checkout page that web application firewalls should have detected?
- **P2 -> P1**: Were there dark web intelligence indicators of card dumps from specific issuers being actively traded, which could have predicted testing activity against those BIN ranges? Were there Telegram channel advertisements for new tester services that could have provided early warning?
- **Cross-team gap**: Acquirers manage merchant relationships. Payment networks monitor authorization patterns. Issuers detect fraud on individual cards. Merchants manage their own checkout security. Card testing signals span all four parties — the acquirer sees the merchant-level velocity anomaly, the payment network sees the cross-issuer BIN pattern, the issuer sees the individual card compromise, but no single party has the complete picture without cross-party data sharing.

**Look Right** (predicted next steps if uninterrupted):

- Validated cards will be listed for premium sale on carding markets and Telegram channels within 24-48 hours of testing
- BIN enumeration results will produce new valid card numbers that have never been part of a known data breach, evading breach-based fraud rules
- Validated cards will feed into digital wallet provisioning fraud (TP-0037), where they are loaded onto attacker wallets for contactless purchases
- Triangulation fraud operations (TP-0030) will use validated cards as the payment method behind fraudulent marketplace listings
- Tester merchants will be abandoned within 30-60 days as fraud controls catch up, and replacement tester merchants will be registered (the 94% new merchant rate confirms this rotation pattern)
- Card testing infrastructure and validated card databases will be offered as-a-service to downstream fraud operators, further commoditizing the attack

---

## Underground Ecosystem Context

### Actor Network and Roles

| Role | Description | Platform | Pricing Model |
|------|-------------|----------|---------------|
| Card Data Broker | Supplies bulk stolen card credentials from breaches, skimmers, and phishing | Telegram, carding forums | $5-$30 per card (unverified) |
| BIN Researcher | Compiles and sells BIN databases with issuer, country, and card tier mapping | Carding forums | $50-$500 per BIN database; subscription models |
| Tester Merchant Operator | Registers and manages merchant accounts for card testing | Underground forums | $0.01-$0.05 per card tested; subscription tiers |
| Bot Developer | Creates and maintains automated card testing scripts and infrastructure | Telegram, forums | $200-$2,000 per tool; monthly licenses |
| Proxy Network Provider | Supplies residential proxy infrastructure to distribute testing requests | Telegram, dedicated sites | $50-$500/month depending on IP pool size |
| Verified Card Reseller | Aggregates, packages, and resells validated card data at premium prices | Telegram, carding forums | $30-$300 per verified card depending on card tier and balance |
| Downstream Fraud Operator | Uses validated cards for CNP fraud, wallet provisioning, or triangulation | Multiple platforms | Varies by fraud type |

### Tester Merchant Characteristics

| Characteristic | Detail |
|----------------|--------|
| Total tester merchants identified (2025) | 1,350+ |
| Percentage new/previously unobserved | 94% (up from 90% in 2024) |
| Average operational lifespan | 30-60 days before detection/abandonment |
| Types of abused legitimate merchants | School e-commerce platforms, U.S. state court payment systems, small nonprofit donation portals, subscription services |
| New tester services in 2025 | 7 new services joining the trend |
| Abused payment infrastructure | Major retailers' payment gateways |

### Card Data on Telegram

| Metric | Value |
|--------|-------|
| Total card records observed on Telegram (2025) | ~71M (estimated from 38% ratio) |
| Card records linked to validation/testing activity | 27M (38% of total observed) |
| Primary card data channels | Carding channels, automated bot services, dump shops |
| Median time from testing to downstream fraud | 24-72 hours |

### Intelligence Sources

- Recorded Future Annual Payment Fraud Intelligence Report 2025
- Payment network authorization analytics (aggregate patterns)
- Telegram channel monitoring and OSINT
- Carding forum intelligence (underground market pricing data)
- Acquirer and issuer transaction monitoring data
- Merchant risk assessment vendor reports

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Dark web and Telegram monitoring for BIN-specific card dump listings and tester service advertisements — early warning of which BIN ranges are likely to be targeted | Detective | Threat Intelligence / Fraud Operations |
| P1 | Issuer-level monitoring for data breach indicators — proactive card reissuance for compromised BINs | Preventive | Card Issuing |
| P2 | Enhanced merchant onboarding due diligence — flag merchant applications from newly formed businesses with minimal web presence, fabricated identities, or payment profiles inconsistent with stated business type | Preventive | Acquiring / Payment Processing |
| P2 | Merchant early-life monitoring — enhanced transaction monitoring for the first 90 days of a new merchant account, with automated alerts for anomalous authorization patterns | Detective | Acquiring |
| P3 | Bot detection on merchant checkout pages — CAPTCHA, device fingerprinting, and behavioral analytics to identify automated form submissions and headless browser testing tools | Preventive | Merchant / eCommerce Platform |
| P3 | IP reputation and residential proxy detection — identify and rate-limit authorization requests from known residential proxy infrastructure and VPN exit nodes | Preventive | Payment Gateway / Acquiring |
| P4 | Sub-dollar authorization velocity controls — rate limiting and automated blocking for merchants exceeding threshold sub-dollar authorization volumes relative to their baseline profile | Detective / Preventive | Acquiring / Payment Network |
| P4 | BIN enumeration pattern detection — automated identification of sequential card number authorization attempts sharing the same BIN prefix, triggering immediate blocking and merchant investigation | Detective | Payment Network / Issuer |
| P4 | Decline rate monitoring — automated alerts when a merchant's decline rate exceeds 30% (normal baseline under 15%), indicating potential card testing activity | Detective | Acquiring |
| P5 | Cross-merchant card fraud correlation — link cards tested at known tester merchants to subsequent fraud events at other merchants, enabling proactive card blocking | Detective | Payment Network / Issuer |
| P5 | Tester merchant intelligence sharing — share identified tester merchant accounts across acquirers and payment networks to enable industry-wide blocking | Detective | Industry Consortium / Payment Network |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Organizational recognition that card testing is a distinct fraud threat requiring monitoring at the merchant, acquirer, and issuer levels; basic budget allocation for authorization pattern monitoring and merchant risk assessment tools |
| ASSESS | Level 3 (Established) | Assessment of merchant portfolio exposure to card testing abuse; evaluation of authorization velocity controls and BIN enumeration detection capabilities; identification of high-risk merchant categories susceptible to testing exploitation; gap analysis of cross-party data sharing for tester merchant intelligence |
| PLAN | Level 2 (Developing) | Basic card testing detection playbooks covering sub-dollar velocity alerts, decline rate anomalies, and BIN enumeration patterns; merchant investigation procedures for suspected tester accounts; coordination protocols between acquiring and issuing fraud teams |
| ACT | Level 3 (Established) | Automated sub-dollar authorization velocity monitoring with real-time blocking capability; BIN enumeration pattern detection at the payment network and issuer level; merchant early-life monitoring for anomalous authorization profiles; bot detection deployment on merchant checkout pages |
| MONITOR | Level 3 (Established) | KRIs for tester merchant identification rate, sub-dollar authorization volume as percentage of total, decline rate distribution across merchant portfolio, BIN enumeration detection rate, time-to-detection for new tester merchants, validated-to-fraud conversion rate for tested cards |
| REPORT | Level 2 (Developing) | Tester merchant reporting to payment networks and industry consortiums; SAR filing for identified card testing operations; issuer notification for cards confirmed as tested through known tester merchants; regulatory reporting as required |
| IMPROVE | Level 2 (Developing) | Periodic review of tester merchant detection effectiveness; decline rate threshold tuning based on false positive analysis; BIN enumeration pattern signature updates; integration of new tester service intelligence from underground monitoring |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**SQL -- Card Testing Micro-Authorization Detection (Phase 4)**

```sql
SELECT
    m.merchant_id,
    m.merchant_name,
    m.account_open_date,
    COUNT(*) AS auth_count,
    COUNT(DISTINCT a.card_number_hash) AS unique_cards,
    SUM(CASE WHEN a.response_code != '00' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) AS decline_rate,
    SUM(CASE WHEN a.amount < 1.00 THEN 1 ELSE 0 END)::FLOAT / COUNT(*) AS sub_dollar_rate,
    AVG(a.amount) AS avg_amount,
    COUNT(DISTINCT a.source_ip) AS unique_ips
FROM authorizations a
JOIN merchants m ON a.merchant_id = m.merchant_id
WHERE a.auth_timestamp > CURRENT_TIMESTAMP - INTERVAL '1 hour'
    AND a.amount < 1.00
GROUP BY m.merchant_id, m.merchant_name, m.account_open_date
HAVING COUNT(*) > 50
    AND (SUM(CASE WHEN a.response_code != '00' THEN 1 ELSE 0 END)::FLOAT / COUNT(*)) > 0.70
ORDER BY auth_count DESC;
```

**Splunk -- BIN Enumeration Pattern Detection (Phase 4)**

```spl
index=authorization sourcetype=card_auth amount<1.00
| eval bin_prefix = substr(card_number_hash, 1, 8)
| eval card_suffix = substr(card_number_hash, 9, 99)
| stats count AS auth_count,
        dc(card_number_hash) AS unique_cards,
        values(card_suffix) AS suffixes,
        sum(eval(if(response_code!="00", 1, 0))) AS declines,
        dc(source_ip) AS unique_ips
    BY bin_prefix, merchant_id
| eval decline_rate = round(declines / auth_count * 100, 1)
| where auth_count > 20 AND unique_cards > 15 AND decline_rate > 80
| eval sequential_indicator = if(unique_cards > 10 AND auth_count / unique_cards < 1.5, "HIGH", "MODERATE")
| table merchant_id, bin_prefix, auth_count, unique_cards, decline_rate, sequential_indicator, unique_ips
| sort - auth_count
```

**Sigma -- Tester Merchant Early-Life Anomaly (Phase 2-4)**

```yaml
title: New Merchant Card Testing Activity
status: experimental
description: Detects card testing patterns on merchant accounts opened within the last 90 days, characterized by high-velocity sub-dollar authorizations and elevated decline rates.
logsource:
    product: ecommerce
    service: payment_gateway
detection:
    selection:
        transaction_amount|lt: 1.00
        merchant_account_age_days|lte: 90
    aggregation:
        count|gte: 50
        groupby: merchant_id
        timeframe: 1h
    filter_decline:
        decline_rate|gte: 0.5
    condition: selection and aggregation and filter_decline
level: high
tags:
    - fraud.card_testing
    - cfpf.phase4.execution
    - attack.t1110.001
```

### Behavioral Analytics

- **Merchant authorization profile deviation**: Establish baseline authorization profiles for each merchant (average amount, volume, decline rate, card diversity). Alert when the current hour's profile deviates by more than 3 standard deviations, which captures both volume spikes and amount distribution anomalies characteristic of card testing.
- **BIN concentration analysis**: Monitor for authorization streams where more than 50% of unique card numbers share the same 6-8 digit BIN prefix. Legitimate merchant traffic shows diverse BIN distribution; BIN enumeration attacks produce extreme BIN concentration.
- **Decline rate anomaly detection**: Normal established merchants maintain decline rates under 15%. Card testing produces 70-90% decline rates. Rapid decline rate increase (from baseline to 50%+ within a 1-hour window) is a strong testing indicator.
- **Sequential card number detection**: Analyze card number patterns within authorization streams for sequential or near-sequential numbering. Any sequential card numbers from the same BIN prefix in a single merchant's authorization stream is effectively pathognomonic for BIN enumeration (zero false positive rate for legitimate merchants).

### Cross-Team Correlation

- **Acquiring -> Issuing**: Tester merchant identification should trigger proactive card monitoring and potential reissuance for all cards that returned successful authorizations at the identified tester merchant.
- **Issuing -> Payment Network**: Issuer-detected card testing (individual cards receiving sub-dollar authorizations at suspicious merchants) should be reported to the payment network for cross-issuer correlation to identify the tester merchant.
- **Payment Network -> Acquiring**: Payment network-level BIN enumeration detection should trigger acquirer investigation of the originating merchant account, including potential account suspension and remediation requirements.
- **Threat Intelligence -> Fraud Operations**: Underground monitoring intelligence on new tester services, BIN attack tools, and validated card resale channels should feed into fraud operations detection rule tuning and merchant risk scoring models.
- **Merchant -> Acquiring**: Merchants detecting bot activity on their checkout pages should report to their acquirer, as this may indicate that the merchant's payment infrastructure is being abused for card testing without the merchant's knowledge.

---

## References

- **Recorded Future -- Annual Payment Fraud Intelligence Report 2025**: Primary source documenting 1,350+ tester merchant accounts, 94% new merchant rate, 27M card records on Telegram linked to validation activity, 7 new tester services in 2025, and abused merchant examples including school e-commerce and U.S. state court payment systems. [Link](https://www.recordedfuture.com/research/)

- **Payment Card Industry Data Security Standard (PCI DSS) v4.0**: Framework requirements for merchant and payment processor security controls, including authorization monitoring and anomaly detection capabilities relevant to card testing detection. [Link](https://www.pcisecuritystandards.org/document_library/)

- **Visa Account Attack Intelligence (VAAI)**: Visa's card testing detection and reporting service providing payment network-level visibility into BIN enumeration and tester merchant activity. [Link](https://usa.visa.com/)

- **Mastercard Decision Intelligence**: Mastercard's authorization scoring system incorporating card testing pattern detection as an input to real-time authorization decisions. [Link](https://www.mastercard.com/)

- **Related FLAME Threat Paths**: [TP-0030: eCommerce Triangulation Fraud](TP-0030-ecommerce-triangulation-fraud.md) (downstream consumer of validated cards); [TP-0037: Digital Wallet Fraud & NFC Relay Attacks](TP-0037-digital-wallet-nfc-relay-fraud.md) (validated cards used for wallet provisioning); [TP-0013: Credential Stuffing & Loyalty Point Drain](TP-0013-credential-stuffing-loyalty-drain.md) (shared automated attack infrastructure).

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-04 | FLAME Project | Initial submission -- sourced from Recorded Future Annual Payment Fraud Report 2025 |
