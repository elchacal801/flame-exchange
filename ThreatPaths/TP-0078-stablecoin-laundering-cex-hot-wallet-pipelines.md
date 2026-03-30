# TP-0078: Stablecoin Laundering via Centralized Exchange Hot Wallet Pipelines

```yaml
---
id: TP-0078
title: "Stablecoin Laundering via Centralized Exchange Hot Wallet Pipelines"
category: ThreatPath
date: 2026-03-30
author: "FLAME Project"
source: "ICIJ Coin Laundry Investigation (2024-2025); FinCEN Huione Group Designation (May 2025); ICIJ/OpenCorporates 'The Modern Money Trail' Webinar (2026)"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - crypto-laundering
  - crypto-laundering-infrastructure
  - money-laundering
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
confidence_score: 82
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1657      # Financial Theft
  - T1583.001  # Acquire Infrastructure: Domains
  - T1036      # Masquerading
ft3_tactics:
  - FTA007     # Money Laundering
  - FTA003     # Identity/Document Fraud (shell entity formation)
mitre_f3: []
groupib_stages:
  - "Resource Development"
  - "Initial Access"
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
  - id: TP-0055
    relationship: related-to
  - id: TP-0049
    relationship: related-to
  - id: TP-0045
    relationship: related-to
  - id: TP-0058
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-AML
  - REG-FATF-R16
  - REG-FINCEN-HUIONE-311
  - REG-OFAC-CRYPTO-2021
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - stablecoin-laundering
  - tron-usdt
  - hot-wallet-sweep
  - cex-pipeline
  - huione-group
  - proof-of-reserves
  - crypto-to-cash
  - exchange-attribution
  - laundering-as-a-service
  - icij-coin-laundry
  - fincen-311
  - shell-company-convergence
  - beneficial-ownership-gap
---
```

## Summary

Criminal conglomerates are operating industrialized cryptocurrency laundering services that process hundreds of millions of dollars through centralized exchange (CEX) hot wallet pipelines. Unlike the narco-terror Ponzi convergence model documented in TP-0055, this threat path describes a distinct operational model: a criminal organization that builds and operates a full-service laundering infrastructure — issuing its own stablecoin, running its own exchange, and routing proceeds through major centralized exchanges via traceable deposit-to-hot-wallet sweep patterns.

The Huione Group, a Cambodian financial conglomerate designated by FinCEN as a primary money laundering concern in May 2025, is the paradigm case. ICIJ's year-long "Coin Laundry" investigation documented at least $408 million flowing from Huione-controlled TRON addresses to Binance and at least $226 million to OKX over approximately one year (July 2024 to July 2025). The group operated Huione Pay (a cryptocurrency exchange) and issued its own stablecoin (USDH) deployed across four major blockchains: Ethereum, TRON, Binance Smart Chain, and Solana. TRON/USDT was identified as the dominant rail for Southeast Asian fraud compound money laundering due to speed and low transaction fees.

Critically, neither Binance nor OKX demonstrably curtailed their transaction volume with Huione following their own DOJ plea agreements (Binance: November 2023; OKX: February 2025), indicating that plea-deal compliance commitments did not immediately translate into effective flow interdiction.

The convergence of this laundering infrastructure with offshore shell company opacity (see DL-0198) and unlicensed crypto-to-cash desk operations (see DL-0197) creates a complete end-to-end pipeline from illicit proceeds to usable physical currency.

**Key Distinction from TP-0055**: TP-0055 covers narco-terror organizations using crypto Ponzi schemes to launder drug/extortion proceeds — the criminal actors *using* crypto as a laundering tool. TP-0078 covers the *industrialized laundering service provider* model — a criminal conglomerate offering laundering-as-a-service at scale via its own stablecoin and exchange infrastructure, serving multiple criminal actor types including SE Asian scam compounds.

**Key Distinction from TP-0049**: TP-0049 covers cryptocurrency laundering infrastructure broadly. TP-0078 provides the specific operational pattern of the stablecoin-to-CEX hot wallet pipeline, including the 2-hop attribution methodology and Proof-of-Reserves cross-referencing technique.

## Threat Path Hypothesis

