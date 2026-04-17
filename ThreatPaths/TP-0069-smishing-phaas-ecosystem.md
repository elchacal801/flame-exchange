# TP-0069: Smishing PhaaS Ecosystem — Darcula, Smishing Triad, and Mass-Messaging Credential Harvest

```yaml
---
id: TP-0069
title: "Smishing PhaaS Ecosystem — Darcula, Smishing Triad, and Mass-Messaging Credential Harvest"
category: ThreatPath
date: 2026-03-23
author: "FLAME Project"
source: "Phishing kits and AiTM platforms: a comprehensive threat intelligence reference (2026)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - smishing
  - phishing
  - card-not-present-fraud
  - identity-theft
  - fraud-as-a-service
sector:
  - cross-sector
  - banking
  - retail
  - payments
  - government
  - transportation
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 80
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1566.002  # Phishing: Spearphishing Link
  - T1598      # Phishing for Information
  - T1583.001  # Acquire Infrastructure: Domains
  - T1583.003  # Acquire Infrastructure: Virtual Private Server
  - T1656      # Impersonation
  - T1539      # Steal Web Session Cookie
ft3_tactics: ["FTA001", "FTA002", "FT007.009", "FT011.001", "FT016.001"]
mitre_f3: ["F1006.002", "F1038", "F1001", "F1012", "F1019", "F1029", "F1040", "F1048", "T1189", "T1555"]
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "Credential Access"
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
  - id: TP-0067
    relationship: related-to
  - id: TP-0023
    relationship: shares-infrastructure
  - id: TP-0008
    relationship: related-to
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-CFPB-REGE
  - REG-WCI-2024
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - smishing
  - darcula
  - magic-cat
  - smishing-triad
  - lucid
  - lighthouse
  - chenlun
  - panda-shop
  - imessage-exploitation
  - rcs-phishing
  - phaas
  - toll-scam
  - card-not-present
  - wci-geographic-attribution
  - phaas-market-fragmentation
  - vacuum-effect
  - bluekit
  - kratos
  - evilTokens
  - interisle-2025
  - xinxin-lucid
  - dominet-hk
  - xin-tld
---
```

## Summary

The Smishing PhaaS Ecosystem is a loosely federated Chinese-speaking cybercrime network — collectively known as the Smishing Triad — that operates industrialized smishing infrastructure at unprecedented scale: 194,000+ malicious domains registered since January 2024, 884,000+ credit cards compromised in a seven-month period, and victims in 121+ countries. The ecosystem centers on three major Phishing-as-a-Service (PhaaS) platforms — Darcula (tracked as LARVA-246), Lucid (operated by XinXin Group / LARVA-242), and Lighthouse (developed by Wang Duo Yu / LARVA-241) — supported by independent kit developers (Chenlun), bulk SMS enablers (Oak Tel/Carrie SMS), and dedicated smishing message platforms (Panda Shop, StupidFISH). What distinguishes this threat path from traditional SMS phishing is the exploitation of Apple iMessage and Android RCS to bypass carrier-level SMS filtering, real-time character-by-character credential streaming via Magic Cat, and the integration of GenAI-powered phishing form generation (darcula-suite 3.0). FBI IC3 received 59,271 toll-scam complaints in 2024 alone, reflecting the scale of the toll/road fee lure campaign impersonating E-ZPass, SunPass, FasTrak, and I-Pass across 8+ U.S. states.

**Distinction from TP-0067**: TP-0067 covers AiTM phishing kit infrastructure focused on session token hijacking and MFA bypass via reverse proxy. TP-0069 covers the smishing delivery ecosystem — the SMS/iMessage/RCS-based credential harvest pipeline, the PhaaS platforms that power it, and the supporting bulk messaging and kit development infrastructure specific to mobile messaging channels.

## Threat Path Hypothesis

