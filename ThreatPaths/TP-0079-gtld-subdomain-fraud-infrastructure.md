# TP-0079: Cheap gTLD and PaaS Subdomain Abuse for Fraud Infrastructure at Scale

```yaml
---
id: TP-0079
title: "Cheap gTLD and PaaS Subdomain Abuse for Fraud Infrastructure at Scale"
category: ThreatPath
date: 2026-04-01
last_reviewed: 2026-04-02
author: "FLAME Project"
source: "Interisle Consulting Group — Phishing Landscape 2025 (September 2025)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - phishing
  - brand-impersonation
  - credential-harvesting
  - fraud-enabling-infrastructure
  - paas-subdomain-abuse
sector:
  - cross-sector
  - banking
  - crypto
  - payments
  - government
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "fraud-infrastructure"
primary_phase: "P1"
short_name: "gTLD Subdomain Abuse"
confidence_score: 90
source_reliability: A
info_credibility: 1
mitre_attack:
  - T1583.001
  - T1583.003
  - T1566.002
  - T1608.005
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT007.002", "FT005.001", "FT006", "FT028", "FT001", "FT003", "FT016.001", "FT019", "FT011.001", "FT018"]
mitre_f3: ["T1189", "T1555", "T1557", "T1598", "T1660"]
groupib_stages:
  - "Resource Development"
  - "Initial Access"
  - "Perform Fraud"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0041
    relationship: shares-infrastructure
  - id: TP-0067
    relationship: enables
  - id: TP-0069
    relationship: enables
  - id: TP-0048
    relationship: related-to
regulatory_refs:
  - REG-INTERPOL-GFFTA
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - gtld-abuse
  - bulk-registration
  - paas-subdomain
  - cloudflare-proxy
  - phishing-infrastructure
  - interisle-2025
  - idn-homograph
  - unpaid-toll-scam
  - xinxin-lucid
  - dominet-hk
  - webflow-abuse
  - vercel-abuse
  - domain-pricing
---
```

## Summary

Phishing infrastructure has undergone a structural shift toward cheap new generic top-level domains (gTLDs) and free Platform-as-a-Service (PaaS) subdomains as the dominant delivery mechanism for credential harvesting, brand impersonation, and fraud-enabling infrastructure at global scale. Interisle Consulting Group's Phishing Landscape 2025 report, covering May 2024 through April 2025, documented approximately 2 million phishing attacks worldwide across more than 1.5 million unique domains — with 77% of phishing domains identified as maliciously registered (a 36% year-over-year increase).

The defining finding is the dramatic asymmetry between new gTLD market share and phishing concentration: new gTLDs hold only 11% of the global domain market but accounted for 51% of all phishing domains during the reporting period. This represents a significant escalation from 21% in 2021, indicating that threat actors have systematically migrated to new gTLDs as their preferred registration namespace. The economic driver is clear: 18 new gTLDs offered registrations under $2, and sub-$2 pricing correlates directly with the highest phishing abuse scores.

Simultaneously, PaaS subdomain abuse has emerged as a parallel infrastructure channel. Cloudflare pages.dev saw a 157% increase in phishing attacks (43,800 attacks), Webflow's webflow.io surged 980% (33,400 attacks), Vercel's vercel.app grew 279% (21,400 attacks), and GitBook's gitbook.io appeared as a new vector with 22,000 attacks. These platforms provide free hosting with legitimate SSL certificates and trusted domain reputations, enabling phishers to bypass email security filters and browser warnings.

A specific campaign — the "Unpaid Toll Scam" — illustrates the convergence of these techniques: 37,000 domains were registered via Dominet (HK) registrar across the .XIN and .TOP TLDs, operated by the Chinese PhaaS provider XinXin/LUCID, and hosted on Tencent (AS132203), Alibaba (AS45102), and Cloudflare (AS13335) infrastructure. IDN homograph attacks further compound the threat, with 2,655 domains targeting cryptocurrency brands through internationalized domain name spoofing (e.g., xn--btpay-b4a.com rendering as bitpay.com).

Cloudflare AS13335 has been the number one hosting network for phishing attacks for four consecutive years, with 540,000 attacks during the reporting period, largely because its reverse proxy architecture obscures the true hosting location of phishing pages from investigators and automated takedown systems.

## Threat Path Hypothesis

> **Hypothesis**: The convergence of sub-$2 new gTLD registrations, permissive registrar verification policies, and free PaaS subdomain provisioning has created a fraud infrastructure supply chain that enables phishing operations at industrial scale with negligible marginal cost per attack domain. Threat actors exploit three structural weaknesses simultaneously: (1) ICANN's failure to impose meaningful anti-abuse requirements on new gTLD registries, (2) registrar financial incentives that align with bulk registration volumes regardless of intent, and (3) PaaS providers' prioritization of frictionless onboarding over abuse prevention. The result is a bifurcated infrastructure model where maliciously registered gTLD domains serve as disposable phishing endpoints (77% of phishing domains, 37% bulk-registered), while PaaS subdomains provide high-trust, difficult-to-block delivery channels that inherit the reputation of legitimate hosting platforms. Cloudflare's reverse proxy architecture further compounds detection difficulty by obscuring true hosting infrastructure from investigators and automated systems.

