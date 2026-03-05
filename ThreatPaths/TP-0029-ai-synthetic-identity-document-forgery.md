# TP-0029: AI Synthetic Identity & Document Forgery

```yaml
---
id: TP-0029
title: "AI Synthetic Identity & Document Forgery"
category: ThreatPath
date: 2026-03-04
author: "FLAME Project"
source: "https://www.federalreserve.gov/newsevents/pressreleases/bcreg20240715a.htm"
tlp: WHITE
sector:
  - banking
  - fintech
fraud_types:
  - synthetic-identity
  - ai-document-fraud
  - new-account-fraud
  - application-fraud
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
mitre_attack:
  - T1585.001  # Establish Accounts: Social Media Accounts
  - T1588.005  # Obtain Capabilities: Exploits
  - T1656      # Impersonation
  - T1657      # Financial Theft
  - T1204      # User Execution
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT003", "FT005.001", "FT006.001", "FT007.009", "FT008.002", "FT016", "FT017", "FT028"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Credential Access"
  - "Account Access"
  - "Perform Fraud"
  - "Monetization"
  - "Laundering"
ucff_domains:
  commit: "Level 3"
  assess: "Level 4"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 4"
  report: "Level 3"
  improve: "Level 4"
confidence_score: 68
source_reliability: C
info_credibility: 2
related_tps:
  - id: TP-0003
    relationship: escalates-from
  - id: TP-0015
    relationship: related-to
regulatory_refs:
  - REG-FINCEN-CDD
tags:
  - ai-generated
  - synthetic-identity
  - document-forgery
  - deepfake
  - kyc-bypass
  - onlyfake
  - prokyc
  - behavioral-biometrics
  - new-account-fraud
  - bust-out
  - credit-farming
---
```

---

## Summary

Threat actors are leveraging generative AI to produce high-fidelity forged identity documents, synthetic facial images, and behavioral biometric mimicry to bypass KYC/identity verification controls at scale. Digital document forgery surpassed physical forgery in 2024, reaching 57% of all detected forgeries (a 244% increase), while AI-generated document fraud overall increased 311%. Underground services like OnlyFake and ProKYC have democratized access to convincing forged IDs, selfie-matching images, and video-based liveness check bypasses for as little as $30 per identity package. Combined with traditional synthetic identity techniques (CPN/SSN manipulation, credit farming), AI-enabled document forgery represents an evolution that threatens to overwhelm current identity verification defenses. The Federal Reserve Board estimates synthetic identity fraud generates $6B+ in annual losses to the US financial system.

---

## Threat Path Hypothesis

> **Hypothesis**: Financially motivated actors are using generative AI tools and underground document forgery services to create high-fidelity synthetic identity packages -- including forged government IDs, AI-generated facial images, deepfake liveness videos, and behavioral biometric mimicry -- to bypass KYC verification controls at banking and fintech institutions, establish fraudulent accounts, build creditworthiness through credit farming, and execute bust-out schemes or application fraud at scale.

**Confidence**: High -- based on Entrust 2025 Identity Fraud Report (311% increase in AI document fraud), Federal Reserve Board synthetic identity research ($6B+ annual losses), Trend Micro underground market research (KYC bypass pricing), and documented law enforcement disruptions of forgery services.

