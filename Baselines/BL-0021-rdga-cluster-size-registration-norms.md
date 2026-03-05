# Baseline: RDGA Cluster Size and Registration Norms

```yaml
---
id: BL-0021
title: "RDGA Cluster Size and Registration Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project"
tags:
  - rdga
  - zone-file-analysis
  - bulk-registration
  - nameserver-clustering
  - dns-intelligence
---
```

## Description

This baseline defines normal parameters for domain registration clusters detected in CZDS zone file daily diffs, supporting detection logic for TP-0041 (Registered DGA Domain Clustering). It establishes behavioral norms for bulk registration volumes, nameserver concentration ratios, inter-registration timing distributions, and lexical entropy thresholds that distinguish legitimate bulk registrar activity from algorithmically generated domain campaigns. These baselines are derived from Infoblox 2025 DNS threat intelligence data on RDGA proliferation, Revolver Rabbit campaign analysis, and ICANN CZDS zone file differential analysis. Organizations should calibrate these thresholds to their specific zone file monitoring scope and registrar portfolio.

## Normal Patterns

* **Legitimate Bulk Registration Volume:** Legitimate bulk registrars register **50-500 domains per day** with diverse nameserver configurations spanning multiple hosting providers and geographic regions. Registration volumes within this range accompanied by heterogeneous nameserver assignments are consistent with domain portfolio management, brand protection programs, and reseller activity. Volumes exceeding **500 domains per day** from a single registrar account warrant additional scrutiny but are not inherently malicious when nameserver diversity is maintained.

* **RDGA Cluster Registration Volume:** RDGA clusters typically show **1,000-50,000+ domains** registered within a **24-hour window**, all pointing to fewer than **5 nameserver clusters**. This concentration pattern is the primary differentiator from legitimate bulk registration activity. Infoblox 2025 data documents over **3 million RDGA domains** observed in the wild, with **tens of thousands** of new RDGA domains appearing daily across monitored zone files. The Revolver Rabbit campaign alone accounted for over **500,000 registered domains**, demonstrating the industrial scale of modern RDGA operations.

* **Inter-Registration Timing Standard Deviation:** Normal bulk registration activity exhibits timing variability with a standard deviation exceeding **30 minutes** between successive registrations, reflecting human-initiated batch processes, manual review steps, and variable processing queues. RDGA registration timing standard deviation is typically **under 5 minutes**, reflecting automated scripted registration through registrar APIs with minimal variability. Timing analysis should be performed per registrar account per 24-hour window to avoid conflating multiple legitimate registrants into a single timing distribution.

* **Registrar-to-Nameserver Ratio:** Normal registrar behavior shows **1 registrar distributing domains across 10 or more nameserver providers**, reflecting diverse hosting arrangements, customer preferences, and CDN integrations. RDGA activity shows **1 registrar concentrated on 1-3 nameserver providers**, as the threat actor controls a limited infrastructure footprint and routes all generated domains through a small number of controlled nameservers. This ratio should be calculated on a rolling 7-day window to account for legitimate registrars that may temporarily concentrate on fewer providers during migration events.

* **Lexical Entropy of Domain Names:** Legitimate bulk registrations exhibit diverse naming patterns with Shannon entropy values exceeding **3.5 bits per character**, reflecting meaningful words, brand names, geographic terms, and intentional human-selected strings. RDGA domains exhibit constrained entropy in the range of **2.0-3.2 bits per character** due to algorithmic generation constraints — the generation algorithms produce strings that are pronounceable or pass basic validation checks but lack the full lexical diversity of human-selected names. Entropy should be calculated across the second-level domain label only, excluding the TLD, and assessed in aggregate across registration clusters rather than on individual domains.

* **Observed RDGA Scale (Infoblox 2025):** Infoblox 2025 threat intelligence data documents over **3 million RDGA domains** observed across their sensor network, with daily generation rates in the **tens of thousands**. This establishes the operational scale that detection systems must be prepared to handle — zone file differential analysis must process and classify thousands of new domains per zone per day to maintain detection coverage.

* **Revolver Rabbit Campaign Reference:** The Revolver Rabbit threat actor registered over **500,000 domains** using RDGA techniques, demonstrating that individual campaigns can sustain registration volumes of thousands of domains per day over extended periods. This campaign serves as a calibration reference for expected cluster sizes and persistence durations in production detection systems.

## Application to Detection

Detection rules DL-0092, DL-0093, and DL-0094 should use these baselines for threshold calibration. DL-0092 (cluster size detection) should trigger on registration clusters exceeding 1,000 domains per 24-hour window with nameserver concentration below 5 providers. DL-0093 (timing analysis) should flag registration batches with inter-registration timing standard deviation below 5 minutes across 100 or more domains. DL-0094 (lexical entropy scoring) should flag domain clusters with aggregate Shannon entropy below 3.2 bits per character.

Threshold calibration should reference Infoblox 2025 data as the primary empirical source for RDGA prevalence rates and cluster characteristics. The 3 million observed RDGA domains and tens-of-thousands daily generation rate establish the scale parameters that detection systems must accommodate without alert fatigue.

Multi-signal correlation is essential — individual signals (high volume, low entropy, concentrated nameservers) each produce false positives in isolation. Brand protection registrations may trigger volume thresholds; CDN migrations may trigger nameserver concentration alerts; internationalized domain names may trigger entropy anomalies. Combining all three signals with timing analysis produces the highest-confidence detection with acceptable false positive rates. Organizations should establish per-registrar behavioral profiles over a 30-day burn-in period before activating alerting thresholds.
