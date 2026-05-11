# TP-0088: Logistics Sector Spearphishing — Carrier Impersonation and Freight Document Fraud

```yaml
---
id: TP-0088
title: "Logistics Sector Spearphishing — Carrier Impersonation and Freight Document Fraud"
category: ThreatPath
date: 2026-05-10
author: "FLAME Project (sourced from Recorded Future Insikt Group, CTA-2026-0319)"
source: "Recorded Future Insikt Group, 2025 Year in Review: Malicious Infrastructure (CTA-2026-0319), March 2026"
tlp: WHITE
sector:
  - logistics
  - transportation
  - cross-sector
fraud_types:
  - phishing
  - brand-impersonation
  - social-engineering
  - credential-harvesting
  - fraud-enabling-infrastructure
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "social-engineering"
primary_phase: "P2"
short_name: "Logistics Spearphish"
confidence_score: 80
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1583.001  # Acquire Infrastructure: Domains
  - T1584.001  # Compromise Infrastructure: Domains
  - T1566.002  # Spearphishing Link
  - T1204.001  # User Execution: Malicious Link
  - T1059.001  # PowerShell
ft3_tactics:
  - "FTA001"
  - "FTA005"
  - "FTA009"
  - "FTA010"
  - "FT007"
mitre_f3:
  - "T1189"
  - "T1555"
  - "T1598"
  - "T1660"
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "Execution"
  - "Credential Access"
  - "Perform Fraud"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
related_tps:
  - id: TP-0002
    relationship: variant-of
  - id: TP-0020
    relationship: related-to
  - id: TP-0042
    relationship: shares-infrastructure
  - id: TP-0054
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-AML
  - REG-DORA
  - REG-RF-CTA-2026-0319
baseline_ids: []
nation_state_nexus: none
geopolitical_timing: none
tags:
  - tag-160
  - logistics-fraud
  - carrier-impersonation
  - clickfix
  - castleloader
  - graybravo
  - freight-fraud
  - spearphishing
  - domain-reregistration
  - england-logistics
  - recorded-future
---
```

## Summary

TAG-160 is a financially motivated threat cluster active since at least March 2025 that specifically targets the logistics and freight sector. The actor impersonates legitimate carriers (notably England Logistics) using a combination of spoofed legitimate email addresses and typosquatted domains. Victims receive fraudulent freight rate confirmations and are directed to information-harvesting landing pages, followed by ClickFix-style instructions (e.g., DocuSign-themed) that trick users into executing malicious PowerShell commands.

A distinctive feature is TAG-160's pre-operational research: the actor deliberately re-registers expired domains previously owned by legitimate logistics companies (e.g., cdlfreightlogistics.com in August 2025, hometownlogisticsllc.com in June 2025), inheriting domain reputation and brand recognition. TAG-160 also abuses access to legitimate freight-matching platforms including DAT Freight & Analytics and Loadlink Technologies.

The attack chain delivers CastleLoader (by GrayBravo/TAG-150) and additional payloads. TAG-160's infrastructure overlaps with AS211659 (STIMUL-AS) and AS216341 (OPTIMA-AS), both linked to the TAE BEARHOST ecosystem. The use of premium malware tooling (including Matanbuchus at $15,000/month) indicates a well-resourced operation.

## Threat Path Hypothesis

> **Hypothesis**: TAG-160 exploits the high-trust, time-sensitive nature of logistics operations — where brokers and carriers routinely exchange rate confirmations and freight documents under tight deadlines — to deliver credential-harvesting and malware payloads. The actor's pre-operational investment in re-registering expired legitimate logistics domains and spoofing known carrier brands creates a high-confidence initial access vector that bypasses standard email filtering. The ClickFix delivery mechanism exploits user trust in DocuSign-style document workflows common in the freight industry.

**Confidence**: High (80) — Recorded Future Insikt Group primary research (A reliability) with confirmed infrastructure overlaps and documented attack chain.

**Estimated Impact**: $10,000 to $500,000+ per victim organization. Freight billing manipulation, payment diversion on high-value loads, and credential theft from logistics platforms can generate significant losses. Credential access to freight-matching platforms enables downstream fraud across the supply chain.

## CFPF Phase Mapping

### Phase 1: Recon (P1)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Carrier/broker identification | TAG-160 identifies target logistics companies, brokers, and freight carriers operating on major freight platforms | Reconnaissance activity on DAT Freight & Analytics, Loadlink Technologies, and other freight-matching platforms |
| Expired domain research | Actor monitors domain expiration lists for previously legitimate logistics company domains with residual reputation | WHOIS monitoring for expired logistics-branded domains; domain drop-catching activity |
| Employee email harvesting | Gather employee contact information from freight platform profiles, company websites, and public directories | Email enumeration against logistics companies; scraping of freight platform member directories |
| Freight workflow analysis | Research standard freight documentation workflows — rate confirmations, bills of lading, DocuSign processes — to craft convincing lures | Access to freight industry documentation templates and communication patterns |

