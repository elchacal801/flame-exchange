# INTERPOL GFFTA 2026 — FLAME Enrichment Design

**Date**: 2026-03-17
**Source Document**: `docs/docs_internal/INTERPOL_Global_Financial_Fraud_Threat_Assessment_2026.md`
**Approach**: Full Integration (Approach A) — new TPs, new fraud types, existing TP enrichments

---

## Summary

The INTERPOL Global Financial Fraud Threat Assessment (Second Edition, March 2026) provides substantial intelligence that can enrich the FLAME framework. This design covers:

- **6 new Threat Paths** (TP-0051 through TP-0056)
- **4 new fraud types** added to the taxonomy
- **8 existing TPs enriched** with INTERPOL citations, statistics, and case studies
- **Database rebuild** to regenerate all derived artifacts

---

## 1. New Threat Paths

### TP-0051 — QR Code Payment Fraud / Quishing

- **Fraud types**: `quishing`, `credential-stuffing`, `account-takeover`, `social-engineering`
- **Sectors**: Banking, Payments, Retail, Cross-sector
- **CFPF Phases**: P1-P5
- **Kill chain**: Fraudster poses as buyer on marketplace -> moves conversation to messaging app -> sends fake QR code claiming payment at post office -> victim scans -> fake bank login page -> credentials harvested -> 2FA device added -> funds drained via mobile money
- **Source**: INTERPOL GFFTA 2026 (European member country report, USD 110K case)
- **Related TPs**: TP-0012, TP-0037, TP-0050
- **Detection focus**: QR code URL domain analysis, new 2FA device enrollment velocity, mobile money transfer patterns post-credential entry

### TP-0052 — Sextortion-Investment Hybrid Fraud

- **Fraud types**: `sextortion`, `investment-scam`, `deepfake-fraud`, `social-engineering`, `romance-scam`
- **Sectors**: Banking, Crypto, Investment, Cross-sector
- **CFPF Phases**: P1-P5
- **Kill chain**: Social media grooming -> deepfake intimate imagery generation or coerced image sharing -> blackmail threat -> pivot to "investment opportunity" to recover losses -> victim deposits into fraudulent crypto platform -> funds laundered
- **Source**: INTERPOL GFFTA 2026 (multi-regional: Americas targeting teens 14-17, Asia-Pacific hybrid schemes, Latin America targeting executives)
- **Related TPs**: TP-0011, TP-0017, TP-0025, TP-0026
- **Detection focus**: Account age vs. transaction velocity, crypto deposit patterns following social media contact, cross-platform behavioral signals

### TP-0053 — Vehicle Export Financing Fraud

- **Fraud types**: `vehicle-export-fraud`, `identity-theft`, `application-fraud`, `loan-fraud`
- **Sectors**: Banking, Cross-sector
- **CFPF Phases**: P1-P5
- **Kill chain**: Criminal network recruits straw buyers -> forged employment/income docs submitted -> vehicle financed with minimal down payment -> vehicle exported overseas before lender detects default -> loan defaults -> vehicle untraceable in INTERPOL systems
- **Source**: INTERPOL GFFTA 2026 (Americas, detected early 2024, spreading)
- **Related TPs**: TP-0018, TP-0019, TP-0029
- **Detection focus**: Loan-to-export timing analysis, straw buyer identity velocity, cross-border vehicle registration queries, default-to-detection gap monitoring

### TP-0054 — Fraud-as-a-Service (FaaS) Platforms

- **Fraud types**: `fraud-as-a-service`, `ai-accelerated-fraud-infrastructure`, `phishing`, `brand-impersonation`
- **Sectors**: Cross-sector, Banking, Payments, Crypto, Technology
- **CFPF Phases**: P1-P5
- **Kill chain**: FaaS operator builds GenAI-powered platform -> offers subscription access to phishing kits, fake payment gateways, deepfake tools, bot-generated testimonials -> low-skill actors purchase access -> launch professional-grade BEC/phishing campaigns -> proceeds split between operator and affiliates
- **Source**: INTERPOL GFFTA 2026 (Asia-Pacific FaaS + global AI enablement chapter)
- **Related TPs**: TP-0043, TP-0041, TP-0042
- **Distinction from TP-0043**: TP-0043 covers infrastructure *generation*; TP-0054 covers the *marketplace/subscription model* that democratizes access
- **Detection focus**: Shared infrastructure fingerprints across campaigns, template reuse patterns, payment gateway clone detection, affiliate payout patterns

### TP-0055 — Crypto Fraud-Terrorism/Narco Financing Nexus

