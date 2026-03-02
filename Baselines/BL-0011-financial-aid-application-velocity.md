# Baseline: Financial Aid Application Velocity

```yaml
---
id: BL-0011
title: "Financial Aid Application Velocity Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - education-fraud
  - financial-aid
  - fafsa
  - ghost-students
---
```

## Description

This baseline defines normal patterns for federal financial aid applications (FAFSA), institutional enrollment, and disbursement activity, supporting detection logic for TP-0033 (Ghost Student Financial Aid Botnets). Ghost student schemes use synthetic or stolen identities to enroll fictitious students at eligible institutions, file FAFSA applications to receive Pell Grants and student loan disbursements, then withdraw funds without attending classes.

Behavioral baselines for financial aid application velocity and disbursement patterns are critical because ghost student operations generate distinctive aggregate signals at the institution level. While individual fraudulent applications may appear legitimate, the timing, volume, and device-reuse patterns across a coordinated botnet diverge measurably from organic student enrollment behavior.

## Normal Patterns

* **Application Timing Relative to Academic Calendar:** Approximately **70%** of legitimate FAFSA applications are submitted **3-6 months before the term start date**, with a secondary peak **1-2 months** before the term. Applications submitted within **2 weeks of the enrollment deadline** represent fewer than **10%** of legitimate applications. A surge of **50+ applications** arriving in the final 7 days before a deadline from a single institution is anomalous.
* **Application Volume per Institution:** Community colleges and open-enrollment institutions receive **500-5,000 FAFSA applications per term** depending on size. A term-over-term increase exceeding **40%** without corresponding marketing or program expansion is anomalous. Institutions experiencing a **100%+ increase** in applications within a single term warrant priority review.
* **Disbursement-to-Enrollment Ratio:** Legitimate institutions disburse financial aid to **85-95%** of enrolled aid-eligible students. A disbursement rate exceeding **98%** of all enrolled students, particularly when combined with a withdrawal rate exceeding **30%** within the first 4 weeks of the term, deviates from normal patterns.
* **IP and Device Reuse:** Normal FAFSA submission patterns show **1-2 applications per residential IP address** per term (family members). More than **5 unique applicant submissions** from a single IP address or device fingerprint within a 30-day window is anomalous. Botnet operations frequently generate **20-100+ applications** from a small pool of IP addresses or cloud-hosted infrastructure.
* **Disbursement Withdrawal Patterns:** Legitimate students spend financial aid over the course of a **12-16 week term**, with the largest single expenditure typically being tuition. Ghost students withdraw **80-100% of disbursed funds** within **72 hours** of receipt via ATM withdrawals, peer-to-peer transfers, or outbound wires. Fewer than **5%** of legitimate students withdraw more than **50%** of aid within the first week.

## Application to Detection

Detection rules for TP-0033 should operate at both the individual application level and the institutional aggregate level. At the application level, flag submissions originating from IP addresses with 5+ prior applications in the current term, particularly when the applicant profiles share demographic similarities (same zip code, similar ages, identical school selections). At the institutional level, alert when term-over-term application volume increases by more than 2 standard deviations above the institution's 3-year rolling average.

Threshold tuning should incorporate the institution type: large state universities naturally have higher application volumes and greater variance than small community colleges. Detection engines should use peer-group comparisons (same Carnegie classification, same state, similar enrollment size) to normalize thresholds. The highest-confidence composite signal combines rapid post-disbursement withdrawal (>80% within 72 hours), no subsequent tuition payment or bookstore activity, and course withdrawal within the census date -- the co-occurrence of all three factors on more than 10 students at a single institution within a single term should trigger an institutional-level investigation.
