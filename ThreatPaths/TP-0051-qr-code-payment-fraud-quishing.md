# TP-0051: QR Code Payment Fraud / Quishing

```yaml
---
id: TP-0051
title: "QR Code Payment Fraud / Quishing"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - quishing
  - credential-stuffing
  - account-takeover
  - social-engineering
sector:
  - banking
  - payments
  - retail
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 82
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1566.002  # Phishing: Spearphishing Link
  - T1204.001  # User Execution: Malicious Link
  - T1056.003  # Input Capture: Web Portal Capture
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FTA009", "FT016"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0012
    relationship: related-to
  - id: TP-0037
    relationship: related-to
  - id: TP-0050
    relationship: enhances
regulatory_refs:
  - REG-CFPB-REGE
  - REG-UK-PSR-APP
  - REG-PSD3-SCA
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - qr-code-fraud
  - quishing
  - credential-harvesting
  - fake-bank-login
  - marketplace-fraud
  - 2fa-bypass
  - mobile-money
  - post-office-impersonation
---
```

## Summary

QR code payment fraud — colloquially termed "quishing" — exploits consumer trust in QR technology by distributing malicious codes via email, SMS, public posters, digital ads, and online marketplaces. INTERPOL's 2026 Threat Assessment documents a specific European modus operandi in which fraudsters impersonate buyers on online marketplaces, migrate victims off-platform to messaging apps using local phone numbers, and then send a fake QR code claiming that payment is available for collection at a local post office. Scanning the code leads to a fraudulent website impersonating the post office, where a "Receive Money" prompt redirects victims through a bank-selection menu to a fake bank login page. Entering credentials grants the fraudster full account access; the attacker immediately enrolls a new two-factor authentication (2FA) device to lock the victim out of notifications, then drains funds via mobile money transfer. In one documented European case, over USD 110,000 was stolen through this method. The attack chain is fast, highly localized, and exploits a fundamental gap in QR code UX: unlike hyperlinks, QR codes do not display a destination URL before the victim commits to following them.

## Threat Path Hypothesis

> **Hypothesis**: Actors exploit consumer trust in QR codes — normalized during COVID-era contactless payment adoption — to redirect marketplace sellers to credential-harvesting pages impersonating legitimate banking or postal service portals. By initiating contact as a credible buyer and migrating the conversation off-platform before delivering the malicious QR code, attackers evade marketplace fraud detection systems. The subsequent 2FA device enrollment step is the critical escalation point: it converts credential capture into persistent, uninterrupted account control.

**Confidence**: Medium-High (82) — INTERPOL GFFTA 2026 documents a concrete European case with a confirmed USD 110,000 loss figure and a clearly described step-by-step modus operandi. The quishing vector is also corroborated by broader trend reporting across European member countries.

**Estimated Impact**: USD 5,000–110,000+ per victim (single-incident ceiling observed). Campaign-level losses scale with the number of marketplace sellers targeted.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Target identification on online marketplaces | Fraudsters survey online marketplace listings (classified ads, second-hand goods platforms) for high-value items to identify motivated sellers who will respond quickly to apparent buyer interest | Newly created buyer accounts on marketplace platforms with limited transaction history; multiple inquiries across high-value listings within short windows |
| Infrastructure provisioning | Register fraudulent domains impersonating local post offices and banking institutions; configure fake bank login pages with institution-specific branding; acquire local phone numbers to increase credibility when migrating victims off-platform | Newly registered domains impersonating postal or banking brands; hosting infrastructure in jurisdictions with weak takedown response; local virtual number acquisition |
| QR code generation | Generate malicious QR codes pointing to fraudulent post office impersonation sites; prepare localized content matching regional institution branding (language, logo, UX) | QR code URLs pointing to domains registered within 30 days; site content in victim's local language impersonating national postal service |

**Data Sources**: Domain registration feeds, marketplace abuse reports, virtual phone number registrar logs, threat intelligence feeds for post office / bank impersonation sites

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Buyer impersonation on marketplace | Fraudster contacts marketplace seller posing as a legitimate buyer, expresses serious purchase interest, and initiates conversation using platform messaging | Buyer account with no transaction history or reviews; rapid escalation from first contact to purchase agreement; unusually high offered price with no negotiation |
| Off-platform conversation migration | Fraudster requests that the seller continue communication via a messaging app (WhatsApp, Telegram, Signal), citing "convenience" or "faster payment processing," providing a local phone number to reinforce legitimacy | Requests to leave marketplace messaging environment within first 1–3 messages; provision of local phone numbers by overseas-based actors |
| QR code delivery with payment pretext | Fraudster sends a QR code image via the messaging app, claiming a payment for the goods has been sent to the local post office for the seller to collect | QR code image sent via messaging platform; payment pretext referencing postal collection; urgency framing ("collect within 24 hours") |

