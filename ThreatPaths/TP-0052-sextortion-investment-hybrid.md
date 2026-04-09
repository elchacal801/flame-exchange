# TP-0052: Sextortion-Investment Hybrid Fraud

```yaml
---
id: TP-0052
title: "Sextortion-Investment Hybrid Fraud"
category: ThreatPath
date: 2026-03-17
author: "FLAME Project"
source: "INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - sextortion
  - investment-scam
  - deepfake
  - social-engineering
  - romance-scam
sector:
  - banking
  - crypto
  - investment
  - cross-sector
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
confidence_score: 78
source_reliability: B
info_credibility: 2
mitre_attack:
  - T1566.003  # Phishing: Spearphishing via Service
  - T1589.001  # Gather Victim Identity: Credentials
  - T1656       # Impersonation
  - T1657       # Financial Theft
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FT016"]
mitre_f3: ["F1020.001", "F1018", "F1025", "F1031", "F1032", "F1040", "T1598", "T1660"]
groupib_stages:
  - "Reconnaissance"
  - "Social Engineering"
  - "Resource Development"
  - "Initial Access"
  - "End-user Interaction"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 2"
  assess: "Level 3"
  plan: "Level 2"
  act: "Level 3"
  monitor: "Level 3"
  report: "Level 2"
  improve: "Level 2"
related_tps:
  - id: TP-0011
    relationship: related-to
  - id: TP-0017
    relationship: enhances
  - id: TP-0025
    relationship: enhances
  - id: TP-0026
    relationship: enhances
regulatory_refs:
  - REG-CFPB-REGE
  - REG-FINCEN-AML
  - REG-INTERPOL-GFFTA
baseline_ids:
  - BL-0003
  - BL-0004
geopolitical_timing: none
nation_state_nexus: none
tags:
  - sextortion
  - investment-fraud
  - deepfake-imagery
  - romance-baiting
  - hybrid-fraud
  - crypto-laundering
  - teen-targeting
  - executive-targeting
  - scripted-fallback
  - interpol-gffta
---
```

## Summary

Sextortion-investment hybrid fraud combines AI-generated deepfake intimate imagery or coerced image sharing with fraudulent investment scheme mechanics. INTERPOL's 2026 Threat Assessment identifies this as a globally escalating pattern driven by the low marginal effort required once a romance or social engineering relationship is established. INTERPOL documents three distinct regional variants: in North America, teen boys aged 14–17 are targeted with AI-generated deepfake images used to demand money under threat of exposure; in Latin America, financially motivated sextortion targets business executives with high-value ransom demands in cryptocurrency; and in Asia-Pacific, hybrid investment-sextortion schemes use deepfakes to blackmail victims as part of or alongside fake cryptocurrency and Forex investment platforms. In scam centres across Southeast Asia and Africa, INTERPOL reports that if standard investment fraud scripts fail to yield returns, operators are systematically instructed to pivot to sextortion — making the hybrid not an opportunistic escalation but a scripted operational fallback embedded in organized fraud operations. The investment fraud mechanics (TP-0017) and the sextortion mechanics are mutually reinforcing: blackmail leverage suppresses reporting, while the "investment recovery" pivot extracts additional funds under the guise of recouping losses.

## Threat Path Hypothesis

> **Hypothesis**: Actors leverage AI-generated intimate imagery or relationship-based coercion to establish blackmail leverage over victims, then exploit the shame and psychological suppression of reporting to either extract ransom payments directly or pivot to fraudulent investment platforms — positioning the sextortion as the "hook" and the investment scheme as the second-stage extraction mechanism. The hybrid structure is deliberately designed to maximize total extraction while minimizing the probability of law enforcement reporting at any stage.

**Confidence**: Medium-High (78) — INTERPOL GFFTA 2026 documents this as a global trend with specific regional variants corroborated by multiple member country reports. The scripted operational integration of sextortion into scam centre playbooks elevates the confidence level relative to opportunistic hybrid cases.

