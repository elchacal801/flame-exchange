# FLAME STIX 2.1 Fraud Extension Specification

| Field     | Value                                                  |
|-----------|--------------------------------------------------------|
| Version   | 1.0.0                                                  |
| Namespace | `x-flame`                                              |
| Status    | Draft                                                  |
| Created   | 2026-03-02                                             |
| License   | Apache-2.0 (same as FLAME project)                     |

## 1. Scope

This specification defines custom STIX 2.1 extensions for representing fraud intelligence produced by the FLAME platform. It introduces **4 new STIX Domain Objects (SDOs)** and **5 new relationship types** that capture fraud-specific semantics not expressible with the base STIX 2.1 vocabulary.

**v1 scope is limited to SDOs.** STIX Cyber-observable Objects (SCOs) such as bank accounts, payment cards, crypto wallets, and device fingerprints are out of scope. FLAME carries fraud patterns, not operational indicators of compromise. SCOs may be added in a future extension version when FLAME begins ingesting real observables.

All custom objects follow the STIX 2.1 custom object naming convention, using the `x-flame-` prefix registered under the FLAME project namespace.

---

## 2. Custom SDO Definitions

### 2.1 x-flame-fraud-scheme

Represents a complete fraud lifecycle pattern. One `x-flame-fraud-scheme` object is produced per FLAME Threat Path (TP). This is the primary SDO representation of a Threat Path.

**Type name:** `x-flame-fraud-scheme`

#### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | Must be `"x-flame-fraud-scheme"` |
| `spec_version` | `string` | Yes | Must be `"2.1"` |
| `id` | `identifier` | Yes | Deterministic; see section 5 |
| `created` | `timestamp` | Yes | Object creation time |
| `modified` | `timestamp` | Yes | Object modification time |
| `name` | `string` | Yes | Human-readable name (TP title) |
| `description` | `string` | No | Full narrative summary of the fraud scheme |
| `scheme_type` | `string` | Yes | Fraud scheme classification. Must be one of: `ato`, `bec`, `synthetic-identity`, `app-fraud`, `check-fraud`, `wire-fraud`, `insurance-fraud`, `investment-fraud`, `romance-scam`, `first-party`, `insider`, `mule-recruitment`, `credential-stuffing`, `deepfake`, `identity-theft`, `other` |
| `cfpf_phases` | `list` of `string` | No | CFPF lifecycle phases covered. Values from: `P1`, `P2`, `P3`, `P4`, `P5` |
| `loss_estimate` | `object` | No | Estimated loss range. Structure: `{ "low": <number>, "high": <number>, "currency": "<ISO 4217>" }` |
| `affected_sectors` | `list` of `string` | No | Economic sectors impacted (e.g., `"banking"`, `"insurance"`, `"healthcare"`) |
| `kill_chain_phases` | `list` of `kill-chain-phase` | No | STIX kill chain phases using the `"cfpf"` kill chain name. Phase names follow the pattern `P1-reconnaissance`, `P2-initial-access`, `P3-positioning`, `P4-execution`, `P5-monetization` |
| `confidence_score` | `integer` | No | Analytical confidence in the scheme definition. Range: 0-100 |
| `object_marking_refs` | `list` of `identifier` | No | TLP and other marking definitions |
| `external_references` | `list` of `external-reference` | No | Links to source material, MITRE ATT&CK techniques, etc. |

---

### 2.2 x-flame-financial-transaction

Models the fraudulent money movement pattern associated with a fraud scheme. Derived from P4 (Execution) and P5 (Monetization) phase content within each Threat Path.

**Type name:** `x-flame-financial-transaction`

#### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | Must be `"x-flame-financial-transaction"` |
| `spec_version` | `string` | Yes | Must be `"2.1"` |
| `id` | `identifier` | Yes | Deterministic; see section 5 |
| `created` | `timestamp` | Yes | Object creation time |
| `modified` | `timestamp` | Yes | Object modification time |
| `name` | `string` | Yes | Human-readable name |
| `description` | `string` | No | Narrative description of the transaction pattern |
| `transaction_type` | `string` | Yes | Payment method category. Must be one of: `wire`, `ACH`, `A2A`, `crypto`, `check`, `card`, `other` |
| `amount_range` | `object` | No | Typical transaction value range. Structure: `{ "low": <number>, "high": <number>, "currency": "<ISO 4217>" }` |
| `rail` | `string` | No | Payment rail used. Must be one of: `SWIFT`, `FedWire`, `ACH`, `blockchain`, `card-network`, `RTP`, `other` |
| `velocity_pattern` | `string` | No | Free-text description of transaction velocity characteristics (e.g., `"3-5 transfers within 24 hours of account compromise"`) |

