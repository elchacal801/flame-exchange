# Baseline: Precious Metals Purchase Norms

```yaml
---
id: BL-0038
title: "Precious Metals Purchase Norms by Customer Segment"
category: Baseline
date: 2026-04-06
author: "FLAME Project"
tags:
  - precious-metals
  - gold-courier
  - elder-fraud
  - physical-cashout
  - mcc-5094
  - mcc-5944
---
```

## Description

Establishes normal behavioral patterns for precious metals purchases (MCC 5094: Precious Stones/Metals, MCC 5944: Jewelry/Watch/Clock stores), segmented by customer type. FBI IC3 2025 data shows gold courier scams generated 725 complaints with $311.8 million in losses — an extraordinary average of ~$430,000 per victim. These baselines help detection rules (DL-0213) distinguish legitimate precious metals activity from scam-directed purchases.

## Normal Patterns

### Purchase Frequency
- **General retail banking customers**: 97%+ have zero precious metals merchant transactions in a 12-month period
- **Occasional purchasers** (jewelry for gifts/events): 1-3 transactions per year, typically correlated with holidays or life events (December, February, engagement/wedding season)
- **Active collectors/investors**: 4-12 transactions per year with consistent patterns over multiple years

### Dollar Amounts per Transaction
- **Jewelry retail (MCC 5944)**: Median $200-$1,500; 95th percentile under $10,000
- **Precious metals dealers (MCC 5094)**: Median $2,000-$8,000 for established investors; purchases > $25,000 are uncommon for retail customers
- **Gold courier scam amounts**: Median $50,000-$200,000; often at or near account balance. IC3 average: $430,000.
- **Anomaly threshold**: Any MCC 5094/5944 transaction > $10,000 from a customer with no prior precious metals history warrants review

### Funding Source Patterns
- **Legitimate**: Paid via credit/debit card, check, or existing account balance
- **Fraud-directed**: Preceded by large cash withdrawal (often $50K-$500K+) or wire transfer. Cash withdrawal → same-day precious metals purchase is a strong fraud indicator.

### Customer Demographics
- **Gold courier scam victims**: Predominantly 60+, high-net-worth, no prior precious metals purchasing history
- **Legitimate investors**: Established patterns across age groups; typically have prior transactions and may hold precious metals accounts at dealers

### Behavioral Red Flags (FinCEN-aligned)
- Customer states purchase is for "safekeeping" or "government protection"
- Customer mentions being told not to inform bank staff of the reason
- Customer appears nervous, is on the phone during transaction, or reads instructions from a note
- Multiple large precious metals purchases within 7-14 days (serial courier pickups)

## Application to Detection

- **DL-0213** (Gold Purchase Anomaly): Uses cash withdrawal or wire > $10K to MCC 5094/5944 within 72h, from customer with no prior precious metals history. Elevated priority for age >= 60.
- Bank teller alert: Large cash withdrawal + stated intent to purchase gold/precious metals from a customer with no history = immediate fraud team referral
- FinCEN SAR trigger: Cash purchase of precious metals > $10,000 from new customer without established business relationship
- Cross-channel correlation: Government impersonation call (CDR analytics) + large withdrawal + precious metals purchase within 72 hours