**Estimated Impact**: USD 5,000–500,000+ per victim. Teen variant: lower ransom amounts but high psychological harm with documented suicide risk. Executive variant: high ransom demands in cryptocurrency, potentially USD 50,000–500,000+. General investment-sextortion: additional investment losses stacked on ransom demands.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Target identification via social media | Actors survey social media platforms (Instagram, Facebook, Snapchat, LinkedIn, dating apps) to identify targets; teen targets selected for accessible profile imagery; executives targeted via LinkedIn for financial profile and public image; general investment fraud targets selected for wealth indicators | Bulk profile scraping activity; targeting patterns aligned to age group (teen accounts with public imagery) or professional profile (executives with public company affiliations) |
| AI deepfake tooling acquisition | Acquire generative AI image synthesis tools via Dark Web marketplaces or commercially available deepfake-as-a-service platforms; these tools can generate intimate imagery from minimal public photos or social media content | Dark Web transactions for synthetic identity kits or deepfake generation tools; use of commercially available face-swap or image generation APIs |
| Fraudulent investment platform provisioning | For hybrid schemes, establish fake cryptocurrency trading or Forex investment platform with fabricated dashboards showing inflated returns; configure crypto wallet infrastructure for receiving victim deposits | Newly registered domain hosting fake investment platform; SSL certificate issuance; fake testimonials and AI-generated review content; crypto wallet generation activity |

**Data Sources**: Open-source intelligence on social media targeting patterns, Dark Web monitoring for deepfake tool acquisition, domain registration feeds for fake investment platforms

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Social media grooming initiation | Actors initiate contact via dating apps, social platforms, or direct messaging, establishing a persona that matches the target's social context; AI-generated or stolen profile photos used to create convincing personas | New social media or dating app contact with no mutual connections; profile photographs consistent with AI generation (reverse-image search yields no prior appearance); rapid escalation of intimacy within 1–2 weeks |
| Relationship and trust building | Sustained communication over days to weeks establishes emotional connection and reduces the victim's guard; actors may use scripted playbooks documented in academic research on pig-butchering and romance-based fraud | Regular communication patterns over extended period; actor avoids video calls or limits to pre-recorded content; escalating personal disclosures to build reciprocal trust |
| Investment opportunity introduction (hybrid variant) | For investment-sextortion hybrid, actor introduces a "successful investment platform" during the relationship phase, initially offering small demonstrable returns to build credibility before soliciting larger deposits | Reference to investment platform emerging organically in relationship conversation; small initial "trial investment" with fabricated profit returns; urgency framing around limited investment windows |

**Target**: Consumer (teen and general public variants); Business Executive (Latin America executive variant)

**Data Sources**: Platform abuse reports, dating app anomaly detection, social media account age and connection graph analysis

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Intimate content acquisition or generation | Actor solicits or coerces real intimate images from victim via relationship grooming (teen and general variants), or uses AI deepfake tools to generate synthetic intimate imagery from publicly available photos (all variants) | Escalation of messaging toward intimate content requests; victim's public social media imagery used as source material for AI synthesis; deepfake generation event correlated with target profile scraping |
| Blackmail leverage establishment | Actor informs victim that intimate imagery (real or AI-generated) has been captured and will be distributed to family, employer, or social network contacts unless payment is made | First extortion demand message; threat to distribute imagery to named contacts; time pressure framing to suppress deliberate response |
| Sextortion-to-investment pivot (hybrid variant) | After initial ransom payment or alongside ongoing extortion demands, actor presents a fraudulent investment platform as a path to "recover" money lost or generate funds to pay the ransom — blending the extortion and investment fraud phases | Investment platform offer introduced concurrent with or immediately following extortion demands; actor frames investment as victim-controlled solution to ransom pressure |

