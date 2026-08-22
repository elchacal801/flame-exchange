# FLAME Intelligence Report Roadmap

**Date:** March 5, 2026
**Source:** CrimsonVector Strategic Intelligence Report — Fraud Infrastructure Threat Landscape and SIGIL/FLAME Product Implications (March 5, 2026)
**Scope:** Phases 7, 8, 9 of FLAME development + supporting work items
**Current FLAME version:** v0.8.0 (40 threat paths, 91 detection rules, 20 baselines, 5 emulation playbooks, 71 fraud types, 18 sectors)

---

## Context and Motivation

CrimsonVector's Strategic Intelligence Report synthesizes primary-source intelligence from Infoblox, Chainalysis, the FBI IC3, the WEF, Recorded Future, OFAC designations, and academic literature to map the 2025-2026 fraud infrastructure threat landscape. The central finding is that graph-based infrastructure intelligence operating at the DNS layer is the single most defensible detection paradigm against the industrialized, AI-accelerated fraud ecosystem now emerging.

The report identifies three categories of threat that FLAME does not yet cover:

1. **Infrastructure generation techniques** (RDGAs, TDS chains, AI-accelerated domain infrastructure) that represent the upstream supply chain enabling downstream fraud campaigns FLAME already documents.
2. **Geopolitical and state-actor convergence** (DPRK-criminal partnerships, sanctions evasion infrastructure, geopolitically timed campaigns) that crosses the traditional boundary between APT and criminal taxonomies.
3. **Emerging threat vectors** (human trafficking-linked fraud infrastructure, bulletproof hosting migration, cryptocurrency laundering infrastructure) that represent the next wave of systemic threats to financial services.

This roadmap translates these findings into actionable FLAME work items organized across three phases, with taxonomy updates, detection rules, baselines, emulation playbooks, and supporting tooling changes.

---

## Summary Table

| ID | Type | Title | Phase | Priority | Effort Est. |
|----|------|-------|-------|----------|-------------|
| **TAX-01** | Taxonomy | Add `infrastructure_generation_method` frontmatter field | 7 | Critical | S |
| **TAX-02** | Taxonomy | Add fraud types: `rdga-infrastructure`, `tds-exploitation`, `ai-accelerated-fraud-infrastructure` | 7 | Critical | S |
| **TP-0041** | Threat Path | RDGA-Based Infrastructure Campaigns | 7 | Critical | L |
| **TP-0042** | Threat Path | Traffic Distribution System (TDS) Chain Exploitation | 7 | Critical | L |
| **TP-0043** | Threat Path | AI-Accelerated Fraud Infrastructure Generation | 7 | Critical | L |
| **DL-0092** | Detection | RDGA Registration Timing Pattern | 7 | Critical | M |
| **DL-0093** | Detection | RDGA Nameserver Clustering Anomaly | 7 | Critical | M |
| **DL-0094** | Detection | RDGA Registrar Concentration Anomaly | 7 | Critical | M |
| **DL-0095** | Detection | TDS Redirect Chain Depth Analysis | 7 | Critical | M |
| **DL-0096** | Detection | TDS Cloaking Behavior Detection | 7 | Critical | M |
| **DL-0097** | Detection | TDS Shared Infrastructure Cross-Campaign Correlation | 7 | Critical | M |
| **DL-0098** | Detection | AI-Generated Domain Lexical Pattern Detection | 7 | Critical | M |
| **DL-0099** | Detection | Bulk Let's Encrypt Certificate Issuance Correlation | 7 | Critical | M |
| **DL-0100** | Detection | Zone File Daily Diff Anomaly Detection | 7 | Critical | M |
| **BL-0021** | Baseline | RDGA Cluster Size and Registration Norms | 7 | Critical | M |
| **BL-0022** | Baseline | TDS Chain Hop Count Norms | 7 | Critical | M |
| **BL-0023** | Baseline | AI vs Human Domain Registration Rate Norms | 7 | Critical | M |
| **TAX-03** | Taxonomy | Add `geopolitical_timing` frontmatter field | 8 | High | S |
| **TAX-04** | Taxonomy | Add `nation_state_nexus` frontmatter field | 8 | High | S |
| **TAX-05** | Taxonomy | Add fraud types: `sanctions-evasion-infrastructure`, `state-criminal-convergence` | 8 | High | S |
| **TP-0044** | Threat Path | State-Criminal Infrastructure Convergence | 8 | High | L |
| **TP-0045** | Threat Path | Sanctions Evasion via Fraud Infrastructure | 8 | High | L |
| **TP-0046** | Threat Path | Geopolitically-Timed Fraud Campaigns | 8 | High | L |
| **DL-0101** | Detection | State-Criminal Shared Infrastructure Overlap | 8 | High | M |
| **DL-0102** | Detection | Sanctions Designation Infrastructure Migration | 8 | High | M |
| **DL-0103** | Detection | Stablecoin Settlement Pattern Anomaly | 8 | High | M |
| **DL-0104** | Detection | BPH Rebranding Chain Detection | 8 | High | M |
| **DL-0105** | Detection | Election-Cycle Domain Registration Spike | 8 | High | M |
| **DL-0106** | Detection | Sanctions-Announcement Infrastructure Correlation | 8 | High | M |
| **DL-0107** | Detection | Politically-Motivated DDoS Financial Sector Targeting | 8 | High | M |
| **BL-0024** | Baseline | State-Actor Infrastructure Reuse Norms | 8 | High | M |
| **BL-0025** | Baseline | Geopolitical Event Domain Registration Norms | 8 | High | M |
| **TAX-06** | Taxonomy | Add fraud types: `human-trafficking-facilitation`, `bph-migration`, `crypto-laundering-infrastructure` | 9 | Medium | S |
| **TP-0047** | Threat Path | Human Trafficking-Linked Fraud Infrastructure | 9 | Medium | L |
| **TP-0048** | Threat Path | Bulletproof Hosting Migration Patterns | 9 | Medium | L |
| **TP-0049** | Threat Path | Cryptocurrency Laundering Infrastructure | 9 | Medium | L |
| **DL-0108** | Detection | Pig Butchering Domain Infrastructure Clustering | 9 | Medium | M |
| **DL-0109** | Detection | Scam Compound Cryptocurrency Payment Infrastructure | 9 | Medium | M |
| **DL-0110** | Detection | BPH IP Block Migration Post-Sanctions | 9 | Medium | M |
| **DL-0111** | Detection | Cloud Provider IP Abuse for BPH Resale | 9 | Medium | M |
| **DL-0112** | Detection | CNAME Clustering for DGA Domain Networks | 9 | Medium | M |
| **DL-0113** | Detection | CMLN Wallet Cluster Velocity | 9 | Medium | M |
| **DL-0114** | Detection | No-KYC Exchange Off-Ramp Pattern | 9 | Medium | M |
| **BL-0026** | Baseline | BPH Migration Timing and Relocation Norms | 9 | Medium | M |
| **BL-0027** | Baseline | Cryptocurrency Laundering Cycle Duration Norms | 9 | Medium | M |
| **EP-0006** | Emulation | RDGA Campaign Simulation | 9 | Medium | L |
| **EP-0007** | Emulation | TDS Chain Exploitation Simulation | 9 | Medium | L |
| **DOCS-01** | Docs | Update TAXONOMY.md with new fraud types and fields | All | Critical | M |
| **DOCS-02** | Docs | Update CONTRIBUTING.md with new field guidance | All | Critical | S |
| **SCRIPTS-01** | Scripts | Update validate_submission.py for new fields | All | Critical | M |
| **SCRIPTS-02** | Scripts | Update build_database.py for new field indexing | All | High | M |
| **SCRIPTS-03** | Scripts | Update export_flame_stix.py for new SDO types | All | High | M |
| **MCP-01** | MCP | Update MCP tools to support new fields | All | High | M |
| **CI-01** | CI | Update validate-pr.yml for new field validation | All | High | S |