> **Hypothesis**: Criminal conglomerates have discovered that operating a full laundering ecosystem — own stablecoin + own exchange + CEX off-ramp pipeline — provides superior operational security and throughput compared to ad-hoc mixing or chain-hopping. The issuance of a proprietary stablecoin (e.g., USDH) across multiple blockchains enables the operator to control the entire funds flow from initial receipt to CEX deposit. TRON's low fees and high throughput make it the preferred rail for bulk stablecoin transfers. The 2-hop hot wallet sweep pattern (illicit address -> CEX deposit wallet -> CEX hot wallet) is publicly observable on-chain but exploits the fact that: (a) major exchanges' compliance teams do not systematically monitor inbound flows against public illicit wallet databases, and (b) post-plea-deal compliance improvements are slow to operationalize. The public availability of exchange Proof-of-Reserves data and Arkham Intelligence illicit wallet tags means this pipeline is detectable by external observers — the attribution deficit that protects these flows is not inherent to the blockchain but reflects inadequate monitoring by the exchanges themselves.

**Confidence**: High — ICIJ documented specific dollar amounts ($408M Binance, $226M OKX) through reproducible blockchain tracing methodology. FinCEN formally designated Huione Group in May 2025. Both Binance and OKX DOJ plea deals are public record. ICIJ methodology was independently reproduced by external blockchain analysts prior to publication.

**Estimated Impact**: $634 million minimum confirmed flows to two exchanges over approximately one year. Broader Huione Group laundering volume estimated in the billions. FinCEN designation reflects assessment that Huione Group is among the largest cryptocurrency money laundering operations ever documented.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Laundering infrastructure establishment | Criminal conglomerate establishes cryptocurrency exchange (Huione Pay), registers in permissive jurisdiction (Cambodia), builds technical infrastructure for stablecoin issuance | New exchange registration in SE Asian jurisdiction with minimal regulatory oversight; stablecoin smart contract deployment across multiple blockchains (ETH, TRON, BSC, SOL) |
| Exchange vulnerability assessment | Operator identifies major CEX platforms with weak inbound flow monitoring or slow post-plea compliance implementation | Concentration of test transactions to specific exchanges; monitoring of exchange compliance announcements and DOJ settlement timelines |
| Shell company infrastructure | Registration of corporate entities in opacity-friendly jurisdictions to hold exchange accounts and provide beneficial ownership obfuscation | LLC registrations in Wyoming, BVI, Seychelles linked to exchange operator principals; registered agent services at high-concentration addresses (see DL-0198) |

**Data Sources**: Corporate registry monitoring (OpenCorporates bulk data), blockchain smart contract deployment monitoring, SE Asian exchange licensing databases

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Criminal client onboarding | SE Asian scam compounds, fraud networks, and other criminal actors are onboarded to the laundering service; TRON selected as primary operating rail | New wallet addresses receiving funds from known scam compound wallet clusters; Huione Pay account creation patterns correlated with scam compound operational timelines |
| Multi-chain stablecoin deployment | Proprietary stablecoin (USDH) deployed across ETH, TRON, BSC, SOL to offer clients chain flexibility | Smart contract deployment for new stablecoin token on multiple chains within compressed timeframe; identical contract code or ownership across deployments |
| Victim funds ingestion | Fraud proceeds from pig butchering, investment scams, romance scams, and other schemes deposited to laundering service wallets | Inbound USDT flows from wallets previously associated with known scam typologies; wallet addresses appearing in victim complaint databases or Arkham illicit tags |

**Target**: SE Asian scam compound operators, fraud network principals, sanctioned entities seeking off-ramp services

**Data Sources**: Blockchain analytics, Arkham Intelligence illicit tag database, victim complaint correlation, scam compound intelligence (TP-0058)

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Fund aggregation across victim wallets | Proceeds from multiple fraud victims consolidated from individual scam wallets into operator-controlled aggregation wallets | Fan-in pattern: multiple small-to-medium USDT transfers converging on a single wallet within 24-48h; source wallets have short operational histories |
| Stablecoin conversion and layering | Funds converted between USDT, USDC, and proprietary stablecoin (USDH) to complicate tracing; cross-chain bridges used for additional layering | Stablecoin swap transactions on DEXs; cross-chain bridge transfers (TRON -> ETH, BSC -> SOL); conversion to/from proprietary stablecoin |
| Wallet address rotation | Fresh deposit addresses generated for each batch to prevent address-based blocking by exchanges | High-velocity wallet address generation; deposit addresses used once or twice then abandoned; addresses not appearing in any attribution database |