**Data Sources**: Domain expiration feeds, freight platform access logs, OSINT on logistics industry communications

---

### Phase 2: Initial Access (P2)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Spoofed carrier emails | Send emails from spoofed addresses (e.g., no-reply@englandlogistics.com) with freight rate confirmation and quote lures | SPF/DKIM failures on emails purporting to originate from legitimate carrier domains; freight-themed subject lines |
| Typosquatted domain emails | Send emails from typosquatted versions of legitimate logistics company domains | Newly registered domains with character substitutions or additions mimicking known carriers |
| Expired domain re-registration | Re-register expired domains previously owned by legitimate logistics companies (cdlfreightlogistics.com, hometownlogisticsllc.com) to inherit brand trust | Domain re-registration of previously legitimate logistics domains; change in registrant details on known logistics domains |
| Freight platform abuse | Leverage access to legitimate freight-matching platforms (DAT, Loadlink) to distribute phishing links through trusted channels | Suspicious link sharing or message activity on freight-matching platforms from newly created or compromised accounts |

**Data Sources**: Email gateway logs, DMARC/DKIM/SPF authentication results, domain registration feeds, freight platform activity logs

---

### Phase 3: Positioning (P3)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Information-harvesting landing pages | Victim clicks link in freight document lure, directed to credential-harvesting page mimicking logistics or document-signing portals | Landing pages on re-registered or typosquatted logistics domains collecting credentials; URL patterns matching freight document themes |
| ClickFix delivery (DocuSign-themed) | Landing page presents DocuSign-themed ClickFix instructions prompting victim to press Win+R, Ctrl+V, Enter to execute a pre-staged PowerShell command | Pages with ClickFix UI elements (fake CAPTCHA, document verification prompts); clipboard manipulation JavaScript; mshta.exe or PowerShell execution from user-initiated Run dialog |
| Infrastructure staging on BEARHOST | C2 infrastructure hosted on AS211659 (STIMUL-AS) and AS216341 (OPTIMA-AS) within the TAE BEARHOST ecosystem | Network connections to known BEARHOST ASNs; DNS resolution to STIMUL-AS or OPTIMA-AS IP ranges |

**Data Sources**: Web content analysis, endpoint telemetry (clipboard access, Win+R invocation), network traffic to BEARHOST ASNs

---

### Phase 4: Execution (P4)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| PowerShell payload execution | ClickFix-delivered PowerShell command downloads and executes CastleLoader first-stage payload | PowerShell process spawned from explorer.exe or mshta.exe following user execution; encoded PowerShell commands fetching remote payloads |
| CastleLoader deployment | CastleLoader (GrayBravo/TAG-150 tooling) establishes persistence and C2 communication | CastleLoader behavioral indicators; C2 beaconing to known CastleLoader infrastructure; scheduled task or registry persistence |
| Additional payload delivery | CastleLoader delivers secondary payloads including RATs and infostealers | Post-exploitation tool deployment; credential dumping activity; lateral movement within logistics networks |
| Credential harvesting from logistics platforms | Infostealers and RATs harvest saved credentials for freight platforms (DAT, Loadlink), email accounts, and financial systems | Credential access to browser password stores; access to freight platform session tokens; exfiltration of saved credentials |

**Data Sources**: Endpoint detection (PowerShell logging, process creation), network C2 detection, credential access monitoring

---

### Phase 5: Monetization (P5)

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Payment diversion | Redirect freight payments by modifying banking details in carrier/broker communications | Changes to payment instructions in freight transactions; new banking details substituted in invoices or rate confirmations |
| Freight billing manipulation | Use compromised freight platform credentials to create fraudulent loads, modify billing, or divert shipments | Anomalous load creation or billing modifications on freight platforms from compromised accounts; loads booked to unfamiliar carriers |
| Identity theft | Harvested PII and credentials sold or used for downstream identity fraud | Credential listings on dark web markets referencing logistics sector; new account creation using stolen logistics employee identities |
| Credential sale | Compromised freight platform and corporate credentials sold to other threat actors | Bulk credential offerings for DAT, Loadlink, or logistics company VPN/email accounts on underground forums |

