# TP-0084: Government Impersonation — Authority-Based Authorized Push Payment Fraud

```yaml
---
id: TP-0084
title: "Government Impersonation — Authority-Based Authorized Push Payment Fraud"
category: ThreatPath
date: 2026-04-06
author: "FLAME Project"
source: "FBI IC3, 2025 Internet Crime Report"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - impersonation
  - authorized-push-payment
  - social-engineering
  - elder-exploitation
sector:
  - banking
  - cross-sector
  - government
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 85
source_reliability: A
info_credibility: 1
mitre_attack:
  - T1656
  - T1598
ft3_tactics: []
mitre_f3: []
groupib_stages:
  - "Social Engineering"
  - "Perform Fraud"
  - "Cash Out"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0012
    relationship: related-to
  - id: TP-0027
    relationship: feeds-into
  - id: TP-0062
    relationship: enhances
  - id: TP-0082
    relationship: enables
  - id: TP-0081
    relationship: shares-infrastructure
  - id: TP-0085
    relationship: enables
regulatory_refs:
  - REG-FBI-IC3
  - REG-CFPB-REGE
  - REG-OCC-FRAUD
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - ic3-2025
  - government-impersonation
  - authority-abuse
  - caller-id-spoofing
  - irs-impersonation
  - ssa-impersonation
  - elder-fraud
  - app-fraud
---
```

## Summary

Government impersonation fraud uses the authority of federal and state agencies — IRS, SSA, DOJ, FBI, DEA, and state attorneys general — as a social engineering weapon to compel victims into making authorized push payments. The FBI IC3 2025 Annual Report documented 32,424 complaints with $797.9 million in losses, representing an 87% increase in complaints and 97% increase in losses from 2024. This is fundamentally distinct from government program fraud (TP-0022) which exploits government systems for unauthorized benefit claims. Here, the government is not the victim — it is the impersonated authority used to intimidate and control the actual victim.

The payment channel distribution reveals the scheme's adaptability: Cryptocurrency 40%, Wire Transfer/ACH 21%, Prepaid card/Gift card 15%, Cash 14%, Check/Cashier's Check 10%. Victims aged 60+ are disproportionately targeted, accounting for 8,628 complaints and $413.2 million in losses (52% of total losses).

A notable sub-variant involves scammers impersonating the FBI IC3 itself (PSA250418), exploiting victims' awareness of IC3 as a fraud reporting resource to add credibility to recovery or refund schemes.

## Threat Path Hypothesis

> **Hypothesis**: Criminal networks — primarily operating from transnational call centers in India and Southeast Asia — impersonate government officials via phone, email, and text messages to create urgency and fear in victims. Using caller ID spoofing and official-sounding scripts, actors fabricate legal threats (arrest warrants, tax liens, benefit suspension, identity theft investigations) to compel victims to make immediate payments through diverse channels. The multi-channel payment distribution (crypto, wire, prepaid, cash) makes single-channel detection insufficient; comprehensive behavioral analytics covering all outbound payment methods are required.

**Confidence**: Very High (85). Source: FBI IC3 (A reliability), confirmed by IC3 PSA250418 and international law enforcement operations.

**Estimated Impact**: $5,000 to $500,000+ per victim. Average IC3 2025 loss: ~$24,600. Elder victims average higher due to larger accessible funds.

## CFPF Phase Mapping

### Phase 1: Recon (P1)

Actor acquires victim contact information from data brokers, prior victim lists, and public records. Caller ID spoofing infrastructure configured to display legitimate government agency numbers. Scripts tailored to impersonate specific agencies (IRS for tax season, SSA for benefits, DOJ/FBI for legal threats). Elder targets prioritized based on estimated account balances and social isolation indicators.

---

### Phase 2: Initial Access (P2)

Robocall or live call from "government official" with fabricated scenario. Common pretexts: "Your Social Security number has been used in criminal activity," "Tax fraud has been filed under your name," "An arrest warrant has been issued — pay to resolve," "Your accounts have been compromised and must be secured." Caller ID shows legitimate government phone number via STIR/SHAKEN bypass or VoIP spoofing. Secondary contact via email or text with fabricated case numbers, badge numbers, and official letterhead.

---

### Phase 3: Positioning (P3)

