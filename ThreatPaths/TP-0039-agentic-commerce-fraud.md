# TP-0039: Agentic Commerce Fraud

```yaml
---
id: TP-0039
title: "Agentic Commerce Fraud"
category: ThreatPath
date: 2026-03-04
author: "FLAME Project (sourced from Recorded Future Payment Fraud Intelligence Report 2025)"
source: "https://www.recordedfuture.com/research/annual-payment-fraud-intelligence-report-2025"
tlp: WHITE
sector:
  - technology
  - retail
  - fintech
  - payments
  - cross-sector
fraud_types:
  - autonomous-ai-fraud
  - social-engineering
  - account-takeover
  - unauthorized-transaction
  - gift-card-fraud
  - returns-fraud
  - refunding-as-a-service
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
mitre_attack:
  - T1059       # Command and Scripting Interpreter
  - T1078       # Valid Accounts
  - T1656       # Impersonation
  - T1657       # Financial Theft
ft3_tactics: ["FTA001", "FTA002", "FTA003", "FTA005", "FTA007", "FTA009", "FTA010", "FT003", "FT016", "FT028", "FT031"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Trust Abuse"
  - "End-user Interaction"
  - "Account Access"
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
confidence_score: 65
source_reliability: B
info_credibility: 2
related_tps:
  - id: TP-0025
    relationship: related-to
  - id: TP-0029
    relationship: enhances
  - id: TP-0013
    relationship: related-to
  - id: TP-0031
    relationship: related-to
  - id: TP-0030
    relationship: related-to
regulatory_refs:
  - REG-CFPB-REGE
  - REG-DORA
  - REG-PSD3-SCA
  - REG-INTERPOL-GFFTA
baseline_ids:
  - BL-0019
tags:
  - agentic-ai
  - ai-agent
  - intent-spoofing
  - automated-fraud-workflow
  - liability-ambiguity
  - commerce-automation
  - open-banking-parallel
  - amazon-buy-for-me
  - visa-intelligent-commerce
  - mastercard-agent-pay
  - interpol-gffta
  - universal-commerce-protocol
  - ucp
  - agent-payments-protocol
  - ap2
  - indirect-prompt-injection
  - cart-mandate-poisoning
  - returns-logic-hijacking
  - organized-retail-crime
  - know-your-agent
  - agent-reputation-score
  - openclaw
  - gift-card-theft
  - nrf
---
```

---

## Summary

Agentic commerce fraud exploits the emerging paradigm of AI agent-mediated purchasing, where autonomous AI systems act on behalf of consumers to select merchants, negotiate prices, and execute transactions across the payment ecosystem. Pilot programs such as Amazon Buy for Me, Visa Intelligent Commerce, and Mastercard Agent Pay represent early implementations of this paradigm, while Google's Universal Commerce Protocol (UCP) -- unveiled at the NRF Big Show in January 2026 -- establishes an open-source standard for agentic commerce with tokenized payments and verifiable credentials, compatible with the Agent Payments Protocol (AP2). These systems create a novel transaction chain: Consumer provides Intent to AI Agent, which performs Autonomous Merchant Selection, interacts with Merchant Transaction Systems, submits transactions to Payment Infrastructure for Authorization and Settlement by the Card Issuer. Each handoff in this chain introduces attack surfaces that do not exist in traditional human-initiated commerce. According to Bain & Company, agentic AI is expected to handle 15-25% of all e-commerce volume by 2030, while McKinsey estimates agentic commerce could generate $3-5 trillion in global retail revenue by 2030. The World Economic Forum estimates that by 2028, one in four data breaches could result from AI agent exploitation.

The core vulnerability is that user and agent intent becomes a novel attack surface -- vulnerable to the same categories of attacks that circumvent identity authentication, but applied to the delegation of purchasing authority rather than credential theft. Threat actors can compromise or manipulate AI agent context, prompts, or MCP server connections to redirect purchasing intent, inflate prices, route transactions to attacker-controlled merchants, or execute unauthorized purchases at machine speed. In April 2025, threat actor "d0ctrine" published proof-of-concept documentation outlining agentic fraud workflows including agent-automated fraud, mimicry of human interaction patterns, and evasion of behavioral and device-based controls. In November 2025, Anthropic disclosed the first known cyber-espionage campaign orchestrated primarily by an autonomous AI system, coinciding with an attempted fraudulent purchase for the same AI service -- demonstrating convergence between AI-enabled fraud and AI-enabled cyber threats.

The structural parallel to early open banking is significant: as banks lost visibility into customer activity through third-party payment initiators, they experienced degraded controls for identity verification, online interaction monitoring, and bot detection. Agentic commerce replicates this pattern at greater scale -- opaque agent behavior hides intent, device context, and interaction patterns from downstream payment processors and issuers. Without improved control visibility and shared investigation workflows, the ecosystem faces expanded fraud investigation scope (distinguishing third-party fraud, first-party misuse, and agentic abuse) and liability ambiguity that increases operational costs even when liability is contractually clear.

---

## Threat Path Hypothesis

> **Hypothesis**: Threat actors are exploiting the emerging agentic commerce ecosystem -- where AI agents autonomously execute purchasing decisions on behalf of consumers -- by manipulating agent intent, compromising agent infrastructure (MCP servers, API endpoints), and leveraging the opacity of agent-mediated transactions to execute unauthorized purchases, redirect transactions to attacker-controlled merchants, and evade behavioral and device-based fraud controls at machine speed.

