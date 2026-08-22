# TP-0008: SIM Swap to Cryptocurrency Exchange ATO

```yaml
---
id: TP-0008
title: "SIM Swap to Cryptocurrency Exchange ATO"
category: ThreatPath
date: 2026-03-04
last_reviewed: 2026-03-28
author: "FLAME Project"
source: "FBI IC3 / DOJ SIM swap prosecutions / industry reporting"
tlp: WHITE
sector:
  - crypto
  - fintech
  - banking
fraud_types:
  - account-takeover
  - crypto-laundering
cfpf_phases: [P1, P2, P3, P4, P5]
fraud_family: "account-takeover"
primary_phase: "P2"
short_name: "SIM Swap ATO"
mitre_attack: [T1111, T1078, T1657]
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA004", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT011.002", "FT043", "FT003", "FT006.002", "FT038.002", "FT044", "FT005.001", "FT008.001", "FT013", "FT016"]                  # Stripe FT3 (when mapped)
mitre_f3: ["F1006.002", "T1110.001", "T1555", "F1004", "F1018", "F1025", "F1045", "F1047", "T1185", "T1451"]
groupib_stages:               # Group-IB Fraud Matrix (reference)
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "Credential Access"
  - "Account Access"
  - "Defence Evasion"
  - "Perform Fraud"
  - "Monetization"
  - "Laundering"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 3"
  report: "Level 3"
  improve: "Level 3"
confidence_score: 82
source_reliability: B
info_credibility: 2
related_tps:
  - id: TP-0001
    relationship: enables
  - id: TP-0005
    relationship: enables
  - id: TP-0013
    relationship: enables
  - id: TP-0037
    relationship: enables
regulatory_refs:
  - REG-CFPB-REGE
  - REG-DORA
  - REG-EU-AMLD6
  - REG-FFIEC-AUTH
  - REG-FINCEN-AML
  - REG-OCC-FRAUD
  - REG-PSD3-SCA
baseline_ids: []
tags:
  - SIM-swap
  - cryptocurrency
  - MFA-bypass
  - carrier-social-engineering
  - high-value-individual
  - otp-interception
  - otp-bot
  - evilginx
---
```

## Summary

Actors social-engineer mobile carriers to transfer a victim's phone number to an actor-controlled SIM card, then use intercepted SMS-based MFA codes to take over cryptocurrency exchange accounts and drain digital assets. FBI IC3 reported $68M+ in SIM swap losses in 2021 alone, with individual losses frequently exceeding $1M for high-net-worth crypto holders. DOJ has prosecuted multiple SIM swap rings targeting crypto investors specifically.

## Threat Path Hypothesis

> **Hypothesis**: Actors are targeting high-value cryptocurrency holders through SIM swap attacks at mobile carriers, using intercepted MFA codes to bypass exchange security and drain digital wallets, then laundering proceeds through mixing services and cross-chain bridges.

**Confidence**: High — extensive DOJ prosecution history, FBI IC3 data, confirmed attack chains.
**Estimated Impact**: $50,000 – $10,000,000+ per victim. Crypto's irreversibility makes recovery near-impossible.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-005: Social media recon | Identify crypto holders through social media posts (trading screenshots, NFT displays, conference attendance, Discord/Telegram group membership) | Scraping of crypto-focused social media; monitoring of blockchain conference attendee lists |
| CFPF-P1-004: Dark web acquisition | Purchase victim PII (SSN, DOB, account PINs, carrier account details) from dark web markets or data broker leaks | PII packages for sale referencing crypto investors |
| Carrier employee recruitment | Bribe or recruit insiders at mobile carriers to execute SIM swaps without standard verification | Carrier insider activity outside normal patterns |

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-006: SIM swap | Contact mobile carrier impersonating victim (or via bribed insider) to port phone number to new SIM. Victim's phone immediately loses service. | Victim reports sudden loss of cellular service; unauthorized SIM change on carrier records |
| SMS MFA interception | With phone number controlled, receive all SMS-based MFA codes for victim's accounts | MFA codes delivered to new device; login attempts immediately following SIM swap |
| CFPF-P2-005: Credential access | Use previously obtained credentials (phishing, breach data, social engineering) combined with intercepted MFA to authenticate to exchange | Login from new device/IP with valid credentials + MFA |

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-003: Contact info modification | Change email, phone, and recovery options on exchange account to actor-controlled addresses | Account recovery contact changes immediately after login from new device |
| CFPF-P3-005: New MFA device | Enroll actor-controlled authenticator app, disable SMS MFA | MFA device changes following SIM swap window |
| API key creation | Generate API keys for programmatic access to exchange account (enables faster, automated withdrawals) | New API key creation from anomalous session |

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Cryptocurrency withdrawal | Drain all exchange balances — spot holdings, staking positions, DeFi deposits — to actor-controlled wallets | Maximum withdrawal activity; withdrawals to previously unused addresses; withdrawal of all asset types simultaneously |
| NFT transfer | Transfer high-value NFTs to actor wallets | NFT transfers to new wallets during same session as crypto withdrawals |

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-003: Crypto laundering | Funds routed through mixing services (Tornado Cash, Sinbad), cross-chain bridges, or chain-hopping (BTC → Monero → BTC) | Transactions to known mixer addresses; rapid cross-chain transfers; peel chain patterns |
| Peer-to-peer off-ramping | Convert crypto to fiat through P2P OTC desks, LocalBitcoins-style platforms, or international exchanges with weak KYC | Fiat withdrawals at exchanges in low-oversight jurisdictions |

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| PII Sourcer | Fullz shops providing name, SSN, DOB, address, phone | High | $5-$200 per fullz |
| Carrier Insider | Corrupt mobile carrier employees performing unauthorized SIM swaps | Medium | $500-$5,000 per swap |
| Social Engineer | Caller impersonating account holder to carrier support | High | $100-$500 per successful swap |
| SIM Swap Service Operator | End-to-end SIM swap execution as a service | Medium | $300-$1,500 per target |
| OTP Interception | Services that capture one-time passwords post-swap | High | Bundled with swap service |
| Crypto Cashout | Rapid exchange conversion and tumbling services | High | 5-15% of stolen assets |

