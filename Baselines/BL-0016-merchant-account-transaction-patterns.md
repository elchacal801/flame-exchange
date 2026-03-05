# Baseline: Merchant Account Transaction Patterns

```yaml
---
id: BL-0016
title: "Merchant Account Transaction Patterns Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - purchase-scam
  - merchant-fraud
  - subscription-trap
  - chargeback
  - merchant-onboarding
  - card-testing
  - acquirer-risk
---
```

## Description

This baseline defines normal versus anomalous transaction patterns for merchant accounts, supporting detection logic for TP-0036 (Purchase Scam Merchant Networks) and TP-0038 (Card Testing Operations). It establishes behavioral norms for new merchant transaction ramp-up velocity, chargeback ratios by merchant age, recurring billing enrollment rates, and dispute rates by merchant category. These baselines are derived from Recorded Future's 2025 Annual Payment Fraud Intelligence Report (3,600+ scam merchants identified across 40+ countries and 230+ acquirers), payment network monitoring thresholds (Visa and Mastercard), and acquirer risk management industry data. Organizations should calibrate these thresholds to their specific acquirer portfolio composition, geographic risk profile, and merchant category mix.

## Normal Patterns

* **New Merchant Ramp-Up Velocity:** Legitimate new merchants exhibit a gradual transaction ramp-up curve. During the first 30 days, normal merchants process **fewer than 50 transactions per day**, increasing to **200+ transactions per day** by day 90 as the business establishes its customer base and marketing reaches maturity. Merchants that exceed **200 transactions per day** within their first 14 days — particularly when combined with a high ratio of unique cards to total transactions (exceeding **80%**) — are anomalous and consistent with scam merchant or card testing operations. Legitimate exceptions include marketplace migrations, seasonal businesses launching during peak periods, and merchants with pre-existing customer bases transferring from another acquirer.

* **Chargeback Ratio by Merchant Age:** Established merchants (older than 6 months) maintain chargeback ratios **under 0.5%** of total transactions. New merchants (under 6 months) may experience slightly elevated chargeback rates of **under 1.5%** due to operational growing pains, unclear return policies, and customer unfamiliarity. Chargeback ratios exceeding **1.5%** for merchants under 6 months of age, or exceeding **0.8%** for established merchants, warrant investigation. Scam merchants identified by Recorded Future in 2025 typically exhibited chargeback ratios of **3-15%** before acquirer termination, with the chargeback curve accelerating rapidly after the first 30-60 days of operation. Visa's Dispute Monitoring Program threshold is **0.9%** and Mastercard's Excessive Chargeback Program threshold is **1.5%**.

* **Recurring Billing Enrollment Rate:** For legitimate subscription merchants, recurring billing constitutes **5-15%** of total transactions. This reflects the natural mix of one-time purchases and subscription enrollments. Subscription trap scam merchants show recurring billing rates exceeding **30-50%** of transactions, often with initial trial charges below **$10** followed by recurring charges exceeding **$50**. A ratio of maximum charge amount to minimum charge amount exceeding **5:1** combined with recurring billing rates above **25%** is a strong subscription trap indicator. Legitimate subscription businesses (SaaS, streaming, membership services) may have recurring billing rates of **60-90%** but will show consistent charge amounts rather than the trial-to-premium escalation pattern.

* **Dispute Rate by Merchant Category:** Normal dispute rates vary significantly by Merchant Category Code (MCC), ranging from **0.2% to 2.0%** across categories. Low-dispute categories include grocery and pharmacy (**0.2-0.4%**). Moderate-dispute categories include general retail and restaurants (**0.5-1.0%**). Higher-dispute categories include digital goods, travel, and subscription services (**1.0-2.0%**). Scam merchants frequently misclassify their MCC — for example, a purported clothing retailer (MCC 5651, expected dispute rate **0.5-0.8%**) operating with a dispute rate exceeding **3%** is strongly anomalous. MCC misclassification itself (merchant's actual product/service does not match the assigned MCC) is an independent risk indicator regardless of dispute rates.

* **Transaction Amount Distribution:** Legitimate merchants exhibit transaction amount distributions consistent with their product catalog and pricing. Scam merchants often show bimodal distributions: a cluster of low-value transactions (trial charges, card testing) and a cluster of higher-value transactions (scam purchases, subscription charges). A coefficient of variation (standard deviation divided by mean) in transaction amounts exceeding **1.5** for a merchant with fewer than 1,000 total transactions in its first 90 days is anomalous and may indicate mixed-mode fraud operations.

* **Merchant Account Lifecycle Duration:** Legitimate merchants maintain active accounts for **years**, with median account lifespans exceeding **24 months**. Scam merchant accounts identified in 2025 had median lifespans of **30-90 days** before termination due to chargeback thresholds, fraud investigations, or voluntary abandonment. Merchant accounts that become inactive (zero transactions for 14+ consecutive days) within their first 120 days of operation, particularly following a period of high transaction velocity, are consistent with the "extract and abandon" pattern used by scam merchant networks.

## Application to Detection

Detection rules for TP-0036 and TP-0038 should combine velocity, chargeback, and behavioral signals into composite risk scores rather than relying on single-indicator thresholds. A new merchant with high transaction velocity alone may be a legitimate fast-growing business, but high velocity combined with elevated chargeback trajectories, MCC mismatches, and recently registered domains creates a high-confidence scam merchant signal.

Threshold tuning should account for merchant category: digital goods and travel merchants legitimately have higher dispute rates than physical goods retailers. Geographic adjustments are also necessary — merchants processing cross-border transactions typically experience 2-3x higher chargeback rates than domestic-only merchants. Seasonal adjustments should be applied for categories with known peak periods (retail during holidays, travel during summer).

Acquirers should implement risk-based settlement holds for new merchants, delaying payouts when velocity or chargeback trajectory signals exceed baseline thresholds. This preventive control limits financial exposure when a scam merchant is detected mid-operation. Cross-acquirer intelligence sharing through programs like Mastercard's MATCH (Member Alert to Control High-Risk Merchants) and Visa's VMAS (Visa Merchant Screening Service) is essential for propagating scam merchant indicators across the ecosystem and preventing merchant account cycling across acquirers.