**Data Sources**: Blockchain transaction monitoring, DEX swap analytics, cross-chain bridge monitoring, wallet age/transaction history analysis

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Bulk USDT transfer to CEX deposit wallets | Large USDT transfers from aggregation wallets to individual deposit wallets associated with major exchanges (Binance, OKX) | USDT transfers >= $10,000 from high-risk-scored wallets to addresses appearing in exchange Proof-of-Reserves datasets; destination addresses subsequently swept to known exchange hot wallets |
| Hot wallet sweep confirmation | CEX automatically sweeps deposit wallet contents into institutional hot wallet, confirming exchange receipt of funds — the 2-hop pattern | Hop 1: illicit wallet -> CEX deposit address; Hop 2: deposit address -> CEX hot wallet (observable on-chain within 24h); both hops confirmable via public blockchain data |
| Volume distribution across exchanges | Operator distributes laundering volume across multiple exchanges to stay below individual exchange monitoring thresholds | Parallel high-value USDT flows from same source wallet cluster to deposit addresses at different exchanges within compressed timeframe |

**Data Sources**: Tronscan API, Arkham Intelligence API, exchange Proof-of-Reserves CSVs (Binance, OKX, Bybit), blockchain analytics platforms

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CEX fiat off-ramp | Once funds are in exchange hot wallets, operator or associates convert to fiat currency through exchange withdrawal | Fiat withdrawal requests from accounts with deposit history matching illicit flow patterns; withdrawals to bank accounts in high-risk jurisdictions |
| Crypto-to-cash desk conversion | Parallel off-ramp through unlicensed OTC desks in Dubai, Eastern Europe, and SE Asia that convert USDT to physical cash with minimal KYC | USDT transfers to ephemeral wallet addresses (< 7 days old, < 3 prior transactions) not attributed in any analytics database; geographic clustering in known OTC hub cities (see DL-0197) |
| Re-investment in criminal operations | Cleaned proceeds fund further scam compound operations, real estate purchases, luxury goods, or reinvestment in laundering infrastructure | Fiat flows from exchange withdrawal accounts to known scam compound operating accounts; real estate purchases by shell entities linked to exchange operator network |

**Data Sources**: Exchange withdrawal monitoring, fiat off-ramp transaction analysis, OTC desk intelligence, real estate registry monitoring, shell company network analysis

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA007: Money Laundering — stablecoin conversion, CEX hot wallet pipeline, crypto-to-cash desk off-ramp
- FTA003: Identity/Document Fraud — shell entity formation for exchange accounts and beneficial ownership obfuscation

**MITRE ATT&CK:**
- T1657: Financial Theft — proceeds laundering through cryptocurrency infrastructure
- T1583.001: Acquire Infrastructure: Domains — exchange platform registration, stablecoin smart contract deployment
- T1036: Masquerading — legitimate exchange transaction patterns used to mask illicit flows

**Group-IB Fraud Matrix:**
- Resource Development -> Initial Access -> Perform Fraud -> Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P4** — typically discovered when blockchain analysts identify the 2-hop hot wallet sweep pattern linking flagged wallets to exchange deposit addresses. The Huione case was discovered through Arkham Intelligence's illicit wallet tag database, followed by open-source confirmation via Chinese-language financial statements published by Huione subsidiaries.

**Look Left** (what did you miss before discovery?):

- P1: Stablecoin smart contract deployment across 4 blockchains (ETH, TRON, BSC, SOL) by a single entity — observable on-chain before any illicit transactions
- P1: Shell company registrations in Cambodia and opacity-friendly jurisdictions associated with exchange operator principals
- P2: Wallet addresses receiving funds from known scam compound clusters — Arkham illicit tag correlation available before exchange deposit
- P3: Fan-in aggregation pattern in TRON wallets — multiple small victim deposits consolidating into operator wallets — visible in blockchain data before off-ramp

