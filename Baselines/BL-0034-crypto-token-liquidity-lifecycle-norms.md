# Baseline: Crypto Token Liquidity Lifecycle Norms

```yaml
---
id: BL-0034
title: "Crypto Token Liquidity Lifecycle Norms"
category: Baseline
date: 2026-03-22
author: "FLAME Project (sourced from 2026 Technical Landscape Report, Mazorra et al. 2022, Yu & Lee 2025)"
related_tps:
  - id: TP-0049
    relationship: related-to
  - id: TP-0017
    relationship: related-to
tags:
  - rug-pull
  - crypto
  - defi
  - liquidity
  - token-lifecycle
  - baseline
---
```

## Summary

This baseline defines normal and anomalous patterns for cryptocurrency token liquidity lifecycles on decentralized exchanges (DEXs). Rug pulls constituted 68% of all crypto scams in 2025 (350+ documented cases in 2024). Detection methods include Uniswap trading/liquidity feature engineering (Mazorra et al., 2022), EVM bytecode balance-flow heuristics (Yu & Lee, 2025), and temporal graph learning (TokenScout, Wu et al., 2024). ChainAware achieves 68% detection across Ethereum, BSC, Polygon, and Solana. Critical finding: OSINT signals precede on-chain anomalies by days or weeks. These baselines calibrate DL-0142 (rug pull early warning) detection thresholds.

## Normal Patterns

* **Holder distribution (legitimate tokens):** Legitimate tokens show **Gini coefficient <0.70** for holder distribution after the first 30 days. Rug pull tokens maintain **Gini >0.85** (top 5 holders control >60% of supply) throughout their lifecycle, as the deployer retains the majority for exit.

* **Liquidity provision stability:** Legitimate projects maintain liquidity within **±20% of initial provision** for the first 90 days, with gradual organic growth. Rug pull tokens show **sudden liquidity removal of >80% in a single transaction** — the defining on-chain event of a rug pull.

* **Trading volume progression:** Legitimate tokens show **variable daily trading volume** with organic growth correlating to market events. Rug pull tokens show an **artificial promotion spike** (wash trading or social media-driven FOMO) followed by volume collapse before or coinciding with liquidity removal.

* **Smart contract characteristics:** Legitimate tokens typically have **renounced ownership, locked liquidity, and no hidden mint/pause/blacklist functions**. Rug pull tokens retain owner control: unrenounced ownership (owner can modify contract), unlocked liquidity (owner can withdraw at any time), and hidden functions (mint to inflate supply, pause to prevent selling, blacklist to block specific addresses).

* **Social media and community activity:** Legitimate projects maintain **consistent social media presence** with organic community engagement. Rug pull projects show a **burst of promotional activity** (paid influencers, bot engagement, airdrop campaigns) followed by abrupt silence from the development team — OSINT signals that precede on-chain anomalies by days or weeks.

* **Developer wallet activity:** Legitimate project developers show **ongoing on-chain activity** (contract upgrades, governance, treasury management). Rug pull deployer wallets show **cessation of activity** after the initial deployment and liquidity provision, reactivating only for the exit transaction.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Holder distribution Gini coefficient (after 30 days) | <0.70 | 0.70–0.85 | >0.85 |
| Top 5 holder concentration | <40% | 40–60% | >60% |
| Maximum single-transaction liquidity removal | <10% | 10–50% | >80% |
| Liquidity lock status | Locked (>6 months) | Locked (<3 months) | Unlocked |
| Contract ownership | Renounced | Active but multi-sig | Single owner, unrenounced |
| Hidden contract functions (mint/pause/blacklist) | None detected | Pause function present | Mint + pause + blacklist all present |
| Social media activity (7-day vs 30-day avg) | >80% of baseline | 40–80% of baseline | <20% of baseline (silence) |
| Developer wallet inactivity | <7 days | 7–14 days | >14 days after active period |
| Trading volume spike followed by >90% collapse | Not expected | 50–90% collapse within 7 days | >90% collapse within 48 hours |

## Measurement Methodology

Holder distribution measured by querying token transfer events from the blockchain and computing the Gini coefficient of the balance distribution. Top-N holder concentration calculated as the sum of the top N addresses' balances divided by total circulating supply. Exclude known exchange hot wallets and burn addresses.

Liquidity monitoring tracks the token's primary DEX pair (typically Uniswap V2/V3, PancakeSwap, or Raydium). Monitor `RemoveLiquidity` events and calculate the percentage of total liquidity removed. Single-transaction removals >80% are the defining indicator.

Smart contract analysis uses EVM bytecode decompilation to identify function signatures for mint, pause, blacklist, and ownership transfer. Check the Ownable pattern — whether `renounceOwnership()` has been called. Verify liquidity lock by checking if LP tokens are held in a timelock contract.

OSINT monitoring tracks project-associated Twitter/X accounts, Telegram groups, and Discord servers. Calculate 7-day rolling activity as a percentage of the 30-day average. Alert on >80% activity drop.

## Data Sources

* **Blockchain nodes / analytics APIs (Etherscan, BscScan, Dune Analytics):** On-chain token transfer events, liquidity pool events, contract bytecode.
* **DEX analytics (DeFiLlama, Uniswap subgraph):** Liquidity pool TVL tracking, trading volume data.
* **Social media monitoring (Twitter/X API, Telegram Bot API):** Project social media activity metrics.
* **Contract analysis tools (Slither, Mythril):** EVM bytecode analysis for hidden function detection.
* **ChainAware, RPHunter, TokenScout:** Academic rug pull detection tools for cross-validation.

## Application

DL-0142 should use these baselines to calibrate rug pull early warning thresholds. The highest-confidence signal is single-transaction liquidity removal >80% combined with holder Gini >0.85 — this represents a confirmed or near-confirmed rug pull in progress.

For early warning (pre-rug), prioritize OSINT signals: social media activity collapse (>80% drop) combined with developer wallet inactivity (>14 days) and unlocked liquidity should trigger investigation before the on-chain exit occurs. Research shows OSINT signals precede on-chain anomalies by days or weeks.

Contract analysis should be performed at token listing time: tokens with unrenounced ownership, unlocked liquidity, and hidden mint/pause/blacklist functions should be flagged at the highest risk tier regardless of other indicators.
