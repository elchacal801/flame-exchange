# Baseline: AI vs Human Domain Registration Rate Norms

```yaml
---
id: BL-0023
title: "AI vs Human Domain Registration Rate Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project"
tags:
  - ai-generated
  - domain-generation
  - zone-file-analysis
  - content-generation
  - dns-intelligence
---
```

## Description

This baseline defines registration rate and pattern baselines for distinguishing AI-assisted from human-operated domain infrastructure campaigns, supporting detection logic for TP-0043 (AI-Accelerated Domain Infrastructure). It establishes behavioral norms for registration velocity, timing regularity, naming pattern characteristics, certificate provisioning speed, and campaign creation efficiency across human-operated and AI-assisted threat actor workflows. These baselines are derived from Palo Alto Networks newly registered domain classification data, Bolster 2026 scam page proliferation analysis, Chainalysis 2026 AI-enabled fraud profitability data, and KnowBe4 AI-generated phishing content prevalence research. Organizations should calibrate these thresholds to their specific zone file monitoring scope and evolving AI tooling capabilities.

## Normal Patterns

* **Human-Operated Campaign Registration Rate:** Human-operated domain infrastructure campaigns register **10-100 domains per day** with irregular timing patterns reflecting manual workflow constraints — work hours, registration fatigue, payment processing delays, and manual DNS configuration steps. Naming patterns in human-operated campaigns are diverse, often incorporating misspellings of target brands, geographic terms, and varied TLD selections. The irregularity in timing and naming diversity are the primary distinguishing characteristics from AI-assisted operations.

* **AI-Assisted Campaign Registration Rate:** AI-assisted campaigns register **100-10,000+ domains per day** with regular timing patterns reflecting automated scripted workflows driven by large language model output and API-based registration pipelines. Naming patterns in AI-assisted campaigns are lexically coherent — the generated domain names are grammatically plausible, often resembling natural-language phrases or compound words, but do not correspond to established brands or legitimate organizations. This coherence-without-provenance pattern is a key detection signal.

* **Pre-ChatGPT NRD Malicious Classification Rate (2022):** Prior to widespread AI tool availability, approximately **70% of newly registered domains** (NRDs) were classified as malicious or suspicious by Palo Alto Networks analysis. This pre-AI baseline establishes the historical threat landscape against which AI-accelerated changes should be measured. The high baseline malicious rate reflects existing automated domain generation techniques (traditional DGAs, bulk registration scripts) that predated generative AI tooling.

* **Post-AI Scam Page Acceleration (Bolster 2026):** Bolster 2026 data documents over **38,000 new scam pages per day**, representing a significant acceleration from pre-AI baselines. This daily generation rate reflects the force-multiplying effect of AI tools on scam infrastructure creation — threat actors can now generate convincing landing pages, product descriptions, and brand impersonation content at machine speed rather than manual speed.

* **AI-Generated Domain Naming Characteristics:** AI-generated domains exhibit natural-language-like names that are grammatically plausible but do not correspond to established brands, organizations, or common dictionary terms. These names often combine real words in novel ways (e.g., compound nouns, adjective-noun pairs) that pass human visual inspection but lack any legitimate web presence history. This pattern is distinct from traditional DGA output (random character strings) and from human-selected domains (which typically reference known entities or descriptive terms).

* **Campaign Creation Time Comparison:** Human-operated campaign creation requires approximately **16 hours** of manual effort to register domains, configure DNS, build landing pages, and deploy content. AI-assisted campaign creation reduces this to approximately **5 minutes** using generative AI for content creation, scripted registration APIs, and automated DNS configuration templates. This **192x acceleration factor** fundamentally changes the economics of domain infrastructure campaigns and the detection window available to defenders.

* **AI-Enabled Scam Profitability (Chainalysis 2026):** AI-enabled scams are **4.5 times more profitable** than non-AI scams according to Chainalysis 2026 data, driven by higher-quality social engineering content, more convincing brand impersonation, faster infrastructure deployment, and the ability to scale personalized targeting across victim populations. This profitability multiplier incentivizes continued adoption of AI tools by threat actors and predicts increasing volumes of AI-assisted domain infrastructure.

* **AI-Generated Phishing Content Prevalence (KnowBe4):** KnowBe4 research indicates that **82.6% of phishing emails** now contain AI-generated content, establishing that AI-assisted content generation is already the dominant mode of phishing operations rather than an emerging trend. Domain infrastructure supporting these phishing campaigns should be expected to exhibit AI-assisted registration patterns at comparable prevalence rates.

* **Certificate Provisioning Velocity:** AI-assisted campaigns provision Let's Encrypt TLS certificates **within minutes of domain registration**, leveraging automated ACME protocol clients integrated into the campaign deployment pipeline. Human-operated campaigns typically provision certificates **1-24 hours** after registration, reflecting manual certificate request processes and delayed infrastructure configuration. The time delta between domain registration timestamp (from zone file diff) and certificate transparency log entry provides a measurable signal for distinguishing AI-assisted from human-operated infrastructure.

## Application to Detection

Detection rules DL-0098 and DL-0100 should use these baselines for threshold calibration. DL-0098 (registration velocity anomaly) should trigger on registration clusters exceeding 100 domains per day from a single registrant with timing standard deviation below 10 minutes and lexically coherent naming patterns. DL-0100 (certificate provisioning velocity) should flag domains where the certificate transparency log entry appears within 10 minutes of the zone file registration timestamp, indicating automated end-to-end deployment pipelines.

Pre/post AI-acceleration rate comparisons are essential for contextualizing detection thresholds. The shift from 70% malicious NRD classification (pre-ChatGPT) to 38,000+ scam pages per day (post-AI) represents a qualitative change in threat actor operational tempo. Detection systems calibrated to pre-AI registration volumes will experience alert fatigue without threshold adjustment. The 192x campaign creation acceleration (16 hours to 5 minutes) means that detection and response windows must correspondingly compress — infrastructure that previously persisted for days while under construction now appears fully operational within minutes.

The 4.5x profitability multiplier from Chainalysis 2026 data predicts continued growth in AI-assisted domain infrastructure campaigns. Detection thresholds should be reviewed quarterly and recalibrated against observed AI-assisted campaign characteristics, as generative AI capabilities continue to evolve and threat actor adoption deepens. The convergence of AI-generated content (82.6% of phishing emails) with AI-assisted infrastructure deployment creates a fully automated attack chain that demands equally automated detection and response capabilities.
