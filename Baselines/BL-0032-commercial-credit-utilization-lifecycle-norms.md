# Baseline: Commercial Credit Utilization Lifecycle Norms

```yaml
---
id: BL-0032
title: "Commercial Credit Utilization Lifecycle Norms"
category: Baseline
date: 2026-03-22
author: "FLAME Project (sourced from UNODC Organized Fraud Issue Paper 2024, UK SFO prosecutions)"
related_tps:
  - id: TP-0064
    relationship: related-to
  - id: TP-0003
    relationship: related-to
tags:
  - long-firm-fraud
  - commercial-credit
  - credit-utilization
  - bust-out
  - trade-finance
  - baseline
---
```

## Summary

This baseline defines normal and anomalous credit utilization lifecycle patterns for commercial accounts. It establishes norms for credit utilization progression, payment behavior variance, credit limit increase request frequency, and trade finance drawdown patterns. Long-firm fraud involves organized criminal groups building creditworthiness over 6–24 months before exploiting that trust in a rapid credit burst. The artificially smooth buildup period followed by a discontinuous utilization spike is the hallmark behavioral indicator. Organizations should calibrate DL-0135 detection thresholds against these norms. This baseline is derived from UNODC organized fraud typology, UK Serious Fraud Office prosecution data, and commercial credit industry benchmarks.

## Normal Patterns

* **Credit utilization progression (legitimate business):** Legitimate businesses display **variable credit utilization** over time, reflecting seasonal demand, business cycles, and operational needs. Monthly utilization standard deviation is typically **>10% of the credit limit** over a 6-month window. Long-firm fraud accounts display **artificially low variance** (standard deviation <5%) during the buildup phase, reflecting deliberate maintenance of a clean credit profile.

* **Credit utilization range (legitimate business):** Legitimate commercial accounts typically operate between **20–70% credit utilization** on average, with occasional spikes above 80% during peak business periods. Long-firm fraud accounts maintain utilization **below 30%** during buildup, then spike to **>85%** during the burst phase.

* **Payment timing variance:** Legitimate businesses display **normal variance in payment timing** — some payments early, some on due date, occasional late payments. Long-firm fraud accounts pay **consistently early or on time** with near-zero variance during the buildup phase, as the OCG deliberately cultivates a perfect payment record.

* **Credit limit increase request frequency:** Legitimate businesses request credit limit increases **1–2 times per year**, typically tied to business growth milestones. Long-firm fraud accounts may request increases **3+ times in 6 months**, with each request supported by fabricated financial documentation showing steady revenue growth.

* **Trade finance drawdown pattern:** Legitimate trade finance facilities show **variable drawdown amounts** reflecting genuine trade activity. Long-firm fraud accounts show a pattern of **steadily increasing drawdowns** culminating in simultaneous maximum drawdowns across multiple facilities (the burst).

* **Cross-creditor activity:** Legitimate businesses may have credit relationships with **2–5 institutions** with staggered credit facility establishment. Long-firm fraud accounts may rapidly establish credit facilities with **5+ institutions** in a compressed timeframe, maximizing total available credit for the burst.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Monthly utilization standard deviation (6-month window) | >10% of credit limit | 5–10% (unusually consistent) | <5% (artificially smooth) |
| Average credit utilization during first 12 months | 20–70% | <20% (building capacity) | <15% with subsequent spike to >85% |
| Payment timing variance (std dev of days-before-due) | >3 days | 1–3 days (very consistent) | <1 day (robotic precision) |
| Credit limit increase requests per 6 months | 0–1 | 2 | 3+ |
| Utilization month-over-month change rate | Gradual, variable | Steady 5–10% increase per month | <30% to >80% in single month |
| Simultaneous maximum drawdowns across facilities | Not expected | 2 facilities at >80% same month | 3+ facilities at >85% same month |
| Trade finance facility count established within 12 months | 1–3 | 4–5 | 6+ with different banks |

## Measurement Methodology

Measure monthly credit utilization as the average of daily utilization snapshots within each calendar month. Calculate the trailing 6-month standard deviation to detect artificially smooth patterns characteristic of the long-firm buildup phase. The key detection metric is the ratio between trailing standard deviation and current utilization — accounts with low historical variance that suddenly spike represent the classic long-firm signature.

Payment timing variance is measured as the standard deviation of the number of days between payment receipt and the payment due date over a rolling 6-month window. Near-zero variance (payments consistently N days before due date) is anomalous for legitimate business operations.

Cross-creditor activity requires inter-institutional data sharing or credit bureau monitoring. Count the number of new credit facilities established within rolling 12-month windows and flag accounts establishing facilities with multiple institutions in compressed timeframes.

## Data Sources

* **Commercial credit bureau data (D&B, Experian Business):** Credit utilization history, payment behavior scores, credit limit changes, and new credit facility establishment across institutions.
* **Internal credit management systems:** Account-level utilization snapshots, payment timing records, credit limit modification logs.
* **Trade finance systems:** Drawdown amounts, timing, and counterparty information for letters of credit and trade finance facilities.
* **Corporate registry databases:** Company registration dates, director changes, and beneficial ownership information for credit applicants.
* **Financial statement repositories:** Revenue and balance sheet data for independent verification against credit application claims.

## Application

DL-0135 should calibrate long-firm fraud detection thresholds against these baselines. Specifically, DL-0135 should trigger review when:
- Monthly utilization standard deviation is below 5% over a 6-month window AND current month utilization exceeds 80% (the smooth-buildup-then-burst pattern)
- Previous month utilization was below 50% and current month exceeds 80% (discontinuous spike)
- Credit limit increase requests exceed 2 in a 6-month period for accounts with low utilization variance

Enhanced due diligence should be triggered for:
- Trade finance facilities where simultaneous maximum drawdowns occur across 3+ banks in the same month
- New commercial accounts that establish credit facilities with 6+ institutions within their first 12 months
- Accounts where financial statements supporting credit applications come from a small set of audit firms also associated with other high-utilization commercial accounts

Analysts should pay particular attention to sectors identified by UNODC as vulnerable to long-firm fraud: steel/commodities trading, electronics distribution, and cross-border trade with complex documentation chains.