**Estimated Impact**: $5,000 -- $200,000+ per synthetic identity at bust-out. Aggregate losses from synthetic identity fraud exceed $6B annually (FRB estimate). AI-enabled forgery tools reduce per-identity creation cost to under $30, enabling industrial-scale production.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: PII harvesting for synthetic identity construction | Actors acquire real SSNs (often belonging to children, elderly, immigrants, or deceased individuals with minimal credit history), then combine them with fabricated name, date of birth, and address to construct a synthetic identity that passes initial validation checks. | SSN-name mismatches in credit bureau inquiries; credit file creation for SSNs with no prior history; SSNs associated with age ranges inconsistent with the application (child SSNs with adult applicants) |
| CFPF-P1-002: AI document forgery service procurement | Actors access underground document forgery services (e.g., OnlyFake, ProKYC, and successors) that generate photo-realistic government identity documents using generative AI. Services produce driver's licenses, passports, and national IDs for any jurisdiction, complete with holograms, microprint simulation, and barcode data. | Underground market listings for document forgery services; pricing tiers for standard ($30) versus exchange-specific ($180-$200) KYC packages; service advertisements targeting cryptocurrency exchange and fintech onboarding |
| CFPF-P1-003: Biometric attack tool acquisition | Actors procure deepfake video generation tools, AI-generated selfie services, and behavioral biometric mimicry software (e.g., Herodotus malware) that can simulate human-like mouse movements, typing cadence, and device interaction patterns to defeat behavioral analytics. | Underground market listings for liveness check bypass tools; deepfake video generation services targeting specific KYC platforms; behavioral biometric spoofing software advertisements |

**Data Sources**: Underground market monitoring, threat intelligence feeds, document forgery service disruption reports, biometric vendor threat assessment publications, law enforcement disruption press releases.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: AI-forged document KYC submission | Actors submit AI-generated identity documents during account opening or KYC verification processes. Documents are tailored to specific institution requirements and may include matching selfie images generated by the same AI pipeline. | Document image metadata indicating AI generation (texture anomalies, font inconsistencies, edge artifacts); identical document templates appearing across multiple applications; documents passing automated checks but failing manual review |
| CFPF-P2-002: Deepfake liveness verification bypass | Actors use real-time deepfake video to pass video-based liveness checks during KYC onboarding. Pre-recorded deepfake videos or real-time face-swap applications defeat challenges requiring head turns, blinking, or phrase repetition. | Liveness check sessions with unusual video compression artifacts; facial rendering inconsistencies during motion challenges; identical facial geometry appearing across separate applications; device fingerprints associated with multiple distinct identities |
| CFPF-P2-003: Behavioral biometric spoofing | Malware such as Herodotus injects human-like behavioral patterns (mouse movements, typing rhythm, scroll behavior) into automated sessions, defeating behavioral biometric systems that distinguish human users from bots. | Behavioral biometric profiles that match known spoofing patterns; sessions showing statistically improbable consistency in behavioral metrics; device-level indicators of injection frameworks |

**Target**: Institution (banking and fintech KYC/onboarding systems)

**Data Sources**: KYC platform submission logs, document verification system audit trails, liveness check session recordings, behavioral biometric analytics platforms, device fingerprinting systems, application fraud databases.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: Credit file establishment | After successful account opening, actors use the synthetic identity to establish a credit file at the major credit bureaus. Initial activity may include becoming an authorized user on an existing account (credit piggybacking) or securing a small secured credit card. | New credit files with thin history; authorized user additions from unrelated primary cardholders; secured credit card applications with minimal deposit amounts |
| CFPF-P3-002: Credit farming / seasoning | Actors systematically build creditworthiness over 6-24 months through responsible payment behavior, gradual credit limit increase requests, and diversification of credit products. This "credit farming" phase establishes the trust profile needed for high-value bust-out. | Synthetic identities with unusually linear credit score trajectories; accounts showing textbook-perfect payment patterns with no behavioral variation; multiple credit products opened in rapid succession after score thresholds are reached |
| CFPF-P3-003: Multi-institution account proliferation | Using the established credit profile, actors open accounts at multiple financial institutions simultaneously, positioning for coordinated bust-out across all accounts. | Credit inquiries from multiple institutions within short time windows; new account openings across diverse institution types (banks, credit unions, fintech lenders); address and phone numbers shared across applications at different institutions |

