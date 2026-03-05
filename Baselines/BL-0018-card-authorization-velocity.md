# Baseline: Card Authorization & Testing Velocity Patterns

```yaml
---
id: BL-0018
title: "Card Authorization & Testing Velocity Patterns Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - card-testing
  - BIN-attack
  - authorization-velocity
  - decline-rate
  - tester-merchant
  - payment-gateway
---
```

## Description

This baseline defines normal versus anomalous patterns for card authorization behavior at the merchant level, relevant to detecting card testing infrastructure abuse. It supports detection logic for TP-0038 (Card Testing Infrastructure Abuse) by establishing behavioral norms for sub-dollar authorization rates, BIN-level sequential authorization patterns, decline-to-approval ratios, and unique card diversity per source. These baselines are derived from the Recorded Future 2025 Annual Payment Fraud Intelligence Report (documenting 1,350+ tester merchants and 27M card records on Telegram linked to validation activity), payment network authorization analytics, and acquirer merchant monitoring data. The key insight is that card testing produces authorization patterns that are fundamentally different from legitimate commerce in multiple measurable dimensions simultaneously.

## Normal Patterns

* **Sub-Dollar Authorization Rate:** Established retailers maintain sub-dollar ($0.01-$0.99) authorization rates of **under 0.5%** of total merchant authorizations. Sub-dollar transactions in legitimate commerce are rare and typically limited to account verification holds for subscription services, tip adjustments, or rounding-related authorizations. Card testing operations produce sub-dollar authorization rates of **50-95%** of total volume, a deviation of two orders of magnitude from normal merchant behavior.

* **BIN-Level Sequential Authorization:** Legitimate merchants observe **zero** sequential card number authorization attempts from the same BIN prefix during normal commerce. Customers present cards with randomly distributed card numbers; sequential numbers from the same BIN are exclusively the product of BIN enumeration attacks. Any detection of 5 or more card numbers from the same 6-8 digit BIN prefix with incremental variation in the remaining digits within a single merchant's authorization stream is pathognomonic for BIN enumeration and has a **zero false positive rate** for legitimate merchants.

* **Decline-to-Approval Ratio:** Established merchants maintain authorization decline rates of **under 15%**, reflecting the normal proportion of expired cards, insufficient funds, and issuer declines in legitimate commerce. New merchants in their first 90 days may have slightly elevated decline rates (up to 20%) as they establish their customer base. Card testing operations produce decline rates of **70-90%**, as the majority of stolen or enumerated card numbers are associated with closed, expired, or blocked accounts. A merchant decline rate exceeding **30%** in any 1-hour window warrants investigation.

* **Unique Card Numbers per Source IP per Hour:** Legitimate online shoppers submit authorization requests for **under 5** unique card numbers per source IP per hour, reflecting individual purchase activity. Card testing operations generate **50-500+** unique card numbers per source IP per hour using automated scripts and bot infrastructure. Even with residential proxy distribution, the per-IP card diversity in testing operations significantly exceeds legitimate patterns.

* **Merchant Account Age and Transaction Profile:** Established merchants (operating for more than 180 days) show stable authorization profiles with predictable volume, amount distribution, and decline rates. Tester merchants, 94% of which are newly registered, show immediate high-volume, low-amount authorization activity inconsistent with their stated business type within the first days of account activation. The combination of merchant account age under 90 days with sub-dollar authorization velocity exceeding 50 per hour is a strong tester merchant indicator.

* **Authorization-to-Capture Ratio:** Legitimate merchants capture (settle) **85-98%** of their successful authorizations within 7 days. Card testing operations that use authorization-only requests show capture rates of **under 10%**, as the testers have no intention of completing transactions — they only need the authorization response to determine card validity.

## Application to Detection

Detection rules for TP-0038 should combine multiple authorization pattern indicators to produce high-confidence composite signals. No single indicator is sufficient: sub-dollar transactions occur legitimately in subscription verification, high decline rates can result from processing errors, and high card diversity can occur during legitimate promotional events. However, the simultaneous presence of high sub-dollar rates + elevated decline rates + high card diversity + low-age merchant account produces a composite signal with very low false positive rates.

BIN enumeration detection is the highest-confidence single indicator, with zero false positives for legitimate merchants. Sequential card number detection should be implemented as an independent alerting mechanism separate from the velocity-based composite rules, as it is conclusive evidence of card enumeration regardless of volume.

Threshold tuning should distinguish between merchant categories: subscription services legitimately generate higher sub-dollar authorization volumes; high-volume retailers have naturally higher card diversity; seasonal merchants may show variable decline rates. Merchant-category-specific baselines reduce false positives while maintaining detection sensitivity for tester merchant activity.

Cross-party correlation between acquirers, payment networks, and issuers is essential. A single acquirer may see a tester merchant as a normal low-volume account, while the payment network can observe the same card numbers being tested across multiple tester merchants, and the issuer can detect individual cards receiving sub-dollar authorizations at suspicious merchants. Industry-wide tester merchant intelligence sharing amplifies detection effectiveness.
