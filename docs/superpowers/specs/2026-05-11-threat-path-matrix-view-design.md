# FLAME Threat Path Matrix View — Design Spec

**Date:** 2026-05-11
**Status:** Approved
**Author:** FLAME Project

## Problem

FLAME's 89 threat paths are displayed as a flat card grid with sidebar filters. While functional, there's no visual taxonomy — practitioners can't intuitively see how threats relate by attack stage or fraud category. Comparable frameworks (MITRE ATT&CK, MITRE F3, Group-IB Fraud Matrix) use matrix layouts that organize content by attack stage, making them instantly scannable.

## Solution

An ATT&CK-style matrix view as the default browse experience:
- **Sector tabs** across the top (Banking, Crypto, Insurance, etc.)
- **Fraud family rows** (~11 curated categories) as the vertical axis
- **CFPF phase columns** (P1-P5) as the horizontal axis
- **TP chips** placed at their primary phase within each row
- **Matrix/Grid toggle** to switch to the existing flat card grid

## Layout

```
[Sector Tabs: Banking | Crypto | Insurance | Payments | Retail | Cross-Sector | +18 more]
[Showing N threat paths in {Sector}                          [Matrix] [Grid]]
+-------------------+----------+-----------+-----------+-----------+------------+
| Fraud Family      | P1 Recon | P2 Access | P3 Posit. | P4 Exec.  | P5 Monetize|
+-------------------+----------+-----------+-----------+-----------+------------+
| Account Takeover  | TP-0041  | TP-0067   | TP-0001   | TP-0008   |            |
| & Credential Theft|          | TP-0087   | TP-0023   | TP-0081   |            |
+-------------------+----------+-----------+-----------+-----------+------------+
| Payment & Wire    |          | TP-0002   | TP-0004   | TP-0024   | TP-0007    |
+-------------------+----------+-----------+-----------+-----------+------------+
| ...               |          |           |           |           |            |
+-------------------+----------+-----------+-----------+-----------+------------+
```

## Interactions

- **Sector tabs** filter TPs to only those tagged with that sector
- **"All" tab** shows all 89 TPs without sector filtering
- **TP chips** show ID; hover shows full title tooltip; click navigates to `#detail/TP-XXXX`
- **Severity color coding:** Critical = red-tinted, Infrastructure-enabling = green-tinted
- **Sidebar filters** dim non-matching TPs in matrix rather than hiding rows
- **Search** highlights matching TPs in matrix

## Data Model

Two new TP frontmatter fields:

```yaml
fraud_family: "account-takeover"     # One of 11 curated families
primary_phase: "P2"                   # Phase for matrix column placement
```

### 11 Fraud Families

| Key | Label |
|-----|-------|
| `account-takeover` | Account Takeover & Credential Theft |
| `payment-wire` | Payment & Wire Fraud |
| `social-engineering` | Social Engineering & APP |
| `identity-synthetic` | Identity & Synthetic Fraud |
| `investment-romance` | Investment & Romance Scams |
| `insurance-healthcare` | Insurance & Healthcare Fraud |
| `crypto-laundering` | Crypto & Laundering |
| `fraud-infrastructure` | Fraud Infrastructure & FaaS |
| `retail-ecommerce` | Retail & E-Commerce Fraud |
| `state-geopolitical` | State-Linked & Geopolitical |
| `telecom-specialized` | Telecom & Specialized Fraud |

## Files to Modify

| File | Change |
|------|--------|
| `ThreatPaths/TP-*.md` (89) | Add `fraud_family` and `primary_phase` frontmatter |
| `scripts/build_database.py` | Propagate new fields to JSON outputs |
| `scripts/validate_submission.py` | Validate new fields |
| `data/flame_taxonomy.json` | Add `fraud_families` definition |
| `app.js` | `renderMatrixView()`, toggle, sector tabs, tooltips |
| `index.html` | Matrix container, toggle controls |
| `style.css` | Matrix table, chips, responsive, sector tabs |
| `flame-data.js` | Expose new fields |

## Responsive

- **Desktop (>1024px):** Full matrix
- **Tablet (768-1024px):** Horizontally scrollable, sticky first column
- **Mobile (<768px):** Falls back to grouped card grid

## What Does NOT Change

Detail view, Framework Navigator, Coverage Assessment, UCFF view, search (Lunr.js), all other views.
