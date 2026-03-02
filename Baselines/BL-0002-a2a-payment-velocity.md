# Baseline: A2A Payment Velocity

```yaml
---
id: BL-0002
title: "A2A Payment Velocity Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - a2a-payments
  - instant-payments
  - zelle
  - fednow
  - rtp
---
```

## Description

This baseline defines normal operating parameters for account-to-account (A2A) instant payment rails including Zelle, FedNow, and RTP (Real-Time Payments). It supports detection logic for TP-0024 (A2A Instant Payment Fraud), which targets abuse of irrevocable instant payment systems through social engineering, account takeover, and mule-driven cash-out schemes.

Behavioral baselines for A2A payments are critical because the irrevocable nature of these transactions means fraud losses cannot be recovered through traditional chargeback mechanisms. Establishing normal velocity, dollar ranges, and payee patterns allows detection engines to flag anomalous bursts before funds leave the institution.

## Normal Patterns

* **Daily Transaction Frequency:** A typical retail consumer initiates **2-4 Zelle transactions per day** and **fewer than 2 RTP/FedNow transactions per week**. Sustained activity exceeding **8 transactions in a rolling 24-hour window** is anomalous for non-business accounts.
* **P2P Dollar Range:** Normal person-to-person Zelle payments average **$50-$250** per transaction, with **90% of transactions falling below $500**. P2B (person-to-business) payments via RTP/FedNow average **$1,200-$3,500** for small business payroll and vendor payments.
* **New Payee Addition Rate:** Established accounts (> 6 months) add **1-2 new payees per month**. Adding **3 or more new payees within a 48-hour window** is a significant deviation, particularly when followed by immediate transfers.
* **Time-of-Day Distribution:** Approximately **78% of legitimate A2A transactions** occur between 7:00 AM and 10:00 PM local time. Transactions initiated between **1:00 AM and 5:00 AM** represent fewer than **4%** of normal volume and correlate with elevated fraud rates.
* **Cumulative Daily Outflow:** The median daily outbound A2A total for retail consumers is **$350**. Single-day outflows exceeding **$2,500** across all A2A rails combined occur in fewer than **2%** of legitimate account-days.

## Application to Detection

Detection rules for TP-0024 should layer velocity thresholds against payee novelty and time-of-day signals. A single transaction to a new payee during business hours may score low, but the same transaction at 3:00 AM following two other new-payee additions within 24 hours should escalate significantly. Rules should trigger alerts when daily A2A transaction counts exceed 3 standard deviations above the account's 30-day rolling average, or when cumulative daily outflow surpasses $2,500 for accounts with a historical median below $500.

Threshold tuning should account for the payment rail: Zelle transactions skew smaller and more frequent, while FedNow/RTP payments tend to be larger and less frequent. Separate velocity counters per rail will reduce false positives from legitimate users who shift volume between payment channels.
