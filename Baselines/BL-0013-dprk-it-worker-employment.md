# Baseline: DPRK IT Worker Employment Indicators

```yaml
---
id: BL-0013
title: "DPRK IT Worker Employment Indicators Baseline"
category: Baseline
date: 2026-03-03
author: "FLAME Project"
tags:
  - dprk-it-worker
  - employment-fraud
  - insider-threat
  - remote-work
  - identity-verification
---
```

## Description

This baseline defines normal versus anomalous employment patterns relevant to detecting DPRK state-sponsored IT worker infiltration. It supports detection logic for TP-0034 (DPRK State-Sponsored IT Worker Fraud & Data Extortion) by establishing behavioral norms for remote software engineering employees across hiring pipeline, network access, code repository interaction, and payroll patterns. These baselines are derived from FBI IC3 advisories, DOJ enforcement action details, and threat intelligence reporting from Google, Microsoft, CrowdStrike, and Palo Alto Unit 42.

## Normal Patterns

* **Hiring Pipeline:** Legitimate remote software engineers typically have LinkedIn profiles older than **2 years** with **50+ connections**, GitHub accounts with **multi-year commit history**, and education credentials that can be verified through university registrar offices. Background checks complete without identity element conflicts (address, SSN issuance date, credit history depth are consistent with claimed biography).

* **VPN/Network Access:** Remote employees typically connect from **1-2 consistent geographic locations** (home office, co-working space) with stable IP addresses. Connection source changes occur **fewer than 3 times per month** and correlate with travel or relocation events. Direct VPN connections without intermediate proxy or VPN layering are the norm — **fewer than 2%** of legitimate remote employees route through consumer VPN services during work hours.

* **Onboarding Code Access:** New software engineers typically clone **2-5 repositories** in their first week, focused on their assigned team's codebase. Accessing repositories outside assigned project scope occurs in **fewer than 10%** of new hires during the first 14 days. Full organizational repository enumeration (listing all available repos) during the first 48 hours occurs in **fewer than 5%** of new hires and is typically associated with platform engineering or DevOps roles.

* **Credential Access:** New employees typically generate **1-3 API keys** and access credential stores **5-15 times** during their first week of onboarding. Accessing browser credential export functions, session token storage, or password manager bulk export features during onboarding occurs in **fewer than 1%** of legitimate employees.

* **Communication Consistency:** Employee communication style (vocabulary, syntax, response patterns) remains consistent across time windows. Legitimate employees show **fewer than 5% variance** in writing style metrics across morning and evening work sessions. Device fingerprints remain stable, with changes occurring **fewer than twice per month** outside of hardware upgrade cycles.

* **Payroll Patterns:** Salary direct deposits remain in the receiving account for a median of **5-7 days** before significant outflows. Immediate full-balance withdrawal within **48 hours** of deposit occurs in **fewer than 3%** of legitimate employee accounts. Salary-to-cryptocurrency conversion within 48 hours of deposit occurs in **fewer than 1%** of employee payroll accounts.

* **Interview-to-Performance Correlation:** Legitimate hires show a performance correlation coefficient of **0.6-0.8** between technical interview scores and first-90-day code review quality metrics. A correlation below **0.3** — where interview performance significantly exceeds job performance — is anomalous and observed in DPRK IT worker cases.

## Application to Detection

Detection rules for TP-0034 should layer hiring pipeline indicators (geographic mismatch, thin profiles) with post-hire behavioral signals (VPN anomalies, code access patterns, communication shifts). A single indicator (e.g., non-North American education) has a high false positive rate among legitimate international talent. However, the combination of geographic mismatch + VPN proxy patterns + early bulk repository access + credential harvesting creates a high-confidence composite signal.

Threshold tuning should account for role type: platform engineers and DevOps roles legitimately access broader repository scopes than application developers. Security engineers may legitimately interact with credential stores more frequently. These role-based baselines should be established per organization to reduce false positives.

Financial monitoring should flag payroll accounts where salary deposits are converted to cryptocurrency within 48 hours, especially when multiple employee accounts at the same organization show the same conversion pattern through the same exchange — a strong indicator of coordinated DPRK IT worker operations.
