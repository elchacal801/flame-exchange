# TP-0071: IRSF & Telecom Revenue Share Fraud

```yaml
---
id: TP-0071
title: "IRSF & Telecom Revenue Share Fraud"
category: ThreatPath
date: 2026-03-29
author: "FLAME Project"
source: "Subex Telecom Fraud Intelligence (2025, 2026); TNS/CFCA Global Fraud Loss Survey (2026); Akamai Telecom Threat Report; NDSS Symposium"
tlp: WHITE
infrastructure_generation_method: manual
fraud_types:
  - irsf
  - premium-rate-fraud
  - telecom-revenue-fraud
  - wangiri
sector:
  - telecommunications
cfpf_phases:
  - P1
  - P2
  - P3
  - P4
  - P5
fraud_family: "telecom-specialized"
primary_phase: "P4"
short_name: "IRSF Revenue Fraud"
confidence_score: 80
source_reliability: A
info_credibility: 2
mitre_attack:
  - T1496      # Resource Hijacking
  - T1078      # Valid Accounts
  - T1059      # Command and Scripting Interpreter
  - T1583.001  # Acquire Infrastructure: Domains
  - T1571      # Non-Standard Port
  - T1205      # Traffic Signaling
ft3_tactics: ["FTA001", "FT011.002"]
mitre_f3: []
groupib_stages:
  - "Reconnaissance"
  - "Resource Development"
  - "Initial Access"
  - "Perform Fraud"
  - "Monetization"
ucff_domains:
  commit: "Level 3"
  assess: "Level 3"
  plan: "Level 3"
  act: "Level 4"
  monitor: "Level 4"
  report: "Level 3"
  improve: "Level 3"
related_tps:
  - id: TP-0008
    relationship: enables
  - id: TP-0065
    relationship: related-to
baseline_ids: []
geopolitical_timing: none
nation_state_nexus: none
regulatory_refs:
  - REG-INTERPOL-GFFTA
  - REG-WCI-2024
tags:
  - irsf
  - premium-rate-fraud
  - wangiri
  - sim-box-fraud
  - telecom-revenue-share
  - international-revenue-share
  - pbx-hacking
  - one-ring-callback
  - traffic-pumping
  - wci-geographic-attribution
---
```

## Summary

International Revenue Share Fraud (IRSF) is the single largest category of telecommunications fraud, generating $10.76 billion in annual losses according to the CFCA/TNS Global Fraud Loss Survey (2026). IRSF exploits the inter-carrier settlement system where originating carriers pay terminating carriers per-minute rates for international calls. Fraudsters establish revenue-sharing agreements with premium-rate number providers in high-rate destinations, then generate artificial call traffic to those numbers using compromised PBX systems, SIM boxes, or automated dialers. Wangiri ("one-ring") fraud, a variant where victims are tricked into calling back premium-rate numbers, adds a social engineering dimension. The convergence of SIM box fraud (TP-0008), compromised enterprise PBX systems, and sophisticated traffic routing creates a multi-layered ecosystem that is difficult to detect in real time. Machine learning-based detection has achieved 98% accuracy in identifying IRSF traffic patterns.

## Threat Path Hypothesis

> **Hypothesis**: Criminal networks exploit the international telecom revenue-sharing model by establishing agreements with premium-rate number providers in jurisdictions with high termination rates (e.g., certain Pacific Island nations, African countries, and Eastern European premium rate ranges). They then generate high volumes of artificial traffic to these numbers through three primary vectors: (1) compromised enterprise PBX/VoIP systems that are hijacked to place automated calls, (2) SIM box operations that route international traffic as local calls to inflate termination revenues, and (3) Wangiri schemes that trick legitimate subscribers into calling back premium-rate numbers. The fraud revenue is shared between the premium-rate number operator and the traffic generator, with payments laundered through multi-jurisdictional settlement systems that are difficult to audit.

**Confidence**: High -- CFCA/TNS, Subex, and industry bodies publish detailed loss quantification and technical analysis. IRSF is the most extensively studied telecom fraud category with decades of operational evidence.

**Estimated Impact**: $10.76B annually (CFCA/TNS 2026). Individual enterprise PBX compromises can generate $50K-$500K in fraudulent charges within hours. Total telecom fraud across all categories: $41.82B.

## CFPF Phase Mapping

