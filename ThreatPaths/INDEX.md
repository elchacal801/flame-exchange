# FLAME Threat Path Index

> 89 threat paths covering 141 fraud types across 24 sectors
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
| TP-0069 | Smishing PhaaS Ecosystem — Darcula, Smishing Triad, and Mass-Messaging Credential Harvest | smishing, phishing, card-not-present-fraud, identity-theft, fraud-as-a-service | Cross-sector, Banking, Retail, Payments, Government, Transportation | P1-P5 |
| TP-0070 | Travel Booking Fraud & Fake OTA Networks | travel-booking-fraud, buy-for-you-fraud, fake-ota, loyalty-point-laundering | Travel, Payments, Cross-sector | P1-P5 |
| TP-0071 | IRSF & Telecom Revenue Share Fraud | irsf, premium-rate-fraud, telecom-revenue-fraud, wangiri | Telecommunications | P1-P5 |
| TP-0072 | Telecom Subscription & Billing Fraud | subscription-fraud, telecom-billing-fraud, premium-sms-fraud | Telecommunications | P2-P5 |
| TP-0073 | Real Estate Title Fraud & Deed Theft | title-fraud, deed-theft, seller-impersonation, appraisal-fraud | Real-estate | P1-P5 |
| TP-0074 | Ghost Broking & Unauthorized Insurance Portals | ghost-broking, ghost-portal, insurance-policy-fraud, unlicensed-insurance | Insurance | P1-P5 |
| TP-0075 | Friendly Fraud & Chargeback Abuse | friendly-fraud, chargeback-abuse, first-party-misuse, dispute-fraud | Payments, Ecommerce, Retail | P4-P5 |
| TP-0076 | Affiliate Network Fraud & Invalid Traffic | affiliate-fraud, click-fraud, ad-fraud, cookie-stuffing, invalid-traffic | Ecommerce, Technology | P1-P5 |
| TP-0077 | AI-Generated Insurance Claims Fraud | ai-generated-claims, deepfake-claims, document-fraud, insurance-fraud | Insurance | P3-P5 |
| TP-0078 | Stablecoin Laundering via Centralized Exchange Hot Wallet Pipelines | crypto-laundering, crypto-laundering-infrastructure, money-laundering | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0079 | Cheap gTLD and PaaS Subdomain Abuse for Fraud Infrastructure at Scale | phishing, brand-impersonation, credential-harvesting, fraud-enabling-infrastructure, paas-subdomain-abuse | Cross-sector, Banking, Crypto, Payments, Government | P1-P5 |
| TP-0080 | Stablecoin Freeze-Evasion via Wrapped Tokens, Decentralized Stablecoins, and Cross-Chain Bridges | crypto-laundering, stablecoin-freeze-evasion, sanctions-evasion-infrastructure, money-laundering | Crypto, Banking, Cross-sector | P1-P5 |
| TP-0081 | Vishing-Led Identity Abuse and Hybrid Social Engineering for Financial Fraud | vishing, account-takeover, social-engineering, BEC, fake-captcha-fraud | Banking, Cross-sector, Technology, Insurance | P1-P5 |
| TP-0082 | Gold Courier Scam — Physical Precious Metal Cash-Out | social-engineering, impersonation, authorized-push-payment, elder-exploitation | Banking, Cross-sector | P1-P5 |
| TP-0083 | Investment Club Scam — Social Media Insider Group Fraud | investment-scam, social-engineering, authorized-push-payment, crypto-laundering | Investment, Banking, Crypto | P1-P5 |
| TP-0084 | Government Impersonation — Authority-Based Authorized Push Payment Fraud | impersonation, authorized-push-payment, social-engineering, elder-exploitation | Banking, Cross-sector, Government | P1-P5 |
| TP-0085 | Crypto ATM/Kiosk Directed Fraud — Physical-to-Digital Monetization Channel | crypto-laundering, authorized-push-payment, elder-exploitation | Banking, Crypto, Cross-sector | P3-P5 |
| TP-0086 | Crisis-Exploitation Fraud Infrastructure | phishing, brand-impersonation, credential-harvesting, investment-scam, impersonation, fraud-enabling-infrastructure | Government, Banking, Insurance, Cross-sector | P1-P5 |
| TP-0087 | Infostealer-to-Fraud Pipeline — MaaS Credential Harvesting to Financial Fraud | credential-harvesting, account-takeover, data-theft, fraud-as-a-service, crypto-laundering, unauthorized-transaction | Banking, Crypto, E-commerce, Technology, Cross-sector | P1-P5 |
| TP-0088 | Logistics Sector Spearphishing — Carrier Impersonation and Freight Document Fraud | phishing, brand-impersonation, social-engineering, credential-harvesting, fraud-enabling-infrastructure | Logistics, Transportation, Cross-sector | P1-P5 |
| TP-0089 | TAE Upstream Transit Provider Complicity — Structural Enablement of Malicious Hosting | bulletproof-hosting, fraud-enabling-infrastructure, sanctions-evasion-infrastructure, hosting-provider-complicity, bph-migration | Technology, Telecommunications, Cross-sector | P1-P5 |

