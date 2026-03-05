# Baseline: Digital Wallet & Contactless Transaction Patterns

```yaml
---
id: BL-0017
title: "Digital Wallet & Contactless Transaction Patterns Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - digital-wallet
  - contactless
  - nfc-relay
  - wallet-provisioning
  - otp-interception
  - ghost-tapping
---
```

## Description

This baseline defines normal versus anomalous patterns for digital wallet provisioning and contactless transaction behavior relevant to detecting digital wallet fraud and NFC relay attacks. It supports detection logic for TP-0037 (Digital Wallet Fraud & NFC Relay Attacks) by establishing behavioral norms for wallet provisioning frequency, OTP-to-provisioning time intervals, contactless transaction geographic spread, and multi-terminal transaction velocity. These baselines are derived from the Recorded Future 2025 Annual Payment Fraud Intelligence Report, Cleafy Labs SuperCardX analysis, TransUnion 2025 Global Identity and Fraud Report, and payment network transaction analytics. The critical insight is that wallet provisioning is the key disruption point, and the timing relationship between OTP delivery and provisioning completion provides a high-signal detection opportunity.

## Normal Patterns

* **Wallet Provisioning Frequency:** Legitimate cardholders provision **1-3 cards per account per year** onto digital wallets. Multiple provisioning events within a single day or week are rare for individual consumers (fewer than 2% of cardholders). Corporate card administrators may provision more frequently, but are identifiable by account type. More than **5 provisioning events from the same account within 30 days** is anomalous and warrants investigation.

* **OTP-to-Provisioning Time Interval:** Legitimate self-provisioning typically takes **30-120 seconds** from OTP delivery to provisioning completion, reflecting the time for a user to receive the OTP via SMS or push notification, switch to the wallet app, and enter the code. Automated interception-to-provision attack chains complete in **under 15 seconds**, as the OTP is programmatically captured and forwarded to the provisioning request without human interaction. A provisioning event completing within **under 15 seconds** of OTP delivery is a strong indicator of automated interception.

* **Contactless Transaction Geographic Spread:** Individual cardholders typically conduct contactless transactions at POS terminals in **fewer than 3 unique cities per day** during normal shopping activity. Geographic spread exceeding 3 cities within a single day, or terminal locations more than 100 kilometers apart within a 2-hour window, indicates potential NFC relay or unauthorized wallet token use. Exceptions include business travelers, who show predictable travel patterns correlating with flight data.

* **Multi-Terminal Transaction Velocity:** Normal shopping behavior produces a **maximum of 2-3 contactless transactions per hour** across different POS terminals for a single wallet token. This reflects the physical constraints of moving between retail locations. NFC relay operations produce **5-10+ transactions per hour** across **3+ distinct terminals**, often in different cities, which is physically impossible for a single cardholder.

* **Wallet Token Age at Transaction:** Established wallet tokens (provisioned more than 7 days prior) account for **over 95%** of legitimate contactless transactions. Newly provisioned tokens (under 24 hours old) used for high-value purchases or gift card transactions represent an elevated risk profile. Fewer than **3%** of legitimate contactless transactions involve tokens provisioned within the preceding 24 hours.

* **Contactless Transaction Amount Distribution:** Legitimate contactless transactions average **$15-$45** per tap, with the majority under **$100** reflecting the contactless transaction limits in many markets. NFC relay fraud operations often target higher-value individual transactions ($100-$500) or high-value gift card purchases, deviating from the typical contactless amount distribution.

## Application to Detection

Detection rules for TP-0037 should layer provisioning-time signals (OTP-to-provisioning timing, device reputation, geographic consistency) with post-provisioning behavioral signals (contactless velocity, geographic spread, transaction amount patterns). The OTP-to-provisioning time interval is the highest-signal single indicator, with automated interception completing in under 15 seconds versus the 30-120 second legitimate baseline. However, provisioning-time detection alone will miss attacks where the OTP interception delay is artificially increased to evade timing-based rules.

Post-provisioning monitoring should focus on the first 48-72 hours after a new wallet token is created, when the majority of NFC relay and ghost-tapping fraud occurs. Multi-terminal velocity monitoring using the 3+ terminals in 30 minutes threshold has very low false positive rates, as tokenized wallet payments generate unique tokens per device, making multi-device concurrent use of the same token an extremely strong fraud signal.

Threshold tuning should account for market-specific contactless limits, regional shopping patterns, and cardholder behavioral history. Business travelers and cardholders with multiple authorized family wallet tokens require adjusted baselines to avoid false positives.