### Phase 1: Recon

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Premium-rate number acquisition | Fraudsters establish or lease premium-rate numbers in high-termination-rate destinations with revenue-sharing agreements | New premium-rate number registrations in known high-fraud destinations; revenue-sharing contract creation with shell entities |
| PBX/VoIP vulnerability scanning | Automated scanning for exposed enterprise PBX systems, SIP trunks, and VoIP gateways with default credentials or known vulnerabilities | Port scans on SIP (5060/5061), H.323, and MGCP ports; credential brute-force attempts against PBX admin interfaces |
| SIM procurement and box setup | Operators acquire bulk pre-paid SIM cards and configure SIM box hardware to route international traffic through local mobile networks | Bulk SIM purchases from multiple retailers; SIM box hardware procurement; co-location of SIM boxes near cell towers |

**Data Sources**: Telecom regulatory filings, number allocation databases, network scanning logs, SIM registration databases

---

### Phase 2: Initial Access

| Technique | Description | Indicators |
|-----------|-------------|------------|
| PBX system compromise | Attackers exploit default credentials, unpatched vulnerabilities, or misconfigured SIP trunks to gain control of enterprise PBX systems | Unauthorized admin login to PBX management interface; new outbound routes created for international prefixes; voicemail system configuration changes |
| SIM box activation | SIM boxes activated on mobile networks, presenting as legitimate local subscribers while routing international bypass traffic | Multiple SIM registrations from same IMEI; rapid SIM swapping patterns; high call volumes from geographic clusters |
| Wangiri campaign initiation | Automated systems place short-duration calls (one ring) to large numbers of subscribers from premium-rate numbers to trigger callbacks | Mass outbound calls lasting < 3 seconds to subscriber populations; calls originating from known high-rate international prefixes |

**Target**: Enterprise PBX systems, mobile subscribers (Wangiri), telecom carrier interconnect infrastructure

**Data Sources**: PBX audit logs, network signaling records (SS7/Diameter), call detail records (CDRs), SIM registration systems

---

### Phase 3: Positioning

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Traffic routing configuration | Fraudsters configure compromised PBX systems to route calls through least-cost routes that maximize revenue share while minimizing detection | New call routing rules targeting specific international prefixes; outbound call volume increases during off-hours; call routing through multiple intermediate carriers |
| SIM box traffic management | SIM box operators manage traffic distribution across multiple SIMs to avoid per-SIM velocity limits and detection thresholds | Call distribution patterns across SIMs within a SIM box; deliberate call volume throttling per SIM; periodic SIM rotation |
| Premium-rate number chain obfuscation | Traffic routed through intermediate numbers and carriers to obscure the ultimate premium-rate destination | Multi-hop call routing; intermediate carrier legs that are unnecessary for direct routing; call forwarding chains |

**Data Sources**: Call detail records, SS7 signaling analysis, routing table audit logs, carrier interconnect billing records

---

### Phase 4: Execution

| Technique | Description | Indicators |
|-----------|-------------|------------|
| IRSF traffic generation | Compromised PBX systems or automated dialers generate sustained high-volume calls to premium-rate numbers, accumulating per-minute charges | Sudden spike in international call volume to premium-rate destinations (DL-0182); calls during non-business hours; long-duration calls to known IRSF-target number ranges |
| Wangiri callback exploitation | Victims call back premium-rate numbers and are kept on the line through IVR systems, recorded messages, or connection to premium content | Subscriber callbacks to international numbers within minutes of receiving one-ring calls (DL-0183); call durations exceeding expected callback patterns; callbacks to numbers in known Wangiri-target countries |
| SIM box bypass traffic | International calls terminated through SIM boxes, generating interconnect revenue at mobile termination rates while bypassing international gateway settlements | Calls with audio quality degradation patterns consistent with SIM box transcoding; IMEI patterns associated with known SIM box hardware; geographic clustering of high-volume SIM registrations |

**Data Sources**: Real-time CDR analysis, network traffic monitoring, IVR interaction logs, audio quality metrics

---

### Phase 5: Monetization

