# FLAME Threat Path Index

> 68 threat paths covering 103 fraud types across 18 sectors
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
| TP-0013 | Credential Stuffing to Loyalty Point / Gift Card Account Drain | credential-stuffing, account-takeover | Banking, Cross-sector, Fintech, Retail | P1-P5 |
| TP-0014 | Insider-Enabled Account Fraud at Financial Institution | insider-threat, collusion, account-takeover, data-theft | Banking, Credit-union, Insurance | P1-P5 |
| TP-0015 | Employment Fraud via Brand Impersonation | impersonation, advance-fee-fraud, identity-theft | Healthcare, Staffing, Employment | P1-P5 |
| TP-0016 | First-Party Fraud (Bust-Out) | first-party-fraud, bust-out | Banking, Credit-union | P1, P3, P4, P5 |
| TP-0017 | Pig Butchering (Investment Scam) | investment-scam, social-engineering, authorized-push-payment | Banking, Crypto, Cross-sector | P1-P5 |
| TP-0018 | Deepfake Document Fraud | documentary-fraud, identity-theft, synthetic-identity, new-account-fraud | Banking, Credit-union, Fintech | P1-P3 |
| TP-0019 | Business Identity Theft | identity-theft, business-email-compromise, loan-fraud, account-takeover | Banking, Investment | P1-P5 |
| TP-0020 | Supply Chain Payment Fraud | business-email-compromise, vendor-impersonation, wire-fraud | Banking, Cross-sector | P1-P5 |
| TP-0021 | Healthcare Provider Billing Fraud | healthcare-fraud, phantom-billing, upcoding, hospice-fraud, aba-therapy-fraud, provider-fraud, money-mule | Healthcare, Insurance, Government | P1-P5 |
| TP-0022 | Government Program Fraud (Unemployment/Tax) | benefit-fraud, identity-theft, synthetic-identity, tax-fraud | Government, Banking | P1, P3, P4, P5 |
| TP-0023 | Mobile Banking Trojan / Overlay Attack | account-takeover, malware, unauthorized-transaction | Banking, Fintech, Crypto | P1-P5 |
| TP-0024 | Account-to-Account Instant Payment Fraud (Zelle / FedNow / Pix / UPI) | authorized-push-payment, wire-fraud, payment-diversion | Banking, Fintech, Payments | P1-P5 |
| TP-0025 | GenAI-Enhanced Authorized Push Payment Fraud — Romance Variant | authorized-push-payment, romance-scam, deepfake-fraud, social-engineering | Banking, Cross-sector | P1-P5 |
| TP-0026 | GenAI-Enhanced Authorized Push Payment Fraud — Investment Variant | authorized-push-payment, investment-scam, deepfake-fraud, crypto-laundering | Banking, Crypto, Investment | P1-P5 |
| TP-0027 | Elder Financial Exploitation (Multi-Vector) | social-engineering, authorized-push-payment, account-takeover, romance-scam | Banking, Cross-sector | P1-P5 |
| TP-0028 | DME Phantom Billing (Medicare Fraud) | healthcare-fraud, phantom-billing, provider-fraud, synthetic-medical-fraud, deepfake, money-mule, crypto-laundering | Healthcare, Insurance, Government | P1-P5 |
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
| TP-0039 | Agentic Commerce Fraud | autonomous-ai-fraud, social-engineering, account-takeover, unauthorized-transaction, gift-card-fraud, returns-fraud, refunding-as-a-service | Technology, Retail, Fintech, Payments, Cross-sector | P1-P5 |
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
| TP-0057 | Deepfake-as-a-Service Marketplace Ecosystem | deepfake-as-a-service, deepfake-fraud, ai-face-voice-changer, fraud-as-a-service, impersonation | Cross-sector, Banking, Technology, Employment, Staffing | P1-P5 |
| TP-0058 | Scam Compound Operational Infrastructure | scam-compound-operations, chatbot-enabled-fraud, social-engineering, romance-scam, investment-scam, sextortion, human-trafficking-facilitation | Cross-sector, Banking, Crypto, Investment | P1-P5 |
| TP-0059 | Automated Mule Account Infrastructure | automated-mule-accounts, money-laundering, bot-driven-account-opening, kyc-circumvention | Banking, Crypto, Fintech, Payments | P1-P5 |
| TP-0060 | Investment Fraud TDS Pipeline | traffic-distribution-system, investment-fraud, cloaking, geo-routing, rdga-infrastructure | Banking, Investment, Crypto, Insurance | P1-P5 |
| TP-0061 | Threat Actor Enabling Bulletproof Hosting Infrastructure | bulletproof-hosting, fraud-enabling-infrastructure, hosting-provider-complicity, infrastructure-rotation | Cross-sector, Technology, Telecommunications | P1-P3 |
| TP-0062 | Recovery Fraud — Double-Dip Re-victimization | recovery-fraud, impersonation, advance-fee-fraud, social-engineering | Cross-sector, Banking, Investment | P1-P5 |
| TP-0063 | Organized Counterfeit Goods and Non-Delivery Fraud Networks | purchase-scam, auction-fraud, brand-impersonation, identity-theft, money-mule | Retail, Payments, Cross-sector | P1-P5 |
| TP-0064 | Long-Firm and Organized Business Credit Fraud | long-firm-fraud, bust-out, application-fraud, loan-fraud, invoice-fraud, documentary-fraud | Banking, Cross-sector, Trade | P1-P5 |
| TP-0065 | Organized Mass-Marketing Fraud Infrastructure (Boiler Rooms & Lead Lists) | social-engineering, impersonation, vishing, robodialling-fraud, advance-fee-fraud, investment-scam, fraud-as-a-service | Cross-sector, Banking, Investment, Telecommunications | P1-P5 |
| TP-0066 | Crash-for-Cash and Organized Insurance Fraud Rings | crash-for-cash, insurance-fraud, fraudulent-claim, collusion, documentary-fraud | Insurance, Healthcare | P1-P5 |
| TP-0067 | AiTM Phishing Kit Infrastructure and Session Token Hijacking | aitm-phishing, phishing, account-takeover, credential-stuffing, fraud-as-a-service | Cross-sector, Banking, Fintech, Technology | P1-P5 |
| TP-0068 | Gift Card Fraud Lifecycle — Generation, Tampering, and Monetization | gift-card-fraud, gift-card-tampering, loyalty-point-fraud, social-engineering | Retail, Payments | P1-P5 |

