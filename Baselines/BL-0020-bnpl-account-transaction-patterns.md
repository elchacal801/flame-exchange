# Baseline: BNPL Account & Transaction Patterns

```yaml
---
id: BL-0020
title: "BNPL Account & Transaction Patterns Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - bnpl-fraud
  - synthetic-stacking
  - friendly-fraud
  - multi-provider
  - onboarding
  - transaction-patterns
---
```

## Description

This baseline defines normal versus anomalous patterns for BNPL account lifecycle and transaction behavior, supporting detection logic for TP-0040 (BNPL Multi-Provider Fraud). It establishes behavioral norms for onboarding signals (email age, digital footprint), transaction patterns (time-to-first-order, spending ramp-up, payment completion), multi-provider usage frequency, dispute rates, shipping address behavior, and device reuse ratios. These baselines are derived from the LexisNexis Risk Solutions Global State of Fraud and Identity Report 2026, Experian BNPL fraud rate analysis, ACI Worldwide synthetic identity exposure data, and Merchant Risk Council survey data on friendly fraud prevalence. Organizations should calibrate these thresholds to their specific BNPL provider portfolio, market segment, and customer demographic mix.

## Normal Patterns

* **Email Domain Age at Onboarding:** Legitimate BNPL applicants have email addresses with domain ages of **180 days or more** (median). Email addresses less than **30 days old** at the time of BNPL application are rare among legitimate consumers (under 2% of applications) and are a strong indicator of synthetic identity or recently fabricated accounts. Email age should be assessed in conjunction with digital footprint scoring — a new email address with an established social media presence is lower risk than a new email with no digital footprint.

* **Time from Account Creation to First Order:** Legitimate consumers typically place their first BNPL order **2-7 days** after account creation (median), with a significant portion (30-40%) making their first purchase on the same day as account creation. Accounts that remain dormant for more than **14 days** before placing a first order are uncommon (under 10%) and may indicate accounts created in bulk for later use. However, the same-day first purchase pattern is also exhibited by legitimate consumers responding to a specific purchase need.

* **Payment Completion Rate:** Legitimate BNPL users maintain payment completion rates of **95% or higher** across their account lifecycle. Users who miss payments represent 3-5% of accounts, with most missed payments resolved within 7 days. Accounts with payment completion rates below **80%** within the first 90 days are anomalous and may indicate intent to default (first-party fraud) or inability to pay (over-extension).

* **BNPL Providers Used Simultaneously:** Over a 12-month period, legitimate consumers use **1-2 BNPL providers** on average. Usage of **3 or more** distinct providers within 72 hours is rare (under 0.5% of consumers) and strongly indicative of multi-provider stacking, particularly when combined with other risk signals. Legitimate multi-provider usage is typically spread over weeks or months as consumers discover different providers through different merchant integrations.

* **INR Dispute Rate:** Legitimate INR (item-not-received) dispute rates are **under 1%** of total orders. Rates exceeding **3%** per account are anomalous. Legitimate INR disputes typically involve delivery to addresses with known postal challenges, orders during peak shipping seasons, or high-value items requiring signature confirmation. Disputes concentrated on orders exceeding **$300** in value are more concerning than disputes on lower-value orders, as organized fraud targets high-resale-value goods.

* **Shipping Address Change Pre-Dispatch:** Fewer than **1%** of legitimate BNPL orders involve a shipping address change after order placement but before dispatch. Post-order address changes, particularly to addresses in different geographic regions than the account holder's verified address, are a strong indicator of goods diversion. Legitimate address changes are typically minor corrections (apartment number, suite number) rather than complete address changes.

* **Device Reuse Across Accounts:** Normal BNPL usage involves **1 device per 1-2 accounts** over a 12-month period. A single device associated with **4 or more** BNPL accounts within 30 days is anomalous and indicative of account farming or synthetic identity ring operations. Shared household devices may legitimately be associated with 2-3 accounts (family members), but this typically occurs over months rather than days.

* **First Order Value as Percentage of Credit Limit:** Legitimate consumers' first BNPL orders typically represent **20-40%** of their approved credit limit. First orders exceeding **80%** of the credit limit are uncommon among legitimate consumers (under 5%) and may indicate an intent to maximize value extraction before default. However, consumers using BNPL for a specific planned large purchase may legitimately use a higher percentage of their limit on first order.

* **Digital Footprint Score at Onboarding:** Legitimate BNPL applicants typically have active online profiles on **3 or more** platforms with account histories exceeding **6 months**. Digital footprint scores below **0.2** (on a 0-1 scale) indicate minimal or no verifiable online presence and correlate strongly with synthetic identity risk. Thin-file populations (immigrants, young adults) may have lower digital footprint scores but typically have at least some verifiable online presence.

## Application to Detection

Detection rules for TP-0040 should layer multiple baseline deviations rather than relying on any single indicator. A new email address alone has moderate false positive rates (students, email migrators), but a new email address combined with a low digital footprint score and a device fingerprint associated with multiple accounts creates a high-confidence composite signal for synthetic identity fraud at onboarding.

Multi-provider stacking detection (DL-0088) is the highest-value detection rule but requires consortium-level data sharing. In the absence of consortium data, individual providers should focus on the signals they can observe in isolation: device clustering (DL-0091), spending step-up patterns (DL-0089), INR claim velocity (DL-0090), and onboarding risk signals (DL-0087).

Threshold tuning should account for market differences: providers operating in markets with younger demographics will have lower baseline email ages and digital footprint scores. Providers in markets with high delivery failure rates will have higher baseline INR dispute rates. Provider-specific baselines should be established and refined over the first 90 days of monitoring, with quarterly recalibration based on observed fraud and false positive rates.

The credit grooming phase (small purchases → on-time payments → limit increase → bust-out) represents the most challenging detection problem because it mimics legitimate consumer behavior during the grooming phase. The transition point — the sharp spending escalation from grooming to bust-out — is the highest-confidence detection window and is captured by DL-0089.
