# Baseline: Automated Account Opening Velocity Norms

```yaml
---
id: BL-0029
title: "Automated Account Opening Velocity Norms"
category: Baseline
date: 2026-03-20
author: "FLAME Project (sourced from UNODC Emerging Threats Sept 2025, INTERPOL GFFTA 2026)"
related_tps:
  - id: TP-0059
    relationship: related-to
tags:
  - mule-account
  - bot-detection
  - velocity-norms
  - kyc
  - account-onboarding
  - baseline
---
```

## Summary

This baseline defines normal and anomalous patterns for legitimate versus automated account opening activity, KYC verification timing, and per-device application rates. It establishes behavioral norms for application completion speed, document submission timing, device-level velocity, liveness check performance, and human interaction indicators during the onboarding process. These baselines are derived from the UNODC Emerging Threats report (September 2025) and INTERPOL Global Financial Fraud Threat Assessment 2026. Organizations should calibrate detection thresholds against these norms to identify bot-driven mule account creation and distinguish it from legitimate customer onboarding. This baseline supports detection logic DL-0118 and DL-0119.

## Normal Patterns

* **Account Application Completion Time:** Legitimate account applications have a median completion time of **8-15 minutes** for a full digital application including document upload. Bot-assisted applications complete in **under 2 minutes**, reflecting pre-staged data entry and automated form filling.

* **KYC Document Submission Timing:** Legitimate document submission takes **1-10 minutes**, which is variable and includes photo capture, document positioning, and retry attempts. Automated submissions complete in **under 30 seconds** using pre-staged document images.

* **Per-Device/IP Account Application Rate:** Legitimate behavior is **1 application per device**. Bot-driven operations generate **5 or more applications per device per 24 hours**, as automation scripts cycle through identity packages on shared infrastructure.

* **Liveness Check Pass Rates:** Legitimate in-person liveness checks pass at **98%+**. Remote legitimate checks pass at **92-96%**, reflecting normal failures from poor lighting, camera quality, and user error. Remote checks with synthetic faces may produce anomalously high pass rates approaching 99-100%, as synthetic faces present idealized conditions that real users rarely achieve.

* **Mouse/Keyboard Interaction During Application:** Legitimate applications show variable click timing, scroll events, and field corrections throughout the process. Bot-driven applications show **zero mouse movement**, instant field completion, and no corrections — a behavioral signature distinct from any human interaction pattern.

* **Application Form Field Completion Speed:** Legitimate users show variable per-field timing of **2-15 seconds per field**, reflecting reading, comprehension, and data entry. Bot-driven completion shows uniform rapid completion at **under 0.5 seconds per field**.

## Measurement Methodology

Instrument the account opening web application and mobile app to capture behavioral telemetry including timestamps for each form field focus/blur event, mouse movement coordinates, scroll events, keyboard timing, and page navigation events. Calculate application completion time as the interval from first page load to final submission. Measure KYC document submission time from the document upload page load to successful document image submission.

Per-device application rates are measured using device fingerprinting (browser fingerprint, device ID, or hardware identifiers) and IP address tracking. Count distinct account applications per device fingerprint and per IP subnet (/24) within rolling 24-hour windows.

Liveness check pass rates are aggregated across all remote onboarding sessions, segmented by device type, operating system, and browser. Track both the overall pass rate and the distribution of pass/fail patterns — legitimate populations show a natural failure rate, while synthetic face attacks may produce anomalously uniform pass distributions.

Mouse and keyboard interaction metrics are captured via JavaScript event listeners embedded in the application form. Count total mouse events, calculate inter-keystroke timing distributions, measure field correction frequency (backspace, select-all-delete, and re-entry events), and flag sessions with zero mouse movement events.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Application completion time | 8-15 minutes | 2-8 minutes | <2 minutes |
| KYC document submission time | 1-10 minutes | 30s-1 minute | <30 seconds |
| Applications per device per 24h | 1 | 2-3 | >3 |
| Applications per IP subnet /24 per 24h | 1-5 | 5-15 | >15 |
| Liveness check pass rate (remote) | 92-96% | 85-92% | <85% or >99% (too-perfect = synthetic) |
| Mouse events during application | 50-500+ events | 10-50 events | 0 events |
| Per-field completion time | 2-15 seconds | 0.5-2 seconds | <0.5 seconds |
| Form correction rate | 5-20% of fields | 1-5% | 0% (no corrections = pre-staged data) |

## Data Sources

* **UNODC Emerging Threats Report (September 2025):** Documents the scale and methodology of automated mule account creation operations, including bot-driven onboarding patterns observed across Southeast Asian financial institutions.
* **INTERPOL Global Financial Fraud Threat Assessment 2026:** Provides validated intelligence on mule account industrialization, KYC bypass techniques, and the operational infrastructure supporting mass automated account opening.
* **Financial institution onboarding telemetry:** Aggregated behavioral data from account opening flows across banking and fintech platforms, providing baseline human interaction patterns and completion timing distributions.
* **Device fingerprinting and IP intelligence services:** Provide device-level and network-level velocity data for account application tracking and bot detection.
* **Liveness detection vendor performance data:** Pass/fail rate distributions from commercial liveness check providers, segmented by legitimate users and known attack scenarios.

## Application

DL-0118 and DL-0119 should use these baselines for threshold calibration. DL-0118 (automated account opening velocity detection) should trigger review when application completion times fall below 8 minutes and alert when completion times are under 2 minutes, particularly when correlated with zero mouse events and zero form corrections. DL-0119 (device/IP velocity anomaly) should trigger review when per-device application counts exceed 1 within 24 hours and alert when counts exceed 3, or when per-IP-subnet application counts exceed 15.

Analysts should treat the combination of sub-2-minute completion, zero mouse events, and zero form corrections as a high-confidence bot indicator. Liveness check pass rates above 99% in remote sessions should be flagged for synthetic face investigation, as this counter-intuitive signal (too-perfect performance) is a hallmark of deepfake-assisted onboarding attacks.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-20 | 1.0 | Initial baseline established from UNODC and INTERPOL GFFTA intelligence |
