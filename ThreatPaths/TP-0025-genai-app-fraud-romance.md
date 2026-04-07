# TP-0025: GenAI-Enhanced Authorized Push Payment Fraud — Romance Variant

```yaml
---
id: TP-0025
title: "GenAI-Enhanced Authorized Push Payment Fraud — Romance Variant"
category: ThreatPath
date: 2026-03-02
author: "FLAME Project"
source: "Original Research — multi-source intelligence compilation"
tlp: WHITE
sector:
  - banking
  - cross-sector
fraud_types:
  - authorized-push-payment
  - romance-scam
  - deepfake-fraud
  - social-engineering
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
mitre_attack:
  - T1566.001  # Phishing: Spearphishing Attachment
  - T1566.003  # Phishing: Spearphishing via Service
  - T1656      # Impersonation
  - T1657      # Financial Theft
  - T1589.002  # Gather Victim Identity Information: Email Addresses
  - T1583.001  # Acquire Infrastructure: Domains
  - T1585.001  # Establish Accounts: Social Media Accounts
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA005", "FTA006", "FTA007", "FTA009", "FTA010", "FT003", "FT006.001", "FT007.009", "FT016", "FT017", "FT028", "FT031", "FT052.003"]
mitre_f3: []                     # MITRE F3 (placeholder)
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Account Access"
  - "Defence Evasion"
  - "Perform Fraud"
  - "Monetization"
  - "Laundering"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 3"
  improve: "Level 4"
confidence_score: 72
source_reliability: B
info_credibility: 3
related_tps:
  - id: TP-0007
    relationship: shares-infrastructure
  - id: TP-0011
    relationship: escalates-from
  - id: TP-0026
    relationship: shares-infrastructure
regulatory_refs:
  - REG-AU-SPF
  - REG-DORA
  - REG-FCA-APP
  - REG-MAS-SRF
  - REG-UK-PSR-APP
  - REG-UNODC-ORGANIZED-FRAUD-2024
baseline_ids:
  - BL-0003
  - BL-0033
tags:
  - genai
  - deepfake
  - romance-scam
  - social-engineering
  - authorized-push-payment
  - voice-cloning
  - scam-compounds
  - pig-butchering
  - ai-chatbot
  - cross-border
  - unodc
  - unodc-organized-fraud-2024
---
```

---

## Summary

Threat actors leverage generative AI capabilities — including deepfake voice cloning, AI-generated profile imagery, and large language model-driven chatbots — to operate romance scam campaigns at unprecedented scale and sophistication. Unlike traditional romance scams that require skilled human operators for each victim relationship, GenAI-enhanced variants enable a single operator to maintain dozens of simultaneous romantic personas with consistent, emotionally intelligent conversations. The attack culminates in authorized push payments where the victim willingly transfers funds based on fabricated emotional bonds, with average losses of $64,000 per victim (FTC) making romance fraud the highest per-incident loss category among APP fraud types. The integration of deepfake voice and video into relationship grooming eliminates many of the traditional red flags (refusal to video call, inconsistent accents) that historically helped victims identify romance scams.

---

## Threat Path Hypothesis

> **Hypothesis**: Organized fraud operations — particularly those based in scam compound facilities in Southeast Asia — are deploying generative AI tools (voice cloning, face-swap deepfakes, LLM chatbots) to dramatically scale romance scam operations, enabling single operators to manage multiple victim relationships simultaneously with higher conversion rates and larger per-victim losses, resulting in authorized push payments that circumvent traditional fraud controls because the victim initiates the transactions themselves.

**Confidence**: High — based on law enforcement reporting (FBI IC3, Interpol), industry fraud data (UK Finance, FTC), and documented technical capabilities of commercially available GenAI tools.

