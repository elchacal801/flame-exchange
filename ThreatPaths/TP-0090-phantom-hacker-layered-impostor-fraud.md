# TP-0090: Phantom Hacker — Layered Impostor Account Drain

```yaml
---
id: TP-0090
title: "Phantom Hacker — Layered Impostor Account Drain"
category: ThreatPath
date: 2026-08-22
last_reviewed: 2026-08-22
author: "FLAME Project"
source: "https://www.ic3.gov/PSA/2023/PSA230929"
tlp: WHITE
sector:
  - banking
  - credit-union
  - investment
  - cross-sector
fraud_types:
  - phantom-hacker
  - tech-support-scam
  - impersonation
  - vishing
  - authorized-push-payment
  - elder-exploitation
  - wire-fraud
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "social-engineering"
primary_phase: "P3"
short_name: "Phantom Hacker"
mitre_attack:
  - T1566.002  # Phishing: Spearphishing Link (pop-up/email lure)
  - T1219      # Remote Access Software
  - T1656      # Impersonation
  - T1657      # Financial Theft
ft3_tactics: ["FTA001", "FTA003", "FTA005", "FTA009", "FT001", "FT005", "FT016"]
mitre_f3: ["F1029", "F1032", "F1040.002", "T1219", "F1025.003", "F1018", "F1017.001", "F1044"]
groupib_stages:
  - "Reconnaissance"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 2"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
confidence_score: 82
source_reliability: A
info_credibility: 2
related_tps:
  - id: TP-0012
    relationship: related-to
  - id: TP-0084
    relationship: related-to
  - id: TP-0082
    relationship: enhances
  - id: TP-0085
    relationship: enhances
  - id: TP-0062
    relationship: feeds-into
regulatory_refs:
  - REG-FBI-IC3
  - REG-FINCEN-EFE
baseline_ids:
  - BL-0037
tags:
  - phantom-hacker
  - tech-support-scam
  - layered-impostor
  - safe-account
  - remote-access
  - elder-fraud
  - wire-fraud
  - crypto-atm
---
```

## Summary

The Phantom Hacker scam — the FBI's name for a three-actor impostor chain first described in IC3 PSA230929 — is an industrialized evolution of the tech support scam in which victims are handed off between a fake technology support worker, a fake financial-institution fraud department, and finally a fake government official, each escalation engineered to deepen trust and isolate the victim. The scheme's signature is the "safe account" fiction: victims are persuaded their savings are exposed to a foreign hacker and must be moved — by wire, cash, or cryptocurrency — to a "protected" account at the Federal Reserve or another government agency that is in fact actor-controlled.

The scheme sits inside the IC3's largest loss categories: tech/customer support fraud recorded 47,794 complaints and $2.13B in reported losses in 2025, with individuals over 60 accounting for roughly half of victims and losses. In the 2023 baseline period that prompted the FBI's PSA, half of victims were over 60 and bore 66% of losses; many lost entire banking, savings, retirement, or investment balances "protecting" them.

What distinguishes this path from generic tech support fraud (TP-0012) or government impersonation APP fraud (TP-0084) is the **layered, sequential structure**: an internal reconnaissance phase (the "tech support" actor has the victim open every financial account while screen-sharing, so the ring can select the most lucrative target), followed by role-segregated social engineering where each successive impostor validates the previous one's story.

## Threat Path Hypothesis

> **Hypothesis**: Transnational call-center rings execute a scripted three-role relay — tech support impostor (access + account reconnaissance), bank impostor (threat narrative + transfer instruction), government impostor (authority reinforcement + objection handling) — to convert a victim's own authenticated access into serial authorized push payments toward "safe accounts." Because every transfer is customer-initiated and authenticated, controls anchored on credential compromise miss it entirely; effective detection must key on remote-access-tool telemetry coinciding with account survey behavior, and on out-of-pattern outbound transfers narrated as "account protection."

**Confidence**: High (82). Source: FBI IC3 PSA230929 and 2025 Annual Report (A reliability); corroborated by financial-sector fraud advisories and IC3 PSA251125 on financial-institution-support impersonation.

**Estimated Impact**: $10,000 to full account drain (retirement/brokerage balances routinely six figures). Transfers repeat over days or months; victims are told to keep the "investigation" secret.

## CFPF Phase Mapping

### Phase 1: Recon (P1)

Ring acquires target lists skewed toward older adults (data brokers, prior sucker lists, breach data). Pop-up/email lure infrastructure staged; support phone lines and scripts prepared for all three roles. Official-looking correspondence templates (Federal Reserve letterhead) prepared for objection handling.

---

### Phase 2: Initial Access (P2)

Victim contacted via pop-up window, email, text, or call directing them to a "support" number. The tech support impostor instructs the victim to install legitimate remote-access software (screen sharing), then stages a fake malware discovery. Under the pretext of "checking for unauthorized charges," the victim is told to open all banking, brokerage, and retirement accounts while the actor watches — an in-session account survey that selects the highest-value target.

---

### Phase 3: Positioning (P3)

Handoff one: the victim receives a call from the impostor "fraud department" of their actual bank or brokerage (name gleaned in P2), told a foreign hacker has access, and that funds must move to a "safe" government-protected account. Handoff two: a "Federal Reserve" or agency official reinforces the story; skeptical victims receive official-looking letters or emails. Victims are instructed to tell no one — bank staff included — because bank insiders are "part of the investigation." Secrecy coaching defeats branch-level interdiction.

---

