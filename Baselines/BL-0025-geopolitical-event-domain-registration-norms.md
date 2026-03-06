# Baseline: Geopolitical Event Domain Registration Norms

```yaml
---
id: BL-0025
title: "Geopolitical Event Domain Registration Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project (sourced from CrimsonVector Strategic Intelligence Report, Finance Derivative 2026, Radware)"
related_tps:
  - id: TP-0045
    relationship: related-to
  - id: TP-0046
    relationship: related-to
tags:
  - geopolitical-timing
  - domain-registration
  - election-cycle
  - sanctions-response
  - baseline
---
```

## Summary

This baseline defines normal and anomalous domain registration volumes correlated with geopolitical events, supporting detection logic for TP-0045 and TP-0046. It establishes behavioral norms for financial brand-impersonating domain registrations during steady-state periods, pre-election escalation windows, post-sanctions infrastructure migration patterns, and seasonal adjustment factors. These baselines are derived from the CrimsonVector Strategic Intelligence Report, Finance Derivative 2026 geopolitical risk analysis, and Radware application threat intelligence. Organizations should calibrate these thresholds against their monitored brand keyword lists and geographic scope of elections and sanctions events.

## Normal Patterns

* **Steady-State Financial Brand Domain Registration:** The baseline rate of new domain registrations containing major bank and financial institution brand names (exact match and common misspellings) is **50-200 new registrations per week** across all monitored TLDs. This range reflects the persistent background level of brand-squatting, phishing infrastructure preparation, and speculative domain registration targeting financial services. The baseline fluctuates seasonally, with higher rates during tax filing periods (Q1) and holiday shopping seasons (Q4).

* **Pre-Election Registration Spike (Normal):** In the **60 days before national elections** in major economies (US, UK, EU member states, India, Brazil), financial brand domain registrations increase by **1.5-2x baseline** (75-400 registrations per week). This elevation reflects both legitimate political domain registration activity that incidentally contains financial keywords and opportunistic threat actors positioning phishing infrastructure to exploit election-related uncertainty and information-seeking behavior. This range is considered normal seasonal variation and should not trigger anomaly alerts.

* **Anomalous Election-Correlated Surge:** Registration rates exceeding **3x baseline** (150-600+ registrations per week) within **30 days of national elections or major sanctions announcements** are anomalous and indicate coordinated threat actor campaign preparation. This threshold accounts for the compounding effect when election uncertainty coincides with sanctions activity, as observed in Finance Derivative 2026 analysis of financial fraud escalation during geopolitical instability periods.

* **Post-Sanctions Infrastructure Migration:** Following the designation of entities or jurisdictions on the OFAC SDN list, **10-50 domains** previously hosted on IP ranges associated with the sanctioned jurisdiction migrate to non-sanctioned hosting providers within **14 days of designation**. This migration pattern reflects threat actor infrastructure adaptation to maintain operational continuity despite sanctions enforcement. Migration volumes exceeding 50 domains within 14 days suggest large-scale coordinated infrastructure relocation and may indicate state-directed rather than independent criminal adaptation.

* **Sanctions Announcement Domain Spike:** Within **72 hours of a major sanctions announcement**, new domain registrations containing the names of newly sanctioned entities or their associated financial institutions increase by **5-10x** over the pre-announcement baseline for those specific keywords. This spike reflects both legitimate news and commentary sites and threat actors registering domains to impersonate sanctioned entities for fraud, sanctions evasion facilitation, or intelligence collection.

* **Geographic Correlation:** Domain registrations from registrars in the same geographic region as the geopolitical event account for **40-60%** of the event-correlated spike. Registrations from geographically distant registrars (particularly those in jurisdictions with limited cooperation on domain abuse) exceeding **50%** of the spike volume indicate externally directed campaigns rather than organic local registration activity.

## Measurement Methodology

Monitor CZDS zone file daily diffs for new registrations matching financial brand keyword lists (bank names, payment processor brands, regulatory body names, and common misspellings). Keyword lists should be maintained with at least the top 200 global financial brands and updated quarterly. Correlate registration volumes with an election calendar database covering national elections in G20 countries and a sanctions announcement feed (OFAC SDN list changes, EU consolidated sanctions list updates, UN Security Council designation changes).