**Look Right** (what comes next after discovery?):

- P5: Exchange-side investigation required — which accounts received the deposit wallet funds? Were fiat withdrawals already processed?
- P5: Crypto-to-cash desk identification — parallel off-ramp channels likely active; unlicensed OTC desks generating ephemeral wallets remain in analytics dark space
- Post-discovery: FinCEN 311 designation may follow (as occurred with Huione Group in May 2025), triggering correspondent banking restrictions
- Post-discovery: Criminal actors will migrate to alternative laundering infrastructure — monitor for new stablecoin deployments and exchange account creation patterns from related wallet clusters

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Laundering service operator | Full-stack crypto laundering (own stablecoin + exchange + CEX pipeline) | Low (requires significant capital and technical capability) | Commission-based (2-5% of laundered volume) |
| Scam compound operator | Generates fraud proceeds requiring laundering | High (SE Asian compound ecosystem well-documented) | Revenue share with laundering service |
| Shell company registrant | Provides corporate vehicles for exchange accounts and ownership obfuscation | High (Wyoming/BVI/Seychelles formation services widely available) | USD 500-5,000 per entity |
| Crypto-to-cash desk operator | Converts USDT to physical currency at unlicensed OTC locations | Medium (Dubai, Eastern Europe, SE Asia hubs) | 3-8% commission |
| Exchange account facilitator | Provides verified exchange accounts or KYC documentation for account opening | Medium | USD 200-2,000 per account |

### Intelligence Sources
- ICIJ, "Coin Laundry" investigation series (2024-2025)
- ICIJ/OpenCorporates, "The Modern Money Trail: Crypto & Cash" webinar (2026)
- FinCEN, Huione Group 311 Designation (May 2025)
- Binance DOJ Plea Agreement (November 2023)
- OKX DOJ Plea Agreement (February 2025)
- Arkham Intelligence illicit wallet tag database
- Exchange Proof-of-Reserves publications (Binance, OKX, Bybit)

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor stablecoin smart contract deployments across major chains — flag new stablecoins from unregistered issuers deploying on 3+ chains simultaneously | Detective | Blockchain Intelligence |
| P2 | Arkham Intelligence and OFAC illicit wallet tag monitoring — cross-reference inbound deposit addresses against known illicit/suspicious wallet databases before crediting accounts | Preventive | Exchange Compliance |
| P3 | Fan-in aggregation detection — flag wallets receiving from 10+ distinct source wallets within 48h where source wallets have < 30-day history | Detective | AML |
| P4 | Proof-of-Reserves-based inbound flow monitoring — cross-reference all inbound deposits > $10,000 against internal deposit address list and flag sources with risk score >= 70 (see DL-0196) | Detective | AML |
| P4 | Hot wallet sweep correlation — when deposit address receives from flagged source, trace the subsequent hot wallet sweep to confirm receipt and trigger enhanced review | Detective | AML |
| P4 | Multi-exchange flow correlation — share flagged wallet cluster data across exchanges via industry intelligence sharing (FinCEN SAR, FS-ISAC) to detect volume distribution patterns | Detective | AML |
| P5 | Fiat withdrawal holds on accounts with deposit patterns matching illicit flow indicators — require enhanced verification before fiat off-ramp | Preventive | Compliance |
| P5 | Crypto-to-cash desk pattern detection — flag USDT transfers to ephemeral wallets not attributed in any analytics database (see DL-0197) | Detective | AML |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive recognition that CEX platforms are active laundering conduits; investment in blockchain analytics and Proof-of-Reserves monitoring |
| ASSESS | Level 3 (Established) | Risk assessment covers stablecoin laundering pipeline as distinct threat; exchange-specific inbound flow risk model |
| PLAN | Level 3 (Established) | Playbooks for hot wallet sweep correlation; FinCEN 311 designation response procedures; inter-exchange intelligence sharing protocols |
| ACT | Level 4 (Advanced) | Real-time blockchain monitoring with Proof-of-Reserves cross-referencing; Arkham/OFAC wallet tag integration; 2-hop sweep detection automation |
| MONITOR | Level 4 (Advanced) | KRIs for inbound illicit flow volume, deposit-to-hot-wallet sweep timing, ephemeral wallet transfer patterns; exchange-level flow concentration metrics |
| REPORT | Level 3 (Established) | Dual SAR filing (laundering + predicate fraud); FinCEN referral for potential 311 designation targets; inter-exchange intelligence sharing |
| IMPROVE | Level 3 (Established) | Post-designation review of detection effectiveness; Proof-of-Reserves address list refresh cycle; Arkham tag integration update cadence |