**Data Sources**: Credit bureau inquiry logs, authorized user addition records, credit score trajectory analytics, multi-institution application correlation databases, identity network analysis tools.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Coordinated bust-out | After credit limits have been maximized across multiple accounts, actors simultaneously max out all credit lines -- cash advances, balance transfers, point-of-sale purchases of resalable goods -- and abandon the synthetic identity. | Simultaneous credit utilization spike across multiple accounts with shared identity elements; cash advance maximization within days; purchases concentrated in easily resalable categories (electronics, gift cards) |
| CFPF-P4-002: Application fraud (instant credit) | Actors use AI-forged identity packages to apply for and immediately draw on instant credit products -- buy-now-pay-later, personal loans, or credit cards with instant virtual card issuance -- without the credit farming phase. | Multiple instant credit applications from same device fingerprint or IP range; applications with AI-generated documents passing automated checks; immediate max utilization of newly issued credit |
| CFPF-P4-003: Account takeover amplification | Actors combine synthetic identity infrastructure with account takeover of existing legitimate accounts, using AI-forged documents to pass re-verification challenges and identity restoration processes. | Identity verification challenges answered with AI-generated documents; document submissions during account recovery processes showing forgery indicators; existing accounts showing sudden behavioral changes after identity re-verification |

**Data Sources**: Transaction monitoring systems, credit utilization analytics, application fraud scoring models, device fingerprinting correlation, cross-institutional identity verification databases.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Goods resale laundering | Products purchased during bust-out (electronics, luxury goods, gift cards) are resold through online marketplaces, pawn shops, or fencing networks. | High-volume resale activity on marketplace platforms from newly created seller accounts; bulk gift card liquidation; electronics resale at below-market prices |
| CFPF-P5-002: Cash advance extraction | Cash advances and balance transfers are extracted to bank accounts controlled by the actor, then moved through mule networks or converted to cryptocurrency. | Cash advances deposited to accounts with no prior relationship to the cardholder; rapid crypto conversion of cash advance proceeds; mule account patterns associated with synthetic identity accounts |
| CFPF-P5-003: Cryptocurrency exit | Funds are converted to cryptocurrency through exchanges where the actor has also bypassed KYC using AI-forged documents, creating a closed ecosystem of fraudulent identities across financial and crypto platforms. | Crypto exchange accounts opened with documents matching known forgery service templates; rapid conversion of fiat deposits to privacy coins; cross-platform identity linkage between banking fraud and crypto exchange accounts |

**Data Sources**: Marketplace seller analytics, gift card liquidation tracking, cash advance destination account analysis, cryptocurrency exchange KYC verification logs, blockchain analysis tools, cross-platform identity correlation.

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001 (Fraud Enablement) -- AI forgery services and PII harvesting enable synthetic identity creation at scale
- FTA005 (Identity Fraud) -- Core technique: synthetic identity construction and deployment
- FTA006 (Document Fraud) -- AI-generated forged government IDs, selfies, and supporting documents
- FTA003 (Account Compromise) -- ATO amplification using forged re-verification documents
- FTA007 (Payment Fraud) -- Bust-out execution, instant credit exploitation
- FTA009 (Money Laundering) -- Goods resale, crypto conversion, mule network utilization
- FT003 (Bot Activity) -- Automated application submission with behavioral biometric spoofing
- FT005.001 (Synthetic Identity) -- Primary fraud type: constructed identities combining real and fabricated PII
- FT006.001 (Document Forgery) -- AI-generated identity documents as KYC bypass mechanism
- FT008.002 (Liveness Bypass) -- Deepfake video and face-swap for liveness check defeat

**MITRE ATT&CK:**

- T1585.001 (Establish Accounts: Social Media Accounts) -- Creation of social media and online presence to support synthetic identity credibility
- T1588.005 (Obtain Capabilities: Exploits) -- Procurement of AI forgery tools, deepfake software, and behavioral biometric spoofing malware
- T1656 (Impersonation) -- Impersonation of non-existent individuals through synthetic identity packages
- T1657 (Financial Theft) -- Bust-out execution and application fraud resulting in direct financial loss
- T1204 (User Execution) -- Manipulation of KYC verification workflows through forged document submission

**Group-IB Fraud Matrix:**

