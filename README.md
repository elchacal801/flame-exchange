# FLAME -- Fraud Lifecycle Analysis & Mitigation Exchange

**Everyone built the dictionary. Nobody built the library.**

Between April 2025 and February 2026, five organizations independently concluded that fraud needs structured taxonomy frameworks. Stripe published FT3 (then abandoned it). MITRE announced F3 (still hasn't shipped). Group-IB released Fraud Matrix 2.0 (commercially gated). FS-ISAC assembled 300+ members for the Cyber Fraud Prevention Framework. The taxonomy layer is converging. The community knowledge exchange layer remains entirely unserved in open source.

FLAME fills that gap.

---

## What is FLAME?

FLAME is an open-source, community-driven platform for sharing structured fraud detection intelligence. It is framework-agnostic: each submission maps simultaneously to multiple fraud taxonomies so practitioners can use whichever framework their organization adopted.

**Supported frameworks:**

| Framework | Status |
|-----------|--------|
| FS-ISAC Cyber Fraud Prevention Framework (CFPF) | Primary structure -- all submissions mapped |
| MITRE ATT&CK | Supplementary mapping where applicable |
| Group-IB Fraud Matrix 2.0 | Cross-reference mapping (stage names) |
| Stripe FT3 | Mapped (40/40 TPs) -- auto-mapped via ft3_mapper.py |
| Group-IB UCFF | Defense-side maturity alignment |
| MITRE F3 | Placeholder (will map when shipped) |

**What FLAME is not:** FLAME is not a taxonomy project. It is a knowledge exchange that sits on top of existing taxonomies, providing the operational intelligence -- threat paths, detection queries, investigation playbooks, and cross-team correlation guidance -- that no taxonomy alone delivers.

## Architecture

FLAME is modeled on [HEARTH](https://github.com/THOR-Collective/HEARTH), the threat hunting hypothesis exchange created by the THOR Collective.

- **Markdown-first**: Threat paths are authored as structured markdown files with YAML frontmatter. Markdown is the source of truth.
- **Database is derived**: A Python build script parses the markdown, builds a SQLite index, and exports JSON for the frontend. The database is regenerated on every push.
- **Static frontend**: A vanilla HTML/CSS/JS frontend served via GitHub Pages. No build step, no framework dependencies.
- **Ecosystem interop**: Build-time exports produce STIX 2.1 bundles, MISP galaxy/feed, and TAXII 2.1-compatible endpoints.
- **CI/CD**: GitHub Actions validate PR submissions, auto-rebuild the database, and regenerate all export artifacts on merge.

```
ThreatPaths/          Fraud scheme lifecycle mappings (40 TPs)
Baselines/            Environmental profiling (BL-XXXX)
DetectionLogic/       Rules, queries, analytics (91 DL rules)
Templates/            Submission templates
config/               Regulatory requirements and source configs
scripts/              Build, validation, and export scripts
database/             Generated artifacts (auto-built)
├─ flame-index.json         Metadata-only index (fast load)
├─ flame-content/           Individual TP content files (lazy load)
├─ flame-stats.json         Pre-computed aggregate statistics
├─ flame_stix_bundle.json   STIX 2.1 bundle with fraud extensions
├─ flame_detection_rules.json  STIX detection rule bundle
├─ sigma-exports/           Sigma packs (SPL, Lucene, KQL)
├─ misp-feed/               Per-TP MISP event files + manifest
└─ regulatory-alerts.json   Automated regulatory alert feed
data/misp/            MISP galaxy and cluster definitions
api/
├─ v1/                Static JSON API (114 endpoints)
└─ taxii/             TAXII 2.1 discovery, collections, objects
docs/                 Project documentation, designs, and plans
.github/              Workflows and issue templates
```

## Ecosystem Integration (v0.5 SIGNAL)

FLAME produces standard-format outputs for integration with threat intelligence platforms:

**STIX 2.1 Fraud Extension** -- 4 custom SDOs (`x-flame-fraud-scheme`, `x-flame-financial-transaction`, `x-flame-mule-network`, `x-flame-fraud-actor-profile`) with 5 fraud-specific relationship types. See [STIX-FRAUD-EXTENSION.md](docs/STIX-FRAUD-EXTENSION.md).

**MISP Galaxy & Feed** -- A subscribable MISP galaxy with 40 cluster entries cross-referenced to MITRE ATT&CK, plus a per-TP event feed at `database/misp-feed/`.

**TAXII 2.1 Endpoints** -- Static TAXII 2.1-compatible files at `api/taxii/` with 3 collections (threat paths, detection rules as course-of-action SDOs, baselines) enabling automated sync from any TIP (MISP, OpenCTI, ThreatConnect).

**Regulatory Compliance Mapping** -- 15 regulations across 6 jurisdictions (EU, UK, US, Singapore, Australia, International) mapped to relevant threat paths via `regulatory_refs` frontmatter.

**Sigma Detection Packs** -- 91 detection rules exported to Splunk SPL, Elastic Lucene, and Microsoft Sentinel KQL via pySigma. Rules using aggregation/correlation syntax include pseudocode fallback exports with SIEM-specific implementation guidance.

## MCP Server

FLAME includes a [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that exposes fraud intelligence through 7 tools, enabling AI assistants like Claude to query threat paths, detection rules, and framework mappings conversationally.

**Available tools:**

| Tool | Description |
|------|-------------|
| `search_threat_paths` | Search by keyword, sector, fraud type, or CFPF phase |
| `get_threat_path` | Get full details of a specific threat path |
| `get_detection_rules` | Get detection rules filtered by TP, fraud type, or severity |
| `map_framework` | Get framework-specific mappings (cfpf, mitre, groupib, ft3, ucff) |
| `assess_coverage` | Assess fraud detection coverage by sector and fraud type |
| `get_baseline` | Get fraud baseline measurements for benchmarking |
| `look_left_right` | Analyze upstream/downstream threat relationships (CFPF Look Left/Right) |

**Example queries an AI assistant can answer via the MCP server:**

- "What fraud schemes target the insurance sector?"
- "Show me detection rules for wire fraud"
- "What MITRE ATT&CK techniques map to TP-0007?"
- "Assess my coverage for banking account-takeover and wire-fraud"
- "What threat paths feed into TP-0011?"

### Running the MCP server

```bash
python -m mcp_server.server
```

### Claude Desktop integration

Add the following to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flame-fraud": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/flame-fraud"
    }
  }
}
```

## Threat Path Collection

FLAME ships with **40 threat paths** and **91 detection rules** covering major fraud categories across 18 sectors:

| ID | Scheme | Key Fraud Types |
|----|--------|-----------------|
| TP-0001 | Treasury Management ATO via Malvertising | ATO, vishing, wire fraud |
| TP-0002 | BEC -- Vendor Impersonation Wire Fraud | BEC, invoice fraud |
| TP-0003 | Synthetic Identity -- Credit Card Bust-Out | Synthetic identity, application fraud |
| TP-0004 | Payroll Diversion via HR Portal Compromise | Payroll diversion, BEC |
| TP-0005 | Insurance Premium Diversion via Agent Portal ATO | ATO, premium diversion |
| TP-0006 | Real Estate Wire Fraud -- Closing Scam | BEC, wire fraud |
| TP-0007 | Deepfake Voice Authorization for Wire Transfer | Deepfake, impersonation |
| TP-0008 | SIM Swap to Cryptocurrency Exchange ATO | ATO, crypto laundering |
| TP-0009 | Check Washing and Fraudulent Mobile Deposit | Check fraud |
| TP-0010 | Disability Insurance Fraud | Fraudulent claims |
| TP-0011 | Romance Scam to Money Mule Recruitment | Romance scam, money mule |
| TP-0012 | APP Fraud -- Tech Support / Bank Impersonation | Vishing, impersonation |
| TP-0013 | Credential Stuffing to Loyalty Point Drain | Credential stuffing, ATO |
| TP-0014 | Insider-Enabled Account Fraud | Insider threat, collusion |
| TP-0015 | Employment Fraud via Brand Impersonation | Job scam, identity theft |
| TP-0016 | First-Party Fraud (Bust-Out) | Bust-out, first-party fraud |
| TP-0017 | Pig Butchering (Investment Scam) | Investment scam, romance scam |
| TP-0018 | Deepfake Document Fraud | Deepfake fraud, documentary fraud |
| TP-0019 | Business Identity Theft | Identity theft, application fraud |
| TP-0020 | Supply Chain Payment Fraud | BEC, vendor impersonation |
| TP-0021 | Healthcare Provider Billing Fraud | Healthcare fraud, phantom billing |
| TP-0022 | Government Program Fraud | Benefit fraud, tax fraud |
| TP-0023 | Mobile Banking Trojan / Overlay Attack | Malware, ATO |
| TP-0024 | A2A Instant Payment Fraud (Zelle/FedNow/Pix) | APP, unauthorized transaction |
| TP-0025 | GenAI-Enhanced APP Fraud -- Romance Variant | Romance scam, deepfake |
| TP-0026 | GenAI-Enhanced APP Fraud -- Investment Variant | Investment scam, deepfake |
| TP-0027 | Elder Financial Exploitation | Social engineering, APP |
| TP-0028 | DME Phantom Billing (Medicare Fraud) | Healthcare fraud, phantom billing |
| TP-0029 | AI Synthetic Identity & Document Forgery | Synthetic identity, deepfake fraud |
| TP-0030 | E-Commerce Triangulation Fraud | Payment diversion, identity theft |
| TP-0031 | Refund-as-a-Service (FTID / RaaS) | Refunding-as-a-service |
| TP-0032 | Web3 Wallet Drainer / Approval Phishing | Approval phishing, crypto laundering |
| TP-0033 | Ghost Student Financial Aid Botnets | Ghost student fraud, application fraud |
| TP-0034 | DPRK State-Sponsored IT Worker Fraud & Data Extortion | DPRK IT worker fraud, employment fraud, data theft |
| TP-0035 | Magecart E-Skimmer Data Compromise | E-skimmer, data theft, malware |
| TP-0036 | Purchase Scam Merchant Networks | Purchase scam, brand impersonation |
| TP-0037 | Digital Wallet Fraud & NFC Relay Attacks | Digital wallet fraud, NFC relay, ATO |
| TP-0038 | Card Testing Infrastructure Abuse | Card testing, identity theft |
| TP-0039 | Agentic Commerce Fraud | Autonomous AI fraud, unauthorized transaction |
| TP-0040 | BNPL Multi-Provider Fraud | BNPL fraud, synthetic stacking, friendly fraud |

## Quick Start

### View the database

Open `index.html` in a browser (via local server) or visit the [GitHub Pages site](https://elchacal801.github.io/flame-fraud/).

### Build the database locally

```bash
pip install -r requirements.txt
python scripts/build_database.py
```

### Export all artifacts

```bash
python scripts/export_flame_stix.py    # STIX 2.1 bundle
python scripts/export_misp.py          # MISP galaxy & feed
python scripts/export_taxii.py         # TAXII 2.1 endpoints
python scripts/export_sigma.py         # Sigma detection packs
```

### Validate a submission

```bash
python scripts/validate_submission.py ThreatPaths/TP-0001-treasury-mgmt-ato-malvertising.md
```

### Run the MCP server

```bash
python -m mcp_server.server
```

### Subscribe via MISP

Point your MISP instance feed URL to `database/misp-feed/manifest.json` on the GitHub Pages site.

### Subscribe via TAXII

Configure your TIP with the TAXII root at `api/taxii/discovery.json` on the GitHub Pages site.

### Contribute a threat path

See [CONTRIBUTING.md](CONTRIBUTING.md) for submission guidelines.

## Contributing

FLAME is community-driven. Contributions of threat paths, baselines, and detection logic are welcome from practitioners across all financial sectors. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Operational Evidence

Threat paths can include an **Operational Evidence** section linking real-world investigation findings to the fraud lifecycle. The build script parses these entries and includes them in:

- `flame-content/TP-XXXX.json` -- full evidence array per threat path
- `flame-index.json` -- `evidence_count` per entry
- `flame-evidence-index.json` -- cross-TP evidence listing for deduplication

Evidence entries follow the format `EV-[TP-ID]-[YYYY]-[NNN]` and are currently sourced from the [domain_intel](https://github.com/elchacal801/domain_intel) investigation pipeline.

## Documentation

- [Project Design](docs/FLAME-project-design.md) -- Architecture and roadmap
- [STIX Fraud Extension](docs/STIX-FRAUD-EXTENSION.md) -- Custom SDO specification
- [Taxonomy Reference](docs/TAXONOMY.md) -- Fraud types, sectors, CFPF phases, cross-framework mappings
- [Competitive Landscape](docs/COMPETITIVE-LANDSCAPE.md) -- How FLAME relates to other fraud frameworks
- [Changelog](CHANGELOG.md) -- Release history

## Credits

- **HEARTH / THOR Collective** -- Architectural model and inspiration
- **FS-ISAC CFPF Working Group** -- Primary fraud lifecycle framework
- **Group-IB** -- Fraud Matrix 2.0 stage names and UCFF governance domains referenced for cross-taxonomy interoperability
- **Stripe** -- FT3 (MIT-licensed) taxonomy structure
- **MITRE** -- ATT&CK framework; F3 fraud extension (pending)
- **OASIS** -- STIX 2.1 and TAXII 2.1 specifications

## License

MIT License. See [LICENSE](LICENSE).