## Coverage by Fraud Type

| Fraud Type | Threat Paths |
|------------|-------------|
| Bec | TP-0002, TP-0004, TP-0006, TP-0007, TP-0081 |
| Aba Therapy Fraud | TP-0021 |
| Account Takeover | TP-0001, TP-0004, TP-0005, TP-0008, TP-0012, TP-0013, TP-0014, TP-0019, TP-0023, TP-0027, TP-0037, TP-0039, TP-0040, TP-0051, TP-0067, TP-0081, TP-0087 |
| Ad Fraud | TP-0076 |
| Advance Fee Fraud | TP-0015, TP-0062, TP-0065 |
| Affiliate Fraud | TP-0076 |
| Ai Accelerated Fraud Infrastructure | TP-0043, TP-0054 |
| Ai Document Fraud | TP-0029 |
| Ai Face Voice Changer | TP-0057 |
| Ai Generated Claims | TP-0077 |
| Aitm Phishing | TP-0067 |
| Application Fraud | TP-0003, TP-0029, TP-0053, TP-0064 |
| Appraisal Fraud | TP-0073 |
| Approval Phishing | TP-0032 |
| Auction Fraud | TP-0063 |
| Authorized Push Payment | TP-0017, TP-0024, TP-0025, TP-0026, TP-0027, TP-0082, TP-0083, TP-0084, TP-0085 |
| Automated Mule Accounts | TP-0059 |
| Autonomous Ai Fraud | TP-0039 |
| Benefit Fraud | TP-0022, TP-0033 |
| Bnpl Fraud | TP-0040 |
| Bot Driven Account Opening | TP-0059 |
| Bph Migration | TP-0048, TP-0089 |
| Brand Impersonation | TP-0036, TP-0043, TP-0054, TP-0063, TP-0079, TP-0086, TP-0088 |
| Bulletproof Hosting | TP-0061, TP-0089 |
| Business Email Compromise | TP-0019, TP-0020 |
| Bust Out | TP-0016, TP-0064 |
| Buy For You Fraud | TP-0070 |
| Calendar Phishing | TP-0050 |
| Card Not Present Fraud | TP-0069 |
| Card Testing | TP-0038 |
| Chargeback Abuse | TP-0075 |
| Chatbot Enabled Fraud | TP-0058 |
| Check Fraud | TP-0009 |
| Click Fraud | TP-0076 |
| Cloaking | TP-0060 |
| Cmln Operations | TP-0049 |
| Collusion | TP-0014, TP-0066 |
| Cookie Stuffing | TP-0076 |
| Crash For Cash | TP-0066 |
| Credential Harvesting | TP-0079, TP-0086, TP-0087, TP-0088 |
| Credential Stuffing | TP-0013, TP-0051, TP-0067 |
| Crypto Laundering | TP-0008, TP-0026, TP-0028, TP-0032, TP-0044, TP-0045, TP-0047, TP-0055, TP-0078, TP-0080, TP-0083, TP-0085, TP-0087 |
| Crypto Laundering Infrastructure | TP-0049, TP-0078 |
| Data Theft | TP-0014, TP-0034, TP-0035, TP-0038, TP-0087 |
| Deed Theft | TP-0073 |
| Deepfake | TP-0007, TP-0028, TP-0052 |
| Deepfake As A Service | TP-0057 |
| Deepfake Claims | TP-0077 |
| Deepfake Fraud | TP-0025, TP-0026, TP-0057 |
| Digital Wallet Fraud | TP-0037 |
| Disability Fraud | TP-0010 |
| Dispute Fraud | TP-0075 |
| Document Fraud | TP-0077 |
| Documentary Fraud | TP-0018, TP-0056, TP-0064, TP-0066 |
| Dprk It Worker Fraud | TP-0034 |
| E Skimmer | TP-0035 |
| Elder Exploitation | TP-0082, TP-0084, TP-0085 |
| Employment Fraud | TP-0034 |
| Fake Captcha Fraud | TP-0081 |
| Fake Ota | TP-0070 |
| First Party Fraud | TP-0016, TP-0030, TP-0031, TP-0036, TP-0040 |
| First Party Misuse | TP-0075 |
| Fraud As A Service | TP-0054, TP-0057, TP-0065, TP-0067, TP-0069, TP-0087 |
| Fraud Enabling Infrastructure | TP-0061, TP-0079, TP-0086, TP-0088, TP-0089 |
| Fraudulent Claim | TP-0010, TP-0056, TP-0066 |
| Friendly Fraud | TP-0075 |
| Geo Routing | TP-0060 |
| Ghost Broking | TP-0074 |
| Ghost Portal | TP-0074 |
| Ghost Student Fraud | TP-0033 |
| Gift Card Fraud | TP-0039, TP-0068 |
| Gift Card Tampering | TP-0068 |
| Healthcare Fraud | TP-0021, TP-0028 |
| Hospice Fraud | TP-0021 |
| Hosting Provider Complicity | TP-0061, TP-0089 |
| Human Trafficking Facilitation | TP-0047, TP-0058 |
| Identity Theft | TP-0015, TP-0018, TP-0019, TP-0022, TP-0030, TP-0034, TP-0035, TP-0038, TP-0040, TP-0053, TP-0056, TP-0063, TP-0069 |
| Impersonation | TP-0006, TP-0007, TP-0012, TP-0015, TP-0057, TP-0062, TP-0065, TP-0082, TP-0084, TP-0086 |
| Infrastructure Rotation | TP-0061 |
| Insider Threat | TP-0014 |
| Insurance Fraud | TP-0056, TP-0066, TP-0077 |
| Insurance Policy Fraud | TP-0074 |
| Invalid Traffic | TP-0076 |
| Investment Fraud | TP-0060 |
| Investment Scam | TP-0017, TP-0026, TP-0052, TP-0055, TP-0058, TP-0065, TP-0083, TP-0086 |
| Invoice Fraud | TP-0002, TP-0064 |
| Irsf | TP-0071 |
| Kyc Circumvention | TP-0059 |
| Loan Fraud | TP-0019, TP-0053, TP-0064 |
| Long Firm Fraud | TP-0064 |
| Loyalty Point Fraud | TP-0068 |
| Loyalty Point Laundering | TP-0070 |
| Malvertising | TP-0001, TP-0042 |
| Malware | TP-0023, TP-0035, TP-0044 |
| Money Laundering | TP-0059, TP-0078, TP-0080 |
| Money Mule | TP-0011, TP-0021, TP-0028, TP-0055, TP-0063 |
| New Account Fraud | TP-0003, TP-0018, TP-0029 |
| Nfc Relay | TP-0037 |
| Paas Subdomain Abuse | TP-0079 |
| Payment Diversion | TP-0002, TP-0006, TP-0024, TP-0030 |
| Payroll Diversion | TP-0004 |
| Phantom Billing | TP-0021, TP-0028 |
| Phishing | TP-0004, TP-0005, TP-0032, TP-0042, TP-0043, TP-0054, TP-0067, TP-0069, TP-0079, TP-0086, TP-0088 |
| Premium Diversion | TP-0005 |
| Premium Rate Fraud | TP-0071 |
| Premium Sms Fraud | TP-0072 |
| Provider Fraud | TP-0010, TP-0021, TP-0028 |
| Purchase Scam | TP-0036, TP-0063 |
| Quishing | TP-0051 |
| Rdga Infrastructure | TP-0041, TP-0060 |
| Recovery Fraud | TP-0062 |
| Refunding As A Service | TP-0031, TP-0039 |
| Returns Fraud | TP-0039 |
| Robodialling Fraud | TP-0065 |
| Romance Scam | TP-0011, TP-0025, TP-0027, TP-0052, TP-0058 |
| Sanctions Evasion Infrastructure | TP-0045, TP-0048, TP-0080, TP-0089 |
| Scam Compound Operations | TP-0047, TP-0058 |
| Seller Impersonation | TP-0073 |
| Sextortion | TP-0052, TP-0058 |
| Smishing | TP-0069 |
| Social Engineering | TP-0017, TP-0025, TP-0027, TP-0036, TP-0037, TP-0039, TP-0040, TP-0050, TP-0051, TP-0052, TP-0058, TP-0062, TP-0065, TP-0068, TP-0081, TP-0082, TP-0083, TP-0084, TP-0088 |
| Stablecoin Freeze Evasion | TP-0080 |
| State Criminal Convergence | TP-0044, TP-0046, TP-0055 |
| Subscription Fraud | TP-0072 |
| Synthetic Identity | TP-0003, TP-0018, TP-0022, TP-0029, TP-0033 |
| Synthetic Medical Fraud | TP-0028 |
| Tax Fraud | TP-0022 |
| Tds Exploitation | TP-0042 |
| Telecom Billing Fraud | TP-0072 |
| Telecom Revenue Fraud | TP-0071 |
| Title Fraud | TP-0073 |
| Traffic Distribution System | TP-0060 |
| Travel Booking Fraud | TP-0070 |
| Unauthorized Transaction | TP-0023, TP-0039, TP-0087 |
| Unlicensed Insurance | TP-0074 |
| Upcoding | TP-0021 |
| Vehicle Export Fraud | TP-0053 |
| Vendor Impersonation | TP-0020 |
| Vishing | TP-0001, TP-0012, TP-0065, TP-0081 |
| Wangiri | TP-0071 |
| Wire Fraud | TP-0001, TP-0002, TP-0006, TP-0007, TP-0020, TP-0024 |