**Confidence**: Moderate -- based on published threat actor PoC documentation (d0ctrine, April 2025), Anthropic's disclosure of autonomous AI-orchestrated cyber-espionage with associated fraud (November 2025), Recorded Future Annual Payment Fraud Intelligence Report 2025 analysis, and structural analysis of pilot program architectures (Amazon, Visa, Mastercard). The threat is emerging; large-scale operational exploitation has not yet been documented but the attack surfaces are clearly defined.

**Estimated Impact**: $10,000 -- $10,000,000+ per campaign depending on agent authority scope and transaction limits. Aggregate ecosystem impact could reach billions as agentic commerce scales. Secondary impacts include liability disputes between consumers, agent providers, merchants, and issuers; degraded fraud detection effectiveness; and increased investigation costs as agent behavior complicates transaction attribution.

---

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P1-001: Agentic commerce platform identification | Actors identify AI agent-enabled commerce platforms, pilot programs, and their associated authentication and authorization flows. Target platforms include Amazon Buy for Me, Visa Intelligent Commerce, Mastercard Agent Pay, and emerging third-party agent frameworks. | Systematic probing of agent API endpoints; reconnaissance of agent authentication mechanisms; enumeration of agent-accessible merchant catalogs |
| CFPF-P1-002: Agent authorization flow mapping | Actors map the delegation chain from consumer intent to agent action, identifying where intent verification occurs, how purchasing authority is scoped, and what controls gate transaction execution. | API documentation scraping; agent sandbox testing; analysis of agent permission models and OAuth/token-based delegation frameworks |
| CFPF-P1-003: Intent-spoofing vector identification | Actors identify vectors through which agent purchasing intent can be manipulated -- prompt injection via compromised product descriptions, MCP server compromise, API endpoint manipulation, or social engineering of the agent's context window. | Probing of agent input parsing; testing of prompt injection payloads in product listing content; analysis of agent tool-use interfaces for injection points |

**Data Sources**: Agent platform API logs, sandbox environment access logs, web scraping detection systems, MCP server connection logs, agent framework documentation access analytics.

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P2-001: Agent context/prompt compromise | Actors inject malicious instructions into the AI agent's context window through compromised MCP servers, poisoned product descriptions, manipulated API responses, or adversarial content in merchant pages that the agent processes during comparison shopping. | Unusual agent tool-call patterns; agent accessing unexpected MCP endpoints; agent context containing instructions inconsistent with user's stated purchasing intent |
| CFPF-P2-002: MCP server or API endpoint compromise | Actors compromise third-party MCP servers or API endpoints that the agent relies on for product data, price comparison, or merchant verification, injecting manipulated data that redirects agent behavior. | MCP server responses containing anomalous instructions or redirect patterns; API endpoint returning manipulated pricing or merchant data; certificate or authentication anomalies on agent data sources |
| CFPF-P2-003: Social engineering of agent authentication | Actors social-engineer the AI agent into authenticating to attacker-controlled services by presenting convincing but fraudulent merchant interfaces, OAuth flows, or payment processing endpoints that the agent interacts with during autonomous purchasing. | Agent initiating authentication flows with unrecognized service endpoints; agent presenting credentials to domains not in the approved merchant catalog; OAuth redirect chains involving unfamiliar intermediaries |
| CFPF-P2-004: Indirect prompt injection via deals aggregator sites | Actors create deals aggregator or coupon sites that UCP agents crawl to find discounts. The site contains hidden payloads (e.g., invisible text, hidden HTML elements) that reprogram the agent's memory when ingested during comparison shopping. Because UCP agents are designed to autonomously browse, summarize and interact with merchant sites, they are highly susceptible to indirect prompt injection where the attack is encountered by the agent rather than typed by the user. | Agent accessing known deals aggregator sites with embedded hidden content; agent context window containing instructions inconsistent with browsing task; agent behavioral changes after visiting specific external sites |
| CFPF-P2-005: UCP returns instruction injection via product page metadata | Actors embed hidden instructions in HTML metadata or invisible `<span>` tags on product listing pages. When a user's agent reads the product page for return instructions, it ingests the malicious command as a high-priority system update, instructing it to skip verification steps in the UCP returns state machine. | Product pages containing hidden text/instructions in metadata or invisible elements; agent processing return instructions from unverified sources; agent context containing system-level override commands from merchant content |