**Estimated Impact**: $10,000 - $500,000+ per victim. Average loss per victim $64,000 (FTC 2024). UK APP fraud total GBP 450.7M with romance as the largest single category. Pindrop reports 1,300% increase in deepfake voice attempts against financial institutions.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Victim profiling via social media OSINT | Actors scrape dating platforms, social media profiles, and public records to identify targets based on vulnerability indicators: recent divorce/widowhood, geographic isolation, age demographics (45-65 overrepresented), and financial indicators (home ownership, professional titles). AI tools automate profile analysis at scale. | Automated scraping of dating platform profiles; bulk social media profile access patterns; OSINT tool usage targeting relationship-status and financial signals |
| CFPF-P1-002: AI-generated persona creation | Actors use generative AI to create synthetic romantic personas — face-swapped profile photos (often using stolen images of attractive individuals with AI modification to evade reverse image search), fabricated backstories generated by LLMs, and consistent personality profiles that can be maintained across extended conversations. | GAN-generated profile images (detectable via artifact analysis); profile photos with no reverse-image-search matches; dating profiles with unusually polished/consistent biographical narratives |
| CFPF-P1-003: Scam compound infrastructure setup | Organized operations establish physical scam compound facilities (documented in Myanmar, Cambodia, Laos, Philippines) with workstation-per-operator infrastructure, shared victim databases, and GenAI tooling deployed at organizational scale. Operations run as businesses with shift schedules, quotas, and specialization by victim demographic. | Law enforcement intelligence on scam compound locations; traffic analysis of communication infrastructure serving known compound regions; recruitment patterns for compound workers (often trafficking victims themselves) |
| CFPF-P1-004: Deepfake voice profile preparation | Actors prepare voice cloning models using 3-30 seconds of sample audio to create convincing voice profiles matching the persona's claimed identity (gender, age, accent, language). Commercial voice cloning services are available for $5-$300, enabling real-time voice conversion during phone and video calls. | N/A (preparation occurs offline using commercial GenAI tools) |

**Data Sources**: Dating platform abuse reports, social media platform integrity data, law enforcement intelligence on scam compound operations, deepfake detection services, reverse image search analytics.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Dating platform engagement | Actors initiate contact through dating applications (Tinder, Bumble, Hinge, Match.com) and social media platforms (Facebook, Instagram, LinkedIn) using AI-generated personas. Initial messages are crafted by LLMs to appear natural and contextually appropriate to the victim's profile. | Accounts with profile images flagged as potentially AI-generated; messaging patterns showing unnaturally rapid response times across multiple conversations; profiles with limited organic social connections |
| CFPF-P2-002: AI-maintained conversation grooming | LLM chatbots maintain extended romantic conversations with victims, calibrating emotional tone, mirroring the victim's communication style, and progressively building intimacy. A single operator can manage 20-80 simultaneous victim relationships by monitoring AI-generated responses and intervening only for critical decision points. | Messaging cadence patterns consistent with automated responses; conversation style analysis showing unusual linguistic consistency; communication volume exceeding human capacity for single sender |
| CFPF-P2-003: Deepfake voice and video verification | When victims request phone calls or video chats (a traditional red-flag check), actors deploy real-time deepfake voice cloning and face-swap video to satisfy the verification request. This eliminates the primary detection mechanism that historically protected victims from romance scams. | Audio artifacts in voice calls (latency, spectral anomalies); video artifacts in video calls (face boundary inconsistencies, lighting mismatches); victims reporting "something felt off" about calls but proceeding |
| CFPF-P2-004: Emotional dependency establishment | Over weeks to months, actors escalate emotional intimacy — declarations of love, future planning (marriage, relocation), and creation of perceived mutual financial obligations. GenAI enables consistent, emotionally intelligent escalation without the fatigue or inconsistency that limited human-operated romance scams. | Extended relationship duration before financial requests; progressive escalation patterns in communication intensity; victim isolation from friends/family advice |

**Target**: Consumer (individuals on dating platforms and social media)

**Data Sources**: Dating platform abuse detection systems, social media platform integrity reports, communication pattern analysis, deepfake audio/video detection tools, customer complaint narratives.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: Financial narrative construction | Actors introduce financial elements to the relationship — sharing fabricated stories of financial success (often crypto or investment themed), building trust through apparent financial transparency, and creating a framework where sending money feels like a natural extension of the relationship. | Victim accounts showing research into cryptocurrency or investment platforms suggested by the romantic interest; communication logs referencing financial topics with increasing frequency |
| CFPF-P3-002: Crisis fabrication for urgency | Actors create fabricated emergencies requiring immediate financial assistance — medical crises, legal problems, business emergencies, or travel complications. GenAI enables creation of convincing supporting artifacts (fake hospital documents, legal notices, travel itineraries). | Victim reports of partner's sudden emergencies; AI-generated documents with metadata inconsistencies; urgency patterns designed to bypass victim's rational evaluation |
| CFPF-P3-003: Payment method grooming | Actors gradually condition victims to use specific payment methods that maximize irrevocability and minimize institutional intervention — progressing from small gift cards to Zelle/Venmo, then to wire transfers, cryptocurrency, and ultimately direct bank transfers. | Progressive escalation in payment amounts and methods; shift from reversible to irrevocable payment channels; victim opening new financial accounts at the partner's suggestion |
| CFPF-P3-004: Isolation and counter-detection coaching | Actors preemptively counter fraud warnings by coaching victims on what banks will say ("they'll try to stop you because they don't understand our relationship"), normalizing secrecy from friends and family, and providing scripts for responding to bank staff questioning unusual transactions. | Victims providing coached responses to bank staff fraud inquiries; victims expressing pre-emptive defensiveness about transactions; social isolation patterns correlated with financial activity |