## Coverage by Sector

| Sector | Threat Paths |
|--------|-------------|
| Banking | TP-0001, TP-0002, TP-0003, TP-0006, TP-0007, TP-0008, TP-0009, TP-0012, TP-0013, TP-0014, TP-0016, TP-0017, TP-0018, TP-0019, TP-0020, TP-0022, TP-0023, TP-0024, TP-0025, TP-0026, TP-0027, TP-0029, TP-0034, TP-0036, TP-0037, TP-0040, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0056, TP-0057, TP-0058, TP-0059, TP-0060, TP-0062, TP-0064, TP-0065, TP-0067, TP-0069, TP-0078, TP-0079, TP-0080, TP-0081, TP-0082, TP-0083, TP-0084, TP-0085, TP-0086, TP-0087 |
| Credit Union | TP-0009, TP-0012, TP-0014, TP-0016, TP-0018 |
| Cross Sector | TP-0002, TP-0004, TP-0006, TP-0007, TP-0011, TP-0013, TP-0017, TP-0020, TP-0025, TP-0027, TP-0039, TP-0041, TP-0042, TP-0043, TP-0044, TP-0045, TP-0046, TP-0047, TP-0048, TP-0049, TP-0050, TP-0051, TP-0052, TP-0053, TP-0054, TP-0055, TP-0057, TP-0058, TP-0061, TP-0062, TP-0063, TP-0064, TP-0065, TP-0067, TP-0069, TP-0070, TP-0078, TP-0079, TP-0080, TP-0081, TP-0082, TP-0084, TP-0085, TP-0086, TP-0087, TP-0088, TP-0089 |
| Crypto | TP-0008, TP-0017, TP-0023, TP-0026, TP-0032, TP-0034, TP-0041, TP-0043, TP-0044, TP-0045, TP-0047, TP-0049, TP-0052, TP-0054, TP-0055, TP-0058, TP-0059, TP-0060, TP-0078, TP-0079, TP-0080, TP-0083, TP-0085, TP-0087 |
| E Commerce | TP-0087 |
| Ecommerce | TP-0075, TP-0076 |
| Education | TP-0033 |
| Employment | TP-0015, TP-0034, TP-0057 |
| Fintech | TP-0003, TP-0008, TP-0013, TP-0018, TP-0023, TP-0024, TP-0029, TP-0035, TP-0037, TP-0038, TP-0039, TP-0040, TP-0059, TP-0067 |
| Government | TP-0021, TP-0022, TP-0028, TP-0033, TP-0034, TP-0056, TP-0069, TP-0079, TP-0084, TP-0086 |
| Healthcare | TP-0015, TP-0021, TP-0028, TP-0034, TP-0056, TP-0066 |
| Insurance | TP-0005, TP-0010, TP-0014, TP-0021, TP-0028, TP-0056, TP-0060, TP-0066, TP-0074, TP-0077, TP-0081, TP-0086 |
| Investment | TP-0019, TP-0026, TP-0041, TP-0052, TP-0058, TP-0060, TP-0062, TP-0065, TP-0083 |
| Logistics | TP-0088 |
| Payments | TP-0024, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0043, TP-0046, TP-0051, TP-0054, TP-0059, TP-0063, TP-0068, TP-0069, TP-0070, TP-0075, TP-0079 |
| Real Estate | TP-0073 |
| Retail | TP-0013, TP-0030, TP-0031, TP-0035, TP-0036, TP-0037, TP-0038, TP-0039, TP-0040, TP-0042, TP-0051, TP-0063, TP-0068, TP-0069, TP-0075 |
| Staffing | TP-0015, TP-0057 |
| Technology | TP-0034, TP-0039, TP-0054, TP-0057, TP-0061, TP-0067, TP-0076, TP-0081, TP-0087, TP-0089 |
| Telecommunications | TP-0061, TP-0065, TP-0071, TP-0072, TP-0089 |
| Trade | TP-0064 |
| Transportation | TP-0069, TP-0088 |
| Travel | TP-0070 |
| Web3 | TP-0032 |

