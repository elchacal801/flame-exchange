# TP-0050: Calendar/Invite Injection Phishing

```yaml
---
id: TP-0050
title: "Calendar/Invite Injection Phishing"
category: ThreatPath
date: 2026-03-10
author: "FLAME Project"
source: "Malwarebytes Labs / Google Workspace security advisories"
tlp: WHITE
infrastructure_generation_method: rdga-registered
fraud_types:
  - calendar-phishing
  - social-engineering
sector:
  - banking
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 78
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1566.003  # Phishing: Spearphishing via Service
  - T1566.002  # Phishing: Spearphishing Link
  - T1204.001  # User Execution: Malicious Link
  - T1036.005  # Masquerading: Match Legitimate Name/Location
  - T1583.001  # Acquire Infrastructure: Domains
ft3_tactics: ["FTA001", "FTA009", "FTA010", "FT016"]
mitre_f3: ["F1020", "F1031", "F1032", "F1040", "T1598", "T1660"]
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
  improve: "Level 3"
related_tps:
  - id: TP-0012
    relationship: enhances
  - id: TP-0041
    relationship: shares-infrastructure
regulatory_refs:
  - REG-CFPB-REGE
  - REG-UK-PSR-APP
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - calendar-phishing
  - invite-injection
  - ics-abuse
  - google-calendar
  - outlook-calendar
  - fake-renewal-scam
  - antivirus-scam
  - rdga-sender-domains
  - calendar-spam
---
```

## Summary

Phishing campaigns that abuse calendar invite protocols (Google Calendar, Outlook/Exchange) to bypass email gateway filtering. Attackers send emails containing .ics calendar invitations that auto-populate on victim calendars, creating persistent lure events that outlive the original email. These campaigns are commonly paired with RDGA sender infrastructure (TP-0041) and tech support / fake AV renewal lures (TP-0012). An observed March 2026 campaign delivered 6,000+ emails across 10 sender domains, with 9 of 10 domains generated via RDGA techniques on high-abuse TLDs.

## Threat Path Hypothesis

> **Hypothesis**: Actors are exploiting calendar invite auto-accept behavior in Google Calendar and Outlook/Exchange to inject persistent phishing lures directly onto victim calendars, bypassing email security gateways that focus on message body and attachment analysis. The calendar events survive email deletion and serve as delayed-action social engineering triggers (fake renewal notices, meeting invites) that redirect victims to phishing pages or tech support scam call centers.

**Confidence**: Medium-High — multiple campaigns observed in 2025-2026 with consistent TTPs. Google acknowledged the auto-accept vector in Workspace security updates.

**Estimated Impact**: $200 – $5,000 per victim (renewal scam variant); higher if combined with tech support ATO chain (TP-0012). Campaign-level impact scales with volume (6,000+ emails per wave observed).

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Target list acquisition | Harvest email addresses from data brokers, breach data, or scraped directories; filter for accounts likely using Google Workspace or Outlook | Bulk email acquisition targeting corporate/consumer Google and Microsoft accounts |
| RDGA domain registration | Register sender domains via RDGA on high-abuse TLDs (.cyou, .sbs, .click) in bulk (10+ domains per campaign wave); configure MX records for outbound email delivery | Burst domain registration on high-abuse TLDs within 24-48h window; high consonant-to-vowel ratio (>0.75) in domain labels |
| Lure template preparation | Prepare calendar event templates impersonating antivirus renewal notices (McAfee, Bitdefender, Norton), meeting invites (Zoom, Google Meet), or deal/offer notifications | Branded lure content matching known scam templates; .ics file generation tooling |