**Size key:** S = < 1 day, M = 1-2 days, L = 3-5 days

---

## Phase 7: Infrastructure Intelligence Expansion (Critical Priority)

Intel report Tier 1 -- high feasibility, high impact. These items extend FLAME into the infrastructure generation layer, addressing the upstream supply chain that enables downstream fraud campaigns.

### TAX-01: Add `infrastructure_generation_method` Frontmatter Field

**Description:** Add a new optional frontmatter field `infrastructure_generation_method` to the threat path schema. This field classifies how the fraud infrastructure (domains, hosting, certificates) was generated.

**Allowed values:**
- `manual` -- Domains registered individually or in small batches by human operators
- `dga-embedded` -- Domain Generation Algorithm embedded in malware; algorithm is discoverable through reverse engineering
- `rdga-registered` -- Registered Domain Generation Algorithm; all domains are registered, algorithm is secret, detection requires cluster analysis
- `ai-assisted` -- AI tools used to generate domain names, content, or infrastructure configurations at scale

**Schema change:** Add to the `frontmatter_schema` in `Templates/threat-path-template.md` and `flame_taxonomy.json`.

**Acceptance criteria:**
- Field is documented in TAXONOMY.md with allowed values and descriptions
- `validate_submission.py` validates the field when present (optional field, but values must match the allowed list)
- Existing TPs are not required to retroactively populate this field
- `build_database.py` indexes the field for search and filtering
- `flame_taxonomy.json` includes the field definition

### TAX-02: Add New Fraud Types

**Description:** Add three new fraud types to the taxonomy:
- `rdga-infrastructure` -- Registered Domain Generation Algorithm campaigns where all generated domains are registered and the algorithm is secret
- `tds-exploitation` -- Traffic Distribution System exploitation as an infrastructure-layer threat, including multi-hop redirect chains with cloaking capabilities
- `ai-accelerated-fraud-infrastructure` -- AI-assisted generation of fraud infrastructure at scale, including domain registration, content generation, and campaign orchestration

**Acceptance criteria:**
- Fraud types added alphabetically to `flame_taxonomy.json`
- Descriptions added to `docs/TAXONOMY.md` fraud types table
- `validate_submission.py` accepts the new types

---

### TP-0041: RDGA-Based Infrastructure Campaigns

**Description:** Registered Domain Generation Algorithms represent a fundamentally different threat path from traditional embedded DGAs. In RDGA campaigns, all generated domains are registered (not just resolved), the algorithm remains secret (not embedded in discoverable malware), and detection requires cluster analysis of registration timing, nameserver patterns, and registrar concentration rather than reverse engineering.

**Key intelligence (from report):**
- Infoblox has observed over 3 million RDGA domains to date, with tens of thousands discovered daily
- The Revolver Rabbit actor alone registered 500,000+ domains at a cost exceeding $1 million
- Key actors: Prolific Puma (malicious link shortening), VexTrio Viper (TDS), Savvy Seahorse (investment scams), Vault Viper (illegal gambling)
- Detection is possible through clustering algorithms operating on zone file diffs and DNS resolution metadata

**Frontmatter requirements:**
- `infrastructure_generation_method: rdga-registered`
- `fraud_types: [rdga-infrastructure]`
- `sector: [cross-sector, banking, crypto, investment]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**CFPF phase mapping scope:**
- P1 (Recon): Algorithm development, registrar selection for bulk registration, nameserver infrastructure provisioning
- P2 (Initial Access): Bulk domain registration via RDGA, DNS configuration, certificate provisioning (bulk Let's Encrypt)
- P3 (Positioning): Domain activation, TDS/redirect chain configuration, cloaking implementation, content population
- P4 (Execution): Campaign launch, victim routing through RDGA domains, payload delivery or credential harvesting
- P5 (Monetization): Revenue through affiliate fraud, credential sale, scam conversion, infrastructure rental to affiliates

**Sub-classifications to document:**
- C2 infrastructure generation
- TDS entry point generation
- Malicious link shortening services
- Investment scam landing pages
- Gambling/adult content infrastructure

**Cross-references:** TP-0042 (TDS chains use RDGA domains), TP-0043 (AI may assist RDGA pattern generation)

**Acceptance criteria:**
- Full CFPF phase mapping with techniques, descriptions, and indicators per phase
- Sub-classification table for RDGA use cases with named actor examples
- Detection approaches section with Sigma rules for zone file diff analysis and nameserver clustering
- Look Left / Look Right analysis
- Controls and mitigations section with controls per CFPF phase
- Underground ecosystem context documenting RDGA-as-a-service offerings
- UCFF alignment table
- All references cited with URLs

### TP-0042: Traffic Distribution System (TDS) Chain Exploitation

**Description:** Model TDS as an infrastructure-layer threat path with defined architectural roles: entry point domains, intermediate redirect nodes, cloaking nodes, and landing page hosts. TDS operators serve as critical enablers for downstream fraud campaigns, routing victim traffic through multi-hop redirect chains with geolocation and device-based cloaking.

**Key intelligence (from report):**
- VexTrio operates 70,000+ TDS domains serving 60+ affiliate cybercrime groups
- In June 2025, Infoblox shared 100,000 VexTrio domain names with Spamhaus
- 82% of customer environments contacted domains tied to malicious adtech
- Nearly 500,000 TDS domains observed in a 12-month period
- Hazy Hawk hijacks abandoned cloud resources via DNS misconfigurations, targeting CDC, Fortune 500, and government entities

**Frontmatter requirements:**
- `fraud_types: [tds-exploitation]`
- `sector: [cross-sector, banking, payments, retail]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**CFPF phase mapping scope:**
- P1 (Recon): Identification of legitimate domain resources to hijack (Hazy Hawk pattern), selection of high-traffic malvertising entry points
- P2 (Initial Access): Entry point domain deployment, SEO poisoning or malvertising to drive traffic into TDS
- P3 (Positioning): Multi-hop redirect chain configuration, cloaking rules (geolocation, device type, referrer, time-of-day), affiliate routing setup
- P4 (Execution): Active traffic routing to landing pages, real-time cloaking to evade security scanners, payload or credential harvesting delivery
- P5 (Monetization): Pay-per-install commissions, affiliate fraud revenue sharing, credential data sale

**Architecture model to document:**
- Entry point domains (malvertising, compromised legitimate sites, typosquats)
- Intermediate redirect nodes (HTTP 302 chains, JavaScript redirects)
- Cloaking nodes (geolocation filtering, device fingerprint checks, bot detection)
- Landing page hosts (phishing kits, exploit kits, scam pages)

**Cross-references:** TP-0041 (RDGAs generate TDS domains), TP-0043 (AI generates landing page content)

**Acceptance criteria:**
- TDS architectural role taxonomy with defined node types and their functions
- Full CFPF phase mapping with graph traversal implications documented
- Detection approaches for multi-hop redirect resolution and cloaking behavior identification
- Sigma rules for DNS-layer TDS chain detection
- Look Left / Look Right analysis emphasizing graph traversal from any detected node to campaign attribution
- Controls section including DNS-layer blocking, redirect chain analysis, and cloaking detection

### TP-0043: AI-Accelerated Fraud Infrastructure Generation

**Description:** Document how AI tools have collapsed the economics of fraud infrastructure generation, reducing campaign creation time from 16 hours to 5 minutes, increasing phishing click-through rates from 12% to 54%, and enabling 38,000+ new scam pages per day.

