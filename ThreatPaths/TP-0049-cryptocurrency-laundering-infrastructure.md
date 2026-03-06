# TP-0049: Cryptocurrency Laundering Infrastructure

```yaml
---
id: TP-0049
title: "Cryptocurrency Laundering Infrastructure"
category: ThreatPath
date: 2026-03-05
author: "FLAME Project (sourced from CrimsonVector Strategic Intelligence Report, Chainalysis, TRM Labs)"
source: "https://www.chainalysis.com/blog/crypto-crime-midyear-2025/"
tlp: WHITE
fraud_types:
  - crypto-laundering-infrastructure
  - cmln-operations
sector:
  - crypto
  - banking
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 85
source_reliability: A
info_credibility: 1
mitre_attack:
  - T1583.001
  - T1071.001
  - T1048
  - T1565.003
ft3_tactics: []
mitre_f3: []
groupib_stages:
  - "Monetization"
  - "Laundering"
ucff_domains:
  commit: "Level 4"
  assess: "Level 4"
  plan: "Level 4"
  act: "Level 4"
  monitor: "Level 4"
  report: "Level 4"
  improve: "Level 4"
related_tps:
  - id: TP-0044
    relationship: related-to
  - id: TP-0045
    relationship: shares-infrastructure
  - id: TP-0047
    relationship: related-to
tags:
  - cmln
  - cryptocurrency-laundering
  - no-kyc-exchange
  - otc-broker
  - black-u
  - dprk-laundering-cycle
  - cross-chain-bridge
  - huione-group
  - chainalysis
  - trm-labs
---
```

---

## Summary

Cryptocurrency Money Laundering Networks (CMLNs) have emerged as the dominant infrastructure layer enabling the monetization of virtually every category of crypto-enabled fraud and cybercrime. In 2025, CMLNs processed $16.1 billion across 1,799+ active wallets, averaging approximately $44 million per day (Chainalysis 2026). CMLNs now represent approximately 20% of all known illicit cryptocurrency laundering over the past five years, making them the single most consequential infrastructure component in the crypto-crime ecosystem. Critically, CMLN inflows have grown 7,325x faster than illicit inflows to centralized exchanges since 2020 -- a structural shift indicating that professional laundering networks have almost entirely displaced direct exchange-based cash-out as the preferred monetization pathway.

The CMLN ecosystem is composed of six distinct service types, each with specialized operational characteristics: running point brokers, money mules, OTC services, "Black U" services, gambling platforms, and money movement services. These service types operate as a layered, modular infrastructure -- threat actors can chain multiple CMLN services together to create complex laundering paths that frustrate blockchain analytics and law enforcement tracing. The "Black U" service category is particularly notable: a single Black U operation processed $1 billion in just 236 days with an average transaction processing time of 1.6 minutes, demonstrating industrial-scale, near-real-time laundering capability.

TRM Labs reports that Chinese-language escrow and underground banking volume exceeded $103 billion in adjusted crypto volume in 2025, indicating that CMLNs are deeply embedded in transnational organized crime networks operating at a scale that rivals legitimate financial infrastructure. CMLNs launder over 10% of funds stolen in pig butchering scams, establishing a direct operational link between upstream social engineering fraud and downstream crypto laundering infrastructure. The DPRK laundering cycle -- a structured 45-day process moving from distancing through integration to off-ramping -- demonstrates that nation-state actors have adopted CMLN infrastructure as a core component of their financial operations.

This threat path documents the CMLN service taxonomy, maps the laundering lifecycle across CFPF phases, and identifies both on-chain and infrastructure-layer detection approaches that can be operationalized to disrupt CMLN operations at scale.

---

## Threat Path Hypothesis

> **Hypothesis**: Cryptocurrency Money Laundering Networks have evolved into a professionalized, modular infrastructure ecosystem processing $16.1B annually across six distinct service types, enabling the monetization of upstream fraud (pig butchering, ransomware, state-sponsored theft) at a scale and velocity that overwhelms traditional AML controls. The 7,325x growth differential between CMLN inflows and centralized exchange illicit inflows since 2020 demonstrates a structural migration of criminal monetization away from regulated touchpoints and toward purpose-built laundering infrastructure. The DPRK 45-day laundering cycle, Black U services processing $1B in 236 days at 1.6-minute average transaction speed, and Chinese-language underground banking volumes exceeding $103B collectively indicate that CMLNs now function as a parallel financial system with industrial-scale throughput, specialized service differentiation, and operational resilience against law enforcement disruption.