**Data Sources**: Victim reports to platform trust and safety teams, law enforcement intake reports, financial institution fraud reports for crypto transactions following new social media contacts

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Ransom demand and collection | Actor demands cryptocurrency payment (Bitcoin, USDT, Monero) under threat of distributing intimate imagery; payment instructions delivered via messaging app; multiple escalating demands common | First crypto transaction from victim wallet to previously unseen address; transaction amount consistent with ransom demand range; messaging platform communication immediately prior to transaction |
| Fraudulent investment deposit extraction | Victim deposits funds into fake cryptocurrency or Forex investment platform; platform displays fabricated returns to encourage further deposits; withdrawal attempts are blocked or subjected to fabricated "tax" or "unlock fee" demands | Deposits into investment platform with no regulatory registration; platform withdrawal functionality non-functional or subject to escalating fee demands; fabricated profit dashboard |
| Executive ransom escalation (Latin America variant) | High-value ransom demands targeting business executives, often leveraging fabricated evidence of affairs or deepfake imagery of professional misconduct; demands denominated in cryptocurrency to obstruct tracing | Large-value cryptocurrency transaction from executive personal or business accounts; transaction preceded by targeted spearphishing or intimate content threat |

**Data Sources**: Cryptocurrency transaction monitoring, financial institution SAR filings, law enforcement reports, victim disclosures to mental health and support services

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Cryptocurrency laundering through mixing services | Ransom and investment fraud proceeds laundered through cryptocurrency mixing services, chain-hopping across multiple blockchains, and conversion through unregulated exchanges | Crypto transaction graph showing mixing service interaction within 1–3 hops of victim payment; chain-hop to privacy coins (Monero, Zcash) |
| Platform disappearance | Fraudulent investment platform ceases operations once extraction targets are met; victim funds unrecoverable; platform domain deregistered or abandoned | Investment platform domain suddenly unavailable; no customer service response; withdrawal requests permanently pending |
| Re-victimization cycle | Victims who have already paid ransom or lost investment funds are re-contacted by actors posing as recovery agents, law enforcement, or legal firms offering to recover stolen assets — extracting additional payments | Second extortion or "recovery" contact following initial victimization; new actor persona with legal or law enforcement framing; fee-for-recovery payment demand |

**Data Sources**: Cryptocurrency blockchain analytics, dark web monitoring for compromised victim data, law enforcement intake reports for recovery fraud re-victimization

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001: Social Engineering
- FTA002: Romance Fraud
- FTA003: Investment Fraud
- FT016: Brand Impersonation (investment platform)

**MITRE ATT&CK:**

- T1566.003: Phishing: Spearphishing via Service — social media and dating app initial contact
- T1589.001: Gather Victim Identity: Credentials — social media profile scraping for deepfake source imagery
- T1656: Impersonation — actor persona construction and investment platform impersonation
- T1657: Financial Theft — ransom collection and investment fraud extraction

**Group-IB Fraud Matrix:**

- Reconnaissance → Social Engineering → Resource Development → Initial Access → End-user Interaction → Perform Fraud → Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: **P3/P4** — typically discovered when the victim reports the extortion demand to law enforcement or a financial institution, or when the investment platform withdrawal refusal prompts the victim to seek help. The teen variant is frequently discovered only after a family member notices behavioral changes or the victim discloses.

**Look Left** (what did you miss before discovery?):

- Fake investment platform domain registration and hosting provisioning in the weeks before victim targeting
- Social media account creation patterns consistent with actor persona construction — low connection count, AI-generated profile imagery, rapid relationship escalation
- Cryptocurrency wallet activation prior to first extortion demand — wallets prepared in advance for ransom collection
- Darkweb acquisition of deepfake generation tools or synthetic identity kits correlating with actor activity period

**Look Right** (what comes next after discovery?):

