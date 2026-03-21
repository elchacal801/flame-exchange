# FLAME Threat Path Index

> 61 threat paths covering 81 fraud types across 16 sectors
> Framework-agnostic: mapped to CFPF phases with cross-references to FT3, ATT&CK, and Group-IB Fraud Matrix

## Coverage Summary

| ID | Title | Fraud Types | Sectors | CFPF Phases |
|----|-------|-------------|---------|-------------|
| TP-0001 | Treasury Management ATO via Malvertising and Vishing | account-takeover, vishing, wire-fraud, malvertising | Banking | P1-P5 |
| TP-0002 | Business Email Compromise — Vendor Impersonation Wire Fraud | BEC, wire-fraud, invoice-fraud, payment-diversion | Banking, Cross-sector | P1-P5 |
| TP-0003 | Synthetic Identity — Credit Card Bust-Out | synthetic-identity, new-account-fraud, application-fraud | Banking, Fintech | P1-P5 |
| TP-0004 | Payroll Diversion via HR Portal Compromise | payroll-diversion, BEC, phishing, account-takeover | Cross-sector | P1-P5 |
| TP-0005 | Insurance Premium Diversion via Agent Portal ATO | account-takeover, premium-diversion, phishing | Insurance | P1-P5 |
| TP-0006 | Real Estate Wire Fraud — Closing Scam | BEC, wire-fraud, payment-diversion, impersonation | Banking, Cross-sector | P1-P5 |
| TP-0007 | Deepfake Voice Authorization for Wire Transfer | wire-fraud, impersonation, BEC, deepfake | Banking, Cross-sector | P1-P5 |
| TP-0008 | SIM Swap to Cryptocurrency Exchange ATO | account-takeover, crypto-laundering | Crypto, Fintech, Banking | P1-P5 |
| TP-0009 | Check Washing and Fraudulent Mobile Deposit | check-fraud | Banking, Credit-union | P1-P5 |
| TP-0010 | Disability Insurance Fraud via Fabricated Medical Documentation | fraudulent-claim, disability-fraud, provider-fraud | Insurance | P1-P5 |
| TP-0011 | Romance Scam to Money Mule Recruitment Pipeline | romance-scam, money-mule | Cross-sector | P1-P5 |
| TP-0012 | Authorized Push Payment Fraud — Tech Support / Bank Impersonation | vishing, impersonation, account-takeover | Banking, Credit-union | P1-P5 |
| TP-0013 | Credential Stuffing to Loyalty Point / Gift Card Account Drain | credential-stuffing, account-takeover | Fintech, Banking, Cross-sector | P1-P5 |
| TP-0014 | Insider-Enabled Account Fraud at Financial Institution | insider-threat, collusion, account-takeover, data-theft | Banking, Credit-union, Insurance | P1-P5 |
| TP-0015 | Employment Fraud via Brand Impersonation | impersonation, advance-fee-fraud, identity-theft | Healthcare, Staffing, Employment | P1-P5 |
| TP-0016 | First-Party Fraud (Bust-Out) | first-party-fraud, bust-out | Banking, Credit-union | P1, P3, P4, P5 |
| TP-0017 | Pig Butchering (Investment Scam) | investment-scam, social-engineering, authorized-push-payment | Banking, Crypto, Cross-sector | P1-P5 |
| TP-0018 | Deepfake Document Fraud | documentary-fraud, identity-theft, synthetic-identity, new-account-fraud | Banking, Credit-union, Fintech | P1-P3 |
| TP-0019 | Business Identity Theft | identity-theft, business-email-compromise, loan-fraud, account-takeover | Banking, Investment | P1-P5 |
| TP-0020 | Supply Chain Payment Fraud | business-email-compromise, vendor-impersonation, wire-fraud | Banking, Cross-sector | P1-P5 |
| TP-0021 | Healthcare Provider Billing Fraud | healthcare-fraud, phantom-billing, upcoding | Healthcare, Insurance | P3-P5 |
| TP-0022 | Government Program Fraud (Unemployment/Tax) | benefit-fraud, identity-theft, synthetic-identity, tax-fraud | Government, Banking | P1, P3, P4, P5 |
| TP-0023 | Mobile Banking Trojan / Overlay Attack | account-takeover, malware, unauthorized-transaction | Banking, Fintech, Crypto | P1-P5 |
| TP-0024 | Account-to-Account Instant Payment Fraud (Zelle / FedNow / Pix / UPI) | authorized-push-payment, wire-fraud, payment-diversion | Banking, Fintech, Payments | P1-P5 |
| TP-0025 | GenAI-Enhanced Authorized Push Payment Fraud — Romance Variant | authorized-push-payment, romance-scam, deepfake-fraud, social-engineering | Banking, Cross-sector | P1-P5 |
| TP-0026 | GenAI-Enhanced Authorized Push Payment Fraud — Investment Variant | authorized-push-payment, investment-scam, deepfake-fraud, crypto-laundering | Banking, Crypto, Investment | P1-P5 |
| TP-0027 | Elder Financial Exploitation (Multi-Vector) | social-engineering, authorized-push-payment, account-takeover, romance-scam | Banking, Cross-sector | P1-P5 |
| TP-0028 | DME Phantom Billing (Medicare Fraud) | healthcare-fraud, phantom-billing, provider-fraud, synthetic-medical-fraud | Healthcare, Insurance, Government | P1-P5 |
| TP-0029 | AI Synthetic Identity & Document Forgery | synthetic-identity, ai-document-fraud, new-account-fraud, application-fraud | Banking, Fintech | P1-P5 |
| TP-0030 | E-Commerce Triangulation Fraud | first-party-fraud, identity-theft, payment-diversion | Retail | P1-P5 |
| TP-0031 | Refund-as-a-Service (FTID / RaaS) | first-party-fraud, refunding-as-a-service | Retail | P1-P5 |
| TP-0032 | Web3 Wallet Drainer / Approval Phishing | approval-phishing, crypto-laundering, phishing | Web3, Crypto | P1-P5 |
| TP-0033 | Ghost Student Financial Aid Botnets | ghost-student-fraud, synthetic-identity, benefit-fraud | Education, Government | P1-P5 |
| TP-0034 | DPRK State-Sponsored IT Worker Fraud & Data Extortion | dprk-it-worker-fraud, employment-fraud, identity-theft, data-theft | Technology, Banking, Crypto, Healthcare, Government, Employment | P1-P5 |
| TP-0035 | Magecart E-Skimmer Data Compromise | e-skimmer, data-theft, malware, identity-theft | Retail, Payments, Fintech | P1-P5 |
| TP-0036 | Purchase Scam Merchant Networks | purchase-scam, brand-impersonation, first-party-fraud, social-engineering | Retail, Payments, Banking | P1-P5 |
| TP-0037 | Digital Wallet Fraud & NFC Relay Attacks | digital-wallet-fraud, nfc-relay, account-takeover, social-engineering | Banking, Fintech, Payments, Retail | P1-P5 |
| TP-0038 | Card Testing Infrastructure Abuse | card-testing, identity-theft, data-theft | Payments, Retail, Fintech | P1-P5 |
| TP-0039 | Agentic Commerce Fraud | autonomous-ai-fraud, social-engineering, account-takeover, unauthorized-transaction | Technology, Retail, Fintech, Payments, Cross-sector | P1-P5 |
| TP-0040 | BNPL Multi-Provider Fraud — Synthetic Stacking, ATO & Friendly Fraud | bnpl-fraud, first-party-fraud, identity-theft, account-takeover, social-engineering | Retail, Payments, Fintech, Banking | P1-P5 |
| TP-0041 | RDGA-Based Infrastructure Campaigns | rdga-infrastructure | Cross-sector, Banking, Crypto, Investment | P1-P5 |
| TP-0042 | Traffic Distribution System (TDS) Chain Exploitation | tds-exploitation, malvertising, phishing | Cross-sector, Banking, Payments, Retail | P1-P5 |
| TP-0043 | AI-Accelerated Fraud Infrastructure Generation | ai-accelerated-fraud-infrastructure, phishing, brand-impersonation | Cross-sector, Banking, Payments, Crypto | P1-P5 |
| TP-0044 | State-Criminal Infrastructure Convergence | state-criminal-convergence, crypto-laundering, malware | Banking, Crypto, Cross-sector | P1-P5 |
| TP-0045 | Sanctions Evasion via Fraud Infrastructure | sanctions-evasion-infrastructure, crypto-laundering | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0046 | Geopolitically-Timed Fraud Campaigns | state-criminal-convergence | Banking, Payments, Cross-sector | P1-P5 |
| TP-0047 | Human Trafficking-Linked Fraud Infrastructure | human-trafficking-facilitation, scam-compound-operations, crypto-laundering | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0048 | Bulletproof Hosting Migration Patterns | bph-migration, sanctions-evasion-infrastructure | Cross-sector | P1-P5 |
| TP-0049 | Cryptocurrency Laundering Infrastructure | crypto-laundering-infrastructure, cmln-operations | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0050 | Calendar/Invite Injection Phishing | calendar-phishing, social-engineering | Banking, Cross-sector | P1-P5 |
| TP-0051 | QR Code Payment Fraud / Quishing | quishing, credential-stuffing, account-takeover, social-engineering | Banking, Payments, Retail, Cross-sector | P1-P5 |
| TP-0052 | Sextortion-Investment Hybrid Fraud | sextortion, investment-scam, deepfake, social-engineering, romance-scam | Banking, Crypto, Investment, Cross-sector | P1-P5 |
| TP-0053 | Vehicle Export Financing Fraud | vehicle-export-fraud, identity-theft, application-fraud, loan-fraud | Banking, Cross-sector | P1-P5 |
| TP-0054 | Fraud-as-a-Service (FaaS) Platforms | fraud-as-a-service, ai-accelerated-fraud-infrastructure, phishing, brand-impersonation | Cross-sector, Banking, Payments, Crypto, Technology | P1-P5 |
| TP-0055 | Crypto Fraud–Terrorism/Narco Financing Nexus | crypto-laundering, investment-scam, state-criminal-convergence, money-mule | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0056 | Insurance Claims Fraud (Motor/Medical) | insurance-fraud, fraudulent-claim, identity-theft, documentary-fraud | Insurance, Healthcare, Banking, Government | P1-P5 |
| TP-0057 | Deepfake-as-a-Service (DaaS) Marketplace Ecosystem | deepfake-as-a-service, deepfake-fraud, ai-face-voice-changer, fraud-as-a-service, impersonation | Cross-sector, Banking, Crypto, Technology, Employment | P1-P5 |
| TP-0058 | Scam Compound Operational Infrastructure | scam-compound-operations, social-engineering, investment-scam, romance-scam, chatbot-enabled-fraud, sextortion | Cross-sector, Banking, Crypto, Investment | P1-P5 |
| TP-0059 | Automated Mule Account Infrastructure | automated-mule-infrastructure, money-mule, new-account-fraud, synthetic-identity, application-fraud | Banking, Payments, Crypto, Fintech | P1-P5 |
| TP-0060 | Investment Scam TDS Integrated Pipeline | investment-scam, investment-tds-pipeline, tds-exploitation, rdga-infrastructure | Investment, Banking, Crypto | P1-P5 |
| TP-0061 | Threat Activity Enabler (TAE) Bulletproof Hosting Infrastructure | fraud-as-a-service, state-criminal-convergence, sanctions-evasion-infrastructure, bph-migration | Cross-sector, Banking, Crypto, Technology | P1-P5 |