## Coverage by Fraud Type

| Fraud Type | Threat Paths |
|------------|-------------|
| Bec | TP-0002, TP-0004, TP-0006, TP-0007 |
| Aba Therapy Fraud | TP-0021 |
| Account Takeover | TP-0001, TP-0004, TP-0005, TP-0008, TP-0012, TP-0013, TP-0014, TP-0019, TP-0023, TP-0027, TP-0037, TP-0039, TP-0040, TP-0051, TP-0067 |
| Advance Fee Fraud | TP-0015, TP-0062, TP-0065 |
| Ai Accelerated Fraud Infrastructure | TP-0043, TP-0054 |
| Ai Document Fraud | TP-0029 |
| Ai Face Voice Changer | TP-0057 |
| Aitm Phishing | TP-0067 |
| Application Fraud | TP-0003, TP-0029, TP-0053, TP-0064 |
| Approval Phishing | TP-0032 |
| Auction Fraud | TP-0063 |
| Authorized Push Payment | TP-0017, TP-0024, TP-0025, TP-0026, TP-0027 |
| Automated Mule Accounts | TP-0059 |
| Autonomous Ai Fraud | TP-0039 |
| Benefit Fraud | TP-0022, TP-0033 |
| Bnpl Fraud | TP-0040 |
| Bot Driven Account Opening | TP-0059 |
| Bph Migration | TP-0048 |
| Brand Impersonation | TP-0036, TP-0043, TP-0054, TP-0063 |
| Bulletproof Hosting | TP-0061 |
| Business Email Compromise | TP-0019, TP-0020 |
| Bust Out | TP-0016, TP-0064 |
| Calendar Phishing | TP-0050 |
| Card Testing | TP-0038 |
| Chatbot Enabled Fraud | TP-0058 |
| Check Fraud | TP-0009 |
| Cloaking | TP-0060 |
| Cmln Operations | TP-0049 |
| Collusion | TP-0014, TP-0066 |
| Crash For Cash | TP-0066 |
| Credential Stuffing | TP-0013, TP-0051, TP-0067 |
| Crypto Laundering | TP-0008, TP-0026, TP-0028, TP-0032, TP-0044, TP-0045, TP-0047, TP-0055 |
| Crypto Laundering Infrastructure | TP-0049 |
| Data Theft | TP-0014, TP-0034, TP-0035, TP-0038 |
| Deepfake | TP-0007, TP-0028, TP-0052 |
| Deepfake As A Service | TP-0057 |
| Deepfake Fraud | TP-0025, TP-0026, TP-0057 |
| Digital Wallet Fraud | TP-0037 |
| Disability Fraud | TP-0010 |
| Documentary Fraud | TP-0018, TP-0056, TP-0064, TP-0066 |
| Dprk It Worker Fraud | TP-0034 |
| E Skimmer | TP-0035 |
| Employment Fraud | TP-0034 |
| First Party Fraud | TP-0016, TP-0030, TP-0031, TP-0036, TP-0040 |
| Fraud As A Service | TP-0054, TP-0057, TP-0065, TP-0067 |
| Fraud Enabling Infrastructure | TP-0061 |
| Fraudulent Claim | TP-0010, TP-0056, TP-0066 |
| Geo Routing | TP-0060 |
| Ghost Student Fraud | TP-0033 |
| Gift Card Fraud | TP-0039, TP-0068 |
| Gift Card Tampering | TP-0068 |
| Healthcare Fraud | TP-0021, TP-0028 |
| Hospice Fraud | TP-0021 |
| Hosting Provider Complicity | TP-0061 |
| Human Trafficking Facilitation | TP-0047, TP-0058 |
| Identity Theft | TP-0015, TP-0018, TP-0019, TP-0022, TP-0030, TP-0034, TP-0035, TP-0038, TP-0040, TP-0053, TP-0056, TP-0063 |
| Impersonation | TP-0006, TP-0007, TP-0012, TP-0015, TP-0057, TP-0062, TP-0065 |
| Infrastructure Rotation | TP-0061 |
| Insider Threat | TP-0014 |
| Insurance Fraud | TP-0056, TP-0066 |
| Investment Fraud | TP-0060 |
| Investment Scam | TP-0017, TP-0026, TP-0052, TP-0055, TP-0058, TP-0065 |
| Invoice Fraud | TP-0002, TP-0064 |
| Kyc Circumvention | TP-0059 |
| Loan Fraud | TP-0019, TP-0053, TP-0064 |
| Long Firm Fraud | TP-0064 |
| Loyalty Point Fraud | TP-0068 |
| Malvertising | TP-0001, TP-0042 |
| Malware | TP-0023, TP-0035, TP-0044 |
| Money Laundering | TP-0059 |
| Money Mule | TP-0011, TP-0021, TP-0028, TP-0055, TP-0063 |
| New Account Fraud | TP-0003, TP-0018, TP-0029 |
| Nfc Relay | TP-0037 |
| Payment Diversion | TP-0002, TP-0006, TP-0024, TP-0030 |
| Payroll Diversion | TP-0004 |
| Phantom Billing | TP-0021, TP-0028 |
| Phishing | TP-0004, TP-0005, TP-0032, TP-0042, TP-0043, TP-0054, TP-0067 |
| Premium Diversion | TP-0005 |
| Provider Fraud | TP-0010, TP-0021, TP-0028 |
| Purchase Scam | TP-0036, TP-0063 |
| Quishing | TP-0051 |
| Rdga Infrastructure | TP-0041, TP-0060 |
| Recovery Fraud | TP-0062 |
| Refunding As A Service | TP-0031, TP-0039 |
| Returns Fraud | TP-0039 |
| Robodialling Fraud | TP-0065 |
| Romance Scam | TP-0011, TP-0025, TP-0027, TP-0052, TP-0058 |
| Sanctions Evasion Infrastructure | TP-0045, TP-0048 |
| Scam Compound Operations | TP-0047, TP-0058 |
| Sextortion | TP-0052, TP-0058 |
| Social Engineering | TP-0017, TP-0025, TP-0027, TP-0036, TP-0037, TP-0039, TP-0040, TP-0050, TP-0051, TP-0052, TP-0058, TP-0062, TP-0065, TP-0068 |
| State Criminal Convergence | TP-0044, TP-0046, TP-0055 |
| Synthetic Identity | TP-0003, TP-0018, TP-0022, TP-0029, TP-0033 |
| Synthetic Medical Fraud | TP-0028 |
| Tax Fraud | TP-0022 |
| Tds Exploitation | TP-0042 |
| Traffic Distribution System | TP-0060 |
| Unauthorized Transaction | TP-0023, TP-0039 |
| Upcoding | TP-0021 |
| Vehicle Export Fraud | TP-0053 |
| Vendor Impersonation | TP-0020 |
| Vishing | TP-0001, TP-0012, TP-0065 |
| Wire Fraud | TP-0001, TP-0002, TP-0006, TP-0007, TP-0020, TP-0024 |