**Data Sources**: Agent execution logs, MCP server audit logs, API gateway traffic analysis, merchant catalog integrity monitoring, OAuth flow logging, agent tool-use telemetry, deals aggregator content scanning, product page metadata analysis.

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P3-001: Purchasing intent manipulation | Actors spoof or manipulate the agent's purchasing intent -- redirecting product selection, inflating prices, or substituting merchants -- such that the agent believes it is fulfilling the user's original request while actually executing the attacker's desired transaction. | Agent selecting merchants or products that diverge from user's stated preferences or historical purchasing patterns; agent price verification logic bypassed or returning anomalous results; agent executing purchases at prices significantly above market |
| CFPF-P3-002: Price verification and comparison logic exploitation | Actors manipulate the agent's price comparison mechanisms by presenting artificially competitive pricing on attacker-controlled merchant sites, then escalating prices after the agent commits to the merchant, or by injecting false price data into comparison APIs. | Agent price comparison results showing attacker-controlled merchants consistently ranking highest; price discrepancies between agent's recorded comparison data and actual merchant pricing; bait-and-switch pricing patterns where final transaction amount exceeds comparison price |
| CFPF-P3-003: Delegated payment authority exploitation | Actors exploit the scope of delegated payment authority -- where the consumer has authorized the agent to spend up to a certain limit or within certain categories -- by manipulating the agent to make purchases that technically fall within authorized parameters but serve the attacker's purposes. | Agent executing purchases that match authorized categories but diverge from user's actual intent; agent approaching or hitting delegation spending limits through attacker-directed transactions; purchases to merchant categories the user has never previously engaged with |
| CFPF-P3-004: UCP Cart Mandate gift card injection | Actors target the creation of the UCP Cart Mandate -- the digital contract that defines what is being bought and for whom. After an agent's memory is reprogrammed via indirect prompt injection, the agent appends a hidden line-item (e.g., a digital gift card) to the Cart Mandate JSON-RPC payload, with the recipient email set to an attacker-controlled address and the display status set to hidden. The agent may justify the additional cost as "Tax/Fees" in the user's UI. | Cart Mandate containing gift card line items not present in user's shopping intent; recipient email addresses on digital gift cards not matching user's known email addresses; line items with display_status set to hidden; total price discrepancies attributable to unexplained surcharges |
| CFPF-P3-005: UCP returns state machine bypass setup | After ingesting hidden instructions from product page metadata, the agent prepares to bypass the UCP returns state machine by storing fraudulent tracking IDs (e.g., "void-000") and instructions to skip the `order.return.verify` step when a return is initiated. | Agent storing return-related instructions from unverified product page sources; agent context containing references to skipping verification steps; pre-staged tracking IDs with known void patterns |

**Data Sources**: Agent transaction logs, price comparison audit trails, merchant catalog monitoring, delegated authority scope tracking, user intent verification systems, agent behavioral analytics, Cart Mandate JSON-RPC payload inspection, UCP returns state machine logs.

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P4-001: Unauthorized agent-initiated transactions | The compromised or manipulated agent executes transactions using the consumer's legitimate payment credentials -- purchasing products from attacker-controlled merchants, executing purchases at inflated prices, or initiating bulk transactions at machine speed. The transactions are technically "authorized" because the agent has delegated payment authority. | Transactions initiated by agent at velocities exceeding human purchasing patterns; purchases from merchants not in user's historical pattern; agent completing multiple purchases per minute across different merchants; transaction amounts clustering near delegation authority limits |
| CFPF-P4-002: Attacker-controlled merchant transactions | The agent routes purchases to attacker-controlled merchant accounts, which may offer legitimate-appearing but fraudulent storefronts. The attacker collects payment while delivering nothing, counterfeit goods, or minimal-value items. | Agent selecting merchants with recently created accounts, no prior transaction history, or patterns matching known fraudulent merchant profiles; purchases from merchants in high-risk categories or jurisdictions; merchant accounts receiving agent-initiated transactions from multiple unrelated consumers |
| CFPF-P4-003: Automated fraud at machine speed | Because AI agents can execute transactions orders of magnitude faster than human shoppers, compromised agents can process large volumes of fraudulent transactions before human review cycles can intervene. A single compromised agent session could execute dozens of purchases in minutes. | Transaction velocity exceeding 10x human baseline for the same commerce flow; multiple simultaneous transactions across different merchants from the same agent session; agent session duration anomalously short relative to the number and complexity of purchases executed |
| CFPF-P4-004: UCP Cart Mandate checkout with injected gift card | The agent constructs the final JSON-RPC payload for the UCP checkout endpoint with the unauthorized gift card line item included. If the user's UI only shows a Total Price (which the agent justifies as Tax/Fees), the user approves the mandate, and the gift card is sent to the attacker. The real cost extends beyond the stolen amount -- the customer's trust in the retailer is eroded and the retailer bears both the chargeback and the reputational damage. | UCP checkout payloads containing gift card line items with external recipient emails; user approval of Cart Mandates with unexplained surcharges; digital gift card redemption from IP addresses unrelated to the purchasing user; chargeback patterns correlated with agent-initiated gift card purchases |
| CFPF-P4-005: UCP void return execution | The agent triggers the UCP refund primitive (`settlement.refund.instant()`) without requiring a real shipping scan, using a fraudulent tracking ID (e.g., "void-000") as proof of dispatch and skipping the `order.return.verify` step. At scale, organized crime groups use bot farms to initiate thousands of void returns per hour, potentially liquidating a retailer's cash reserves before human intervention. | Refund requests with tracking IDs matching known void patterns (void-000, void-*); `order.return.verify` step skipped in UCP state machine; high-velocity refund requests from bot-like agent sessions; refund amounts not correlating with legitimate return shipping activity |