## Coverage by Fraud Type

| Fraud Type | Threat Paths |
|------------|-------------|
| Bec | TP-0002, TP-0004, TP-0006, TP-0007 |
| Account Takeover | TP-0001, TP-0004, TP-0005, TP-0008, TP-0012, TP-0013, TP-0014, TP-0019, TP-0023, TP-0027, TP-0037, TP-0039, TP-0040, TP-0051 |
| Advance Fee Fraud | TP-0015 |
| Ai Accelerated Fraud Infrastructure | TP-0043, TP-0054 |
| Ai Document Fraud | TP-0029 |
| Ai Face Voice Changer | TP-0057 |
| Automated Mule Infrastructure | TP-0059 |
| Application Fraud | TP-0003, TP-0029, TP-0053, TP-0059 |
| Approval Phishing | TP-0032 |
| Authorized Push Payment | TP-0017, TP-0024, TP-0025, TP-0026, TP-0027 |
| Autonomous Ai Fraud | TP-0039 |
| Benefit Fraud | TP-0022, TP-0033 |
| Bnpl Fraud | TP-0040 |
| Bph Migration | TP-0048, TP-0061 |
| Brand Impersonation | TP-0036, TP-0043, TP-0054 |
| Business Email Compromise | TP-0019, TP-0020 |
| Bust Out | TP-0016 |
| Calendar Phishing | TP-0050 |
| Card Testing | TP-0038 |
| Chatbot Enabled Fraud | TP-0058 |
| Check Fraud | TP-0009 |
| Cmln Operations | TP-0049 |
| Collusion | TP-0014 |
| Credential Stuffing | TP-0013, TP-0051 |
| Crypto Laundering | TP-0008, TP-0026, TP-0032, TP-0044, TP-0045, TP-0047, TP-0055 |
| Crypto Laundering Infrastructure | TP-0049 |
| Data Theft | TP-0014, TP-0034, TP-0035, TP-0038 |
| Deepfake | TP-0007, TP-0052 |
| Deepfake As A Service | TP-0057 |
| Deepfake Fraud | TP-0025, TP-0026, TP-0057 |
| Digital Wallet Fraud | TP-0037 |
| Disability Fraud | TP-0010 |
| Documentary Fraud | TP-0018, TP-0056 |
| Dprk It Worker Fraud | TP-0034 |
| E Skimmer | TP-0035 |
| Employment Fraud | TP-0034 |
| First Party Fraud | TP-0016, TP-0030, TP-0031, TP-0036, TP-0040 |
| Fraud As A Service | TP-0054, TP-0057, TP-0061 |
| Fraudulent Claim | TP-0010, TP-0056 |
| Ghost Student Fraud | TP-0033 |
| Healthcare Fraud | TP-0021, TP-0028 |
| Human Trafficking Facilitation | TP-0047 |
| Identity Theft | TP-0015, TP-0018, TP-0019, TP-0022, TP-0030, TP-0034, TP-0035, TP-0038, TP-0040, TP-0053, TP-0056 |
| Impersonation | TP-0006, TP-0007, TP-0012, TP-0015, TP-0057 |
| Insider Threat | TP-0014 |
| Insurance Fraud | TP-0056 |
| Investment Scam | TP-0017, TP-0026, TP-0052, TP-0055, TP-0058, TP-0060 |
| Investment Tds Pipeline | TP-0060 |
| Invoice Fraud | TP-0002 |
| Loan Fraud | TP-0019, TP-0053 |
| Malvertising | TP-0001, TP-0042 |
| Malware | TP-0023, TP-0035, TP-0044 |
| Money Mule | TP-0011, TP-0055, TP-0059 |
| New Account Fraud | TP-0003, TP-0018, TP-0029, TP-0059 |
| Nfc Relay | TP-0037 |
| Payment Diversion | TP-0002, TP-0006, TP-0024, TP-0030 |
| Payroll Diversion | TP-0004 |
| Phantom Billing | TP-0021, TP-0028 |
| Phishing | TP-0004, TP-0005, TP-0032, TP-0042, TP-0043, TP-0054 |
| Premium Diversion | TP-0005 |
| Provider Fraud | TP-0010, TP-0028 |
| Purchase Scam | TP-0036 |
| Quishing | TP-0051 |
| Rdga Infrastructure | TP-0041, TP-0060 |
| Refunding As A Service | TP-0031 |
| Romance Scam | TP-0011, TP-0025, TP-0027, TP-0052, TP-0058 |
| Sanctions Evasion Infrastructure | TP-0045, TP-0048, TP-0061 |
| Scam Compound Operations | TP-0047, TP-0058 |
| Sextortion | TP-0052, TP-0058 |
| Social Engineering | TP-0017, TP-0025, TP-0027, TP-0036, TP-0037, TP-0039, TP-0040, TP-0050, TP-0051, TP-0052, TP-0058 |
| State Criminal Convergence | TP-0044, TP-0046, TP-0055, TP-0061 |
| Synthetic Identity | TP-0003, TP-0018, TP-0022, TP-0029, TP-0033, TP-0059 |
| Synthetic Medical Fraud | TP-0028 |
| Tax Fraud | TP-0022 |
| Tds Exploitation | TP-0042, TP-0060 |
| Unauthorized Transaction | TP-0023, TP-0039 |
| Upcoding | TP-0021 |
| Vehicle Export Fraud | TP-0053 |
| Vendor Impersonation | TP-0020 |
| Vishing | TP-0001, TP-0012 |
| Wire Fraud | TP-0001, TP-0002, TP-0006, TP-0007, TP-0020, TP-0024 |

