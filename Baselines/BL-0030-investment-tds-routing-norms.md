# Baseline: Investment Platform TDS Routing Norms

```yaml
---
id: BL-0030
title: "Investment Platform TDS Routing Norms"
category: Baseline
date: 2026-03-20
author: "FLAME Project (sourced from Infoblox DNS Intelligence, Recorded Future CTA-2026-0319)"
related_tps:
  - id: TP-0060
    relationship: related-to
  - id: TP-0042
    relationship: related-to
tags:
  - tds
  - investment-scam
  - geo-routing
  - rdga
  - referral-chain
  - baseline
---
```

## Summary

This baseline defines normal and anomalous patterns for legitimate investment platform referral chain behavior, geographic routing patterns, and Registered Domain Generation Algorithm (RDGA) domain registration volumes. It establishes norms for referral chain depth, domain age of referral sources, DNS TTL configurations, RDGA domain volumes per registrant, and geo-routing content consistency. These baselines are derived from Infoblox DNS Intelligence and Recorded Future threat intelligence. Organizations should calibrate detection thresholds against these norms to identify Traffic Distribution System (TDS) infrastructure used to route victims to fraudulent investment platforms while evading detection by routing analyst and crawler traffic to legitimate platforms. This baseline supports detection logic DL-0120 and DL-0122.

## Normal Patterns

* **Referral Chain Depth (Legitimate Investment Platforms):** Legitimate investment platforms typically involve **1-2 hops** in the referral chain (direct link or single ad redirect). Chains of **3 or more hops** are suspicious for investment-related traffic and indicate potential TDS relay infrastructure inserted between the victim and the final destination.

* **Geo-Routing Behavior:** Legitimate platforms serve the same content globally, with localization changes limited to **language and currency display**. Fraud TDS infrastructure routes different geographies to **entirely different destinations**, serving legitimate platform content to US/EU traffic (where analysts and crawlers operate) while routing target geography traffic to fraudulent clones.

* **RDGA Domain Volume Per Entity:** Legitimate registrar behavior involves **fewer than 10 domains per entity per month**. Investment scam actors leveraging RDGA techniques pre-register **thousands of domains** to maintain resilient TDS infrastructure with rapid domain rotation capability.

* **Domain Age for Investment Platform Referral Sources:** Legitimate referral domains (financial news sites, established ad networks, affiliate platforms) are typically **older than 90 days**. TDS relay domains used in investment scam referral chains are typically **younger than 30 days**, reflecting the disposable nature of fraud infrastructure.

* **DNS TTL for Investment Platform Domains:** Legitimate platforms use DNS TTL values of **300-3600 seconds**, reflecting stable infrastructure. TDS relay domains use TTL values of **under 300 seconds**, enabling rapid IP rotation and infrastructure pivoting to evade blocklists.

* **Content Consistency Across Geolocations:** Legitimate platforms serve functionally equivalent content to all geolocations, with variance limited to localization. Fraud TDS infrastructure may route **US traffic to real eToro** (or similar legitimate platform) while routing target geography traffic to a **newly registered fake platform** — a pattern that defeats single-geography analysis.

## Measurement Methodology

Measure referral chain depth by instrumenting browser navigation to investment platforms from ad clicks, social media links, and search results. Count the number of distinct HTTP redirect hops (301, 302, 307, JavaScript redirects, and meta-refresh redirects) between the initial click and the final destination page. Record each intermediate domain in the chain.

Geo-routing detection requires multi-geography probing of referral chain URLs. Submit the same referral URL from multiple geographic vantage points (using VPN exit nodes or distributed probes in target and non-target geographies) and compare the final destination domain and page content. Calculate a content variance score as the percentage of DOM elements that differ between geographic responses, excluding expected localization elements (language tags, currency symbols).

RDGA domain volume is measured through passive DNS monitoring of new domain registrations, grouped by registrant entity (WHOIS organization, email, or registrant name). Count distinct domains registered per entity per rolling 30-day window. Flag entities whose registration volume exceeds thresholds.

Domain age is calculated as the difference between the current date and the domain creation date from WHOIS records. DNS TTL values are captured from authoritative DNS responses for each domain in the referral chain.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Referral chain hops to investment platform | 1-2 hops | 3-4 hops | >4 hops |
| Referral domain age | >90 days | 30-90 days | <30 days |
| DNS TTL of referral domains | 300-3600 seconds | 60-300 seconds | <60 seconds |
| RDGA domains per registrant per month | <10 | 10-100 | >100 |
| Geo-routing content variance score | <5% (localization only) | 5-25% | >25% (entirely different destinations) |
| US traffic redirection to known legitimate platform | N/A | Present with non-US going to unknown domain | Confirmed pattern: US→eToro, non-US→newly registered platform |

## Data Sources

* **Infoblox DNS Intelligence:** Passive DNS data providing domain registration volume tracking, TTL analysis, RDGA pattern detection, and registrant-level domain clustering for identifying bulk-registered TDS infrastructure.
* **Recorded Future CTA-2026-0319:** Threat intelligence report documenting investment scam TDS infrastructure patterns, geo-routing techniques, and referral chain analysis from active fraud campaigns.
* **Passive DNS databases (Farsight DNSDB, DomainTools):** Historical DNS resolution data enabling domain age verification, TTL trend analysis, and infrastructure mapping of TDS relay chains.
* **Multi-geography web probing infrastructure:** Distributed probe network providing content comparison data across geolocations to detect geo-routing content variance in referral chains.
* **WHOIS registration databases:** Registrant information enabling entity-level domain registration volume analysis and RDGA pattern identification.
* **Ad network referral chain telemetry:** Click-through chain data from advertising platforms providing baseline referral hop counts for legitimate investment platform advertising.

## Application

DL-0120 should calibrate geo-routing detection thresholds against these baselines. Specifically, DL-0120 should trigger review when referral chains to investment platforms exceed 2 hops and alert when chains exceed 4 hops, particularly when intermediate domains are younger than 30 days with DNS TTL values under 60 seconds. Geo-routing content variance scores exceeding 25% should generate high-priority alerts, as this indicates the referral chain is routing different geographies to entirely different destinations — the hallmark of fraud TDS infrastructure.

DL-0122 should use referral chain and domain age baselines to identify RDGA-powered TDS infrastructure. Registrant entities with more than 100 domains per month should be flagged for investigation. Referral chains where all intermediate domains are younger than 30 days and registered by entities with high domain volumes should be treated as confirmed TDS infrastructure indicators.

Analysts should pay particular attention to the US-to-legitimate-platform routing pattern, where US traffic is redirected to known platforms like eToro while non-US traffic reaches newly registered domains. This pattern is specifically designed to defeat analyst and crawler detection and should be considered a high-confidence fraud TDS indicator when confirmed through multi-geography probing.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-20 | 1.0 | Initial baseline established from Infoblox DNS Intelligence and Recorded Future threat intelligence |