Calculate rolling 7-day registration counts to smooth daily variance. Compare rolling counts against the 90-day trailing baseline to determine multiplication factors. Seasonal adjustment factors should be applied before anomaly scoring to account for known periodic variations (tax season, holiday season, fiscal year transitions).

Registration-to-event temporal correlation is measured by calculating the Pearson correlation coefficient between daily registration volumes and a binary event indicator (1 for days within the defined event window, 0 otherwise). Correlation coefficients above **0.6** between registration volume spikes and geopolitical event windows confirm systematic rather than coincidental timing relationships.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) | Seasonal Adjustment |
|---|---|---|---|---|
| Weekly financial brand registrations (steady-state) | 50-200 | 200-400 | >400 | Q1: +25%, Q4: +30% |
| Pre-election spike (60-day window) | 1.5-2x baseline | 2-3x baseline | >3x baseline | +10% during concurrent holiday |
| Post-sanctions domain migration (14-day window) | 10-50 domains | 50-100 domains | >100 domains | N/A |
| Sanctions-keyword domain spike (72-hour window) | 2-5x keyword baseline | 5-10x keyword baseline | >10x keyword baseline | N/A |
| Geographic concentration (event-region registrars) | 40-60% | 30-40% or 60-70% | <30% or >70% | Regional variance +/-10% |
| Registration-to-event correlation coefficient | <0.3 (uncorrelated) | 0.3-0.6 | >0.6 (systematic) | N/A |
| Time-to-first-resolution after registration | 24-72 hours | 4-24 hours | <4 hours | N/A |
| Multi-TLD registration per brand keyword | 1-3 TLDs | 3-5 TLDs | >5 TLDs simultaneously | N/A |

## Data Sources

* **CZDS zone files:** ICANN Centralized Zone Data Service providing daily zone file snapshots for gTLD analysis. Zone file diffs are computed daily to identify new registrations matching financial brand keyword lists.
* **OFAC SDN list change feed:** US Treasury Office of Foreign Assets Control Specially Designated Nationals list, monitored for additions, modifications, and removals that trigger domain registration pattern changes.
* **EU consolidated sanctions list:** European Union sanctions designations providing complementary coverage to OFAC for EU-focused financial brand targeting.
* **Election calendar databases:** International Foundation for Electoral Systems (IFES) election calendar and national electoral commission announcements covering G20 countries and major financial centers.
* **Brand keyword lists:** Maintained list of top 200 global financial institution names, common misspellings, abbreviations, and localized name variants used for zone file matching.
* **Finance Derivative 2026:** Geopolitical risk analysis correlating financial fraud escalation patterns with election cycles and sanctions enforcement actions.
* **Radware application threat intelligence:** Domain-based attack campaign tracking and registration pattern analysis for financial services targeting.
* **CrimsonVector Strategic Intelligence Report:** Strategic assessment of geopolitical event exploitation by threat actors targeting financial infrastructure.

## Application

Detection logic DL-0105 and DL-0106 should use these baselines for threshold calibration. DL-0105 (election-cycle domain surge) should trigger when financial brand domain registrations exceed 3x the seasonally adjusted baseline within 30 days of a national election in any G20 country. DL-0106 (sanctions-response infrastructure migration) should trigger when more than 50 domains migrate from sanctioned IP ranges within 14 days of an OFAC or EU sanctions designation, or when sanctions-keyword domain registrations exceed 10x the keyword-specific baseline within 72 hours of announcement.

Seasonal adjustment factors must be applied before threshold comparison. A registration rate of 250 per week during Q4 (holiday-adjusted baseline: 260) is within normal range, while the same rate during Q2 (unadjusted baseline: 200) exceeds the elevated threshold. Detection systems that do not apply seasonal normalization will generate excessive false positives during Q1 tax season and Q4 holiday periods.

Analysts should prioritize alerts where geographic concentration falls below 30% (indicating externally directed campaigns) and time-to-first-resolution is under 4 hours (indicating pre-staged infrastructure activated in response to the geopolitical event rather than opportunistic registration).

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-05 | 1.0 | Initial baseline established from CrimsonVector report, Finance Derivative 2026, and Radware data |
