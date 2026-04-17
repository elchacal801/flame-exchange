# TP-0020: Supply Chain Payment Fraud

```yaml
---
id: TP-0020
title: "Supply Chain Payment Fraud"
category: ThreatPath
date: 2026-02-20
author: "FLAME Project"
source: "Internal Knowledge Base"
tlp: WHITE
sector:
  - banking
  - cross-sector
fraud_types:
  - business-email-compromise
  - vendor-impersonation
  - wire-fraud
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
mitre_attack:
  - T1566.001 # Phishing: Spearphishing Attachment
  - T1586     # Compromise Accounts
  - T1562.012 # Impair Defenses: Disable or Modify System Firewall (Inbox Rules)
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT007.009", "FT028", "FT008.002", "FT014", "FT043", "FT003", "FT031", "FT042.001", "FT052.003", "FT011.003"]
mitre_f3: ["F1005.006", "F1022", "F1025.002", "F1016", "F1031", "F1032", "F1037", "F1044", "F1046", "F1047"]
groupib_stages:
  - "Reconnaissance"
  - "Account Access"
  - "Trust Abuse"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 3"
confidence_score: 68
source_reliability: B
info_credibility: 3
related_tps:
  - id: TP-0002
    relationship: related-to
  - id: TP-0018
    relationship: related-to
regulatory_refs:
  - REG-FATF-R16
  - REG-FBI-IC3
  - REG-OCC-FRAUD
baseline_ids:
  - BL-0002
  - BL-0012
tags:
  - supply-chain
  - b2b-payments
  - invoice-fraud
  - vendor-fraud
---
```

---

## Summary

Supply Chain Payment Fraud (a variant of Vendor Impersonation / BEC) involves threat actors compromising the email account of a legitimate vendor or supplier. The actors monitor email traffic to identify upcoming large invoice payments, insert themselves into the communication chain, and provide updated, fraudulent banking instructions to the buyer. When the buyer processes the invoice, the funds are wired to a threat-actor-controlled account instead of the true vendor.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors will gain unauthorized access to a vendor's email system, observe billing cycles, intercept legitimate invoices in transit to a corporate buyer, modify the payment instructions to a mule account, and use inbox rules to hide the buyer's clarifying questions from the real vendor, resulting in the misdirection of B2B wire payments.

**Confidence**: High — This is consistently one of the most financially damaging forms of Business Email Compromise according to the FBI IC3.

**Estimated Impact**: Typically $50k to $5M+ per incident, depending on the size of the targeted supply chain relationship.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-003: Target identification | Actors scrape LinkedIn or corporate websites to map out supply chain relationships, identifying accounting departments at corporate buyers and account managers at vendors. | Lookalike domain registrations targeting specific vendor-buyer relationships. |

**Data Sources**: Brand monitoring, threat intelligence feeds.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Email Account Compromise | The actor compromises the vendor's email account via credential stuffing, phishing, or malware. | Successful logins from anomalous IP geolocations; multiple failed logins followed by success. |