- Victim may have already paid ransom and/or lost investment funds before discovery — immediate focus should be on preventing re-victimization via "recovery fraud" re-contact
- Deepfake imagery, if AI-generated from public photos, may persist on actor infrastructure and be used in future victimization cycles — takedown requests to hosting providers warranted
- Teen victims face acute safeguarding risk beyond financial harm — referral to mental health and safeguarding services is a first-priority action
- Cryptocurrency payments may still be traceable if blockchain analysis is initiated rapidly following victim report

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Social media platforms: detect bulk profile scraping and AI-generated profile imagery via computer vision and account graph analysis | Detective | Cyber |
| P2 | Dating app and social media platforms: flag rapid escalation to intimate content requests as anomalous interaction pattern; surface user safety warnings | Detective | Fraud |
| P2 | Financial institution transaction monitoring: flag first-ever cryptocurrency transaction following new social media contact pattern (requires enrichment with platform data) | Detective | Fraud |
| P3 | Victim outreach programs: ensure reporting pathways are low-shame and accessible, particularly for teen victims; partner with mental health services | Preventive | Fraud |
| P4 | Cryptocurrency monitoring: flag transactions to known sextortion wallet addresses or mixing services | Detective | AML |
| P4 | Investment platform due diligence: financial institutions should reject crypto deposits to unregistered investment platforms; provide consumer warnings for commonly spoofed platforms | Preventive | Fraud |
| P5 | Re-victimization alerts: victims who have filed sextortion or investment fraud SARs should be flagged for heightened monitoring against "recovery fraud" re-contact | Detective | Fraud |
| P5 | Cross-border asset tracing: engage INTERPOL IFCACC for cross-border cryptocurrency tracing in high-value cases (USD 50,000+) | Responsive | AML |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Recognize sextortion-investment hybrid as a distinct dual-category fraud type requiring both AML and safeguarding responses |
| ASSESS | Level 3 (Established) | Risk assessment covers AI-enabled sextortion vectors and fraudulent investment platform exposure in consumer digital banking |
| PLAN | Level 2 (Developing) | Incident response playbook addresses both extortion and investment fraud components; safeguarding protocol for vulnerable victims including minors |
| ACT | Level 3 (Established) | Cryptocurrency monitoring integrated with social engineering detection signals; referral pathways to safeguarding services operational |
| MONITOR | Level 3 (Established) | KRIs for first-time crypto transactions following new social contact, investment platform deposits to unregistered entities, and re-victimization patterns |
| REPORT | Level 2 (Developing) | Dual SAR categorization under extortion and investment fraud; NCMEC CyberTipline reporting for cases involving minors |
| IMPROVE | Level 2 (Developing) | Post-incident reviews from hybrid cases drive updates to both AML monitoring rules and customer safeguarding protocols |

---

## Detection Approaches

### Queries / Rules

**First Crypto Transaction Following New Social Media Contact (Splunk SPL)**

```spl
index=transactions sourcetype=payment_events
| where payment_type="cryptocurrency"
| lookup customer_social_media_events customer_id OUTPUT last_new_contact_date, contact_platform
| eval days_since_new_contact = (now() - strptime(last_new_contact_date, "%Y-%m-%d")) / 86400
| where days_since_new_contact < 30
| where is_first_crypto_transaction = "true"
| stats count by customer_id, payment_type, amount, crypto_address, contact_platform, days_since_new_contact
| sort -amount
```

**Investment Platform Deposit — Unregistered Entity Detection (SQL)**

```sql
SELECT t.account_id, t.transaction_date, t.amount, t.currency,
       t.beneficiary_name, t.beneficiary_account, p.registration_status,
       p.regulatory_body, p.registration_date
FROM transactions t
LEFT JOIN investment_platform_registry p
  ON t.beneficiary_name ILIKE '%' || p.platform_name || '%'
  OR t.beneficiary_account = p.platform_account
WHERE t.transaction_type IN ('crypto_deposit', 'wire', 'faster_payment')
AND t.beneficiary_category = 'investment_platform'
AND (p.registration_status IS NULL OR p.registration_status = 'unregistered')
AND t.transaction_date > CURRENT_DATE - INTERVAL '90 days'
ORDER BY t.amount DESC;
```

**Cryptocurrency Address — Mixing Service Proximity Detection (SQL)**

