# Baseline: Deepfake Service Procurement Activity Norms

```yaml
---
id: BL-0028
title: "Deepfake Service Procurement Activity Norms"
category: Baseline
date: 2026-03-20
author: "FLAME Project (sourced from UNODC Emerging Threats Sept 2025, INTERPOL GFFTA 2026, Recorded Future CTA-2026-0319)"
related_tps:
  - id: TP-0057
    relationship: related-to
  - id: TP-0034
    relationship: related-to
tags:
  - deepfake
  - daas
  - procurement-norms
  - telegram-channels
  - baseline
---
```

## Summary

This baseline defines normal and anomalous activity levels for deepfake service marketplace activity, video conferencing artifact detection, and underground channel activity levels. It establishes norms for deepfake-as-a-service (DaaS) vendor proliferation, virtual camera driver usage in legitimate versus fraudulent contexts, and voice synthesis detection thresholds. These baselines are derived from the UNODC Emerging Threats report (September 2025), INTERPOL Global Financial Fraud Threat Assessment 2026, and Recorded Future threat intelligence. Organizations should calibrate detection thresholds against these norms to distinguish legitimate use of video and audio processing tools from deepfake-enabled fraud operations. This baseline supports detection logic DL-0115 and DL-0116.

## Normal Patterns

* **Deepfake Tool Mentions in Underground/Telegram Channels:** Pre-February 2024 baseline levels represent the historical norm for deepfake tool discussion in criminal channels. A **600% increase** in mentions has been documented by UNODC as the anomaly threshold, reflecting the rapid mainstreaming of deepfake tooling within cybercriminal ecosystems.

* **Commercial Deepfake Vendors:** The pre-2024 baseline was **fewer than 5** commercial deepfake vendors serving the Southeast Asia fraud market. UNODC now documents **10+ vendors** as the current observed level, establishing the new baseline for SE Asia-serving DaaS providers.

* **Video Conferencing Virtual Camera Usage:** Legitimate OBS Virtual Camera usage for screen sharing and streaming is common in technology roles, with an estimated **15-25% of remote workers** using virtual camera drivers. Usage of DeepFaceLive and dedicated face-changing tools is **near-zero** in legitimate contexts, making any detection of these specific drivers a strong anomaly signal.

* **Voice Synthesis Detection:** The false positive baseline for legitimate voice processing (noise cancellation, audio enhancement) versus voice cloning indicators shows a spectral anomaly rate in legitimate calls of **<2%**. Synthetic voice detection should trigger above a **15% anomaly score**, with the gap between 2% and 15% representing the review threshold.

* **Deepfake Generation Audio Minimum:** As little as **10 seconds** of target audio is sufficient for generating a usable voice clone, per Group-IB and INTERPOL research. This establishes the security awareness threshold — any audio sample of a high-value target exceeding 10 seconds should be considered exploitable for voice cloning attacks.

## Measurement Methodology

Monitor underground marketplace channels and Telegram groups for deepfake tool and service mentions using keyword tracking across known criminal communication platforms. Establish monthly mention volume baselines per channel and track percentage changes against the pre-February 2024 baseline period.

Commercial DaaS vendor counts are measured by enumerating distinct vendors offering deepfake generation services on underground marketplaces, Telegram channels, and dark web forums, filtered to those advertising SE Asia language support or targeting SE Asia-based fraud operations.

Virtual camera driver detection is measured through endpoint telemetry on corporate devices during video conferencing sessions. Enumerate installed virtual camera drivers and classify them as legitimate (OBS Virtual Camera, screen sharing tools) or suspicious (DeepFaceLive, FaceSwap, and similar face-manipulation tools). Calculate the percentage of video interview sessions where virtual camera drivers are detected.

Voice synthesis detection uses spectral analysis of audio streams during voice calls, measuring the percentage of audio frames that exhibit anomalous spectral characteristics consistent with synthetic voice generation. Baseline the false positive rate against known-legitimate calls with standard noise cancellation and audio enhancement processing.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Deepfake mentions per criminal channel (monthly) | 50-200 (pre-2024 baseline) | 200-500 | >500 (600% increase documented) |
| Commercial DaaS vendors (SE Asia market) | <5 (pre-2024) | 5-10 | >10 (current observed level) |
| Virtual camera driver presence in video interviews | 15-25% (legitimate OBS/screen share) | 25-40% | >40% or presence of DeepFaceLive/FaceSwap drivers |
| Audio spectral anomaly score | <2% (legitimate processing) | 2-10% | >15% (synthetic voice indicators) |
| Target audio needed for voice clone | N/A | 30-60 seconds | 10 seconds (confirmed minimum) |

## Data Sources

* **UNODC Emerging Threats Report (September 2025):** Documents the 600% increase in deepfake tool mentions within criminal channels and the proliferation of commercial DaaS vendors serving the Southeast Asia fraud ecosystem.
* **INTERPOL Global Financial Fraud Threat Assessment 2026:** Provides validated intelligence on deepfake-enabled fraud methodologies, voice cloning minimum audio thresholds, and DaaS marketplace evolution.
* **Recorded Future CTA-2026-0319:** Threat intelligence report covering underground marketplace activity levels, vendor enumeration, and deepfake tooling proliferation metrics.
* **Group-IB Threat Intelligence:** Research establishing the 10-second minimum audio sample threshold for viable voice clone generation.
* **Endpoint telemetry from corporate video conferencing deployments:** Provides baseline data on legitimate virtual camera driver usage rates across enterprise environments.

## Application

DL-0115 and DL-0116 should calibrate thresholds against these baselines. DL-0115 (deepfake artifact detection in video conferencing) should trigger review when virtual camera drivers beyond standard OBS/screen sharing tools are detected during video interviews or onboarding sessions, and should generate alerts when DeepFaceLive, FaceSwap, or similar face-manipulation drivers are identified. DL-0116 (synthetic voice detection) should trigger review when audio spectral anomaly scores exceed 2% and alert when scores exceed 15%.

Analysts should treat any detection of dedicated face-manipulation virtual camera drivers as high-confidence indicators regardless of other contextual factors, given the near-zero legitimate usage rate for these tools. Voice synthesis alerts should be correlated with other session metadata (caller identity verification status, call origin, and relationship to high-value transactions) to prioritize investigation.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-20 | 1.0 | Initial baseline established from UNODC, INTERPOL GFFTA, and Recorded Future intelligence |
