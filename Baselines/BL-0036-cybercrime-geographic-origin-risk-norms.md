# Baseline: Cybercrime Geographic Origin Risk Norms

```yaml
---
id: BL-0036
title: "Cybercrime Geographic Origin Risk Norms"
category: Baseline
date: 2026-03-25
author: "FLAME Project (sourced from World Cybercrime Index, Bruce et al. 2024, PLoS ONE)"
related_tps:
  - id: TP-0044
    relationship: related-to
  - id: TP-0045
    relationship: related-to
  - id: TP-0046
    relationship: related-to
  - id: TP-0048
    relationship: related-to
  - id: TP-0054
    relationship: related-to
  - id: TP-0049
    relationship: related-to
tags:
  - geographic-risk
  - wci-geographic-attribution
  - country-risk
  - transaction-monitoring
  - baseline
---
```

## Summary

This baseline defines geographic cybercrime production risk tiers derived from the World Cybercrime Index (WCI), a peer-reviewed expert survey of 92 cybercrime intelligence/investigation professionals covering 97 countries across 5 cybercrime categories (Bruce et al., PLoS ONE 2024, DOI: 10.1371/journal.pone.0297312). The WCI establishes the first standardized geographic attribution framework for where cybercrime offenders are primarily based — as opposed to where attacks originate or infrastructure is hosted. These baselines support geographic risk scoring in transaction monitoring, infrastructure origin assessment, and cross-border fraud pattern detection across multiple FLAME threat paths.