### Tool Ecosystem
OSINT tools for target reconnaissance (PII aggregators, social media scrapers), carrier account lookup tools, call spoofing services, VoIP platforms for social engineering calls, cryptocurrency wallet drainers, automated exchange withdrawal tools, SIM cloning hardware (less common than social engineering approach).

### Underground Marketplace Presence
SIM swap services are actively advertised on Telegram channels, dark web forums, and closed Discord/Telegram groups specializing in crypto theft. Carrier insider recruitment occurs on dedicated channels with regional specificity (specific carriers targeted based on known insider availability). Pricing follows a tiered model — basic social engineering swaps at the lower end, confirmed insider-assisted swaps commanding premium prices. The SIM swap to crypto ATO pipeline is a well-documented and commoditized attack chain.

### Intelligence Sources
- Recorded Future "Business of Fraud" (CTA-2021-0225) — SIM swap pricing and supply chain
- FBI PIN 2022-0305-001 — SIM swapping and MFA bypass
- CISA Advisory on SIM swap mitigation
- Princeton University "An Empirical Study of Wireless Carrier Authentication"

## Controls & Mitigations

| Phase | Control | Type |
|-------|---------|------|
| P1 | Carrier account PIN/passphrase (set on mobile account to prevent unauthorized SIM changes) | Preventive |
| P1 | Carrier port-freeze / number lock | Preventive |
| P2 | **Never use SMS-based MFA for high-value accounts** — hardware keys (YubiKey) or authenticator apps only | Preventive |
| P3 | Exchange: flag and hold withdrawals when account recovery contacts change within 24-48hrs of login | Detective |
| P4 | Exchange: mandatory 24-72hr withdrawal hold for new devices/IPs | Preventive |
| P4 | Exchange: withdrawal address whitelisting with time-lock on additions | Preventive |
| P5 | Blockchain analytics: flag transactions to known mixer/tumbler addresses | Detective |

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate to eliminate SMS-based MFA for high-value accounts; investment in hardware security key programs and carrier-level SIM swap detection APIs |
| ASSESS | Level 3 (Established) | Risk assessment of authentication methods across all customer-facing platforms; identification of high-value account holders relying on SMS MFA; evaluation of carrier API integration for SIM swap detection |
| PLAN | Level 3 (Established) | Incident response playbook for SIM swap-initiated ATO including carrier coordination and blockchain tracing; withdrawal hold policies for accounts showing SIM change indicators |
| ACT | Level 4 (Advanced) | Real-time SIM swap detection via carrier network APIs (SIM Swap Check, Number Verification); mandatory withdrawal holds when account recovery contacts change within 24-48 hours of new device login; withdrawal address whitelisting with time-locked additions; blockchain analytics integration for mixer/tumbler detection |
| MONITOR | Level 3 (Established) | Correlation of SIM change events with subsequent MFA authentication attempts and withdrawal requests; monitoring for new device logins followed by contact info changes and maximum withdrawal activity |
| REPORT | Level 3 (Established) | SAR filing with SIM swap and crypto laundering indicators; coordination with carrier fraud teams and law enforcement for active SIM swap investigations; blockchain intelligence sharing with exchanges |
| IMPROVE | Level 3 (Established) | Post-incident review incorporating carrier-side SIM change data; tracking of emerging OTP interception techniques (OTP bots, AiTM kits, eSIM hijacking) to update authentication controls |

## Detection Approaches

**Exchange-Side — SIM Swap Indicator Correlation**

```sigma
title: New Device Login After SIM Swap
status: experimental
description: Detects a new device login following a recently detected SIM and MFA change.
logsource:
    category: application
    product: exchange_platform
detection:
    selection_login:
        EventName: 'UserLogin'
        DeviceIsNew: true
    selection_mfa:
        EventName: 'MFAMethodChanged'
    selection_contact:
        EventName: 'ContactInfoChanged'
    selection_withdraw:
        EventName: 'CryptoWithdrawal'
        AddressIsNew: true
    timeframe: 24h
    condition: selection_login and selection_mfa and selection_contact and selection_withdraw
```

