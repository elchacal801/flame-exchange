# TP-0023: Mobile Banking Trojan / Overlay Attack

```yaml
---
id: TP-0023
title: "Mobile Banking Trojan / Overlay Attack"
category: ThreatPath
date: 2026-02-20
author: "FLAME Project"
source: "Internal Knowledge Base; Thales Threat Landscape Report 2025 H2 — Finance sector mobile malware analysis"
tlp: WHITE
sector:
  - banking
  - fintech
  - crypto
fraud_types:
  - account-takeover
  - malware
  - unauthorized-transaction
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
mitre_attack:
  - T1624     # Event Triggered Execution (Overlay)
  - T1626     # Device Lockout
  - T1417     # Input Capture
  - T1636     # Protected User Data (SMS MFA bypass)
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT011.001", "FT013", "FT003", "FT016.001", "FT006", "FT007.001", "FT008.002", "FT015", "FT018", "FT031"]
mitre_f3: []
groupib_stages:
  - "Resource Development"
  - "Initial Access"
  - "Execution"
  - "Credential Access"
  - "Perform Fraud"
ucff_domains:
  commit: "Level 3"
  assess: "Level 4"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 4"
confidence_score: 72
source_reliability: B
info_credibility: 2
related_tps:
  - id: TP-0001
    relationship: related-to
  - id: TP-0008
    relationship: shares-infrastructure
  - id: TP-0069
    relationship: related-to
regulatory_refs:
  - REG-CFPB-REGE
  - REG-DORA
  - REG-FFIEC-AUTH
  - REG-OCC-FRAUD
  - REG-PSD3-SCA
baseline_ids: []
tags:
  - mbanking
  - android-malware
  - overlay-attack
  - ats
---
```

---

## Summary

Mobile Banking Trojans (primarily targeting Android environments) are sophisticated malware variants that deceive users into granting extensive device "Accessibility" permissions. Once installed, the malware monitors the foreground applications. When the user launches a targeted banking app, the malware draws a pixel-perfect "overlay" (a fake login screen) on top of the legitimate app. It captures the user's credentials and SMS MFA tokens, sending them to the threat actor, or uses an Automated Transfer System (ATS) to initiate fraudulent transactions invisibly on the victim's device.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors distribute malicious Android APKs via smishing or third-party app stores. The malware convinces the victim to grant accessibility services, allowing the malware to detect banking app launches, present spoofed overlays to harvest credentials, intercept SMS-based MFA, and autonomously execute wire transfers via the legitimate banking app.

**Confidence**: High — Widely documented by threat intelligence firms analyzing malware families such as Anubis, Cerberus, Octo, and Vultur.

**Estimated Impact**: Complete Account Takeover (ATO) with the ability to drain the victim's deposit accounts up to daily transaction limits. Severe reputational damage to the institution due to the compromise occurring on the "trusted" mobile channel.

---

## CFPF Phase Mapping

### Phase 1: Recon & Resource Dev

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-002: Malware Infrastructure | Actors lease Banking-Trojan-as-a-Service (MaaS) panels, pack malicious APKs (often disguising them as PDF readers, utility apps, or fake software updates), and set up C2 infrastructure. | (External to financial institution) |

**Data Sources**: Mobile Threat Defense (MTD) telemetry, malware sandboxes.

---