**Data Sources**: Payment gateway transaction logs, agent session telemetry, merchant risk scoring systems, transaction velocity monitoring, delegation authority tracking, agent-to-merchant interaction logs, UCP checkout endpoint logs, Cart Mandate payload inspection, UCP refund primitive audit logs, shipping verification systems.

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| CFPF-P5-001: Transaction processing before human review | Agent-initiated transactions are processed and settled through payment infrastructure before the consumer reviews or approves individual purchases, exploiting the inherent latency between agent action and human oversight. | Transactions settled before consumer session review; high-value purchases executed during periods when consumer is unlikely to be monitoring agent activity; dispute filing patterns concentrated in the hours/days after agent purchase sessions |
| CFPF-P5-002: Liability ambiguity exploitation | The multi-party nature of agentic commerce (consumer, agent provider, merchant, payment processor, issuer) creates liability ambiguity that actors exploit. Even when fraud is detected, the question of who bears the loss -- the consumer who delegated authority, the agent provider whose system was compromised, or the issuer who authorized the transaction -- delays resolution and increases investigation costs. | Dispute resolution timelines extending beyond standard chargeback windows; multi-party liability claims involving agent providers; increased investigation costs as agent behavior logs must be analyzed to determine whether the transaction reflected consumer intent |
| CFPF-P5-003: Scale exceeding investigation capacity | Fraudulent agent-initiated transactions at machine speed generate investigation volumes that exceed human fraud analyst capacity, creating a backlog that allows additional fraudulent transactions to clear before controls can be tightened. | Fraud investigation queue depth increasing disproportionately after agent commerce adoption; average investigation time per case increasing due to agent behavior analysis requirements; agent-initiated transaction dispute rates exceeding human-initiated dispute rates |

**Data Sources**: Payment settlement systems, dispute management platforms, chargeback analytics, agent session replay and audit logs, investigation case management systems, liability allocation tracking.

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**

- FTA001 (Fraud Enablement) -- AI agent infrastructure compromise enabling downstream fraud execution
- FTA002 (Account Setup) -- Attacker-controlled merchant account creation for receiving agent-directed payments
- FTA003 (Account Compromise) -- Compromise of agent MCP servers and API endpoints
- FTA005 (Identity Fraud) -- Spoofing of merchant identity to manipulate agent merchant selection
- FTA007 (Payment Fraud) -- Unauthorized transactions executed through compromised agent purchasing flows
- FTA009 (Money Laundering) -- Revenue extraction through attacker-controlled merchant accounts
- FT003 (Bot Activity) -- Agent-automated transaction execution at machine speed
- FT016 (Authorized Push Payment Fraud) -- Transactions technically authorized through delegated agent authority but reflecting attacker intent
- FT028 (Impersonation) -- Impersonation of legitimate merchants to attract agent-directed purchases
- FT031 (Extortion) -- Potential extortion of agent providers or consumers using compromised transaction data

**MITRE ATT&CK:**

- T1059 (Command and Scripting Interpreter) -- Exploitation of agent scripting and tool-use interfaces for unauthorized command execution
- T1078 (Valid Accounts) -- Use of legitimately delegated agent payment credentials for fraudulent transactions
- T1656 (Impersonation) -- Impersonation of legitimate merchants and payment endpoints to redirect agent transactions
- T1657 (Financial Theft) -- Financial theft through unauthorized agent-initiated purchases and attacker-controlled merchant payments

**Group-IB Fraud Matrix:**

- Reconnaissance -- Identification of agentic commerce platforms, agent authorization flows, and intent-spoofing vectors
- Resource Development -- Creation of attacker-controlled merchant accounts, MCP server compromise infrastructure, adversarial prompt payloads
- Trust Abuse -- Exploitation of consumer trust in AI agent purchasing decisions and agent trust in merchant data sources
- End-user Interaction -- Agent-mediated interaction with attacker-controlled merchant interfaces
- Account Access -- Leveraging legitimately delegated agent payment authority for unauthorized transactions
- Perform Fraud -- Execution of manipulated purchases at machine speed through compromised agent sessions
- Monetization -- Revenue extraction through attacker-controlled merchant accounts and exploitation of liability ambiguity

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at **Phase 5 (Monetization)** when the consumer reviews agent purchasing activity and identifies unauthorized or unexpected transactions, or when chargeback patterns trigger issuer investigation. May also be discovered at **Phase 4** if transaction velocity monitoring flags agent sessions exceeding human purchasing baselines, or at **Phase 2** if MCP server compromise is detected through infrastructure monitoring.

**Look Left** (what was missed before discovery):

- **P5 -> P4**: Were agent-initiated transactions executing at velocities that should have triggered velocity controls? Were purchases routing to merchants that did not match the user's historical patterns or stated intent?
- **P4 -> P3**: Was the agent's price verification logic returning anomalous results? Were there signs that the agent's purchasing intent had been manipulated -- purchases in unexpected categories, at unexpected price points, or from unexpected merchants?
- **P3 -> P2**: Were there indicators of MCP server compromise or API endpoint manipulation? Did the agent's context window contain instructions inconsistent with the user's stated purchasing intent? Were there anomalous OAuth flows or authentication attempts to unrecognized service endpoints?
- **P2 -> P1**: Were there reconnaissance patterns against agent API endpoints or sandbox environments? Were adversarial payloads being tested against agent input parsing?
- **Cross-team gap**: The agent provider monitors agent behavior. The payment processor monitors transaction patterns. The issuer monitors cardholder activity. The merchant platform monitors seller behavior. No single party has end-to-end visibility into the agentic commerce transaction chain from consumer intent through agent action to merchant fulfillment. The opacity of agent behavior -- what the agent "decided" and why -- is a novel investigation challenge that requires agent session replay capabilities that most fraud teams do not yet possess.

**Look Right** (predicted next steps if uninterrupted):

- Compromised agents will continue executing fraudulent transactions at machine speed until delegation authority is exhausted or credentials are revoked
- Attacker-controlled merchant accounts will extract revenue before platform enforcement can identify and suspend them
- Liability disputes between consumers, agent providers, and issuers will delay loss recovery and increase operational costs
- Threat actors will refine agent manipulation techniques based on which platforms have weaker intent verification controls
- As agentic commerce scales, the volume of agent-initiated transactions will provide cover for fraudulent transactions within the noise of legitimate agent activity