## Coverage by Sector

| Sector | Threat Paths |
|--------|-------------|
| Banking | TP-0001, TP-0002, TP-0003, TP-0006, TP-0007, TP-0008, TP-0009, TP-0012, TP-0013, TP-0014, TP-0016, TP-0017, TP-0018, TP-0019, TP-0020, TP-0022, TP-0023, TP-0024, TP-0025, TP-0026, TP-0027, TP-0029, TP-0034, TP-0036, TP-0037, TP-0040, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0056, TP-0057, TP-0058, TP-0059, TP-0060, TP-0062, TP-0064, TP-0065, TP-0067 |
| Credit Union | TP-0009, TP-0012, TP-0014, TP-0016, TP-0018 |
| Cross Sector | TP-0002, TP-0004, TP-0006, TP-0007, TP-0011, TP-0013, TP-0017, TP-0020, TP-0025, TP-0027, TP-0039, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0048, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0057, TP-0058, TP-0061, TP-0062, TP-0063, TP-0064, TP-0065, TP-0067 |
| Crypto | TP-0008, TP-0017, TP-0023, TP-0026, TP-0032, TP-0034, TP-0041, TP-0043, TP-0044, TP-0045, TP-0047, TP-0049, TP-0052, TP-0054, TP-0055, TP-0058, TP-0059, TP-0060 |
| Education | TP-0033 |
| Employment | TP-0015, TP-0034, TP-0057 |
| Fintech | TP-0003, TP-0008, TP-0013, TP-0018, TP-0023, TP-0024, TP-0029, TP-0035, TP-0037, TP-0038, TP-0039, TP-0040, TP-0059, TP-0067 |
| Government | TP-0021, TP-0022, TP-0028, TP-0033, TP-0034, TP-0056 |
| Healthcare | TP-0015, TP-0021, TP-0028, TP-0034, TP-0056, TP-0066 |
| Insurance | TP-0005, TP-0010, TP-0014, TP-0021, TP-0028, TP-0056, TP-0060, TP-0066 |
| Investment | TP-0019, TP-0026, TP-0041, TP-0052, TP-0058, TP-0060, TP-0062, TP-0065 |
| Payments | TP-0024, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0043, TP-0046, TP-0051, TP-0054, TP-0059, TP-0063, TP-0068 |
| Retail | TP-0013, TP-0030, TP-0031, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0051, TP-0063, TP-0068 |
| Staffing | TP-0015, TP-0057 |
| Technology | TP-0034, TP-0039, TP-0054, TP-0057, TP-0061, TP-0067 |
| Telecommunications | TP-0061, TP-0065 |
| Trade | TP-0064 |
| Web3 | TP-0032 |