**Target**: Consumer (marketplace sellers)

**Data Sources**: Marketplace platform messaging logs, off-platform referral detection, messaging app abuse reports, QR code delivery patterns

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Fraudulent post office site delivery | Scanning the malicious QR code loads a website impersonating the victim's national post office, displaying a "payment waiting for collection" message and a "Receive Money" call-to-action button | Navigation to newly-registered domain impersonating national postal brand; site UX cloned from legitimate postal service; QR scan event initiating navigation |
| Bank selection redirect | Victim clicks "Receive Money" and is presented with a dropdown or grid of national banking institutions; selecting their bank redirects to a fake bank login page cloned from the genuine institution | Intermediate redirect through post office impersonation page to banking impersonation page; domain chaining on separate hosting infrastructure; bank-specific CSS/logo assets loaded from fraudulent domain |
| Credential capture page | Victim is presented with a convincing replica of their bank's online login interface, including username, password, and potentially OTP/PIN fields | Login form POST destination is a fraudulent domain; site certificate is newly issued (Let's Encrypt on newly-registered domain); no prior appearance in threat intelligence feeds |

**Data Sources**: Web proxy logs, DNS resolution logs, certificate transparency logs, browser telemetry for QR-scan-to-navigation events

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Banking credential capture | Victim submits login credentials on the fake bank login page; credentials are passed to the fraudster's backend in real time, enabling near-instantaneous account access | Authentication event from unrecognized device/IP immediately following credential submission; credential submission to non-legitimate domain detected by web proxy |
| 2FA device enrollment | Fraudster immediately logs into the victim's real bank account and initiates enrollment of a new 2FA device (authenticator app, SMS number, or hardware token), using the captured credentials; this blocks the victim from receiving legitimate authentication notifications | New 2FA device enrollment from previously unseen device/IP; enrollment occurring within seconds to minutes of legitimate credential entry; victim's existing 2FA device receiving no further authentication requests |
| Mobile money transfer initiation | With persistent account access secured via the new 2FA device, the fraudster initiates one or more mobile money or wire transfers to mule accounts, draining available balances and credit lines | High-value outbound transfer(s) to new beneficiary within minutes of account access; transfer amount(s) approaching or equaling available balance; beneficiary account opened recently or flagged as mule |

**Data Sources**: Bank authentication logs, device enrollment audit trails, transaction monitoring systems, mobile money transfer logs, behavioral biometrics

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Mobile money drain | Captured funds transferred via mobile money platform to mule accounts; mules rapidly cash out or forward funds through additional hops | High-velocity outbound mobile money transactions from victim account; mule account receiving multiple inbound transfers in short window |
| Further account exploitation | With persistent 2FA access secured, fraudster may continue exploiting the account over subsequent days — opening credit facilities, authorizing additional payments, or using stored card details for card-not-present fraud | Account access events continuing after initial drain event; new credit applications initiated without victim knowledge; card-not-present transactions on stored payment methods |
| Credential resale | Banking credentials and account access details may be packaged and sold on underground markets for further exploitation by other actors | Victim account appearing in credential breach feeds; account access from multiple distinct actor infrastructure sets days after initial compromise |

**Data Sources**: Transaction monitoring, fraud reporting systems, dark web monitoring, account access audit logs, card-not-present fraud alerts

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001: Social Engineering
- FTA009: Phishing
- FT016: Brand Impersonation

**MITRE ATT&CK:**

- T1566.002: Phishing: Spearphishing Link — malicious QR code directing victim to credential-harvesting site
- T1204.001: User Execution: Malicious Link — victim scanning QR code and navigating to fraudulent site
- T1056.003: Input Capture: Web Portal Capture — fake bank login page capturing banking credentials
- T1583.001: Acquire Infrastructure: Domains — fraudulent post office and bank impersonation domains

**Group-IB Fraud Matrix:**

- Reconnaissance → Resource Development → Initial Access → End-user Interaction → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P3/P4** — typically discovered when the victim attempts to log into their real bank account after credential submission and finds themselves locked out (2FA device changed), or when transaction monitoring flags the high-value mobile money transfer to a new beneficiary.

**Look Left** (what did you miss before discovery?):

- Fraudulent domain registration impersonating local postal or banking brands in the days prior to campaign launch (certificate transparency logs, newly-registered domain feeds)
- Marketplace buyer accounts created with no transaction history targeting high-value listings — early indicator of quishing campaign targeting sellers
- Off-platform conversation migration request in marketplace messaging system — the clearest pre-attack behavioral signal before QR code delivery
- QR code image files delivered via messaging apps linking to newly-registered domains

**Look Right** (what comes next after discovery?):

