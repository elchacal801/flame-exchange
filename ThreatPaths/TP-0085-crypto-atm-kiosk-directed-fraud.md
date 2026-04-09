# TP-0085: Crypto ATM/Kiosk Directed Fraud — Physical-to-Digital Monetization Channel

```yaml
---
id: TP-0085
title: "Crypto ATM/Kiosk Directed Fraud — Physical-to-Digital Monetization Channel"
category: ThreatPath
date: 2026-04-06
author: "FLAME Project"
source: "FBI IC3, 2025 Internet Crime Report"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - crypto-laundering
  - authorized-push-payment
  - elder-exploitation
sector:
  - banking
  - crypto
  - cross-sector
cfpf_phases:
  - P3
  - P4
  - P5
confidence_score: 80
source_reliability: A
info_credibility: 1
mitre_attack:
  - T1656
ft3_tactics: []
mitre_f3: ["F1025.003", "F1032", "F1017", "F1018", "F1031", "F1040", "F1045", "F1047"]
groupib_stages:
  - "Perform Fraud"
  - "Cash Out"
ucff_domains:
  commit: "Level 2"
  assess: "Level 2"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0012
    relationship: feeds-into
  - id: TP-0027
    relationship: feeds-into
  - id: TP-0049
    relationship: enables
  - id: TP-0084
    relationship: feeds-into
regulatory_refs:
  - REG-FBI-IC3
  - REG-FINCEN-AML
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - ic3-2025
  - crypto-atm
  - kiosk-fraud
  - elder-fraud
  - physical-to-digital
  - monetization-channel
---
```

## Summary

Crypto ATM/kiosk fraud is a cross-cutting monetization channel where victims of upstream fraud schemes (tech support, government impersonation, romance, investment) are directed to deposit cash at cryptocurrency ATMs/kiosks, converting physical currency to digital assets that are immediately transferred to attacker-controlled wallets. The FBI IC3 2025 Annual Report documented 13,460 complaints with $389 million in losses — a 58% increase from 2024. The elder demographic is disproportionately impacted: victims aged 60+ accounted for 6,188 complaints (46%) and $257 million in losses (66% of total crypto ATM losses).

This TP is distinct from general cryptocurrency fraud because it focuses specifically on the physical-to-digital conversion point — the crypto ATM itself — as the execution and monetization channel. The crypto ATM serves as the critical chokepoint where detection and intervention are possible before funds become irrecoverable on-chain.

## Threat Path Hypothesis

> **Hypothesis**: Victims already engaged in an upstream fraud scheme (tech support scam, government impersonation, romance scam, investment scam) are directed to locate a nearby crypto ATM, coached through the deposit process via phone, provided with a QR code or wallet address, and instructed to deposit cash. The physical-to-digital conversion at the kiosk makes the funds immediately available on-chain, where they are rapidly split through wallet fan-out, mixer, or DeFi swap operations. The crypto ATM is the last physical intervention point before funds become effectively irrecoverable.

**Confidence**: High (80). Source: FBI IC3 (A reliability), confirmed by FinCEN crypto ATM operator guidance.

**Estimated Impact**: $1,000 to $100,000+ per victim transaction. Average IC3 2025 loss: ~$28,900. Elder average: ~$41,500. Multiple deposits common.

## CFPF Phase Mapping (P3-P5 focused — this is a monetization-layer TP)

### Phase 3: Positioning (P3)

Victim coached to locate nearby crypto ATM (often via Google Maps link or specific address). Actor provides wallet address or QR code. Victim may be told crypto ATM is a "government payment terminal," "secure transfer kiosk," or "federal escrow machine." Actor stays on the phone throughout, guiding victim through unfamiliar kiosk interface.

---

### Phase 4: Execution (P4)

Victim deposits cash at crypto ATM. Machine converts cash to cryptocurrency (typically Bitcoin) and sends to provided wallet address. Transaction fees (typically 8-20% at crypto ATMs) reduce victim's deposited amount. Actor confirms receipt on-chain. Victim may be directed to make additional deposits ("the first transaction didn't process correctly," "additional fees required"). Multiple visits across multiple days are common.

---

### Phase 5: Monetization (P5)

Funds immediately split from receiving wallet through fan-out to multiple addresses. Rapid conversion through DeFi protocols, crypto mixers/tumblers, or cross-chain bridges (see TP-0049, TP-0078, TP-0080). Time from crypto ATM deposit to fund dispersion: typically < 30 minutes. Physical cash trail ends at the crypto ATM; on-chain trail is obfuscated within hours.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P3 | Crypto ATM operator: warning screens for first-time or elderly users | Preventive | Crypto ATM Operator |
| P3 | Bank-side: detect large cash withdrawal followed by no corresponding account activity | Detective | Transaction Monitoring |
| P4 | Crypto ATM operator: transaction limits for new/unverified users | Preventive | Compliance |
| P4 | Crypto ATM operator: real-time wallet screening against known-bad addresses | Detective | Blockchain Analytics |
| P4 | Crypto ATM operator: flag deposits from users over age 60 exceeding $3,000 | Detective | Compliance |
| P5 | On-chain analytics: rapid fan-out from crypto ATM deposit addresses | Detective | Blockchain Analytics |
| P5 | FinCEN SAR filing for suspicious crypto ATM transactions | Regulatory | Compliance |

---

## Detection Approaches

- Bank-side: Account holder age >= 60 AND cash withdrawal > $5,000 AND no corresponding deposit/transfer within 48 hours (DL-0212 pattern)
- Crypto ATM operator-side: First-time user, age 60+, depositing > $3,000, with wallet address flagged by blockchain analytics
- Behavioral: Customer making multiple cash withdrawals on different days, each followed by no account activity (serial kiosk deposit pattern)
- Temporal: Inbound phone call (CDR) duration > 30 minutes coinciding with cash withdrawal and crypto ATM location proximity

---

## References

- FBI IC3, 2025 Internet Crime Report — Crypto ATM/kiosk fraud: 13,460 complaints, $389M losses (58% increase)
- FBI IC3, 2025 — Elder crypto ATM fraud: 6,188 complaints, $257M from 60+ victims
- FinCEN guidance on money services business obligations for crypto ATM operators
- https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf

---

## Analyst Notes

1. **Critical chokepoint for intervention**: The crypto ATM is the critical chokepoint for intervention. Once funds are deposited and converted to cryptocurrency, recovery rates drop dramatically. Detection and intervention must occur at or before the kiosk.

2. **Elder loss concentration**: The 66% elder loss concentration (60+ victims = $257M of $389M total) makes age-based risk scoring at crypto ATMs one of the highest-ROI detection investments.

3. **Regulatory scrutiny increasing**: Crypto ATM operators face increasing regulatory scrutiny. FinCEN requires SAR filing for suspicious transactions, and several states have implemented deposit limits. Detection partnerships between banks and crypto ATM operators can create a feedback loop: banks flag unusual cash withdrawals, notify crypto ATM operators to watch for the customer.

4. **Downstream monetization path**: This TP serves as a downstream monetization path for multiple upstream TPs: TP-0012 (tech support → crypto ATM), TP-0084 (government impersonation → crypto ATM), TP-0011 (romance → crypto ATM). Detection rules should correlate upstream fraud indicators with crypto ATM deposit behavior.

5. **Growth outpacing overall crypto fraud**: The 23% complaint increase and 58% loss increase from 2024 indicate this channel is growing faster than the overall crypto fraud trend (21% complaint increase), suggesting criminals are increasingly directing victims to crypto ATMs as a preferred monetization path.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-04-06 | FLAME Project | Initial submission from FBI IC3 2025 Annual Report |
