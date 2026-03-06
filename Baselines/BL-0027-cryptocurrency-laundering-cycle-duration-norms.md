# Baseline: Cryptocurrency Laundering Cycle Duration Norms

```yaml
---
id: BL-0027
title: "Cryptocurrency Laundering Cycle Duration Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project (sourced from CrimsonVector Strategic Intelligence Report, Chainalysis, TRM Labs)"
related_tps:
  - id: TP-0049
    relationship: related-to
tags:
  - crypto-laundering
  - cmln
  - dprk-laundering-cycle
  - baseline
---
```

## Summary

This baseline defines normal and anomalous timing patterns for cryptocurrency laundering cycles, covering the full lifecycle from initial theft or illicit acquisition through distancing, integration, and final off-ramping to fiat currency. It establishes behavioral norms for DPRK state-sponsored laundering operations, Chinese Money Laundering Network (CMLN) processing services, legitimate exchange settlement timelines, pig butchering proceeds laundering, and cross-chain bridge hopping during the distancing phase. These baselines are derived from the CrimsonVector Strategic Intelligence Report, Chainalysis 2026 Crypto Crime Report, and TRM Labs illicit flow analysis. Organizations should calibrate detection thresholds against these timing norms to distinguish legitimate cryptocurrency transaction patterns from laundering activity.

## Normal Patterns

* **DPRK Laundering Cycle (Full Duration):** The complete DPRK state-sponsored cryptocurrency laundering cycle from initial theft to final off-ramp spans approximately **45 days**. This cycle is divided into three distinct phases: distancing (1-5 days), integration (5-14 days), and off-ramping (20-45 days). The extended off-ramping phase reflects the operational security discipline of DPRK-affiliated actors who distribute withdrawals across many accounts and jurisdictions to avoid triggering exchange compliance thresholds. Cycles completing in under 20 days indicate either operational urgency (funding deadline pressure) or a shift in tradecraft.

* **DPRK Distancing Phase:** The initial distancing phase spans **1-5 days** from the theft event. During this window, stolen funds are rapidly moved through a series of self-controlled wallets, mixers, and cross-chain bridges to break the direct on-chain link between the theft address and subsequent laundering infrastructure. Transaction volumes during distancing are high-frequency and high-value, with individual transactions often exceeding $1M equivalent.

* **DPRK Integration Phase:** The integration phase spans **5-14 days** following distancing. Funds are consolidated into intermediate wallets and begin interacting with semi-legitimate services including decentralized exchanges, OTC desks, and nested exchange accounts. Transaction values decrease as funds are split across multiple streams, and interaction with mixing services may continue.

* **DPRK Off-Ramping Phase:** The final off-ramping phase spans **20-45 days** and involves the conversion of cryptocurrency to fiat currency or stable value stores. This phase uses CMLN services, complicit OTC desks, and nested exchange accounts across multiple jurisdictions. The extended duration reflects deliberate pacing to remain below exchange reporting thresholds and compliance monitoring triggers.

* **CMLN Processing Time:** Chinese Money Laundering Network services operating under the "Black U" model process individual cryptocurrency-to-fiat or cryptocurrency-to-cryptocurrency transactions with an average processing time of **1.6 minutes per transaction**. This near-real-time processing speed enables high-volume laundering throughput and makes transaction-level interdiction extremely challenging. CMLN services typically operate 18-22 hours per day with brief maintenance windows.

* **Legitimate Exchange Settlement:** Standard cryptocurrency exchange settlement for fiat withdrawals takes **1-5 business days** depending on the exchange, jurisdiction, and withdrawal method. This baseline distinguishes normal exchange activity from laundering-associated rapid settlement patterns.

* **Pig Butchering Proceeds Laundering:** Cryptocurrency proceeds from pig butchering (romance-investment) scams follow a laundering cycle of **30-90 days** from theft to final off-ramp. The extended timeline reflects the multi-layered mule account networks and CMLN integration required to process proceeds from numerous individual victims aggregated through the scam operation. Cycles shorter than 30 days indicate streamlined laundering infrastructure with fewer intermediary hops.

