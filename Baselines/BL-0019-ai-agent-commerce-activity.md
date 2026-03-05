# Baseline: AI Agent Commerce Activity

```yaml
---
id: BL-0019
title: "AI Agent Commerce Activity Baseline"
category: Baseline
date: 2026-03-04
author: "FLAME Project"
tags:
  - agentic-ai
  - ai-agent
  - commerce-automation
  - transaction-velocity
  - agent-purchasing
  - ecommerce
---
```

## Description

This baseline defines normal versus anomalous behavioral patterns for AI agent-initiated commerce transactions, supporting detection logic for TP-0039 (Agentic Commerce Fraud). As agentic commerce platforms such as Amazon Buy for Me, Visa Intelligent Commerce, and Mastercard Agent Pay move from pilot to production, fraud teams require calibrated baselines to distinguish legitimate agent purchasing behavior from compromised or manipulated agent sessions. These baselines are derived from early pilot program behavioral data, human purchasing velocity studies, and the Recorded Future Annual Payment Fraud Intelligence Report 2025 analysis of agentic commerce attack surfaces.

## Normal Patterns

* **Agent-Initiated Transaction Frequency:** Legitimate agent purchasing sessions typically involve **1-5 purchases per user session**, reflecting the consumer's stated purchasing intent. Sessions with more than 5 purchases are uncommon outside corporate procurement contexts and should trigger enhanced monitoring.

* **Agent Session Duration Before Purchase:** Agents performing comparison shopping typically spend **2-15 minutes** evaluating options before executing a purchase. This includes merchant catalog browsing, price comparison across sources, and review analysis. Sessions where purchases occur within seconds of session initiation -- bypassing comparison logic -- are anomalous.

* **Agent Purchasing Category Distribution:** Normal agent purchasing activity is concentrated in **1-3 product categories** per user, closely matching the user's historical purchasing preferences. Agent sessions that suddenly purchase across 5+ unrelated categories, or that purchase in categories the user has never engaged with, indicate potential intent manipulation.

* **Human-vs-Agent Transaction Velocity Ratios:** Agents complete transactions **3-5x faster** than manual human browsing due to automated form filling and streamlined checkout flows, but are still limited by page load times, API response latencies, and merchant-side processing. Velocities exceeding **10x human baseline** -- more than 5 transactions per minute or simultaneous purchases across more than 3 merchants within a 60-second window -- suggest automated fraud exploitation rather than legitimate agent-assisted shopping.

* **Agent Merchant Selection Patterns:** Legitimate agents select merchants from a relatively stable pool matching the user's preferences, with **fewer than 20%** of transactions going to merchants the user has never previously purchased from. Agent sessions routing more than 50% of transactions to novel merchants, especially recently created merchant accounts, are anomalous.

* **Agent Price Deviation Tolerance:** Normal agent-initiated transactions fall within **+/- 15%** of the market average price for the selected product. Agents executing purchases at prices more than 30% above market average -- potentially due to price verification logic manipulation -- or consistently selecting the highest-priced option across categories warrant investigation.

## Application to Detection

Detection rules for TP-0039 should layer transaction velocity monitoring with merchant selection analysis and intent consistency verification. A single indicator (e.g., a purchase in a new category) has a high false positive rate, as users legitimately explore new purchasing categories through agent assistance. However, the combination of high velocity + novel merchants + category divergence + price anomaly creates a high-confidence composite signal for agent compromise or manipulation.

Threshold tuning should account for agent platform type: corporate procurement agents legitimately execute higher-volume, multi-category purchasing sessions, while consumer-facing shopping agents should adhere to tighter velocity and category constraints. These platform-specific baselines should be established per agent provider and refined as agentic commerce adoption scales and behavioral norms stabilize.

Financial institutions processing agent-initiated transactions should flag sessions where the agent's total spend approaches the user's delegation authority limit through rapid transactions, as this pattern -- spending to the maximum authorized amount at machine speed -- is a strong indicator of compromised agent activity.
