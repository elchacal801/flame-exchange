# Baseline: Romance Scam Communication Patterns

```yaml
---
id: BL-0003
title: "Romance Scam Communication Patterns Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - romance-scam
  - social-engineering
  - communication-patterns
---
```

## Description

This baseline establishes normal communication and financial interaction patterns within online dating and relationship contexts, supporting detection logic for TP-0025 (GenAI APP Fraud - Romance) and TP-0011 (Romance Scam Mule Pipeline). Romance scams exploit emotional trust to manipulate victims into sending money, and GenAI-powered scam operations have dramatically accelerated the grooming phase.

Understanding the normal cadence of legitimate online relationships is essential for identifying the compressed, financially-oriented timelines characteristic of scam operations. These baselines help financial institutions and platforms differentiate between genuine relationship-driven transactions and coerced or manipulated fund transfers.

## Normal Patterns

* **Communication-to-Financial-Request Timeline:** In legitimate online relationships, the first financial interaction (shared expense, gift) typically occurs **90-180 days** after initial contact. Scam operations compress this to **14-30 days** on average, with GenAI-assisted operations reducing it further to **7-14 days**.
* **Gift Card and Wire Frequency:** Legitimate personal relationships involve **fewer than 2 gift card purchases per month** and **fewer than 1 wire transfer per quarter** to a romantic partner. A pattern of **3+ gift card purchases within a 7-day window** or **2+ wire transfers within 30 days** to a person never met in person is a strong deviation.
* **Escalation Pattern:** Normal relationship-related financial activity remains relatively stable in dollar terms. An escalation pattern where successive transfers increase by **50% or more** over a 4-week period (e.g., $200, $500, $1,000, $2,000) is characteristic of romance scam grooming.
* **Payment Channel Diversity:** Legitimate P2P transfers between partners typically use **1-2 consistent payment methods** (e.g., Zelle, Venmo). Scam victims are often directed across **3+ payment channels** within a 30-day period, including wire transfers, gift cards, cryptocurrency, and money orders.
* **Daily Messaging Volume:** Normal online dating communication averages **5-15 messages per day** during early stages. Scam operations often exhibit **50+ messages per day** with rapid escalation to off-platform communication channels within **48-72 hours** of initial contact.

## Application to Detection

Detection rules supporting TP-0025 and TP-0011 should monitor for the convergence of compressed communication timelines and escalating financial transfers. A single wire transfer to a new international beneficiary is not inherently suspicious, but when preceded by a pattern of increasing gift card purchases and the beneficiary was added within 30 days, the composite signal warrants escalation. Rules should establish per-account baselines for gift card purchase frequency and flag accounts that exceed 2 standard deviations above their 90-day rolling average.

For mule pipeline detection (TP-0011), focus on accounts receiving multiple small deposits from unrelated senders followed by rapid outbound wire transfers or crypto purchases. The receiving account's transaction pattern will deviate sharply from its historical baseline, typically showing a 500%+ increase in inbound volume over a 2-week period.
