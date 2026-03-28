# TP-0002: Business Email Compromise — Vendor Impersonation Wire Fraud

```yaml
---
id: TP-0002
title: "Business Email Compromise — Vendor Impersonation Wire Fraud"
category: ThreatPath
date: 2026-02-12
author: "FLAME Project"
source: "FBI IC3 / FinCEN Advisory FIN-2019-A005 / multiple public reporting"
tlp: WHITE
sector:
  - banking
  - cross-sector
fraud_types:
  - BEC
  - wire-fraud
  - invoice-fraud
  - payment-diversion
cfpf_phases: [P1, P2, P3, P4, P5]
mitre_attack: [T1566.001, T1534, T1114.003, T1657]
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT052.003", "FT026.001", "FT028", "FT031", "FT012", "FT027", "FT039", "FT042.001", "FT043", "FT053.001"]                  # Stripe FT3 (when mapped)
mitre_f3: []                     # MITRE F3 (placeholder)
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "Account Access"
  - "Perform Fraud"
  - "Monetization"
  - "Laundering"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
confidence_score: 88
source_reliability: B
info_credibility: 1
related_tps:
  - id: TP-0007
    relationship: enhances
  - id: TP-0011
    relationship: provides-mules-for
  - id: TP-0020
    relationship: related-to
regulatory_refs:
  - REG-FATF-R16
  - REG-FBI-IC3
  - REG-OCC-FRAUD
  - REG-UNODC-ORGANIZED-FRAUD-2024
baseline_ids:
  - BL-0012
tags:
  - vendor-impersonation
  - accounts-payable
  - email-compromise
  - high-value
  - unodc
  - unodc-organized-fraud-2024
---
```

## Summary

Threat actors compromise or spoof vendor email accounts, then impersonate the vendor to redirect legitimate invoice payments to actor-controlled accounts. BEC caused $2.9B+ in reported losses in 2023 per FBI IC3. The scheme exploits trust relationships between businesses and their vendors, often going undetected until the legitimate vendor inquires about unpaid invoices weeks or months later.

## Threat Path Hypothesis

> **Hypothesis**: Actors are compromising vendor email infrastructure or registering lookalike domains to intercept ongoing business relationships and redirect invoice payments via modified banking details, targeting accounts payable departments across all sectors.

**Confidence**: High — most-reported financial cybercrime category globally.
**Estimated Impact**: $50,000 – $5,000,000+ per incident. Median BEC loss ~$125,000.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-005: Social media recon | Identify target company's vendors, AP staff, and payment workflows via LinkedIn, corporate websites, SEC filings, press releases | Unusual profile views on AP staff LinkedIn accounts |
| CFPF-P1-003: Lookalike domain registration | Register domains resembling vendor (e.g., `vendorname-invoices.com`, `vendornarne.com`) | Domain monitoring alerts; CT log entries |
| CFPF-P1-008: Target list compilation | Build target lists of companies with known vendor relationships from public contract data, supplier directories | N/A (pre-attack) |

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-004: Email phishing | Phish vendor employees to gain access to vendor's email system, or phish target company's AP staff directly | Credential harvesting URLs in emails to vendor employees |
| CFPF-P2-007: Business email compromise | Gain access to vendor's actual email account, or establish convincing spoofed email infrastructure | Email forwarding rules created in vendor mailbox; authentication from unusual locations |

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-007: Email forwarding rule | Create inbox rules in compromised vendor account to monitor invoice-related correspondence and suppress replies from legitimate vendor staff | New forwarding rules to external addresses; rules filtering keywords like "payment", "invoice", "wire" |
| CFPF-P3-008: Data exfiltration | Harvest invoice templates, payment schedules, contract terms, and AP contact details from compromised email to craft convincing impersonation | Unusual mailbox search activity; bulk email export |

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-004: Fraudulent invoice submission | Send modified invoice with updated banking details from compromised or spoofed vendor email. Often timed to coincide with legitimate payment cycles. | Banking detail changes on invoices; invoices from slightly different email addresses; urgency language ("updated bank details effective immediately") |

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Domestic wire to mule | Funds wired to domestic mule accounts, often business accounts opened with fraudulent documentation | Recently opened business accounts receiving large inbound wires |
| CFPF-P5-002: International wire | Funds wired to foreign accounts, commonly in West Africa, Southeast Asia, or Eastern Europe | Wire destinations to high-risk jurisdictions with no prior relationship |

## Evasion Techniques

| Technique | Description | Detection Signal |
|-----------|-------------|------------------|
| Strategic HTTP Redirect | Lookalike vendor domain redirects to the real vendor's website; appears legitimate in basic checks, but email from the domain reaches the attacker | FP-0007: `redirects_to_brand=True` in domain_intel |
| Geo-Targeted Content | Domain serves different content based on visitor geography — benign pages for scanners/researchers in certain regions, malicious content for targets | Manual verification required; inconsistent scan results across geolocations |

**Source**: CrowdStrike Counter Adversary Operations — typosquatting evasion research.

---

## Look Left / Look Right

**Discovery Phase**: Typically **P4/P5** — discovered when the legitimate vendor contacts the target about unpaid invoices, sometimes 30-90 days after payment diversion.

**Look Left**: Did the vendor's email account show signs of compromise (unusual login locations, forwarding rules) before the fraudulent invoice? Were there phishing campaigns targeting the vendor's employees in the weeks prior?

**Look Right**: Are there parallel BEC campaigns using the same compromised vendor email against other customers of that vendor? Is the same mule network being used across multiple BEC schemes?