### Phase 4: Execution (P4)

Victim initiates transfers: wire transfers to actor-controlled domestic or foreign accounts, cash withdrawals (courier pickup or mailing), or cryptocurrency purchases at exchanges and kiosks. Transfers are structured as multiple transactions across days or months, each below the victim's anxiety threshold, often timed to available balances as CDs mature or retirement disbursements arrive.

---

### Phase 5: Monetization (P5)

Wires layered through mule accounts toward foreign endpoints; cash consolidated through courier networks; crypto fanned out through intermediary wallets. Victims who exhaust liquid funds are recycled into recovery-fraud targeting (TP-0062).

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P2 | Detect remote-access tool session overlapping online-banking session (RAT-in-session flag) | Detective | Digital Channel Fraud |
| P2 | In-session warning when screen sharing is active during authenticated banking | Preventive | Digital Banking |
| P3 | Customer education: banks never move money to "safe accounts"; government never requests wires | Preventive | Fraud Awareness |
| P3 | Outbound-payment interview scripts keyed to "account protection" narratives | Detective | Branch/Contact Center |
| P4 | Hold-and-verify for first-time high-value wires by customers 60+ with no wire history | Preventive | Payment Operations |
| P4 | Crypto kiosk age/velocity thresholds (BL-0037 norms) | Detective | Crypto ATM Compliance |
| P4 | Serial-transfer pattern: repeated out-of-pattern transfers to a common beneficiary over days | Detective | Transaction Monitoring |
| P5 | FFKC initiation and IC3 RAT referral on confirmed safe-account wires | Responsive | Fraud Operations |

---

## Detection Approaches

- **RAT + account-survey correlation**: remote-access software fingerprint (or screen-share session) concurrent with an authenticated session that touches an unusual breadth of accounts (checking + savings + brokerage + retirement within minutes) — the P2 reconnaissance signature
- **Safe-account narrative detection**: outbound wire/transfer requests where the customer references the Federal Reserve, "safe account," "federal investigation," or account protection; contact-center speech/text analytics keyed to the scripted vocabulary
- **Serial drain pattern**: multiple out-of-pattern transfers from a 60+ customer to the same new beneficiary across days-to-weeks, especially following an inbound-call-adjacent session
- **Cross-channel sequence**: new remote-access session → large balance inquiry sweep → first-ever wire request within 72 hours = high-priority alert
- **Secrecy indicator**: customer declines routine wire-purpose questions or gives rehearsed non-answers at branch; pair with age and first-time-wire flags

---

## References

- FBI IC3 PSA230929, September 29, 2023 — "'Phantom Hacker' Scams Target Senior Citizens and Result in Victims Losing their Life Savings": the canonical three-phase description; Jan–Jun 2023: 19,000 tech-support complaints, $542M losses, 50% of victims over 60 bearing 66% of losses. [Link](https://www.ic3.gov/PSA/2023/PSA230929)
- FBI IC3, 2025 Internet Crime Report — Tech/customer support: 47,794 complaints, $2.13B losses; ~50% of victims and losses aged 60+. [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)
- FBI IC3 PSA251125, November 2025 — Account takeover via impersonation of financial-institution support (the phase-two persona operating standalone). [Link](https://www.ic3.gov/PSA/2025/PSA251125)
- **Related FLAME Threat Paths**: [TP-0012](TP-0012-app-fraud-tech-support-impersonation.md) (single-persona tech-support/bank APP fraud); [TP-0084](TP-0084-government-impersonation-app-fraud.md) (government-authority APP coercion — the phantom hacker's phase 3 as a standalone scheme); [TP-0082](TP-0082-gold-courier-scam.md) and [TP-0085](TP-0085-crypto-atm-kiosk-directed-fraud.md) (alternative monetization channels for the same coercion chain); [TP-0062](TP-0062-recovery-fraud-double-dip-revictimization.md) (downstream re-victimization).

---

## Analyst Notes

1. **The account survey is the tell**: The phase-2 "open all your accounts so I can check for fraud" step is operationally unique to this scheme — it is target selection performed through the victim's own authenticated session. RAT-plus-breadth-of-account-access telemetry is the highest-precision early signal available, and it fires before any money moves.

2. **Role segregation defeats single-touchpoint verification**: Each impostor's story is validated by the next caller, so a victim who "verifies" by expecting a bank call or a government letter receives exactly that. Verification advice to customers must specify *outbound* contact through independently obtained numbers, not any inbound confirmation.

3. **Authenticated ≠ authorized-by-informed-consent**: Every transfer in this path passes authentication, device, and (often) behavioral-biometric checks — it is the genuine customer, on their genuine device, under coached duress. This is the strongest argument in the corpus for narrative-aware controls (payment-purpose interviews, speech analytics) layered over transaction analytics.

4. **Distinction from TP-0012 and TP-0084**: TP-0012 covers the compressed one-or-two-persona variant; TP-0084 covers government-authority coercion without the tech-support entry or account survey. The phantom hacker chain is distinguished by the reconnaissance phase and the three-role relay — and by loss severity, since target selection ensures the drained account is the victim's largest.

5. **Elder-protection reporting hooks**: U.S. institutions filing SARs on suspected cases should consider FinCEN's elder financial exploitation guidance alongside IC3 reporting; rapid FFKC initiation materially improves wire recovery odds inside 72 hours.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-08-22 | FLAME Project | Initial submission from FBI IC3 PSA230929, IC3 2025 Annual Report, PSA251125 |
