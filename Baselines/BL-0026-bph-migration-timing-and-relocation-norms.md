# Baseline: BPH Migration Timing and Relocation Norms

```yaml
---
id: BL-0026
title: "BPH Migration Timing and Relocation Norms"
category: Baseline
date: 2026-03-05
author: "FLAME Project (sourced from CrimsonVector Strategic Intelligence Report, OFAC, CISA)"
related_tps:
  - id: TP-0048
    relationship: related-to
tags:
  - bph-migration
  - sanctions-response
  - infrastructure-relocation
  - baseline
---
```

## Summary

This baseline defines normal and anomalous timing patterns for bulletproof hosting (BPH) provider infrastructure migration following sanctions designations, law enforcement actions, or upstream provider deplatforming events. It establishes behavioral norms for the speed and completeness of hosted domain migration, the timing of rebranding entity registration relative to enforcement events, and the geographic trajectory of infrastructure relocation. These baselines are derived from the CrimsonVector Strategic Intelligence Report analysis of the Aeza Group sanctions case, OFAC enforcement action timelines, and CISA bulletproof hosting advisories. Organizations should calibrate these thresholds against their monitored BPH provider watchlists and sanctions designation feeds to detect infrastructure migration campaigns in progress.

## Normal Patterns

* **Sanctions-to-Migration Latency:** The time from an OFAC or equivalent sanctions designation of a BPH provider to the observable start of infrastructure migration is **7-30 days**. The initial 7-day period typically involves internal assessment and upstream provider compliance action (IP block announcements, BGP route withdrawals). Active migration of hosted domains to new infrastructure begins during this window and accelerates through day 30. Migration activity observed within 48 hours of designation suggests pre-positioned fallback infrastructure and indicates a higher level of operational sophistication.

* **Domain Migration vs. Abandonment Ratio:** Following a BPH provider disruption event, **60-80% of previously hosted domains migrate** to alternative hosting infrastructure, while **20-40% are abandoned**. Abandoned domains are typically lower-value commodity phishing pages and expired campaign infrastructure. Higher migration rates (above 80%) indicate well-organized threat actor collectives with established contingency plans. Migration rates below 60% suggest the disruption event successfully degraded the hosting ecosystem.

* **Rebranding Entity Registration Timing:** New corporate entities associated with BPH provider operators are typically registered **0-14 days before or after** the sanctions announcement or enforcement action. Registration occurring before the public announcement suggests advance knowledge of pending enforcement, insider information leakage, or routine corporate diversification that coincidentally precedes the action. The Aeza Group case demonstrated entity pre-positioning in non-sanctioned jurisdictions prior to OFAC designation.

* **Geographic Relocation Trajectory:** Infrastructure migration following sanctions designation typically moves from the sanctioned jurisdiction to an **adjacent or culturally affiliated jurisdiction** with weaker enforcement cooperation. In the Aeza Group case, infrastructure migrated from Russia to Serbia and Uzbekistan. Common relocation corridors include Russia to Central Asia (Uzbekistan, Kazakhstan), China to Southeast Asia (Malaysia, Cambodia), and Iran to UAE or Turkey.

* **DNS Propagation and Re-resolution Timing:** Migrated domains typically complete DNS re-resolution to new IP ranges within **24-72 hours** of the hosting transition. Domains that re-resolve within 4 hours indicate pre-staged DNS configurations. Bulk DNS changes affecting more than 100 domains within a 24-hour window from a single former BPH provider IP range constitute an anomalous migration event.

## Measurement Methodology

Monitor OFAC SDN list additions, EU sanctions designations, and law enforcement takedown announcements for BPH-related enforcement actions. Maintain a watchlist of IP ranges and ASNs associated with known and suspected BPH providers. Upon a designation event, begin tracking DNS resolution changes for all domains previously hosted on the designated provider's infrastructure using passive DNS data feeds.

Calculate migration rate as the percentage of previously hosted domains that resolve to new IP addresses within 30 days of the designation. Track the geographic distribution of destination IP ranges using MaxMind GeoIP and ASN-to-organization mapping. Monitor corporate registry filings in common relocation jurisdictions for new entity registrations matching known BPH operator naming patterns, officer names, and registration agent networks.

Temporal analysis should use hourly resolution for the first 72 hours post-designation and daily resolution thereafter. Migration velocity is measured as domains migrated per day, with acceleration calculated as the day-over-day change in migration velocity.

## Baseline Values

| Metric | Normal Range | Elevated (Review) | Anomalous (Alert) |
|---|---|---|---|
| Time from designation to first migration activity | 7-30 days | 3-7 days | <72 hours |
| Domain migration rate (% of hosted domains) | 60-80% | 80-90% | >90% |
| Domain abandonment rate | 20-40% | 10-20% | <10% |
| Rebranding entity registration offset | 0-14 days from event | 15-30 days before event | >30 days before event |
| Geographic shift distance | Adjacent jurisdiction | Same continent, non-adjacent | Cross-continental relocation |
| DNS re-resolution time for migrated domains | 24-72 hours | 4-24 hours | <4 hours |
| Bulk DNS changes per 24-hour window | <50 domains | 50-100 domains | >100 domains |
| Migration velocity (domains/day, peak) | 10-30 | 30-75 | >75 |

## Data Sources

* **OFAC SDN list change feed:** US Treasury Office of Foreign Assets Control Specially Designated Nationals list, monitored for BPH provider and hosting infrastructure operator designations.
* **CISA bulletproof hosting advisories:** Cybersecurity and Infrastructure Security Agency alerts and advisories identifying BPH providers and their associated infrastructure indicators.
* **CrimsonVector Strategic Intelligence Report:** Strategic assessment of BPH provider migration patterns following the Aeza Group sanctions designation, including timeline reconstruction and geographic relocation analysis.
* **Passive DNS data feeds:** Farsight DNSDB, DomainTools Iris, and similar passive DNS repositories providing historical and real-time DNS resolution data for migration tracking.
* **Corporate registry monitoring:** OpenCorporates and jurisdiction-specific registry APIs for tracking new entity registrations in common BPH relocation jurisdictions.
* **BGP routing data:** RIPE RIS and RouteViews BGP announcement archives for tracking IP range migrations and ASN changes associated with BPH infrastructure relocation.

## Application

Detection logic DL-0110 and DL-0104 should use these baselines for threshold calibration. DL-0110 (BPH migration velocity anomaly) should trigger when more than 75 domains migrate from a sanctioned provider's IP ranges within a single day, or when DNS re-resolution for migrated domains completes in under 4 hours, indicating pre-staged fallback infrastructure. DL-0104 (rebranding entity detection) should trigger when new corporate entity registrations in common relocation jurisdictions match known BPH operator patterns within 30 days of a sanctions designation.

Analysts should prioritize alerts where the migration-to-designation latency is under 72 hours, as this strongly indicates pre-positioned infrastructure and advance knowledge of enforcement action. Cases where the domain migration rate exceeds 90% with sub-4-hour DNS re-resolution should be escalated as high-confidence indicators of sophisticated BPH operator contingency planning.

## Revision History

| Date | Version | Change Description |
|---|---|---|
| 2026-03-05 | 1.0 | Initial baseline established from CrimsonVector report, OFAC enforcement data, and CISA advisories |