## Coverage by Sector

| Sector | Threat Paths |
|--------|-------------|
| Banking | TP-0001, TP-0002, TP-0003, TP-0006, TP-0007, TP-0008, TP-0009, TP-0012, TP-0013, TP-0014, TP-0016, TP-0017, TP-0018, TP-0019, TP-0020, TP-0022, TP-0023, TP-0024, TP-0025, TP-0026, TP-0027, TP-0029, TP-0034, TP-0036, TP-0037, TP-0040, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0056, TP-0057, TP-0058, TP-0059, TP-0060, TP-0061 |
| Credit Union | TP-0009, TP-0012, TP-0014, TP-0016, TP-0018 |
| Cross Sector | TP-0002, TP-0004, TP-0006, TP-0007, TP-0011, TP-0013, TP-0017, TP-0020, TP-0025, TP-0027, TP-0039, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0048, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0057, TP-0058, TP-0061 |
| Crypto | TP-0008, TP-0017, TP-0023, TP-0026, TP-0032, TP-0034, TP-0041, TP-0043, TP-0044, TP-0045, TP-0047, TP-0049, TP-0052, TP-0054, TP-0055, TP-0058, TP-0059, TP-0061 |
| Education | TP-0033 |
| Employment | TP-0015, TP-0034, TP-0057 |
| Fintech | TP-0003, TP-0008, TP-0013, TP-0018, TP-0023, TP-0024, TP-0029, TP-0035, TP-0037, TP-0038, TP-0039, TP-0040, TP-0059 |
| Government | TP-0022, TP-0028, TP-0033, TP-0034, TP-0056 |
| Healthcare | TP-0015, TP-0021, TP-0028, TP-0034, TP-0056 |
| Insurance | TP-0005, TP-0010, TP-0014, TP-0021, TP-0028, TP-0056 |
| Investment | TP-0019, TP-0026, TP-0041, TP-0052, TP-0058, TP-0060 |
| Payments | TP-0024, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0043, TP-0046, TP-0051, TP-0054, TP-0059 |
| Retail | TP-0030, TP-0031, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0051, TP-0060 |
| Staffing | TP-0015, TP-0057 |
| Technology | TP-0034, TP-0039, TP-0054, TP-0057, TP-0061 |
| Web3 | TP-0032 |