**Data Sources**: Zone file diffs (TLD registries), passive DNS, domain WHOIS, email threat intelligence feeds

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Calendar invite email delivery | Send phishing emails containing .ics calendar attachments or Google Calendar invite links from RDGA sender domains; email triggers auto-accept in victim's calendar application | Inbound email with .ics attachment or calendar invite header from newly-registered domain; sender domain on high-abuse TLD |
| Calendar auto-population | Google Calendar auto-accept or Outlook .ics processing creates calendar event on victim's device without explicit user consent; event persists even if email is deleted or filtered | New calendar event appearing from unknown organizer; event created within minutes of email receipt; no prior relationship with sender |
| Email gateway bypass | Calendar invite format (.ics / Google Calendar protocol) is treated differently by many email security gateways, which focus on body text, URLs, and traditional attachment types | .ics attachments passing through email security without sandbox analysis; calendar invite metadata not inspected by DLP rules |

**Target**: Consumer

**Data Sources**: Email gateway logs, Google Workspace admin audit logs, Exchange message tracking, calendar event creation logs

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Persistent calendar lure | Calendar event remains on victim's calendar for days/weeks with reminder notifications, creating repeated exposure to the phishing lure even after the original email is deleted | Calendar events from unknown external organizers with reminder alerts enabled; events containing phone numbers or URLs in description |
| Brand impersonation in event | Calendar event title and description impersonate legitimate brands (McAfee, Norton, Google, Zoom) with renewal amounts, subscription IDs, and urgency language | Calendar event descriptions containing dollar amounts, "subscription renewal," toll-free phone numbers, or shortened URLs |
| Reminder-based re-engagement | Calendar reminder notifications (15 min, 1 hour, 1 day before) re-surface the lure content to the victim at scheduled times, increasing probability of engagement | Multiple reminder triggers for a single injected calendar event |

**Data Sources**: Calendar event metadata, calendar sync logs, push notification logs

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Phishing link click | Victim clicks URL in calendar event description, redirecting to credential harvesting page or fake renewal portal that captures payment card details | Navigation to newly-registered domain from calendar app; credential submission to non-legitimate domain |
| Tech support call | Victim calls toll-free number in calendar event description, reaching a scam call center that impersonates antivirus or tech support; call center operators execute TP-0012 playbook | Outbound call to phone number associated with known tech support scam campaigns; call duration consistent with social engineering engagement (15-60 min) |
| Payment card capture | Fake renewal portal captures victim's credit/debit card details under guise of "renewing" antivirus subscription or "confirming" meeting registration | Card-not-present transaction to merchant associated with scam infrastructure; small initial charge followed by larger unauthorized charges |

**Data Sources**: Web proxy logs, DNS query logs, telephony CDRs, transaction monitoring systems

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-002: Card-not-present fraud | Stolen payment card details used for unauthorized purchases or resold on carding forums | CNP transactions using cards previously submitted to fake renewal portals |
| CFPF-P5-001: Authorized push payment | If victim is routed through tech support scam variant (TP-0012), victim may be coached into wire transfer or Zelle payment to "refund" account | Wire/Zelle transfer to new beneficiary following tech support call |
| Credential resale | Harvested credentials (email, banking) sold on underground markets or used for downstream account takeover | Credential stuffing attempts using email/password pairs captured via calendar phishing landing pages |

**Data Sources**: Transaction monitoring, fraud reporting systems, dark web monitoring, credential leak detection

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001: Social Engineering
- FTA009: Phishing
- FTA010: Infrastructure Acquisition
- FT016: Brand Impersonation

**MITRE ATT&CK:**

- T1566.003: Phishing: Spearphishing via Service — calendar invite delivery mechanism
- T1566.002: Phishing: Spearphishing Link — malicious URLs in calendar event descriptions
- T1204.001: User Execution: Malicious Link — victim clicking calendar event URL
- T1036.005: Masquerading: Match Legitimate Name/Location — brand impersonation in event metadata
- T1583.001: Acquire Infrastructure: Domains — RDGA-based sender domain registration

**Group-IB Fraud Matrix:**

- Reconnaissance → Resource Development → Initial Access → End-user Interaction → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P2/P3** — typically discovered when email security teams notice .ics-based phishing bypassing gateways, or when victims report suspicious calendar events they don't remember creating.

**Look Left** (what did you miss before discovery?):

