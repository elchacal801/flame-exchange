# Baseline: E-Commerce Order and Return Velocity

```yaml
---
id: BL-0008
title: "E-Commerce Order and Return Velocity Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - ecommerce-fraud
  - return-fraud
  - order-velocity
  - refund-patterns
---
```

## Description

This baseline defines normal ordering and return behavior for e-commerce consumer accounts, supporting detection logic for TP-0030 (E-Commerce Triangulation) and TP-0031 (Refund-as-a-Service). Triangulation fraud uses stolen payment credentials to fulfill orders placed on third-party marketplaces, while refund-as-a-service operations exploit merchant return policies through social engineering, empty-box claims, and "did not arrive" (DNA) disputes.

Behavioral baselines for order and return velocity are essential because both fraud types rely on blending into normal commerce activity. Triangulation fraudsters need to maintain plausible order volumes, and refund abusers must keep their return rates below merchant review thresholds. Establishing quantitative norms enables detection at the margins where fraudulent activity diverges from legitimate shopping behavior.

## Normal Patterns

* **Order Frequency:** The average active e-commerce consumer places **3-8 orders per month** across all merchants. Accounts placing **20+ orders per month** represent fewer than **2%** of the consumer population and warrant enhanced monitoring, particularly when orders ship to multiple distinct addresses.
* **Return Rate:** The industry-average return rate is **8-10%** of orders for general merchandise, rising to **15-20%** for apparel and footwear. An individual account return rate exceeding **30%** over a rolling 90-day period deviates from normal behavior. Accounts with return rates above **50%** over any 30-day window are extreme outliers.
* **Purchase-to-Return Interval:** Legitimate returns are initiated a median of **7-14 days** after delivery, with **90%** of returns filed within **30 days**. Returns filed within **24 hours** of confirmed delivery represent fewer than **5%** of legitimate returns and are associated with elevated DNA fraud risk.
* **Item Category Return Rate Variation:** Electronics return rates average **8%**, home goods **9%**, and apparel **18-22%**. An account returning **40%+ of electronics purchases** over a 90-day period, or an account that exclusively returns high-value items (>$200) while keeping low-value items, deviates from category norms.
* **Shipping Address Diversity:** Normal consumer accounts ship to **1-3 addresses** (home, office, gift recipients). Accounts shipping to **5+ unique addresses within 30 days**, particularly when combined with high order velocity, exhibit patterns consistent with triangulation fulfillment operations.

## Application to Detection

Detection rules for TP-0030 should focus on the convergence of high order velocity, multiple shipping addresses, and payment anomalies (e.g., card-not-present transactions with mismatched billing/shipping). Flag accounts exceeding 15 orders per month when more than 40% ship to addresses used only once. For TP-0031, rules should track per-account return rates on a rolling 90-day basis and escalate when return rates exceed 2 standard deviations above the category-adjusted mean, particularly for accounts with a pattern of returning only high-value items.

Threshold calibration should incorporate seasonal variation: return rates naturally increase by **5-8 percentage points** during the post-holiday period (January-February). Detection engines should use year-over-year seasonal adjustments rather than static thresholds. Additionally, rules should weight DNA claims more heavily when the account has filed 3+ DNA claims within 180 days, as the probability of legitimate repeated delivery failures to the same address is extremely low.
