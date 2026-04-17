# TP-0067: AiTM Phishing Kit Infrastructure and Session Token Hijacking

```yaml
---
id: TP-0067
title: "AiTM Phishing Kit Infrastructure and Session Token Hijacking"
category: ThreatPath
date: 2026-03-22
author: "FLAME Project"
source: "Organized fraud detection in 2026: a technical landscape report; Phishing kits and AiTM platforms: a comprehensive threat intelligence reference (2026); Bluekit PhaaS Threat Intelligence Report (CrimsonVector, March 2026)"
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
  - T1111      # Multi-Factor Authentication Interception
  - T1098.005  # Account Manipulation: Device Registration
  - T1528      # Steal Application Access Token
  - T1185      # Browser Session Hijacking
  - T1550.004  # Use Alternate Authentication Material: Web Session Cookie
  - T1078.004  # Valid Accounts: Cloud Accounts
  - T1027      # Obfuscated Files or Information
ft3_tactics: ["FTA001", "FT007.009", "FT011.001"]
mitre_f3: ["F1006.002", "T1110.004", "T1539", "T1555", "F1004", "F1007", "T1185", "T1189", "T1451", "T1557"]
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
  - id: TP-0069
    relationship: related-to
  - id: TP-0079
    relationship: related-to
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-STIX-FCI
  - REG-WCI-2024
  - REG-CROWDSTRIKE-GTR-2026
baseline_ids: []
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
  - sneaky-2fa
  - mamba-2fa
  - evilproxy
  - flowerstorm
  - rockstar-2fa
  - nakedpages
  - w3ll-panel
  - greatness
  - caffeine
  - sessionshark
  - darcula
  - smishing-triad
  - wci-geographic-attribution
  - bluekit
  - phaas-market-fragmentation
  - vacuum-effect
  - antibot-cloaking
  - imperial-kitten
  - shinyhunters
  - cozy-bear
  - crowdstrike-gtr-2026
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
- T1557: Adversary-in-the-Middle — core AiTM reverse proxy/relay technique
- T1539: Steal Web Session Cookie — session token capture (primary objective)
- T1566.001/.002: Phishing via Attachment/Link — initial delivery
- T1111: Multi-Factor Authentication Interception — real-time MFA relay
- T1550.004: Use Alternate Authentication Material: Web Session Cookie — token replay
- T1098.005: Account Manipulation: Device Registration — post-compromise MFA addition
- T1528: Steal Application Access Token — OAuth abuse
- T1078.004: Valid Accounts: Cloud Accounts — replayed sessions
- T1114: Email Collection — post-compromise data access
- T1185: Browser Session Hijacking — session manipulation
- T1534: Internal Spearphishing — BEC lateral movement
- T1027: Obfuscated Files or Information — JavaScript/HTML obfuscation in kits
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
| AiTM kit developer | Tycoon 2FA, Evilginx, W3LL Panel, Caffeine, NakedPages, Greatness, Bluekit | High | $90–$350/month subscription ($90/7 days, $170/14 days, $350/month for Bluekit; $200–$1,500/month for established kits) |
| Domain registrar | Bulk domain registration for phishing pages | High | $10–$50/domain |
| Hosting provider | Bulletproof hosting for reverse proxy infrastructure | High | $50–$200/month |
| Template designer | Login page templates mimicking specific identity providers | Medium | $50–$500 per template |
| Session token buyer | Purchasers of captured session tokens for downstream fraud | High | $10–$500 per active session depending on target organization |

### Tool Ecosystem — Active AiTM Kits (2025–2026)

| Kit | Architecture | Key Signature | Price | Status |
|-----|-------------|---------------|-------|--------|
| Evilginx 3.x / Pro | Go reverse proxy with YAML phishlets | `X-Evilginx` header (community); 8-char alpha lure paths; rickroll redirect; `/s/<64hex>.js` canary | Open-source (Pro: paid) | Active — used by Scattered Spider, Star Blizzard, Void Blizzard, Storm-0485 |
| Tycoon 2FA | Synchronous relay (not true proxy) | Cloudflare Turnstile + "browser checks" text; admin panel stats categories; CYFIRMA YARA `Tycoon_2FA_Phishing_Indicators` | $120/10 days, $350/month | **Taken down March 4, 2026** — Europol-led, 330 domains seized |
| EvilProxy (Moloch) | Docker-based reverse proxy via TOR portal | "lmo." subdomain pattern; nginx reverse proxy; supports PyPI/npmjs (supply chain) | $150/10 days to $400/month | Active — ~280 servers, 150–250 customers |
| Rockstar 2FA → FlowerStorm | Storm-1575 lineage (Dadsec → Phoenix) | App ID `72782ba9-4490-4f03-8d82-562370ea3566`; hardcoded WebView/3.0 User-Agent; car-themed → botanical-themed HTML titles; `next.php` backend | ~$200/2 weeks, $350/month | Active — FlowerStorm surged within 10 days of Rockstar collapse |
| NakedPages | True Node.js reverse proxy (`nkp.app`) | Up to 9 sequential redirects via `href.li`; `.buzz` TLD long-name domains; Cloudflare Workers abuse; 120-country geofencing | $1,000 upfront | Active — ~220 servers, consistently top 5 |
| W3LL Panel OV6 | AiTM kit + 16 BEC tools | Anti-bot → Wikipedia redirect; Punycode email obfuscation; CONTOOL M365 monitoring | $500/3 months + $150/month | Active — 500+ threat actors, no arrests |
| Sneaky 2FA | PhaaS via Telegram bot (`@SneakyLog_bot`) | **Impossible device shift**: Safari/iOS for login → Edge/Windows for resume; food-content initial page ("Gourmet Delights"); base64 favicon SHA256 `5d91563b...`; empty HTML tags between characters | $200/month | Active — W3LL OV6 code reuse detected |
| Mamba 2FA | Socket.IO WebSocket relay | Socket.IO events: `new-session`, `password_command`, `otp_command`; URL pattern `/{m,n,o}/?{Base64}`; NO Cloudflare Turnstile; IPRoyal proxy masking | $250/month | Active — link domains rotate weekly |
| Greatness | M365-exclusive with Autograb | `/admin/js/mj.php` URI; `httpd.grt` config; blurred Excel + spinner lure; auto-steals victim logo/background | $120/month | Active — deploys on compromised WordPress |
| Caffeine | Open-registration PhaaS (no vetting) | Self-service web portal; Chinese/Russian templates; WordPress deployment via license tokens | $250–$850/month | Active |
| SessionShark | "Educational" proxy-based AiTM | Telegram bot exfiltration; custom HTTP headers to bypass threat intel feeds; dynamic content alteration for scanners | Unknown | Active (primarily advertised) |
| Bluekit | Fully managed AiTM dashboard; bulletproof/decentralized infrastructure; automated domain purchase | Antibot cloaking; safebrowsing bypass; CIS geo-blocking default; 40+ "1:1 copy" templates; Doraemon branding in forum posts | $90/7 days, $170/14 days, $350/month | Active — emerged 25 March 2026, post-Tycoon2FA takedown |
| Modlishka | Go single-domain transparent proxy | `/SayHello2Modlishka` panel; "id" tracking cookie; "ident" URL parameter | Open-source | Active — pen-test/red-team primary use |
| Muraena + NecroBrowser | Go proxy + Node.js/Puppeteer post-exploitation | TOML config; `/instrument` API endpoint; automated SSH key injection, inbox rule manipulation across headless Chromium instances | Open-source | Active — pioneered automated session exploitation |

### Intelligence Sources
- Sekoia.io, "Tycoon 2FA phishing kit analysis" (2025) — kit infrastructure and domain tracking
- Canadian Cyber Centre — FIDO2 effectiveness data (93.9% AiTM block rate)
- Microsoft Threat Intelligence — Entra ID AiTM detection patterns

---

## Law Enforcement Actions

| Date | Operation | Target | Outcome |
|------|-----------|--------|---------|
| November 2023 | Royal Malaysian Police + FBI + AFP | BulletProofLink / AnthraxBP | 8 arrests, ~$213K crypto seized; operator Adrian Bin Katong identified |
| August 2023 | INTERPOL | 16shop | 3 arrests (Indonesia, Japan); 21-year-old admin; 70K users, 150K+ domains |
| April 2024 | UK Metropolitan Police + Europol + 19 countries | LabHost | 37 arrests including developer Zak Coyne (8.5 years); 207 servers; 480K cards, 1M+ passwords stolen |
| November 2024 | Infrastructure collapse | Rockstar 2FA | Platform went offline; FlowerStorm absorbed customers within ~10 days |
| March 4, 2026 | Europol + Microsoft DCU + 11 partners | Tycoon 2FA (Storm-1747 / Saad Fridi) | 330 domains seized across 6 countries; phishing volume had dropped 57.6% pre-operation; defendant named in SDNY civil complaint |

Despite these victories, impact is consistently temporary — displaced customers migrate to successor platforms within days. The underlying economic incentives ($120–$1,500/month subscriptions) and low barriers to entry guarantee rapid successor proliferation.

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
| P2 | Deploy Continuous Access Evaluation (CAE) with Strict Location Enforcement — rejects stolen tokens replayed from outside trusted networks | Preventive | IT Security |
| P3 | Enable Token Protection (Primary Refresh Token binding) — cryptographically ties tokens to device | Preventive | IT Security |
| P3 | Require compliant/Intune-managed devices via Conditional Access for sensitive applications | Preventive | IT Security |
| P2 | Browser-based real-time AiTM detection (e.g., Push Security) analyzing page behavioral attributes during authentication | Detective | IT Security |

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
// Microsoft Sentinel KQL: Detect AiTM session token replay (DL-0137)
// User-Agent or IP mismatch between MFA completion and subsequent access
let mfa_events = SigninLogs
| where TimeGenerated > ago(24h)
| where AuthenticationRequirement == "multiFactorAuthentication"
| where ResultType == 0
| project MFATime=TimeGenerated, UserPrincipalName, MFA_IP=IPAddress,
          MFA_UserAgent=UserAgent, MFA_AppId=AppId;
let access_events = SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType == 0
// Exclude MFA events to prevent self-join noise
| where AuthenticationRequirement != "multiFactorAuthentication"
| project AccessTime=TimeGenerated, UserPrincipalName, Access_IP=IPAddress,
          Access_UserAgent=UserAgent, Access_AppId=AppId;
mfa_events
| join kind=inner access_events on UserPrincipalName
// Access must occur 5min–4h after MFA (skip trivially close auth flow events)
| where AccessTime > MFATime + 5m and AccessTime < MFATime + 4h
| where MFA_IP != Access_IP or MFA_UserAgent != Access_UserAgent
| project UserPrincipalName, MFATime, AccessTime,
          MFA_IP, Access_IP, MFA_UserAgent, Access_UserAgent
```