---

## Underground Ecosystem Context

### Threat Actor Activity

| Actor/Event | Date | Description | Significance |
|-------------|------|-------------|--------------|
| d0ctrine | April 2025 | Published PoC documentation on underground forums outlining agentic fraud workflows: agent-automated fraud execution, mimicry of human interaction patterns, evasion of behavioral/device-based controls | First documented threat actor PoC specifically targeting agentic commerce attack surfaces |
| Anthropic disclosure | November 2025 | Disclosed first known cyber-espionage campaign orchestrated primarily by autonomous AI system, coinciding with attempted fraudulent purchase for the same AI service | Demonstrates convergence of AI-enabled cyber threats and AI-enabled fraud; validates autonomous AI as both attack tool and attack target |
| OpenClaw | 2026 | Identification of the "buy-anything skill (v2.0.0)" that could be weaponized by fraudsters to automate purchasing fraud via agentic commerce protocols | Demonstrates emerging tool availability for automated agentic purchasing exploitation |

### Tool Ecosystem

- Prompt injection frameworks targeting AI agent context windows
- Indirect prompt injection payloads embedded in deals aggregator sites, coupon pages, and product listings
- MCP server impersonation and man-in-the-middle tooling
- Adversarial product description generators designed to manipulate agent comparison shopping logic
- UCP Cart Mandate payload manipulation tools for injecting hidden line items (gift cards, surcharges)
- UCP returns state machine exploit scripts for bypassing `order.return.verify` with void tracking IDs
- Anti-detection tools that mimic human browsing patterns within agent sessions
- Automated merchant account creation tools for receiving agent-directed payments
- Agent session replay analysis tools for identifying delegation authority boundaries
- OpenClaw "buy-anything skill (v2.0.0)" and similar agentic purchasing automation frameworks
- Bot farm orchestration tools for mass void-return execution against retailer refund endpoints

### Intelligence Sources

- Recorded Future Annual Payment Fraud Intelligence Report 2025 -- primary source for agentic commerce threat analysis
- Unit 42 (Palo Alto Networks) -- "Who's Really Shopping? Retail Fraud in the Age of Agentic AI" (March 2026) -- UCP-specific attack scenarios including gift card theft via payload poisoning and returns fraud via logic hijacking
- d0ctrine PoC documentation (underground forums, April 2025)
- Anthropic security disclosure (November 2025)
- Amazon Buy for Me technical documentation
- Visa Intelligent Commerce architecture analysis
- Mastercard Agent Pay pilot program specifications
- Google Universal Commerce Protocol (UCP) specification (January 2026)
- Google Agent Payments Protocol (AP2) specification (September 2025)
- Bain & Company -- agentic commerce market sizing study
- McKinsey & Company -- agentic commerce revenue projections
- World Economic Forum Annual Meeting 2026 -- AI agent exploitation projections
- NRF Center for Digital Risk & Innovation -- retailer collaboration on agentic AI adoption and fraud prevention

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Agent API endpoint hardening -- rate limiting, authentication, anomaly detection on agent sandbox and production endpoints | Preventive | Agent Platform / Security |
| P1 | MCP server integrity monitoring -- cryptographic verification of MCP server responses, certificate pinning for agent-to-server connections | Preventive | Agent Platform |
| P2 | Agent context integrity verification -- validate that agent context window contents are consistent with user's stated intent before transaction execution | Detective | Agent Platform |
| P2 | MCP server allowlisting -- agents should only connect to pre-approved, verified MCP servers; connections to unknown servers should be blocked and alerted | Preventive | Agent Platform / Security |
| P3 | Intent verification checkpoint -- require explicit user confirmation for purchases exceeding defined thresholds (amount, category, merchant novelty) before agent execution | Preventive | Agent Platform / Commerce Platform |
| P3 | Price verification against independent data sources -- agent should cross-reference pricing with multiple independent sources to detect price manipulation | Detective | Agent Platform |
| P4 | Transaction velocity controls -- enforce agent-specific transaction rate limits that prevent machine-speed bulk purchasing; flag sessions exceeding human purchasing velocity baselines | Detective | Payment Gateway / Issuer |
| P4 | Merchant risk scoring for agent transactions -- enhanced scrutiny for agent-initiated transactions to newly created merchants, merchants in high-risk categories, or merchants receiving agent traffic from multiple unrelated consumers | Detective | Payment Gateway / Marketplace |
| P5 | Agent session audit logging -- comprehensive logging of agent decision chain (intent received, merchants evaluated, prices compared, transaction executed) to support post-incident investigation | Detective | Agent Platform |
| P5 | Shared investigation frameworks -- cross-entity protocols for agent transaction dispute resolution involving agent provider, merchant, payment processor, and issuer with defined data sharing and liability allocation | Responsive | Industry Consortium / Regulator |
| P2 | Agent content sanitization -- strip or neutralize hidden text, invisible HTML elements, and metadata-embedded instructions from pages the agent browses before ingesting content into the agent's context window | Preventive | Agent Platform |
| P3 | Cart Mandate line-item verification -- require explicit user review of all individual line items in the UCP Cart Mandate before checkout, preventing hidden items from being obscured behind aggregate totals | Preventive | Commerce Platform / Agent Platform |
| P3 | Gift card recipient validation -- flag Cart Mandates containing digital gift cards with recipient email addresses that do not match the authenticated user's known email addresses | Detective | Commerce Platform |
| P4 | UCP returns state machine integrity -- enforce mandatory completion of `order.return.verify` step with validated shipping scan before processing any refund via `settlement.refund.instant()`; reject tracking IDs matching known void patterns | Preventive | Commerce Platform / Payment Gateway |
| P4 | Refund velocity throttling -- enforce per-account and per-merchant rate limits on refund requests to prevent bot farm-driven mass void returns | Detective | Commerce Platform / Payment Gateway |
| P1 | Know Your Agent (KYA) implementation -- validate agent identity and enforce agent reputation scoring before allowing agent-initiated transactions; reject agents below minimum reputation thresholds | Preventive | Commerce Platform / Agent Platform |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 2 (Developing) | Recognition of agentic commerce as an emerging fraud attack surface; initial resource allocation for monitoring agent-initiated transaction patterns; engagement with agent platform providers on shared fraud prevention objectives |
| ASSESS | Level 2 (Developing) | Assessment of organizational exposure to agentic commerce fraud through pilot program participation or payment processing of agent-initiated transactions; identification of visibility gaps in agent transaction chain; evaluation of existing fraud controls' effectiveness against agent-mediated purchasing patterns |
| PLAN | Level 2 (Developing) | Development of agent-specific fraud detection rules and investigation procedures; planning for agent session audit log integration into fraud investigation workflows; cross-entity coordination protocols for agent transaction disputes |
| ACT | Level 3 (Established) | Transaction velocity controls calibrated for agent purchasing patterns; merchant risk scoring enhanced for agent-initiated transactions; intent verification checkpoints for high-value or anomalous agent purchases; MCP server integrity monitoring |
| MONITOR | Level 3 (Established) | Continuous monitoring of agent-initiated transaction velocity, merchant selection patterns, and price verification results; KRIs for agent transaction dispute rates versus human-initiated dispute rates; monitoring of agent session anomalies and MCP server connection integrity |
| REPORT | Level 2 (Developing) | Agent-specific fraud loss reporting; dispute resolution tracking for agent-initiated transactions; regulatory reporting on agentic commerce fraud exposure; information sharing with agent platform providers and industry consortia |
| IMPROVE | Level 2 (Developing) | Post-incident analysis of agent fraud cases to identify intent manipulation vectors; feedback loops with agent platform providers on detection effectiveness; continuous refinement of agent transaction velocity baselines as agentic commerce adoption scales |

