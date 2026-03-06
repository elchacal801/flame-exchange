# Baseline: State-Actor Infrastructure Reuse Pattern Norms

```yaml
---
id: BL-0024
title: "State-Actor Infrastructure Reuse Pattern Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project (sourced from CrimsonVector Strategic Intelligence Report, Gen Digital, Microsoft Threat Intelligence)"
related_tps:
  - id: TP-0044
    relationship: related-to
tags:
  - state-criminal-convergence
  - infrastructure-reuse
  - nation-state
  - baseline
---
```

## Summary

This baseline defines normal and anomalous parameters for infrastructure reuse between state-sponsored and criminal threat actor campaigns, supporting detection logic for TP-0044. It establishes behavioral norms for IP address overlap percentages, temporal proximity of attributed infrastructure on shared hosting, and convergence indicators that signal deliberate state-criminal cooperation versus coincidental co-tenancy. These baselines are derived from the CrimsonVector Strategic Intelligence Report, Gen Digital attribution databases, and Microsoft Threat Intelligence infrastructure tracking. Organizations should calibrate these thresholds to their specific threat intelligence feed coverage and attribution confidence levels.

## Normal Patterns

* **IP Address Reuse Between Unrelated Campaigns:** IP address overlap between campaigns attributed to unrelated threat actors is typically **1-5%** when measured across shared hosting providers, cloud infrastructure, and bulletproof hosting services. This baseline overlap reflects the finite pool of preferred hosting providers (particularly in jurisdictions with limited law enforcement cooperation) and the natural reuse of IP space as hosting accounts are provisioned and released. Overlap percentages above **5%** between campaigns with distinct attribution warrant investigation for deliberate infrastructure sharing or common operational support.

* **Temporal Proximity of State/Criminal Infrastructure on Same IP:** When state-attributed and criminal-attributed infrastructure coincidentally occupies the same IP address due to shared hosting rotation, the temporal separation between active use periods is typically **30 or more days**. This gap reflects the natural lifecycle of hosting account provisioning, use, abandonment, and re-provisioning by unrelated actors. Temporal separation below 30 days indicates either accelerated infrastructure rotation or potential coordination between the attributed parties.

* **State-Criminal Convergence Indicator:** The same IP address hosting infrastructure attributed to both a state-sponsored actor and a criminal organization within a **7-day window** is a high-confidence convergence indicator. This pattern was observed in the Gamaredon-Lazarus case documented in the CrimsonVector report, where state and criminal infrastructure operated on shared IP addresses with near-simultaneous activity windows. A 7-day co-tenancy window exceeds what coincidental hosting rotation can explain and suggests deliberate infrastructure sharing, common procurement channels, or operational coordination.

* **Attribution Confidence Decay:** Infrastructure attribution confidence degrades over time as IP addresses are reassigned and hosting configurations change. Attribution reports older than **90 days** should be weighted at **50%** confidence for IP-level indicators. Reports older than **180 days** should be weighted at **25%** or excluded from convergence calculations unless corroborated by additional indicators (domain registration continuity, TLS certificate reuse, or nameserver persistence).

* **Hosting Provider Concentration:** State-sponsored actors and criminal organizations independently converge on a small number of hosting providers in jurisdictions with limited international cooperation. Approximately **60-70%** of both state and criminal infrastructure concentrates in **fewer than 20 hosting providers** globally. This natural concentration inflates raw IP overlap percentages and must be normalized against provider-specific co-tenancy baselines to avoid false convergence signals.

## Measurement Methodology

Cross-reference threat intelligence attribution databases from at least three independent sources (government attribution reports, commercial CTI platforms, and open-source intelligence feeds) to establish IP-to-actor mappings. Measure IP overlap percentages by calculating the intersection of IP sets attributed to state-sponsored groups versus criminal organizations, normalized by the total IP footprint of each group. Temporal proximity is measured as the minimum number of days between the last observed state-attributed activity and the first observed criminal-attributed activity (or vice versa) on the same IP address.

Attribution confidence must meet a minimum threshold of **medium confidence** from at least two independent sources before an IP is included in overlap calculations. Single-source attributions should be flagged but excluded from convergence scoring to prevent false positives from misattribution.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) | Percentile Reference |
|---|---|---|---|---|
| IP overlap between unrelated campaigns | 1-5% | 5-10% | >10% | 95th percentile: 5.2% |
| Temporal separation (state/criminal on same IP) | 30+ days | 14-30 days | <7 days | 10th percentile: 28 days |
| State-criminal co-tenancy window | N/A (no overlap) | 7-30 days | <7 days (convergence) | 99th percentile: 8 days |
| Attribution source agreement | 3+ sources | 2 sources | 1 source only | Median: 2.4 sources |
| Hosting provider concentration (top 20) | 60-70% of infrastructure | 70-80% | >80% single-provider | 90th percentile: 74% |
| Attribution confidence decay (90-day) | 50% weight | 30% weight | <25% weight | Linear decay model |
| Campaign IP footprint size (state actor) | 50-500 IPs | 500-2,000 IPs | >2,000 IPs | 75th percentile: 380 IPs |
| Campaign IP footprint size (criminal) | 100-5,000 IPs | 5,000-20,000 IPs | >20,000 IPs | 75th percentile: 3,200 IPs |

## Data Sources

* **Government attribution reports:** US CISA advisories, FBI Flash alerts, NCSC (UK) technical advisories, and allied government joint attribution statements providing high-confidence actor-to-infrastructure mappings.
* **Commercial CTI feeds:** Microsoft Threat Intelligence, Gen Digital (Norton/Avast) telemetry, Recorded Future, Mandiant, and CrowdStrike threat actor infrastructure tracking databases.
* **MITRE ATT&CK group infrastructure databases:** ATT&CK group profiles with associated infrastructure indicators, cross-referenced with ATT&CK campaign entries for temporal context.
* **CrimsonVector Strategic Intelligence Report:** Primary source for state-criminal convergence case studies, including the Gamaredon-Lazarus infrastructure overlap analysis.
* **Passive DNS databases:** Historical DNS resolution data providing IP-to-domain mappings that supplement direct attribution feeds.
* **Certificate Transparency logs:** TLS certificate issuance records that provide additional infrastructure correlation signals when IP-level attribution is ambiguous.

## Application

Detection logic DL-0101 should use these baselines for threshold calibration. The primary detection trigger is IP overlap exceeding 10% between state-attributed and criminal-attributed infrastructure with temporal co-tenancy below 7 days. Secondary indicators include hosting provider concentration above 80% in a single provider and attribution source agreement from fewer than 2 independent sources (which may indicate fabricated or manipulated attribution designed to create false convergence signals).

Analysts should apply the attribution confidence decay model when evaluating historical infrastructure overlaps. Convergence alerts based on attribution data older than 90 days require corroboration from at least one non-IP indicator (shared TLS certificates, common domain registration patterns, or nameserver overlap) before escalation.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-05 | 1.0 | Initial baseline established from CrimsonVector report, Gen Digital, and Microsoft Threat Intelligence data |
