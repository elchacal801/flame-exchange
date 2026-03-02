# Baseline: Investment Account Deposit Velocity

```yaml
---
id: BL-0004
title: "Investment Account Deposit Velocity Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - investment-fraud
  - deposit-velocity
  - crypto-exchanges
---
```

## Description

This baseline defines normal deposit behavior for retail brokerage and cryptocurrency exchange accounts, supporting detection logic for TP-0026 (GenAI APP Fraud - Investment) and TP-0017 (Pig Butchering). Investment scams, particularly pig butchering operations, manipulate victims into making progressively larger deposits to fraudulent platforms or controlled exchange accounts.

Establishing deposit velocity and escalation norms for legitimate investment activity enables detection engines to identify the distinctive ramp-up patterns associated with scam-driven funding. These baselines are especially critical because victims often believe they are making rational investment decisions, making transaction-level fraud signals ambiguous without behavioral context.

## Normal Patterns

* **Funding Frequency:** Legitimate retail investors fund brokerage accounts **1-3 times per month** on average. Crypto exchange accounts see slightly higher frequency at **2-5 deposits per month**. Sustained funding exceeding **8 deposits in a rolling 30-day window** is anomalous for accounts less than 1 year old.
* **Deposit Amount Ranges:** The median initial brokerage deposit is **$2,000-$5,000**, with subsequent deposits averaging **$500-$2,000**. Crypto exchange deposits average **$200-$1,000** per transaction. Individual deposits exceeding **$10,000** represent fewer than **5%** of retail account funding events.
* **Escalation Patterns:** Normal investment funding shows stable or slowly increasing deposits over months. An escalation where each successive deposit is **2x or greater** than the previous within a **14-day window** (e.g., $500, $1,500, $5,000, $15,000) deviates sharply from legitimate behavior and is characteristic of pig butchering grooming.
* **Deposit-to-Withdrawal Ratio:** Legitimate investors maintain a deposit-to-withdrawal ratio of approximately **1.5:1 to 3:1** over a 90-day period, reflecting periodic rebalancing and profit-taking. Scam-driven accounts exhibit ratios exceeding **10:1**, with little to no successful withdrawal activity.
* **Funding Source Diversity:** Normal accounts are funded from **1-2 linked bank accounts**. Victims under scam pressure often tap **3+ funding sources** within 30 days, including retirement account rollovers, HELOCs, and personal loans, signaling financial stress-driven funding.

## Application to Detection

Detection rules for TP-0026 and TP-0017 should track deposit escalation velocity on a per-account basis. Flag accounts where the trailing 7-day deposit total exceeds 3x the account's 30-day rolling average, particularly when combined with zero or near-zero withdrawal activity. The deposit-to-withdrawal ratio is a high-confidence signal: accounts exceeding a 10:1 ratio over 60 days with more than $10,000 in cumulative deposits should generate priority alerts.

Threshold tuning should differentiate between brokerage and crypto exchange accounts, as crypto accounts naturally show higher funding frequency. Rules should also weight the escalation signal more heavily when deposits are sourced from newly linked bank accounts or non-traditional funding sources, as this pattern strongly correlates with coerced investment behavior.