---

## Detection Approaches

### Queries / Rules

**Hot Wallet Sweep Attribution (SQL) — DL-0196**

```sql
-- Detect 2-hop pattern: flagged source -> deposit address -> hot wallet
WITH flagged_deposits AS (
  SELECT
    t1.transaction_hash AS deposit_tx,
    t1.from_address AS source_wallet,
    t1.to_address AS deposit_address,
    t1.amount_usd,
    t1.token_symbol,
    t1.chain,
    t1.block_timestamp AS deposit_time,
    w.risk_score AS source_risk_score,
    w.tags AS source_tags
  FROM transactions t1
  JOIN wallet_risk w ON t1.from_address = w.wallet_address
  WHERE t1.token_symbol IN ('USDT', 'USDC')
    AND t1.amount_usd >= 10000
    AND w.risk_score >= 70
    AND t1.block_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
),
sweep_events AS (
  SELECT
    t2.from_address AS deposit_address,
    t2.to_address AS hot_wallet,
    t2.block_timestamp AS sweep_time,
    hw.exchange_name
  FROM transactions t2
  JOIN exchange_hot_wallets hw ON t2.to_address = hw.wallet_address
  WHERE t2.block_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
SELECT
  fd.source_wallet,
  fd.deposit_address,
  se.hot_wallet,
  se.exchange_name,
  fd.amount_usd,
  fd.token_symbol,
  fd.chain,
  fd.source_risk_score,
  fd.source_tags,
  fd.deposit_time,
  se.sweep_time,
  EXTRACT(EPOCH FROM (se.sweep_time - fd.deposit_time))/3600 AS hours_to_sweep
FROM flagged_deposits fd
JOIN sweep_events se ON fd.deposit_address = se.deposit_address
WHERE se.sweep_time > fd.deposit_time
  AND se.sweep_time < fd.deposit_time + INTERVAL '24 hours'
ORDER BY fd.amount_usd DESC;
```

**Ephemeral Wallet OTC Desk Detection (SQL) — DL-0197**

```sql
-- Detect crypto-to-cash desk patterns: ephemeral wallets receiving from multiple sources
SELECT
  t.to_address AS desk_wallet,
  COUNT(DISTINCT t.from_address) AS unique_senders,
  SUM(t.amount_usd) AS total_volume_usd,
  MIN(t.block_timestamp) AS first_tx,
  MAX(t.block_timestamp) AS last_tx,
  w.first_seen_date,
  w.total_transaction_count,
  CASE
    WHEN w.total_transaction_count < 3 AND w.first_seen_date > CURRENT_DATE - 7 THEN 'ephemeral'
    ELSE 'established'
  END AS wallet_age_class,
  CASE
    WHEN por.wallet_address IS NOT NULL THEN 'CEX_ATTRIBUTED'
    WHEN ark.wallet_address IS NOT NULL THEN 'ARKHAM_ATTRIBUTED'
    ELSE 'UNATTRIBUTED'
  END AS attribution_status
FROM transactions t
JOIN wallet_metadata w ON t.to_address = w.wallet_address
LEFT JOIN proof_of_reserves por ON t.to_address = por.wallet_address
LEFT JOIN arkham_attributions ark ON t.to_address = ark.wallet_address
WHERE t.token_symbol = 'USDT'
  AND t.chain = 'TRON'
  AND t.block_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY t.to_address, w.first_seen_date, w.total_transaction_count,
         por.wallet_address, ark.wallet_address
HAVING COUNT(DISTINCT t.from_address) >= 5
  AND w.total_transaction_count < 3
  AND w.first_seen_date > CURRENT_DATE - 7
  AND por.wallet_address IS NULL
  AND ark.wallet_address IS NULL
ORDER BY total_volume_usd DESC;
```

