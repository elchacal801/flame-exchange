# TP-0067: AiTM Phishing Kit Infrastructure and Session Token Hijacking

```yaml
---
id: TP-0067
title: "AiTM Phishing Kit Infrastructure and Session Token Hijacking"
category: ThreatPath
date: 2026-03-22
author: "FLAME Project"
source: "Organized fraud detection in 2026: a technical landscape report"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - aitm-phishing
  - phishing
  - account-takeover
  - credential-stuffing
  - fraud-as-a-service
sector:
  - cross-sector
  - banking
  - fintech
  - technology
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 82
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1557      # Adversary-in-the-Middle
  - T1539      # Steal Web Session Cookie
  - T1566.002  # Phishing: Spearphishing Link
  - T1114.003  # Email Collection: Email Forwarding Rule
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FT007.009", "FT011.001"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "Credential Access"
  - "Account Access"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 4"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0002
    relationship: enables
  - id: TP-0054
    relationship: shares-infrastructure
  - id: TP-0001
    relationship: related-to
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-STIX-FCI
geopolitical_timing: none
nation_state_nexus: none
tags:
  - aitm-phishing
  - tycoon-2fa
  - evilginx
  - session-token-replay
  - phaas
  - fido2
  - mfa-bypass
  - phishing-kit
  - credential-phishing
---
```

## Summary

Adversary-in-the-Middle (AiTM) phishing kits represent the most significant evolution in credential theft infrastructure, enabling attackers to bypass multi-factor authentication by proxying victim sessions through attacker-controlled infrastructure in real time. The attacker captures both credentials and session tokens/cookies as the victim authenticates with the legitimate service. Sekoia.io identified 11 major AiTM phishing kits active in early 2025, with Tycoon 2FA as the most prevalent (1,200+ domains, targeting 500K+ organizations monthly). Credential phishing attacks surged 703% in H2 2024. These kits operate as Phishing-as-a-Service (PhaaS) marketplaces, lowering the barrier to sophisticated MFA-bypass attacks. FIDO2/phishing-resistant MFA blocks 93.9% of AiTM campaigns, making it the primary defensive recommendation.

**Distinction from TP-0054**: TP-0054 (FaaS Ecosystem) covers the broader fraud-as-a-service model. TP-0067 focuses specifically on the AiTM phishing kit infrastructure — the reverse proxy technology, session token capture mechanics, and PhaaS distribution model that enables downstream BEC, account takeover, and wire fraud.

## Threat Path Hypothesis

> **Hypothesis**: AiTM phishing kit infrastructure has industrialized MFA-bypass credential theft by providing turnkey reverse proxy platforms that intercept and relay authentication sessions between victims and legitimate services. The kits capture session tokens in real time, enabling attackers to hijack authenticated sessions without needing the victim's MFA device. This infrastructure operates as PhaaS — kit operators sell access via Telegram and dark web forums, with subscription pricing and customer support. The captured session tokens are used for BEC (TP-0002), wire fraud (TP-0001), and lateral movement. Detection relies on authentication telemetry anomalies (User-Agent/Application ID inconsistencies, impossible travel, inbox rule creation) rather than traditional phishing content analysis.

**Confidence**: High — Sekoia.io, Canadian Cyber Centre, and Microsoft have published detailed analyses of AiTM kits. Tycoon 2FA infrastructure is actively tracked. FIDO2 effectiveness is quantified.

**Estimated Impact**: Individual compromises lead to $10K–$10M+ losses (via BEC/wire fraud downstream). Aggregate: credential phishing is the primary initial access vector for the majority of enterprise fraud, with 703% growth in H2 2024.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Target organization profiling | AiTM operators identify target organizations' identity providers (Microsoft Entra ID, Google Workspace, Okta) and MFA configurations to select appropriate kit templates | Reconnaissance of organization's SSO configuration; enumeration of email domains |
| PhaaS kit procurement | Operators purchase or subscribe to AiTM kits (Tycoon 2FA, Evilginx, Caffeine, NakedPages, Greatness, W3LL Panel) from dark web or Telegram marketplaces | Kit advertisements on underground forums; subscription payments to PhaaS providers |
| Infrastructure provisioning | Operators register domains mimicking target organization login pages, provision reverse proxy servers, and configure SSL certificates | Domain registrations resembling legitimate login portals (e.g., login-microsoftonline[.]com variants); bulk Let's Encrypt certificate issuance |