**Confidence**: High (85/100) -- Multiple authoritative primary sources converge on consistent findings. Chainalysis provides independent blockchain analytics quantifying CMLN volume ($16.1B in 2025) and wallet counts (1,799+). TRM Labs independently corroborates Chinese-language underground banking volumes ($103B). The DPRK laundering cycle timeline is documented across both Chainalysis and TRM Labs tracing methodologies. Black U operational metrics ($1B/236 days, 1.6-min processing) are derived from on-chain transaction analysis. The 7,325x growth differential is computed from longitudinal blockchain data spanning 2020-2025.

**Estimated Impact**: CMLNs enable the monetization of an estimated $16.1B+ annually in illicit cryptocurrency proceeds. The downstream impact extends across every fraud category that touches cryptocurrency: pig butchering scams (10%+ of stolen funds laundered through CMLNs), ransomware payments, DPRK state-sponsored theft, and sanctions evasion operations. Financial institutions face direct exposure through correspondent banking relationships with exchanges that serve as CMLN off-ramp endpoints, payment processing for OTC brokers, and fiat settlement channels exploited by money movement services.

---

## Quantitative Evidence

| Statistic | Value | Source | Year |
|---|---|---|---|
| Total CMLN volume processed | $16.1B | Chainalysis | 2025 |
| Daily average CMLN throughput | ~$44M/day | Chainalysis | 2025 |
| Active CMLN wallets identified | 1,799+ | Chainalysis | 2025 |
| CMLN share of all illicit crypto laundering (5-year) | ~20% | Chainalysis | 2020-2025 |
| CMLN inflow growth vs. centralized exchange illicit inflow growth | 7,325x faster | Chainalysis | 2020-2025 |
| Chinese-language underground banking crypto volume | $103B+ (adjusted) | TRM Labs | 2025 |
| Black U single-operation volume | $1B in 236 days | Chainalysis | 2025 |
| Black U average transaction processing time | 1.6 minutes | Chainalysis | 2025 |
| Pig butchering funds laundered via CMLNs | 10%+ of stolen funds | Chainalysis | 2025 |
| DPRK full laundering cycle duration | 45 days | Chainalysis / TRM Labs | 2025 |
| DPRK distancing phase | 1-5 days | Chainalysis | 2025 |
| DPRK integration phase | 5-14 days | Chainalysis | 2025 |
| DPRK off-ramping phase | 20-45 days | Chainalysis | 2025 |

---

## CMLN Service Type Taxonomy

The following table documents the six primary CMLN service types identified through blockchain analytics and underground marketplace intelligence.