```kql
// Microsoft Sentinel KQL: Same SessionId from Multiple IPs (DL-0146)
// Strongest AiTM detection signal — phishing proxy IP and attacker replay IP on same session
let timeWindow = 4h;
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType == 0
| summarize
    IPCount = dcount(IPAddress),
    IPs = make_set(IPAddress),
    UserAgents = make_set(UserAgent),
    AppIds = make_set(AppId),
    MinTime = min(TimeGenerated),
    MaxTime = max(TimeGenerated),
    RiskLevels = make_set(RiskLevelDuringSignIn)
  by SessionId, UserPrincipalName
| where IPCount >= 2
| where datetime_diff('hour', MaxTime, MinTime) <= 4
| project UserPrincipalName, SessionId, IPCount, IPs, UserAgents,
          AppIds, MinTime, MaxTime, RiskLevels
```

```sigma
title: Post-Compromise Inbox Rule Manipulation (DL-0138 — Standalone)
status: experimental
description: >
  Basic detection: inbox rule creation from non-RFC1918 IP.
  For the full correlated detection (new-IP sign-in + inbox rule), use the
  KQL queries in DL-0138 which perform cross-log temporal correlation.
logsource:
    product: m365
    service: exchange
detection:
    selection:
        Operation:
            - New-InboxRule
            - Set-InboxRule
            - Enable-InboxRule
    filter_internal:
        ClientIP|cidr:
            - 10.0.0.0/8
            - 172.16.0.0/12
            - 192.168.0.0/16
    condition: selection and not filter_internal
fields:
    - UserId
    - ClientIP
    - Parameters
level: high
falsepositives:
    - Users creating inbox rules from external networks (home, mobile)
    - Cloud-hosted email management tools with non-RFC1918 IPs
    - Corporate networks using public IP NAT for Exchange clients
```

