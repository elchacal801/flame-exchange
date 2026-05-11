# TP-0060: Investment Fraud TDS Pipeline

```yaml
---
id: TP-0060
title: "Investment Fraud TDS Pipeline"
category: ThreatPath
date: 2026-03-20
author: "FLAME Project"
source: "Recorded Future CTA-2026-0319, Infoblox Keitaro/Binom Analysis 2025, INTERPOL GFFTA 2026"
tlp: WHITE
infrastructure_generation_method: tds-routing
fraud_types:
  - traffic-distribution-system
  - investment-fraud
  - cloaking
  - geo-routing
  - rdga-infrastructure
sector:
  - banking
  - investment
  - crypto
  - insurance
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "fraud-infrastructure"
primary_phase: "P1"
short_name: "Investment TDS"
confidence_score: 70
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1583.001  # Acquire Infrastructure: Domains
  - T1583.003  # Acquire Infrastructure: Virtual Private Server
  - T1102       # Web Service
  - T1036       # Masquerading
  - T1568.002  # Dynamic Resolution: Domain Generation Algorithms
ft3_tactics: ["FTA001", "FTA009", "FT016"]
mitre_f3: []
groupib_stages:
  - "Resource Development"
  - "Initial Access"
  - "Traffic Distribution"
  - "End-user Interaction"
  - "Perform Fraud"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
related_tps:
  - id: TP-0041
    relationship: shares-infrastructure
  - id: TP-0042
    relationship: variant-of
  - id: TP-0017
    relationship: enhances
  - id: TP-0034
    relationship: enhances
regulatory_refs:
  - REG-RF-CTA-2026-0319
  - REG-INTERPOL-GFFTA
baseline_ids:
  - BL-0030
geopolitical_timing: none
nation_state_nexus: none
tags:
  - tds
  - keitaro
  - binom
  - investment-scam
  - cloaking
  - geo-routing
  - rdga
  - reckless-rabbit
  - ruthless-rabbit
  - savvy-seahorse
  - domain-age-evasion
  - referral-chain
---
```

## Summary

Traffic Distribution Systems (TDS) weaponized specifically for investment fraud delivery — routing potential victims from legitimate advertising platforms through multi-hop cloaking chains to fraudulent investment platforms. Recorded Future documents TDS infrastructure as a critical fraud-enabling service exploited by investment scam operators. Infoblox identifies specific RDGA actors (Reckless Rabbit, Ruthless Rabbit, Savvy Seahorse) operating TDS infrastructure that routes victims based on geolocation, device fingerprint, and behavioral profile. Commercial TDS platforms (Keitaro, Binom) are abused for traffic cloaking and geo-routing, showing compliant content to security researchers while routing real victims to scam investment platforms.

**Distinction from TP-0042**: TP-0042 covers TDS chain exploitation broadly across fraud types; TP-0060 covers the specific investment fraud TDS pipeline — from advertising click to fake investment platform — with emphasis on the investment-specific cloaking, victim qualification, and platform routing techniques.

## Threat Path Hypothesis

> **Hypothesis**: Investment fraud operators have adopted sophisticated TDS pipelines as their primary victim acquisition and filtering infrastructure. These pipelines abuse commercial TDS platforms (Keitaro, Binom) combined with RDGA-generated domain infrastructure to create multi-hop routing chains that qualify victims by geography, wealth indicators, and behavioral profile before routing them to tailored fake investment platforms. The TDS layer serves dual purposes: maximizing conversion rates by matching victims to appropriate scam variants, and evading detection by cloaking — presenting legitimate content to security scanners, researchers, and non-target geographies while only exposing fraud content to qualified victims.

**Confidence**: Medium — Recorded Future and Infoblox provide technical analysis of TDS infrastructure, but the direct attribution chain from advertising click to investment fraud monetization is often obscured by the multi-hop routing design.

**Estimated Impact**: Investment fraud losses globally exceed $4.6B annually (FBI IC3). TDS infrastructure is estimated to support 60-80% of online investment scam campaigns, making it a critical single point of leverage for disruption.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| TDS platform procurement | Operators procure commercial TDS licenses (Keitaro, Binom) or build custom TDS infrastructure; configure geo-routing rules, cloaking logic, and victim qualification criteria | Keitaro/Binom license activations from suspicious accounts; custom TDS infrastructure deployment on bulletproof hosting |
| RDGA domain generation | RDGA actors (Reckless Rabbit, Ruthless Rabbit, Savvy Seahorse) generate thousands of domains for TDS infrastructure using registered domain generation algorithms | Bulk domain registrations with algorithmic naming patterns; DNS TTL < 300s; domains registered via privacy-protected registrars |
| Fake investment platform development | Operators create convincing replicas of legitimate investment/trading platforms; integrate with TDS backend for victim tracking | Recently registered domains with investment/trading keywords; cloned UI from legitimate platforms; platform backend hosted on bulletproof infrastructure |
| Advertising account setup | Operators create advertising accounts on Google, Meta, TikTok to drive traffic into TDS pipeline; use cloaked landing pages to pass ad platform review | New advertising accounts with investment-related campaigns; landing pages that change content based on visitor profile |