> **Hypothesis**: The Smishing Triad ecosystem has industrialized mobile-channel credential theft by combining PhaaS platforms (Darcula, Lucid, Lighthouse) with bulk messaging infrastructure (Oak Tel, Panda Shop) and independent kit developers (Chenlun) to deliver smishing lures at scale via iMessage, RCS, and SMS. The ecosystem exploits the fact that iMessage and RCS messages bypass traditional carrier-level SMS filtering — victims are prompted to reply "Y" to enable link clickability in iMessage, circumventing Apple's link-disabling protection for unknown senders. Once victims click the link, Magic Cat streams entered credentials character-by-character in real time, enabling immediate OTP interception and card-not-present fraud. The toll/road fee scam lure is the dominant vector in the U.S. market, exploiting urgency ("overdue toll — pay now to avoid penalty"). The ecosystem's PhaaS model means operators require no technical skill — Lighthouse subscriptions start at $88/week, and Oak Tel provides bulk SMS at $8 per 1,000 texts with sender ID spoofing for major financial institutions.

**Confidence**: High — Resecurity, Netcraft, PRODAFT, NRK/Mnemonic, and FBI IC3 have published independent analyses. Google filed a RICO lawsuit against Darcula operators in November 2025. PRODAFT has attributed Darcula to a specific developer (Yucheng C., Henan province).

**Estimated Impact**: 884,000+ cards compromised in seven months across 121+ countries. FBI IC3 received 59,271 toll-scam complaints in 2024. Individual victim losses range from $50–$5,000 per compromised card. Aggregate ecosystem revenue estimated in the hundreds of millions annually. Lucid achieves ~5% success rate (versus typical <2% for traditional phishing), indicating high lure effectiveness.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| PhaaS platform procurement | Operators subscribe to Darcula, Lucid, or Lighthouse PhaaS platforms via Telegram channels. Lighthouse pricing: $88/week to $1,588/year. Lucid operated by XinXin Group (LARVA-242). ~600 cybercrime groups use Darcula | Telegram channel subscriptions for PhaaS services; USDT cryptocurrency payments to known PhaaS wallets |
| Bulk messaging infrastructure setup | Operators provision bulk SMS/iMessage/RCS delivery through Oak Tel/Carrie SMS ($8/1,000 texts) or Panda Shop (2 million messages/day capacity). Sender ID spoofing configured for Chase, Bank of America, Wells Fargo, Citi | Accounts created on Oak Tel (oak-tel[.]com); bulk message sending configurations with spoofed sender IDs; iMessage account farms |
| Domain registration and kit deployment | Mass registration of domains for phishing landing pages. Darcula: 90,000+ flagged domains. Infrastructure hosted on Tencent (AS132203) and Alibaba (AS45102). Container registry: registry[.]magic-cat[.]world | Bulk domain registrations on Chinese hosting providers; domains with toll/postal/government impersonation patterns; SSL certificates issued for newly registered domains |
| Lure template selection | Operators select from pre-built lure templates: toll/road fee scams (E-ZPass, SunPass, FasTrak, I-Pass), package delivery (USPS, DHL, Royal Mail), government services, financial institutions. GenAI form generation available in darcula-suite 3.0 | Phishing pages matching known Darcula/Lucid/Lighthouse template fingerprints; pages containing ResourceRedConfig.js or /ResourceConfig/urlConfig.json (Chenlun kits) |