| Service Type | Description | Volume / Operational Metrics | Detection Indicators |
|---|---|---|---|
| **Running Point Brokers** | Individuals who physically collect and distribute cash at designated locations, converting crypto to fiat and vice versa. Operate as the human interface layer between digital laundering networks and the physical cash economy. | High transaction frequency with small-to-medium denominations; geographically clustered wallet activity patterns | Repeated wallet-to-cash conversion at consistent geographic nodes; burst transaction patterns tied to physical handoff schedules; wallets receiving from multiple illicit upstream sources within narrow time windows |
| **Money Mules** | Recruited individuals (witting or unwitting) who provide personal bank accounts and crypto wallets to receive, hold, and forward illicit funds. Function as disposable identity layers in the laundering chain. | High wallet turnover; short wallet lifespan (days to weeks); many wallets with single-use patterns | Rapid wallet creation/abandonment cycles; wallets with short active lifespans receiving from known CMLN clusters; forwarding patterns where 90%+ of received funds are moved within 24-48 hours |
| **OTC (Over-the-Counter) Services** | Unlicensed brokers operating outside regulated exchanges, facilitating large-volume crypto-to-crypto and crypto-to-fiat conversions with minimal or no KYC. Often embedded in Telegram groups and encrypted messaging channels. | Large individual transaction sizes ($10K-$1M+); high aggregate daily volume; persistent wallet infrastructure | Wallets with high-value, low-frequency transaction patterns; direct interactions with wallets flagged across multiple illicit categories; advertising on Telegram/dark web with no KYC requirements |
| **Black U Services** | Specialized USDT (Tether) laundering operations that convert "dirty" USDT to "clean" USDT through rapid chain-hopping and wallet layering. Named for "black USDT" (illicit-origin stablecoins). A single operation processed $1B in 236 days. | $1B/236 days documented; 1.6-minute average processing time; near-real-time throughput | Ultra-fast transaction velocity (sub-2-minute processing); high-volume USDT-specific wallet clusters; cross-chain bridge usage immediately following receipt; wallet addresses appearing on multiple chain analytics blacklists simultaneously |
| **Gambling Platforms** | Online gambling sites (often unlicensed) used to commingle illicit crypto with legitimate gambling flows. Deposits of dirty crypto are "won back" as ostensibly legitimate gambling winnings. | Variable volume; designed to obscure origin through commingling with legitimate gambling transactions | Deposits and withdrawals with minimal actual gameplay; deposit-to-withdrawal ratios inconsistent with genuine gambling behavior; crypto gambling platforms operating without licensing in permissive jurisdictions |
| **Money Movement Services** | Full-service laundering operations that combine multiple CMLN service types into end-to-end laundering pipelines. Offer "turnkey" laundering as a service, managing the entire distancing-integration-off-ramping lifecycle. | Highest aggregate volume; multi-stage transaction chains; cross-border fiat settlement | Complex multi-hop transaction chains spanning 5+ intermediate wallets; coordinated timing patterns across wallet clusters; simultaneous fiat settlement in multiple jurisdictions; infrastructure overlap with known CMLN clusters |

---

## DPRK 45-Day Laundering Cycle

The Democratic People's Republic of Korea (DPRK) has developed a structured, repeatable laundering cycle that leverages CMLN infrastructure across three distinct phases. This cycle is documented across Chainalysis and TRM Labs tracing data and represents the most operationally mature state-sponsored laundering methodology observed.

### Phase 1: Distancing (Days 1-5)

**Objective**: Rapidly separate stolen funds from the compromise event to frustrate immediate law enforcement seizure.

- Stolen cryptocurrency is immediately split across dozens to hundreds of wallets within minutes of the initial theft
- Cross-chain bridges are used to convert stolen assets from the original chain (e.g., Ethereum) to alternative chains (e.g., Tron, Avalanche, BSC)
- Mixing services and privacy coins (Monero, Tornado Cash successor protocols) are employed to break transaction graph linkability
- Stolen tokens are swapped through decentralized exchanges (DEXs) to convert identifiable tokens to USDT or ETH
- **Infrastructure touchpoints**: Cross-chain bridges, DEX smart contracts, mixing protocol interfaces, freshly generated wallet clusters

### Phase 2: Integration (Days 5-14)

**Objective**: Layer funds through CMLN infrastructure to create sufficient transaction distance that blockchain analytics tools lose tracing confidence.

- Funds are distributed across OTC brokers and Black U services for stablecoin laundering
- Multiple rounds of wallet-to-wallet transfers create layering depth (typically 5-15 intermediate hops)
- Funds are commingled with legitimate transaction flows through gambling platforms and high-volume merchant wallets
- Time delays are introduced between transaction hops to avoid velocity-based detection triggers
- Partial amounts are routed through Chinese-language underground banking networks for fiat conversion
- **Infrastructure touchpoints**: OTC broker wallets, Black U service clusters, gambling platform deposit addresses, underground banking escrow wallets

### Phase 3: Off-Ramping (Days 20-45)

**Objective**: Convert laundered cryptocurrency to fiat currency or stable stores of value outside the blockchain analytics perimeter.

- Funds arrive at no-KYC or compromised-KYC exchange accounts for fiat conversion
- Running point brokers facilitate physical cash collection in target jurisdictions (primarily Southeast Asia)
- Money mule bank accounts receive fiat wire transfers from exchange withdrawals
- Remaining crypto holdings are consolidated into long-term storage wallets using freshly generated addresses
- Fiat proceeds are integrated into legitimate business flows through shell companies and trade-based money laundering
- **Infrastructure touchpoints**: No-KYC exchange deposit addresses, money mule bank accounts, running point broker physical networks, shell company bank accounts, long-term cold storage wallets

### Cycle Timeline Visualization