**Data Sources**: Domain registration monitoring, TDS platform abuse reports, advertising platform fraud intelligence, RDGA detection feeds

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Cloaked advertising | Investment advertisements on legitimate platforms (search, social media, display) route through TDS infrastructure; ad review sees compliant content while real visitors see investment scam | Ads with referral chains > 3 hops; landing page content inconsistent between direct access and ad-referred access; geo-variable content |
| SEO poisoning | TDS-backed pages optimized for investment-related search terms; organic search results route victims through TDS pipeline | Search results for investment terms leading to recently registered domains; SEO content matching investment scam templates |
| Social media amplification | Investment testimonials and success stories posted across social media platforms with TDS-tracked links; influencer impersonation for credibility | Short URLs with TDS tracking parameters; social media posts with investment returns claims linking to TDS-routed destinations |

**Target**: Retail investors, crypto enthusiasts, retirees seeking income, individuals searching for investment opportunities online

**Data Sources**: Advertising platform analytics, search engine intelligence, social media monitoring, URL analysis

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Victim qualification via TDS | TDS evaluates incoming traffic and routes based on: geolocation (target high-wealth countries), device (desktop preferred for investment platforms), time-of-day (business hours), and referral source quality | TDS routing decisions visible in redirect chain analysis; different destinations for same initial URL based on visitor profile; non-target visitors redirected to benign content |
| Geographic routing to localized scam | TDS routes victims to investment platforms localized for their region — appropriate language, local payment methods, jurisdiction-specific regulatory claims | Same advertising campaign serving different investment platform variants by geography; platform language matching visitor geolocation |
| Multi-hop cloaking chain | Traffic passes through 3-7 intermediate domains between ad click and final investment platform; each hop performs filtering and validation | Redirect chains with > 3 intermediate domains; domains with low TTL DNS records; chain includes known TDS platform domains |
| Legitimate platform mimicry | Final investment platform mimics legitimate broker/exchange UI, includes fake regulatory registration numbers, fabricated testimonials, and simulated trading interface | Platform design matching known legitimate broker templates; regulatory registration numbers that don't validate; testimonials using stock photos or GAN-generated faces |

**Data Sources**: URL redirect chain analysis, DNS monitoring, domain registration intelligence, web content analysis

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Victim registration and deposit | Victim registers on fake investment platform; makes initial deposit (typically $250-$500 minimum); platform displays fabricated returns to encourage larger deposits | Deposits to recently registered investment platforms; platform shows unrealistic consistent returns; escalating deposit requests |
| Fabricated profit display | Investment platform displays fabricated trading activity and profits; victim sees account balance growing, encouraging further deposits | Platform trading data not matching any real market data; consistent positive returns regardless of market conditions; withdrawal restrictions when victim attempts to cash out |
| Escalating deposit extraction | Compound operators or automated systems apply pressure for larger deposits — "limited time opportunities," "margin calls," "tax payments required before withdrawal" | Sequential deposits of increasing amounts; deposits following specific request patterns; victim accessing crypto exchange for first time to fund investment platform |

**Data Sources**: Transaction monitoring, crypto exchange intelligence, victim complaint analysis, platform takedown intelligence

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Payment processor exploitation | Victim deposits processed through payment processors with weak merchant vetting; funds routed to operator accounts before chargebacks | Payment processor complaints from investment platform victims; merchant accounts with high chargeback ratios; processor-level blocking of known scam merchants |
| Crypto deposit laundering | Victims directed to deposit crypto directly to platform wallet; funds immediately moved through mixing/tumbling infrastructure | Crypto deposits to wallets with no legitimate exchange history; immediate fund movement post-deposit; chain-hopping patterns |
| TDS infrastructure resale | TDS operators monetize infrastructure by selling traffic routing services to multiple investment scam campaigns; revenue from both TDS-as-a-service and affiliate commissions | Multiple distinct investment platforms using same TDS infrastructure; TDS platform with multiple campaign configurations |

**Data Sources**: Payment processor analytics, crypto blockchain analysis, TDS infrastructure correlation, affiliate network intelligence

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001: Social Engineering — Investment opportunity persuasion through fabricated returns
- FTA009: Phishing — Cloaked advertising driving victims to fraudulent investment platforms
- FT016: Brand Impersonation — Fake investment platforms mimicking legitimate brokers

**MITRE ATT&CK:**

