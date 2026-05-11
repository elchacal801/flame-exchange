# TP-0083: Investment Club Scam — Social Media Insider Group Fraud

```yaml
---
id: TP-0083
title: "Investment Club Scam — Social Media Insider Group Fraud"
category: ThreatPath
date: 2026-04-06
author: "FLAME Project"
source: "FBI IC3, 2025 Internet Crime Report"
tlp: WHITE
infrastructure_generation_method: ai-assisted
fraud_types:
  - investment-scam
  - social-engineering
  - authorized-push-payment
  - crypto-laundering
sector:
  - investment
  - banking
  - crypto
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "investment-romance"
primary_phase: "P3"
short_name: "Investment Club Scam"
confidence_score: 72
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1566.003
  - T1656
ft3_tactics: []
mitre_f3: ["F1020.002", "F1025.003", "F1018", "F1031", "F1032", "F1040", "F1045", "F1047", "T1598", "T1660"]
groupib_stages:
  - "Reconnaissance"
  - "Social Engineering"
  - "Perform Fraud"
  - "Cash Out"
ucff_domains:
  commit: "Level 2"
  assess: "Level 2"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 2"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0017
    relationship: related-to
  - id: TP-0026
    relationship: enhances
  - id: TP-0060
    relationship: feeds-into
regulatory_refs:
  - REG-FBI-IC3
  - REG-SEC-SAR
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
tags:
  - ic3-2025
  - investment-club
  - social-media
  - group-fraud
  - social-proof
  - telegram
  - whatsapp
  - discord
---
```

## Summary

Investment club scams exploit social media and messaging platforms to create fraudulent "insider" trading groups that lure victims with fabricated trading success, AI-generated celebrity endorsements, and peer pressure dynamics. The FBI IC3 2025 Annual Report documented approximately 1,600 complaints with $160 million in losses, and PSA250703 (July 3, 2025) specifically warned about investment clubs accessed on social media and messaging applications. Unlike traditional pig butchering (TP-0017) which relies on 1:1 grooming, investment club scams leverage group dynamics — social proof from other "members" (often shills or bots), fake trading screenshots, and the illusion of an exclusive community — to accelerate victim conversion and increase investment amounts.

## Threat Path Hypothesis

> **Hypothesis**: Criminal groups create investment clubs on Telegram, WhatsApp, Discord, Instagram, and similar platforms, presenting themselves as knowledgeable traders or financial insiders offering exclusive access to profitable opportunities. AI-generated videos and deepfake celebrity endorsements are used to create legitimacy. Victims join the group, observe fabricated trading wins from other members (shills), and are directed to deposit funds via cryptocurrency exchanges or wire transfers to fraudulent trading platforms. The group dynamic creates social proof and peer pressure that accelerates the exploitation cycle.

**Confidence**: Medium-High (72). Source: FBI IC3 (A reliability), corroborated by PSA250703. Lower confidence than pig butchering due to newer emergence and less documented case history.

**Estimated Impact**: $10,000 to $500,000+ per victim. Aggregated losses from organized operations can reach tens of millions.

## CFPF Phase Mapping

### Phase 1: Recon (P1)

Creation of social media profiles posing as successful traders/investors. Establishment of Telegram/WhatsApp/Discord groups with fabricated member counts. AI-generated content production (trading screenshots, video testimonials, celebrity endorsements). Target identification through social media ad targeting (interests: investing, crypto, financial independence).

---

### Phase 2: Initial Access (P2)

Victims recruited via targeted social media ads, direct messages, or referrals from already-recruited members. Invitation to "exclusive" or "VIP" investment group. Initial engagement with group content showing fabricated returns and member testimonials.

---

### Phase 3: Positioning (P3)

Group moderators coach new members on "trading strategies." Fake trading wins displayed in real-time (screenshots, platform demos). Social proof from shill accounts confirming profits. Small initial investments encouraged with fabricated returns shown on fraudulent dashboard. Victims encouraged to recruit friends/family (MLM-style expansion).

---

### Phase 4: Execution (P4)

Victims directed to deposit via crypto exchanges, wire transfers, or P2P platforms to fraudulent trading platforms. Progressive investment increases encouraged by fabricated returns. "Premium" or "VIP" tiers requiring larger deposits introduced. Withdrawal requests delayed with excuses (tax obligations, verification, minimum balances).

---

### Phase 5: Monetization (P5)

Deposited funds immediately laundered through crypto mixing, layered transfers, or mule networks. Fraudulent platform shows fabricated balances while funds have already been extracted. Group eventually dissolved or members blocked when extraction is complete.

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P2 | Social media ad monitoring for fraudulent investment group ads | Preventive | Brand Protection |
| P3 | Customer awareness: investment club red flags | Preventive | Customer Communications |
| P4 | Detection of crypto exchange deposits correlated with social media referral patterns | Detective | Fraud Operations |
| P4 | Multiple unrelated customers sending to same novel beneficiary (cluster detection) | Detective | Transaction Monitoring |
| P5 | Rapid crypto conversion post-deposit | Detective | AML/Blockchain Analytics |

---

## Detection Approaches

- Cluster deposit detection: >= 5 unique, unrelated customers depositing to the same novel beneficiary within 14 days
- Social media referral tracking: multiple new accounts funded from crypto exchanges within short windows, all with investment-related payment references
- Behavioral analytics: customer with no prior investment activity suddenly making repeated large deposits to crypto exchanges

---

## References

- FBI IC3, 2025 Internet Crime Report — Investment club scams: ~1,600 complaints, $160M losses
- FBI IC3 PSA250703, July 3, 2025 — "Fraudsters Target US Stock Investors through Investment Clubs Accessed on Social Media and Messaging Applications"
- https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf
- https://www.ic3.gov/PSA/2025/PSA250703

---

## Analyst Notes

1. **Distinction from pig butchering**: The key distinction between investment club scams and pig butchering (TP-0017) is the attack surface: investment clubs exploit group dynamics (social proof, peer pressure, FOMO) rather than 1:1 relationship grooming. This makes the exploitation cycle faster — victims can be converted in days rather than weeks.

2. **AI-generated content is central**: AI-generated content is central to the scheme: fabricated trading screenshots, deepfake celebrity endorsements (CEOs, financial personalities), and professional-looking video analyses create an illusion of legitimacy that individual pig butchering operations typically lack.

3. **Transaction channel distribution**: IC3 2025 investment fraud transaction data: 72% crypto, 19% wire/ACH, 4% P2P. The crypto dominance suggests detection should focus on exchange deposit patterns.

4. **SE Asia scam compound nexus**: IC3 2025 confirms these operations are largely run by organized criminal enterprises in Southeast Asia using human trafficking victims as forced labor.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-04-06 | FLAME Project | Initial submission from FBI IC3 2025 Annual Report and PSA250703 |
