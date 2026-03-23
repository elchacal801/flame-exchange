# Baseline: Recovery Fraud Victim Contact Norms

```yaml
---
id: BL-0031
title: "Recovery Fraud Victim Contact Norms"
category: Baseline
date: 2026-03-22
author: "FLAME Project (sourced from UNODC Organized Fraud Issue Paper 2024, FBI IC3)"
related_tps:
  - id: TP-0062
    relationship: related-to
  - id: TP-0011
    relationship: related-to
  - id: TP-0017
    relationship: related-to
tags:
  - recovery-fraud
  - victim-contact
  - complaint-monitoring
  - double-victimization
  - baseline
---
```

## Summary

This baseline defines normal and anomalous contact and payment patterns for customers who have filed fraud complaints. It establishes norms for legitimate post-complaint contact (callbacks from investigators, victim support outreach) versus anomalous contact patterns indicative of recovery fraud targeting. Recovery fraud operators re-contact prior fraud victims posing as recovery agents, lawyers, or government officials, exploiting the victim's emotional vulnerability and financial desperation. Organizations should calibrate DL-0133 detection thresholds against these norms to distinguish legitimate recovery-related contact from organized recovery fraud. This baseline is derived from UNODC organized fraud typology and FBI IC3 recovery fraud reporting.

## Normal Patterns

* **Legitimate investigator callback timing:** Following a fraud complaint, legitimate callbacks from institutional investigators or law enforcement typically occur **within 5–30 business days**. Contact beyond 90 days from the complaint date from unfamiliar numbers is anomalous, particularly if the caller claims to be from the same institution.

* **Legitimate contact channels:** Institutional investigators contact victims through **verified institutional phone numbers, official email domains, and registered mail**. Contact via personal mobile numbers, unverified VoIP numbers, social media direct messages, or messaging apps is anomalous for legitimate recovery processes.

* **Post-complaint payment activity to new recipients:** In the **30–90 days following a fraud complaint**, victims making payments to previously unseen recipients warrants elevated scrutiny. Legitimate recovery processes do not require victims to send money; any payment request during this window — particularly for "tax clearance," "legal retainers," "insurance bonding," or "anti-money-laundering compliance fees" — is a high-confidence recovery fraud indicator.

* **Payment method for recovery services:** Legitimate recovery attorneys and services accept payment via **business checks, ACH to verified business accounts, or credit card**. Requests for wire transfers, cryptocurrency, gift cards, or prepaid debit cards are anomalous and strongly indicative of recovery fraud.

* **Contact frequency:** Legitimate institutional follow-up involves **1–3 contacts** over the investigation period. Recovery fraud operators make **5+ contacts** with increasing urgency and payment demands, often with fabricated progress updates between payment requests.

* **Information requests:** Legitimate investigators may request **case reference numbers and incident details**. Recovery fraud operators request **bank account details, SSN/TIN, passport copies, and login credentials** under the guise of verifying identity for fund release.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Days from complaint to unsolicited contact from unfamiliar source | N/A (not expected) | 1–30 days | 30–90 days, especially referencing specific loss details |
| Payment to new recipient within 90 days of complaint | 0 payments for "recovery" purposes | 1 payment, any amount | 2+ payments or single payment >$1,000 to unfamiliar recipient |
| Payment method requested | Business check / verified ACH | Wire transfer to business account | Wire transfer to personal account, crypto, gift cards |
| Contact frequency from recovery claimant | 0 (legitimate recovery doesn't cold-call) | 1–2 unsolicited contacts | 3+ contacts with escalating urgency |
| Information requested beyond case details | Case number, incident summary | Bank account details | SSN, passport, login credentials |
| Caller ID verification (STIR/SHAKEN) | Full attestation (Level A) | Partial attestation (Level B) | No attestation (Level C) or unattested |

## Measurement Methodology

Monitor outbound payment activity for customers in the fraud complaint database, focusing on the 90-day window following complaint submission. Cross-reference recipient accounts against the customer's historical transaction partners — any payment to a previously unseen recipient during this window should be flagged for review.

Track inbound contact (calls, emails, messages) to customers with active fraud complaints. Correlate caller identity with verified institutional contact lists to distinguish legitimate investigator callbacks from unsolicited recovery fraud outreach.

For telephone contact, leverage STIR/SHAKEN attestation levels: calls from legitimate institutions should carry Level A (full) attestation. Calls claiming institutional identity but carrying Level C or no attestation are high-confidence spoofing indicators.

## Data Sources

* **Fraud complaint databases:** Customer complaint records with complaint dates, fraud types, reported loss amounts, and assigned investigator contacts.
* **Transaction monitoring systems:** Outbound payment activity correlated with complaint database records.
* **Call detail records (CDR):** Inbound call patterns to customer phone numbers on file, including caller ID verification status.
* **STIR/SHAKEN attestation data:** Caller ID verification levels for inbound calls.
* **FBI IC3 recovery fraud statistics:** Published data on recovery fraud patterns, common narratives, and victim demographics.

## Application

DL-0133 should calibrate recovery fraud detection thresholds against these baselines. Specifically, DL-0133 should flag payments from customers with fraud complaints within 90 days to previously unseen recipients, with higher severity for:
- Wire transfers or cryptocurrency payments (vs. ACH/check)
- Payments exceeding $1,000
- Multiple sequential payments to the same new recipient
- Payments accompanied by inbound calls from unattested or partially attested caller IDs

Victim support teams should proactively warn recent fraud complainants about recovery fraud during the initial complaint handling process, reducing the victim's susceptibility to recovery fraud narratives.