```
Day 0          Day 1-5              Day 5-14                Day 20-45
[THEFT] -----> [DISTANCING] -------> [INTEGRATION] ---------> [OFF-RAMPING]
               |                     |                        |
               |- Chain hopping      |- OTC brokers           |- No-KYC exchanges
               |- Mixing services    |- Black U services      |- Running point brokers
               |- DEX swaps          |- Gambling platforms    |- Money mule accounts
               |- Wallet splitting   |- Underground banking   |- Shell companies
               |- Bridge transfers   |- Wallet layering       |- Cold storage
```

---

## CFPF Phase Mapping

### P1 -- Initiation

**CMLN infrastructure development and service provisioning**

- CMLN operators establish wallet infrastructure, recruit money mules, and set up OTC broker networks in advance of receiving illicit funds
- Underground marketplace listings advertise laundering services with specific commission rates (typically 1-5% for high-volume operations)
- Infrastructure is pre-positioned across multiple blockchains to enable immediate cross-chain movement upon receipt of illicit funds
- Chinese-language escrow platforms establish trust relationships and reputation systems for CMLN service providers
- **Key indicator**: New wallet clusters appearing with pre-established cross-chain bridge approvals and DEX token allowances before receiving any funds

### P2 -- Execution

**Illicit fund ingestion and initial layering**

- Stolen, scammed, or otherwise illicit cryptocurrency enters the CMLN ecosystem through initial deposit wallets
- Running point brokers and OTC services begin the conversion process, splitting funds across multiple wallets and chains
- Black U services activate rapid USDT conversion pipelines, processing transactions at sub-2-minute velocity
- Gambling platforms receive deposits for commingling with legitimate transaction flows
- **Key indicator**: Sudden high-volume inflows to previously dormant wallet clusters, followed by rapid distribution to multiple downstream addresses within minutes

### P3 -- Monetization

**Value extraction through fiat conversion and asset consolidation**

- Off-ramping through no-KYC exchanges converts laundered crypto to fiat currency
- Money mule bank accounts receive wire transfers from exchange withdrawal operations
- Running point brokers execute physical cash handoffs at designated geographic nodes
- Trade-based money laundering integrates fiat proceeds into legitimate commercial flows
- **Key indicator**: Correlated fiat withdrawal patterns across multiple exchange accounts linked to the same CMLN wallet cluster

### P4 -- Reinvestment

**Proceeds recycled into criminal infrastructure and operations**

- A portion of laundered proceeds is reinvested in CMLN infrastructure expansion (new wallets, additional mule recruitment, exchange account acquisition)
- DPRK operations funnel off-ramped proceeds into weapons program financing and further cyber operation funding
- Pig butchering networks reinvest laundered funds into new scam infrastructure (domains, social media accounts, victim targeting data)
- OTC brokers use accumulated capital to increase operational float, enabling higher-volume transactions
- **Key indicator**: Wallet clusters associated with known CMLN operations receiving fresh capitalization from fiat on-ramp sources after completing laundering cycles

### P5 -- Feedback & Adaptation

**Operational security improvements and law enforcement evasion**

- CMLN operators monitor blockchain analytics company publications and law enforcement actions to identify compromised wallet infrastructure
- Wallet rotation accelerates in response to address flagging by Chainalysis, TRM Labs, or Elliptic
- New CMLN service types emerge to exploit gaps in detection coverage (e.g., Black U services emerged specifically to address USDT tracing improvements)
- Cross-chain bridge selection shifts based on which bridges implement transaction monitoring
- Underground forums share intelligence on which exchanges have strengthened KYC enforcement
- **Key indicator**: Coordinated wallet abandonment across a CMLN cluster within 24-48 hours of a blockchain analytics company publishing an address flagging update

---

## Cross-Framework Mapping