**Confidence**: Very High (90) — Interisle's methodology is longitudinal (reporting annually since 2020), covers the full DNS ecosystem through multiple authoritative data sources (APWG eCrime Research, DNS abuse feeds, certificate transparency logs), and produces findings consistent with independent registrar and registry reporting. The 2025 report represents the most comprehensive publicly available phishing infrastructure dataset.

**Estimated Impact**: ~2 million phishing attacks over 12 months. 1.5 million unique phishing domains. Financial losses from credential harvesting, account takeover, card-not-present fraud, and cryptocurrency wallet drain across all sectors. USPS alone was impersonated in 67,700 attacks, Facebook in 55,000, and crypto/wallet brands in 44,300.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Registrar selection based on price and lax verification | Actors survey registrar pricing across gTLDs, targeting registrars offering sub-$2 registrations with minimal identity verification or abuse response | Registrar research activity; actor communications on forums discussing "best registrars for bulk"; concentration of phishing domains at specific registrars |
| gTLD selection for cost arbitrage | Actors select TLDs with lowest registration costs and highest abuse tolerance; .TOP, .BOND, .XYZ, .SHOP, and .XIN are primary targets due to sub-$2 pricing and weak registry enforcement | Domain pricing research; TLD-specific registration volume spikes; actor tool configs listing preferred TLDs |
| PaaS platform selection for free subdomain hosting | Actors evaluate PaaS providers offering free-tier hosting with automatic SSL, trusted domain reputation, and minimal abuse detection | Account creation on multiple PaaS platforms (Cloudflare Pages, Webflow, Vercel, GitBook, GitHub Pages); test subdomain deployments with benign content before phishing deployment |
| Brand and target reconnaissance | Phishing operators identify high-value impersonation targets (USPS, banks, crypto exchanges) and collect brand assets, login page templates, and email formats | Scraping of brand login pages; collection of email templates; monitoring of brand domain patterns for convincing lookalike construction |

**Top Abused TLDs by Phishing Domain Count (May 2024 - April 2025)**

| Rank | TLD | Phishing Domains | Market Share | Phishing Score | Registration Price Range |
|------|-----|-----------------|--------------|----------------|------------------------|
| 1 | .COM | 455,000 | ~50% | N/A (baseline) | $8-12 |
| 2 | .TOP | 188,000 | <1% | 10,257 | $0.50-2.00 |
| 3 | .BOND | 80,000 | <0.5% | 69,017 | $0.50-2.00 |
| 4 | .XYZ | 74,000 | <1% | 1,155 | $1.00-2.00 |
| 5 | .SHOP | 50,000 | <1% | 2,850 | $0.50-2.00 |
| 6 | .XIN | 43,000 | <0.1% | 10,810 | $0.50-1.00 |

*Note: Phishing Score = (phishing domains / total domains in TLD) x 10,000. Higher score indicates greater concentration of phishing relative to TLD size. .BOND's score of 69,017 indicates extreme abuse concentration.*

**Data Sources**: WHOIS bulk data, registrar pricing APIs, domain registration feeds, APWG eCrime Research phishing feed, Certificate Transparency logs

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Bulk domain registration | Actors register domains in bulk sets across multiple TLDs and registrars to create disposable phishing infrastructure; 37% of all phishing domains were identified as bulk-registered (up from 27% prior year) | Burst registration patterns: 50+ domains registered by same entity within 24h; identical WHOIS privacy settings across batch; 70,541 bulk registration sets identified at 174 registrars |
| PaaS subdomain provisioning | Actors create accounts on PaaS platforms and provision subdomains mimicking target brands (e.g., pancake-swapv2.vercel.app, v3-pancakeswap.vercel.app) | Rapid subdomain creation on free-tier PaaS accounts; subdomain names containing brand strings with version numbers or typosquats; deployment of static HTML phishing pages |
| IDN homograph domain registration | Actors register internationalized domain names that visually mimic legitimate brands by substituting Latin characters with similar Unicode glyphs | Punycode domain registrations (xn-- prefix) targeting known brands; 2,655 IDN homograph domains identified targeting crypto brands; e.g., xn--btpay-b4a.com rendering as bitpay.com |
| Unpaid Toll Scam infrastructure deployment | Chinese PhaaS provider XinXin/LUCID provisions 37,000 domains via Dominet (HK) registrar on .XIN/.TOP TLDs, targeting USPS and toll authority impersonation | Mass registration through single registrar (Dominet HK); concentration on .XIN and .TOP; DNS resolution to Tencent AS132203, Alibaba AS45102, and Cloudflare AS13335 |

**Top PaaS Subdomain Providers Abused for Phishing (May 2024 - April 2025)**