**Key intelligence (from report):**
- 82.6% of phishing emails contain AI-generated content (KnowBe4 2025)
- 1,265% increase in malicious phishing email since ChatGPT launch (SlashNext)
- AI-generated phishing campaigns 24% more effective than elite human red teams by March 2025 (Hoxhunt)
- 54% click-through rate for AI-generated vs 12% for human-crafted (CrowdStrike 2025)
- 456-1,900% growth in GenAI-enabled scams (Sift Q2 2025, TRM Labs)
- Campaign creation time reduced from 16 hours to 5 minutes
- AI-enabled scams 4.5x more profitable than traditional scams (Chainalysis 2026)
- Scam technology vendors received $375.9M in crypto in 2024, with AI service vendors growing at 1,900% CAGR

**Frontmatter requirements:**
- `infrastructure_generation_method: ai-assisted`
- `fraud_types: [ai-accelerated-fraud-infrastructure, phishing, brand-impersonation]`
- `sector: [cross-sector, banking, payments, crypto]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**CFPF phase mapping scope:**
- P1 (Recon): AI-powered target identification, automated OSINT, brand asset scraping for impersonation
- P2 (Initial Access): AI-generated phishing emails and landing pages, personalized spearphishing at scale, AI-crafted vishing scripts
- P3 (Positioning): Automated domain infrastructure deployment, AI-generated content for credential harvesting pages, deepfake integration for verification bypass
- P4 (Execution): AI-optimized campaign delivery, adaptive content based on victim interaction, automated credential capture and relay
- P5 (Monetization): Automated credential monetization, AI-optimized pricing on dark web markets, infrastructure recycling

**Cross-references:** TP-0041 (AI may assist RDGA generation), TP-0042 (AI generates TDS landing page content), TP-0029 (AI document forgery)

**Acceptance criteria:**
- Quantitative evidence section citing all statistics from the intelligence report with original sources
- CFPF phase mapping showing how AI accelerates each phase
- Comparison table: traditional vs AI-accelerated fraud infrastructure (time, cost, scale, detection difficulty)
- Detection approaches focused on infrastructure patterns rather than content (the report's core thesis)
- Controls section addressing the structural challenge that content-based detection cannot scale against AI-generated content

---

### DL-0092 through DL-0100: Phase 7 Detection Rules

**DL-0092: RDGA Registration Timing Pattern**
- Threat paths: TP-0041
- CFPF phase: P2
- Fraud types: `rdga-infrastructure`
- Logic: Detect clusters of domain registrations with algorithmically regular timing intervals (e.g., N domains registered at M-second intervals across a 24-hour zone file diff). Alert when cluster size exceeds threshold and inter-registration timing standard deviation is below threshold.
- Logsource: `zone_file_diff`
- Acceptance criteria: Sigma-format rule with tunable cluster size and timing parameters; false positive documentation

**DL-0093: RDGA Nameserver Clustering Anomaly**
- Threat paths: TP-0041
- CFPF phase: P2
- Fraud types: `rdga-infrastructure`
- Logic: Detect disproportionate concentration of newly registered domains pointing to the same nameserver infrastructure within a 24-hour window. RDGA campaigns typically use a small number of nameservers for large domain clusters.
- Logsource: `zone_file_diff`
- Acceptance criteria: Sigma-format rule with configurable NS concentration threshold; false positive list for legitimate bulk registrars

**DL-0094: RDGA Registrar Concentration Anomaly**
- Threat paths: TP-0041
- CFPF phase: P2
- Fraud types: `rdga-infrastructure`
- Logic: Detect anomalous concentration of new registrations at a single registrar that share lexical similarity patterns and nameserver infrastructure, suggesting algorithmic generation.
- Logsource: `zone_file_diff`
- Acceptance criteria: Sigma-format rule combining registrar ID, lexical entropy, and NS clustering

**DL-0095: TDS Redirect Chain Depth Analysis**
- Threat paths: TP-0042
- CFPF phase: P3
- Fraud types: `tds-exploitation`
- Logic: Detect HTTP redirect chains (302/301/JavaScript) exceeding N hops where intermediate nodes are newly registered or have low reputation scores. Legitimate redirects rarely exceed 3 hops; TDS chains commonly use 4-7+.
- Logsource: `dns_resolution`, `web_proxy`
- Acceptance criteria: Sigma-format rule with configurable hop depth threshold; DNS-layer and proxy-layer variants

**DL-0096: TDS Cloaking Behavior Detection**
- Threat paths: TP-0042
- CFPF phase: P3
- Fraud types: `tds-exploitation`
- Logic: Detect domains that serve different content based on geolocation, device fingerprint, or user agent. Specifically, domains that return benign content (parked pages, 404 errors, legitimate-looking content) to security scanner user agents or datacenter IP ranges but serve redirects or malicious content to residential IP ranges.
- Logsource: `web_proxy`, `dns_resolution`
- Acceptance criteria: Rule documents both active probing and passive detection approaches

**DL-0097: TDS Shared Infrastructure Cross-Campaign Correlation**
- Threat paths: TP-0042
- CFPF phase: P3
- Fraud types: `tds-exploitation`
- Logic: Detect when domains from different apparent campaigns share hosting infrastructure, nameservers, or registration patterns -- indicating a common TDS operator serving multiple affiliates. Graph-based detection: domains resolving to the same IP CIDR block with different registrant information but similar registration timing.
- Logsource: `zone_file_diff`, `dns_resolution`
- Acceptance criteria: Rule includes graph traversal logic description suitable for Neo4j or similar graph database

**DL-0098: AI-Generated Domain Lexical Pattern Detection**
- Threat paths: TP-0043
- CFPF phase: P2
- Fraud types: `ai-accelerated-fraud-infrastructure`
- Logic: Detect domain registrations exhibiting lexical patterns consistent with AI-generated names: natural-language-like domain names that are grammatically plausible but not established brands, unusual TLD selection patterns, and registration in bulk with similar lexical characteristics.
- Logsource: `zone_file_diff`, `ct_log`
- Acceptance criteria: Sigma-format rule with entropy and n-gram analysis parameters

**DL-0099: Bulk Let's Encrypt Certificate Issuance Correlation**
- Threat paths: TP-0041, TP-0042, TP-0043
- CFPF phase: P2
- Fraud types: `rdga-infrastructure`, `tds-exploitation`, `ai-accelerated-fraud-infrastructure`
- Logic: Detect clusters of Let's Encrypt certificate issuances for domains sharing nameserver or registrar characteristics within a short time window. RDGA and AI-generated campaigns frequently provision certificates in bulk immediately after registration.
- Logsource: `ct_log`
- Acceptance criteria: Sigma-format rule correlating CT log entries with zone file registration data

**DL-0100: Zone File Daily Diff Anomaly Detection**
- Threat paths: TP-0041, TP-0042, TP-0043
- CFPF phase: P2
- Fraud types: `rdga-infrastructure`, `tds-exploitation`, `ai-accelerated-fraud-infrastructure`
- Logic: Detect anomalous patterns in daily zone file diffs: unusual volume of new registrations in a single TLD, concentration of registrations at specific registrars, or patterns suggesting algorithmic generation (lexical similarity, sequential naming, entropy clustering).
- Logsource: `zone_file_diff`
- Acceptance criteria: Sigma-format rule with tunable thresholds for registration volume, registrar concentration, and lexical similarity

---

### BL-0021 through BL-0023: Phase 7 Baselines

**BL-0021: RDGA Cluster Size and Registration Norms**
- Description: Defines normal parameters for domain registration clusters detected in CZDS zone file daily diffs
- Normal patterns:
  - Legitimate bulk registrars register 50-500 domains/day with diverse nameserver configurations
  - RDGA clusters typically show 1,000-50,000+ domains registered within a 24-hour window pointing to fewer than 5 nameserver clusters
  - Normal inter-registration timing standard deviation exceeds 30 minutes; RDGA timing standard deviation is typically under 5 minutes
  - Normal registrar-to-nameserver ratios show 1 registrar distributing across 10+ NS providers; RDGA shows 1 registrar concentrated on 1-3 NS providers
- Application: DL-0092, DL-0093, DL-0094 threshold calibration
- Acceptance criteria: Quantitative thresholds with cited sources (Infoblox 2025 data)

**BL-0022: TDS Chain Hop Count Norms**
- Description: Defines normal redirect chain depth for legitimate web traffic vs TDS exploitation
- Normal patterns:
  - Legitimate marketing redirects: 1-3 hops (mean 1.8)
  - Legitimate ad networks: 2-4 hops (mean 2.7)
  - TDS exploitation chains: 4-7+ hops (mean 5.2)
  - Legitimate redirects complete within 2 seconds; TDS chains introduce 500ms-2s latency per hop
  - Legitimate redirect chains use consistent geolocation; TDS chains traverse 2+ countries
- Application: DL-0095 threshold calibration
- Acceptance criteria: Hop count distributions with percentile breakdowns

**BL-0023: AI vs Human Domain Registration Rate Norms**
- Description: Defines registration rate and pattern baselines for distinguishing AI-assisted from human-operated domain infrastructure campaigns
- Normal patterns:
  - Human-operated campaigns: 10-100 domains/day, irregular timing, diverse naming patterns
  - AI-assisted campaigns: 100-10,000+ domains/day, regular timing, lexically coherent naming patterns
  - Pre-ChatGPT baseline (2022): approximately 70% of NRDs classified as malicious/suspicious (Palo Alto)
  - Post-AI acceleration: 38,000+ new scam pages per day (Bolster 2026)
- Application: DL-0098, DL-0100 threshold calibration
- Acceptance criteria: Rate comparisons with pre/post AI-acceleration data

---

## Phase 8: Geopolitical and State-Actor Context (High Priority)

Intel report Tier 2 -- medium feasibility, high impact. These items extend FLAME into the geopolitical dimension, modeling threats that cross the traditional boundary between APT and criminal taxonomies.

### TAX-03: Add `geopolitical_timing` Frontmatter Field

**Description:** Add a new optional frontmatter field `geopolitical_timing` to capture whether a threat path's campaigns are correlated with geopolitical events.

**Allowed values:**
- `none` -- No observed geopolitical timing correlation
- `election-cycle` -- Campaigns timed to election periods
- `sanctions-response` -- Infrastructure changes triggered by sanctions announcements
- `conflict-triggered` -- Activity spikes correlated with military conflicts
- `seasonal-political` -- Campaigns timed to political budget cycles, legislative sessions, or diplomatic summits

**Acceptance criteria:**
- Field documented in TAXONOMY.md
- `validate_submission.py` validates allowed values
- Existing TPs not required to retroactively populate

### TAX-04: Add `nation_state_nexus` Frontmatter Field

**Description:** Add a new optional frontmatter field `nation_state_nexus` to classify the degree of nation-state involvement in a threat path.

**Allowed values:**
- `none` -- No nation-state involvement
- `suspected` -- Circumstantial evidence of state involvement (shared infrastructure, timing correlation)
- `confirmed` -- Attribution by government agencies or multiple independent threat intelligence firms
- `hybrid` -- Documented convergence of state and criminal actors (e.g., Moonstone Sleet deploying Qilin ransomware)

**Acceptance criteria:**
- Field documented in TAXONOMY.md with evidentiary standards for each level
- `validate_submission.py` validates allowed values
- Analyst guidance documented: `confirmed` requires at least one government attribution or two independent CTI firm attributions; `suspected` requires documented infrastructure overlap or timing correlation

### TAX-05: Add New Fraud Types

**Description:** Add two new fraud types to the taxonomy:
- `sanctions-evasion-infrastructure` -- Fraud infrastructure that exists because of sanctions pressure, including alternative payment rails, stablecoin systems designed to circumvent enforcement, and infrastructure migration patterns following OFAC designations
- `state-criminal-convergence` -- Threat paths where state-sponsored actors and criminal organizations share infrastructure, tools, or operational relationships

**Acceptance criteria:**
- Fraud types added alphabetically to `flame_taxonomy.json`
- Descriptions added to `docs/TAXONOMY.md` fraud types table

---

### TP-0044: State-Criminal Infrastructure Convergence

**Description:** Document threat paths where actors cross the traditional APT/criminal boundary, sharing infrastructure, tools, and operational relationships in ways that current taxonomies (MITRE ATT&CK, STIX) do not model.

**Key intelligence (from report):**
- Moonstone Sleet (DPRK) deploying Qilin ransomware (Russian-origin RaaS) -- first documented state-criminal ransomware partnership (Microsoft, March 2025)
- Gen Digital (July 2025) found an IP address hosting both Gamaredon (Russian FSB-linked) C2 infrastructure and obfuscated Lazarus Group malware four days later -- shared Russian-DPRK infrastructure
- DPRK using Chinese laundering networks (CMLNs) for off-ramping heist proceeds
- Atlantic Council "Hidden Enablers" report mapped four DPRK third-country exploitation pathways
- Korean Leaks campaign targeting 25 South Korean financial institutions in a single month (Sept-Oct 2025)

**Frontmatter requirements:**
- `nation_state_nexus: hybrid`
- `fraud_types: [state-criminal-convergence, crypto-laundering, malware]`
- `sector: [banking, crypto, cross-sector]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**CFPF phase mapping scope:**
- P1 (Recon): State intelligence apparatus provides target identification; criminal networks provide infrastructure knowledge
- P2 (Initial Access): State-developed exploit tools deployed through criminal infrastructure (RaaS platforms)
- P3 (Positioning): Shared hosting infrastructure, shared C2 servers, overlapping DNS configurations
- P4 (Execution): State objectives (espionage, financial theft) executed through criminal operational methods (ransomware, credential harvesting)
- P5 (Monetization): Criminal laundering networks (CMLNs, no-KYC exchanges) used for state-sponsored theft proceeds