### Behavioral Analytics

- User-Agent string mismatch between MFA authentication event and subsequent session access
- Sign-in IP geographic impossibility (MFA from one country, session access from another within minutes)
- Inbox rule creation/modification within 24 hours of authentication from new IP address
- MFA method enrollment from device/location inconsistent with user's established pattern
- Bulk email access or forwarding rule creation following new authentication

### Kit-Specific Detection Fingerprints

Each AiTM kit leaves distinctive artifacts enabling targeted detection:

| Kit | Network/Log Signature | Detection Method |
|-----|----------------------|-----------------|
| Evilginx (community) | `X-Evilginx` HTTP header; Go TLS JA3 fingerprint distinct from real browsers | HTTP header inspection; JA3/JA4 TLS fingerprinting |
| Evilginx (all) | 8-char alphabetic lure paths; rickroll redirect for unauthorized visitors; `/s/<64hex>.js` canary (content-length=0) | URL pattern matching; redirect behavior analysis |
| Tycoon 2FA | Cloudflare Turnstile with "this page is running browser checks to ensure your security" text | Page content inspection; CYFIRMA YARA rule `Tycoon_2FA_Phishing_Indicators` |
| Sneaky 2FA | **Impossible device shift**: different User-Agent per auth step (Safari/iOS for `Login:login`, Edge/Windows for `Login:resume`) | Sigma correlation rule: mismatched UAs within same correlation ID within 10 minutes |
| Mamba 2FA | Socket.IO WebSocket events (`new-session`, `password_command`, `otp_command`); URL pattern `/{m,n,o}/?{Base64}` | WebSocket traffic analysis; URL pattern matching |
| Rockstar 2FA / FlowerStorm | Office365 App ID `72782ba9-4490-4f03-8d82-562370ea3566`; hardcoded User-Agent `Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0)...` | Entra ID sign-in log filtering on AppId + UserAgent |
| Greatness | URI path `/admin/js/mj.php`; config file `httpd.grt`; blurred Excel + spinner before redirect | WAF/proxy URI pattern detection |
| NakedPages | `nkp.app` binary; `href.li` referrer stripping; `.buzz` TLD with long descriptive names | Domain intelligence; referrer chain analysis |
| Darcula | `registry[.]magic-cat[.]world` container registry; `com-` domain prefix pattern; React client-side rendering | Domain pattern matching; infrastructure fingerprinting |
| Chenlun | `ResourceRedConfig.js` and `/ResourceConfig/urlConfig.json` files | Web content analysis |