| Rank | Provider | Subdomain | Attacks | YoY Change | Notes |
|------|----------|-----------|---------|------------|-------|
| 1 | Cloudflare | pages.dev | 43,800 | +157% | Free static hosting with CDN |
| 2 | Webflow | webflow.io | 33,400 | +980% | Largest YoY increase |
| 3 | Google | various | 30,700 | -88% | Significant improvement in abuse response |
| 4 | Weebly | weebly.com | 29,900 | +21% | Legacy website builder |
| 5 | GitBook | gitbook.io | 22,000 | New | First appearance in top rankings |
| 6 | Vercel | vercel.app | 21,400 | +279% | Free frontend hosting |
| 7 | GitHub | github.io | 20,200 | +76% | GitHub Pages abuse |

**Bulk Registration Statistics**

| Metric | Value |
|--------|-------|
| Phishing domains bulk-registered | 37% of total |
| Year-over-year increase | Up from 27% |
| Distinct bulk registration sets | 70,541 |
| Registrars involved | 174 |

**Data Sources**: Certificate Transparency logs, passive DNS, PaaS platform account creation monitoring, WHOIS registration feeds, Interisle bulk registration detection methodology

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Phishing kit deployment on gTLD domains | Actors deploy phishing kits (credential capture forms, brand-impersonation pages) to bulk-registered domains; kits typically cloned from legitimate brand login pages | HTML/JS phishing kit fingerprints on newly registered domains; known phishing kit hashes (16Shop, Kr3pto, EvilProxy components); brand logo/CSS asset loading from legitimate CDNs |
| Cloudflare reverse proxy cloaking | Actors route phishing domains through Cloudflare's reverse proxy to obscure true hosting IP, gain free SSL certificates, and benefit from Cloudflare's trusted reputation with email security filters | Cloudflare NS records on newly registered phishing domains; AS13335 as apparent hosting provider; 540,000 phishing attacks hosted behind Cloudflare during reporting period |
| Registrar rotation strategy | Actors distribute bulk registrations across multiple registrars to avoid single-point takedown and delay abuse response; 174 registrars involved in bulk registration sets | Sequential domain registrations across different registrars within 48h; same phishing kit deployed on domains from 3+ distinct registrars; varying WHOIS patterns across registrar boundaries |
| PaaS-hosted phishing page staging | Actors deploy phishing content as static sites on PaaS platforms, exploiting legitimate SSL, CDN distribution, and trusted domain reputation to bypass security filters | Phishing content deployed to *.pages.dev, *.webflow.io, *.vercel.app, *.gitbook.io subdomains; brand-impersonation content with credential capture forms; rapid deployment/teardown cycles |
| IDN homograph page staging | Actors deploy crypto exchange phishing pages on visually deceptive IDN domains with SSL certificates that display the punycode in the certificate but render the homograph in the browser address bar | SSL certificate issuance for xn-- prefixed domains targeting known crypto brands; phishing page content mimicking DeFi exchange interfaces (PancakeSwap, BitPay, MetaMask) |

**Top Hosting Networks for Phishing (May 2024 - April 2025)**

| Rank | Network | ASN | Attacks | Notes |
|------|---------|-----|---------|-------|
| 1 | Cloudflare | AS13335 | 540,000 | #1 for 4 consecutive years; reverse proxy obscures true hosting |
| 2 | Tencent | AS132203 | Significant | Major host for XinXin/LUCID toll scam infrastructure |
| 3 | Alibaba | AS45102 | Significant | Chinese cloud hosting for .XIN/.TOP phishing domains |

**Data Sources**: Passive DNS, Cloudflare transparency reports, ASN routing analysis, phishing kit hash databases, web crawl data from phishing domain feeds

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Credential harvesting at scale | Phishing pages capture username/password combinations, banking credentials, SSN, and card details from victims who follow phishing links; ~2M attacks in 12 months | POST request logs from phishing domains; exfiltration to actor-controlled collection servers; credential log files on compromised infrastructure; Telegram bot exfiltration channels |
| AiTM session token theft via PaaS-hosted pages | Adversary-in-the-middle (AiTM) phishing pages hosted on trusted PaaS subdomains intercept session tokens and MFA codes in real-time by proxying authentication to legitimate services | PaaS-hosted pages making real-time API calls to legitimate authentication endpoints; EvilProxy/Evilginx indicators on *.vercel.app or *.pages.dev subdomains; session cookie relay patterns |
| Card capture via brand impersonation | Fake payment pages impersonating USPS (toll payment), banks, and e-commerce sites capture card numbers, CVVs, and billing addresses | Card data exfiltration endpoints on bulk-registered gTLD domains; USPS impersonation pages requesting card details for "toll payments"; form submissions to non-brand collection endpoints |
| Crypto wallet drain via phishing | Phishing pages mimicking DeFi exchanges and wallet providers prompt users to connect wallets or enter seed phrases, enabling direct wallet drain | Wallet connection prompts on IDN homograph domains; seed phrase capture forms on PancakeSwap/MetaMask impersonation pages; smart contract approval requests draining token allowances |

**Top Phished Brands (May 2024 - April 2025)**