**Acceptance criteria:**
- Convergence model documenting at least three confirmed state-criminal infrastructure sharing patterns
- CFPF phase mapping with indicators for detecting shared infrastructure
- Cross-framework mapping noting where MITRE ATT&CK and STIX assumptions of APT/criminal separation break down
- Detection approaches focused on infrastructure overlap indicators
- References to government attributions (FBI IC3, Microsoft Threat Intelligence, CSIS)

### TP-0045: Sanctions Evasion via Fraud Infrastructure

**Description:** Model sanctions evasion infrastructure as a distinct fraud motivation category, documenting how sanctions pressure creates structural demand for disposable domain infrastructure, bulletproof hosting, and alternative payment rails that then become commercially available to non-state fraud actors.

**Key intelligence (from report):**
- A7A5 ruble-backed stablecoin: $93.3B processed in less than one year, $39B linked to sanctions evasion (Chainalysis/TRM Labs 2026)
- Huione Group: $98B total crypto inflows, $4B+ confirmed illicit, including $37M from DPRK cyber heists
- Huione launched USDH stablecoin specifically designed to be "unfreezable" by law enforcement
- Funnull Technology: 332,000+ DGA domains across 548 CNAMEs, purchased Polyfill.io for supply chain attacks (OFAC designated May 2025)
- BPH rebranding chains: Garantex to Grinex, Aeza to Smart Digital/Datavice (OFAC sanctioned November/July 2025)