| Framework | Mapping | Notes |
|---|---|---|
| **MITRE ATT&CK** | T1583.001 (Acquire Infrastructure: Domains) | CMLN operations acquire domains for OTC broker advertising, gambling platform frontends, and escrow service interfaces |
| **MITRE ATT&CK** | T1071.001 (Application Layer Protocol: Web) | CMLN coordination occurs over web-based messaging (Telegram, encrypted chat) and web interfaces for OTC and escrow services |
| **MITRE ATT&CK** | T1048 (Exfiltration Over Alternative Protocol) | Cross-chain bridge transfers and DEX swaps function as value exfiltration across protocol boundaries |
| **MITRE ATT&CK** | T1565.003 (Data Manipulation: Runtime Data Manipulation) | Gambling platform transaction manipulation to generate synthetic "winning" records for laundered funds |
| **Group-IB Fraud Matrix** | Monetization | CMLN services directly enable the monetization phase of upstream fraud operations |
| **Group-IB Fraud Matrix** | Laundering | CMLNs are the primary infrastructure for the laundering phase across all crypto-enabled fraud types |
| **UCFF** | All domains at Level 4 | CMLN operations demonstrate advanced capability across all UCFF domains, with industrial-scale commit, assess, plan, act, monitor, report, and improve functions |

---

## Look Left / Look Right Analysis

### Look Left (Upstream Threat Activity)

Understanding what precedes CMLN activation provides early warning opportunities.

| Upstream Activity | Connection to CMLNs | Detection Opportunity |
|---|---|---|
| **Pig butchering scam execution** | 10%+ of stolen funds flow directly into CMLN infrastructure for laundering | Monitor for wallet addresses receiving funds from known pig butchering victim wallets, then forwarding to CMLN-associated clusters |
| **DPRK crypto exchange/bridge exploits** | Stolen funds enter the 45-day DPRK laundering cycle through CMLN distancing infrastructure | Track large-value theft events and correlate with subsequent cross-chain bridge activity within 1-5 day windows |
| **Ransomware payment collection** | Ransomware proceeds are routed through CMLN OTC brokers and Black U services for conversion | Monitor ransomware payment wallets for downstream transfers to known CMLN service addresses |
| **Money mule recruitment campaigns** | Telegram and dark web recruitment precedes CMLN mule network expansion | Track recruitment advertising patterns on underground platforms as leading indicators of CMLN capacity scaling |
| **No-KYC exchange account provisioning** | Bulk account creation at no-KYC exchanges precedes off-ramping phase activation | Monitor for anomalous account creation patterns at exchanges with weak KYC enforcement |

### Look Right (Downstream Consequences)

Understanding what follows CMLN operations informs impact assessment and interdiction strategy.

| Downstream Activity | Connection to CMLNs | Detection Opportunity |
|---|---|---|
| **Fiat integration into banking system** | Money mule accounts and shell companies receive fiat proceeds from CMLN off-ramping | Monitor for wire transfer patterns consistent with crypto exchange withdrawal-to-bank account flows in correspondent banking data |
| **Criminal infrastructure reinvestment** | Laundered proceeds fund new fraud campaigns, domain purchases, and infrastructure expansion | Track wallet clusters that both receive from and send to known criminal infrastructure provisioning services |
| **DPRK weapons program financing** | Off-ramped fiat from DPRK laundering cycles finances weapons and missile programs | Correlate DPRK-attributed wallet cluster activity with geopolitical intelligence on weapons development timelines |
| **Regulatory enforcement actions** | Law enforcement seizures and exchange sanctions disrupt but do not terminate CMLN operations | Monitor for infrastructure migration patterns following enforcement announcements (see TP-0045) |
| **New CMLN service type emergence** | Detection pressure on existing service types drives innovation in new laundering methodologies | Track underground marketplace listings for novel laundering services as indicators of CMLN evolution |

---

## Underground Ecosystem Context

The CMLN underground ecosystem operates as a mature, stratified marketplace with distinct service tiers, reputation systems, and operational specializations.

**Chinese-Language Underground Banking Networks**: TRM Labs documented that Chinese-language escrow and underground banking operations exceeded $103 billion in adjusted crypto volume in 2025. These networks operate through encrypted messaging platforms (primarily Telegram and WeChat) and provide full-service laundering including crypto-to-fiat conversion, cross-border fund transfers, and trade-based money laundering through shell import/export companies. The Huione Group ecosystem, with $98 billion in total crypto inflows and $4 billion confirmed illicit, functions as the largest known single-entity CMLN infrastructure provider.

**Service Pricing and Commission Structures**: CMLN operators typically charge 1-5% commission for high-volume laundering, with premium pricing for expedited processing (Black U services) and complex multi-jurisdiction off-ramping. Running point brokers charge higher commissions (5-15%) reflecting the physical risk of cash handling. OTC brokers operating through Telegram typically advertise rates of 2-4% for USDT-to-fiat conversion with no KYC requirements.

