# Baseline: Gift Card Transaction Velocity and Pattern Norms

```yaml
---
id: BL-0035
title: "Gift Card Transaction Velocity and Pattern Norms"
category: Baseline
date: 2026-03-22
author: "FLAME Project (sourced from NRF Retail Fraud Taxonomy v1.0)"
related_tps:
  - id: TP-0068
    relationship: related-to
  - id: TP-0013
    relationship: related-to
tags:
  - gift-card
  - retail
  - balance-probing
  - card-tampering
  - nrf-rft
  - baseline
---
```

## Summary

This baseline defines normal and anomalous patterns for gift card transaction activity including balance checks, merges/transfers, activation-to-redemption timing, and resale platform listings. The NRF Retail Fraud Taxonomy v1.0 documents gift card fraud as a primary scheme with 24 techniques across the full lifecycle. These baselines calibrate DL-0144 (balance probing) and DL-0145 (merge anomaly) detection thresholds. Key insight: the physical-to-digital bridge in gift card tampering creates a unique timing anomaly — tampered cards are redeemed within minutes of activation by a different device/IP than the purchaser.

## Normal Patterns

* **Balance check frequency (legitimate customers):** Legitimate customers check gift card balances **1–3 times per card**, typically before a purchase. Automated probing generates **50+ checks per hour** from a single source, often across hundreds of distinct card numbers.

* **Gift card merge frequency:** Legitimate merges occur **1–2 times per customer per year**, typically combining 2–3 cards. Fraudulent merging involves **5+ source cards merged into a single destination** within minutes — consolidating illicit value for monetization.

* **Activation-to-first-redemption timing:** Legitimate gift cards are typically redeemed **days to weeks** after activation (median: 7–14 days). Tampered cards (NRF FT1203) show first redemption **within minutes to hours** of activation, from a device/IP different from the purchaser.

* **Purchase pattern with gift cards:** Legitimate gift card purchases show **diverse product categories** reflecting personal use. Fraudulent redemptions concentrate on **high-value, easily resold items** (electronics, jewelry, luxury goods) — items with strong secondary market demand.

* **Resale platform listing timing:** Legitimate gift card resale occurs **days to weeks** after receipt. Fraudulent listings appear on exchange platforms **within hours** of gift card merge or transfer activity.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Balance checks per card per hour | 1–3 total | 4–10 | >10 in 1 hour |
| Balance checks per source IP per hour | 1–5 | 6–20 | >50 |
| Unique cards checked per source IP per hour | 1–3 | 4–10 | >20 |
| Gift card merges per destination card per day | 0–1 | 2–3 | 4+ source cards in <1 hour |
| Activation-to-first-redemption (same device/IP) | Days–weeks | Hours | Minutes (different device/IP = tamper indicator) |
| High-value item purchases with gift cards per day | 0–1 | 2–3 | 4+ across different cards from same device/IP |
| Gift card resale listing after merge/transfer | Days–weeks | <24 hours | <4 hours |

## Measurement Methodology

Balance check velocity is measured by monitoring gift card balance check API endpoints and IVR phone systems. Count requests per source IP, per device fingerprint, and per VoIP number over rolling 1-hour windows. Cross-reference with NRF RFT detection sources: Network Traffic Attributes (FD1007), Time-Based Attributes (FD1004), Device Attributes (FD1005), Velocity Attributes (FD1006), and VoIP Attributes (FD1008).

Merge/transfer velocity measured by counting distinct source cards per destination card over rolling 1-hour windows. Flag destination cards receiving value from 3+ sources within 60 minutes.

Activation-to-redemption timing calculated as the interval between card activation event and first redemption event, with device/IP comparison between the two events. Mismatch between activating purchaser and first redeemer is the primary tamper indicator.

## Data Sources

* **Gift card management system logs:** Balance check requests, activation events, merge/transfer events, redemption events with associated device/IP/customer data.
* **Web application firewall (WAF) logs:** Request velocity and bot detection signals on balance check endpoints.
* **IVR/telephony systems:** Phone-based balance check activity with caller number attributes.
* **Transaction monitoring systems:** Gift card redemption patterns linked to product categories and purchase amounts.
* **Resale platform monitoring:** Gift card listings on exchange platforms correlated with internal merge/transfer timing.

## Application

DL-0144 should use these baselines to calibrate balance probing detection. The primary threshold is >50 balance checks per source IP per hour or >20 unique cards per source IP per hour. VoIP source numbers and off-hours timing (NRF FD1004, FD1008) are strong additional indicators.

DL-0145 should use merge velocity baselines: 3+ source cards to a single destination within 60 minutes is the primary threshold, with higher severity for 5+ sources or total transferred value >$500.

For tampered card detection, the activation-to-first-redemption timing with device/IP mismatch is the highest-confidence signal. Cards redeemed within minutes of activation by a different device than the purchaser should be flagged as high-priority tamper candidates.
