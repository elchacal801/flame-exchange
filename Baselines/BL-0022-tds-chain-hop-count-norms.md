# Baseline: TDS Chain Hop Count Norms

```yaml
---
id: BL-0022
title: "TDS Chain Hop Count Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project"
tags:
  - tds
  - redirect-chain
  - cloaking
  - web-proxy
  - dns-intelligence
---
```

## Description

This baseline defines normal redirect chain depth for legitimate web traffic versus TDS (Traffic Distribution System) exploitation, supporting detection logic for TP-0042 (TDS Redirect Chain Abuse). It establishes behavioral norms for redirect hop counts, per-hop latency, geographic traversal patterns, cloaking node behavior, and TDS infrastructure scale. These baselines are derived from Infoblox 2025 DNS threat intelligence data on VexTrio and related TDS operations, web traffic analysis of legitimate advertising and marketing redirect chains, and differential content serving analysis across IP reputation classes. Organizations should calibrate these thresholds to their specific network monitoring capabilities and user traffic profiles.

## Normal Patterns

* **Legitimate Marketing Redirect Depth:** Legitimate marketing redirect chains consist of **1-3 hops** with a mean of **1.8 hops**. These chains typically involve a click tracker, a landing page redirect, and the final destination URL. Chains within this range are consistent with standard email marketing platforms, affiliate link tracking, and URL shortener services. Single-hop redirects (direct click-to-destination) account for approximately 40% of legitimate marketing traffic.

* **Legitimate Ad Network Redirect Depth:** Legitimate advertising network redirect chains consist of **2-4 hops** with a mean of **2.7 hops**. These chains involve an ad server, a demand-side platform redirect, an optional verification service, and the advertiser landing page. Programmatic advertising chains are inherently deeper than marketing chains due to the multi-party auction and verification ecosystem. Chains of 4 hops within established ad network infrastructure are normal and should not trigger alerts.

* **TDS Exploitation Chain Depth:** TDS exploitation chains consist of **4-7+ hops** with a mean of **5.2 hops**. These chains involve an initial compromised page or malvertising injection, one or more TDS gate nodes that perform fingerprinting and filtering, intermediate redirect domains that provide operational resilience, and the final malicious payload or scam landing page. Chains exceeding 4 hops that traverse domains with no established reputation or web presence are high-confidence indicators of TDS activity.

* **Per-Hop Latency:** Legitimate redirect chains complete the full chain within **2 seconds** total, with per-hop latency typically under **200 milliseconds** for well-provisioned infrastructure. TDS chains introduce **500 milliseconds to 2 seconds of latency per hop** due to fingerprinting logic execution, conditional routing decisions, geographic distribution of TDS nodes, and intentional timing delays designed to evade automated analysis. A redirect chain with cumulative latency exceeding **4 seconds** across 4 or more hops is anomalous relative to legitimate redirect infrastructure.

* **Geographic Traversal:** Legitimate redirect chains use consistent geolocation, with all hops typically resolving to infrastructure within **1 country** or within a single CDN provider's global network. TDS chains traverse **2 or more countries** as the chain progresses through geographically distributed gate nodes, bullet-proof hosting providers, and destination infrastructure in different jurisdictions. Geographic traversal analysis should use GeoIP resolution of each hop's IP address and flag chains that cross 2 or more distinct country boundaries without a CDN provider explanation.

* **VexTrio TDS Scale:** VexTrio operates over **70,000 TDS domains** at any given time, with approximately **500,000 TDS domains** observed over a 12-month period as domains are rotated and replaced. This establishes VexTrio as one of the largest known TDS operations and provides a scale reference for detection system capacity planning. Detection systems must be prepared to track and classify tens of thousands of active TDS domains simultaneously.

* **Malicious Adtech Contact Rate:** Infoblox 2025 data indicates that **82% of customer environments** contacted at least one malicious adtech or TDS-affiliated domain during the observation period. This prevalence rate demonstrates that TDS exposure is near-universal across enterprise and consumer networks, making TDS chain detection a high-priority capability rather than a niche concern.

* **Cloaking Node Differential Content Serving:** TDS cloaking nodes serve differential content based on visitor characteristics — delivering **benign content to scanners, crawlers, and known security vendor IP ranges** while serving **malicious redirects to residential IP addresses** and consumer user agents. Detection of cloaking behavior requires comparing content served to known-clean scanner IPs versus residential proxy IPs for the same URL. A differential serving rate (different content for different IP reputation classes) exceeding **10%** of requests to a given domain is anomalous and indicative of active cloaking.

## Application to Detection

Detection rules DL-0095, DL-0096, and DL-0097 should use these baselines for threshold calibration. DL-0095 (hop count anomaly detection) should trigger on redirect chains exceeding 4 hops where intermediate domains have registration ages under 30 days or lack established web presence. DL-0096 (latency profiling) should flag chains with cumulative latency exceeding 4 seconds or per-hop latency exceeding 500 milliseconds across 3 or more hops. DL-0097 (cloaking detection) should identify domains exhibiting differential content serving rates above 10% when probed from diverse IP reputation classes.

The 82% contact rate across customer environments underscores the importance of network-level TDS detection — relying solely on endpoint protection leaves significant coverage gaps. DNS-level monitoring of redirect chain construction, combined with passive HTTP header analysis, provides the most comprehensive detection surface.

Threshold tuning should account for legitimate deep redirect chains in programmatic advertising. Allowlisting of known ad exchange and verification service domains prevents false positives from legitimate 4-hop ad chains. The key discriminator between legitimate deep chains and TDS chains is domain reputation and registration recency — TDS chains traverse recently registered or low-reputation domains, while legitimate ad chains traverse well-established infrastructure.