- T1583.001: Acquire Infrastructure: Domains — RDGA domain generation for TDS infrastructure
- T1583.003: Acquire Infrastructure: Virtual Private Server — TDS and fake platform hosting
- T1102: Web Service — Abuse of commercial TDS platforms (Keitaro, Binom) as web services
- T1036: Masquerading — Cloaking to present legitimate content to security scanners
- T1568.002: Dynamic Resolution: Domain Generation Algorithms — RDGA for TDS domain infrastructure

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P3/P4** — typically discovered when a victim reports inability to withdraw from an investment platform, ad platform detection identifies cloaked investment ads, or security researchers trace TDS redirect chains.

**Look Left** (what did you miss before discovery?):

- RDGA domain registration patterns — algorithmic bulk registrations detectable weeks before campaign activation
- TDS platform abuse — Keitaro/Binom configurations for investment scam routing detectable via platform monitoring
- Advertising account creation — new accounts immediately running investment campaigns with cloaked landing pages
- Fake platform infrastructure setup — recently registered domains with investment platform templates

**Look Right** (what comes next after discovery?):

- Same TDS infrastructure routes traffic to multiple investment scam variants — one detection enables discovery of parallel campaigns
- RDGA domain infrastructure connects to broader actor ecosystem — Reckless Rabbit, Ruthless Rabbit, Savvy Seahorse infrastructure overlaps
- Victim deposits trace to compound-operated laundering infrastructure — transaction analysis connects TDS pipeline to TP-0058 and TP-0049
- TDS operator may be selling services to multiple fraud campaigns — infrastructure takedown disrupts clients beyond investment fraud

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | RDGA domain detection: monitor DNS for algorithmic domain registration patterns and low-TTL bulk registrations | Detective | Cyber |
| P1 | TDS platform abuse monitoring: coordinate with Keitaro/Binom for abuse reporting; monitor for investment scam configurations | Detective | Cyber |
| P2 | Advertising platform coordination: share investment scam TDS indicators with Google, Meta, TikTok ad fraud teams | Preventive | Fraud |
| P3 | URL redirect chain analysis: deploy tools to follow full redirect chains from ad clicks; flag chains with > 3 hops and recently registered domains | Detective | Cyber |
| P3 | Geo-routing detection: test suspicious URLs from multiple geographies to identify cloaking behavior; compare content served to different regions | Detective | Cyber |
| P4 | Customer advisory: publish investment platform verification guidance; maintain registry of known fake investment platforms | Preventive | Fraud |
| P4 | Transaction monitoring: flag customer deposits to recently registered investment platforms, especially first-time crypto purchases | Detective | Fraud |
| P5 | Payment processor intelligence sharing: coordinate with processors to identify and block known scam investment merchants | Responsive | AML |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Investment TDS fraud recognized as distinct threat; investment in URL chain analysis and RDGA detection |
| ASSESS | Level 3 (Established) | Risk assessment includes TDS-mediated investment fraud across customer segments |
| PLAN | Level 3 (Established) | Playbooks for TDS chain investigation; advertising platform abuse reporting; fake platform takedown procedures |
| ACT | Level 3 (Established) | Automated RDGA detection; URL chain analysis on customer-reported links; geo-routing detection capability |
| MONITOR | Level 3 (Established) | KRIs for RDGA domain detection rates, fake investment platform identification, customer deposit-to-scam-platform rates |
| REPORT | Level 2 (Developing) | Investment fraud via TDS reported with infrastructure IOCs; shared with industry and advertising platforms |
| IMPROVE | Level 3 (Established) | TDS detection updated as cloaking techniques evolve; RDGA actor tracking maintained |

---

## Detection Approaches

### Queries / Rules

**RDGA Domain Investment Infrastructure Detection (SQL)**

```sql
SELECT d.domain, d.registration_date, d.registrar,
       dns.ttl, dns.query_count_24h,
       LENGTH(SPLIT_PART(d.domain, '.', 1)) AS label_length,
       r.redirect_depth, r.final_destination
FROM domains d
JOIN dns_records dns ON d.domain = dns.domain
LEFT JOIN redirect_chains r ON d.domain = r.intermediate_domain
WHERE d.registration_date > CURRENT_DATE - INTERVAL '30 days'
  AND dns.ttl < 300
  AND dns.query_count_24h > 100
  AND LENGTH(SPLIT_PART(d.domain, '.', 1)) > 10
  AND (r.final_destination LIKE '%invest%' OR r.final_destination LIKE '%trade%' OR r.final_destination LIKE '%broker%')
ORDER BY dns.query_count_24h DESC;
```

**Cloaked Investment Ad Redirect Detection (Splunk SPL)**