**Data Sources**: Domain registration monitoring, Certificate Transparency logs, dark web marketplace monitoring, threat intelligence feeds

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Phishing delivery | Victims receive emails containing links to the AiTM phishing page, typically impersonating Microsoft 365 login, password reset, or document sharing notifications | Emails with links to recently registered domains; URLs containing organization-specific parameters; QR codes in emails directing to phishing pages |
| Reverse proxy session establishment | When victim clicks the link, the AiTM kit establishes a reverse proxy session between the victim's browser and the legitimate identity provider — the victim sees and interacts with the real login page | HTTP requests proxied through non-legitimate infrastructure; TLS certificate mismatches between presented domain and proxied service |
| MFA relay and session capture | As the victim completes MFA (push notification, SMS, authenticator code), the AiTM kit captures the resulting session token/cookie in real time | Authentication events where the session token is subsequently used from a different IP/User-Agent than the authenticating device |

**Target**: Enterprise employees with access to email, financial systems, and administrative functions

**Data Sources**: Email security logs, identity provider authentication logs, network proxy logs, endpoint detection

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Session token replay | Attacker replays the captured session token from their own infrastructure to access the victim's authenticated session | Sign-in events with User-Agent or Application ID inconsistent with the authentication event; session access from IP address different from authentication IP; geographic impossibility between auth and access events |
| Inbox rule manipulation | Within minutes of session hijack, attacker creates inbox rules to redirect or delete specific emails (payment notifications, security alerts, colleague communications) | New inbox rules created within 24h of sign-in from new IP; rules forwarding to external domains; rules deleting emails matching specific sender/subject patterns |
| MFA method manipulation | Attacker registers additional MFA methods or modifies existing methods to maintain persistent access | New MFA method enrollment from unfamiliar device; MFA method downgrade (from FIDO2 to SMS); authentication method change within 24h of new-IP sign-in |

**Data Sources**: Identity provider audit logs (Entra ID, Okta), Exchange Online/Google Workspace admin logs, MFA registration logs

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Business email compromise | Using the hijacked session, attacker sends emails to colleagues, clients, or partners requesting wire transfers, payment redirection, or sensitive information | Emails sent from victim's account but from different IP/device; payment instruction emails with altered banking details; emails to finance department with urgency language |
| Internal lateral movement | Attacker uses the compromised account to access shared drives, internal applications, or target additional accounts within the organization | Access to SharePoint/OneDrive from the hijacked session; enumeration of organizational contacts and distribution lists |
| Data exfiltration | Attacker downloads sensitive documents, financial records, or customer data from the compromised account | Bulk download activity from cloud storage; email forwarding rules exfiltrating attachments to external addresses |

**Data Sources**: Email security (DLP), cloud access security broker (CASB), identity provider sign-in logs, data loss prevention alerts

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Wire fraud execution | BEC-initiated wire transfers directed to attacker-controlled accounts | Wire transfers to new beneficiaries initiated from or authorized by the compromised account; payment instruction changes coinciding with session hijack timing |
| Session token resale | Captured session tokens sold on dark web markets for use by other threat actors | Active session tokens appearing in underground markets; multiple distinct actors using the same compromised session |
| Credential database enrichment | Captured credentials (even if MFA-protected) added to credential databases for future credential stuffing campaigns | Compromised credentials appearing in subsequent credential stuffing attacks against other services |

**Data Sources**: Wire transfer monitoring, dark web monitoring, credential breach monitoring, identity provider sign-in anomaly detection

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering (phishing delivery)
- FT007.009: Impersonation of authority (spoofed login pages)
- FT011.001: Credential theft

**MITRE ATT&CK:**
- T1557: Adversary-in-the-Middle — core AiTM technique
- T1539: Steal Web Session Cookie — session token capture
- T1566.002: Spearphishing Link — phishing delivery
- T1114.003: Email Forwarding Rule — post-compromise persistence
- T1583.001: Acquire Infrastructure: Domains — phishing domain registration