**Frontmatter requirements:**
- `nation_state_nexus: confirmed`
- `geopolitical_timing: sanctions-response`
- `fraud_types: [sanctions-evasion-infrastructure, crypto-laundering]`
- `sector: [crypto, banking, cross-sector]`

**CFPF phase mapping scope:**
- P1 (Recon): Identification of sanctions enforcement gaps, selection of jurisdictions with weak regulatory oversight
- P2 (Initial Access): Establishment of alternative payment rails (stablecoins, escrow services), BPH infrastructure deployment
- P3 (Positioning): Onboarding of criminal clients to sanctions-evasion infrastructure, integration with existing fraud ecosystems
- P4 (Execution): Processing of sanctioned entity transactions, domain infrastructure provision for fraud campaigns
- P5 (Monetization): Revenue from infrastructure rental, transaction fees, stablecoin issuance

**Acceptance criteria:**
- Case studies for at least three sanctions evasion infrastructure patterns (A7A5, Huione/USDH, Funnull, BPH rebranding)
- Infrastructure migration timeline documenting post-sanctions relocation patterns
- Detection approaches for sanctions-triggered infrastructure changes
- Integration points with OFAC SDN list cross-referencing

### TP-0046: Geopolitically-Timed Fraud Campaigns

**Description:** Document how fraud campaigns and hacktivist attacks are timed to elections, sanctions announcements, military conflicts, and other geopolitical events, specifically targeting financial services.

**Key intelligence (from report):**
- Finance Derivative 2026 research validates that hacktivist attacks on banks and payment providers are carefully timed to elections and geopolitical events
- Financial services bore 44% of total Layer 7 DNS attack activity in 2024 (Radware)
- 393% year-over-year growth in DDoS volume per financial organization
- 550+ claimed DDoS attacks from politically motivated groups in Q1 2025 (U.S. targets)
- Pro-Russian groups (NoName, Killnet) target countries with pro-Ukrainian positions
- Pro-Palestinian groups target Western and Gulf financial sectors
- Orange Cyberdefense warns of hacktivism extending toward cyber-physical risk in ICS/OT environments

**Frontmatter requirements:**
- `geopolitical_timing: election-cycle` (or other applicable value)
- `nation_state_nexus: suspected`
- `fraud_types: [state-criminal-convergence]`
- `sector: [banking, payments, cross-sector]`

**Acceptance criteria:**
- Timeline visualization of geopolitical events correlated with fraud campaign spikes
- CFPF phase mapping with geopolitical trigger points identified per phase
- Detection approaches for election-cycle and sanctions-announcement domain registration spikes
- Controls section addressing the compounding threat of fraud infrastructure, state pre-positioning, and politically motivated disruption through overlapping DNS and hosting infrastructure

---

### DL-0101 through DL-0107: Phase 8 Detection Rules

**DL-0101: State-Criminal Shared Infrastructure Overlap**
- Threat paths: TP-0044
- CFPF phase: P3
- Fraud types: `state-criminal-convergence`
- Logic: Detect when IP addresses, nameservers, or hosting infrastructure previously attributed to state-sponsored threat actors begin hosting domains or services associated with criminal campaigns (or vice versa). Graph-based detection: shared IP CIDR blocks, nameserver overlap, and temporal proximity of domain registrations.
- Acceptance criteria: Rule includes threat intelligence feed integration points; graph traversal query for Neo4j

**DL-0102: Sanctions Designation Infrastructure Migration**
- Threat paths: TP-0045
- CFPF phase: P3
- Fraud types: `sanctions-evasion-infrastructure`
- Logic: Detect infrastructure migration patterns following OFAC sanctions designations. Specifically: domains previously resolving to sanctioned entity IP ranges that migrate to new hosting within 7-30 days of designation, retaining similar DNS configurations but different IP blocks. Track the Aeza to Smart Digital/Datavice and Garantex to Grinex patterns.
- Acceptance criteria: Rule includes OFAC SDN list cross-reference integration; temporal correlation with designation dates

**DL-0103: Stablecoin Settlement Pattern Anomaly**
- Threat paths: TP-0045
- CFPF phase: P4
- Fraud types: `sanctions-evasion-infrastructure`, `crypto-laundering`
- Logic: Detect stablecoin transaction patterns consistent with sanctions evasion settlement: Monday-Friday volume surges with weekend drops (indicating business settlement rather than retail), transaction clustering to known no-KYC exchange addresses, and volume patterns matching the A7A5 profile.
- Acceptance criteria: Rule documents on-chain indicators; integration points with blockchain analytics platforms

**DL-0104: BPH Rebranding Chain Detection**
- Threat paths: TP-0045, TP-0048
- CFPF phase: P3
- Fraud types: `sanctions-evasion-infrastructure`, `bph-migration`
- Logic: Detect bulletproof hosting providers that rebrand following law enforcement or sanctions action. Indicators: new hosting entities advertising the same IP ranges, same BGP ASN prefixes, or same upstream transit providers as recently sanctioned or seized BPH operations.
- Acceptance criteria: Rule includes BGP and IP allocation database integration points

**DL-0105: Election-Cycle Domain Registration Spike**
- Threat paths: TP-0046
- CFPF phase: P1
- Fraud types: `state-criminal-convergence`
- Logic: Detect anomalous increases in domain registrations containing financial institution brand names or financial services keywords during election periods. Compare registration volumes against a 90-day rolling baseline, alerting on 3x+ increases within 30 days of scheduled elections.
- Acceptance criteria: Rule includes election calendar integration; configurable baseline window

**DL-0106: Sanctions-Announcement Infrastructure Correlation**
- Threat paths: TP-0045, TP-0046
- CFPF phase: P3
- Fraud types: `sanctions-evasion-infrastructure`
- Logic: Detect correlations between OFAC/EU sanctions announcements and subsequent infrastructure changes: new domain registrations by sanctioned entity-linked registrars, IP block migrations, and new BGP announcements from previously quiet ASNs within 14 days of sanctions designation.
- Acceptance criteria: Rule includes sanctions announcement feed integration; 14-day temporal correlation window

**DL-0107: Politically-Motivated DDoS Financial Sector Targeting**
- Threat paths: TP-0046
- CFPF phase: P4
- Fraud types: `state-criminal-convergence`
- Logic: Detect Layer 7 DNS attack patterns targeting financial services infrastructure that correlate with geopolitical event timelines. Differentiate politically motivated DDoS from criminal extortion DDoS by examining claim attribution (Telegram channel claims), target selection patterns (geopolitically aligned targets), and timing correlation.
- Acceptance criteria: Rule documents L7 DNS attack indicators; Telegram channel monitoring integration

---

### BL-0024 through BL-0025: Phase 8 Baselines

**BL-0024: State-Actor Infrastructure Reuse Norms**
- Description: Defines baseline parameters for infrastructure sharing patterns between known state-sponsored and criminal threat actors
- Normal patterns:
  - IP address reuse between unrelated campaigns: typically 1-5% overlap due to shared hosting providers
  - Temporal proximity of state/criminal infrastructure on same IP: unrelated campaigns typically show 30+ day separation
  - State-criminal convergence indicator: same IP hosting attributed state and criminal infrastructure within 7 days (as observed in Gamaredon-Lazarus case)
- Application: DL-0101 threshold calibration

**BL-0025: Geopolitical Event Domain Registration Norms**
- Description: Defines baseline domain registration patterns around geopolitical events for financial services brand keywords
- Normal patterns:
  - Baseline: 50-200 new registrations per week containing major bank brand names
  - Pre-election spike (normal): 1.5-2x baseline in the 60 days before national elections
  - Anomalous: 3x+ baseline within 30 days of elections or sanctions announcements
  - Post-sanctions migration: 10-50 domains migrating from sanctioned IP ranges within 14 days of designation