| Technique | Description | Indicators |
|-----------|-------------|------------|
| Inter-carrier settlement collection | Premium-rate number operators collect termination revenue through normal carrier settlement processes | Settlement payments to entities in high-fraud jurisdictions; disproportionate revenue from specific number ranges; settlement amounts inconsistent with legitimate traffic patterns |
| Revenue share distribution | Fraud proceeds distributed between premium-rate number operators, traffic generators, and facilitators | Wire transfers to shell companies in multiple jurisdictions; cryptocurrency payments correlated with traffic generation periods |
| Compromised PBX billing impact | Enterprise victims receive inflated telecom bills reflecting fraudulent international calls | Anomalous billing spikes on enterprise accounts; customer disputes for international calls not authorized by the organization |

**Data Sources**: Carrier billing systems, settlement records, financial transaction monitoring, customer billing dispute databases

---

## Cross-Framework Mapping

**FT3 (Stripe Fraud Taxonomy):**
- FTA001: Social engineering (Wangiri callback manipulation)
- FT011.002: Infrastructure abuse (PBX hijacking for traffic generation)

**MITRE ATT&CK:**
- T1496: Resource Hijacking -- compromised PBX systems used for traffic generation
- T1078: Valid Accounts -- stolen PBX admin credentials
- T1059: Command and Scripting Interpreter -- automated dialer scripts
- T1583.001: Acquire Infrastructure: Domains -- premium-rate number and SIM box infrastructure
- T1571: Non-Standard Port -- SIP/VoIP port exploitation
- T1205: Traffic Signaling -- SS7 manipulation for traffic routing

**Group-IB Fraud Matrix:**
- Reconnaissance -> Resource Development -> Initial Access -> Perform Fraud -> Monetization

---

## Look Left / Look Right Analysis

**Discovery Phase**: Typically discovered at Phase 4 (Execution) through CDR anomaly detection or at Phase 5 when billing spikes appear on enterprise accounts.

**Look Left**:
- P1: Premium-rate number intelligence databases can flag known IRSF-target number ranges
- P1: PBX vulnerability scanning detection would identify pre-compromise reconnaissance
- P2: SIM registration anomaly detection would identify SIM box activation patterns

**Look Right**:
- P4: Compromised PBX systems may be used for additional fraud (vishing, caller ID spoofing)
- P5: IRSF revenue laundered through multi-jurisdictional settlement systems
- P5: SIM box infrastructure repurposed for SMS fraud, OTP interception (TP-0008)

---

## Underground Ecosystem Context

### Service Supply Chain
| Role | Service Type | Underground Availability | Typical Cost Range |
|------|-------------|--------------------------|-------------------|
| Premium-rate number provider | Number ranges in high-termination-rate jurisdictions with revenue sharing | Medium | Revenue share agreements (40-60% of termination fees) |
| PBX exploit developer | Zero-day and N-day exploits for common PBX/VoIP platforms | Medium | $1,000-$10,000 per exploit |
| SIM box operator | Bulk SIM procurement and SIM box hardware deployment | High | $2,000-$10,000 for hardware; $5-$20/SIM |
| Traffic generator | Automated dialing software and call management systems | High | $500-$5,000 for software licenses |
| Wangiri operator | Mass-dialing infrastructure for one-ring callback campaigns | High | $1,000-$5,000 per campaign setup |

### Intelligence Sources
- Subex, "Global Telecom Fraud Intelligence Report" (2025, 2026) -- IRSF patterns and ML detection
- TNS/CFCA, "Global Fraud Loss Survey" (2026) -- $10.76B IRSF loss quantification
- Akamai, "Telecom Threat Landscape Report" -- PBX exploitation and SIP abuse
- NDSS Symposium -- Academic research on ML-based IRSF detection achieving 98% accuracy

---

## Controls & Mitigations

| Phase | Control | Type | Owner |
|-------|---------|------|-------|
| P1 | Premium-rate number range intelligence and blacklisting | Preventive | Network Security |
| P1 | PBX hardening: disable default accounts, enforce strong authentication, restrict international dialing | Preventive | IT/Telecom Operations |
| P2 | Real-time SIM registration anomaly detection for SIM box indicators | Detective | Mobile Network Security |
| P2 | SIP trunk authentication and encryption (TLS/SRTP) | Preventive | VoIP Security |
| P3 | International call routing restrictions with whitelist/blacklist by destination | Preventive | Telecom Operations |
| P4 | Real-time CDR analysis for IRSF traffic patterns (DL-0182) | Detective | Fraud Management |
| P4 | Wangiri callback detection and subscriber alerting (DL-0183) | Detective | Fraud Management |
| P4 | ML-based traffic anomaly detection with 98% IRSF identification accuracy | Detective | Fraud Analytics |
| P5 | Carrier settlement monitoring for anomalous revenue patterns | Detective | Revenue Assurance |
| P5 | Cross-carrier IRSF intelligence sharing via i3 Forum and CFCA | Detective | Industry Collaboration |