| Rank | Brand | Attacks | Category |
|------|-------|---------|----------|
| 1 | USPS | 67,700 | Government/Postal |
| 2 | Facebook | 55,000 | Social Media |
| 3 | Crypto/Wallet (various) | 44,300 | Cryptocurrency |
| 4 | Meta | 24,600 | Social Media |
| 5 | Telegram | 17,400 | Messaging |

**Data Sources**: Phishing URL feeds (APWG, OpenPhish, PhishTank), credential exfiltration endpoint analysis, PaaS platform abuse reports, wallet drain transaction monitoring

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Card-not-present fraud | Harvested card details used for unauthorized purchases, card-not-present transactions, and card testing across e-commerce platforms | Spike in CNP fraud attempts using cards whose holders recently visited phishing pages; velocity of card usage at online merchants within hours of phishing capture |
| Account takeover (ATO) | Stolen credentials and session tokens used to access victim accounts for financial fraud, identity theft, and further social engineering | Login from new device/IP on accounts whose credentials were submitted to known phishing domains; account profile changes (email, phone, shipping address) following phishing exposure |
| Crypto wallet drain and liquidation | Wallet drain proceeds (tokens, NFTs) liquidated through DEX swaps and cross-chain bridges to obfuscate trail | Token transfers from victim wallets to actor-controlled addresses following phishing page interaction; rapid DEX swap from drained tokens to stablecoins; bridge transfers to alternative chains |
| Credential resale on underground markets | Bulk credentials that are not immediately monetized are packaged and sold on dark web marketplaces, Telegram channels, and log shops | Credential listings on Russian Market, Genesis Market successors, and Telegram channels matching domains/brands from known phishing campaigns; credential combo lists with brand-specific formatting |
| PhaaS revenue generation | PhaaS operators (XinXin/LUCID) monetize through subscription fees charged to downstream phishing operators who use the platform's infrastructure, kits, and domain supply | Subscription payments to PhaaS platforms; monthly recurring charges from downstream operators; panel access logs showing multi-tenant phishing kit management |

**Data Sources**: Card network fraud reporting, ATO incident analysis, blockchain transaction monitoring, dark web marketplace monitoring, PhaaS platform intelligence

---

## Cross-Framework Mapping

**MITRE ATT&CK:**
- T1583.001: Acquire Infrastructure: Domains — bulk gTLD registration, IDN homograph domain acquisition
- T1583.003: Acquire Infrastructure: Virtual Private Server — PaaS subdomain provisioning as infrastructure acquisition
- T1566.002: Phishing: Spearphishing Link — phishing URLs distributed via email and SMS using registered gTLD domains and PaaS subdomains
- T1608.005: Stage Capabilities: Link Target — staging phishing content on registered domains and PaaS subdomains

**Group-IB Fraud Matrix:**
- Resource Development -> Initial Access -> Perform Fraud

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P3** — most commonly discovered when security vendors or abuse teams identify phishing content deployed on newly registered domains or PaaS subdomains through automated web crawling, Certificate Transparency monitoring, or user reports. The infrastructure itself (bulk registration, subdomain creation) is observable before phishing content goes live.

**Look Left** (what did you miss before discovery?):

- P1: Bulk domain registration patterns at specific registrars — 70,541 bulk registration sets are observable in WHOIS feed data before any phishing content is deployed
- P1: PaaS account creation patterns — burst account creation from similar IP ranges, disposable email addresses, and automated signup patterns
- P2: Certificate Transparency log monitoring — new SSL certificates for suspicious domain names or PaaS subdomains containing brand strings are visible immediately upon issuance
- P2: IDN homograph registration — punycode domain registrations targeting known brand strings are detectable at registration time

**Look Right** (what comes next after discovery?):

- P4: Credential logs have already been exfiltrated — determine which victims submitted credentials before takedown; initiate forced password resets for affected accounts
- P5: Stolen credentials are likely already in monetization pipeline — monitor for ATO attempts using known compromised credential sets; alert card networks for captured card data
- Post-discovery: Actor will rotate to fresh domains from pre-registered inventory (bulk registration provides buffer stock) — monitor for same phishing kit fingerprint on new domains
- Post-discovery: PaaS takedown of one subdomain prompts migration to alternative PaaS provider — monitor for same content fingerprint across Vercel, Cloudflare Pages, Webflow, GitBook

---

## Underground Ecosystem Context

### Service Supply Chain

| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Bulk domain registrar (complicit/negligent) | Mass gTLD registration with minimal verification | High — 174 registrars identified serving bulk registration sets | $0.50-2.00 per domain (sub-$2 gTLDs) |
| PhaaS platform operator | End-to-end phishing infrastructure: kits, domain management, hosting, credential exfiltration | High — XinXin/LUCID, LabHost (seized 2024), 16Shop, and numerous active operators | $100-500/month subscription |
| PaaS account provider | Pre-created accounts on Cloudflare Pages, Vercel, Webflow, GitHub with aged reputation | Medium — sold on Telegram channels and forums | $5-50 per account |
| Phishing kit developer | Custom credential capture pages mimicking specific brands, with AiTM capability | High — commoditized market with both open-source and commercial kits | $50-500 per kit (one-time or subscription) |
| Cloudflare configuration service | Setup of Cloudflare reverse proxy for phishing domains to obscure hosting and gain trusted SSL | Medium — offered as part of phishing infrastructure packages | Included in PhaaS subscriptions or $10-50 per domain |
| IDN homograph specialist | Registration and configuration of internationalized domain names targeting specific brands | Low-Medium — specialized skill requiring Unicode knowledge | $20-100 per domain |
| Credential monetization broker | Bulk purchase and resale of harvested credentials through log shops, Telegram channels, and dark web markets | High — Russian Market, 2easy, Telegram channels with thousands of subscribers | $1-50 per credential set (varies by brand/type) |

### PhaaS Ecosystem: XinXin/LUCID Case Study

The XinXin/LUCID operation represents a mature PhaaS ecosystem specifically targeting toll payment and postal service impersonation:

| Component | Detail |
|-----------|--------|
| PhaaS Provider | XinXin (also known as LUCID) |
| Origin | Chinese-speaking threat actor group |
| Registrar | Dominet (HK) — primary registrar for bulk domain provisioning |
| TLDs Used | .XIN, .TOP — sub-$1 registration pricing |
| Domains Registered | ~37,000 for Unpaid Toll Scam campaign alone |
| Hosting Infrastructure | Tencent (AS132203), Alibaba (AS45102), Cloudflare (AS13335) |
| Primary Targets | USPS, state toll authorities, postal services |
| Delivery Method | SMS/smishing with shortened URLs to phishing domains |
| Monetization | Card capture (toll payment pretext), credential harvesting |

### Economic Model of gTLD Phishing Infrastructure

The economic incentive structure that enables industrial-scale phishing through cheap gTLDs:

| Cost Component | Per-Domain Cost | At Scale (1,000 domains) |
|----------------|----------------|--------------------------|
| gTLD registration (.TOP/.BOND/.XIN) | $0.50-2.00 | $500-2,000 |
| Cloudflare reverse proxy | Free | Free |
| Phishing kit (commercial, amortized) | $0.10-0.50 | $100-500 |
| PaaS hosting alternative | Free | Free |
| Total infrastructure cost | $0.60-2.50 | $600-2,500 |
| Revenue per successful credential capture | $5-500+ | — |
| **Break-even**: 5-50 successful captures across 1,000 domains | — | — |

The sub-$2 domain registration price combined with free Cloudflare proxying and free PaaS hosting creates a near-zero marginal cost per phishing endpoint. At 77% malicious registration rates, the economic model is self-evidently profitable.

### Intelligence Sources

- Interisle Consulting Group, "Phishing Landscape 2025" (September 2025)
- APWG, eCrime Research phishing activity reports
- Cloudflare Radar and transparency reporting
- ICANN DAAR (Domain Abuse Activity Reporting)
- Certificate Transparency log monitoring (crt.sh)
- PhishTank, OpenPhish community phishing feeds
- Resecurity, "LUCID: The Rising Threat of PhaaS" (2025)

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor bulk domain registration feeds — flag registration sets of 20+ domains at sub-$2 gTLDs within 24h from single registrant or registrar | Detective | Domain Intelligence |
| P1 | Certificate Transparency log monitoring — alert on new certificates issued for domains containing protected brand strings on new gTLDs (.TOP, .BOND, .XIN, .XYZ, .SHOP) | Detective | Brand Protection |
| P1 | PaaS subdomain monitoring — scan for new subdomains on pages.dev, webflow.io, vercel.app, gitbook.io, github.io containing protected brand keywords | Detective | Brand Protection |
| P2 | IDN homograph detection — monitor punycode registrations (xn-- prefix) that visually resolve to protected brand names; maintain homograph equivalence tables for critical brands | Detective | Domain Intelligence |
| P2 | Registrar abuse reporting automation — automate abuse complaints to registrars when phishing is confirmed on domains they service; track registrar response times and escalate non-responsive registrars to ICANN | Corrective | Legal/Brand Protection |
| P3 | Cloudflare origin IP resolution — use historical DNS, SSL certificate fingerprinting, and HTTP header analysis to identify true hosting behind Cloudflare reverse proxy for phishing takedown | Detective | Threat Intelligence |
| P3 | Phishing kit fingerprinting — maintain hash database of known phishing kit components (HTML structure, JS exfiltration code, CSS patterns) and scan newly registered domains for matches | Detective | Threat Intelligence |
| P4 | Real-time phishing URL blocking — integrate phishing domain feeds (APWG, OpenPhish, internal detection) into email gateway, web proxy, and DNS resolver block lists with <15 minute update cadence | Preventive | Security Operations |
| P4 | Browser-level protection — ensure organizational browsers have Safe Browsing / SmartScreen enabled; push custom block lists for known phishing TLD patterns via enterprise browser policy | Preventive | Endpoint Security |
| P4 | Customer-facing phishing awareness — deploy real-time phishing warnings on login pages when active impersonation campaigns are detected; SMS/email alerts to customers about known phishing campaigns (e.g., USPS toll scam) | Preventive | Customer Security |
| P5 | Credential compromise monitoring — monitor dark web marketplaces and Telegram channels for credential listings matching organizational domains; trigger forced password resets for confirmed compromises | Detective | Threat Intelligence |
| P5 | Card network alerting — when phishing campaign captures card data, notify card networks (Visa/Mastercard) with affected BIN ranges and compromise timeframe for proactive card reissuance | Corrective | Fraud Operations |

