# Baseline: DME Claim Frequency per Provider

```yaml
---
id: BL-0006
title: "DME Claim Frequency per Provider Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - healthcare-fraud
  - dme-billing
  - medicare
  - claims-frequency
---
```

## Description

This baseline defines normal claim submission patterns for Durable Medical Equipment (DME) providers billing Medicare and commercial payers, supporting detection logic for TP-0028 (DME Phantom Billing). DME fraud schemes exploit the complexity of medical billing to submit claims for equipment never delivered, bill for higher-cost items than provided (upcoding), or claim services for deceased or ineligible beneficiaries.

Establishing per-provider claim frequency, dollar distribution, and beneficiary concentration norms is critical because DME fraud often hides within high-volume billing operations. Providers operating within normal parameters are unlikely to trigger individual claim-level reviews, making aggregate behavioral baselines the primary detection mechanism for phantom billing operations.

## Normal Patterns

* **Monthly Claim Volume per NPI:** A legitimate single-location DME provider submits **80-250 claims per month**. Providers consistently exceeding **500 claims per month** without corresponding growth in staff, referral sources, or warehouse capacity fall above the 97th percentile and warrant enhanced scrutiny.
* **Claim Dollar Distribution:** The median DME claim is **$150-$800**, with common items such as CPAP supplies ($200-$400), wheelchairs ($500-$3,000), and oxygen equipment ($300-$1,200). A provider whose average claim value exceeds **$2,500** while primarily billing for routine supply categories deviates from expected coding patterns.
* **Beneficiary-to-Provider Ratio:** Legitimate DME providers serve **50-200 unique beneficiaries per quarter** per location. A provider billing for more than **400 unique beneficiaries per quarter** from a single NPI, particularly when geographic analysis shows beneficiaries spread across **5+ states**, is anomalous.
* **Geographic Service Radius:** Normal DME providers serve beneficiaries within a **50-mile radius** of their registered business address. Approximately **92%** of legitimate claims involve beneficiaries within this radius. Providers with more than **20%** of claims falling outside a 100-mile radius exhibit patterns consistent with phantom billing networks.
* **Claim Timing Patterns:** Legitimate providers submit claims with an average lag of **3-10 business days** after the date of service. Bulk submissions where **50+ claims share the same date of service** and are submitted simultaneously represent fewer than **2%** of normal provider billing events.

## Application to Detection

Detection rules for TP-0028 should combine volume, concentration, and geographic signals to score providers on a composite risk basis. A provider exceeding the 95th percentile in monthly claim volume alone may be a large legitimate operation, but the same volume combined with a beneficiary concentration exceeding 400 per quarter and a geographic spread beyond 100 miles should generate a high-confidence alert. Rules should flag providers whose month-over-month claim volume increases by more than 150% without a corresponding new-supplier registration or facility expansion event.

Threshold calibration should account for provider specialty and geographic density. Urban DME providers naturally serve more beneficiaries within a tighter radius, while rural providers may have wider geographic reach but lower volumes. Detection models should use peer-group comparison (same specialty, same region) rather than absolute thresholds to minimize false positives from legitimate high-volume suppliers.
