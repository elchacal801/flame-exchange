# FLAME MCP Server Tools

The FLAME MCP (Model Context Protocol) server exposes 6 tools that allow LLMs and AI agents to query the FLAME fraud intelligence knowledge base. The server is implemented in `mcp_server/server.py` using the MCP Python SDK (`MCPServer`).

**Server name**: `FLAME Fraud Intelligence`

---

## 1. search_threat_paths

Search FLAME threat paths by keyword, sector, fraud type, CFPF phase, or infrastructure/geopolitical filters.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | No | Search text to match against threat path title and summary |
| `sector` | string | No | Filter by sector (e.g., `banking`, `insurance`, `crypto`) |
| `fraud_type` | string | No | Filter by fraud type (e.g., `account-takeover`, `wire-fraud`) |
| `cfpf_phase` | string | No | Filter by CFPF phase (`P1` through `P5`) |
| `infrastructure_generation_method` | string | No | Filter by infra generation method (`manual`, `dga-embedded`, `rdga-registered`, `ai-assisted`) |
| `geopolitical_timing` | string | No | Filter by geopolitical timing (`none`, `election-cycle`, `sanctions-response`, `conflict-triggered`, `seasonal-political`) |
| `nation_state_nexus` | string | No | Filter by nation-state nexus level (`none`, `suspected`, `confirmed`, `hybrid`) |

### Returns

JSON array of matching threat path summaries, each containing: `id`, `title`, `summary`, `confidence_score`, `cfpf_phases`, and `fraud_types`.

### Example

**Prompt**: "Search for threat paths related to deepfake fraud in the insurance sector"

**Tool call**: `search_threat_paths(query="deepfake", sector="insurance")`

**Response structure**:
```json
[
  {
    "id": "TP-0042",
    "title": "Deepfake Voice Authorization for Insurance Claim Approval",
    "summary": "Threat actors use AI-generated voice...",
    "confidence_score": 75,
    "cfpf_phases": ["P1", "P2", "P3", "P4", "P5"],
    "fraud_types": ["deepfake-fraud", "insurance-fraud"]
  }
]
```

---

## 2. get_threat_path

Get full details of a specific FLAME threat path including the markdown body, detection rules, framework mappings, and relationships.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tp_id` | string | Yes | Threat path ID (e.g., `TP-0001`) |

### Returns

JSON object with the complete threat path data, including all fields from the summary plus the full `body` markdown containing CFPF phase mapping, detection approaches, controls, analyst notes, and UCFF alignment.

Returns `{"error": "Threat path TP-XXXX not found"}` if the ID does not exist.

### Example

**Prompt**: "Show me the full details of threat path TP-0001"

**Tool call**: `get_threat_path(tp_id="TP-0001")`

**Response structure**:
```json
{
  "id": "TP-0001",
  "title": "Treasury Management ATO via Malvertising and Vishing",
  "body": "## Summary\n\nThreat actors target commercial banking...",
  "confidence_score": 82,
  "cfpf_phases": ["P1", "P2", "P3", "P4", "P5"],
  "sectors": ["banking"],
  "fraud_types": ["account-takeover", "vishing", "wire-fraud"],
  "detection_rule_ids": ["DL-0001", "DL-0002", "..."],
  "related_tps": [{"id": "TP-0007", "relationship": "enhances"}],
  "ucff_domains": {"commit": "Level 2", "assess": "Level 3", "...": "..."}
}
```

---

## 3. map_framework

Get framework-specific mappings for a FLAME threat path. Supports five frameworks.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tp_id` | string | Yes | Threat path ID (e.g., `TP-0001`) |
| `framework` | string | Yes | Framework to map: `cfpf`, `mitre`, `groupib`, `ft3`, or `ucff` |

### Returns

JSON object with `tp_id`, `framework`, and a framework-specific field:
- `cfpf` -- `phases`: array of CFPF phase strings (P1-P5)
- `mitre` -- `techniques`: array of MITRE ATT&CK technique IDs
- `groupib` -- `stages`: array of Group-IB fraud kill chain stage names
- `ft3` -- `tactics`: array of Stripe Fraud Taxonomy tactic IDs
- `ucff` -- `domains`: object mapping UCFF domain names to maturity levels

Returns an error if the framework name is not recognized.

### Example

**Prompt**: "Map TP-0001 to the MITRE ATT&CK framework"

**Tool call**: `map_framework(tp_id="TP-0001", framework="mitre")`

**Response structure**:
```json
{
  "tp_id": "TP-0001",
  "framework": "mitre",
  "techniques": ["T1583.001", "T1566.002", "T1656", "T1657"]
}
```

---

## 4. assess_coverage