```spl
index=proxy sourcetype=web_traffic
| eval redirect_count=mvcount(redirect_chain)
| where redirect_count > 3
| eval final_domain=mvindex(redirect_chain, -1)
| lookup domain_age_feed final_domain OUTPUT domain_age_days
| where domain_age_days < 60
| search final_url="*invest*" OR final_url="*trade*" OR final_url="*broker*" OR final_url="*capital*"
| stats count dc(src_ip) AS unique_visitors values(redirect_chain) AS full_chain by final_domain
| sort -count
```

### Behavioral Analytics

- Customer clicks on advertisement and is redirected through 3+ intermediate domains before reaching investment platform — indicates TDS routing
- Same URL serves different content based on geolocation or device fingerprint — indicates cloaking
- Recently registered domain (< 60 days) serving investment platform with high traffic volume — indicates TDS-driven scam
- RDGA domain patterns in DNS: algorithmically generated names, short TTL, bulk registration timing
- Customer making first-ever crypto exchange deposit followed by transfer to unknown investment platform

### Cross-Team Correlation

- **Cyber + Fraud**: Correlate RDGA domain detection and TDS chain analysis with customer transaction monitoring; customers depositing to TDS-routed platforms are likely fraud victims
- **Fraud + External**: Share TDS infrastructure IOCs with advertising platforms for upstream blocking; coordinate fake investment platform takedowns with domain registrars and hosting providers
- **Cyber + AML**: TDS infrastructure payments (hosting, domains, TDS licenses) made via crypto — blockchain analysis may reveal operator identities and connect to broader fraud networks

---

## Operational Evidence

### EV-TP0060-2026-001: Recorded Future TDS-as-Fraud-Infrastructure Analysis

- **Source**: Recorded Future CTA-2026-0319, March 2026
- **Key Finding**: TDS infrastructure identified as critical fraud-enabling service; commercial TDS platforms (Keitaro, Binom) exploited for investment scam routing; cloaking techniques evade ad platform review and security researcher analysis; TDS operators monetize infrastructure through service fees and affiliate commissions
- **CFPF Phase Coverage**: P1 through P5
- **Confidence**: Medium-High

### EV-TP0060-2026-002: Infoblox RDGA Actor TDS Operations

- **Source**: Infoblox, Keitaro TDS and RDGA Actor Analysis, 2025
- **Key Finding**: Reckless Rabbit, Ruthless Rabbit, and Savvy Seahorse RDGA actors operate TDS infrastructure serving investment scam campaigns; thousands of algorithmically generated domains with TTL < 300s; geo-routing logic routes victims to localized investment scam variants based on IP geolocation
- **CFPF Phase Coverage**: P1, P2, P3
- **Confidence**: Medium

### EV-TP0060-2026-003: INTERPOL Investment Fraud Scale

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026
- **Key Finding**: Investment fraud identified as one of the most profitable fraud types globally; TDS-mediated delivery identified as dominant victim acquisition channel; $4.6B+ reported investment fraud losses annually (FBI IC3), estimated actual losses significantly higher due to underreporting
- **CFPF Phase Coverage**: P4, P5
- **Confidence**: High

---

## References

- Recorded Future, *CTA-2026-0319: Criminal Exploitation of Fraud-Enabling Infrastructure*, March 2026 — TDS as fraud-enabling infrastructure, commercial TDS platform abuse
- Infoblox, *Keitaro TDS and RDGA Actor Analysis*, 2025 — Reckless Rabbit, Ruthless Rabbit, Savvy Seahorse RDGA operations
- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — Investment fraud scale and TDS-mediated delivery

---

## Analyst Notes

**TDS as Single Point of Leverage**: The TDS layer is the most valuable disruption target in the investment fraud pipeline. Advertising platforms cannot easily detect cloaked ads, and fake investment platforms can be stood up cheaply. But sophisticated TDS infrastructure — with its geo-routing logic, cloaking configurations, and victim qualification algorithms — represents significant operator investment and is harder to replace quickly. Targeting TDS infrastructure disrupts the connection between victim acquisition and fraud execution across multiple campaigns simultaneously.

**Commercial TDS Platform Complicity Question**: Keitaro and Binom are legitimate commercial products with legitimate use cases (affiliate marketing, A/B testing). However, their deployment in fraud infrastructure raises questions about platform operator responsibility. Defenders should engage with these platforms' abuse teams — their cooperation in identifying and terminating malicious configurations could have outsized impact on investment fraud delivery infrastructure.

**RDGA Evolution from Malware to Fraud**: RDGA was originally a malware C2 technique. Its adoption by investment fraud operators (Reckless Rabbit et al.) for TDS infrastructure represents a significant cross-domain technique transfer. This means defenders can leverage malware-detection RDGA methodologies (developed over years in the cybersecurity domain) for fraud detection — an underexploited opportunity for knowledge transfer between security and fraud teams.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-20 | FLAME Project | Initial submission |
