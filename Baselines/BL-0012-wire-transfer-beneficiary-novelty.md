# Baseline: Wire Transfer Beneficiary Novelty

```yaml
---
id: BL-0012
title: "Wire Transfer Beneficiary Novelty Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - wire-fraud
  - beneficiary-analysis
  - payment-diversion
  - bec
---
```

## Description

This baseline defines normal patterns for new beneficiary additions and first-time wire transfers, supporting detection logic for TP-0001 (Treasury Management ATO), TP-0002 (BEC), and TP-0006 (Real Estate Wire Fraud). Wire fraud schemes across all three threat patterns share a common critical step: directing funds to a beneficiary account not previously known to the sender. Whether through account takeover, business email compromise, or real estate closing diversion, the introduction of a novel beneficiary is the pivotal moment in the fraud chain.

Behavioral baselines for beneficiary novelty are essential because legitimate commercial wire activity is heavily concentrated among established, recurring beneficiaries. The rate at which new beneficiaries appear, the dollar amounts directed to first-time recipients, and the approval workflow timing all provide high-signal behavioral indicators that are difficult for attackers to manipulate without insider access.

## Normal Patterns

* **New Beneficiary Addition Rate:** Established commercial accounts (operating 1+ year) add **1-3 new wire beneficiaries per month**. Adding **5+ new beneficiaries within a 7-day window** exceeds the 98th percentile. Retail consumer accounts add new wire beneficiaries at a rate of fewer than **1 per quarter** on average.
* **Domestic vs. International Beneficiary Ratio:** For U.S.-based commercial accounts, approximately **75-85%** of new beneficiary additions are domestic. An account that historically adds only domestic beneficiaries suddenly registering **2+ international beneficiaries** within 30 days represents a significant deviation, particularly to jurisdictions not previously in the account's geographic payment footprint.
* **First-Time Beneficiary Wire Amounts:** The median wire amount to a first-time beneficiary is **$12,000-$25,000** for commercial accounts and **$3,000-$8,000** for retail accounts. First-time wires exceeding **$50,000** for commercial accounts or **$15,000** for retail accounts represent fewer than **10%** of initial-beneficiary transactions and warrant enhanced verification.
* **Approval Workflow Timing:** For commercial accounts with dual-control requirements, the median time between wire initiation and secondary approval is **1-4 hours** during business days. Approvals occurring within **30 seconds** of initiation represent fewer than **1%** of normal transactions and are consistent with single-actor ATO scenarios where the attacker controls both authentication factors.
* **Beneficiary Persistence:** Approximately **70%** of newly added beneficiaries receive a second wire within **90 days**, indicating legitimate ongoing business relationships. Beneficiaries that receive a single large wire with no subsequent activity within 90 days represent potential one-time diversion events and account for fewer than **15%** of new beneficiary additions in normal commercial operations.

## Application to Detection

Detection rules for TP-0001, TP-0002, and TP-0006 should treat beneficiary novelty as a primary risk amplifier. Any wire to a first-time beneficiary should receive elevated scoring, with additional weight applied when the wire amount exceeds the account's historical median by more than 200%, the beneficiary is international when the account's history is predominantly domestic, or the approval workflow completes in under 60 seconds. Rules should trigger high-priority alerts when a first-time beneficiary wire exceeds $50,000 and the beneficiary was added within the same business day as the wire initiation.

For real estate wire fraud (TP-0006), detection engines should cross-reference wire timing against known real estate closing patterns. Wires initiated within 24 hours of a beneficiary change, where the new beneficiary routing number differs from any previously communicated closing instructions, should generate an immediate hold. Threshold tuning should maintain separate baselines for commercial and retail accounts, as commercial accounts naturally have higher wire volumes and more frequent beneficiary additions. The composite signal of new beneficiary + amount deviation + timing anomaly provides the highest-confidence detection across all three supported threat patterns.