Assess your organization's fraud detection coverage based on selected sectors and fraud types. Calculates coverage scores, identifies gaps, and recommends detection rules.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sectors` | list[string] | Yes | List of sectors to assess (e.g., `["banking", "insurance"]`) |
| `fraud_types` | list[string] | Yes | List of fraud types to assess (e.g., `["account-takeover", "wire-fraud"]`) |

### Returns

JSON object containing:
- `sectors` and `fraud_types_assessed`: echo of inputs
- `total_matching_tps`: count of relevant threat paths
- `coverage_score`: percentage of assessed fraud types with at least one threat path (0-100)
- `coverage_by_fraud_type`: per-fraud-type breakdown with `threat_path_count`, `covered_phases`, and `gap_phases`
- `uncovered_fraud_types`: list of fraud types with zero matching threat paths
- `recommended_detection_rules`: count of applicable detection rules
- `average_confidence`: mean confidence score across matching threat paths
- `phase_weakness`: count of threat paths covering each CFPF phase (P1-P5), useful for identifying under-monitored phases

### Example

**Prompt**: "Assess our coverage for account takeover and wire fraud in the banking sector"

**Tool call**: `assess_coverage(sectors=["banking"], fraud_types=["account-takeover", "wire-fraud"])`

**Response structure**:
```json
{
  "sectors": ["banking"],
  "fraud_types_assessed": ["account-takeover", "wire-fraud"],
  "total_matching_tps": 18,
  "coverage_score": 100.0,
  "coverage_by_fraud_type": {
    "account-takeover": {
      "threat_path_count": 15,
      "covered_phases": ["P1", "P2", "P3", "P4", "P5"],
      "gap_phases": []
    },
    "wire-fraud": {
      "threat_path_count": 3,
      "covered_phases": ["P1", "P2", "P3", "P4", "P5"],
      "gap_phases": []
    }
  },
  "uncovered_fraud_types": [],
  "recommended_detection_rules": 42,
  "average_confidence": 78.5,
  "phase_weakness": {"P1": 18, "P2": 17, "P3": 18, "P4": 17, "P5": 17}
}
```

---

## 5. get_baseline

Get fraud baseline measurements for benchmarking. Retrieve a specific baseline by ID or all baselines related to a threat path.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `baseline_id` | string | No | Specific baseline ID (e.g., `BASE-001` or `BL-0012`) |
| `tp_id` | string | No | Get baselines related to a threat path ID (e.g., `TP-0001`) |

### Returns

JSON array of baseline objects (or a single object if `baseline_id` is provided). Each baseline includes `id`, `title`, `category`, `date`, `author`, `tlp`, `summary`, `tags`, and associated metadata fields.

### Example

**Prompt**: "What baselines are associated with threat path TP-0001?"

**Tool call**: `get_baseline(tp_id="TP-0001")`

**Response structure**:
```json
[
  {
    "id": "BL-0012",
    "title": "Treasury Wire Transfer Baseline",
    "category": "Baseline",
    "date": "2026-02-20",
    "tlp": "WHITE",
    "tags": ["wire-transfer", "commercial-banking"]
  }
]
```

---

## 6. look_left_right

Analyze upstream and downstream relationships for a threat path using the CFPF Look Left/Look Right methodology. Identifies threat paths that feed into, are enabled by, or share infrastructure with the target.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tp_id` | string | Yes | Threat path ID to analyze (e.g., `TP-0001`) |

### Returns

JSON object containing:
- `tp_id` and `title`: the analyzed threat path
- `cfpf_phases`: phases covered by this threat path
- `look_left`: upstream threat paths that feed into or enable this one (relationship types: `feeds-into`, `enables`, `provides-mules-for` from other TPs pointing to this one)
- `look_right`: downstream threat paths enabled or fed by this one (relationship types: `feeds-into`, `enables`, `provides-mules-for` from this TP pointing outward)
- `lateral`: related threat paths sharing infrastructure or enhancing each other (relationship types: `enhances`, `shared-infrastructure`, etc.)

### Example

**Prompt**: "What are the upstream and downstream relationships for TP-0001?"

**Tool call**: `look_left_right(tp_id="TP-0001")`

**Response structure**:
```json
{
  "tp_id": "TP-0001",
  "title": "Treasury Management ATO via Malvertising and Vishing",
  "cfpf_phases": ["P1", "P2", "P3", "P4", "P5"],
  "look_left": {
    "description": "Upstream threat paths that feed into or enable this one",
    "threat_paths": []
  },
  "look_right": {
    "description": "Downstream threat paths enabled or fed by this one",
    "threat_paths": [
      {"id": "TP-0008", "title": "...", "relationship": "enables"},
      {"id": "TP-0011", "title": "...", "relationship": "provides-mules-for"}
    ]
  },
  "lateral": {
    "description": "Related threat paths sharing infrastructure or enhancing each other",
    "threat_paths": [
      {"id": "TP-0007", "title": "...", "relationship": "enhances"}
    ]
  }
}
```