---

### 2.3 x-flame-mule-network

Models money mule infrastructure involved in a fraud scheme. Only generated for Threat Paths that reference mule activity.

**Type name:** `x-flame-mule-network`

#### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | Must be `"x-flame-mule-network"` |
| `spec_version` | `string` | Yes | Must be `"2.1"` |
| `id` | `identifier` | Yes | Deterministic; see section 5 |
| `created` | `timestamp` | Yes | Object creation time |
| `modified` | `timestamp` | Yes | Object modification time |
| `name` | `string` | Yes | Human-readable name |
| `description` | `string` | No | Narrative description of the mule network |
| `recruitment_method` | `string` | Yes | Primary recruitment vector. Must be one of: `romance`, `employment`, `social-media`, `crypto-job`, `other` |
| `geographic_spread` | `list` of `string` | No | Regions where mule accounts are located (e.g., `"US"`, `"EU"`, `"Southeast Asia"`) |
| `estimated_throughput` | `string` | No | Free-text estimate of funds processed (e.g., `"$50K-$200K per month per mule tier"`) |
| `network_type` | `string` | No | Organizational structure. Must be one of: `individual`, `organized`, `hybrid` |

---

### 2.4 x-flame-fraud-actor-profile

Extends threat actor representation with fraud-specific specialization data. Derived from Underground Ecosystem Context sections within Threat Paths, where present.

**Type name:** `x-flame-fraud-actor-profile`

#### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | Must be `"x-flame-fraud-actor-profile"` |
| `spec_version` | `string` | Yes | Must be `"2.1"` |
| `id` | `identifier` | Yes | Deterministic; see section 5 |
| `created` | `timestamp` | Yes | Object creation time |
| `modified` | `timestamp` | Yes | Object modification time |
| `name` | `string` | Yes | Human-readable name |
| `description` | `string` | No | Narrative description of the actor profile |
| `fraud_specialization` | `list` of `string` | No | Fraud types the actor is known for (uses FLAME taxonomy values, e.g., `"account-takeover"`, `"BEC"`) |
| `monetization_methods` | `list` of `string` | No | How the actor converts stolen value (e.g., `"crypto-cashout"`, `"wire-transfer"`, `"gift-cards"`) |
| `sophistication_level` | `string` | No | Assessed operational sophistication. Must be one of: `low`, `medium`, `high`, `expert` |
| `jurisdiction` | `list` of `string` | No | Known or suspected operating regions (e.g., `"West Africa"`, `"Eastern Europe"`) |

---

## 3. Relationship Types

The following custom relationship types connect the SDOs defined above and link them to standard STIX objects.

| Relationship Type | Source Type | Target Type | Description |
|---|---|---|---|
| `monetizes` | `x-flame-fraud-scheme` | `x-flame-financial-transaction` | Describes how a fraud scheme converts to a specific financial action or payment movement |
| `launders-through` | `x-flame-financial-transaction` | `x-flame-mule-network` | Describes how fraudulently obtained funds are moved through mule infrastructure |
| `impersonates` | `x-flame-fraud-actor-profile` | `identity` | Identifies who the fraud actor pretends to be during the scheme |
| `recruits` | `x-flame-fraud-actor-profile` | `x-flame-mule-network` | Describes an actor's recruitment of money mules |
| `enables` | `malware` or `tool` | `x-flame-fraud-scheme` | Identifies technical tools or malware that enable the fraud scheme |

All relationships are expressed as standard STIX `relationship` objects with `relationship_type` set to the value in the first column.

---

## 4. CFPF Kill Chain Definition

FLAME registers a custom kill chain for the FS-ISAC Cyber Fraud Prevention Framework (CFPF):