**Reputation and Trust Systems**: Underground marketplaces employ escrow systems, reputation scoring, and vouching mechanisms to establish trust between CMLN service providers and their criminal clients. Chinese-language platforms have particularly mature trust infrastructure, with multi-level escrow and dispute resolution mechanisms that mirror legitimate e-commerce platforms.

**Operational Security Practices**: CMLN operators employ wallet rotation schedules (typically 7-30 day lifespans per wallet), cross-chain bridge diversification to avoid single-point monitoring, and real-time monitoring of blockchain analytics company flagging activity. Advanced CMLN operations maintain "clean" wallet reserves that have never interacted with flagged addresses, deploying them only when existing infrastructure is compromised.

**Geographic Concentration**: CMLN operations are concentrated in jurisdictions with weak or non-existent crypto regulation, particularly Southeast Asia (Cambodia, Myanmar, Laos), certain Middle Eastern jurisdictions, and Eastern European countries with limited law enforcement cooperation. Running point broker networks are geographically clustered in major urban centers within these jurisdictions.

---

## Controls & Mitigations

| Control ID | Control Description | CFPF Phase | Implementation Notes |
|---|---|---|---|
| CM-0049-01 | Deploy blockchain analytics platforms (Chainalysis, TRM Labs, Elliptic) with CMLN wallet cluster databases integrated into transaction monitoring | P2, P3 | Requires real-time API integration with blockchain analytics providers; update wallet flagging databases at minimum daily frequency |
| CM-0049-02 | Implement cross-chain transaction monitoring covering bridge transfers between Ethereum, Tron, BSC, Avalanche, and Solana | P1, P2 | Cross-chain bridges are primary distancing infrastructure; monitor for bridge transactions originating from or destined to flagged wallet clusters |
| CM-0049-03 | Establish velocity-based transaction alerts for USDT transfers with sub-5-minute processing times across multiple wallets | P2 | Targets Black U service operational signatures; calibrate thresholds against baseline legitimate transaction velocity (see BL-0027) |
| CM-0049-04 | Monitor no-KYC exchange deposit addresses for correlation with known CMLN off-ramping wallet clusters | P3 | Requires maintained list of no-KYC exchanges and their known deposit address ranges; cross-reference with CMLN wallet cluster databases |
| CM-0049-05 | Implement correspondent banking transaction monitoring for wire transfers originating from crypto exchange withdrawal flows | P3, P4 | Detect fiat integration touchpoints where CMLN off-ramping intersects with traditional banking infrastructure |
| CM-0049-06 | Deploy DNS and hosting infrastructure monitoring for OTC broker advertising domains and gambling platform frontends | P1, P2 | Track domain registration patterns, hosting provider selection, and DNS changes associated with CMLN service infrastructure |
| CM-0049-07 | Establish information-sharing protocols with blockchain analytics companies for real-time CMLN wallet cluster intelligence | P1-P5 | Participate in Chainalysis Reactor and TRM Labs collaborative intelligence sharing; enable bidirectional flagging |
| CM-0049-08 | Implement gambling platform transaction pattern analysis to detect deposit/withdrawal patterns inconsistent with genuine gambling behavior | P2, P3 | Flag accounts with high deposit-to-withdrawal ratios, minimal gameplay, and deposits from flagged wallet clusters |

---

## UCFF Alignment

| UCFF Domain | Level | Justification |
|---|---|---|
| **Commit** | Level 4 | CMLN operations demonstrate sustained organizational commitment with dedicated infrastructure, personnel, and capital investment across all six service types |
| **Assess** | Level 4 | CMLN operators actively monitor blockchain analytics flagging, law enforcement actions, and exchange KYC enforcement to assess operational risk and adjust infrastructure |
| **Plan** | Level 4 | The DPRK 45-day laundering cycle demonstrates structured, multi-phase planning with pre-positioned infrastructure and defined timelines for each phase |
| **Act** | Level 4 | Industrial-scale execution with $44M/day throughput, 1.6-minute Black U processing times, and 1,799+ active wallets indicates highly developed operational capability |
| **Monitor** | Level 4 | Real-time monitoring of blockchain analytics company publications, exchange compliance updates, and law enforcement activity informs operational security decisions |
| **Report** | Level 4 | Underground marketplace reputation systems, escrow dispute resolution, and commission accounting demonstrate structured reporting and accountability mechanisms |
| **Improve** | Level 4 | The emergence of new service types (Black U services) in response to detection improvements, and the 7,325x growth rate, demonstrate continuous operational improvement |