- Application: DL-0105, DL-0106 threshold calibration

---

## Phase 9: Emerging Threat Vectors (Medium Priority)

Intel report Tier 3 -- strategic value. These items address the next wave of systemic threats to financial services, including the humanitarian dimension of human trafficking-linked fraud infrastructure.

### TAX-06: Add New Fraud Types

**Description:** Add three new fraud types to the taxonomy:
- `human-trafficking-facilitation` -- Fraud infrastructure that directly supports human trafficking operations, including credential harvesting for labor trafficking recruitment, cryptocurrency payment infrastructure for trafficking, and compound recruitment/control infrastructure
- `bph-migration` -- Bulletproof hosting migration patterns, including post-sanctions infrastructure relocation, rebranding chains, and cloud provider abuse
- `crypto-laundering-infrastructure` -- Cryptocurrency laundering infrastructure at the network level, including CMLN operations, no-KYC exchange off-ramping, and cross-chain bridge exploitation

**Acceptance criteria:**
- Fraud types added alphabetically to `flame_taxonomy.json`
- Descriptions added to `docs/TAXONOMY.md` fraud types table

---

### TP-0047: Human Trafficking-Linked Fraud Infrastructure

**Description:** Document the fraud infrastructure that enables and profits from human trafficking operations, particularly the Southeast Asian scam compound ecosystem. This threat path covers the infrastructure layer -- domains, cryptocurrency payment systems, and operational technology -- rather than the trafficking itself.

**Key intelligence (from report):**
- Americans lost at least $10B to Southeast Asia-based scam operations in 2024 (66% YoY increase)
- An estimated 150,000 people are trapped in Cambodian scam compounds and 100,000 in Myanmar
- Cryptocurrency flows to suspected human trafficking services surged 85% YoY in 2025
- Recruitment payments typically range from $1,000 to $10,000
- Huione Group processed $98B in total cryptocurrency inflows, $4B+ confirmed illicit
- U.S. Scam Center Strike Force froze and seized $578M in cryptocurrency within its first three months
- OFAC sanctioned Karen National Army, Shwe Kokko operators, Funnull Technology, and 146 Prince Group targets