* **Cross-Chain Bridge Hops:** During the distancing phase, stolen funds typically traverse **2-4 distinct blockchain networks** within a **24-hour window** via cross-chain bridges. Common chains include Ethereum, BSC, Avalanche, Polygon, and Tron. More than 4 chain hops within 24 hours indicates heightened operational urgency or advanced obfuscation tradecraft. Single-chain distancing (no bridge hops) is increasingly rare for sophisticated actors.

## Measurement Methodology

Track cryptocurrency theft events through on-chain monitoring, exchange incident reports, and law enforcement notifications. From the confirmed theft timestamp, measure elapsed time to key lifecycle milestones: first mixer or bridge interaction (distancing start), first interaction with exchange or OTC service (integration start), and first confirmed fiat conversion or stablecoin settlement (off-ramp start). Use blockchain analytics platforms (Chainalysis Reactor, TRM Labs Forensics) to trace fund flows across chains and identify phase transitions.

CMLN processing time is measured as the interval between inbound deposit confirmation and outbound transfer initiation on monitored CMLN-associated addresses. Aggregate processing times across multiple observed transactions to establish per-service and network-wide averages.

Cross-chain bridge hop counting uses bridge contract interaction events across monitored chains. A single hop is defined as one bridge transit from Chain A to Chain B. Count distinct chains touched within rolling 24-hour windows starting from the theft event timestamp.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| DPRK full laundering cycle | 30-45 days | 20-30 days | <20 days |
| DPRK distancing phase | 1-5 days | 6-12 hours | <6 hours |
| DPRK integration phase | 5-14 days | 2-5 days | <2 days |
| DPRK off-ramping phase | 20-45 days | 10-20 days | <10 days |
| CMLN per-transaction processing time | 1-3 minutes | 30-60 seconds | <30 seconds |
| Legitimate exchange fiat settlement | 1-5 business days | Same-day settlement | <1 hour |
| Pig butchering laundering cycle | 30-90 days | 14-30 days | <14 days |
| Cross-chain bridge hops (24-hour window) | 2-4 chains | 5-6 chains | >6 chains |
| Distancing-phase transaction frequency | 5-20 transactions/hour | 20-50 transactions/hour | >50 transactions/hour |
| Individual distancing transaction value | $100K-$5M | $5M-$20M | >$20M single transaction |

## Data Sources

* **Chainalysis Reactor and Crypto Crime Reports:** On-chain analytics and annual crime trend data providing DPRK laundering cycle duration measurements and cross-chain tracing capabilities.
* **TRM Labs Forensics:** Blockchain intelligence platform providing CMLN identification, processing time measurements, and illicit flow tracing across multiple chains.
* **CrimsonVector Strategic Intelligence Report:** Strategic assessment of DPRK cryptocurrency theft and laundering operations, including timeline reconstruction of major theft events through complete laundering cycles.
* **Exchange SAR filings:** Suspicious Activity Reports filed by cryptocurrency exchanges providing off-ramp timing data and CMLN interaction patterns from the compliance perspective.
* **Cross-chain bridge monitoring:** Direct monitoring of bridge contract interactions on Ethereum, BSC, Avalanche, Polygon, Tron, and other chains to track cross-chain fund movements during distancing phases.
* **OFAC virtual currency designations:** Treasury designations of cryptocurrency addresses and services associated with DPRK laundering operations, providing confirmed attribution anchors for cycle measurement.

## Application

Detection logic DL-0113 and DL-0114 should use these baselines for threshold calibration. DL-0113 (accelerated laundering cycle detection) should trigger when funds traced from a known or suspected theft event complete the distancing phase in under 6 hours or reach an exchange integration point in under 2 days, indicating an accelerated DPRK-pattern cycle. DL-0114 (CMLN processing anomaly) should trigger when transaction processing times on monitored CMLN-associated addresses drop below 30 seconds, indicating automated high-throughput laundering infrastructure, or when cross-chain bridge hops exceed 6 distinct chains within a 24-hour window.

Analysts should prioritize alerts where the full cycle duration falls below 20 days, as this compression strongly indicates operational urgency such as funding deadline pressure or detection evasion. Cases where pig butchering laundering cycles complete in under 14 days should be escalated as indicators of streamlined, high-efficiency laundering networks that may serve multiple upstream scam operations.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-05 | 1.0 | Initial baseline established from CrimsonVector report, Chainalysis, and TRM Labs data |