### Phase 2: Initial Access & Trust Abuse

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Smishing/Malvertising Delivery | Victims receive SMS messages urging them to install an app (e.g., "DHL package tracking") or encounter malicious ads. The app requests extensive Accessibility permissions. | (External to financial institution) |
| CFPF-P2-004: Credential Harvesting via Overlay | The malware detects the user opening the bank app, injects the fake overlay, logs the username/password, and intercepts the subsequent SMS OTP sent by the bank. | Victim completes login, but the bank sees repeated authentication failures (if the overlay doesn't pass the creds through) or login from anomalous IP (if the actor logs in from their own device). |

**Data Sources**: App analytics (time to login, unusual UI interactions), MFA logs.

---

### Phase 3 & 4: Execution (ATO & Transfer)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: ATS (Automated Transfer System) Execution | Modern variants don't rely on the actor logging in manually. Instead, the malware's ATS module uses Accessibility permissions to click through the legitimate banking app *on the victim's own device*, initiating a transfer to a mule account while dimming the screen or displaying a fake "System Updating" overlay to the user. | Lightning-fast navigation through the app interface; transaction sourced from the victim's trusted device and normal IP (bypassing traditional risk engines). |

**Data Sources**: Mobile app behavioral analytics (keystroke dynamics, screen dimming events, navigation velocity).

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Mule Network Dispersion | The funds are immediately wired to a mule account and withdrawn. | Instant transfer to unrecognized beneficiary followed by rapid cash-out. |

**Data Sources**: Transaction monitoring.

---

## Look Left / Look Right Analysis

**Discovery Phase**: Frequently discovered at **Phase 5** when the victim notices the missing funds.

**Look Left**:

- **P4/3 → P2**: Traditional fraud systems fail because the transaction originates from the victim's *known, trusted device* and *recognized IP address* via the ATS.
- The failure point is lacking visibility into the device posture (e.g., detecting sideloaded apps running with Accessibility permissions active).

**Look Right**:

- Unless the malware is removed from the device, the actor maintains a persistent foothold to intercept further communications or attack other financial apps.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P2 | Implement RASP (Runtime Application Self-Protection) checks within the banking app to detect overlays, sideloading, or active screen-readers. | Preventive | Mobile Engineering |
| P2 | Transition away from SMS OTPs to strong, out-of-band push notifications or FIDO2/WebAuthn. | Preventive | IAM |
| P4 | Implement Mobile Behavioral Biometrics (analyzing swipe pressure, navigation speed, device angle) to detect ATS bot behavior vs. human interaction. | Detective | Fraud Risk |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive commitment to mobile channel security investment including RASP integration, behavioral biometrics, and MFA modernization beyond SMS OTP |
| ASSESS | Level 4 (Advanced) | Threat assessment of mobile banking app attack surface covering overlay attacks, ATS capabilities, and Accessibility Services abuse; evaluation of current authentication methods (SMS OTP) against credential interception by banking trojans; vendor assessment of MaaS ecosystem targeting the institution's app |
| PLAN | Level 3 (Established) | Detection strategy integrating mobile app telemetry (navigation velocity, screen state anomalies) with server-side transaction monitoring; migration roadmap from SMS-based MFA to FIDO2/WebAuthn or push notification authentication |
| ACT | Level 4 (Advanced) | RASP deployment within the mobile banking app to detect overlays, sideloaded apps, and active screen-readers at runtime; mobile behavioral biometrics analyzing swipe pressure, navigation speed, and device orientation to distinguish human interaction from ATS bot behavior; FIDO2/WebAuthn authentication replacing SMS OTP |
| MONITOR | Level 3 (Established) | Continuous monitoring of mobile session telemetry for impossible navigation speeds, screen brightness anomalies, and Accessibility Service activation during banking sessions; real-time correlation of device posture signals with transaction risk scoring |
| REPORT | Level 2 (Developing) | Incident reporting for confirmed mobile malware-facilitated ATO including malware family attribution; customer notification procedures for compromised devices; coordination with mobile threat intelligence providers for C2 infrastructure takedown |
| IMPROVE | Level 4 (Advanced) | Continuous integration of new malware family TTPs (overlay patterns, ATS navigation signatures) into RASP and behavioral biometric detection models; post-incident device forensics feeding back into app hardening priorities; tracking of MaaS ecosystem evolution to anticipate new evasion techniques |

## Detection Approaches

### Queries / Rules

**Sigma — Fast Navigation ATS Anomaly (Conceptual)**

```yaml
title: Mobile Banking - Impossible Navigation Speed (ATS Indicator)
status: experimental
description: Detects when the time between app launch, login, and transaction initiation is faster than humanly possible, indicating an Automated Transfer System.
logsource:
    product: mobile_banking
    service: telemetry
detection:
    selection:
        action: 'transaction_initiated'
    condition: selection | time_since(session_start) < 4s
level: high
tags:
    - attack.t1624
    - cfpf.phase4.execution
```

### Behavioral Analytics

- **Screen State Anomalies**: Flag transactions initiated while the device screen brightness is registered at 0% or while an overlay window is currently active.
- **Accessibility Service Auditing**: Upon app launch, the mobile app queries the OS for active Accessibility services. If anomalous or non-standard services are active, elevate the session risk score.

---

## Analyst Notes

The mobile banking trojan ecosystem is dominated by a handful of malware-as-a-service (MaaS) families that are continuously evolving. As of 2025-2026, the most active families include Octo (v2), Vultur, Anatsa (TeaBot), and Hook — each offering builder kits on underground forums for $3,000-$7,000/month. The Automated Transfer System (ATS) capability represents a paradigm shift in mobile fraud: because the fraudulent transaction originates from the victim's own device using their established session, traditional server-side fraud detection (IP reputation, device fingerprinting, geolocation) is entirely bypassed. ThreatFabric's 2024 Mobile Threat Landscape report documented over 100 banking apps targeted by overlay attacks, with European and Latin American banks most heavily targeted. Google's Play Protect and the restricted accessibility service policies introduced in Android 13+ have raised the bar for malware distribution, pushing actors toward sideloading via smishing and third-party app stores. Financial institutions should prioritize Runtime Application Self-Protection (RASP) integration, behavioral biometrics for ATS detection, and migration away from SMS-based MFA to push notification or FIDO2 authentication.

The Thales Threat Landscape Report 2025 H2 identified four additional mobile banking trojans active in the financial sector during the second half of 2025:

| Trojan | Key Capabilities | Distribution | Notable Technique |
|--------|-----------------|--------------|-------------------|
| Hook v3 | 107 remote commands, ransomware overlays, screen capture | Phishing, GitHub | Expanded remote command set enables full device control beyond banking fraud |
| ToxicPanda | Banking overlays, credential harvesting via Accessibility Services | App stores, smishing | Leverages legitimate app store distribution to bypass sideloading defenses |
| Astaroth | Browser-stored credential theft, session token harvesting | Fake apps, cloud services | Uses GitHub for resilient C2 infrastructure and steganography for payload delivery |
| Coyote | Automated fraudulent transfers via Microsoft UI Automation API | Smishing, fake apps | Abuses Windows UI Automation framework — a novel technique that bypasses traditional ATS behavioral detection |

Hook v3 and ToxicPanda follow the established overlay/Accessibility Services model, while Astaroth and Coyote represent capability evolution: Astaroth's GitHub-based C2 improves resilience against takedowns, and Coyote's abuse of the Microsoft UI Automation API is a novel technique that may evade behavioral biometrics tuned for traditional ATS navigation patterns.

---

## References

- FLAME Project Internal Knowledge Base.
- ThreatFabric: "Mobile Threat Landscape" annual reports — malware family analysis and ATS capability evolution. [Link](https://www.threatfabric.com/)
- Cleafy: "Android Banking Trojan Tracker" — overlay attack and ATS detection research. [Link](https://www.cleafy.com/)
- Google: Android Security & Privacy Year in Review — Play Protect statistics and accessibility service policy changes.
- OWASP Mobile Security: "Mobile Application Security Verification Standard (MASVS)" — RASP and anti-tampering requirements. [Link](https://mas.owasp.org/MASVS/)
- Europol: Internet Organised Crime Threat Assessment (IOCTA) — mobile malware as a service trends. [Link](https://www.europol.europa.eu/publications-events/main-reports/internet-organised-crime-threat-assessment-iocta)
- Thales Group CTI, "Threat Landscape Report 2025 H2" — Finance sector mobile malware analysis (Hook v3, ToxicPanda, Astaroth, Coyote)

---

## Operational Evidence

### EV-TP0023-2026-001: 2025 H2 Mobile Banking Trojan Evolution

- **Source**: Thales Group CTI, "Threat Landscape Report 2025 H2" — Finance sector analysis
- **Key Findings**: Four new mobile banking trojan families identified as active threats in H2 2025: Hook v3 (107 remote commands, ransomware overlays), ToxicPanda (Accessibility Services abuse via legitimate app stores), Astaroth (GitHub-based resilient C2 with steganography), and Coyote (Microsoft UI Automation API abuse for automated fraudulent transfers). Coyote's UI Automation technique represents a novel evasion of traditional ATS behavioral detection. The finance sector recorded 533 ransomware attacks in 2025, with mobile malware serving as a distinct but parallel initial access vector.
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-20 | FLAME Project | Initial creation |
| 2026-02-28 | FLAME Project | v1.5 enrichment: added Stripe FT3 tactic mappings, Analyst Notes, enriched References |
| 2026-03-23 | FLAME Project | Enrichment: added Hook v3, ToxicPanda, Astaroth, Coyote from Thales 2025 H2 report; added TP-0069 relationship; added operational evidence |