**Data Sources**: Threat intelligence feeds (PRODAFT, Resecurity, Netcraft), Telegram OSINT monitoring, domain registration monitoring, Certificate Transparency logs, hosting provider abuse reports

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| iMessage exploitation | Smishing messages delivered via Apple iMessage, bypassing carrier SMS filters entirely. Victims prompted to reply "Y" to re-enable link clickability (iMessage disables links from unknown senders). Apple iOS 26 introduced "Screen Unknown Senders" as mitigation | iMessage delivery from unknown senders containing toll/postal/government lures; messages requesting reply before link engagement; iMessage originating from newly created Apple IDs |
| RCS/SMS delivery | Messages delivered via Android RCS or traditional SMS through bulk providers. Oak Tel enables sender ID spoofing for major banks. Panda Shop capable of 2 million messages daily | SMS/RCS from spoofed sender IDs matching financial institutions; high-volume messages from single originating infrastructure; messages containing shortened URLs to recently registered domains |
| Real-time credential capture via Magic Cat | When victim clicks the link and enters credentials, Magic Cat (Darcula's core toolkit) streams data character-by-character in real time to the operator, enabling immediate interception of OTPs and card details | Real-time WebSocket connections from phishing domains to C2 infrastructure; credential submission events with character-level granularity in server logs |

**Target**: Mobile device users — toll road users, online shoppers expecting packages, banking customers, government service users

**Data Sources**: Mobile carrier abuse reports, iMessage/RCS delivery logs, phishing domain traffic analysis, victim complaint databases (FBI IC3)

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| OTP interception in real time | Magic Cat's character-by-character streaming enables operators to capture OTPs as victims enter them, before they expire. This allows immediate use of the OTP for account access or transaction authorization | OTP usage from IP/device different from the requesting device within seconds of issuance; OTP redemption from geographic location inconsistent with the victim's location |
| Card data capture and aggregation | Full card details (PAN, expiry, CVV) captured from phishing forms and aggregated into operator databases. 884,000+ cards compromised in seven months across the ecosystem | Card data appearing in underground markets shortly after smishing campaigns targeting specific regions; new card-not-present fraud on cards whose holders reported smishing messages |
| PII harvesting for identity theft | StupidFISH and other kits harvest additional PII including SSN, driver's license, ID.me credentials for downstream identity theft | Identity theft reports correlated with prior smishing complaint filings; ID.me account compromises following smishing campaigns |

**Data Sources**: OTP redemption logs, card network fraud alerts, identity theft complaint databases, dark web card shop monitoring

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Card-not-present fraud | Stolen card data used for online purchases, often within hours of capture to outpace card replacement. High-velocity CNP transactions across multiple merchants | CNP transactions on cards whose holders filed smishing complaints within prior 24–72 hours; transactions from device fingerprints or IPs associated with known fraud clusters |
| Identity theft using harvested PII | PII harvested via StupidFISH and similar kits used for new account fraud, account takeover, tax fraud, and benefits fraud (including ID.me exploitation) | New account applications using PII from victims who reported smishing; credit inquiries for individuals with recent smishing complaints |
| Card tokenization for mobile wallets | Stolen card details provisioned into mobile wallets (Apple Pay, Google Pay) for in-person contactless fraud, bypassing CNP fraud controls | Card provisioning attempts from devices/locations inconsistent with cardholder profile; multiple cards provisioned to single device in rapid succession |

**Data Sources**: Card network transaction monitoring, identity theft alert systems, mobile wallet provisioning logs, merchant fraud reporting

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Mule network cashout | Proceeds from CNP fraud and identity theft routed through mule accounts for withdrawal as cash or conversion to cryptocurrency | Rapid fund movement through newly opened accounts; deposits followed by immediate ATM withdrawals or crypto exchange transfers |
| Cryptocurrency cashout | Direct conversion of fraud proceeds to cryptocurrency, particularly USDT (Tether), which is also the ecosystem's internal currency for PhaaS subscriptions | USDT transfers to wallets associated with known PhaaS operators; crypto exchange deposits correlated with CNP fraud timing |
| Card data resale on underground markets | Captured card data sold in bulk on dark web card shops and Telegram channels, extending the monetization window beyond direct fraud | Bulk card listings on underground markets matching demographic/geographic profiles of smishing campaign targets; card data with freshness timestamps correlating to known campaign dates |

**Data Sources**: Mule account detection systems, cryptocurrency blockchain analysis, dark web card shop monitoring, Telegram channel intelligence

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering (smishing delivery)
- FTA002: Phishing (credential harvest)
- FT007.009: Impersonation of authority (toll authority, postal service, bank)
- FT011.001: Credential theft (real-time capture via Magic Cat)
- FT016.001: Card-not-present fraud (downstream monetization)

**MITRE ATT&CK:**
- T1566.002: Phishing: Spearphishing Link — smishing link delivery via iMessage/RCS/SMS
- T1598: Phishing for Information — credential and card data harvest
- T1583.001: Acquire Infrastructure: Domains — 194,000+ malicious domains
- T1583.003: Acquire Infrastructure: Virtual Private Server — Tencent/Alibaba hosting
- T1656: Impersonation — toll authority, postal service, bank impersonation
- T1539: Steal Web Session Cookie — session data capture

**Group-IB Fraud Matrix:**
- Reconnaissance → Resource Development → Initial Access → Credential Access → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4 (Execution) when card-not-present fraud is detected, or at Phase 2 (Initial Access) through victim self-reporting of suspicious messages. FBI IC3 complaint data shows most victims report after financial loss.

**Look Left**:
- P1: Domain registration monitoring for toll/postal/government impersonation patterns on Tencent/Alibaba ASNs
- P1: Telegram OSINT monitoring for PhaaS platform advertisements and operator chatter
- P2: Carrier-level iMessage/RCS abuse detection; Apple "Screen Unknown Senders" adoption metrics
- P2: Chenlun kit fingerprinting via ResourceRedConfig.js and /ResourceConfig/urlConfig.json

**Look Right**:
- P4: CNP fraud on cards whose holders reported smishing links — correlating complaint data with transaction monitoring
- P5: Card data appearing in underground markets with freshness timestamps matching known smishing campaigns
- P5: USDT flows from PhaaS subscription wallets revealing operator networks and scale

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| PhaaS platform operator | Darcula, Lucid, Lighthouse — turnkey smishing kit with templates, hosting, and real-time credential streaming | High | $88/week to $1,588/year (Lighthouse); subscription-based |
| Independent kit developer | Chenlun (Sinkinto01 / "Matt Kikabi") — custom phishing pages fingerprinted by ResourceRedConfig.js | Medium | ~$500 USDT/month for custom sites; ~700 domains tracked |
| Bulk SMS/iMessage enabler | Oak Tel/Carrie SMS — sender ID spoofing for major FIs, $8/1,000 texts | High | $8/1,000 SMS; sender ID spoofing included |
| Mass-messaging platform | Panda Shop — 2 million smishing messages daily capacity (March 2025) | High | Subscription-based |
| Identity theft kit | StupidFISH — personal data/identity theft including ID.me targeting (July 2025) | Medium | $58 USDT/week |
| Card data buyer | Purchasers of captured card data for CNP fraud or resale | High | $5–$50 per card depending on confirmed balance and freshness |

### Tool Ecosystem
- **Magic Cat**: Darcula's core toolkit — real-time character-by-character credential streaming, GenAI form generation (v3.0), container registry at registry[.]magic-cat[.]world
- **Lucid Panel**: XinXin Group's PhaaS platform targeting 169 entities in 88 countries with ~5% success rate
- **Lighthouse Panel**: Wang Duo Yu's platform targeting 204 brands in 50 countries
- **Oak Tel/Carrie SMS**: Bulk messaging platform with sender ID spoofing for Chase, Bank of America, Wells Fargo, Citi
- **Panda Shop**: High-volume smishing delivery platform (2M messages/day)
- **StupidFISH**: Identity theft-focused kit with ID.me targeting

### Intelligence Sources
- Resecurity, "Smishing Triad" (August 2023 — initial identification)
- PRODAFT, LARVA-246/LARVA-242/LARVA-241 tracking reports
- Netcraft, Darcula phishing page takedown data (25,000+ pages)
- NRK/Mnemonic investigative reporting — Yucheng C. attribution
- FBI IC3, 2024 toll-scam complaint data (59,271 complaints)
- Google RICO lawsuit filing (November 2025)

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Domain monitoring for toll/postal/government impersonation on Tencent (AS132203) and Alibaba (AS45102) ASNs | Detective | Cyber/Threat Intel |
| P1 | Telegram OSINT monitoring for PhaaS platform advertisements and Smishing Triad operator activity | Detective | Threat Intel |
| P2 | Apple iOS "Screen Unknown Senders" deployment guidance for customers; RCS spam filtering | Preventive | Customer Security/Comms |
| P2 | Carrier-level iMessage and RCS abuse reporting partnerships | Preventive | Telecom Partnerships |
| P2 | Customer awareness campaigns on toll-scam and package-delivery smishing lures | Preventive | Customer Communications |
| P3 | Real-time OTP velocity monitoring — flag OTP redemptions from device/location inconsistent with requestor | Detective | Fraud Operations |
| P4 | Card-not-present transaction scoring incorporating smishing complaint correlation (24h lookback) | Detective | Fraud/Payments |
| P4 | Accelerated card replacement for customers who report smishing lure engagement | Preventive | Card Operations |
| P5 | Dark web card shop monitoring for bulk card listings matching smishing campaign demographics | Detective | Threat Intel |
| P5 | Cryptocurrency transaction monitoring for USDT flows to known PhaaS operator wallets | Detective | Financial Crime |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Organizational recognition of smishing PhaaS as a distinct threat vector requiring cross-channel response |
| ASSESS | Level 3 (Established) | Risk assessment incorporating iMessage/RCS bypass of traditional SMS filtering; quantified exposure from toll/postal lure campaigns |
| PLAN | Level 3 (Established) | Smishing response plan spanning telecom partnerships, customer awareness, transaction monitoring, and complaint correlation |
| ACT | Level 3 (Established) | Transaction monitoring rules correlating smishing complaints with subsequent CNP fraud; Chenlun kit fingerprint detection |
| MONITOR | Level 3 (Established) | Continuous monitoring of smishing complaint volumes, CNP fraud rates on recently reported cards, PhaaS infrastructure changes |
| REPORT | Level 2 (Developing) | IC3 complaint filing; SAR filing for organized smishing-to-CNP fraud chains; threat intelligence sharing with industry ISACs |
| IMPROVE | Level 2 (Developing) | Post-campaign analysis feeding back into lure detection, customer messaging, and card reissuance speed improvements |

---

## Detection Approaches

### Queries / Rules

```splunk
-- Splunk SPL: Toll-scam smishing pattern detection
-- Correlates inbound smishing complaints with subsequent CNP transactions on the same customer's cards
index=fraud sourcetype=smishing_complaints
| rename customer_id AS smish_customer, _time AS complaint_time
| join type=inner smish_customer
    [search index=transactions sourcetype=card_transactions
     transaction_type="CNP"
     | rename customer_id AS smish_customer, _time AS txn_time]
| where txn_time > complaint_time AND txn_time < complaint_time + 86400
| stats count AS cnp_after_smishing,
        sum(transaction_amount) AS total_fraud_amount,
        dc(merchant_id) AS distinct_merchants,
        values(merchant_name) AS merchants
  BY smish_customer, complaint_time
| where cnp_after_smishing >= 1
| sort - total_fraud_amount
```

```sql
-- SQL: Card-not-present fraud correlated with smishing complaint timestamps
-- Identifies cards used for CNP transactions within 24 hours of a smishing report
-- for the same phone number or customer
SELECT
    sc.customer_id,
    sc.phone_number,
    sc.complaint_timestamp,
    sc.lure_type,
    ct.card_number_hash,
    ct.transaction_id,
    ct.transaction_timestamp,
    ct.merchant_name,
    ct.transaction_amount,
    ct.device_fingerprint,
    ct.ip_address,
    DATEDIFF(hour, sc.complaint_timestamp, ct.transaction_timestamp) AS hours_after_complaint
FROM smishing_complaints sc
INNER JOIN card_transactions ct
    ON sc.customer_id = ct.customer_id
WHERE ct.transaction_type = 'CNP'
  AND ct.transaction_timestamp > sc.complaint_timestamp
  AND ct.transaction_timestamp <= DATEADD(hour, 24, sc.complaint_timestamp)
  AND ct.transaction_timestamp >= DATEADD(day, -30, GETDATE())
  AND ct.fraud_score >= 50
ORDER BY sc.customer_id, ct.transaction_timestamp
```

### Behavioral Analytics

- Smishing complaint-to-CNP correlation: card-not-present transactions within 24 hours of a customer filing a smishing complaint or reporting a suspicious message
- OTP velocity anomaly: OTP requested from victim's device but redeemed from a different IP/device within seconds (Magic Cat real-time relay indicator)
- Domain pattern detection: newly registered domains matching toll authority naming conventions (e.g., *-ezpass[.]*, *sunpass-pay[.]*, *fastrak-toll[.]*) hosted on Tencent or Alibaba ASNs
- Sender ID spoofing detection: SMS/RCS messages with sender IDs matching financial institutions (Chase, BofA, Wells Fargo, Citi) originating from non-institutional infrastructure
- Chenlun kit fingerprinting: HTTP requests containing ResourceRedConfig.js or /ResourceConfig/urlConfig.json paths

### Cross-Team Correlation

- **Fraud + Customer Service**: Smishing complaint volumes correlated with CNP fraud spikes on the same customer population within 24–72 hours
- **Fraud + Threat Intel**: Dark web card shop listings with freshness timestamps matching known smishing campaign dates and geographic targeting
- **Telecom + Fraud**: iMessage/RCS abuse reports correlated with phishing domain registrations on monitored ASNs
- **Fraud + Identity**: ID.me account compromise reports correlated with StupidFISH campaign indicators

---

## Operational Evidence

### EV-TP0069-2026-001: Smishing Triad Ecosystem Scale

- **Source**: Resecurity (August 2023 — initial identification); Netcraft domain tracking; FBI IC3 2024 complaint data
- **Key Findings**: The Smishing Triad is a loosely federated Chinese-speaking cybercrime ecosystem operating at industrial scale: 194,000+ malicious domains registered since January 2024, 884,000+ credit cards compromised in a seven-month period, targeting users in 121+ countries. FBI IC3 received 59,271 toll-scam complaints in 2024. Three major PhaaS platforms serve the ecosystem: Darcula (~600 cybercrime groups, 90,000+ flagged domains), Lucid (169 entities in 88 countries, ~5% success rate), and Lighthouse (204 brands in 50 countries). Supporting infrastructure includes Oak Tel ($8/1,000 SMS with sender ID spoofing), Panda Shop (2M messages/day), and Chenlun (~700 domains).
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High

### EV-TP0069-2026-002: Darcula/Magic Cat Platform Analysis

- **Source**: PRODAFT (LARVA-246 tracking); NRK/Mnemonic investigative reporting; Google RICO lawsuit (November 2025)
- **Key Findings**: Darcula's core toolkit, Magic Cat, was developed by Yucheng C. (24-year-old from Henan province, China). Magic Cat streams victim-entered data character-by-character in real time, enabling immediate OTP interception. In April 2025, darcula-suite 3.0 added GenAI-powered phishing form generation. Delivery exploits Apple iMessage (prompting victims to reply "Y" to enable link clickability) and Android RCS, bypassing traditional SMS filters. Infrastructure is hosted on Tencent (AS132203) and Alibaba (AS45102) with a container registry at registry[.]magic-cat[.]world. Netcraft has executed 25,000+ page takedowns and blocked ~31,000 IPs. Google filed a RICO lawsuit in November 2025 against Darcula operators. Apple iOS 26 (2025) introduced "Screen Unknown Senders" as a mitigation for iMessage exploitation.
- **CFPF Phase Coverage**: P1–P3
- **Confidence**: High

### EV-TP0069-2026-003: PhaaS Ecosystem Growth and Market Fragmentation

- **Source**: Barracuda Networks PhaaS threat review (January 2026); KnowBe4 "The Rise of Kratos" (February 2026); CrowdStrike Tycoon2FA post-takedown analysis (March 2026); Bluekit PhaaS TI report (CrimsonVector, March 2026)
- **Key Findings**: PhaaS ecosystem is in a period of explosive growth and fragmentation. Active PhaaS kits doubled during 2025. 90% of credential compromise attacks predicted to use modular PhaaS kits by end of 2026. Post-Tycoon2FA takedown (March 4, 2026), CrowdStrike observed activity returning to pre-disruption levels within days — at least 30 phishing incidents observed between March 4-6 alone with no meaningful TTP changes. The reputational damage created a "vacuum effect" spawning new competitors: Bluekit (25 March 2026), Kratos, Whisper 2FA, GhostFrame, EvilTokens, CoGUI. Sekoia TDR separately discovered EvilTokens (device code phishing PhaaS) on the same day as Bluekit's launch (25 March 2026), indicating parallel market fragmentation.
- **CFPF Phase Coverage**: P1 (market landscape)
- **Confidence**: High — multi-source vendor telemetry (CrowdStrike, Barracuda, KnowBe4, Sekoia)

### EV-TP0069-2026-004: Unpaid Toll Scam at Global Scale (Interisle 2025)

- **Source**: Interisle Consulting Group, "Phishing Landscape 2025" (September 2025)
- **Geography**: United States, global
- **CFPF Phase Coverage**: P1, P2
- **Confidence**: High — independent quantitative domain analysis
- **Summary**: Interisle's September 2025 analysis confirms the toll scam as the most audacious phishing campaign of the period, identifying 37,000 scam domains containing strings such as EZ-pass, EZpass, EZdrive, and SunPass. Attribution points to Chinese PhaaS group XinXin operating the LUCID platform, offering weekly subscription licenses via Telegram. Attacks are delivered via Apple iMessage and Android RCS, by design bypassing telecom SMS filtering. Key infrastructure findings:
  - 24,000 domains registered at Dominet (HK) registrar (IANA ID 3775, formerly Alibaba Singapore)
  - 18,500 domains in .XIN TLD (Elegant Leader / HiChina / Alibaba Group) — .XIN had an unprecedented phishing score of 10,810.2
  - 5,500 domains in .TOP (Jiangsu Bangning, which received an ICANN breach letter in July 2024)
  - Hosting: 12,300 on Tencent (AS132203), 2,100 on Alibaba (AS45102), 7,600 behind Cloudflare (AS13335)
  - XinXin also uses the Darcula PhaaS platform and offers subscribers weekly licenses via Telegram

  This validates and extends the existing LUCID/Darcula content documented in EV-TP0069-2026-001 and EV-TP0069-2026-002 at massive quantitative scale, confirming the toll scam as a dominant global smishing vector and providing registrar-level and TLD-level attribution for infrastructure takedown targeting.

---

## References

- "Phishing kits and AiTM platforms: a comprehensive threat intelligence reference (2026)" — primary source document
- Resecurity, "Smishing Triad: the impersonation game" (August 2023) — initial ecosystem identification, 194,000+ domains, 884,000+ cards
- Netcraft, Darcula takedown data — 90,000+ flagged domains, 25,000+ page takedowns, ~31,000 blocked IPs
- PRODAFT, LARVA-246 (Darcula), LARVA-242 (Lucid/XinXin Group), LARVA-241 (Lighthouse/Wang Duo Yu) tracking reports
- NRK/Mnemonic investigative reporting — Yucheng C. attribution, Magic Cat container registry discovery
- FBI IC3, 2024 Internet Crime Report — 59,271 toll-scam complaints
- Google, RICO lawsuit against Darcula operators (November 2025)
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) — smishing trends
- Barracuda Networks, PhaaS threat review (January 2026) — PhaaS kit doubling statistic
- KnowBe4, "The Rise of Kratos" (February 2026) — 90% credential compromise prediction
- CrowdStrike, "Tycoon2FA Phishing-as-a-Service Platform Persists After Takedown" (March 2026) — post-takedown resilience, vacuum effect analysis
- Sekoia TDR, "New widespread EvilTokens kit" (30 March 2026) — device code phishing, parallel market fragmentation
- Interisle Consulting Group, "Phishing Landscape 2025" (September 2025) — 37,000 toll-scam domains, XinXin/LUCID attribution, Dominet/HK registrar, .XIN TLD abuse, hosting infrastructure breakdown

