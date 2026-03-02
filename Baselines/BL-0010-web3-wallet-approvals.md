# Baseline: Web3 Wallet Approval Patterns

```yaml
---
id: BL-0010
title: "Web3 Wallet Approval Patterns Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - web3-fraud
  - wallet-drainer
  - token-approvals
  - defi
---
```

## Description

This baseline defines normal token approval and smart contract interaction patterns for Web3 wallets, supporting detection logic for TP-0032 (Web3 Wallet Drainer / Approval Phishing). Wallet drainer attacks trick users into signing malicious token approval transactions that grant the attacker's contract unlimited access to the victim's token balances, enabling subsequent theft without further user interaction.

Behavioral baselines for wallet approval activity are essential because legitimate DeFi usage requires token approvals, making approval transactions inherently ambiguous. The distinction between a legitimate DEX approval and a malicious drainer approval lies in the patterns surrounding the transaction: the contract's age, the approval amount, the user's interaction history, and the gas fee dynamics. These baselines provide the behavioral context needed to differentiate routine DeFi participation from social engineering attacks.

## Normal Patterns

* **Approval Frequency:** Active DeFi users grant **2-5 new token approvals per month** on average. Users issuing **10+ approvals in a single day** represent fewer than **0.5%** of the active wallet population. A wallet that has been dormant for 30+ days suddenly granting multiple approvals in a single session is a strong anomaly.
* **Approval Amounts:** Approximately **65%** of legitimate token approvals are set to the maximum uint256 value (unlimited), a common default in DeFi interfaces. However, approvals to **contracts younger than 7 days** with unlimited amounts occur in fewer than **3%** of legitimate approval events. Bounded approvals (specific token amounts) represent **35%** of approvals, typically set to **1.5-3x** the immediate transaction need.
* **Contract Interaction Patterns:** Legitimate users typically interact with **3-10 unique smart contracts per month**. Approximately **80%** of approvals go to contracts with **1,000+ unique interacting wallets** and **90+ days** of deployment history. Approvals to contracts with fewer than **50 unique users** and less than **24 hours** of deployment age represent fewer than **2%** of legitimate activity.
* **Gas Fee Patterns:** Normal DeFi approval transactions use gas prices within **20%** of the current network median. Drainer operations frequently set elevated gas prices (**150-300% of median**) to ensure rapid confirmation before the victim can revoke. Multiple approval transactions from the same wallet within a single block or across 2-3 consecutive blocks represent fewer than **1%** of normal behavior.
* **Pre-Approval Behavior:** Legitimate DeFi users typically visit a protocol's interface for **2-10 minutes** before signing an approval, often reviewing token pairs, liquidity pools, or yield rates. Approval signatures occurring within **15 seconds** of first interaction with a previously unknown contract URL are consistent with phishing-driven drainer flows.

## Application to Detection

Detection rules for TP-0032 should prioritize the combination of contract age, approval scope, and user interaction history. A wallet granting an unlimited approval to a contract deployed within the last 24 hours that has fewer than 50 unique interacting wallets should generate a high-severity alert, regardless of the token being approved. Rules should also flag approval transactions where the gas price exceeds 200% of the network median, as this urgency signal correlates with drainer operations attempting to front-run potential revocations.

Threshold tuning should account for network-specific norms: Ethereum mainnet approvals are less frequent but higher value, while Layer 2 networks (Arbitrum, Optimism, Base) see higher approval frequency due to lower gas costs. Detection engines should maintain per-network baseline distributions. For wallet-level scoring, the most effective composite signal combines dormancy-to-activity transition (no transactions for 30+ days), interaction with a new contract (zero prior transactions with the contract address), and unlimited approval scope -- the co-occurrence of all three factors warrants an immediate intervention alert.