**Data Sources**: Customer interaction logs (call center narratives), transaction pattern analysis, communication metadata, social media activity changes, account opening records at suggested platforms.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Authorized push payment — crisis response | Victim initiates payments in response to fabricated emergencies. Payments are authorized by the victim themselves, passing all authentication and authorization controls. The victim is emotionally motivated and often resistant to bank intervention. | High-value payments to new recipients preceded by extended phone/messaging sessions; payments described as "helping a friend/partner"; customer insistence when challenged by bank staff |
| CFPF-P4-002: Progressive payment escalation | Initial payments are small (testing victim compliance), then rapidly escalate. Successful initial transfers are followed by increasingly larger requests, often with escalating urgency. The average romance scam involves 5-15 separate payment events over weeks to months. | Escalating payment amounts to the same recipient category; increasing frequency of payments over time; payments across multiple channels (Zelle, wire, crypto) to the same ultimate beneficiary |
| CFPF-P4-003: Multi-channel payment diversification | Actors direct victims to send payments through multiple channels simultaneously — wire transfers, Zelle, cryptocurrency purchases, gift cards, and direct bank transfers — to distribute the financial extraction across channels that may have independent monitoring. | Same victim making payments across multiple payment channels within compressed timeframe; diversification of payment methods for payments to related recipients; unusually complex payment behavior for the account's history |
| CFPF-P4-004: Deepfake-reinforced urgency | During the payment execution phase, actors deploy deepfake voice calls to maintain emotional pressure, using voice cloning to simulate crying, desperation, or fear that motivates the victim to complete transfers despite hesitation or bank warnings. | Phone calls immediately preceding or during payment sessions; victim emotional state observations by bank staff; payment attempts immediately following call activity |

**Data Sources**: Transaction monitoring systems, payment channel logs, call center interaction records (including emotional indicators), multi-channel payment correlation, customer behavioral analytics.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Mule account cascading | Funds from victim payments are received by first-layer mule accounts and immediately cascaded through multiple layers of mule infrastructure. Romance scam mule networks often overlap with money mule recruitment pipelines (victims of romance scams are themselves recruited as mules in a secondary exploitation). | Fan-out payment patterns from receiving accounts; mule accounts showing receive-and-forward behavior; accounts with thin transaction history suddenly processing large inbound transfers |
| CFPF-P5-002: Cryptocurrency conversion and mixing | Funds are converted to cryptocurrency through exchanges, peer-to-peer platforms, or Bitcoin ATMs, then processed through mixing services or cross-chain bridges to obfuscate the trail. | Transfers from mule accounts to cryptocurrency exchange deposit addresses; crypto purchases at ATMs following fund receipt; mixing service and cross-chain bridge activity |
| CFPF-P5-003: Cross-border repatriation | Funds are ultimately repatriated to the scam operation's base jurisdiction (often Southeast Asia) through hawala networks, underground money exchanges, or cryptocurrency-to-fiat conversion in jurisdictions with limited AML oversight. | International wire patterns to SE Asian jurisdictions from mule accounts; hawala-consistent transaction patterns; crypto-to-fiat conversion in high-risk jurisdictions |
| CFPF-P5-004: Scam compound revenue distribution | Within scam compound operations, extracted funds are distributed among compound operators, team leaders, and (minimally) the individual operators. The organizational structure mirrors legitimate business revenue sharing, with operators receiving a small percentage and the majority going to compound owners. | Law enforcement intelligence on compound financial structures; fund flow analysis tracing to known compound-associated accounts |

**Data Sources**: Mule account analytics, cryptocurrency blockchain analysis (Chainalysis, Elliptic, TRM Labs), international wire transfer monitoring, correspondent banking alerts, law enforcement intelligence sharing (Interpol, FBI IC3).

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA002: Social Engineering — core technique; AI-enhanced romantic manipulation driving authorized payments
- FTA003: Identity Fraud — synthetic persona creation using GenAI-generated images and backstories
- FTA005: Payment Fraud — victim-initiated authorized push payments across multiple channels
- FTA007: Money Laundering — mule network layering and cryptocurrency conversion
- FT016: Deepfake/Synthetic Media — voice cloning, face-swap video, AI-generated profile imagery
- FT028: Impersonation of Individual — fabricated romantic persona maintained via AI
- FT031: Payment Diversion — funds directed to actor-controlled accounts via emotional manipulation
- FT052.003: Romance Scam — primary fraud category