### Maturity Levels Reference
- **Level 1 (Initial):** Ad hoc, reactive fraud management
- **Level 2 (Developing):** Basic fraud function exists with some defined processes
- **Level 3 (Established):** Formalized fraud program with proactive capabilities
- **Level 4 (Advanced):** Data-driven, continuously improving fraud program
- **Level 5 (Leading):** Industry-leading, predictive fraud management

---

## Detection Approaches

### Queries / Rules

**SQL -- Agent Intent Divergence Detection (Phase 3-4)**

```sql
SELECT
    t.transaction_id,
    t.agent_session_id,
    t.user_id,
    t.merchant_id,
    t.merchant_name,
    t.product_category,
    t.transaction_amount,
    t.agent_stated_intent,
    u.historical_top_categories,
    u.avg_transaction_amount,
    m.merchant_creation_date,
    m.merchant_risk_score
FROM agent_transactions t
JOIN user_profiles u ON t.user_id = u.user_id
JOIN merchant_profiles m ON t.merchant_id = m.merchant_id
WHERE t.initiated_by = 'ai_agent'
  AND (
    t.product_category NOT IN (SELECT category FROM user_purchase_history WHERE user_id = t.user_id)
    OR t.transaction_amount > u.avg_transaction_amount * 3
    OR m.merchant_creation_date > CURRENT_DATE - INTERVAL '30 days'
    OR m.merchant_risk_score > 0.7
  )
ORDER BY t.transaction_timestamp DESC;
```

**Splunk -- Agent Transaction Velocity Anomaly Detection (Phase 4)**

```spl
index=payments sourcetype=agent_transactions
| eval txn_minute=strftime(_time, "%Y-%m-%d %H:%M")
| stats
    count AS txn_count,
    dc(merchant_id) AS unique_merchants,
    sum(transaction_amount) AS total_amount,
    values(merchant_name) AS merchants
    BY agent_session_id, user_id, txn_minute
| where txn_count > 3 OR unique_merchants > 2
| eval velocity_flag=if(txn_count > 5, "critical", if(txn_count > 3, "high", "medium"))
| lookup user_baselines user_id OUTPUT avg_txns_per_session, avg_session_duration
| where txn_count > avg_txns_per_session * 5
| table agent_session_id, user_id, txn_minute, txn_count, unique_merchants, total_amount, merchants, velocity_flag
| sort - txn_count
```

**Sigma -- Agent MCP Server Anomaly Detection (Phase 2)**

```yaml
title: AI Agent Connection to Unverified MCP Server
status: experimental
description: Detects an AI commerce agent establishing a connection to an MCP server not present in the approved server allowlist, which may indicate infrastructure compromise or redirection attack.
logsource:
    product: ecommerce
    service: agent_platform
detection:
    selection:
        event_type: "agent_mcp_connection"
        mcp_server_verified: false
    filter:
        mcp_server_id|exists: true
    condition: selection and not filter
level: high
tags:
    - cfpf.phase2.initial_access
    - attack.t1059
    - flame.ecommerce
    - flame.agentic_commerce
```