### Microsoft Entra ID Log-Based Detection

The strongest AiTM detection signals in Entra ID:

1. **Same SessionId from multiple IPs** — the phishing proxy IP and the attacker's replay IP appear on the same session
2. **Error code sequence**: 50074 (MFA required) → 50140 (Keep Me Signed In) → 0 (success) in rapid succession with medium/high risk
3. **OfficeHome application ID** (`4765445b-32c6-49b0-83e6-1d93765276ca`) commonly appears in token replay
4. **AnomalousToken risk detection** in Entra ID Identity Protection (Risky Sign-ins blade)
5. **Post-compromise UAL indicators**: Exchange Online operations `New-InboxRule`, `Set-InboxRule`, `Set-Mailbox` (forwarding), new MFA device registration from suspicious IPs

**Published detection resources:**
- Microsoft Sentinel: `PossibleAiTMPhishingAttemptAgainstAAD.yaml` analytic rule
- reprise99: `Identity-PotentialAiTM.kql` (error code + risk level correlation)
- Bert-JanP: `PotentialAiTMPhishing.md` hunting query
- Splunk: `O365 Concurrent Sessions From Different IPs` (detection ID: 58e034de)
- PhishingKit-Yara-Rules repo (github.com/t4d/PhishingKit-Yara-Rules): 850+ YARA rules covering 300+ brands

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

### EV-TP0067-2026-002: Tycoon 2FA Takedown and Scale

- **Source**: Phishing kits and AiTM platforms: a comprehensive threat intelligence reference (2026); Microsoft DCU; Europol
- **Key Findings**: Tycoon 2FA was responsible for 62% of all phishing blocked by Microsoft, generating ~30 million phishing emails per month targeting 500,000+ organizations. Over its lifetime it operated ~24,000 domains with ~2,000 subscribers, producing 64,000+ confirmed phishing incidents. Operator tracked as Storm-1747 (Saad Tycoon Group); named defendant Saad Fridi of Pakistan. Bitcoin wallet `19NReVFKJsYYCCFLq1uNKYrUqQE2bB4Jwx` accumulated $250,000+ since August 2023. Europol-led takedown on March 4, 2026 seized 330 domains across 6 countries with 11 private-sector partners.
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High

### EV-TP0067-2026-003: EvilProxy C-Suite Targeting