**Data Sources**: Vendor's M365/Google Workspace audit logs (external to the financial institution).

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-002: Establish persistence / Inbox manipulation | The actor sets up email forwarding rules or deletes emails to prevent the true vendor from seeing communications from the targeted buyer. | Creation of new inbox rules involving keywords ("invoice", "wire", "payment", the buyer's domain). |
| CFPF-P3-004: Payment instruction alteration | The actor sends a seemingly legitimate email from the compromised vendor account (or a lookalike domain if access is lost) providing "updated banking details" for an upcoming invoice. | Vendor master data changes in the buyer's ERP system. |

**Data Sources**: M365 Security logs, ERP audit logs.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Unauthorized wire transfer | The buyer updates their vendor master file and initiates the wire transfer or ACH payment to the new, fraudulent account. | Outbound commercial wires to accounts/banks not previously associated with the vendor's historical payment profile. |

**Data Sources**: Treasury management platform logs, corporate banking wire logs.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Wire to domestic mule account | Funds hit the actor-controlled account and are rapidly dispersed to secondary accounts or converted to cryptocurrency. | Large inbound commercial wire followed within 24 hours by multiple sub-$10k outbound wires or crypto purchases. |

**Data Sources**: AML transaction monitoring, wire transfer logs.

---

## Look Left / Look Right Analysis

**Discovery Phase**: Frequently discovered at **Phase 5 (or weeks later)** when the true vendor follows up on the unpaid invoice, at which point the buyer realizes they paid a fraudulent account.

**Look Left**:

- **P4 → P3**: Did the buyer's accounts payable team verify the changing bank account details "out-of-band" (e.g., calling a known phone number rather than replying to the email)?
- **P3 → P2**: If the vendor had enforced MFA or impossible travel rules, the initial email compromise could have been prevented.

**Look Right**:

- Recovery of funds is often impossible if discovery takes weeks. The financial loss often leads to intense legal disputes between the buyer and vendor over who is liable for the breach.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P3 | Mandatory out-of-band verification for all vendor banking detail changes | Preventive | Accounts Payable |
| P3 | Alerting on vendor master data changes in ERP systems | Detective | AP / IT Security |
| P4 | Outbound transaction monitoring comparing beneficiary against historical payees | Detective | Corporate Banking |
| P5 | Inbound transaction monitoring flagging large B2B wires into consumer accounts | Detective | Bank AML/Fraud |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive sponsorship of vendor payment security program; investment in ERP audit integration and out-of-band verification infrastructure for B2B payments |
| ASSESS | Level 3 (Established) | Risk assessment of vendor payment processes across all business units; evaluation of vendor master data change controls and approval workflows; mapping of high-value supply chain relationships most vulnerable to BEC-style interception |
| PLAN | Level 3 (Established) | Detection strategy integrating email security (inbox rule monitoring), ERP vendor master change alerts, and outbound payment anomaly detection; defined vendor banking detail change verification procedures |
| ACT | Level 3 (Established) | Mandatory out-of-band verification for all vendor banking detail changes using historical contact information; automated ERP alerts on vendor master data modifications; outbound wire monitoring comparing beneficiary accounts against historical payee profiles |
| MONITOR | Level 3 (Established) | Continuous monitoring for first-time beneficiary accounts on high-value B2B wire transfers; M365/Google Workspace inbox rule creation surveillance for invoice-related keywords; vendor payment pattern analysis flagging deviations from historical amounts and frequencies |
| REPORT | Level 2 (Developing) | Incident reporting workflows for suspected vendor impersonation; coordination with vendor's security team for email compromise investigation; law enforcement notification for fund recovery within critical time windows |
| IMPROVE | Level 3 (Established) | Post-incident review incorporating vendor communication chain reconstruction; periodic testing of out-of-band verification procedures; updating vendor risk tiers based on email security posture assessments |

## Detection Approaches

### Queries / Rules

**Sigma — Malicious Inbox Rule Creation (Positioning)**

```yaml
title: Supply Chain Fraud - Suspicious Inbox Rule Creation
status: active
description: Detects creation of inbox rules common in Invoice Fraud/BEC to hide communications from the victim.
logsource:
    product: m365
    service: exchange
detection:
    selection:
        operation: 'New-InboxRule'
    keywords:
        - '*invoice*'
        - '*payment*'
        - '*wire*'
        - '*bank*'
        - '*updated detail*'
    actions:
        - '*MoveToFolder*'
        - '*Delete*'
        - '*MarkAsRead*'
    condition: selection and keywords and actions
level: high
tags:
    - attack.t1562.012
    - cfpf.phase3.positioning
```

**SQL — B2B Payment to First-Time Beneficiary**

```sql
SELECT 
    t.transaction_id,
    t.originator_company_name,
    t.amount,
    t.beneficiary_name,
    t.beneficiary_routing_number,
    t.beneficiary_account_number
FROM b2b_wire_transfers t
WHERE t.amount > 50000 
  AND NOT EXISTS (
      -- Has this company ever paid this specific routing/account combo before?
      SELECT 1 FROM b2b_wire_transfers t_hist
      WHERE t_hist.originator_id = t.originator_id
        AND t_hist.beneficiary_routing_number = t.beneficiary_routing_number
        AND t_hist.beneficiary_account_number = t.beneficiary_account_number
        AND t_hist.transaction_date < CURRENT_DATE
  );
```

---

## Analyst Notes

Supply chain payment fraud extends beyond traditional BEC (TP-0002) by targeting the structural trust relationships between organizations and their vendors. Where BEC typically involves email compromise and impersonation at the point of payment, supply chain payment fraud can involve deeper infiltration — compromising vendor portals, manipulating procurement systems, or inserting fraudulent line items into legitimate invoices. The FBI IC3 2024 report's $2.8B BEC loss figure includes a substantial supply chain component, though it is not broken out separately. The attack surface expands with organizational complexity: enterprises with thousands of vendors, decentralized procurement, and multiple ERP systems face exponentially more opportunities for exploitation. Invoice manipulation (changing amounts or adding fraudulent charges to legitimate invoices) is particularly difficult to detect because the vendor relationship and invoice format are authentic — only the payment details are altered. Procurement fraud analytics should focus on detecting anomalies in banking detail changes, invoice amount deviations from historical patterns, and velocity changes in vendor payment requests.

---

## References

- FBI IC3: "2024 Internet Crime Report" (April 2025) — BEC and vendor fraud statistics. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)
- FLAME Project Internal Knowledge Base.
- Deloitte: "Supply Chain Fraud: Managing the Risks" — procurement fraud typologies.
- ACFE: Report to the Nations — vendor billing scheme classification and detection. [Link](https://www.acfe.com/report-to-the-nations/2024/)
- CISA: "Supply Chain Compromise" advisory series — cybersecurity intersection with payment fraud. [Link](https://www.cisa.gov/topics/cyber-threats-and-advisories)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-20 | FLAME Project | Initial creation |
| 2026-02-28 | FLAME Project | v1.5 enrichment: added Stripe FT3 tactic mappings, Analyst Notes, enriched References |