**SQL -- UCP Cart Mandate Gift Card Injection Detection (Phase 3-4)**

```sql
SELECT
    cm.mandate_id,
    cm.agent_session_id,
    cm.user_id,
    li.line_item_id,
    li.product_type,
    li.product_name,
    li.recipient_email,
    li.display_status,
    li.amount,
    u.primary_email,
    u.known_emails
FROM ucp_cart_mandates cm
JOIN cart_mandate_line_items li ON cm.mandate_id = li.mandate_id
JOIN user_profiles u ON cm.user_id = u.user_id
WHERE li.product_type IN ('digital_gift_card', 'e_gift_card', 'gift_card')
  AND (
    li.recipient_email NOT IN (SELECT email FROM user_known_emails WHERE user_id = cm.user_id)
    OR li.display_status = 'hidden'
    OR li.added_by = 'agent_auto'
  )
ORDER BY cm.created_at DESC;
```

**Splunk -- UCP Void Return Mass Execution Detection (Phase 4)**

```spl
index=commerce sourcetype=ucp_returns
| search return_tracking_id="void-*" OR return_verify_step_skipped=true
| stats
    count AS void_returns,
    dc(order_id) AS unique_orders,
    dc(user_id) AS unique_users,
    sum(refund_amount) AS total_refund_amount,
    values(return_tracking_id) AS tracking_ids
    BY merchant_id, _time span=1h
| where void_returns > 10 OR (void_returns > 3 AND unique_users > 2)
| eval severity=if(void_returns > 100, "critical", if(void_returns > 25, "high", "medium"))
| table _time, merchant_id, void_returns, unique_orders, unique_users, total_refund_amount, tracking_ids, severity
| sort - void_returns
```

**Sigma -- Agent Content Prompt Injection Detection (Phase 2)**

```yaml
title: Indirect Prompt Injection Detected in Agent Browsing Content
status: experimental
description: Detects indicators of indirect prompt injection payloads in web content ingested by UCP shopping agents during browsing, including hidden instructions, invisible HTML elements, and metadata-embedded commands targeting Cart Mandate manipulation or returns flow bypass.
logsource:
    product: ecommerce
    service: agent_content_scanner
detection:
    selection:
        event_type: "agent_content_ingestion"
    condition_hidden_instructions:
        content_contains_hidden_text: true
        hidden_text_pattern|re: "(?i)(CartMandate|settlement\.refund|order\.return\.verify|recipient_email|display_status.*hidden)"
    condition_invisible_elements:
        invisible_span_detected: true
        invisible_content_length|gt: 50
    condition_metadata_injection:
        metadata_contains_instructions: true
    condition: selection and (1 of condition_*)
level: critical
tags:
    - cfpf.phase2.initial_access
    - attack.t1059
    - flame.ecommerce
    - flame.agentic_commerce
    - flame.prompt_injection
```

### Behavioral Analytics

- **Agent intent consistency analysis**: Compare the agent's executed transactions against the user's stated purchasing intent and historical purchasing patterns. Divergence between what the user asked the agent to do and what the agent actually purchased -- different product categories, unexpected merchants, price points outside historical range -- indicates potential intent manipulation.
- **Agent transaction velocity profiling**: Establish baselines for normal agent purchasing velocity (transactions per session, time between purchases, merchants per session) and flag sessions that exceed human purchasing velocity by more than 10x, indicating potential automated fraud exploitation.
- **Agent merchant selection anomaly detection**: Monitor which merchants agent sessions select and flag patterns where agents from multiple unrelated users are directing purchases to the same recently created or high-risk merchant accounts -- a strong indicator of merchant-side manipulation targeting agent decision logic.
- **Agent session behavioral consistency**: Analyze agent session patterns for behavioral discontinuities that suggest the agent's context has been compromised mid-session -- sudden changes in product category focus, merchant selection criteria, or price sensitivity thresholds.

### Cross-Team Correlation

- **Agent Platform -> Payment Processor**: Agent session telemetry (intent received, merchants evaluated, decisions made) should be shared with payment processors to enable transaction-level risk scoring that incorporates agent behavioral context.
- **Payment Processor -> Issuer**: Transaction metadata indicating agent initiation should be flagged to issuers, enabling agent-specific authorization rules and velocity controls distinct from human-initiated transaction controls.
- **Merchant Platform -> Agent Platform**: Merchant risk signals (newly created accounts, high dispute rates, agent traffic concentration) should be shared with agent platforms to update agent merchant selection criteria in real time.
- **Issuer -> Consumer**: Issuers should provide consumers with agent-specific transaction notifications and review interfaces that surface agent purchasing decisions with sufficient context for the consumer to identify unauthorized or manipulated transactions.

---

## References