**MITRE ATT&CK:**

- T1585.001 (Establish Accounts: Social Media Accounts) — creation of fake dating and social media profiles
- T1566.003 (Phishing: Spearphishing via Service) — initial contact through dating platforms and social media
- T1656 (Impersonation) — sustained impersonation of fabricated romantic persona
- T1657 (Financial Theft) — extraction of funds through authorized push payments
- T1589.002 (Gather Victim Identity Information: Email Addresses) — OSINT collection for victim targeting
- T1583.001 (Acquire Infrastructure: Domains) — supporting infrastructure for fake investment platforms shown to victims

**Group-IB Fraud Matrix:**

- Reconnaissance: social media OSINT, dating platform scraping, victim vulnerability profiling
- Resource Development: AI persona creation, deepfake voice model training, scam compound setup, mule network pre-staging
- Trust Abuse: exploitation of romantic trust built over weeks/months of AI-maintained grooming
- End-user Interaction: sustained emotional manipulation via LLM chatbots, deepfake voice/video calls
- Defence Evasion: victim coaching against bank fraud warnings, payment channel diversification, isolation tactics
- Perform Fraud: authorized push payment initiation by the victim
- Monetization: mule account cascading, cryptocurrency conversion, gift card liquidation
- Laundering: cross-border fund repatriation, mixing services, hawala networks

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 4 (Execution)** or **post-Phase 5** — either when bank transaction monitoring flags unusual payment patterns, or (more commonly) when the victim themselves realizes they have been defrauded, often weeks or months after payments began. Romance scams have the longest average time-to-discovery of any fraud type because victims are emotionally invested in believing the relationship is genuine.

**Look Left** (what was missed before discovery):

- **P4 to P3**: Were there progressive payment escalation patterns that should have triggered behavioral alerts earlier? Did bank staff note coached responses during customer interactions that indicated social engineering?
- **P3 to P2**: Were there communication patterns (dating platform engagement, social media contact) that preceded the financial relationship? Dating platform abuse reports may contain early indicators.
- **P2 to P1**: Did the AI-generated persona leave detectable artifacts? Were the profile images flagged by reverse image search or GAN detection tools? Were there bulk account creation patterns on dating platforms from infrastructure associated with known scam compound regions?
- **Cross-team gap**: Consumer banking fraud teams see the payment anomalies. Platform trust & safety teams see the abusive accounts. Law enforcement sees the scam compound intelligence. AML sees the mule networks. No single team has visibility across the full chain without deliberate coordination.

**Look Right** (predicted next steps if uninterrupted):

- Victims will continue making payments until financial exhaustion or external intervention (family, bank, law enforcement)
- The same AI persona will be deployed against multiple victims simultaneously; identifying one victim should trigger a search for others
- Victims who have been fully extracted may be re-approached with "recovery scams" (fake law enforcement or recovery services offering to retrieve lost funds for a fee)
- Some victims will be recruited as money mules — the romantic relationship is leveraged to convince them to receive and forward funds from other fraud schemes
- Scam compound operations will iterate on GenAI capabilities, incorporating newer models with improved emotional intelligence and more convincing deepfake output

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Voice cloning provider | Real-time voice cloning as a service | High | $5-$300 per voice model |
| Face-swap deepfake provider | Real-time video face-swap for video calls | Medium-High | $50-$500 per session or subscription |
| LLM conversation manager | AI chatbot platforms configured for romance scam scripts | Medium | $100-$1,000 per month (platform access) |
| Profile image generator | GAN-generated dating profile images | High | $1-$10 per image batch |
| Scam compound operator | Full-service romance scam operation (facility, staff, tools) | Medium | Revenue share (60-80% to compound owners) |
| Mule network manager | Mule account recruitment, activation, and fund routing | High | 15-30% commission on funds processed |
| Document forger | AI-generated supporting documents (medical records, legal documents) | High | $20-$200 per document set |