**Critical caveats:**
- WCI survey data was collected March–October 2021. The SE Asian scam compound explosion (2022+) post-dates this data — Cambodia, Myanmar, and Laos are absent from WCI rankings despite being major operational bases by 2025–2026. Supplement with current intelligence for SE Asian geographic risk.
- WCI measures cybercrime **production** (where offenders reside), not infrastructure hosting or attack transit. A country's WCI score does not indicate where attacks are launched from or where malicious infrastructure is hosted.
- WCI is based on expert perception from 92 professionals, not measured incident rates. Expert pool skewed towards Europe and North America; South America and Africa are under-represented.
- US (#4) and UK (#8) rankings reflect their roles as major financial centers with significant cash-out/money laundering activity, not as traditional cybercrime production hubs.

## WCI Country Risk Tiers

Risk tiers are derived from WCI Overall scores (0–100 scale). Tier boundaries are set at natural score clusters observed in the WCI top 15.

### Tier 1 — Critical (WCI Overall > 25)

Countries producing the highest volume and most impactful cybercrime across multiple categories.

| Country | WCI Overall | Primary Specialization | Secondary Specialization |
|---------|-------------|----------------------|-------------------------|
| Russia | 58.39 | Technical products (82.17) | Attacks/extortion (81.34) |
| Ukraine | 36.44 | Technical products (52.97) | Attacks/extortion (50.76) |
| China | 27.86 | Technical products (40.22) | Data/identity theft (34.89) |
| United States | 25.01 | Data/identity theft (30.36) | Cash-out/laundering (26.63) |

### Tier 2 — High (WCI Overall 10–25)

Countries with significant cybercrime output, often with pronounced category specialization.

| Country | WCI Overall | Primary Specialization | Secondary Specialization |
|---------|-------------|----------------------|-------------------------|
| Nigeria | 21.28 | Scams (52.17) | Data/identity theft (23.04) |
| Romania | 14.83 | Data/identity theft (22.50) | Technical products (17.83) |
| North Korea | 10.61 | Attacks/extortion (25.33) | Data/identity theft (13.01) |

### Tier 3 — Elevated (WCI Overall 2–10)

Countries with notable but lower-volume cybercrime, often with a single-category focus.

| Country | WCI Overall | Primary Specialization |
|---------|-------------|----------------------|
| United Kingdom | 9.01 | Cash-out/laundering (21.63) |
| Brazil | 8.93 | Technical products (13.70) |
| India | 6.13 | Scams (12.75) |
| Iran | 4.78 | Attacks/extortion (10.00) |
| Belarus | 3.87 | Technical products (11.92) |
| Ghana | 3.58 | Scams (10.36) |
| South Africa | 2.58 | Scams (7.17) |
| Moldova | 2.57 | Technical products (6.70) |

## Category-Specific Risk Profiles

The WCI reveals that cybercrime hubs **specialize** — a country's overall score does not predict its risk profile across all fraud types. Category-specific scores should be used for targeted monitoring.

### Technical Products/Services (malware, botnets, tools, FaaS)
Top producers: Russia (82.17), Ukraine (52.97), China (40.22), US (27.64), Romania (17.83), Brazil (13.70), Belarus (11.92)
**Application:** Weight infrastructure procurement, malware delivery, and tooling-as-a-service activity from these jurisdictions. Relevant to TP-0048, TP-0054, TP-0067.

### Attacks and Extortion (DDoS, ransomware)
Top producers: Russia (81.34), Ukraine (50.76), North Korea (25.33), China (24.24), US (17.68), Iran (10.00)
**Application:** Weight DDoS origin, ransomware deployment, and extortion campaign attribution. Relevant to TP-0044, TP-0046.

### Scams (advance fee, BEC, social engineering)
Top producers: Nigeria (52.17), US (22.72), Russia (21.70), China (15.83), Romania (13.15), India (12.75), Ghana (10.36)
**Application:** Weight social engineering, romance scam, investment scam, and BEC origin patterns. Relevant to TP-0011, TP-0017, TP-0065.

### Cash-out/Money Laundering (mule networks, illicit VCPs)
Top producers: Russia (41.56), Ukraine (31.27), US (26.63), China (24.13), UK (21.63), Nigeria (14.86)
**Application:** Weight mule account geography, cryptocurrency off-ramp jurisdiction, and laundering flow destination patterns. Relevant to TP-0049, TP-0059.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Transaction volume from WCI Tier 1 countries | Varies by institution | >2x baseline for the jurisdiction | >5x baseline or sudden spike |
| Infrastructure registrations from WCI Tier 1 Technical countries (RU/UA/CN) | Institution-specific | >3x normal daily registration volume | >10x or new CIDR block allocation |
| Scam-pattern transactions with WCI Tier 2 Scams countries (NG/GH/IN) | Institution-specific | >2x baseline | >5x with social engineering indicators |
| Cash-out flow concentration in single WCI Tier 1 jurisdiction | <30% of total flows | 30–50% | >50% in single jurisdiction |
| Cross-category geographic mismatch (e.g., technical origin ≠ cash-out destination) | Expected (different hubs) | N/A | Same jurisdiction dominates both origin and monetization (unusual per WCI specialization pattern) |
| New correspondent banking/payment relationships with WCI Tier 1 countries | Gradual growth | >2 new relationships/quarter | >5 new relationships/quarter or relationship with sanctioned-adjacent entity |

## Measurement Methodology

Geographic origin risk scoring should combine WCI country scores with institution-specific transaction baselines. The WCI provides a **prior probability** for geographic risk that should be updated with observed transaction patterns (Bayesian approach). Raw WCI scores should not be used as standalone risk thresholds — they must be calibrated to the institution's geographic transaction profile.

For institutions with significant legitimate business in WCI Tier 1 countries, use **category-specific** WCI scores rather than overall scores to avoid false positives. For example, a bank with extensive Russian corporate banking relationships should not flag all Russian transactions, but should apply elevated monitoring for transactions matching the technical products/services pattern (tool procurement, infrastructure payments, hosting services).

## Data Sources

* **World Cybercrime Index:** Bruce M, Lusthaus J, Kashyap R, Phair N, Varese F (2024) PLoS ONE 19(4): e0297312. DOI: 10.1371/journal.pone.0297312. Data: https://osf.io/5s72x/
* **Institutional transaction baselines:** Organization-specific geographic transaction volume data, refreshed quarterly.
* **OFAC SDN List:** Cross-reference WCI country rankings with current sanctions designations for composite risk scoring.
* **FATF Mutual Evaluation Reports:** Supplement WCI data with FATF AML/CFT effectiveness assessments for cash-out jurisdictions.

## Application

These baselines inform geographic risk scoring in transaction monitoring rules and should be cross-referenced with detection logic for TP-0044 (state-criminal convergence), TP-0045 (sanctions evasion), TP-0046 (geopolitically-timed campaigns), TP-0048 (BPH migration), TP-0049 (crypto laundering), and TP-0054 (FaaS platforms). The category-specific WCI scores are particularly valuable for distinguishing between fraud production geography (where offenders reside) and fraud impact geography (where victims and financial infrastructure are located).

Institutions should update these baselines when the WCI publishes future survey iterations. The WCI authors have indicated plans for longitudinal data collection, which will enable trend analysis of geographic cybercrime production shifts over time.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-25 | 1.0 | Initial baseline established from World Cybercrime Index (Bruce et al. 2024) |