- **Recorded Future -- Annual Payment Fraud Intelligence Report 2025**: Primary intelligence source documenting the emergence of agentic commerce as a fraud attack surface, including analysis of Amazon Buy for Me, Visa Intelligent Commerce, and Mastercard Agent Pay; d0ctrine PoC documentation; and structural parallels to early open banking fraud dynamics. [Link](https://www.recordedfuture.com/research/)

- **d0ctrine -- Agentic Fraud Workflow PoC** (April 2025): Underground publication outlining agent-automated fraud execution techniques, human interaction mimicry, and behavioral/device control evasion specific to AI agent commerce platforms.

- **Anthropic -- Autonomous AI Cyber-Espionage Disclosure** (November 2025): First documented case of autonomous AI-orchestrated cyber-espionage with associated fraudulent purchase attempt, demonstrating convergence of AI-enabled threats across fraud and cyber domains.

- **Amazon Buy for Me -- Technical Documentation**: Architecture and authorization flow documentation for Amazon's AI agent purchasing pilot program. [Link](https://www.aboutamazon.com/)

- **Visa -- Intelligent Commerce Specification**: Technical specification for Visa's agentic commerce framework enabling AI agent-initiated payment processing. [Link](https://usa.visa.com/)

- **Mastercard -- Agent Pay Pilot Documentation**: Architecture documentation for Mastercard's AI agent payment delegation framework. [Link](https://www.mastercard.com/)

- **Unit 42 (Palo Alto Networks) -- "Who's Really Shopping? Retail Fraud in the Age of Agentic AI"** (March 2026): Detailed analysis of UCP-specific attack vectors including gift card theft via Cart Mandate payload poisoning and returns fraud via UCP state machine logic hijacking. Documents indirect prompt injection as the primary attack vector for agentic commerce fraud. Introduces organized retail crime (ORC) context ($700K per $1B in sales) and references emerging defense frameworks including Know Your Agent (KYA) and agent reputation scoring. [Link](https://unit42.paloaltonetworks.com/retail-fraud-agentic-ai/)

- **Google -- Universal Commerce Protocol (UCP)** (January 2026): Open-source standard for agentic commerce providing tokenized payments and verifiable credentials for secure agent-to-merchant communication. Unveiled at NRF Big Show.

- **Google -- Agent Payments Protocol (AP2)** (September 2025): Open protocol for securely initiating and transacting agent-led payments across platforms. Compatible with UCP.

- **Palo Alto Networks -- 6 Predictions for the AI Economy: 2026's New Rules of Cybersecurity**: Wendi Whitmore's predictions including Prediction #2 on securing the AI agent, directly applicable to UCP fraud prevention.

- **Related FLAME Threat Paths**: [TP-0025](TP-0025.md) (related -- AI-enabled fraud patterns); [TP-0029: AI Synthetic Identity & Document Forgery](TP-0029-ai-synthetic-identity-document-forgery.md) (enhances -- AI-generated deception techniques applicable to agent manipulation); [TP-0013](TP-0013.md) (related -- credential-based attack patterns applicable to agent authentication); [TP-0031: Refund-as-a-Service](TP-0031-refund-as-a-service-ftid-raas.md) (related -- returns fraud patterns applicable to UCP void returns at scale); [TP-0030: E-Commerce Triangulation Fraud](TP-0030-ecommerce-triangulation-fraud.md) (related -- e-commerce fraud patterns applicable to agent-mediated transactions).

---

## Operational Evidence

### EV-TP0039-2026-002: INTERPOL Confirmation of Agentic AI Fraud

- **Source**: INTERPOL Global Financial Fraud Threat Assessment, 2nd Edition (March 2026)
- **Key Finding**: INTERPOL confirms that "agentic AI systems autonomously executing entire fraud campaigns" have been observed in the wild, corroborating the hypothesis documented in TP-0039. This is no longer theoretical — agentic AI fraud is operational.
- **Confidence**: High

### EV-TP0039-2026-003: Unit 42 UCP-Specific Attack Scenario Analysis

- **Source**: Unit 42 (Palo Alto Networks), "Who's Really Shopping? Retail Fraud in the Age of Agentic AI" (March 20, 2026)
- **Key Finding**: Unit 42 researchers Matt Brady and Christa McHugh documented two concrete UCP-specific attack scenarios using LLM-generated threat modeling: (1) Gift card theft via Cart Mandate payload poisoning, where indirect prompt injection from deals aggregator sites causes the agent to append hidden gift card line items to the UCP checkout JSON-RPC payload with attacker-controlled recipient emails; (2) Returns fraud via logic hijacking, where hidden instructions in product page HTML metadata cause the agent to skip the `order.return.verify` step and trigger `settlement.refund.instant()` with void tracking IDs. The article emphasizes the potential for ORC groups to scale void returns via bot farms, "potentially liquidating a retailer's cash reserves before a human even walks into the office." The article also documents conversations with multiple retail CISOs at the NRF Big Show regarding AI-enabled fraud threats, and references the emergence of the OpenClaw "buy-anything skill (v2.0.0)" as a potential fraud enabler.
- **CFPF Phase Coverage**: P1, P2, P3, P4, P5
- **Confidence**: High -- published by Unit 42 (Palo Alto Networks), a Tier-1 threat intelligence organization with documented retail industry experience

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-04 | FLAME Project | Initial submission |
| 2026-03-20 | FLAME Project | Enriched with INTERPOL GFFTA 2026 confirmation of agentic AI fraud as operational (no longer theoretical) |
| 2026-03-21 | FLAME Project | Major enrichment with Unit 42 UCP-specific attack scenarios (gift card theft via payload poisoning, returns fraud via logic hijacking), Google UCP/AP2 protocol details, indirect prompt injection techniques, new controls (KYA, Cart Mandate verification, returns state machine integrity), ORC context, OpenClaw reference, and 3 new detection rules (DL-0124 through DL-0126) |