- Reconnaissance -- PII harvesting, SSN acquisition for synthetic identity base
- Resource Development -- AI forgery service procurement, deepfake tool acquisition, behavioral biometric spoofing malware deployment
- Trust Abuse -- Exploitation of KYC verification trust, credit bureau trust in identity data
- End-user Interaction -- KYC document submission, liveness check participation (with deepfakes)
- Credential Access -- Credit file establishment through synthetic identity
- Account Access -- Multi-institution account opening using forged credentials
- Perform Fraud -- Bust-out execution, application fraud, instant credit exploitation
- Monetization -- Goods resale, cash advance extraction
- Laundering -- Crypto conversion, mule networks, cross-platform laundering

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 4 (Execution)** during bust-out, when credit utilization spikes trigger transaction monitoring alerts, or at **Phase 2** when document verification systems detect forgery indicators. Increasingly, discovery occurs post-loss during **Phase 5** charge-off analysis when credit bureaus identify the identity was synthetic.

**Look Left** (what was missed before discovery):

- **P4 -> P3**: Was the credit farming pattern detectable? Synthetic identities show unnaturally consistent credit behavior -- no late payments, no usage variation, steady linear score growth. This "too perfect" pattern is itself an indicator.
- **P3 -> P2**: Did the KYC verification process flag any anomalies in the submitted documents? Were document metadata, facial image provenance, or behavioral biometric baselines analyzed beyond automated pass/fail?
- **P2 -> P1**: Were the SSNs used in synthetic identity construction associated with known compromise events? Were there credit bureau inquiries for SSNs with no prior history that should have triggered enhanced verification?
- **Cross-team gap**: KYC/onboarding teams, credit risk teams, and fraud operations often operate with separate data systems. A document flagged as marginal during onboarding may not inform the credit risk model, and credit farming patterns visible to the credit team may not trigger fraud investigation.

**Look Right** (predicted next steps if uninterrupted):