**Frontmatter requirements:**
- `fraud_types: [human-trafficking-facilitation, scam-compound-operations, crypto-laundering]`
- `sector: [crypto, banking, cross-sector]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**CFPF phase mapping scope:**
- P1 (Recon): Victim recruitment infrastructure (fake job postings, social media lures), target identification for pig butchering operations
- P2 (Initial Access): Compound operational infrastructure (communication platforms, cryptocurrency wallets), initial victim contact via romance/investment scam domains
- P3 (Positioning): Relationship building infrastructure (scripted messaging platforms, deepfake video tools), cryptocurrency payment page deployment
- P4 (Execution): Pig butchering investment platform infrastructure, credential harvesting from scam targets, cryptocurrency transfer execution
- P5 (Monetization): CMLN off-ramping, Guarantee-style marketplace transactions, cross-border cryptocurrency flows

**Acceptance criteria:**
- Infrastructure taxonomy separating trafficking recruitment, compound operations, and fraud execution infrastructure
- Cryptocurrency flow analysis documenting the recruitment-to-laundering pipeline
- Detection approaches focused on infrastructure patterns detectable from DNS and hosting metadata
- Explicit scope limitation: this TP documents fraud infrastructure, not trafficking operations themselves
- References to OFAC designations and law enforcement actions

### TP-0048: Bulletproof Hosting Migration Patterns

**Description:** Document the lifecycle of bulletproof hosting providers, focusing on post-sanctions and post-seizure infrastructure relocation patterns that create detection opportunities.

**Key intelligence (from report):**
- Funnull Technology: 332,000+ domains, 548 CNAMEs, purchased Polyfill.io for supply chain attacks (OFAC designated May 2025)
- Aeza Group to Smart Digital/Datavice rebranding after OFAC sanctions (July 2025)
- Media Land sanctioned (November 2025) -- Russia-based BPH enabling ransomware, phishing, malware delivery
- CISA noted "marked increase" in BPH use against critical infrastructure
- Cloud provider abuse patterns: legitimate cloud IPs purchased in bulk and resold to cybercriminals

**Frontmatter requirements:**
- `fraud_types: [bph-migration, sanctions-evasion-infrastructure]`
- `sector: [cross-sector]`
- `cfpf_phases: [P1, P2, P3, P4, P5]`

**Acceptance criteria:**
- BPH lifecycle model from establishment through sanctions/seizure to rebranding and relocation
- At least three documented migration case studies (Funnull, Aeza, Garantex)
- Detection approaches for identifying BPH rebranding through BGP, IP allocation, and DNS infrastructure analysis
- Cloud provider abuse detection indicators (bulk IP acquisition, CNAME clustering)
- Controls section addressing the gap between BPH identification and enforcement action

### TP-0049: Cryptocurrency Laundering Infrastructure

**Description:** Document the cryptocurrency laundering infrastructure ecosystem at scale, focusing on Chinese Money Laundering Networks (CMLNs) as the primary off-ramp for state-sponsored theft and organized fraud.

**Key intelligence (from report):**
- CMLNs processed $16.1B in 2025, approximately $44M/day across 1,799+ active wallets
- CMLNs represent roughly 20% of all known illicit crypto laundering over the past five years
- CMLN inflows growing 7,325x faster than illicit inflows to centralized exchanges since 2020
- TRM Labs: Chinese-language escrow and underground banking volume exceeded $103B in adjusted crypto volume in 2025
- Six distinct CMLN service types: running point brokers, money mules, OTC services, "Black U" services ($1B in 236 days, 1.6 min average processing), gambling platforms, money movement services
- DPRK 45-day laundering cycle: distancing (days 1-5) to integration (days 5-14) to off-ramping (days 20-45)
- CMLNs launder over 10% of funds stolen in pig butchering scams

**Frontmatter requirements:**
- `fraud_types: [crypto-laundering-infrastructure, cmln-operations]`
- `sector: [crypto, banking, cross-sector]`
- `cfpf_phases: [P4, P5]` (primarily monetization and laundering infrastructure)

**Acceptance criteria:**
- CMLN service type taxonomy with six categories documented
- DPRK 45-day laundering cycle timeline with infrastructure touchpoints at each stage
- On-chain detection approaches for CMLN wallet cluster identification
- Cross-reference with TP-0044 (state-criminal convergence) and TP-0045 (sanctions evasion)
- Infrastructure detection approaches that can be operationalized through DNS/hosting analysis (not requiring blockchain analytics)

---

### DL-0108 through DL-0114: Phase 9 Detection Rules

**DL-0108: Pig Butchering Domain Infrastructure Clustering**
- Threat paths: TP-0047
- CFPF phase: P3
- Fraud types: `human-trafficking-facilitation`, `scam-compound-operations`
- Logic: Detect clusters of domains exhibiting pig butchering investment platform characteristics: similar page structures, cryptocurrency wallet integration, registration through privacy-protected registrars, hosted on known scam compound infrastructure IP ranges.
- Acceptance criteria: Sigma-format rule; documents Funnull-pattern CNAME clustering

**DL-0109: Scam Compound Cryptocurrency Payment Infrastructure**
- Threat paths: TP-0047
- CFPF phase: P4
- Fraud types: `human-trafficking-facilitation`, `crypto-laundering`
- Logic: Detect domain clusters with cryptocurrency payment page patterns (wallet address display, QR code generation, transaction verification) registered in bulk through shared registrar/nameserver infrastructure.
- Acceptance criteria: Rule documents both DNS-layer and content-layer indicators

**DL-0110: BPH IP Block Migration Post-Sanctions**
- Threat paths: TP-0048
- CFPF phase: P3
- Fraud types: `bph-migration`
- Logic: Detect IP address blocks that were previously associated with sanctioned or seized BPH providers appearing under new BGP announcements from different ASNs. Track the continuity of malicious hosting through IP block ownership changes.
- Acceptance criteria: Rule includes BGP monitoring integration points and IP allocation database lookups

**DL-0111: Cloud Provider IP Abuse for BPH Resale**
- Threat paths: TP-0048
- CFPF phase: P2
- Fraud types: `bph-migration`
- Logic: Detect patterns consistent with legitimate cloud provider IP blocks being resold for BPH: unusual CNAME density (100+ domains per IP), diverse domain registrants sharing the same cloud IP range, and high complaint-to-domain ratios.
- Acceptance criteria: Rule documents Funnull-pattern indicators (332K domains across 548 CNAMEs)

**DL-0112: CNAME Clustering for DGA Domain Networks**
- Threat paths: TP-0048
- CFPF phase: P3
- Fraud types: `bph-migration`, `rdga-infrastructure`
- Logic: Detect anomalous CNAME record density where hundreds or thousands of apparently unrelated domains share CNAME chains terminating at a small number of infrastructure endpoints. This pattern indicates centrally managed infrastructure reusing cloud or CDN providers for mass domain hosting.
- Acceptance criteria: Sigma-format rule with configurable CNAME-to-endpoint ratio thresholds

**DL-0113: CMLN Wallet Cluster Velocity**
- Threat paths: TP-0049
- CFPF phase: P5
- Fraud types: `crypto-laundering-infrastructure`, `cmln-operations`
- Logic: Detect cryptocurrency wallet clusters exhibiting CMLN operational characteristics: high transaction velocity (average processing time under 2 minutes), incoming transfers from multiple unrelated sources, and rapid outbound distribution to exchange or OTC wallets.
- Acceptance criteria: Rule documents on-chain indicators; specifies integration with blockchain analytics platforms (Chainalysis, TRM Labs)

**DL-0114: No-KYC Exchange Off-Ramp Pattern**
- Threat paths: TP-0049
- CFPF phase: P5
- Fraud types: `crypto-laundering-infrastructure`
- Logic: Detect cryptocurrency flows matching the DPRK 45-day laundering cycle pattern: initial rapid distancing through DeFi protocols (days 1-5), integration through no-KYC exchanges (days 5-14), and off-ramping through Chinese OTC brokers (days 20-45). Temporal pattern matching against known laundering cycle timelines.
- Acceptance criteria: Rule includes temporal correlation parameters aligned with documented DPRK laundering timeline

---

### BL-0026 through BL-0027: Phase 9 Baselines

**BL-0026: BPH Migration Timing and Relocation Norms**
- Description: Defines baseline parameters for bulletproof hosting provider migration patterns following sanctions or seizure actions
- Normal patterns:
  - Time from sanctions designation to infrastructure migration: 7-30 days
  - Percentage of hosted domains that migrate vs abandon: typically 60-80% migrate, 20-40% abandoned
  - Rebranding entity registration timing: typically 0-14 days before or after the sanctions announcement (suggesting pre-positioning)
  - Geographic shift: typically moves from sanctioned jurisdiction to adjacent jurisdiction (Russia to Serbia/Uzbekistan in Aeza case)
- Application: DL-0110, DL-0104 threshold calibration

**BL-0027: Cryptocurrency Laundering Cycle Duration Norms**
- Description: Defines baseline parameters for cryptocurrency laundering cycle timelines
- Normal patterns:
  - DPRK laundering cycle: 45 days (distancing 1-5 days, integration 5-14 days, off-ramping 20-45 days)
  - CMLN processing time: average 1.6 minutes per transaction (Black U services)
  - Legitimate exchange settlement: 1-5 business days
  - Pig butchering proceeds laundering: 30-90 days from theft to final off-ramp
  - Cross-chain bridge hops: typically 2-4 chains in a 24-hour window during distancing phase
- Application: DL-0113, DL-0114 threshold calibration

---

### EP-0006: RDGA Campaign Simulation

**Description:** Emulation playbook simulating an end-to-end RDGA-based infrastructure campaign. Tests detection coverage across CFPF phases P1-P5 for RDGA domain registration, nameserver clustering, TDS integration, and campaign monetization patterns.

**Target threat paths:** TP-0041, TP-0042
**CFPF phases:** P1, P2, P3, P4, P5
**Fraud types:** `rdga-infrastructure`, `tds-exploitation`

**Steps (high-level):**
1. (P1) Simulate RDGA algorithm output generating 1,000+ domain names with controlled lexical patterns
2. (P2) Simulate bulk domain registration with concentrated registrar and nameserver configurations
3. (P2) Simulate bulk Let's Encrypt certificate provisioning for registered domains
4. (P3) Simulate TDS redirect chain configuration with cloaking rules
5. (P4) Simulate victim traffic routing through the RDGA-TDS infrastructure
6. (P5) Simulate affiliate revenue tracking and infrastructure rotation

**Expected detections triggered:** DL-0092, DL-0093, DL-0094, DL-0095, DL-0099, DL-0100

**Acceptance criteria:**
- JSON format following `Templates/emulation-playbook-template.json` schema
- Each step maps to a CFPF phase with expected detection rule references
- Prerequisites document required test environment capabilities (zone file simulation, DNS resolution monitoring)
- Expected outcomes section documents full detection coverage validation

### EP-0007: TDS Chain Exploitation Simulation

**Description:** Emulation playbook simulating a TDS chain exploitation campaign with multi-hop redirect chains, cloaking, and multi-affiliate routing.

**Target threat paths:** TP-0042
**CFPF phases:** P1, P2, P3, P4, P5
**Fraud types:** `tds-exploitation`

**Steps (high-level):**
1. (P1) Simulate identification of abandoned cloud resources for Hazy Hawk-style hijacking
2. (P2) Simulate entry point domain deployment via typosquats and malvertising
3. (P3) Simulate multi-hop redirect chain with 5+ intermediate nodes
4. (P3) Simulate cloaking rules: serve benign content to datacenter IPs, redirect residential IPs
5. (P4) Simulate victim routing to credential harvesting landing pages
6. (P5) Simulate affiliate revenue tracking across multiple downstream campaigns

**Expected detections triggered:** DL-0095, DL-0096, DL-0097

**Acceptance criteria:**
- JSON format following `Templates/emulation-playbook-template.json` schema
- Cloaking simulation step includes both active probing and passive detection validation
- Graph traversal validation: demonstrate that detection at any single TDS node enables traversal to full campaign infrastructure

---

## Supporting Work Items (All Phases)

These items must be completed to support the new content across all three phases. Taxonomy and validation updates are prerequisites for new threat paths and detection rules.

### DOCS-01: Update TAXONOMY.md

**Scope:**
- Add all new fraud types from TAX-02, TAX-05, TAX-06 (8 total) to the fraud types table with descriptions
- Add documentation for new frontmatter fields: `infrastructure_generation_method` (TAX-01), `geopolitical_timing` (TAX-03), `nation_state_nexus` (TAX-04)
- Add allowed values and usage guidance for each new field

**Acceptance criteria:**
- All new fraud types appear alphabetically in the fraud types table
- All new fields documented with allowed values, descriptions, and examples
- No existing documentation is removed or modified

### DOCS-02: Update CONTRIBUTING.md

**Scope:**
- Add field guidelines for `infrastructure_generation_method`, `geopolitical_timing`, and `nation_state_nexus` to the Field Guidelines section
- Document evidentiary standards for `nation_state_nexus` values (confirmed requires government attribution)
- Add guidance on when to use infrastructure-focused vs campaign-focused threat path structure

**Acceptance criteria:**
- New fields documented in Field Guidelines with same level of detail as existing fields
- Evidentiary standards are clear and actionable

### SCRIPTS-01: Update validate_submission.py

**Scope:**
- Add validation for `infrastructure_generation_method` field (optional, must be one of: manual, dga-embedded, rdga-registered, ai-assisted)
- Add validation for `geopolitical_timing` field (optional, must be one of: none, election-cycle, sanctions-response, conflict-triggered, seasonal-political)
- Add validation for `nation_state_nexus` field (optional, must be one of: none, suspected, confirmed, hybrid)
- Add new fraud types to the accepted values list

**Acceptance criteria:**
- Validation passes for existing TPs (no regressions)
- Validation accepts the new optional fields when present
- Validation rejects invalid values for new fields
- New fraud types accepted by validator

### SCRIPTS-02: Update build_database.py

**Scope:**
- Index new frontmatter fields (`infrastructure_generation_method`, `geopolitical_timing`, `nation_state_nexus`) in SQLite and JSON exports
- Add new fraud types to taxonomy export
- Update `flame-stats.json` generation to include new field aggregations

**Acceptance criteria:**
- New fields appear in `flame-data.json` and `flame-index.json`
- New fields are queryable in SQLite database
- `flame-stats.json` includes coverage counts for new fields

### SCRIPTS-03: Update export_flame_stix.py

**Scope:**
- Map new fraud types to STIX 2.1 SDO types
- Map `nation_state_nexus` field to STIX threat actor motivation vocabulary
- Map `geopolitical_timing` field to STIX campaign properties

**Acceptance criteria:**
- STIX 2.1 export includes new fraud types as observable objects
- Nation-state nexus maps to appropriate STIX threat-actor-motivation values
- Export passes STIX 2.1 validation

### MCP-01: Update MCP Tools

**Scope:**
- Update the 7 MCP tools to support filtering and searching by new frontmatter fields
- Ensure new fraud types are returned in taxonomy queries
- Add new field descriptions to tool documentation

**Acceptance criteria:**
- MCP tools return results filtered by `infrastructure_generation_method`, `geopolitical_timing`, and `nation_state_nexus`
- New fraud types appear in taxonomy tool responses
- Tool descriptions updated

### CI-01: Update validate-pr.yml

**Scope:**
- Update the PR validation workflow to validate new frontmatter fields in submitted threat paths
- Ensure the workflow accepts new fraud types

**Acceptance criteria:**
- PR validation passes for existing content (no regressions)
- PR validation accepts new optional fields with valid values
- PR validation rejects invalid values for new fields

---

## Dependencies

The following dependency chain must be respected during implementation:

```
Phase 7:
  TAX-01 + TAX-02 ─── must complete before ─── TP-0041, TP-0042, TP-0043
  SCRIPTS-01 ──────── must complete before ─── TP-0041, TP-0042, TP-0043 (validation)
  TP-0041 ──────────── should complete before ── DL-0092, DL-0093, DL-0094, BL-0021
  TP-0042 ──────────── should complete before ── DL-0095, DL-0096, DL-0097, BL-0022
  TP-0043 ──────────── should complete before ── DL-0098, BL-0023
  TP-0041 + TP-0042 ── should complete before ── DL-0099, DL-0100 (cross-TP rules)