**Group-IB Fraud Matrix:**
- Reconnaissance → Resource Development → Initial Access → Credential Access → Account Access → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 3 (Positioning) through identity provider anomaly detection or at Phase 4 (Execution) when a BEC wire transfer is flagged.

**Look Left**:
- P1: Domain registration monitoring would identify AiTM kit infrastructure during setup
- P1: Certificate Transparency monitoring for bulk cert issuance to suspicious domains
- P2: Email security would catch phishing delivery if link reputation is current

**Look Right**:
- P4: Compromised accounts used for BEC wire fraud (TP-0002)
- P5: Session tokens resold for downstream account takeover
- P5: Inbox rule manipulation enables long-term persistent access for ongoing fraud

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| AiTM kit developer | Tycoon 2FA, Evilginx, W3LL Panel, Caffeine, NakedPages, Greatness | High | $200–$1,500/month subscription |
| Domain registrar | Bulk domain registration for phishing pages | High | $10–$50/domain |
| Hosting provider | Bulletproof hosting for reverse proxy infrastructure | High | $50–$200/month |
| Template designer | Login page templates mimicking specific identity providers | Medium | $50–$500 per template |
| Session token buyer | Purchasers of captured session tokens for downstream fraud | High | $10–$500 per active session depending on target organization |

### Tool Ecosystem
- Evilginx3: open-source AiTM framework with modular "phishlets" for different identity providers
- Tycoon 2FA: commercial PhaaS platform with Telegram-based distribution
- W3LL Panel: sophisticated BEC-focused AiTM kit with built-in email collection
- Modlishka: open-source reverse proxy for credential interception
- GoPhish: legitimate phishing simulation tool repurposed for AiTM campaigns

### Intelligence Sources
- Sekoia.io, "Tycoon 2FA phishing kit analysis" (2025) — kit infrastructure and domain tracking
- Canadian Cyber Centre — FIDO2 effectiveness data (93.9% AiTM block rate)
- Microsoft Threat Intelligence — Entra ID AiTM detection patterns

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Domain monitoring for login page impersonation patterns | Detective | Cyber/Threat Intel |
| P2 | Deploy FIDO2/phishing-resistant MFA — blocks 93.9% of AiTM | Preventive | IT Security |
| P2 | Email security with real-time URL reputation and sandboxing | Preventive | Email Security |
| P3 | Entra ID / Okta sign-in risk policies: flag User-Agent inconsistencies between auth and access | Detective | Identity Security |
| P3 | Alert on inbox rule creation within 24h of new-IP authentication | Detective | SOC/Fraud |
| P4 | Conditional Access policies requiring compliant devices for sensitive applications | Preventive | IT Security |
| P5 | Wire transfer verification for payments initiated from sessions with identity anomalies | Preventive | Fraud/Payments |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate for phishing-resistant MFA deployment across organization |
| ASSESS | Level 3 (Established) | Risk assessment incorporating AiTM as primary MFA-bypass vector |
| PLAN | Level 3 (Established) | FIDO2 deployment roadmap; identity provider hardening plan |
| ACT | Level 4 (Advanced) | Real-time identity provider log analysis; User-Agent/IP correlation for session anomalies |
| MONITOR | Level 4 (Advanced) | Continuous monitoring of inbox rule changes, MFA method modifications, session token behavior |
| REPORT | Level 3 (Established) | Incident reporting capturing AiTM indicators for threat intelligence sharing |
| IMPROVE | Level 3 (Established) | Post-incident analysis feeding back into email security and identity provider policies |

---

## Detection Approaches

### Queries / Rules

```kql
-- Microsoft Sentinel KQL: Detect AiTM session token replay
-- User-Agent or IP mismatch between MFA completion and subsequent access
let mfa_events = SigninLogs
| where TimeGenerated > ago(24h)
| where AuthenticationRequirement == "multiFactorAuthentication"
| where ResultType == 0
| project MFATime=TimeGenerated, UserPrincipalName, MFA_IP=IPAddress,
          MFA_UserAgent=UserAgent, MFA_AppId=AppId;
let access_events = SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType == 0
| project AccessTime=TimeGenerated, UserPrincipalName, Access_IP=IPAddress,
          Access_UserAgent=UserAgent, Access_AppId=AppId;
mfa_events
| join kind=inner access_events on UserPrincipalName
| where AccessTime > MFATime and AccessTime < MFATime + 4h
| where MFA_IP != Access_IP or MFA_UserAgent != Access_UserAgent
| project UserPrincipalName, MFATime, AccessTime,
          MFA_IP, Access_IP, MFA_UserAgent, Access_UserAgent
```