## Framework Coverage Status

| Framework | Mapping Status | Notes |
|-----------|---------------|-------|
| FS-ISAC CFPF | All 68 TPs mapped | Primary organizational structure |
| MITRE ATT&CK | 63 of 68 TPs mapped | Where applicable (some fraud-only TPs lack ATT&CK equivalents) |
| Stripe FT3 | Mapped (62/68) | MIT-licensed JSON vendored in data/ft3/ |
| MITRE F3 | Awaiting release | Will map when F3 ships |
| Group-IB Fraud Matrix | 68 of 68 TPs mapped | 10-stage lifecycle; stage names referenced for interoperability |
| Group-IB UCFF | 68 of 68 TPs aligned | 7-domain lifecycle maturity assessment |

## Cross-Threat Path Connections

The fraud ecosystem is interconnected. Key relationships:

```
TP-0011 (Romance/Mule Recruitment) ──provides mule accounts to──▶ TP-0001, TP-0002, TP-0006, TP-0009
TP-0003 (Synthetic Identity) ──provides fraudulent accounts to──▶ TP-0009, TP-0013
TP-0014 (Insider Threat) ──provides customer data to──▶ TP-0001, TP-0005, TP-0008, TP-0012
TP-0007 (Deepfake Voice) ──enhances social engineering in──▶ TP-0001, TP-0006, TP-0012
TP-0008 (SIM Swap) ──bypasses MFA controls in──▶ TP-0001, TP-0005, TP-0013
```