Phase 8:
  TAX-03 + TAX-04 + TAX-05 ── must complete before ── TP-0044, TP-0045, TP-0046
  TP-0044 ──────────────────── should complete before ── DL-0101, BL-0024
  TP-0045 ──────────────────── should complete before ── DL-0102, DL-0103, DL-0104, DL-0106
  TP-0046 ──────────────────── should complete before ── DL-0105, DL-0107, BL-0025

Phase 9:
  TAX-06 ───────────── must complete before ─── TP-0047, TP-0048, TP-0049
  TP-0047 ──────────── should complete before ── DL-0108, DL-0109
  TP-0048 ──────────── should complete before ── DL-0110, DL-0111, DL-0112, BL-0026
  TP-0049 ──────────── should complete before ── DL-0113, DL-0114, BL-0027
  TP-0041 + TP-0042 ── should complete before ── EP-0006, EP-0007

Cross-cutting:
  DOCS-01 ──── should complete alongside each TAX item
  DOCS-02 ──── should complete alongside DOCS-01
  SCRIPTS-01 ── must complete before any new TPs are validated
  SCRIPTS-02 ── must complete before database rebuild after new content
  SCRIPTS-03 ── should complete before STIX export after new content
  MCP-01 ────── should complete after SCRIPTS-02
  CI-01 ─────── should complete alongside SCRIPTS-01
```

**Critical path:** SCRIPTS-01 and taxonomy updates (TAX-01 through TAX-06) are the hard blockers. All other items can proceed once their taxonomy prerequisites are met.

---

## Timeline Estimate

| Phase | Scope | Estimated Duration | Prerequisites |
|-------|-------|-------------------|---------------|
| **Pre-work** | SCRIPTS-01, CI-01 | 1-2 days | None |
| **Phase 7** | TAX-01, TAX-02, TP-0041-0043, DL-0092-0100, BL-0021-0023 | 10-14 days | Pre-work complete |
| **Phase 8** | TAX-03-05, TP-0044-0046, DL-0101-0107, BL-0024-0025 | 8-12 days | Phase 7 taxonomy stable |
| **Phase 9** | TAX-06, TP-0047-0049, DL-0108-0114, BL-0026-0027, EP-0006-0007 | 10-14 days | Phase 8 taxonomy stable |
| **Supporting** | DOCS-01, DOCS-02, SCRIPTS-02, SCRIPTS-03, MCP-01 | 3-5 days (parallel) | Ongoing with each phase |
| **Total** | 9 TPs, 23 DLs, 7 BLs, 2 EPs, 6 TAX, 7 supporting | **5-7 weeks** | |

**Notes on timeline:**
- Phases can overlap: Phase 8 taxonomy work can begin while Phase 7 threat paths are being written
- Detection rules and baselines can be written in parallel with their parent threat paths once the TP outline is stable
- Supporting work items (DOCS, SCRIPTS, MCP, CI) should be completed incrementally alongside each phase rather than batched at the end
- Emulation playbooks (EP-0006, EP-0007) are scheduled in Phase 9 but depend on Phase 7 content; they can be written as soon as TP-0041 and TP-0042 are stable

---

## Version Target

Completion of all three phases will constitute FLAME v1.1.0 (or v0.11.0 if following the current versioning convention), adding:
- 9 new threat paths (TP-0041 through TP-0049, total: 49)
- 23 new detection rules (DL-0092 through DL-0114, total: 114)
- 7 new baselines (BL-0021 through BL-0027, total: 27)
- 2 new emulation playbooks (EP-0006, EP-0007, total: 7)
- 8 new fraud types (total: 79)
- 3 new frontmatter fields
- Framework extension into infrastructure intelligence, geopolitical context, and emerging threat vectors

Individual phase releases:
- **Phase 7 release (v0.9.0):** 3 TPs, 9 DLs, 3 BLs, 3 fraud types, 1 frontmatter field
- **Phase 8 release (v0.10.0):** 3 TPs, 7 DLs, 2 BLs, 2 fraud types, 2 frontmatter fields
- **Phase 9 release (v0.11.0):** 3 TPs, 7 DLs, 2 BLs, 2 EPs, 3 fraud types