### Tool Ecosystem
- Commercial voice cloning APIs (legitimate services repurposed for fraud) requiring only 3-30 seconds of sample audio
- Real-time face-swap applications enabling convincing video calls from mobile devices
- LLM-based chatbot platforms with romance scam conversation templates and emotional escalation playbooks
- GAN-based profile image generators producing unique faces that evade reverse image search
- Multi-account management tools for maintaining dozens of simultaneous victim conversations
- Translation APIs enabling cross-language romance scams (operators in one language targeting victims in another)

### Underground Marketplace Presence
- Telegram channels offering "romance scam kits" including AI persona packages, conversation scripts, and deepfake tooling
- Dark web forums with dedicated sections for romance scam methodology and victim "lead lists"
- Southeast Asian underground networks facilitating scam compound operations, worker recruitment, and revenue distribution
- Chinese-language forums with pig butchering methodology guides incorporating GenAI techniques
- Cryptocurrency-focused forums facilitating the monetization and laundering infrastructure

### Intelligence Sources
- FBI IC3 Annual Internet Crime Reports: romance fraud loss statistics and trend analysis
- FTC Consumer Sentinel Network: romance scam complaint data and demographic analysis
- Interpol: Operation Storm Makers (scam compound disruption), human trafficking intersection
- UK Finance: APP fraud statistics with romance scam category breakdown
- Pindrop: Voice intelligence research on deepfake voice attempt volumes and detection
- GASA (Global Anti-Scam Alliance): Scam compound mapping and victim support intelligence

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Dating platform intelligence sharing — participate in cross-platform abuse signal sharing to identify AI-generated personas at scale | Detective | Cyber Threat Intel / Partnerships |
| P1 | Customer education campaigns on AI-enhanced romance scams — specifically addressing deepfake voice/video capabilities that defeat traditional "request a video call" advice | Preventive | Customer Communications |
| P2 | Deepfake voice detection on inbound customer calls — deploy voice biometric and spectral analysis to identify AI-generated or cloned voices during call center interactions | Detective | Cyber / Fraud Ops |
| P2 | Partner with dating platforms for abuse signal exchange — flag accounts associated with known scam compound infrastructure | Detective | Cyber Threat Intel |
| P3 | Progressive payment pattern detection — alert on escalating payment amounts to new recipients over weeks/months, consistent with romance scam grooming timelines | Detective | Fraud Ops |
| P3 | Customer interaction analysis — NLP-based analysis of call center transcripts to identify coached responses and social engineering indicators in customer conversations | Detective | Fraud Ops |
| P3 | Scam warning interstitials — mandatory pause with contextual romance scam education before high-value payments to new recipients | Preventive | Payments / Product |
| P4 | Real-time payment intervention for suspected romance fraud — elevated review threshold for accounts exhibiting progressive payment escalation patterns | Detective | Fraud Ops |
| P4 | Trusted contact notification — with customer consent, notify a designated trusted contact when high-risk payment patterns are detected (similar to elder financial exploitation programs) | Preventive | Fraud Ops / Compliance |
| P4 | Dynamic payment delays — extended hold periods (24-72 hours) for first-time high-value payments to recipients in high-risk categories | Preventive | Payments |
| P5 | Mule account network detection — graph analytics on payment flows to identify mule infrastructure receiving funds from multiple romance fraud victims | Detective | AML / Fraud Ops |
| P5 | SAR filing with romance fraud typology indicators for FinCEN cross-referencing and law enforcement coordination | Responsive | AML / BSA |

### What Actually Worked

Industry reporting indicates that the most effective intervention for romance-variant APP fraud is the "branch-level welfare conversation" — when transaction monitoring flags suspected romance fraud patterns, a trained staff member conducts a non-judgmental conversation with the victim about the relationship context rather than simply blocking the payment. Institutions that implemented this approach report 40-60% victim self-identification rates (victims recognizing the scam during the conversation). This outperforms both automated payment blocks (which victims circumvent by moving to another channel) and generic fraud warnings (which coached victims dismiss). The key insight is that romance fraud intervention is fundamentally a welfare and safeguarding challenge, not just a transaction monitoring problem.

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Executive recognition of romance fraud as a customer welfare issue requiring specialized intervention procedures beyond standard transaction monitoring; budget allocation for deepfake detection capabilities |
| ASSESS | Level 3 (Established) | Comprehensive assessment of GenAI-enhanced social engineering risks including deepfake voice/video capabilities, LLM-driven conversation automation, and scam compound operational models |
| PLAN | Level 3 (Established) | Documented romance fraud intervention playbooks incorporating welfare conversation procedures, trusted contact notification protocols, and law enforcement referral pathways |
| ACT | Level 3 (Established) | Progressive payment pattern detection models, deepfake voice detection on customer calls, NLP analysis of call center transcripts for social engineering indicators, romance fraud-specific transaction scoring |
| MONITOR | Level 3 (Established) | Monitoring for romance fraud behavioral indicators (progressive payment escalation, coached customer responses, multi-channel payment diversification), deepfake attempt frequency tracking |
| REPORT | Level 3 (Established) | Romance fraud-specific SAR typology reporting, regulatory reporting on APP fraud losses by category, customer outcome reporting including successful intervention rates |
| IMPROVE | Level 4 (Advanced) | Continuous model refinement based on confirmed romance fraud cases and emerging GenAI capabilities; incorporation of new deepfake detection techniques as AI generation quality improves; adaptation of intervention procedures based on victim outcome data and evolving scam compound methodologies |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**Splunk — Progressive Payment Escalation to New Recipients (Phase 3-4)**