## Controls & Mitigations

| Phase | Control | Type |
|-------|---------|------|
| P2 | Implement DMARC/DKIM/SPF enforcement for vendor email validation | Preventive |
| P3 | Monitor for email forwarding rule creation in M365/Google Workspace | Detective |
| P4 | Mandatory out-of-band verification (phone call to known number) for any banking detail change on invoices | Preventive |
| P4 | AP process: flag invoices where beneficiary bank differs from previous payments to same vendor | Detective |
| P5 | Wire recall procedures within 24-72 hour window | Responsive |

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive sponsorship for email security and wire transfer verification programs; funded BEC awareness training for AP staff |
| ASSESS | Level 3 (Established) | Formal risk assessment of vendor payment workflows including email-based invoice processing; identification of high-risk vendor relationships |
| PLAN | Level 3 (Established) | Documented procedures for out-of-band verification of banking detail changes; incident response playbook for BEC wire fraud with recall timelines |
| ACT | Level 3 (Established) | DMARC/DKIM/SPF enforcement on all corporate domains; AP process controls requiring dual authorization for beneficiary bank changes; email forwarding rule monitoring in M365/Google Workspace |
| MONITOR | Level 3 (Established) | Continuous monitoring of invoice payment routing changes; email forwarding rule alerting; lookalike domain monitoring via CT logs and domain intelligence |
| REPORT | Level 2 (Developing) | SAR filing procedures for BEC incidents; internal escalation from AP to fraud/security team when suspicious invoice changes are detected |
| IMPROVE | Level 3 (Established) | Post-incident review of BEC attempts including root cause analysis of email compromise vector; regular updates to vendor verification procedures based on emerging evasion techniques |

## Detection Approaches

**Splunk — Invoice Banking Detail Change Detection**

```spl
index=ap_system action="payment_update"
| eval prev_bank=coalesce(previous_routing_number, "none")
| where prev_bank != routing_number AND prev_bank != "none"
| table vendor_name, invoice_id, prev_bank, routing_number, modified_by, _time
```

**Email — Forwarding Rule Monitoring (M365)**

```kql
// Microsoft Sentinel KQL: BEC Forwarding Rule Monitoring (DL-0138)
OfficeActivity
| where Operation in ("New-InboxRule", "Set-InboxRule", "Enable-InboxRule", "Set-Mailbox")
| where Parameters has_any ("ForwardTo", "ForwardAsAttachmentTo", "RedirectTo",
                             "DeleteMessage", "MarkAsRead")
| project TimeGenerated, UserId, Operation, Parameters, ClientIP
```

## Operational Evidence

### EV-TP0002-2026-002: UNODC Organized BEC Fraud Typology

- **Source**: UNODC Organized Fraud Issue Paper (Vienna, 2024)
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: UNODC identifies BEC as one of the most prevalent forms of organized fraud globally under Category 7 (Fraud Against Businesses). Documents OCG use of social engineering to infiltrate communication systems and persuade personnel to make unauthorized transfers. Key case studies: (1) US business lost $1M to BEC impersonating a business partner requesting payment to alternative account "for tax reasons" (Nigerian FIU source); (2) CFO phished via fake ICT login page, credentials used to send wire transfer requests and fake invoices — $11M loss. UNODC positions BEC as organized crime, not individual hacking.

### EV-TP0002-2026-003: 2026 Technical Landscape — AiTM as Primary BEC Enabler

- **Source**: Organized fraud detection in 2026: a technical landscape report
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: AiTM phishing has become the primary initial access vector for BEC. Sekoia.io documents 11 major AiTM kits enabling session token hijacking that bypasses MFA, with compromised sessions used to initiate wire fraud. Detection relies on Entra ID authentication log anomalies: User-Agent/Application ID inconsistencies between MFA completion and subsequent access, inbox rule creation post-compromise, sign-in IP pattern correlation, session token replay from unusual geolocations, and MFA method manipulation. FIDO2/phishing-resistant MFA blocks 93.9% of AiTM campaigns — the strongest quantified BEC prevention measure. See TP-0067 for AiTM infrastructure details.

## Analyst Notes

**IC3 2024 Data:** The FBI IC3 2024 Internet Crime Report (covering 2024 incidents, released April 2025) reported $2.8B in BEC losses, making it the second-highest loss category after investment fraud. Total reported internet crime losses reached $16.6B in 2024, up 33% from 2023's $12.5B. BEC remains among the most financially damaging cybercrime categories despite a slight decline from 2023's $2.9B figure, reflecting improved corporate awareness alongside persistent attacker adaptation.

## References

- FBI IC3: \"2024 Internet Crime Report\" (April 2025) — annual loss and complaint statistics. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)
- FinCEN Advisory FIN-2019-A005: \"Advisory on Business Email Compromise.\" [Link](https://www.fincen.gov/sites/default/files/advisory/2019-07-16/FinCEN%20BEC%20Advisory%20508%20FINAL.pdf)
- Abnormal Security: Annual BEC Trends Report. [Link](https://abnormalsecurity.com/resources/state-of-email-security)
- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Chapter II, Business Email Compromise Fraud

## Case Studies & References

- "Organized fraud detection in 2026: a technical landscape report" — BEC and AiTM phishing section

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-12 | FLAME Project | Initial submission |
| 2026-02-28 | FLAME Project | v1.5 enrichment: added Stripe FT3 tactic mappings, IC3 2024 loss figures in Analyst Notes |