### Behavioral Analytics

- 2-hop hot wallet sweep: source wallet (risk score >= 70) -> exchange deposit address -> exchange hot wallet within 24h — confirms exchange receipt of flagged funds
- Fan-in aggregation: 10+ distinct wallets sending to single wallet within 48h, where source wallets have < 30 days of history — indicates laundering aggregation phase
- Ephemeral wallet cluster: group of wallets (age < 7d, < 3 transactions each) receiving USDT from diverse sources, not attributed in any analytics database — indicates OTC desk operation
- Volume distribution: same source wallet cluster sending comparable amounts to deposit addresses at 3+ different exchanges within 72h — indicates multi-exchange laundering distribution
- Post-plea volume persistence: exchange continues receiving comparable volume from designated/flagged entities after DOJ plea agreement or FinCEN designation — indicates compliance implementation gap

### Cross-Team Correlation

- **AML + Blockchain Intelligence**: Proof-of-Reserves address lists from major exchanges must be maintained and updated quarterly; cross-reference all flagged inbound flows against current PoR datasets
- **AML + Exchange Compliance**: When 2-hop sweep pattern confirmed, immediate account-level investigation required — identify account holder, review KYC documentation, assess fiat withdrawal history
- **Fraud + Scam Compound Intelligence**: Correlate inbound wallet addresses against TP-0058 scam compound wallet databases — inbound flows from compound-linked wallets indicate the predicate fraud type
- **Compliance + Legal**: FinCEN 311 designation of laundering service operators triggers correspondent banking restrictions — monitor FinCEN advisories and implement blocking within 24h of designation

---

## Operational Evidence

### EV-TP0078-2026-001: Huione Group — ICIJ Coin Laundry Investigation

- **Source**: ICIJ "Coin Laundry" investigation series (published November 2024 onwards); ICIJ/OpenCorporates "The Modern Money Trail" webinar (2026)
- **Geography**: Cambodia (Huione Group HQ); SE Asian scam compound ecosystem; global exchange infrastructure (Binance, OKX)
- **Amount**: At least $408 million to Binance (July 2024 – July 2025); at least $226 million to OKX (post-February 2025 plea deal)
- **Entity**: Huione Group — Cambodian financial conglomerate operating Huione Pay exchange and USDH stablecoin across ETH, TRON, BSC, SOL
- **CFPF Phase Coverage**: P1, P2, P3, P4, P5
- **Confidence**: High (ICIJ methodology: Tronscan/Arkham API tracing, Proof-of-Reserves cross-referencing, hot wallet sweep confirmation, independent expert reproduction prior to publication)
- **Summary**: ICIJ traced hundreds of millions of dollars from Huione Group TRON addresses into Binance and OKX deposit wallets using the 2-hop hot wallet sweep methodology. The initial Huione wallet attribution was sourced from Arkham Intelligence's illicit tag database and confirmed via open-source discovery of a Chinese-language Q3 2024 financial report published on a Huione subsidiary website that explicitly listed institutional wallet addresses across all four blockchains. Neither Binance nor OKX demonstrably curtailed Huione-linked transaction volume following their respective DOJ plea agreements.

### EV-TP0078-2026-002: FinCEN Huione Group 311 Designation

- **Source**: FinCEN, Designation of Huione Group as Primary Money Laundering Concern under Section 311 of the USA PATRIOT Act (May 2025)
- **CFPF Phase Coverage**: P5 (regulatory response)
- **Confidence**: High (formal government designation)
- **Summary**: FinCEN formally designated Huione Group as a primary money laundering concern, triggering enhanced due diligence requirements and correspondent banking restrictions for any US financial institution interacting with Huione Group-associated accounts or entities.

### EV-TP0078-2026-003: Post-Plea Compliance Gap

- **Source**: ICIJ analysis of transaction volumes pre- and post-DOJ plea agreements
- **Exchanges**: Binance (plea: November 2023); OKX (plea: February 2025)
- **Finding**: Neither exchange's transaction volume with Huione-linked wallets dropped precipitously immediately following their DOJ plea agreements
- **CFPF Phase Coverage**: P4 (compliance failure enabling continued pipeline operation)
- **Confidence**: Medium-High (volume analysis based on blockchain data; compliance implementation timelines may involve lag)