**Carrier-Side — Anomalous SIM Change Detection**

```
Flag SIM changes where:
  - Change requested through non-standard channel (call center vs. retail)
  - Change followed by immediate account activity at financial services
  - Customer has no prior SIM change history
  - Multiple SIM changes across different customers by same representative
```

## Operational Evidence

### EV-TP0008-2026-001: 2026 Technical Landscape — SIM Swap Surge and Network-Level API Detection

- **Source**: Organized fraud detection in 2026: a technical landscape report
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: SIM swap fraud surged 1,055% in the UK with 3,000 cases in 2024. Network-level APIs provide the most effective detection: SIM Swap Check (has SIM changed recently?), Number Verification (is number still assigned to expected device?), Call Forwarding Signal (is call forwarding active?). These APIs enable real-time verification before MFA code delivery, preventing the core SIM swap attack vector. Detection should correlate SIM change events with subsequent MFA authentication attempts.

## Analyst Notes

**OTP Interception Beyond SIM Swap (2024-2025)**: The Recorded Future Annual Payment Fraud Intelligence Report 2025 documented the cementing of OTP interception as a popular technique for circumventing authentication, extending well beyond SIM swap. TransUnion's 2025 report identified OTPs as the most common form of secondary authentication globally, making OTP interception a high-value capability for threat actors. Key OTP interception techniques that have matured alongside SIM swap include: (1) **OTP bot services** — automated call-back bots on Telegram that call victims and socially engineer them into entering their OTP, which is then relayed to the attacker in real time; (2) **Phishing kits with real-time OTP relay** — frameworks such as EvilginX (which saw a sharp increase in dark web references throughout 2024) that intercept OTPs during phishing sessions by proxying the victim's session to the legitimate service; (3) **Mobile malware with OTP interception** — Android RATs such as "xl-hook Android Banking Bot RAT" (offered by "churk" on XSS Forum, April 2025) and MaaS platforms like "PhantomOS" (offered by "Zero Compile" on XSS Forum, May 2025) that intercept OTPs via Android accessibility services or notification listeners; (4) **SS7/Diameter protocol exploitation** — interception of SMS-based OTPs via telecom signaling vulnerabilities, increasingly offered as-a-service on dark web forums. These techniques are particularly critical as enablers for digital wallet fraud (TP-0037), where intercepted OTPs are used to provision stolen cards into Apple Pay, Google Pay, or Samsung Pay for downstream contactless fraud.

**IC3 2025 Data:** The FBI IC3 2025 Internet Crime Report reported SIM swap losses declining to $17.4 million from 971 complaints (down from $26M/982 in 2024). The decline in losses may indicate improved carrier controls following FCC rule adoption, but SIM swap remains a high-impact technique for targeted attacks on high-value crypto accounts. The per-incident average remains significantly higher than most fraud categories, reflecting the targeted nature of attacks against crypto holders.

SIM swap attacks represent a critical intersection of telecommunications and financial fraud. The FCC adopted new rules in November 2023 requiring carriers to implement more robust customer authentication before processing SIM changes and port-out requests, but enforcement and adoption remain uneven. The threat has evolved beyond targeting individual consumers — organized groups now conduct bulk SIM swaps against high-value targets including cryptocurrency holders, corporate executives, and influencers. Court filings from DOJ prosecutions (e.g., the 2024 "Scattered Spider" cases) reveal that SIM swap capability is routinely sold as a service on Telegram for $300-$1,000 per swap, with carrier insiders sometimes complicit. The shift toward eSIM technology introduces new attack vectors (eSIM profile hijacking via compromised carrier accounts) while partially mitigating traditional physical SIM swap methods. Financial institutions should treat any account activity following a recent SIM change event — detectable via carrier APIs or SS7 monitoring services — as elevated risk requiring step-up authentication beyond SMS OTP.

## References

- FBI IC3 PSA: "SIM Swapping". [Link](https://www.ic3.gov/PSA/2022/PSA220208)
- DOJ: "Eight Individuals Charged in SIM Swap Conspiracy" (various indictments)
- Chainalysis: Crypto Crime Report (annual). [Link](https://www.chainalysis.com/blog/2025-crypto-crime-report-introduction/)
- FBI IC3: "2025 Internet Crime Report" — SIM swap: $17.4M in losses from 971 complaints (down from $26M/982 in 2024). [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)
- T-Mobile, AT&T carrier SIM swap prevention documentation

- "Organized fraud detection in 2026: a technical landscape report" — Specific fraud category detection: Synthetic identity fraud (SIM swap subsection)

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-12 | FLAME Project | Initial submission |
| 2026-02-28 | FLAME Project | v1.5 enrichment: added Stripe FT3 tactic mappings, Underground Ecosystem Context |
| 2026-03-04 | FLAME Project | Enhanced with Recorded Future 2025 intelligence — OTP interception techniques, TP-0037 cross-reference |
| 2026-04-06 | FLAME Project | FBI IC3 2025 enrichment — SIM swap losses declined to $17.4M (from $26M), possible carrier control improvement |
