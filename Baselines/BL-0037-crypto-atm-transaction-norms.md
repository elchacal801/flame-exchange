# Baseline: Crypto ATM Transaction Norms

```yaml
---
id: BL-0037
title: "Crypto ATM Transaction Norms by Age Cohort"
category: Baseline
date: 2026-04-06
author: "FLAME Project"
tags:
  - crypto-atm
  - kiosk
  - elder-fraud
  - cryptocurrency
  - physical-to-digital
---
```

## Description

Establishes normal behavioral patterns for crypto ATM/kiosk transactions, segmented by customer age cohort. FBI IC3 2025 data shows crypto ATM fraud generated 13,460 complaints with $389 million in losses (58% increase from 2024). The elder demographic (60+) is disproportionately impacted: 6,188 complaints (46%) and $257 million (66% of losses). These baselines help detection rules (DL-0212) distinguish legitimate crypto ATM usage from fraud-directed deposits.

## Normal Patterns

### Transaction Frequency
- **Under 40**: 2-6 crypto ATM transactions per month (established crypto users)
- **40-59**: 0-2 transactions per month
- **60+**: 0 transactions per month for 97%+ of customers. Any crypto ATM transaction from a 60+ customer with no prior crypto history is anomalous.

### Dollar Amounts per Transaction
- **Legitimate retail use**: Median $150-$500; 90th percentile under $2,000
- **Fraud-directed deposits**: Median $5,000-$15,000; frequently at or near daily machine limits
- **Anomaly threshold**: Single transaction > $3,000 from first-time user warrants enhanced monitoring

### Time-of-Day Distribution
- **Legitimate**: 60% between 10am-6pm local time (coincides with retail hours)
- **Fraud-directed**: More evenly distributed; 25% occur between 6pm-10pm (victims directed after business hours when bank branches are closed)

### Repeat Visit Patterns
- **Legitimate**: Same-day multiple transactions rare (<2% of users)
- **Fraud-directed**: 35% of fraud victims make 2+ deposits within 7 days (serial deposit pattern as scammers request additional payments)
- **Anomaly threshold**: 2+ crypto ATM deposits within 7 days from customer with no prior history

### Geographic Patterns
- **Legitimate**: Transactions at kiosks near home/work address
- **Fraud-directed**: Victims may travel to unfamiliar locations directed by the scammer; distance from home address > 15 miles is a weak signal

## Application to Detection

- **DL-0212** (Elder Crypto ATM Deposit Pattern): Uses age >= 60, cash withdrawal > $5,000, and no follow-up activity within 48 hours as primary signals
- Age-based risk scoring: Any crypto ATM transaction from a 60+ customer with no prior crypto activity should trigger enhanced review
- Serial deposit detection: 2+ crypto ATM transactions within 7 days from a customer with < 3 lifetime transactions
- Cross-institution correlation: Bank-side cash withdrawal + crypto ATM operator deposit within same day from same geographic area

### IC3 2025 Reference Data

| Age Group | Complaints | Losses | Avg Loss |
|-----------|-----------|--------|----------|
| Under 20 | 58 | $124K | $2,138 |
| 20-29 | 825 | $6.5M | $7,847 |
| 30-39 | 1,275 | $10.9M | $8,578 |
| 40-49 | 1,472 | $20.8M | $14,149 |
| 50-59 | 1,524 | $44.6M | $29,255 |
| 60+ | 6,188 | $257.5M | $41,613 |