```json
{
  "kill_chain_name": "cfpf",
  "phases": [
    { "phase_name": "P1-reconnaissance" },
    { "phase_name": "P2-initial-access" },
    { "phase_name": "P3-positioning" },
    { "phase_name": "P4-execution" },
    { "phase_name": "P5-monetization" }
  ]
}
```

`x-flame-fraud-scheme` objects reference this kill chain via the standard `kill_chain_phases` property.

---

## 5. UUID Namespace and Deterministic IDs

All STIX IDs are generated deterministically to ensure reproducible builds. The scheme uses UUID v5 with `NAMESPACE_DNS` (`6ba7b810-9dad-11d1-80b4-00c04fd430c8`):

```
uuid5(NAMESPACE_DNS, "flame-{tp_id}-{sdo_suffix}")
```

Where:

| SDO Type | `sdo_suffix` | Example Seed | Example ID |
|---|---|---|---|
| `x-flame-fraud-scheme` | `scheme` | `flame-TP-0001-scheme` | `x-flame-fraud-scheme--<uuid5>` |
| `x-flame-financial-transaction` | `transaction` | `flame-TP-0001-transaction` | `x-flame-financial-transaction--<uuid5>` |
| `x-flame-mule-network` | `mule-network` | `flame-TP-0011-mule-network` | `x-flame-mule-network--<uuid5>` |
| `x-flame-fraud-actor-profile` | `actor-profile` | `flame-TP-0001-actor-profile` | `x-flame-fraud-actor-profile--<uuid5>` |

This ensures that the same Threat Path always produces the same STIX IDs across builds.

---

## 6. Backward Compatibility

Existing `attack-pattern` SDOs remain in all FLAME STIX bundles. The new SDOs defined in this specification are **additive** -- they do not replace or remove any existing objects. Consumers that do not understand the `x-flame-` types will simply ignore them and continue to process the standard `attack-pattern`, `relationship`, and `identity` objects as before.

Bundles produced under this extension contain both:
- Standard STIX objects (`attack-pattern`, `identity`, `relationship`, `marking-definition`)
- Extended FLAME objects (`x-flame-fraud-scheme`, `x-flame-financial-transaction`, `x-flame-mule-network`, `x-flame-fraud-actor-profile`)

---

## 7. Example

A sample `x-flame-fraud-scheme` object for TP-0001 (Treasury Management ATO via Malvertising and Vishing):

```json
{
  "type": "x-flame-fraud-scheme",
  "spec_version": "2.1",
  "id": "x-flame-fraud-scheme--a1b2c3d4-e5f6-5a7b-8c9d-0e1f2a3b4c5d",
  "created": "2026-02-12T00:00:00.000Z",
  "modified": "2026-03-02T00:00:00.000Z",
  "name": "Treasury Management ATO via Malvertising and Vishing",
  "description": "Threat actor uses malvertising and vishing to gain access to treasury management platforms, then initiates unauthorized wire transfers.",
  "scheme_type": "ato",
  "cfpf_phases": ["P1", "P2", "P3", "P4", "P5"],
  "loss_estimate": {
    "low": 500000,
    "high": 5000000,
    "currency": "USD"
  },
  "affected_sectors": ["banking"],
  "kill_chain_phases": [
    { "kill_chain_name": "cfpf", "phase_name": "P1-reconnaissance" },
    { "kill_chain_name": "cfpf", "phase_name": "P2-initial-access" },
    { "kill_chain_name": "cfpf", "phase_name": "P3-positioning" },
    { "kill_chain_name": "cfpf", "phase_name": "P4-execution" },
    { "kill_chain_name": "cfpf", "phase_name": "P5-monetization" }
  ],
  "confidence_score": 82,
  "object_marking_refs": ["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"],
  "external_references": [
    {
      "source_name": "FLAME",
      "url": "https://elchacal801.github.io/flame-fraud/threat-path/TP-0001",
      "external_id": "TP-0001"
    }
  ]
}
```

---

## 8. References

- [STIX 2.1 Specification (OASIS)](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [STIX 2.1 Custom Objects](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_p2sz1mp7z524)
- [FS-ISAC Cyber Fraud Prevention Framework (CFPF)](https://www.fsisac.com/hubfs/Knowledge/Fraud/CyberFraudPreventionFramework.pdf)
- [FLAME Taxonomy Reference](TAXONOMY.md)