```sql
SELECT v.victim_account_id, v.sar_id, v.report_date,
       t.transaction_hash, t.crypto_address, t.amount,
       m.service_name AS mixer_service, m.hop_count
FROM sar_reports v
JOIN crypto_transactions t ON v.victim_account_id = t.account_id
JOIN crypto_mixing_proximity m ON t.transaction_hash = m.transaction_hash
WHERE v.fraud_category IN ('sextortion', 'investment_fraud', 'hybrid_fraud')
AND m.hop_count <= 3
AND t.transaction_date BETWEEN v.incident_start_date AND v.report_date + INTERVAL '30 days'
ORDER BY t.amount DESC;
```

### Behavioral Analytics

- Account age versus transaction velocity anomaly: a customer with no prior cryptocurrency transaction history making their first crypto payment within 30 days of a new social media connection is a high-priority signal
- Rapid escalation from small to large deposits on investment platforms — actors typically demonstrate small fabricated "profits" to encourage increasing deposit commitment
- Teen account holders (age 14–17) making any cryptocurrency transaction without prior transaction history should trigger immediate review
- Executive accounts (flagged via LinkedIn or employment data enrichment) making high-value cryptocurrency payments to wallet addresses with no prior relationship warrant immediate investigation

### Cross-Team Correlation

- **Fraud + AML**: Sextortion ransom payments and investment fraud deposits should both generate SAR filings — the hybrid nature warrants dual categorization; coordinate with AML for cryptocurrency tracing
- **Fraud + Customer Service**: Customer-reported distress calls referencing intimate imagery threats or investment platform withdrawal refusals should be flagged immediately to the fraud team for SAR initiation and safeguarding referral
- **Cyber + Fraud**: Dark web monitoring for deepfake generation tools correlated with known actor infrastructure can provide advance warning before victim targeting begins

---

## Operational Evidence

### EV-TP0052-2026-001: Americas Region — Teen Sextortion via AI Deepfakes (North America)

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 (Americas region chapter — "Surges in Sextortion following Global Trends")
- **Victims**: Teenage boys aged 14–17, North America
- **Modus Operandi**: Fraudsters generate AI deepfake intimate imagery using publicly available teen social media photos; extort money under threat of distributing imagery to family and school contacts
- **Confidence**: High (INTERPOL member country reports)
- **Summary**: North American member countries reported a concentrated trend of sextortion targeting teenage boys using AI-generated deepfake imagery. The targeting of minors elevates this beyond a financial fraud concern to an acute safeguarding risk with documented links to victim psychological harm and suicide risk.

### EV-TP0052-2026-002: Latin America — Executive Sextortion with Cryptocurrency Ransom Demands

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 (Americas region chapter — "Surges in Sextortion following Global Trends")
- **Victims**: Business executives, Latin America
- **Modus Operandi**: Financially motivated sextortion targeting executives with high-value cryptocurrency ransom demands; leverage may include fabricated or deepfake evidence of misconduct
- **Confidence**: High (INTERPOL member country reports)
- **Summary**: Latin American member countries reported a pattern of financially motivated sextortion specifically targeting business executives, with ransom demands significantly exceeding those in general population targeting, payable in cryptocurrency to obstruct tracing.

### EV-TP0052-2026-003: Asia-Pacific — Hybrid Investment-Sextortion with Deepfakes

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 (Asia-Pacific region chapter — "Investment Fraud: A Multifaceted Threat Combining Financial Deception, Cultural Exploitation, and Sextortion")
- **Region**: Asia-Pacific (Southeast Asia scam centre nexus)
- **Modus Operandi**: Fake cryptocurrency and Forex investment platforms combined with deepfake-based sextortion; if investment fraud scripts fail, scam centre operators pivot to sextortion per scripted operational playbook
- **Confidence**: High (INTERPOL member country reports, scam centre operational intelligence)
- **Summary**: INTERPOL documents that hybrid investment-sextortion is no longer opportunistic in scam centre operations — it is systematically embedded as a fallback tactic in fraud scripts. This operational integration distinguishes it from standalone sextortion and links the attack chain directly to organized transnational crime infrastructure.

