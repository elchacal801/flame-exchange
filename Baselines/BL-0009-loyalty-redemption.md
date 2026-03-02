# Baseline: Loyalty Redemption Patterns

```yaml
---
id: BL-0009
title: "Loyalty Redemption Patterns Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - loyalty-fraud
  - gift-cards
  - rewards-programs
  - credential-stuffing
---
```

## Description

This baseline defines normal earning, accumulation, and redemption patterns for loyalty programs and rewards accounts, supporting detection logic for TP-0013 (Credential Stuffing to Loyalty/Gift Card Drain). Attackers use credential stuffing and account takeover techniques to access loyalty accounts, then rapidly drain accumulated points through gift card conversions, merchandise redemptions, or transfer to attacker-controlled accounts.

Behavioral baselines for loyalty activity are critical because most consumers interact with their rewards accounts infrequently and in predictable patterns. The abrupt shift from dormant accumulation to rapid high-value redemption creates a distinctive behavioral signature that is difficult for attackers to disguise, making baseline-driven detection highly effective.

## Normal Patterns

* **Redemption Frequency:** The average loyalty program member redeems points **2-4 times per year**. Approximately **60%** of members redeem fewer than **once per quarter**. An account executing **3+ redemptions within a 7-day window** deviates from the 99th percentile of normal redemption frequency.
* **Point Balance Utilization:** Legitimate members typically redeem **20-40%** of their accumulated balance per redemption event. Full balance redemptions (>90% of available points) occur in fewer than **8%** of redemption events and are concentrated around account closures, program migrations, or holiday gifting.
* **Redemption-to-Earning Ratio:** Over a rolling 90-day window, the normal ratio of points redeemed to points earned is **0.5:1 to 1.5:1** for active members. A ratio exceeding **5:1** (redeeming far more than recently earned) indicates a drain of accumulated balance, particularly suspicious when the account has been dormant for 60+ days prior.
* **Login-to-Redemption Timing:** Legitimate members browse their account an average of **2-3 sessions before redeeming**, with a median time from login to redemption of **8-20 minutes**. Redemptions executed within **60 seconds** of login represent fewer than **1%** of legitimate events and are consistent with automated drain scripts.
* **Redemption Channel and Destination:** Approximately **75%** of legitimate redemptions are for the program's own products/services (flights, hotel nights, merchandise). Conversions to third-party gift cards or cash equivalents account for **15-20%** of redemptions. An account that converts **100% of a large balance** exclusively to third-party gift cards in a single session is a strong anomaly.

## Application to Detection

Detection rules for TP-0013 should prioritize the login-to-redemption velocity signal. Accounts that authenticate and execute a full-balance redemption within 60 seconds should trigger immediate hold-and-review workflows, particularly when the authentication occurs from a new device or IP address not previously associated with the account. Rules should also flag accounts where a login from a new geography is followed by any redemption activity within the same session.

Threshold tuning should account for program-specific norms: airline programs see higher redemption values but lower frequency, while retail programs see lower values but more frequent activity. Detection engines should maintain per-program baseline distributions and flag accounts deviating by more than 3 standard deviations on any single metric, or by more than 2 standard deviations on two or more metrics simultaneously. Dormancy-to-activity transitions (no login for 90+ days followed by immediate redemption) should receive the highest risk weighting.
