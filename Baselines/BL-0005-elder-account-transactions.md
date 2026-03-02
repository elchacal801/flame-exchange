# Baseline: Elder Account Transaction Patterns

```yaml
---
id: BL-0005
title: "Elder Account Transaction Patterns Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - elder-fraud
  - senior-accounts
  - financial-exploitation
---
```

## Description

This baseline defines normal transaction behavior for account holders aged 65 and older, supporting detection logic for TP-0027 (Elder Financial Exploitation). Elder financial abuse encompasses a range of schemes including caregiver theft, power-of-attorney abuse, tech support scams, and government impersonation fraud. Older adults are disproportionately targeted due to accumulated wealth, cognitive vulnerability, and social isolation.

Behavioral baselines for senior accounts are essential because transaction patterns for this demographic differ materially from the general population. Seniors exhibit more predictable spending, lower transaction frequency, and greater reliance on established payment channels. Deviations from these stable patterns are highly indicative of third-party influence or coercion.

## Normal Patterns

* **Weekly Transaction Frequency:** Accounts for holders aged 65+ average **8-15 debit transactions per week**, primarily concentrated in grocery, pharmacy, healthcare, and utility categories. A sustained increase to **25+ transactions per week** without a corresponding life event (e.g., relocation, medical event) is anomalous.
* **Withdrawal Patterns:** Normal ATM withdrawals for senior accounts average **$100-$300 per withdrawal**, occurring **2-4 times per month**. Cash withdrawals exceeding **$1,000 per event** or aggregate monthly cash withdrawals exceeding **$3,000** deviate from the 95th percentile for this demographic.
* **Bill Payment Consistency:** Approximately **85%** of monthly outflows from senior accounts go to recurring payees (utilities, insurance, medical providers, subscriptions). New payees receiving more than **$500** in a single transaction represent fewer than **3%** of monthly transactions for established accounts.
* **Gift Card Purchases:** The baseline for gift card purchases among seniors is **fewer than 3 per quarter**, with a median value of **$25-$50** per card. Purchasing **3+ gift cards totaling $500 or more** within a 7-day window is a strong deviation, particularly for cards redeemable outside the holder's normal merchant ecosystem (e.g., Apple, Google Play, Steam).
* **Wire and ACH Outflows:** Senior accounts initiate **fewer than 1 wire transfer per quarter** on average. The median outbound wire amount is **$2,500**, typically directed to family members or known entities. New outbound wires exceeding **$5,000** to first-time beneficiaries occur in fewer than **0.5%** of account-months.

## Application to Detection

Detection rules for TP-0027 should establish per-account behavioral profiles and flag deviations across multiple dimensions simultaneously. A single large withdrawal is ambiguous, but a large withdrawal combined with unusual gift card purchases and a new payee addition within the same 7-day window should generate a high-priority alert. Rules should trigger when any two of the following occur within a 14-day period: cash withdrawals exceeding 200% of the account's 90-day monthly average, gift card purchases exceeding quarterly norms, or outbound transfers to new beneficiaries.

Age-segmented thresholds are critical for reducing false positives. Generic fraud rules calibrated to the general population will under-alert on elder exploitation because the absolute dollar amounts may be modest compared to commercial fraud. Detection engines should apply tighter deviation thresholds (2 standard deviations instead of 3) for accounts in the 65+ cohort, reflecting the lower natural variability in their transaction patterns.