```sigma
title: Post-Authentication Inbox Rule Creation from New IP
status: experimental
description: Detects inbox rule creation within 24h of sign-in from previously unseen IP
logsource:
    product: m365
    service: exchange
detection:
    selection_rule:
        Operation:
            - New-InboxRule
            - Set-InboxRule
            - Enable-InboxRule
    filter_known:
        ClientIP|cidr:
            - 10.0.0.0/8
            - 172.16.0.0/12
            - 192.168.0.0/16
    timeframe: 24h
    condition: selection_rule and not filter_known
fields:
    - UserId
    - ClientIP
    - Parameters
level: high
```

### Behavioral Analytics

- User-Agent string mismatch between MFA authentication event and subsequent session access
- Sign-in IP geographic impossibility (MFA from one country, session access from another within minutes)
- Inbox rule creation/modification within 24 hours of authentication from new IP address
- MFA method enrollment from device/location inconsistent with user's established pattern
- Bulk email access or forwarding rule creation following new authentication

### Cross-Team Correlation

- **Identity Security + Fraud**: Session anomalies correlated with subsequent wire transfer requests
- **Email Security + SOC**: Phishing delivery correlated with authentication anomalies and inbox rule changes
- **IT Security + Fraud**: FIDO2 deployment coverage gaps correlated with AiTM compromise patterns

---

## Operational Evidence

### EV-TP0067-2026-001: AiTM Phishing Kit Landscape 2025

- **Source**: Organized fraud detection in 2026: a technical landscape report; Sekoia.io AiTM kit analysis
- **Key Findings**: 11 major AiTM phishing kits active in early 2025. Tycoon 2FA is the most prevalent with 1,200+ domains targeting 500K+ organizations monthly. Credential phishing attacks surged 703% in H2 2024. Canadian Cyber Centre data shows FIDO2/phishing-resistant MFA blocks 93.9% of AiTM campaigns. AiTM kits operate as PhaaS with subscription pricing ($200–$1,500/month).
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: AiTM phishing kits have industrialized MFA-bypass attacks through a PhaaS model. The technical landscape report documents this as the most significant credential theft evolution, enabling downstream BEC and wire fraud at scale. The 703% surge in credential phishing reflects the accessibility of these kits to non-technical operators. FIDO2 deployment remains the highest-confidence mitigation, blocking 93.9% of AiTM attempts.

---

## Case Studies & References

- Sekoia.io, "Tycoon 2FA phishing kit: dissecting an AiTM campaign" (2025) — kit infrastructure analysis
- Canadian Centre for Cyber Security — FIDO2 effectiveness against AiTM (93.9% block rate)
- Microsoft Threat Intelligence, "AiTM phishing attacks: detection and mitigation guidance" — Entra ID detection patterns
- "Organized fraud detection in 2026: a technical landscape report" — BEC and AiTM phishing section
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) — credential phishing trends

---

## Analyst Notes

AiTM phishing kits fundamentally change the credential theft threat model: MFA is no longer a reliable defense unless it is phishing-resistant (FIDO2). Organizations that rely solely on push-notification or TOTP-based MFA are vulnerable to the entire AiTM kit ecosystem.

Key operational insight: detection has shifted from phishing content analysis (email body, URL reputation) to authentication telemetry analysis (identity provider logs). The most reliable detection signals are post-authentication anomalies — User-Agent mismatches, IP inconsistencies, and inbox rule manipulation — not the phishing email itself.

The PhaaS model means AiTM capability is no longer limited to sophisticated threat actors. Kit operators provide customer support, template updates, and infrastructure management, making AiTM attacks accessible to operators with minimal technical skill. This mirrors the FaaS model documented in TP-0054.

FIDO2 deployment should be the primary recommendation for any organization assessing this threat path. The 93.9% block rate is the strongest quantified mitigation in the fraud detection literature.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-22 | FLAME Project | Initial submission — sourced from technical landscape report (2026) |