- RDGA domain registration bursts on high-abuse TLDs 24-48h before campaign launch (correlate with TP-0041 detection logic)
- MX record configuration on newly-registered domains indicating outbound email capability
- Email gateway logs showing .ics attachments from low-reputation sender domains that were not blocked

**Look Right** (what comes next after discovery?):

- Calendar events persist on victim devices even after email deletion — remediation requires calendar-level cleanup
- Victims who engaged with lures may have entered credentials or payment details on phishing pages
- Same RDGA infrastructure likely supporting parallel campaigns (different lure themes, same sender domains)
- Tech support scam call centers receiving inbound calls from calendar phishing victims (TP-0012 downstream)

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor zone file diffs for RDGA domain registration bursts on high-abuse TLDs; feed to email gateway blocklists | Detective | Cyber |
| P2 | Disable Google Calendar auto-accept for external invitations at the organization level (Google Workspace Admin Console) | Preventive | IT |
| P2 | Configure email gateway to inspect and sandbox .ics attachments; block .ics from newly-registered domains (<30 days) | Preventive | Cyber |
| P2 | Outlook: disable automatic processing of meeting requests from external senders | Preventive | IT |
| P3 | User awareness training: recognize suspicious calendar events from unknown organizers | Preventive | Fraud |
| P4 | Web proxy: block navigation to domains on high-abuse TLDs that are <7 days old | Preventive | Cyber |
| P4 | Transaction monitoring: flag card-not-present transactions to merchants associated with fake renewal infrastructure | Detective | Fraud |
| P5 | Rapid card reissuance for customers who report calendar phishing engagement | Responsive | Fraud |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Recognize calendar phishing as distinct vector in fraud taxonomy |
| ASSESS | Level 3 (Established) | Risk assessment includes email-adjacent vectors (calendar, chat) |
| PLAN | Level 2 (Developing) | Playbook for calendar-based phishing incidents |
| ACT | Level 3 (Established) | Calendar event monitoring integrated with email security stack |
| MONITOR | Level 3 (Established) | KRIs for .ics-based delivery attempts and calendar injection rates |
| REPORT | Level 2 (Developing) | Calendar phishing included in SAR narratives with correct BSA categories |
| IMPROVE | Level 3 (Established) | Feedback from calendar phishing incidents drives email gateway tuning |

---

## Detection Approaches

### Queries / Rules

**Email Gateway — .ics from Newly-Registered Domains (Splunk SPL)**

```spl
index=email sourcetype=email_gateway
| where attachment_type="text/calendar" OR attachment_extension=".ics"
| lookup domain_age_feed sender_domain OUTPUT domain_age_days
| where domain_age_days < 30
| stats count by sender_domain, recipient, subject, domain_age_days
| where count > 5
| sort -count
```

**Calendar Event Injection Detection (SQL)**

```sql
SELECT ce.event_id, ce.organizer_email, ce.title, ce.created_at,
       d.domain_name, d.registration_date, d.tld
FROM calendar_events ce
JOIN domain_intel d ON ce.organizer_domain = d.domain_name
WHERE ce.organizer_is_external = TRUE
AND ce.auto_accepted = TRUE
AND d.registration_date > CURRENT_DATE - INTERVAL '30 days'
AND d.tld IN ('.cyou', '.sbs', '.click', '.biz', '.top', '.xyz')
ORDER BY ce.created_at DESC;
```

**RDGA Sender Domain Consonant Ratio Detection (SQL)**

```sql
SELECT domain_label,
       LENGTH(REGEXP_REPLACE(domain_label, '[aeiou]', '', 'gi'))::FLOAT /
       NULLIF(LENGTH(domain_label), 0) AS consonant_ratio,
       tld, registration_date
FROM zone_file_domains
WHERE registration_date > CURRENT_DATE - INTERVAL '7 days'
AND tld IN ('.cyou', '.sbs', '.click')
AND LENGTH(REGEXP_REPLACE(domain_label, '[aeiou]', '', 'gi'))::FLOAT /
    NULLIF(LENGTH(domain_label), 0) > 0.75
ORDER BY registration_date DESC;
```