```spl
index=transactions payment_type IN ("wire", "zelle", "ach", "crypto_purchase")
| eval recipient_key=account_id."_".recipient_category
| sort 0 account_id _time
| streamstats count as payment_seq values(amount) as amount_history by recipient_key
| where payment_seq >= 3
| eval avg_amount=avg(amount_history)
| eval latest_amount=amount
| eval escalation_ratio=latest_amount/avg_amount
| where escalation_ratio > 1.5
| eval days_span=round((_time - min(_time))/86400, 1)
| where days_span > 7 AND days_span < 180
| table account_id, recipient_key, payment_seq, latest_amount, avg_amount, escalation_ratio, days_span
| sort - escalation_ratio
```

**Sigma — Multi-Channel Payment Diversification (Phase 4)**

```yaml
title: Multi-Channel Payments to Related Recipients - Romance Fraud Indicator
status: experimental
description: Detects accounts sending payments through multiple channels (wire, Zelle, crypto) to related recipients within a compressed timeframe, consistent with romance scam payment diversification.
logsource:
    product: payment_system
    service: transactions
detection:
    selection:
        payment_type:
            - 'wire'
            - 'zelle'
            - 'ach'
            - 'crypto_purchase'
            - 'gift_card'
    timeframe: 30d
    condition: selection | count(distinct payment_type) by account_id > 2 AND sum(amount) by account_id > 10000
level: high
tags:
    - fraud.romance_scam
    - fraud.app_fraud
    - cfpf.phase4.execution
```

**SQL — Coached Customer Response Detection (Phase 3)**

```sql
SELECT
    ci.account_id,
    ci.interaction_date,
    ci.interaction_type,
    ci.transcript_flags,
    t.total_payments_30d,
    t.total_amount_30d,
    t.distinct_recipients_30d
FROM call_center_interactions ci
JOIN (
    SELECT account_id,
           COUNT(*) as total_payments_30d,
           SUM(amount) as total_amount_30d,
           COUNT(DISTINCT recipient_id) as distinct_recipients_30d
    FROM transactions
    WHERE transaction_date > DATEADD(DAY, -30, GETDATE())
    GROUP BY account_id
) t ON ci.account_id = t.account_id
WHERE ci.transcript_flags LIKE '%coached_response%'
   OR ci.transcript_flags LIKE '%defensive_about_recipient%'
   OR ci.transcript_flags LIKE '%refused_fraud_education%'
ORDER BY t.total_amount_30d DESC;
```

### Behavioral Analytics

- **Progressive payment escalation modeling**: Build per-account models of normal payment behavior and flag sustained escalation patterns over 2-12 week periods, particularly to new recipient categories. Romance scams show a distinctive "ramp" pattern that differs from organic payment growth.
- **Communication-correlated payments**: Correlate payment activity with communication patterns (extended phone calls immediately preceding payments, messaging session duration before transfer initiation) to identify socially engineered payment events.
- **Multi-channel payment clustering**: Identify accounts using 3+ payment channels (wire, Zelle, crypto, gift cards) to the same or related recipient entities within 30-day windows — a strong romance fraud indicator as actors diversify extraction channels.
- **Deepfake voice detection**: Deploy spectral analysis and voice biometric scoring on inbound customer calls to identify AI-generated or cloned voices, particularly during calls where the customer is simultaneously initiating transactions.

### Cross-Team Correlation