---

## UCFF Alignment

### Required Organizational Maturity for Effective Detection

| UCFF Domain | Minimum Maturity | Key Deliverables for This Threat Path |
|-------------|-----------------|--------------------------------------|
| COMMIT | Level 3 (Established) | Executive mandate for real-time fraud management system deployment and carrier collaboration |
| ASSESS | Level 3 (Established) | Risk assessment quantifying IRSF exposure by carrier partner, number range, and PBX inventory |
| PLAN | Level 3 (Established) | IRSF detection strategy incorporating CDR analytics, ML models, and premium-rate number intelligence |
| ACT | Level 4 (Advanced) | Real-time CDR analysis with automated blocking for high-confidence IRSF patterns; ML model deployment |
| MONITOR | Level 4 (Advanced) | Continuous monitoring of call traffic patterns, SIM registration anomalies, and PBX system integrity |
| REPORT | Level 3 (Established) | Incident reporting to CFCA/i3 Forum with indicators for cross-carrier threat intelligence |
| IMPROVE | Level 3 (Established) | ML model retraining on new IRSF patterns; PBX security posture continuous improvement |

---

## Detection Approaches

### Queries / Rules

```splunk
`comment("Splunk SPL for IRSF Traffic Spike Detection — DL-0182")`
`comment("Detects abnormal call volume to premium-rate international numbers")`
index=flame_telecom sourcetype=flame:cdr
  call_direction="outbound"
  destination_type="international"
| lookup premium_rate_ranges number_prefix OUTPUT is_premium_rate, risk_country
| where is_premium_rate="true"
| bin _time span=1h
| stats count as call_count,
        sum(call_duration_seconds) as total_duration,
        dc(calling_number) as unique_callers,
        dc(called_number) as unique_destinations,
        avg(call_duration_seconds) as avg_duration
  by source_system, risk_country, _time
| eventstats avg(call_count) as baseline_count, stdev(call_count) as stdev_count by source_system
| eval z_score = (call_count - baseline_count) / stdev_count
| where z_score > 3
| eval risk_score = case(
    z_score > 5 AND total_duration > 36000, "critical",
    z_score > 4 AND total_duration > 18000, "high",
    1=1, "medium")
| table source_system, risk_country, _time, call_count, total_duration,
        unique_callers, unique_destinations, avg_duration, z_score, risk_score
| sort - z_score
```

```sql
-- SQL for Wangiri Callback Velocity Detection — DL-0183
-- Detects high volume of short-duration outbound international calls from single source
SELECT
  c.calling_number,
  c.source_system,
  COUNT(*) AS callback_count,
  COUNT(DISTINCT c.called_number) AS unique_destinations,
  AVG(c.call_duration_seconds) AS avg_duration_seconds,
  SUM(CASE WHEN c.call_duration_seconds < 5 THEN 1 ELSE 0 END) AS short_calls,
  MIN(c.call_start_time) AS first_call,
  MAX(c.call_start_time) AS last_call
FROM call_detail_records c
JOIN premium_rate_numbers p ON c.called_number LIKE p.number_prefix || '%'
WHERE c.call_direction = 'outbound'
  AND c.call_type = 'international'
  AND c.call_start_time >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP)
  AND c.call_duration_seconds < 5
GROUP BY c.calling_number, c.source_system
HAVING COUNT(*) >= 10
   AND COUNT(DISTINCT c.called_number) >= 3
ORDER BY callback_count DESC
```

### Behavioral Analytics

- Sudden spike in outbound international call volume to premium-rate destinations from enterprise PBX systems during non-business hours
- High volume of short-duration (< 5 seconds) outbound calls to international numbers within a 1-hour window
- Subscriber callbacks to international numbers within 5 minutes of receiving inbound one-ring calls
- SIM registrations with IMEI patterns matching known SIM box hardware (e.g., multiple SIMs on same IMEI)
- Call routing through unusual intermediate carrier paths to known high-rate destinations

### Cross-Team Correlation