## Framework Coverage Status

| Framework | Mapping Status | Notes |
|-----------|---------------|-------|
| FS-ISAC CFPF | All 89 TPs mapped | Primary organizational structure |
| MITRE ATT&CK | 84 of 89 TPs mapped | Where applicable (some fraud-only TPs lack ATT&CK equivalents) |
| Stripe FT3 | Mapped (72/89) | MIT-licensed JSON vendored in data/ft3/ |
| MITRE F3 | Awaiting release | Will map when F3 ships |
| Group-IB Fraud Matrix | 89 of 89 TPs mapped | 10-stage lifecycle; stage names referenced for interoperability |
| Group-IB UCFF | 89 of 89 TPs aligned | 7-domain lifecycle maturity assessment |

## Cross-Threat Path Connections

The fraud ecosystem is interconnected. Key relationships:

```
TP-0011 (Romance/Mule Recruitment) ──provides mule accounts to──▶ TP-0001, TP-0002, TP-0006, TP-0009
TP-0003 (Synthetic Identity) ──provides fraudulent accounts to──▶ TP-0009, TP-0013
TP-0014 (Insider Threat) ──provides customer data to──▶ TP-0001, TP-0005, TP-0008, TP-0012
TP-0007 (Deepfake Voice) ──enhances social engineering in──▶ TP-0001, TP-0006, TP-0012
TP-0008 (SIM Swap) ──bypasses MFA controls in──▶ TP-0001, TP-0005, TP-0013
```