---

## Analyst Notes

The Smishing Triad ecosystem represents a fundamentally different threat from email-based phishing (TP-0067). Email phishing operates in an environment with decades of filtering maturity — SPF, DKIM, DMARC, URL reputation, sandbox detonation. Mobile messaging channels (iMessage, RCS) lack equivalent filtering infrastructure. The exploitation of iMessage's link-disabling protection for unknown senders — where victims are socially engineered to reply "Y" to re-enable links — demonstrates how platform-level security features can be subverted through simple social engineering. Apple's iOS 26 "Screen Unknown Senders" is a direct response, but adoption will take years to reach critical mass.

The real-time credential streaming capability of Magic Cat is a qualitative shift from traditional phishing. In a standard phishing attack, credentials are captured on form submission and stored for later retrieval. Magic Cat streams each character as it is typed, enabling operators to intercept OTPs within their validity window (typically 30–60 seconds). This makes time-based OTP defenses ineffective against this specific toolkit. Organizations should monitor for OTP redemption from devices/locations that do not match the requesting device as the primary detection signal.

The ecosystem's pricing structure reveals its accessibility: $88/week for Lighthouse, $8/1,000 SMS via Oak Tel, $58 USDT/week for StupidFISH, $500 USDT/month for custom Chenlun sites. These are not sophisticated, high-barrier operations — they are consumer-grade cybercrime services. The ~5% success rate achieved by Lucid (versus typical <2% for traditional phishing) combined with Panda Shop's 2 million messages/day capacity means even modest campaigns generate thousands of compromised cards daily. Defensive strategy must account for volume: individual lure detection will always lag behind template generation, particularly with GenAI-powered form creation in darcula-suite 3.0. The highest-confidence detection approach is correlating smishing complaints with subsequent CNP fraud on the same customer's cards within a 24–72 hour window.