- 2FA device enrollment change persists after credential capture — remediation requires bank-side 2FA reset, not just password change
- Additional account exploitation may continue for days if 2FA is not revoked by the institution
- Victim's banking credentials may have already been exfiltrated and sold — downstream use by other actors should be anticipated
- Same fraudulent infrastructure (post office / bank impersonation sites) likely targeting additional marketplace sellers in parallel — threat intelligence sharing with the platform can interrupt the campaign

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor certificate transparency logs and newly-registered domain feeds for domains impersonating national postal services and banking institutions; feed to blocklists | Detective | Cyber |
| P2 | Marketplace platforms: detect and alert on off-platform conversation migration requests (messages containing external phone numbers or messaging app handles); flag for manual review | Detective | Fraud |
| P2 | Marketplace platforms: implement seller education warnings when conversation appears to be moving off-platform | Preventive | Fraud |
| P3 | Implement QR code URL reputation scanning at the network edge (web proxy, mobile MDM) — resolve QR destination URLs and check against domain age and threat feeds before allowing navigation | Preventive | Cyber |
| P3 | Browser / mobile OS: surface QR code destination URL to user before navigation (OS-level UX improvement) | Preventive | IT |
| P4 | Banking: alert customers in real time when a new 2FA device is enrolled, via out-of-band channel (push notification to existing enrolled device, email) | Detective | Fraud |
| P4 | Banking: require step-up authentication (call-back or in-branch) for 2FA device enrollment from a new device/IP, especially when following recent credential change | Preventive | Fraud |
| P4 | Transaction monitoring: flag high-value mobile money transfers to new beneficiaries within 30 minutes of new device authentication | Detective | Fraud |
| P5 | Rapid account freeze and 2FA device revocation for customers reporting marketplace-related fraud or credential phishing | Responsive | Fraud |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Recognize quishing as a distinct credential-harvesting vector separate from email phishing |
| ASSESS | Level 3 (Established) | Risk assessment covers QR code attack surface in consumer-facing payment and marketplace contexts |
| PLAN | Level 2 (Developing) | Incident response playbook for 2FA device hijacking and mobile money drain events |
| ACT | Level 3 (Established) | 2FA device enrollment monitoring integrated with real-time fraud alerting and account freeze capability |
| MONITOR | Level 3 (Established) | KRIs for new 2FA device enrollments, mobile money velocity post-authentication, and marketplace off-platform migration signals |
| REPORT | Level 2 (Developing) | Quishing-related losses included in SAR narratives; correct BSA fraud categories applied |
| IMPROVE | Level 2 (Developing) | Post-incident reviews from quishing cases drive 2FA enrollment policy hardening |

---

## Detection Approaches

### Queries / Rules

**QR Code Destination URL — Newly-Registered Domain Detection (Splunk SPL)**

```spl
index=web_proxy sourcetype=proxy_logs
| where url_category="qr-scan" OR referrer_category="qr-scan"
| rex field=url "https?://(?P<fqdn>[^/]+)"
| lookup domain_age_feed fqdn OUTPUT domain_age_days, domain_registrar
| where domain_age_days < 30
| stats count by fqdn, domain_age_days, src_ip, user
| where count > 1
| sort -domain_age_days
```

**New 2FA Device Enrollment Following Recent Authentication (SQL)**

```sql
SELECT a.account_id, a.auth_timestamp, a.auth_ip, a.auth_device_id,
       e.enrollment_timestamp, e.enrolled_device_id, e.enrollment_ip,
       DATEDIFF('minute', a.auth_timestamp, e.enrollment_timestamp) AS minutes_to_enrollment
FROM auth_events a
JOIN mfa_device_enrollments e ON a.account_id = e.account_id
WHERE e.enrollment_timestamp > a.auth_timestamp
AND DATEDIFF('minute', a.auth_timestamp, e.enrollment_timestamp) < 10
AND a.auth_device_id != e.enrolled_device_id
AND a.auth_ip != e.enrollment_ip
ORDER BY minutes_to_enrollment ASC;
```

**Mobile Money Transfer Velocity Post-New-Device-Auth (SQL)**

```sql
SELECT t.account_id, t.transfer_timestamp, t.beneficiary_account_id,
       t.amount, t.currency, e.enrollment_timestamp,
       DATEDIFF('minute', e.enrollment_timestamp, t.transfer_timestamp) AS minutes_post_enrollment
FROM transactions t
JOIN mfa_device_enrollments e ON t.account_id = e.account_id
WHERE t.transfer_type IN ('mobile_money', 'faster_payment', 'wire')
AND t.beneficiary_is_new = TRUE
AND t.transfer_timestamp > e.enrollment_timestamp
AND DATEDIFF('minute', e.enrollment_timestamp, t.transfer_timestamp) < 60
AND t.amount > 1000
ORDER BY t.amount DESC;
```

