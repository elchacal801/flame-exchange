# Baseline: KYC Document Submission Patterns

```yaml
---
id: BL-0007
title: "KYC Document Submission Patterns Baseline"
category: Baseline
date: 2026-03-02
author: "FLAME Project"
tags:
  - kyc-verification
  - document-fraud
  - identity-verification
  - onboarding
---
```

## Description

This baseline defines normal patterns for identity document submission during customer onboarding and KYC verification workflows, supporting detection logic for TP-0029 (AI Synthetic Identity & Document Forgery) and TP-0018 (Deepfake Document Fraud). Advances in generative AI have made it possible to produce convincing synthetic identity documents at scale, necessitating behavioral baselines that look beyond document-level analysis to submission-level patterns.

Understanding the normal cadence, retry behavior, and metadata characteristics of legitimate document submissions enables detection engines to identify the systematic, high-volume patterns associated with synthetic identity factories. These baselines complement document authenticity checks by adding a behavioral layer that is difficult for fraudsters to replicate organically.

## Normal Patterns

* **Submission Timing During Onboarding:** Legitimate applicants submit identity documents within **5-30 minutes** of reaching the document upload step. Approximately **70%** of successful submissions occur within the first attempt. Submissions completed in under **10 seconds** from page load suggest automated or pre-staged uploads characteristic of bot-driven synthetic identity operations.
* **Retry Rate:** The normal document rejection-and-retry rate is **15-25%** across all applicants, driven by image quality issues (blur, glare, cropping). Applicants requiring **4+ submission attempts** represent fewer than **3%** of legitimate onboarding flows. Synthetic document operations often exhibit either zero retries (high-quality forgeries) or excessive retries (iterative testing against verification systems).
* **Image Metadata Consistency:** Legitimate document photos are captured on **mobile devices** approximately **80%** of the time, with EXIF data showing the capture device, timestamp, and GPS coordinates consistent with the applicant's stated location. Documents lacking EXIF data entirely, or showing uniform metadata across multiple applicants (same device model, identical resolution, sequential timestamps), deviate from normal submission patterns.
* **Document Diversity Ratios:** Across a healthy applicant population, document types should reflect regional norms: approximately **60% driver's licenses, 25% passports, and 15% state/national IDs** for U.S.-based onboarding. A sudden shift where **40%+ of submissions** within a 7-day window use a single document type from a single issuing authority may indicate a batch forgery operation.
* **Submission Velocity per Source:** Normal onboarding flows generate **5-20 document submissions per IP address per day** for institutional partners (e.g., branch locations). A single IP address or device fingerprint generating **50+ unique applicant document submissions per day** exceeds the 99th percentile and is consistent with automated synthetic identity pipelines.

## Application to Detection

Detection rules for TP-0029 and TP-0018 should layer submission-level behavioral signals on top of document authenticity scoring. A document that passes visual inspection but was submitted from an IP address associated with 50+ other submissions in the same day should receive elevated risk scoring regardless of its apparent authenticity. Rules should flag onboarding sessions where document upload occurs in under 10 seconds from page load, as this timing is inconsistent with a human photographing or selecting a document.

Threshold tuning should distinguish between individual applicant anomalies and population-level shifts. A single applicant with 4+ retries may simply have poor camera quality, but if the institutional retry rate spikes from 20% to 45% within a week, this population-level signal suggests a coordinated attack against the verification system. Detection engines should maintain rolling 30-day baselines for submission velocity, retry rates, and document type distributions, and alert when any metric deviates by more than 2.5 standard deviations.