### Behavioral Analytics

- Calendar events created from external organizers on newly-registered domains with no prior communication history
- Spike in calendar events containing toll-free phone numbers or shortened URLs across multiple recipients
- Users navigating to high-abuse TLD domains within 24h of calendar event creation
- Outbound calls to phone numbers embedded in calendar event descriptions

### Cross-Team Correlation

- **Cyber + Fraud**: Correlate email gateway .ics delivery logs with downstream card-not-present fraud reports from customers who received calendar invitations
- **Cyber + IT**: Cross-reference Google Workspace / Exchange admin logs for external calendar injection with email security bypass events
- **Fraud + AML**: Connect tech support scam reports (TP-0012) with calendar phishing delivery as initial access vector; include in SAR narrative

---

## Operational Evidence

### EV-TP0050-2026-001: March 2026 Calendar Phishing Campaign — RDGA Infrastructure

- **Source**: Email security telemetry, March 2026
- **Cluster**: 10 sender domains, 9 RDGA-generated
- **Domain Count**: 10 domains (bsvohkitq.cyou, btdsjidb.cyou, ecnbusne.sbs, jphecm.biz, lzawqyhpcn.sbs, okbitd.org, rthhmjsmk.org, usebindbeee.click, xkrqfnzk.click + 1 compromised .sch.id domain)
- **Key Indicators**: RDGA-generated labels on .cyou/.sbs/.click TLDs, high consonant-to-vowel ratios, MX records for outbound delivery, bulk registration within 48h, .ics calendar attachments
- **CFPF Phase Coverage**: P1, P2
- **Confidence**: High
- **Summary**: A campaign delivering 6,000+ phishing emails used calendar invite injection to bypass email security gateways. Nine of ten sender domains were RDGA-generated on high-abuse TLDs (.cyou, .sbs, .click), with one compromised Indonesian educational domain (.sch.id) providing reputation cover. The majority of emails were blocked by email security services, but remaining messages successfully injected calendar events onto victim devices via Google Calendar auto-accept and Outlook .ics processing. Lure themes included antivirus subscription renewals (McAfee, Bitdefender, Norton) and meeting invites. The RDGA infrastructure pattern is consistent with TP-0041 techniques.

---

## References

- Malwarebytes Labs: Calendar phishing campaign analysis (February 2026) — documented Google Calendar and Zoom meeting invite abuse
- Google Workspace Security: Advisory on external calendar invite auto-accept settings
- Infoblox: RDGA domain analysis and zone file monitoring methodology (ref: TP-0041 sources)
- FBI IC3: Tech support scam PSAs — downstream impact when calendar phishing routes to call centers

---

## Analyst Notes

**Vector Persistence**: The key differentiator of calendar phishing from traditional email phishing is persistence. When an email is deleted or filtered, the phishing lure is gone. Calendar events injected via .ics auto-accept survive email deletion and continue to surface via reminder notifications. This creates a delayed-action social engineering vector where the victim may encounter the lure days or weeks after the initial delivery, long after any email security alert has been dismissed.

**RDGA Infrastructure Overlap**: The March 2026 campaign demonstrates tight operational coupling between calendar phishing delivery (TP-0050) and RDGA infrastructure (TP-0041). The consonant-heavy domain labels (bsvohkitq, btdsjidb, ecnbusne) and high-abuse TLD selection are consistent with RDGA actor patterns documented in TP-0041. Detection rules for RDGA domain registration bursts (TP-0041 DL rules) provide early warning for calendar phishing campaigns.

**BSA/SAR Considerations**: Calendar phishing campaigns leading to financial loss should be reported under BSA categories Wire fraud (Q) or Identity theft (Z). Recommended SAR keywords include: "calendar phishing," "invite injection," "fake renewal scam," "antivirus scam," "calendar spam."

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-10 | FLAME Project | Initial submission |