- **Fraud types**: `crypto-laundering`, `investment-scam`, `state-criminal-convergence`, `money-mule`
- **Sectors**: Crypto, Banking, Cross-sector
- **CFPF Phases**: P1-P5
- **Kill chain**: Criminal syndicate (narco/extremist) establishes Ponzi or crypto investment scheme -> recruits victims as investors -> proceeds laundered through crypto mixing/cross-border transfers -> funds finance drug trafficking, extortion, or extremist operations
- **Source**: INTERPOL GFFTA 2026 (Tren de Aragua USD 150M case across Chile, Colombia, Venezuela, Iberian Peninsula)
- **Related TPs**: TP-0044, TP-0045, TP-0049
- **Detection focus**: Ponzi structure indicators, crypto mixer usage patterns, geographic clustering of investor deposits vs. withdrawal destinations, convergence indicators between fraud proceeds and known narco/terror wallets

### TP-0056 — Insurance Claims Fraud (Motor/Medical)

- **Fraud types**: `insurance-fraud`, `fraudulent-claim`, `identity-theft`, `documentary-fraud`
- **Sectors**: Insurance, Healthcare, Banking
- **CFPF Phases**: P1-P5
- **Kill chain**: Staged accident or fabricated medical event -> forged documentation (police reports, medical records) -> fraudulent claim filed with insurer -> identity theft to submit claims under others' policies -> payout via diverted payment channels
- **Source**: INTERPOL GFFTA 2026 (general trend) + gap analysis (FLAME only has premium diversion TP-0005 and disability fraud TP-0010)
- **Related TPs**: TP-0005, TP-0010, TP-0018, TP-0028
- **Detection focus**: Claims frequency analysis, provider network anomaly detection, document authenticity signals, staged accident pattern recognition

---

## 2. New Fraud Types for Taxonomy

| Fraud Type | Description |
|-----------|-------------|
| `sextortion` | Blackmail/extortion using real or AI-generated intimate imagery |
| `quishing` | QR code-based credential harvesting via malicious redirect chains |
| `vehicle-export-fraud` | Straw buyer financing + cross-border vehicle export before default detection |
| `fraud-as-a-service` | GenAI-powered subscription platforms providing turnkey fraud toolkits |

`insurance-fraud` already exists in taxonomy. Net change: 71 -> 75 fraud types.

---

## 3. Existing TP Enrichments

| TP | Enrichment | INTERPOL Section |
|----|-----------|-----------------|
| **TP-0007** | Deepfake audio CEO/CFO impersonation during live calls (Asia-Pacific BEC) | Asia-Pacific BEC |
| **TP-0011** | MENA victims coerced into mule roles; European re-victimization patterns | MENA Investment Fraud, Europe |
| **TP-0012** | Physical impersonation evolution (East Asia doorstep cash collection); grandparent scam surge in Caribbean/Europe | Asia-Pacific Impersonation, Europe Impersonation |
| **TP-0017** | USD 5.6B US losses (2023 FBI IC3); hybrid investment-sextortion convergence; AI-generated dashboards | Investment Fraud |
| **TP-0025** | FaaS platforms enabling low-skill actors with automated phishing sites, fake payment gateways | Technology AI |
| **TP-0026** | FaaS platforms enabling low-skill actors with bot-generated testimonials | Technology AI |
| **TP-0044** | Tren de Aragua narco-crypto convergence (USD 150M, 5 countries) | Americas Organized Crime |
| **TP-0047** | Scam centre expansion to South America, Pacific, MENA; 14,000 detained Myanmar; KK Park demolition; 635 buildings | Scam Centres (multiple regions) |

Changes target **References** and **Analyst Notes** sections, plus relevant body sections where new intelligence adds operational value.

---

## 4. Out of Scope

- **No new detection rules** — new TPs will note where rules are needed; rule authoring is a separate effort
- **No new baselines or emulation playbooks**
- **No regulatory source changes** — existing 6-source pipeline unchanged
- **Database rebuild** via `scripts/build_database.py` after all content changes

---

## 5. Implementation Order

1. Add 4 new fraud types to `data/flame_taxonomy.json`
2. Create 6 new TP markdown files in `ThreatPaths/`
3. Enrich 8 existing TP markdown files
4. Update `ThreatPaths/INDEX.md`
5. Run database rebuild (`scripts/build_database.py`)
6. Verify generated artifacts (API endpoints, stats, search index)

---

## 6. INTERPOL Source Reference

All new and enriched content cites:

> INTERPOL, *Global Financial Fraud Threat Assessment*, Second Edition, March 2026.

Internal document path: `docs/docs_internal/INTERPOL_Global_Financial_Fraud_Threat_Assessment_2026.md`