---

## Detection Approaches

### On-Chain Detection (DL-0113)

**Wallet Cluster Analysis**

- Identify wallet clusters exhibiting CMLN behavioral signatures: high transaction frequency, short wallet lifespans, rapid forwarding patterns (90%+ of received funds moved within 24-48 hours)
- Cross-reference wallet clusters against Chainalysis, TRM Labs, and Elliptic flagging databases for known CMLN associations
- Monitor for wallet clusters with pre-established cross-chain bridge approvals and DEX token allowances before receiving initial funding (pre-positioned infrastructure indicator)
- Baseline transaction velocity against BL-0027 thresholds to identify Black U service operational signatures (sub-2-minute processing)

**Cross-Chain Bridge Monitoring**

- Track bridge transactions originating from wallets with known illicit-source inflows within the 1-5 day distancing window
- Monitor for sequential bridge transfers across multiple chains within compressed timeframes (DPRK distancing phase pattern)
- Flag bridge transactions where the destination chain wallet immediately initiates further distribution to multiple downstream addresses

**Transaction Graph Analysis**

- Apply graph analytics to identify layering patterns consistent with CMLN integration phase operations (5-15 intermediate hops with time delays between transfers)
- Detect commingling patterns where illicit-origin funds merge with legitimate transaction flows at gambling platform or high-volume merchant wallets
- Identify coordinated wallet abandonment events (multiple wallets in a cluster ceasing activity within 24-48 hours) as indicators of CMLN infrastructure rotation

**Stablecoin-Specific Monitoring**

- Focus USDT/USDC transaction monitoring on high-velocity, high-volume patterns consistent with Black U service operations
- Monitor for USDT transfers between wallets where both sender and receiver have no prior transaction history with legitimate services
- Track stablecoin flows through wallets that interact exclusively with other flagged or unattributed wallets (closed-loop CMLN networks)

### DNS / Hosting Infrastructure Detection (DL-0114)

**OTC Broker Domain Monitoring**

- Monitor domain registration patterns for keywords associated with OTC broker advertising: "otc," "exchange," "swap," "nokyc," "instant," "cashout"
- Track bulk domain registration events from registrars commonly used by CMLN operators (privacy-enabled registrars, bulletproof registrars)
- Identify domain clusters sharing hosting infrastructure (IP ranges, ASNs, nameservers) with known CMLN-associated domains
- Monitor for domains resolving to hosting providers in jurisdictions with weak law enforcement cooperation (Cambodia, Myanmar, certain Eastern European providers)

**Gambling Platform Infrastructure Detection**

- Identify unlicensed gambling platform domains through certificate transparency log monitoring and web crawling
- Track gambling platform domains that accept cryptocurrency deposits but lack legitimate gambling licenses in any jurisdiction
- Monitor for gambling platform infrastructure sharing hosting resources with known CMLN service domains

**Telegram and Messaging Platform Monitoring**

- Track Telegram channels and groups advertising OTC services, money mule recruitment, and laundering services
- Monitor for Telegram bot infrastructure used to automate CMLN transaction coordination and customer communication
- Identify advertising domains linked from Telegram CMLN service channels for infrastructure correlation

**Hosting Provider and ASN Analysis**

- Monitor ASNs and hosting providers known to host CMLN-associated infrastructure for new domain provisioning
- Track hosting migrations where CMLN service domains move between providers in response to takedown actions
- Identify shared hosting fingerprints (SSL certificate patterns, server software configurations, response headers) across CMLN infrastructure clusters
- Correlate DNS resolution changes with known law enforcement actions or blockchain analytics flagging events as indicators of infrastructure rotation

### Behavioral Detection Patterns

**DPRK Laundering Cycle Detection**

- Monitor for the three-phase temporal pattern: rapid wallet splitting within 1-5 days of a major crypto theft (distancing), followed by OTC/Black U service interaction within 5-14 days (integration), followed by no-KYC exchange deposits within 20-45 days (off-ramping)
- Correlate major crypto theft/exploit events with subsequent cross-chain bridge activity matching DPRK distancing phase signatures
- Track wallet clusters exhibiting the full 45-day lifecycle pattern across multiple laundering cycles