### Structural Mitigations (Industry/Policy Level)

| Mitigation | Description | Responsible Party |
|------------|-------------|-------------------|
| gTLD pricing floor | Advocate for ICANN policy requiring minimum registration pricing above cost to eliminate sub-$1 throwaway registrations | ICANN / Registries |
| Registrar accountability | Support ICANN enforcement actions against registrars with consistently high abuse rates; Interisle data provides per-registrar abuse metrics | ICANN / Industry coalitions |
| PaaS abuse detection requirements | Engage PaaS providers (Cloudflare, Vercel, Webflow) to implement mandatory content scanning on free-tier subdomain deployments | PaaS Providers |
| Restricted registration policies | EU ccTLD model (strict identity verification at registration) demonstrated lowest malicious registration scores — advocate for adoption of similar policies for new gTLDs | ICANN / Registries |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Organizational recognition that phishing infrastructure (domain and subdomain provisioning) is a distinct threat vector requiring dedicated monitoring; budget allocation for domain intelligence feeds |
| ASSESS | Level 3 (Established) | Risk assessment covers gTLD bulk registration and PaaS subdomain abuse as distinct infrastructure threats; brand-specific homograph risk assessment for critical brands |
| PLAN | Level 2 (Developing) | Playbooks for phishing domain takedown across registrars and PaaS providers; brand protection monitoring scope defined for priority gTLDs and PaaS platforms |
| ACT | Level 3 (Established) | Automated Certificate Transparency monitoring; bulk registration feed analysis; PaaS subdomain scanning for brand impersonation; phishing URL feed integration into security controls with <15 min update cadence |
| MONITOR | Level 3 (Established) | KRIs for phishing domain volume by TLD, PaaS subdomain abuse volume by provider, bulk registration set detection rate, takedown time-to-resolution, and credential compromise detection rate |
| REPORT | Level 2 (Developing) | Phishing infrastructure reporting to APWG, registrar abuse channels, and PaaS provider trust & safety teams; trend reporting on TLD-specific and PaaS-specific abuse metrics |
| IMPROVE | Level 2 (Developing) | Quarterly review of phishing infrastructure trends; registrar and PaaS provider responsiveness scoring; phishing kit fingerprint database refresh; homograph equivalence table updates for new brand assets |

---

## Detection Approaches

### Queries / Rules

**Bulk gTLD Registration Detection (SQL)**

```sql
-- Detect bulk domain registration sets targeting high-abuse gTLDs
SELECT
  registrar_name,
  registrant_hash,
  tld,
  COUNT(DISTINCT domain_name) AS domain_count,
  MIN(registration_date) AS first_registration,
  MAX(registration_date) AS last_registration,
  DATEDIFF(hour, MIN(registration_date), MAX(registration_date)) AS registration_window_hours
FROM domain_registration_feed
WHERE tld IN ('.top', '.bond', '.xyz', '.shop', '.xin', '.loan', '.icu', '.buzz')
  AND registration_date >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY registrar_name, registrant_hash, tld
HAVING COUNT(DISTINCT domain_name) >= 20
  AND DATEDIFF(hour, MIN(registration_date), MAX(registration_date)) <= 48
ORDER BY domain_count DESC;
```

**PaaS Subdomain Brand Impersonation Detection (SQL)**

```sql
-- Detect PaaS subdomains containing protected brand keywords
SELECT
  subdomain_fqdn,
  paas_provider,
  creation_timestamp,
  ssl_cert_issued_date,
  content_hash,
  CASE
    WHEN subdomain_fqdn LIKE '%pancakeswap%' THEN 'crypto-exchange'
    WHEN subdomain_fqdn LIKE '%metamask%' THEN 'crypto-wallet'
    WHEN subdomain_fqdn LIKE '%usps%' OR subdomain_fqdn LIKE '%toll%' THEN 'government-postal'
    WHEN subdomain_fqdn LIKE '%paypal%' OR subdomain_fqdn LIKE '%chase%' THEN 'financial'
    ELSE 'other'
  END AS impersonation_category
FROM paas_subdomain_monitor
WHERE paas_provider IN ('pages.dev', 'webflow.io', 'vercel.app', 'gitbook.io', 'github.io')
  AND creation_timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
  AND (
    subdomain_fqdn REGEXP '(paypal|chase|wells.?fargo|bank.?of.?america|usps|fedex|ups|pancakeswap|uniswap|metamask|coinbase|binance|facebook|instagram|telegram|microsoft|apple)'
  )
ORDER BY creation_timestamp DESC;
```