- **Source**: Proofpoint (2023); phishing kit intelligence reference
- **Key Findings**: March–June 2023 EvilProxy campaign sent 120,000 phishing emails to hundreds of organizations. 39% of compromised users were C-level executives (17% CFOs, 9% CEOs). Campaign exploited YouTube and SlickDeals open redirectors. A July 2023 campaign exploited an indeed.com open redirect specifically targeting U.S. C-suite executives. EvilProxy supports PyPI and npmjs targeting, enabling software supply chain attacks.
- **CFPF Phase Coverage**: P2–P4
- **Confidence**: High

### EV-TP0067-2026-004: FIDO2 Proven Effectiveness

- **Source**: Google, Cloudflare, Microsoft, NIST SP 800-63-4
- **Key Findings**: Google experienced zero successful phishing attacks against 85,000+ employees after FIDO2 deployment. Cloudflare blocked the 0ktapus campaign (August 2022) — employees with FIDO2 keys were protected even after clicking phishing links and entering credentials. Microsoft reports 92% of employee accounts protected with phishing-resistant MFA. NIST SP 800-63-4 (finalized July 2025) requires AAL2 to offer a phishing-resistant option; AAL3 requires non-exportable private keys.
- **CFPF Phase Coverage**: P2
- **Confidence**: High

### EV-TP0067-2026-005: Bluekit PhaaS Platform Emergence

- **Source**: OSINT analysis — Reza Abasi (LinkedIn), Cracked/OGUsers/Patched forum posts, Telegram channel monitoring, bluekit[.]cc analysis
- **Key Findings**: Bluekit is a fully managed PhaaS platform that emerged 21 days after the Europol-led Tycoon2FA takedown (4 March 2026). Advertised on Cracked forum on 25 March 2026 by a newly created "Premium Member" account, then cross-posted to OGUsers and Patched by throwaway accounts. Platform offers 40+ ready-to-use templates targeting Microsoft, Outlook, Okta, Citrix, Bank of America, Wells Fargo, PayPal, and 9+ cryptocurrency exchanges (Binance, Coinbase, Bybit, OKX, Kucoin, Gate, Upbit, MEXC, crypto.com). Key capabilities include full 2FA bypass with geolocation/browser emulation, session cookie/local storage/keyboard capture, automated domain purchase, antibot cloaking, safebrowsing bypass, and AI assistant. March 27 changelog (2 days post-launch) added CIS geo-blocking policy, Outlook full-access session hijacking via OTP capture, French banking templates (Credit Agricole, La Banque Postale, Robinhood), and IP/country whitelist. Attribution indicators point to Eastern European (likely Russian-speaking) operator: CIS exclusion policy, Jabber on exploit[.]im, "petrushka" handle pattern, rapid dev velocity suggesting pre-existing team.
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: Medium — OSINT-derived from forum posts and public Telegram; platform is newly launched with limited operational history

### EV-TP0067-2026-006: IMPERIAL KITTEN EvilGinx2 Campaign (CrowdStrike 2026)

- **Source**: CrowdStrike, "Global Threat Report 2026"
- **Geography**: Israel
- **CFPF Phase Coverage**: P1, P2, P3
- **Confidence**: High
- **Summary**: Iran-nexus adversary IMPERIAL KITTEN conducted credential phishing against Israeli Microsoft 365 users in November 2025 using the AiTM toolkit EvilGinx2 with Israel-themed infrastructure and English/Hebrew-language lures. This represents significant evidence of state-nexus adoption of commercial AiTM tooling — a nation-state intelligence operation leveraging the same PhaaS-grade AiTM infrastructure documented across the criminal ecosystem in this threat path.

### EV-TP0067-2026-007: ShinyHunters CRM SaaS Targeting (CrowdStrike 2026)

- **Source**: CrowdStrike, "Global Threat Report 2026"
- **Geography**: Global
- **CFPF Phase Coverage**: P2, P3, P4
- **Confidence**: High
- **Summary**: Between January and August 2025, ShinyHunters conducted social engineering campaigns targeting CRM instances via AiTM phishing pages. CRM emerged as a key exfiltration target in 2025, extending the AiTM threat beyond traditional email/identity provider compromise to SaaS applications containing customer data, sales pipelines, and financial records.

### EV-TP0067-2026-008: COZY BEAR OAuth 2.0 Device Code Phishing (CrowdStrike 2026)