**Pig Butchering Laundering Correlation**

- Monitor for funds flowing from known pig butchering victim wallets into CMLN-associated wallet clusters
- Track the 10%+ of pig butchering proceeds entering CMLN infrastructure as a correlation point between upstream fraud and downstream laundering

---

## References

1. Chainalysis. "Crypto Crime Mid-Year 2025 Update." Chainalysis Blog, 2025. https://www.chainalysis.com/blog/crypto-crime-midyear-2025/
2. Chainalysis. "2025 Crypto Crime Report: Cryptocurrency Money Laundering Networks." Chainalysis, 2025.
3. TRM Labs. "Illicit Crypto Ecosystem Report 2025." TRM Labs, 2025.
4. TRM Labs. "Chinese-Language Underground Banking and Crypto Volume Analysis." TRM Labs Research, 2025.
5. CrimsonVector. "Strategic Intelligence Report: Cryptocurrency Laundering Infrastructure and CMLN Operations." CrimsonVector, 2026.
6. Chainalysis. "DPRK Cryptocurrency Theft and Laundering Lifecycle Analysis." Chainalysis Research, 2025.
7. Chainalysis. "Black U Services: Industrial-Scale USDT Laundering Operations." Chainalysis Blog, 2025.
8. FLAME Project. "TP-0044: State-Criminal Infrastructure Convergence." FLAME Threat Path Library, 2026.
9. FLAME Project. "TP-0045: Sanctions Evasion via Fraud Infrastructure." FLAME Threat Path Library, 2026.
10. FLAME Project. "TP-0047: Related Threat Path." FLAME Threat Path Library, 2026.
11. FLAME Project. "DL-0113: On-Chain CMLN Detection Logic." FLAME Detection Library, 2026.
12. FLAME Project. "DL-0114: DNS/Hosting CMLN Infrastructure Detection Logic." FLAME Detection Library, 2026.
13. FLAME Project. "BL-0027: Cryptocurrency Transaction Velocity Baseline." FLAME Baseline Library, 2026.

---

## Analyst Notes

- **CMLN growth trajectory**: The 7,325x growth differential between CMLN inflows and centralized exchange illicit inflows since 2020 represents a fundamental structural shift in how criminal actors monetize crypto-enabled fraud. This trend is accelerating, not stabilizing, and suggests that AML controls focused primarily on centralized exchange monitoring are increasingly insufficient.
- **Black U services as an indicator of professionalization**: The emergence of Black U services -- processing $1B in 236 days with 1.6-minute average transaction times -- represents a qualitative leap in CMLN operational capability. This is industrial-scale laundering infrastructure that rivals the throughput of legitimate payment processors.
- **Chinese-language ecosystem scale**: The $103B figure from TRM Labs for Chinese-language underground banking crypto volume likely understates actual throughput due to the inherent difficulty of tracking private, peer-to-peer transactions conducted through encrypted messaging platforms. This ecosystem represents a parallel financial infrastructure that is deeply intertwined with transnational organized crime.
- **Detection gap**: Current blockchain analytics tools are effective at identifying known CMLN wallet clusters but struggle with newly provisioned infrastructure and closed-loop CMLN networks where all participants are unattributed. DNS/hosting infrastructure monitoring (DL-0114) provides a complementary detection layer that can identify CMLN service infrastructure before it processes its first transaction.
- **DPRK cycle regularity**: The consistency of the 45-day laundering cycle across multiple DPRK operations suggests a standardized operational playbook. This regularity creates a detection opportunity -- but the window for interdiction is narrow, particularly during the 1-5 day distancing phase when cross-chain bridge monitoring is most critical.
- **Regulatory implications**: CMLNs operate in a regulatory gap between traditional AML/BSA requirements (which apply to regulated financial institutions) and the largely unregulated crypto infrastructure layer. Effective disruption requires coordination between blockchain analytics, DNS/hosting infrastructure monitoring, and traditional financial intelligence.

---

## Revision History

| Date | Version | Author | Changes |
|---|---|---|---|
| 2026-03-05 | 1.0 | FLAME Project | Initial publication based on CrimsonVector Strategic Intelligence Report, Chainalysis, and TRM Labs data |