### EV-TP0078-2026-004: Crypto-to-Cash Physical Layer

- **Source**: ICIJ field visits to crypto-to-cash exchange desks in Dubai and Eastern European cities
- **Finding**: Unlicensed OTC operations converting USDT to physical currency with minimal KYC; one operation processed $2 million in 10 days on TRON alone; operation did not appear in any major blockchain analytics provider's attribution database
- **CFPF Phase Coverage**: P5 (monetization via physical cash conversion)
- **Confidence**: Medium-High (direct ICIJ observation; single operation documented)

---

## References

- ICIJ, "Coin Laundry" investigation series (published starting November 2024) — Huione Group tracing, exchange attribution methodology, crypto-to-cash desk field reporting
- ICIJ & OpenCorporates, "The Modern Money Trail: Crypto & Cash" webinar — Follow the Data Series, Webinar 1 (2026)
- FinCEN, Section 311 Designation of Huione Group as Primary Money Laundering Concern (May 2025)
- US DOJ, Binance Plea Agreement (November 2023) — AML compliance failures
- US DOJ, OKX Plea Agreement (February 2025) — AML compliance failures
- Arkham Intelligence — illicit wallet tag database used for initial Huione wallet attribution
- FATF Recommendation 16 (Wire Transfer Rule) — applicable to cross-border stablecoin transfers
- FinCEN, Advisory on Illicit Activity Involving Convertible Virtual Currency (May 2019)
- OFAC, Sanctions Compliance Guidance for the Virtual Currency Industry (October 2021)
- ICIJ, "Crypto Giants Moved Billions Linked to Money Launderers, Drug Traffickers and North Korean Hackers" — Spencer Woodman, Agustin Armendariz, Miguel Fiandor Gutierrez, Sam Ellefson

---

## Analyst Notes

**TRON/USDT as Dominant Laundering Rail**: TRON is the preferred blockchain for SE Asian fraud compound money laundering due to its low transaction fees (~$0.01 vs $5-50 on Ethereum) and high throughput. Detection systems that focus primarily on Ethereum or Bitcoin may miss the majority of stablecoin laundering volume. AML monitoring must prioritize TRON network coverage.

**Proof-of-Reserves as Attribution Resource**: Post-FTX collapse, major exchanges began publishing Proof-of-Reserves data — public CSV files listing addresses they claim ownership of. This is an underutilized attribution resource: cross-referencing suspicious outflow addresses against PoR address lists can confirm exchange relationships without requiring proprietary analytics access. PoR datasets should be collected and maintained as a standard AML reference.

**Attribution Deficit Favors Criminal Actors**: The blockchain is transparent but not attributable by default. Dominant analytics vendors (Chainalysis, TRM, Elliptic) hold proprietary attribution databases unavailable to under-resourced investigators. Open-source alternatives exist (Arkham Intelligence illicit tags, Florida FOIA wallet addresses, exchange PoR data) but require manual aggregation. The attribution deficit structurally advantages well-resourced criminal actors who understand which analytics providers' databases they appear in.

**Regulatory Deterioration Context**: The US regulatory environment for crypto AML is degrading: IRS crypto supervision staff (8031 unit) cut during 2024-2025 DOGE-era reductions; Corporate Transparency Act beneficial ownership enforcement suspended and data deleted; crypto exchanges classified as money transmitters (not banks) leaving them outside OCC/Fed/FDIC oversight. Detection systems must compensate for weakening supervisory capacity. EU AMLA (Frankfurt, direct supervision from 2028) represents a contrasting trajectory.

**Cross-Reference TP-0058**: Scam compound operational infrastructure (TP-0058) feeds directly into this laundering pipeline. Proceeds from pig butchering, investment scams, and romance fraud operations run through scam compounds are the primary predicate fraud types flowing through the Huione-style laundering service.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-30 | FLAME Project | Initial submission — sourced from ICIJ Coin Laundry investigation and ICIJ/OpenCorporates "Modern Money Trail" webinar analysis |