- **Source**: CrowdStrike, "Global Threat Report 2026"
- **Geography**: United States
- **CFPF Phase Coverage**: P1, P2, P3
- **Confidence**: High
- **Summary**: Russia-nexus adversary COZY BEAR systematically exploited interpersonal trust to compromise US-based targets through a multi-layered trust exploitation campaign. The attack chain involved: (1) compromising or impersonating individuals from international NGOs, (2) delivering Entra ID OAuth 2.0 authorization code and device code phishing links that redirected to authentic Microsoft login pages, and (3) sustaining multi-day conversations across IM, email, and video conferencing to build rapport before delivering phishing payloads. Timeline example: Day 1 initial contact, Day 5 email access from a legitimate compromised account, Day 31 pivot to a new target. This demonstrates how state actors augment AiTM tooling with sustained social engineering to defeat user vigilance.

### EV-TP0067-2026-009: PaaS Subdomain Hosting for AiTM Pages (Interisle 2025)

- **Source**: Interisle Consulting Group, "Phishing Landscape 2025" (September 2025); cross-reference TP-0079
- **Geography**: Global
- **CFPF Phase Coverage**: P1
- **Confidence**: High
- **Summary**: Interisle's 2025 analysis documents explosive growth in abuse of PaaS subdomain hosting for phishing pages, including AiTM landing pages. Cloudflare pages.dev saw a +157% increase in phishing abuse, Webflow +980%, and Vercel +279%. These platforms provide attacker-controlled subdomains under high-reputation parent domains, effectively bypassing domain reputation filters and browser safelist protections. AiTM kit operators increasingly deploy reverse proxy infrastructure on these PaaS platforms rather than registering dedicated phishing domains — reducing infrastructure cost and improving evasion. See TP-0079 for the dedicated gTLD/subdomain abuse threat path.

---

## References

- Sekoia.io, "Tycoon 2FA phishing kit: dissecting an AiTM campaign" (2025) — kit infrastructure analysis
- Canadian Centre for Cyber Security — FIDO2 effectiveness against AiTM (93.9% block rate)
- Microsoft Threat Intelligence, "AiTM phishing attacks: detection and mitigation guidance" — Entra ID detection patterns
- "Organized fraud detection in 2026: a technical landscape report" — BEC and AiTM phishing section
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) — credential phishing trends
- "Phishing kits and AiTM platforms: a comprehensive threat intelligence reference" (2026) — comprehensive kit catalog and detection engineering
- Europol, "Tycoon 2FA PhaaS takedown" (March 4, 2026) — 330 domains seized, Storm-1747 attribution
- Proofpoint, "EvilProxy C-suite targeting campaign" (2023) — 120K emails, 39% C-level compromise rate
- NIST SP 800-63-4 (July 2025) — AAL2/AAL3 phishing-resistant MFA requirements
- Google, "Security Keys: Practical Cryptographic Second Factors for the Modern Web" — zero phishing after FIDO2
- Cloudflare, "The mechanics of a sophisticated phishing scam" (August 2022) — 0ktapus campaign blocked by FIDO2
- Group-IB, "W3LL DONE" (September 2023) — W3LL Store and Panel OV6 analysis
- Sekoia TDR, "Sneaky 2FA" (December 2024) — impossible device shift detection
- Sekoia TDR, "Mamba 2FA" (May 2024) — Socket.IO relay analysis
- CrimsonVector (Diego Parra), "Bluekit PhaaS Threat Intelligence Report" (30 March 2026) — platform emergence, template analysis, evasion capabilities, attribution indicators
- CrowdStrike, "Tycoon2FA Phishing-as-a-Service Platform Persists After Takedown" (March 2026) — post-takedown resilience analysis
- Barracuda Networks, PhaaS threat review (January 2026) — PhaaS kit doubling statistic
- KnowBe4, "The Rise of Kratos" (February 2026) — 90% credential compromise prediction
- CrowdStrike, "Global Threat Report 2026" — IMPERIAL KITTEN EvilGinx2 campaign, ShinyHunters CRM targeting, COZY BEAR OAuth 2.0 device code phishing
- Interisle Consulting Group, "Phishing Landscape 2025" (September 2025) — PaaS subdomain hosting abuse for phishing/AiTM pages (Cloudflare pages.dev, Webflow, Vercel)

---

## Analyst Notes