- **Fraud to Cyber**: Deepfake detection signals from customer calls should feed into broader GenAI threat tracking, informing capabilities assessment of actor groups
- **Fraud to AML**: Romance fraud mule networks should be mapped as financial crime networks; mule accounts receiving funds from multiple romance fraud victims indicate coordinated infrastructure
- **Fraud to Law Enforcement**: Confirmed romance fraud cases with scam compound indicators should be referred to FBI IC3 and Interpol for cross-jurisdictional investigation
- **Fraud to Platform Trust & Safety**: Dating platform accounts associated with confirmed romance fraud should be reported back to platforms for takedown and pattern matching against other active accounts

---

## Operational Evidence

### EV-TP0025-2026-002: UNODC AI-Enhanced Romance and Investment Fraud Convergence

- **Source**: UNODC Organized Fraud Issue Paper (Vienna, 2024)
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: UNODC documents the convergence of romance fraud with AI-enabled capabilities and cryptocurrency investment fraud ("crypto-confidence investment fraud"). Key findings: (1) offenders establish intimate relationships then exploit trust to lure victims into fraudulent investment schemes; (2) this convergence widens the prospective pool to younger age groups; (3) introduces victims to unfamiliar crypto markets where fund tracing is difficult; (4) AI tools including voice clones and deepfakes enhance the impersonation and grooming phases. UNODC positions this convergence as a key emerging organized crime trend.

### EV-TP0025-2026-003: 2026 Technical Landscape — AI Phishing Effectiveness and Cialdini Persuasion Scoring

- **Source**: Organized fraud detection in 2026: a technical landscape report
- **CFPF Phase Coverage**: P1–P5
- **Confidence**: High
- **Summary**: LLM-generated phishing emails achieve 43–81% click-through rates versus 18–69% for traditional methods. For psychological manipulation scoring — directly applicable to romance fraud and social engineering detection — research quantifying Cialdini's six principles of persuasion (Reciprocity, Consistency, Social Proof, Authority, Liking, Scarcity) as numerical features improves phishing detection F1 by 2.62% when combined with BERT/SBERT embeddings. Most discriminative NLP features: urgency markers, authority indicators, sentiment manipulation, imperative verb frequency, financial trigger words, and semantic inconsistency. A context-aware system using Neural Chat 7B with LoRA achieves >97% accuracy predicting fraudulent intent within three conversational turns.

## References

- **FTC Consumer Sentinel Network (2024)**: Reports average romance scam victim loss of $64,000 per incident, with romance fraud as one of the highest per-incident loss categories.

- **UK Finance Annual Fraud Report (2024)**: Documents GBP 450.7M in APP fraud losses via Faster Payments, with romance scams as the single largest loss category.

- **Pindrop Voice Intelligence Report (2025)**: Reports 1,300% increase in deepfake voice fraud attempts against financial institutions, with voice cloning requiring as little as 3 seconds of sample audio.

- **FBI IC3 2024 Internet Crime Report**: Romance fraud and confidence schemes among top loss categories, with increasing AI enhancement documented. [Link](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf)

- **FBI IC3 2025 Internet Crime Report**: AI-enabled Romance/Confidence scams: $19M in losses, 626 complaints. Distress/grandparent scams using voice cloning technology to impersonate family members: $5M+ in losses. [Link](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)