**Data Sources**: Financial transaction monitoring, freight platform anomaly detection, dark web monitoring, credential leak databases

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Domain expiration monitoring for company-owned and industry-adjacent logistics domains | Detective | Cyber Threat Intel |
| P1 | Freight platform account monitoring for suspicious profile creation or access patterns | Detective | Platform Security |
| P2 | DMARC/DKIM/SPF enforcement for all logistics company domains, including expired domains | Preventive | Email Security |
| P2 | Domain monitoring for typosquats and re-registrations of known logistics brands | Detective | Brand Protection |
| P3 | ClickFix execution pattern detection: mshta.exe or PowerShell spawned from explorer.exe after Win+R | Detective | Endpoint Security |
| P3 | Web proxy blocking of newly registered or re-registered logistics-themed domains (< 30 day NRD policy) | Preventive | Network Security |
| P4 | PowerShell script block logging and constrained language mode enforcement | Detective / Preventive | Endpoint Security |
| P4 | Network detection for CastleLoader C2 communication patterns and BEARHOST ASN traffic | Detective | Network Security |
| P4 | Multi-factor authentication on all freight platform accounts (DAT, Loadlink, etc.) | Preventive | Identity Security |
| P5 | Payment instruction change verification via out-of-band confirmation for freight transactions | Preventive | Finance / Freight Operations |
| P5 | Network segmentation isolating logistics platform access from general corporate network | Preventive | Network Security |

---

## Detection Approaches

### Email-Level Detection

- **DMARC/DKIM/SPF authentication monitoring**: Flag emails claiming to originate from known logistics carriers (englandlogistics.com, etc.) that fail authentication checks
- **Freight document lure detection**: Alert on emails with freight-themed subject lines (rate confirmation, freight quote, load tender) containing links to newly registered or re-registered domains
- **Typosquat detection**: Monitor for inbound emails from domains visually similar to known logistics carriers and brokers

### Endpoint-Level Detection

- **ClickFix execution chain**: Detect the ClickFix pattern — user opens Run dialog (Win+R), pastes clipboard content, executes PowerShell or mshta command. Key telemetry: `explorer.exe` → `cmd.exe`/`powershell.exe` with encoded or obfuscated arguments
- **CastleLoader indicators**: Monitor for CastleLoader behavioral signatures including scheduled task persistence, specific C2 beacon patterns, and known mutex values
- **Credential store access**: Alert on unexpected access to browser credential stores and freight platform session data by non-browser processes

### Infrastructure-Level Detection

- **Domain re-registration monitoring**: Alert on re-registration of previously legitimate logistics company domains, especially when registrant details change
- **BEARHOST ASN monitoring**: Flag network connections to AS211659 (STIMUL-AS) and AS216341 (OPTIMA-AS) associated with the TAE BEARHOST ecosystem
- **Matanbuchus infrastructure**: Monitor for network indicators associated with Matanbuchus loader infrastructure (known C2 patterns, URI structures)

---

## References

- Recorded Future Insikt Group, 2025 Year in Review: Malicious Infrastructure (CTA-2026-0319), March 2026 — TAG-160 analysis, pp. 43-47
- BEARHOST TAE (Threat Actor Ecosystem) assessment — AS211659 (STIMUL-AS) and AS216341 (OPTIMA-AS) infrastructure mapping
- GrayBravo/TAG-150 CastleLoader technical analysis
- Matanbuchus loader infrastructure reporting

---

## Analyst Notes

- TAG-160's deliberate re-registration of expired legitimate logistics domains is a sophisticated pre-operational technique that merits dedicated monitoring. Organizations in the logistics sector should maintain watchlists of their own expired domains and those of known industry partners, with alerts on re-registration events.
- The ClickFix delivery mechanism (DocuSign-themed user execution) bypasses traditional email attachment scanning because no malicious file is delivered — the user manually executes the payload. Detection must focus on the execution chain (Win+R → PowerShell) rather than traditional payload analysis.
- The overlap between TAG-160 and the BEARHOST ecosystem (STIMUL-AS, OPTIMA-AS) provides infrastructure-level detection opportunities. Organizations can proactively block or monitor traffic to these ASNs.
- Matanbuchus at $15,000/month licensing cost indicates TAG-160 is well-resourced and likely generating significant revenue from freight fraud operations to justify this expenditure.
- Cross-reference with TP-0002 (BEC Vendor Impersonation) for the broader vendor/carrier impersonation pattern, TP-0020 (Supply Chain Payment Fraud) for payment diversion tactics, TP-0042 (TDS Chain Exploitation) for shared infrastructure patterns, and TP-0054 (Fraud-as-a-Service Platforms) for the commercial malware tooling ecosystem.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-05-10 | FLAME Project | Initial submission from Recorded Future Insikt Group CTA-2026-0319 research (TAG-160, pp. 43-47) |