**IDN Homograph Registration Detection (SQL)**

```sql
-- Detect punycode domain registrations targeting monitored brands
SELECT
  domain_name,
  punycode_representation,
  unicode_rendering,
  registrar_name,
  registration_date,
  nameserver_provider,
  similarity_score
FROM idn_registration_monitor
WHERE punycode_representation LIKE 'xn--%'
  AND registration_date >= CURRENT_TIMESTAMP - INTERVAL '30 days'
  AND (
    unicode_rendering ILIKE '%bitpay%'
    OR unicode_rendering ILIKE '%coinbase%'
    OR unicode_rendering ILIKE '%metamask%'
    OR unicode_rendering ILIKE '%pancakeswap%'
    OR unicode_rendering ILIKE '%uniswap%'
    OR similarity_score >= 0.85  -- fuzzy match against protected brand list
  )
ORDER BY similarity_score DESC, registration_date DESC;
```

**Certificate Transparency Monitoring for New gTLD Phishing (CQL — CrowdStrike NGSIEM)**

```sql
-- CQL: Alert on new certificates for suspicious gTLD domains
event_simpleName=CertificateIssuance
| search tld IN ("top", "bond", "xyz", "shop", "xin", "loan", "icu", "buzz")
| where domain_age_hours < 48
| stats count AS cert_count, values(domain) AS domains, dc(domain) AS unique_domains BY issuer, registrar
| where unique_domains >= 10
| sort -unique_domains
```

### YARA-Like Phishing Kit Fingerprinting

```
rule phishing_kit_credential_capture {
    meta:
        description = "Generic phishing kit credential exfiltration pattern"
        threat_path = "TP-0079"
    strings:
        $form_action = /action\s*=\s*["'][^"']*\/(post|submit|login|verify|update|confirm)/i
        $hidden_field = /<input[^>]*type\s*=\s*["']hidden["'][^>]*name\s*=\s*["'](token|csrf|session)/i
        $exfil_telegram = /api\.telegram\.org\/bot[0-9]+:[A-Za-z0-9_-]+\/sendMessage/
        $exfil_endpoint = /fetch\s*\(\s*["']https?:\/\/[^"']+\/(save|collect|log|grab|send)/i
        $brand_asset = /<img[^>]*src\s*=\s*["']https?:\/\/(www\.)?(usps|paypal|chase|facebook|instagram)\.com/i
    condition:
        ($form_action and $hidden_field) and ($exfil_telegram or $exfil_endpoint) and $brand_asset
}
```

---

## Case Studies & References

### Case Study 1: Unpaid Toll Scam — XinXin/LUCID PhaaS Campaign

The Unpaid Toll Scam represents one of the largest documented PhaaS-driven phishing campaigns, orchestrated by the Chinese-speaking threat actor group XinXin (also operating under the LUCID brand):

- **Scale**: 37,000 domains registered specifically for this campaign
- **Registrar**: Dominet (HK) — a Hong Kong-based registrar that served as the primary registration channel
- **TLDs**: .XIN and .TOP selected for sub-$1 registration pricing
- **Hosting**: Distributed across Tencent (AS132203), Alibaba (AS45102), and Cloudflare (AS13335)
- **Target**: USPS and state toll authorities — victims received SMS messages claiming unpaid tolls with links to credential/card capture pages
- **Delivery**: SMS/smishing, exploiting the perceived urgency of toll/postal payment notifications
- **Impact**: Contributed significantly to USPS's position as the #1 phished brand globally (67,700 attacks)

The campaign demonstrated the industrialization of phishing: a single PhaaS operator provisioning tens of thousands of domains through a complicit registrar, hosting on multiple cloud providers for resilience, and distributing phishing infrastructure to downstream operators through a subscription model.

### Case Study 2: Vercel Crypto Exchange Phishing — PancakeSwap Impersonation

Phishers systematically abused Vercel's free hosting to create cryptocurrency exchange phishing pages:

- **Subdomains observed**: pancake-swapv2.vercel.app, v3-pancakeswap.vercel.app, and variations
- **Target**: PancakeSwap DEX users — prompted to connect wallets, approve token allowances, or enter seed phrases
- **Technique**: Static phishing pages deployed to Vercel free tier with automatic SSL and vercel.app domain trust reputation
- **Detection challenge**: vercel.app is a widely-trusted domain, and blocking at the domain level would disrupt legitimate services; takedown requires platform-level abuse reporting
- **Volume**: Vercel saw a 279% increase in phishing attacks (21,400 total) during the reporting period

### Case Study 3: IDN Homograph Attacks on Cryptocurrency Brands

2,655 internationalized domain names were identified targeting cryptocurrency brands through visual deception:

- **Example**: xn--btpay-b4a.com renders in browsers as bitpay.com (using Lithuanian i with ogonek: bitpay -> bįtpay)
- **Scale**: 2,655 domains across multiple crypto brands (BitPay, Coinbase, MetaMask, and others)
- **Technique**: Unicode characters from non-Latin scripts that are visually identical or near-identical to ASCII characters
- **SSL certificates**: Legitimate CAs issue certificates for punycode domains without brand verification, providing SSL padlock to phishing pages
- **Mitigation gap**: While modern browsers display punycode for mixed-script domains, single-script homoglyphs (e.g., Cyrillic "а" vs Latin "a") may still render deceptively in some contexts

### Key References

1. Interisle Consulting Group. "Phishing Landscape 2025." September 2025. — Primary source for all quantitative findings in this threat path.
2. APWG. "Phishing Activity Trends Report." Quarterly. — Corroborating phishing volume and brand impersonation data.
3. Resecurity. "LUCID: The Rising Threat of Phishing-as-a-Service." 2025. — XinXin/LUCID PhaaS operator analysis.
4. ICANN. "Domain Abuse Activity Reporting (DAAR)." Monthly. — Registry-level abuse metrics.
5. Google. "CyberCrime Analytics: Phishing Indicators via Certificate Transparency." 2024. — CT log monitoring methodology.
6. Cloudflare. "Cloudflare Radar." Ongoing. — Network-level phishing hosting data.
7. FIRST. "Registrar Abuse Contact Database." — Registrar abuse response tracking.

---

## References

- Interisle Consulting Group. "Phishing Landscape 2025." September 2025.
- ICANN. "Domain Abuse Activity Reporting (DAAR)." Monthly.
- Google. "CyberCrime Analytics: Phishing Indicators via Certificate Transparency." 2024.
- Cloudflare. "Cloudflare Radar." Ongoing.
- FIRST. "Registrar Abuse Contact Database."
- Barracuda Networks. "PhaaS Attacks Spiked in Q1 2025." 2025.

---

## Analyst Notes

**Why This Threat Path Matters for Financial Institutions**: The phishing infrastructure documented here is the upstream supply chain for credential harvesting that directly enables account takeover, card-not-present fraud, and authorized push payment fraud. Every stolen banking credential, every captured card number, and every compromised MFA token originates from infrastructure provisioned through the mechanisms described in this threat path. Monitoring the infrastructure layer (domain registrations, PaaS subdomain creation, Cloudflare proxy configuration) provides earlier detection than monitoring the credential abuse layer.

**Structural Problem — ICANN's Role**: The 51% concentration of phishing domains in new gTLDs that hold only 11% market share is not a technical problem — it is a governance and economic incentive problem. ICANN's registry agreements for new gTLDs do not impose meaningful anti-abuse requirements, and the financial incentives of registries and registrars align with maximizing registration volume regardless of registrant intent. The Interisle data clearly demonstrates that EU ccTLDs with strict registration requirements (identity verification, residency requirements) had the lowest malicious registration scores. This suggests that policy intervention at the registry/registrar level is more effective than downstream technical controls.

**PaaS Provider Responsibility Gap**: PaaS providers benefit from network effects — more users (including malicious ones) mean more revenue and platform growth. The 980% increase in Webflow abuse and 279% increase in Vercel abuse indicate that these platforms have not implemented proportionate abuse prevention measures as they scaled. Google's 88% decrease demonstrates that aggressive abuse response is possible and effective. The contrast between Google's improvement and other providers' deterioration should inform engagement strategies with PaaS trust & safety teams.

**Cloudflare's Dual Role**: Cloudflare AS13335 has been the #1 hosting network for phishing for four consecutive years (540,000 attacks in the reporting period). Its reverse proxy architecture provides genuine security benefits for legitimate websites, but the same architecture obscures the true hosting location of phishing pages from investigators. This creates a persistent tension between Cloudflare's legitimate CDN/security business and its role as the primary network enabling phishing infrastructure persistence. Investigators should use SSL certificate fingerprinting, HTTP header analysis, and historical DNS data to identify origin servers behind Cloudflare proxy.

**Connection to Related Threat Paths**: This threat path provides the infrastructure layer that enables multiple downstream fraud types documented in FLAME:
- **TP-0041** (shares-infrastructure): Phishing domains registered through the mechanisms described here are used to deliver malware and credential harvesting pages for banking trojan campaigns.
- **TP-0067** (enables): Cheap gTLD infrastructure enables the phishing-as-a-service ecosystem that provisions phishing campaigns for downstream operators.
- **TP-0069** (enables): PaaS subdomain abuse directly enables brand impersonation campaigns at scale by providing trusted hosting with legitimate SSL.
- **TP-0048** (related-to): Credential harvesting from phishing infrastructure feeds into account takeover and payment fraud monetization chains.

**Monitoring Priority**: Organizations should prioritize Certificate Transparency log monitoring (free, near-real-time) and bulk registration feed analysis as the highest-ROI detection investments for this threat path. Both provide pre-attack visibility — detecting infrastructure provisioning before phishing content is deployed — and can be implemented with existing SIEM infrastructure and open-source tools (certstream, WHOIS feed parsers).