**PhaaS Market Fragmentation and the Vacuum Effect (March 2026)**: The broader PhaaS ecosystem — encompassing both email-based AiTM platforms (TP-0067) and SMS/iMessage-based platforms like Darcula — is experiencing explosive growth despite headline enforcement successes. Active PhaaS kits doubled during 2025 (Barracuda). By end of 2026, an estimated 90% of credential compromise attacks will be enabled by modular PhaaS kits (KnowBe4). The March 4, 2026 Tycoon2FA takedown illustrates the "vacuum effect": despite seizing 330 domains, CrowdStrike's Falcon Complete team observed activity returning to pre-disruption levels within days. More significantly, the takedown's reputational damage to Tycoon2FA among criminal customers who value operational stability created a market opening that new entrants rapidly filled. Bluekit (TP-0067) emerged 21 days post-takedown as a fully managed AiTM PhaaS platform with 40+ templates. Additional new entrants include Kratos, Whisper 2FA, GhostFrame, EvilTokens (device code phishing), Sneaky 2FA, CoGUI, and SessionShark — indicating the market is fragmenting and specializing rather than consolidating. This fragmentation pattern has direct implications for smishing PhaaS: the Chinese-speaking Darcula/Lucid/Lighthouse ecosystem coexists with a parallel Russian-speaking AiTM ecosystem, each serving different fraud use cases through overlapping infrastructure (bulletproof hosting, cryptocurrency payment, domain registration). Disruption of any single platform merely redistributes customers across the remaining ecosystem within days.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-23 | FLAME Project | Initial submission — sourced from phishing kits and AiTM platforms threat intelligence reference (2026) |
| 2026-03-30 | FLAME Project | Enrichment: PhaaS market fragmentation analysis, vacuum effect pattern, post-Tycoon2FA market dynamics (EV-TP0069-2026-003) — sourced from Barracuda, KnowBe4, CrowdStrike, Bluekit TI report |
| 2026-04-01 | FLAME Project | Enrichment: Interisle 2025 toll-scam quantitative analysis — 37K domains, XinXin/LUCID attribution, Dominet registrar, .XIN TLD abuse (EV-TP0069-2026-004) |