AiTM phishing kits fundamentally change the credential theft threat model: MFA is no longer a reliable defense unless it is phishing-resistant (FIDO2). Organizations that rely solely on push-notification or TOTP-based MFA are vulnerable to the entire AiTM kit ecosystem.

Key operational insight: detection has shifted from phishing content analysis (email body, URL reputation) to authentication telemetry analysis (identity provider logs). The most reliable detection signals are post-authentication anomalies — User-Agent mismatches, IP inconsistencies, and inbox rule manipulation — not the phishing email itself.

The PhaaS model means AiTM capability is no longer limited to sophisticated threat actors. Kit operators provide customer support, template updates, and infrastructure management, making AiTM attacks accessible to operators with minimal technical skill. This mirrors the FaaS model documented in TP-0054.

FIDO2 deployment should be the primary recommendation for any organization assessing this threat path. The 93.9% block rate is the strongest quantified mitigation in the fraud detection literature.

The March 2026 Tycoon 2FA takedown is the most significant law enforcement action against the PhaaS ecosystem to date, but historical precedent (BulletProofLink, LabHost, Rockstar 2FA) shows displaced customers migrate to successor platforms within days. Organizations should use the post-takedown window to accelerate FIDO2 deployment rather than assume diminished threat.

Post-authentication token protection is emerging as the critical second layer. FIDO2 prevents credential theft but does not eliminate token replay if sessions are established through other means. The complete defensive stack requires FIDO2 + Continuous Access Evaluation (CAE) + Token Protection + compliant device requirements + risk-based Conditional Access policies.

Detection engineering should leverage kit-specific fingerprints: the impossible device shift (Sneaky 2FA), hardcoded application IDs (Rockstar 2FA/FlowerStorm), Socket.IO WebSocket events (Mamba 2FA), and URI patterns (Greatness) provide high-fidelity, low-false-positive detection signals that complement behavioral analytics.

**Bluekit Evasion Capabilities (March 2026)**: The newly emerged Bluekit PhaaS platform introduces several evasion features that directly challenge existing detection layers: (1) configurable antibot cloaking designed to evade automated security scanners, (2) safebrowsing bypass specifically targeting Google Safe Browsing red alerts, (3) geolocation and browser fingerprint emulation to defeat location-based anomaly detection, and (4) CAPTCHA disable option for iframe integration. The March 27 changelog's improvement to Outlook session hijacking — capturing full access via one-time codes rather than just passwords — indicates the platform is specifically optimizing for enterprise email account takeover. Organizations relying on OTP-based MFA for Outlook/Exchange are directly exposed.

**Post-Tycoon2FA Market Fragmentation (March 2026)**: The PhaaS ecosystem is experiencing explosive growth despite headline takedown successes. Active PhaaS kits doubled during 2025 (Barracuda). By end of 2026, an estimated 90% of credential compromise attacks will be enabled by modular PhaaS kits (KnowBe4). The Tycoon2FA takedown created a reputational and trust vacuum — even though Tycoon2FA resumed operations within days (CrowdStrike observed activity returning to pre-disruption levels by March 6), the brand damage among criminal customers who value operational stability created a market opening. Bluekit's emergence 21 days post-takedown is a textbook example of this "vacuum effect." Additional new entrants include Kratos, Whisper 2FA, GhostFrame, EvilTokens (device code phishing), Sneaky 2FA, and CoGUI — indicating the market is fragmenting and specializing rather than consolidating.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-22 | FLAME Project | Initial submission — sourced from technical landscape report (2026) |
| 2026-03-23 | FLAME Project | Major enrichment: added 13 kit profiles, Tycoon 2FA takedown, kit-specific detection fingerprints, Entra ID log detection, expanded MITRE ATT&CK (12 techniques), law enforcement timeline, 3 new operational evidence entries, CAE/Token Protection controls — sourced from phishing kit intelligence reference |
| 2026-03-30 | FLAME Project | Enrichment: Bluekit PhaaS platform (EV-TP0067-2026-005), PhaaS market fragmentation analysis, evasion capabilities, post-Tycoon2FA vacuum effect — sourced from Bluekit PhaaS TI report (CrimsonVector) and CrowdStrike post-takedown analysis |
| 2026-04-01 | FLAME Project | Enrichment: CrowdStrike GTR 2026 — IMPERIAL KITTEN EvilGinx2, ShinyHunters CRM targeting, COZY BEAR OAuth device code phishing; Interisle 2025 PaaS subdomain hosting abuse; added TP-0079 cross-reference |