- **FBI PSA250904** (September 4, 2025): ABA Foundation and FBI released deepfake scam infographic to help Americans identify deepfake-enabled fraud. [Link](https://www.ic3.gov/PSA/2025/PSA250904)

- **Interpol Operation Storm Makers II (2024)**: Cross-jurisdictional disruption of scam compound operations in Southeast Asia, documenting the industrial scale of romance scam operations.

- **FS-ISAC Cyber Fraud Prevention Framework (2025)**: Cross-functional investigation methodology applicable to romance fraud kill chain analysis. [Link](https://www.fsisac.com/hubfs/Knowledge/Fraud/CyberFraudPreventionFramework.pdf)

- INTERPOL, *Global Financial Fraud Threat Assessment*, 2nd Edition, March 2026 — documents Fraud-as-a-Service platforms powered by generative AI and LLMs enabling widespread adoption of cybercrime; platforms provide automated phishing websites, fake payment gateways, and bot-generated fake testimonials

- UNODC, "Organized Fraud — Issue Paper" (Vienna, 2024) — Chapter II, Crypto-confidence Investment Fraud; Chapter IV, Enabling Technology

- "Organized fraud detection in 2026: a technical landscape report" — LLMs and transformer models section

---

## Cross-References

- **TP-0011**: Romance Scam to Money Mule Recruitment Pipeline — foundational romance scam mechanics; this TP extends with GenAI enhancement layer
- **TP-0017**: Pig Butchering (Investment Scam) — overlapping actor infrastructure and scam compound operations; romance variant often transitions to investment solicitation
- **TP-0007**: Deepfake Voice Authorization for Wire Transfer — deepfake voice technology applied in romance context rather than institutional impersonation

## Detection Logic References

- **DL-0050**: Deepfake voice detection on inbound customer calls
- **DL-0051**: Progressive payment escalation pattern detection
- **DL-0052**: Multi-channel payment diversification alert
- **DL-0053**: Coached customer response NLP detection
- **DL-0054**: Communication-correlated payment timing analysis

---

## Analyst Notes

This threat path represents the convergence of two major trends in financial crime: the industrialization of romance scams through scam compound operations, and the democratization of deepfake and generative AI capabilities.

**GenAI as a force multiplier**: The traditional bottleneck in romance scam operations was the human operator — each victim relationship required a skilled social engineer investing weeks of personalized conversation. GenAI eliminates this constraint. LLM chatbots can maintain emotionally intelligent conversations 24/7 with consistent persona characteristics across dozens of simultaneous victims. Voice cloning at $5-$300 per model and face-swap deepfakes eliminate the primary detection mechanism (video call verification) that historically protected victims. Pindrop's reported 1,300% jump in deepfake voice attempts quantifies the scale of this shift.

**The authorized payment paradox**: Romance fraud is uniquely challenging for financial institutions because the victim is the threat actor from a technical perspective — they authenticate, they authorize, they confirm. Every traditional fraud control is designed to verify that the account holder is the one initiating the transaction, which in romance fraud, they are. This makes romance APP fraud fundamentally a social engineering and welfare problem, not a transaction monitoring problem. The most effective controls are those that interrupt the social engineering, not the payment.

**Scam compound operations**: The scale of scam compound operations in Southeast Asia is industrial. Facilities in Myanmar, Cambodia, and Laos employ hundreds of operators (many of whom are trafficking victims themselves) running romance scams as shift-based work. These operations are now deploying GenAI tools at organizational scale — centralized LLM platforms managing conversation flows, shared deepfake tooling, and standardized escalation playbooks. The intersection of human trafficking and financial fraud creates both a moral imperative and a practical intelligence opportunity for financial institutions.

**Average loss severity**: The FTC's reported average of $64,000 per romance scam victim makes this the highest per-incident loss among APP fraud categories. Victims often exhaust savings, take out loans, and liquidate retirement accounts. The financial devastation is compounded by psychological trauma and social stigma that prevents reporting — estimated reporting rates for romance fraud are 5-15% of actual incidents, meaning true losses are significantly higher than official statistics suggest.

**Detection arms race**: As GenAI capabilities improve, the artifacts that current deepfake detection tools rely on (spectral anomalies in voice, face boundary artifacts in video) will become increasingly subtle. Institutions investing in deepfake detection must plan for continuous model retraining and should not rely exclusively on technical detection — behavioral analytics (payment patterns, communication correlation) provide more durable detection signals.

**IC3 2025 Data — AI-Enabled Romance Fraud:** The FBI IC3 2025 Internet Crime Report introduced a new AI-related fraud tracking category. AI-enabled romance/confidence scams accounted for $19M in losses from 626 complaints. Distress/grandparent scams using voice cloning technology to impersonate family members generated $5M+ in losses. PSA250904 (September 4, 2025) saw the ABA Foundation and FBI release a deepfake scam infographic to help Americans identify deepfake-enabled fraud. These figures likely represent significant underreporting given the difficulty of attributing AI enhancement in victim reports.

**INTERPOL 2026 Update — FaaS Enablement**: INTERPOL confirms that "Fraud-as-a-Service" platforms powered by generative AI and large language models have enabled low-skill actors to launch professional-grade romance-variant APP campaigns with minimal effort. These platforms provide ready-made tools including automated phishing websites, fake payment gateways, and bot-generated fake testimonials that mimic legitimate communications. See TP-0054 for the full FaaS platform threat path. The democratization of these tools means that romance APP campaigns are no longer limited to sophisticated criminal organizations — individual actors with subscription access can now execute campaigns previously requiring teams.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-02 | FLAME Project | Initial submission |
| 2026-03-17 | FLAME Project | INTERPOL GFFTA 2026 enrichment — FaaS platform enablement of romance APP campaigns |
| 2026-04-06 | FLAME Project | FBI IC3 2025 enrichment — AI-enabled romance fraud $19M losses, voice cloning grandparent scams, PSA250904 deepfake infographic |