Actor escalates urgency: "If you do not comply within 2 hours, officers will be dispatched." Victim instructed to not contact their bank, family, or local police ("this is a sealed federal investigation"). Payment method instructions provided: directed to nearest crypto ATM with QR code, instructed to purchase prepaid gift cards and read numbers, directed to wire funds to "government escrow account," or told to withdraw cash for courier pickup. In gold courier variant (TP-0082), directed to purchase physical gold.

---

### Phase 4: Execution (P4)

Victim makes payment via directed channel. Crypto ATM: victim deposits cash, receives crypto sent to actor's wallet (40% of losses). Wire/ACH: victim initiates wire to actor-controlled account (21%). Prepaid/gift card: victim purchases cards and reads numbers to actor (15%). Cash: victim mails cash or provides to courier (14%). Multiple payment episodes common — actor calls back for additional "fees," "taxes," or "security deposits."

---

### Phase 5: Monetization (P5)

Crypto proceeds immediately split through wallet fan-out and mixing. Wire transfers layered through mule accounts and international transfers (top destinations: Hong Kong, Mexico, India). Gift card values resold on secondary markets or converted to crypto. Cash couriered through money mule networks. International FFKC may be initiated for wire transfers.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P2 | STIR/SHAKEN caller authentication | Preventive | Telecom |
| P2 | Government agency impersonation call detection (CDR analytics) | Detective | Telecom/Fraud |
| P3 | Bank teller training: government payment urgency = red flag | Detective | Branch Operations |
| P3 | Customer outreach for unusual outbound payments with government references | Detective | Fraud Operations |
| P4 | Payment reference keyword monitoring ("IRS", "SSA", "warrant", "penalty", "federal") | Detective | Transaction Monitoring |
| P4 | Crypto ATM operator: flag first-time elderly users making large deposits | Detective | Crypto ATM Compliance |
| P4 | Gift card retailer: flag large gift card purchases by elderly customers | Detective | Retail Partners |
| P5 | FFKC initiation for wire transfers to known mule accounts | Responsive | RAT/FBI IC3 |

---

## Detection Approaches

- Multi-channel payment monitoring: flag customers making outbound payments via crypto, wire, AND prepaid within 72 hours (multi-channel coercion indicator)
- Government reference detection: payment references containing agency names or legal terminology from customers with no prior government-related payment history
- Behavioral anomaly: elderly customer making first-ever crypto ATM deposit, prepaid card purchase, or wire to unfamiliar beneficiary following inbound phone call
- Temporal correlation: inbound VoIP call + large withdrawal/payment within 4 hours = high-priority alert

---

## References

- FBI IC3, 2025 Internet Crime Report — Government impersonation: 32,424 complaints, $797.9M losses (87% increase)
- FBI IC3 PSA250418, April 18, 2025 — "FBI Warns of Scammers Impersonating the IC3"
- FBI IC3, 2025 — Call center fraud: 80,000+ complaints, $2.9B losses across tech support and government impersonation
- FBI/CBI Operation Chakra, December 2025 — Dismantled Noida-based transnational government impersonation call center
- https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf
- https://www.ic3.gov/PSA/2025/PSA250418

---

## Analyst Notes

1. **Fastest-growing IC3 category**: The 87% complaint increase and 97% loss increase make government impersonation the fastest-growing major IC3 fraud category in 2025.

2. **Multi-channel detection required**: The payment channel distribution (40% crypto, 21% wire, 15% prepaid, 14% cash, 10% check) makes this fraud type unusually difficult to detect with single-channel monitoring. Detection strategies must be multi-channel.

3. **India call center nexus**: The India call center nexus is well-documented: FBI/CBI Operation Chakra (December 2025) dismantled a Noida-based network responsible for $48.7M in losses. FBI San Diego EJTF identified 500+ elder victims from a single international network ($40M+).

4. **IC3 impersonation meta-variant**: PSA250418 (scammers impersonating IC3) represents a meta-variant: actors exploit victims' awareness of IC3 as a fraud reporting resource to conduct recovery fraud (TP-0062) under IC3's brand authority.

5. **Distinction from TP-0022**: TP-0022 (Government Program Fraud) covers exploitation OF government programs (fake unemployment claims, tax refund fraud). TP-0084 covers impersonation OF government authority to defraud private victims via APP. Different attack surface, different victim, different controls.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-04-06 | FLAME Project | Initial submission from FBI IC3 2025 Annual Report |