### Behavioral Analytics

- Marketplace seller accounts receiving buyer contact from accounts with zero transaction history, followed by off-platform migration request, is the earliest reliable signal for this attack chain
- QR code scan events (mobile device telemetry) navigating to domains registered within 30 days — particularly domains containing postal service or banking brand names
- New 2FA device enrollment from previously unseen IP/device within 10 minutes of any authentication event
- High-value outbound mobile money transfer to a new beneficiary within 60 minutes of new 2FA device enrollment

### Cross-Team Correlation

- **Cyber + Fraud**: Correlate web proxy logs showing navigation to fake bank login domains with downstream transaction monitoring alerts for mobile money drain events
- **Fraud + Customer Service**: Cross-reference accounts where 2FA device was recently changed with inbound customer complaints about marketplace fraud — victims often call after discovering they cannot log in
- **Fraud + AML**: Mobile money drain events should be evaluated for money mule account patterns on the receiving end; SAR filing recommended where mule account indicators are present

---

## Operational Evidence

### EV-TP0051-2026-001: European QR Code Marketplace Fraud — USD 110,000 Loss

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 (European region chapter — "New QR Code Scam Targeting Online Sellers in Europe")
- **Region**: Europe (specific member country not named)
- **Modus Operandi**: Fraudster impersonates marketplace buyer → migrates victim to messaging app using local phone number → sends fake QR code claiming post office payment → victim scans to fraudulent post office site → "Receive Money" → bank selection → fake bank login → credential capture → 2FA device enrollment → mobile money drain
- **Loss**: USD 110,000 (single documented case)
- **CFPF Phase Coverage**: P1 through P5
- **Confidence**: High (directly cited in INTERPOL member country report)
- **Summary**: A European member country reported this modus operandi to INTERPOL as a new and previously undocumented variant of quishing fraud targeting online marketplace sellers. The attack's effectiveness stems from the combination of social credibility (buyer role), physical plausibility (post office payment pretext), and the QR code's inability to display destination URL before scanning. The 2FA device enrollment step converts a credential phishing event into persistent, victim-locked account takeover. INTERPOL notes this technique exploits the same impersonation and identity fraud convergence observed across European member countries.

---

## References

- INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 — European region chapter, "New QR Code Scam Targeting Online Sellers in Europe" (p. European section); "The Convergence of Impersonation and Identity Fraud" (European region); "Impersonation Fraud" typology section
- INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 — Key Findings: "quishing" cited as a rising form of impersonation fraud exploiting trust in QR technology
- FLAME TP-0037: Digital Wallet / NFC Payment Fraud — mobile payment vector overlap
- FLAME TP-0050: Calendar/Invite Injection Phishing — comparable off-platform lure delivery mechanic
- FLAME TP-0012: Tech Support Scam / ATO Chain — downstream account takeover pattern

---

## Analyst Notes

**QR Code UX as the Core Vulnerability**: The defining characteristic of quishing versus traditional phishing is the absence of URL preview before victim commitment. When a victim receives a phishing link via email or SMS, modern clients surface the destination URL on hover or long-press, offering a moment of inspection. QR codes provide no equivalent — the victim commits to navigation at scan time, with no pre-scan URL visibility. This makes quishing particularly effective against security-aware users who have learned to scrutinize links but have not extended that scrutiny to QR codes.

**Localization as an Amplifier**: The European case documented by INTERPOL depends heavily on localization — the post office impersonation site, the bank login clones, and the local phone numbers used by the fraudster are all market-specific. This means the attack scales by region rather than globally; each new regional deployment requires localized infrastructure. Detection strategies should therefore focus on newly-registered domains impersonating local postal and banking institutions, rather than relying on global threat feed matching.

**The 2FA Enrollment Step**: Unlike simple credential phishing, this attack chain includes an active account takeover step (new 2FA device enrollment) that must be executed in near-real time while the victim is still unaware. This time pressure introduces a detection window: institutions that alert customers out-of-band on 2FA device changes can interrupt the attack before fund transfer. Institutions without this control have no reliable second-chance detection point before the drain occurs.

**TP-0037 Cross-Reference**: TP-0037 (Digital Wallet / NFC Payment Fraud) covers the mobile payment rails abused in the monetization phase. The mobile money drain technique in this TP is consistent with TP-0037's monetization phase analysis and should be reviewed in conjunction.

**BSA/SAR Considerations**: Quishing-related losses should be reported under BSA categories Identity theft (Z) and Wire fraud (Q). Recommended SAR keywords: "QR code fraud," "quishing," "fake post office," "fake bank login," "2FA device hijacking," "mobile money drain," "marketplace seller fraud."

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-17 | FLAME Project | Initial submission |