- Actors will execute coordinated bust-out across all accounts within a 48-72 hour window once credit limits are maximized
- Same AI forgery infrastructure will be reused to generate additional synthetic identities, creating parallel identity networks
- Goods purchased during bust-out will appear on resale platforms within days
- Actors will use the same KYC bypass techniques to open cryptocurrency exchange accounts for monetization, creating a closed laundering loop
- As detection capabilities improve for current AI forgery techniques, actors will rapidly adopt next-generation models with higher fidelity

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Document Forgery Service | AI-generated government IDs (driver's license, passport) | High | $30 standard; $180-$200 exchange-specific |
| Selfie/Liveness Bypass Service | AI-generated selfies and deepfake video for KYC | High | $15-$50 per image; $100-$300 per liveness video |
| SSN Vendor | Real SSNs (children, deceased, immigrants) for synthetic identity base | High | $1-$10 per SSN; $50+ for "clean" SSNs with no credit history |
| Credit Piggybacking Service | Authorized user tradeline additions for credit building | Medium | $200-$1,500 per tradeline |
| Behavioral Biometric Spoofing | Herodotus and similar malware mimicking human interaction patterns | Low-Medium | $500-$2,000 per license |
| Fullz Package Vendor | Complete synthetic identity packages (SSN + forged docs + selfie + credit history) | Medium | $200-$1,000 per complete identity |

### Tool Ecosystem
Generative AI document creation platforms (OnlyFake successors), deepfake face-swap applications (real-time and pre-recorded), anti-detect browsers for managing multiple synthetic identity sessions, residential proxy networks for geographic IP matching, behavioral biometric injection frameworks (Herodotus and variants), credit monitoring tools for tracking synthetic identity credit file maturation, virtual phone number services for application verification.

### Underground Marketplace Presence
AI document forgery services are widely advertised on Telegram channels, dark web marketplaces, and specialized fraud forums. The market has stratified into tiers: commodity services producing basic forged documents for $30, mid-tier services offering platform-specific KYC packages ($180-$200 for exchange-specific documents including matched selfies), and premium services offering full synthetic identity packages with credit history and behavioral biometric profiles. Russian-language carding forums and English-language fraud Telegram channels are primary distribution vectors. The disruption of OnlyFake in early 2024 led to rapid proliferation of successor services, demonstrating the resilience of the underground ecosystem.

### Intelligence Sources
- Entrust Identity Fraud Report (annual publication; documents digital vs. physical forgery trends)
- Federal Reserve Board Synthetic Identity Fraud Mitigation toolkit
- Trend Micro research on underground KYC bypass markets
- 404 Media and WIRED reporting on OnlyFake and ProKYC disruptions
- Recorded Future and Flashpoint reporting on AI-enabled fraud tooling evolution

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Monitor underground markets for AI document forgery services targeting specific institution templates | Detective | Cyber Threat Intel |
| P1 | Implement SSN validation against death records, minor age ranges, and known synthetic identity patterns (eCBSV integration) | Preventive | KYC / Onboarding |
| P2 | Deploy multi-layered document verification: automated checks + AI-forgery-specific detection models + selective manual review for flagged submissions | Preventive | KYC / Identity Verification |
| P2 | Implement injection attack detection for liveness checks: detect virtual cameras, face-swap software, and video injection frameworks | Preventive | Identity Verification / Cybersecurity |
| P2 | Deploy behavioral biometric analysis with spoofing detection capabilities calibrated against known injection tools (Herodotus patterns) | Detective | Fraud Ops / Cybersecurity |
| P3 | Credit file monitoring for synthetic identity indicators: thin files with rapid credit building, authorized user patterns from unrelated primaries, no negative data | Detective | Credit Risk / Fraud Ops |
| P3 | Cross-institutional identity verification: participate in consortium-based synthetic identity detection (e.g., FRB synthetic identity utility) | Detective | Fraud Ops / Industry Consortium |
| P4 | Bust-out prediction models: flag accounts showing credit farming patterns + approaching credit limit maximization + behavioral consistency indicators | Detective | Credit Risk / Fraud Ops |
| P4 | Real-time transaction monitoring for bust-out signatures: sudden utilization spike, cash advance concentration, resalable goods purchases | Detective | Fraud Ops |
| P5 | Coordinate with law enforcement on forged document service takedowns and prosecution | Responsive | Legal / Law Enforcement Liaison |
| P5 | SAR filing with synthetic identity indicators for FinCEN cross-referencing and trend analysis | Responsive | AML / BSA |

### What Actually Worked

Per Federal Reserve Board guidance and industry reporting: **multi-layered identity verification** combining automated document authentication, AI-specific forgery detection models, and selective human review has been the most effective defense against AI-generated documents. Institutions that deployed injection attack detection for liveness checks (detecting virtual cameras and face-swap software rather than relying solely on the biometric match) significantly reduced deepfake bypass rates. On the credit farming side, consortium-based synthetic identity detection -- where multiple institutions share identity signals to identify cross-institutional patterns -- has proven effective at catching synthetic identities during the positioning phase before bust-out.

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate for AI-specific fraud countermeasures; budget allocation for identity verification technology refresh; participation in industry synthetic identity detection consortia |
| ASSESS | Level 4 (Advanced) | Continuous assessment of AI forgery tool capabilities versus current detection controls; red team exercises using commercially available forgery services against own KYC pipeline; vulnerability assessment of liveness check and behavioral biometric systems |
| PLAN | Level 3 (Established) | AI forgery countermeasure roadmap; identity verification vendor evaluation framework incorporating AI-specific threat scenarios; synthetic identity detection rule development plan |
| ACT | Level 4 (Advanced) | Multi-layered document authentication with AI forgery detection models; injection attack detection for liveness checks; behavioral biometric spoofing detection; cross-institutional synthetic identity signals; bust-out prediction models |
| MONITOR | Level 4 (Advanced) | Continuous monitoring of AI forgery tool evolution; synthetic identity credit farming pattern detection; cross-platform identity correlation; underground market intelligence on new forgery services and bypass techniques |
| REPORT | Level 3 (Established) | SAR filing with synthetic identity typology indicators; FinCEN 314(b) information sharing on synthetic identity networks; regulatory reporting on AI forgery detection rates and control effectiveness |
| IMPROVE | Level 4 (Advanced) | Rapid iteration cycle for identity verification models as AI forgery capabilities evolve; post-incident analysis incorporating forgery tool identification; detection model retraining on newly discovered forgery techniques; vendor performance benchmarking against emerging threats |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**Splunk -- Synthetic Identity Credit Farming Pattern Detection (Phase 3)**

```spl
index=credit_bureau sourcetype=credit_file_events
| eval file_age_months=round((now() - strptime(file_creation_date, "%Y-%m-%d")) / 86400 / 30, 0)
| where file_age_months <= 24
| stats
    count(eval(event_type="payment")) as payment_count,
    count(eval(event_type="late_payment")) as late_payment_count,
    count(eval(event_type="new_account")) as new_accounts,
    count(eval(event_type="auth_user_add")) as auth_user_additions,
    max(credit_score) as current_score,
    min(credit_score) as initial_score
    by ssn, identity_name
| eval score_velocity=(current_score - initial_score) / file_age_months
| where late_payment_count=0 AND payment_count > 12 AND score_velocity > 25 AND new_accounts >= 3
| table ssn, identity_name, file_age_months, payment_count, late_payment_count, new_accounts, auth_user_additions, current_score, score_velocity
| sort - score_velocity
```

**Sigma -- AI-Generated Document Submission Detection (Phase 2)**

```yaml
title: KYC Document Submission with AI Forgery Indicators
status: experimental
description: Detects identity document submissions during KYC onboarding that exhibit AI generation artifacts including metadata anomalies, texture inconsistencies, and template matching against known forgery services.
logsource:
    product: identity_verification
    service: document_check
detection:
    selection:
        verification_type: "document_upload"
    forgery_indicators:
        - ai_forgery_score|gte: 0.7
        - metadata_anomaly: true
        - template_match|contains:
            - 'onlyfake'
            - 'prokyc'
            - 'known_forgery_template'
    condition: selection and 1 of forgery_indicators
level: critical
tags:
    - cfpf.phase2.initial_access
    - ai.document_forgery
    - synthetic_identity
```

### Behavioral Analytics

- **Credit trajectory anomaly detection**: Synthetic identities exhibit unnaturally smooth credit score trajectories with zero deviations. Model the expected variance in legitimate credit behavior and flag identities with suspiciously low variance over their credit history lifecycle
- **Cross-platform identity correlation**: Correlate identity signals across banking, fintech, and cryptocurrency platforms to detect the same synthetic identity or AI-generated facial image appearing in KYC submissions at multiple institutions
- **Document provenance analysis**: Beyond content analysis of submitted documents, examine submission metadata (device fingerprint, upload timing, image compression characteristics) to identify batch submissions from forgery service pipelines
- **Liveness session forensics**: Analyze video liveness check sessions for deepfake artifacts including temporal inconsistencies, facial boundary artifacts, and unnatural lighting responses during challenge prompts

### Cross-Team Correlation

- **KYC/Onboarding -> Fraud**: Document verification results (forgery scores, metadata anomalies, liveness check confidence levels) should feed into account risk scoring models, not just binary pass/fail onboarding decisions
- **Fraud -> Cyber Threat Intel**: Identified forgery service templates and deepfake tool signatures should be shared with CTI for underground market monitoring and law enforcement coordination
- **Credit Risk -> Fraud**: Credit farming behavioral patterns (zero-deviation trajectories, rapid account proliferation) should trigger fraud investigation rather than being treated purely as credit risk signals
- **Industry Consortium -> Individual Institution**: Synthetic identity signals from consortium databases (FRB utility, GIACT, LexisNexis) should be integrated into onboarding and ongoing monitoring workflows

---

## References

- **Entrust 2025 Identity Fraud Report**: Documents 311% increase in AI-generated document fraud and the crossover point where digital forgery surpassed physical forgery at 57% of all detected cases (244% increase from prior year).

- **Federal Reserve Board -- Synthetic Identity Fraud Mitigation**: FRB research estimating $6B+ in annual synthetic identity fraud losses to the US financial system, with guidance on detection methodologies and industry collaboration frameworks.

- **Trend Micro -- Underground KYC Bypass Market Research**: Documents pricing and availability of KYC bypass services, including standard packages (~$30) and platform-specific packages ($180-$200 for Binance-specific verification).

- **OnlyFake and ProKYC Service Disruptions**: Media and law enforcement reporting on the disruption of major AI document forgery services, documenting their operational models, pricing structures, and the rapid emergence of successor services.

- **Herodotus Malware Analysis**: Security research documenting behavioral biometric spoofing malware that mimics human interaction patterns (mouse movements, typing cadence, scroll behavior) to defeat behavioral analytics.

- **LexisNexis Risk Solutions — Global State of Fraud and Identity Report 2026**: AI-generated forgery statistics, deepfake detection rates, dark web user growth, enterprise AI risk disclosure trends.

---

## Analyst Notes

This threat path represents the most rapidly evolving area of financial fraud. Several critical observations:

**The arms race is accelerating**: The 311% year-over-year increase in AI document fraud reflects a fundamental shift. Previous document forgery required physical skill and specialized equipment. AI forgery services have reduced the barrier to entry to a $30 purchase and a web browser. The quality gap between AI-generated and genuine documents is narrowing faster than detection capabilities are improving.

**Digital surpassed physical**: The Entrust finding that 57% of detected forgeries are now digital (versus physical) is a watershed moment. Institutions that invested heavily in physical document security features (holograms, watermarks, microprint) are now defending against a different attack surface entirely. The shift demands a parallel shift in verification approach -- from physical feature authentication to AI-provenance detection and multi-signal identity validation.

**The Herodotus problem**: Behavioral biometrics were positioned as the "silver bullet" against automated fraud -- if a session shows human-like interaction patterns, it must be a real human. Herodotus and similar tools undermine this assumption by injecting human-mimicking behavioral patterns into automated sessions. This doesn't mean behavioral biometrics are useless, but they can no longer be treated as a standalone signal.

**Cross-references**: TP-0003 (Synthetic Identity Bust-Out) covers the traditional synthetic identity lifecycle without AI-enhanced document forgery. TP-0018 (AI-Enabled Fraud) provides broader context on AI applications in financial crime. This threat path focuses specifically on the convergence of AI document forgery with synthetic identity techniques, representing the next evolution of both categories.

**Regulatory attention**: FinCEN, the FRB, and OCC are actively developing guidance on AI-specific fraud controls. Institutions without demonstrable AI forgery detection capabilities will face increasing regulatory scrutiny as the threat becomes a supervisory priority.

### AI Fraud Arms Race Escalation — LNRS 2026

The arms race between "good AI" and "bad AI" is accelerating. An estimated 85% of identity fraud cases involve generative AI tools, while a study revealed that people correctly spot deepfakes only 20% of the time. In 2021, virtually no forged documents were AI-generated; by 2024, AI-generated forgeries were involved in 57% of attacks.

A fraudster recently scammed $20 million from Brazilian financial institutions using multiple deepfake accounts. On the dark web, 4.6 million users accessed it daily in 2025 (up from 3M in 2024), with KYC-as-a-service packages available for $500-$800.

Enterprise awareness is rising: 72% of S&P 500 companies disclosed material AI risk in 2025, up from just 12% in 2023. Meanwhile, 88% of senior executives plan to increase AI budgets specifically for agentic AI, signaling both defensive investment and recognition of the AI agent attack surface.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-02 | FLAME Project | Initial submission |