- **Fraud Management + Network Security**: CDR anomalies correlated with PBX compromise indicators (unauthorized admin access, routing changes)
- **Revenue Assurance + Fraud Analytics**: Settlement pattern anomalies correlated with traffic spike detection
- **Mobile Network Security + Regulatory**: SIM box detection correlated with SIM registration anomalies and regulatory compliance

---

## Operational Evidence

### EV-TP0071-2026-001: IRSF Global Loss Quantification

- **Source**: TNS/CFCA Global Fraud Loss Survey (2026)
- **Key Findings**: IRSF remains the single largest telecom fraud category at $10.76B in annual losses. Total telecom fraud across all categories reached $41.82B. IRSF losses increased 8% year-over-year, driven by VoIP infrastructure proliferation and increasingly sophisticated traffic routing obfuscation.
- **CFPF Phase Coverage**: P1-P5
- **Confidence**: High

### EV-TP0071-2026-002: ML-Based IRSF Detection

- **Source**: Subex Telecom Fraud Intelligence (2025, 2026); NDSS Symposium
- **Key Findings**: Machine learning models trained on CDR patterns achieve 98% accuracy in IRSF traffic identification. Key features include call volume deviation from baseline, destination number range risk scoring, call duration distribution analysis, and temporal pattern recognition. Real-time ML scoring reduces mean time to detection from hours to minutes.
- **CFPF Phase Coverage**: P4
- **Confidence**: High

### EV-TP0071-2026-003: Wangiri Campaign Analysis

- **Source**: Subex (2025); Akamai Telecom Threat Report
- **Key Findings**: Wangiri campaigns use automated dialers to place one-ring calls to thousands of subscribers per hour. Premium-rate numbers used as callback destinations employ IVR systems that keep callers on the line, accumulating per-minute charges. Average victim loss is $15-$50 per callback, but aggregate campaign revenues reach $100K-$1M over campaign lifetime. Campaigns increasingly target mobile subscribers in North America and Europe from Pacific Island and African premium-rate ranges.
- **CFPF Phase Coverage**: P2-P5
- **Confidence**: High

---

## References

- Subex, "Global Telecom Fraud Intelligence Report" (2025, 2026) -- IRSF patterns, SIM box detection, and ML-based fraud management
- TNS/CFCA, "Global Fraud Loss Survey" (2026) -- $10.76B IRSF loss quantification and $41.82B total telecom fraud
- Akamai, "Telecom Threat Landscape Report" -- PBX exploitation, SIP abuse, and Wangiri campaign analysis
- NDSS Symposium -- "ML-Based Detection of International Revenue Share Fraud" -- 98% detection accuracy
- i3 Forum -- IRSF number range intelligence sharing and carrier collaboration
- INTERPOL, "Global Financial Fraud Threat Assessment, 2nd Edition" (March 2026) -- telecom fraud cross-border trends

---

## Analyst Notes

IRSF is the oldest and most persistent form of telecom fraud, yet it continues to generate the largest losses ($10.76B) because it exploits a fundamental architectural feature of the global telecom system: inter-carrier revenue sharing on international call termination. Until the settlement model changes, the economic incentive for IRSF will persist.

The convergence of SIM box fraud and IRSF creates a compounding problem. SIM boxes generate bypass revenue (avoiding international gateway fees), and the same infrastructure can be repurposed for IRSF traffic generation. Detection systems must correlate SIM registration anomalies with CDR traffic patterns.

ML-based detection achieving 98% accuracy is the most effective control, but requires real-time CDR ingestion and scoring. Organizations still relying on batch CDR analysis (daily or weekly) will consistently miss IRSF campaigns that can generate hundreds of thousands of dollars in fraudulent charges within hours.

Wangiri remains effective because it exploits human behavior -- the instinct to return a missed call. Subscriber education and carrier-side callback interception (DL-0183) are both necessary. Carrier-side detection is more reliable than subscriber awareness alone.

PBX compromise is the primary vector for enterprise-originated IRSF. The simple control of restricting international dialing to approved destinations and requiring authentication for route changes would prevent the majority of PBX-based IRSF, but many enterprises still operate PBX systems with default credentials and unrestricted international access.

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-29 | FLAME Project | Initial submission -- sourced from Subex, TNS/CFCA, Akamai, and NDSS Symposium intelligence |