### EV-TP0052-2026-002: INTERPOL Sextortion Scripted Integration

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition (March 2026)
- **Key Finding**: Sextortion is now "systematically integrated into romance/investment fraud as a scripted fallback" — not merely opportunistic but formalized in scam compound operating procedures. When an investment fraud script fails to convert a victim, operators activate a sextortion script using compromising material gathered during the relationship-building phase.
- **CFPF Phase Coverage**: P3-P4 transition (sextortion activated when primary investment scam fails)
- **Confidence**: High

---

## References

- INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 — "Increasingly Hybrid Fraud Tactics and the Rise in Sextortion" (global trends chapter); "Surges in Sextortion following Global Trends" (Americas chapter); "Investment Fraud: A Multifaceted Threat Combining Financial Deception, Cultural Exploitation, and Sextortion" (Asia-Pacific chapter)
- INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition, March 2026 — "Sextortion" typology definition and Key Findings section
- Marasa, Marie-Helen, and Ives, Emily R., "Deconstructing a form of hybrid investment fraud: Examining 'pig butchering' in the United States," Journal of Economic Criminology, 2024 (cited in INTERPOL GFFTA 2026 as footnote 23)
- Cross, C., Holt, K., and O'Malley, R., "If U Don't Pay They Will Share the Pics: Exploring Sextortion in the Context of Romance Fraud," Victims & Offenders, 19 May 2022 (cited in INTERPOL GFFTA 2026 as footnote 24)
- FBI IC3: Internet Crime Report 2024 — sextortion statistics and teen victim reporting
- FLAME TP-0017: Pig Butchering / Romance Baiting — investment fraud mechanics in the hybrid scheme
- FLAME TP-0025 / TP-0026: GenAI-Enhanced Fraud variants — deepfake and synthetic imagery attack surface

---

## Analyst Notes

**Dual Categorization for SAR Reporting**: The hybrid nature of this scheme creates a classification challenge for BSA/SAR reporters. The scheme involves both extortion (blackmail with threatened reputational harm) and investment fraud (fake platform deposit extraction). Analysts should categorize SARs under both extortion (category E) and investment fraud (category I) where applicable, and include both in the narrative. For cases involving minors, NCMEC CyberTipline filing is an additional required action.

**Safeguarding Priority for Teen Victims**: The North America teen targeting variant documented by INTERPOL carries documented links to victim psychological harm including suicide risk. Financial institution analysts encountering teen customer sextortion cases should prioritize safeguarding referral over financial case management. Standard fraud investigation timelines may need to be accelerated or suspended in favor of welfare response.

**The Operational Integration Signal**: INTERPOL's documentation that scam centres in Southeast Asia embed sextortion as a scripted fallback — not an opportunistic escalation — is a significant threat intelligence finding. It means that any investment fraud case originating from scam centre infrastructure should be assessed for potential concurrent or follow-on sextortion activity targeting the same victim.

**TP-0017 Cross-Reference**: The investment fraud mechanics in the hybrid scheme (fake platform, fabricated returns, withdrawal blocking, escalating fee demands) are extensively documented in TP-0017 (Pig Butchering / Romance Baiting). Analysts investigating hybrid cases should apply TP-0017 detection logic in parallel to this TP's sextortion-specific detection approaches.

**BSA/SAR Considerations**: Sextortion-investment hybrid losses should be reported under BSA categories Extortion (E) and/or Investment fraud (I) depending on the primary loss vector. For cases with cryptocurrency laundering, include Suspicious use of cryptocurrency (category C). Recommended SAR keywords: "sextortion," "deepfake," "hybrid fraud," "investment platform fraud," "crypto ransom," "pig butchering," "romance baiting," "AI-generated imagery."

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-17 | FLAME Project | Initial submission |
| 2026-03-20 | FLAME Project | Enriched with INTERPOL GFFTA 2026 finding that sextortion is systematically scripted as fallback in compound operations |