## Framework Coverage Status

| Framework | Mapping Status | Notes |
|-----------|---------------|-------|
| FS-ISAC CFPF | All 61 TPs mapped | Primary organizational structure |
| MITRE ATT&CK | 55 of 61 TPs mapped | Where applicable (some fraud-only TPs lack ATT&CK equivalents) |
| Stripe FT3 | Mapped (55/61) | MIT-licensed JSON vendored in data/ft3/ |
| MITRE F3 | Awaiting release | Will map when F3 ships |
| Group-IB Fraud Matrix | 61 of 61 TPs mapped | 10-stage lifecycle; stage names referenced for interoperability |
| Group-IB UCFF | 61 of 61 TPs aligned | 7-domain lifecycle maturity assessment |

## Cross-Threat Path Connections

The fraud ecosystem is interconnected. Key relationships:

```
TP-0011 (Romance/Mule Recruitment) ──provides mule accounts to──▶ TP-0001, TP-0002, TP-0006, TP-0009
TP-0003 (Synthetic Identity) ──provides fraudulent accounts to──▶ TP-0009, TP-0013
TP-0014 (Insider Threat) ──provides customer data to──▶ TP-0001, TP-0005, TP-0008, TP-0012
TP-0007 (Deepfake Voice) ──enhances social engineering in──▶ TP-0001, TP-0006, TP-0012
TP-0008 (SIM Swap) ──bypasses MFA controls in──▶ TP-0001, TP-0005, TP-0013
```
