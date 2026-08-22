#!/usr/bin/env python3
"""
f3_mapper.py - MITRE F3 (Fight Fraud Framework) Auto-Mapper for FLAME Threat Paths

Reads the vendored F3 JSON files and each threat path's existing YAML
frontmatter, then suggests appropriate F3 technique IDs for each threat
path using three mapping signals:
    1. CFPF phase -> F3 tactic position alignment
    2. Group-IB stage -> F3 tactic name matching
    3. Fraud type keywords -> F3 technique name/description matching

Usage:
    python scripts/f3_mapper.py                    # dry-run (default)
    python scripts/f3_mapper.py --apply            # update frontmatter
    python scripts/f3_mapper.py --root /path/to/repo

Output:
    data/f3_mapping_suggestions.json  (written to repo data dir)
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
log = logging.getLogger("f3_mapper")

# ---------------------------------------------------------------------------
# Constants — mapping tables
# ---------------------------------------------------------------------------

# F3 Tactics (7 total):
#   TA0043 Reconnaissance         (ATT&CK-derived)
#   TA0042 Resource Development   (ATT&CK-derived)
#   TA0001 Initial Access         (ATT&CK-derived)
#   FA0001 Positioning            (F3-native)
#   TA0002 Execution              (ATT&CK-derived)
#   TA0005 Defense Evasion        (ATT&CK-derived)
#   FA0002 Monetization           (F3-native)

# CFPF phase -> F3 tactic IDs (kill chain position alignment)
CFPF_TO_F3_TACTICS: dict[str, list[str]] = {
    "P1": ["TA0043", "TA0042"],
    "P2": ["TA0001"],
    "P3": ["FA0001"],
    "P4": ["TA0002", "TA0005"],
    "P5": ["FA0002"],
}

# Group-IB stage name -> F3 tactic ID (name alignment)
GROUPIB_TO_F3_TACTIC: dict[str, str] = {
    "Reconnaissance":       "TA0043",
    "Resource Development": "TA0042",
    "Initial Access":       "TA0001",
    "Social Engineering":   "TA0001",
    "Trust Abuse":          "TA0001",
    "End-user Interaction": "TA0001",
    "Credential Access":    "FA0001",
    "Account Access":       "FA0001",
    "Lateral Movement":     "FA0001",
    "Execution":            "TA0002",
    "Perform Fraud":        "TA0002",
    "Defence Evasion":      "TA0005",
    "Defense Evasion":      "TA0005",
    "Cash Out":             "FA0002",
    "Monetization":         "FA0002",
    "Laundering":           "FA0002",
}

# Fraud-type keyword -> F3 technique search terms
FRAUD_TYPE_KEYWORDS: dict[str, list[str]] = {
    "account-takeover": [
        "account takeover", "credential", "password", "login",
        "session", "exposed credential", "password reset", "brute force",
        "SIM card swap",
    ],
    "vishing": [
        "phone number spoofing", "impersonate", "official", "voice",
        "interactive voice",
    ],
    "wire-fraud": [
        "wire transfer", "electronic funds transfer", "transfer of funds",
        "payment", "scheduled transfer",
    ],
    "BEC": [
        "email", "impersonate", "delete relevant emails",
        "account manipulation", "change of payment", "wire transfer",
    ],
    "business-email-compromise": [
        "email", "impersonate", "delete relevant emails",
        "account manipulation", "change of payment", "wire transfer",
    ],
    "invoice-fraud": [
        "invoice", "payment", "billing", "falsify business documents",
        "new vendor",
    ],
    "payment-diversion": [
        "payment", "change of payment", "add beneficiary",
        "electronic funds transfer", "wire transfer",
    ],
    "synthetic-identity": [
        "fake materials", "fake documents", "identity",
        "create fake", "fabricat", "establish accounts",
    ],
    "new-account-fraud": [
        "establish accounts", "create fake", "application",
        "fake documents", "fraudulent merchant",
    ],
    "check-fraud": [
        "check fraud", "deposit", "mobile deposit", "mail theft",
        "counterfeit", "bank deposit",
    ],
    "card-not-present-fraud": [
        "3DS bypass", "card testing", "PAN", "CVV", "virtual cards",
        "counterfeit card",
    ],
    "card-testing": [
        "card testing", "test payment", "PAN", "CVV",
    ],
    "phishing": [
        "phishing", "fake website", "credential", "drive-by compromise",
        "adversary-in-the-middle",
    ],
    "social-engineering": [
        "impersonate", "phone number spoofing", "phishing",
        "fake materials",
    ],
    "impersonation": [
        "impersonate official", "impersonate account holder",
        "phone number spoofing", "fake materials",
    ],
    "authorized-push-payment": [
        "impersonate", "electronic funds transfer", "wire transfer",
        "transfer of funds", "phone number spoofing",
    ],
    "investment-scam": [
        "convert to cryptocurrency", "fake materials", "fake website",
        "impersonate", "electronic funds transfer",
    ],
    "romance-scam": [
        "impersonate", "social media", "fake materials",
        "electronic funds transfer", "convert to cryptocurrency",
    ],
    "crypto-laundering": [
        "convert to cryptocurrency", "structuring",
        "electronic funds transfer", "transfer of funds",
    ],
    "money-mule": [
        "bank deposit", "electronic funds transfer", "transfer of funds",
        "structuring", "establish accounts",
    ],
    "deepfake": [
        "fake materials", "fake documents", "impersonate",
        "phone number spoofing",
    ],
    "identity-theft": [
        "gather customer information", "fake documents",
        "account takeover", "establish accounts",
    ],
    "credential-stuffing": [
        "brute force", "credential stuffing", "password",
        "account takeover", "exposed credential",
    ],
    "insider-threat": [
        "insider access", "account manipulation",
        "gather customer information",
    ],
    "first-party-fraud": [
        "dispute legitimate transaction", "reversal of transaction",
        "churning",
    ],
    "bust-out": [
        "churning", "dispute", "reversal of transaction",
        "fraudulent purchasing",
    ],
    "friendly-fraud": [
        "dispute legitimate transaction", "reversal of transaction",
        "churning",
    ],
    "chargeback-abuse": [
        "dispute legitimate transaction", "reversal of transaction",
    ],
    "documentary-fraud": [
        "falsify business documents", "fake documents",
        "fake materials", "create fake",
    ],
    "healthcare-fraud": [
        "falsify business documents", "fraudulent purchasing",
        "insider access",
    ],
    "insurance-fraud": [
        "falsify business documents", "fake documents",
        "fraudulent purchasing",
    ],
    "elder-exploitation": [
        "impersonate official", "phone number spoofing",
        "convert to cryptocurrency", "conversion to physical",
    ],
    "gift-card-fraud": [
        "conversion to physical monetary", "fraudulent purchasing",
    ],
    "malware": [
        "adversary-in-the-browser", "DLL injection", "malicious browser",
        "remote access", "screen capture",
    ],
    "e-skimmer": [
        "malicious JavaScript injection", "card dump capture",
        "adversary-in-the-browser",
    ],
    "approval-phishing": [
        "adversary-in-the-browser", "phishing", "session",
    ],
    "nfc-relay": [
        "NFC payment", "counterfeit card",
    ],
    "digital-wallet-fraud": [
        "NFC payment", "account manipulation", "virtual cards",
    ],
    "loan-fraud": [
        "falsify business documents", "fake documents",
        "application", "establish accounts",
    ],
    "sanctions-evasion-infrastructure": [
        "structuring", "convert to cryptocurrency",
        "electronic funds transfer",
    ],
    "advance-fee-fraud": [
        "impersonate", "fake materials", "electronic funds transfer",
    ],
    "recovery-fraud": [
        "impersonate official", "fake materials", "fake website",
        "electronic funds transfer",
    ],
    "government-impersonation-app": [
        "impersonate official", "phone number spoofing",
        "convert to cryptocurrency", "conversion to physical",
    ],
    "gold-courier-scam": [
        "impersonate official", "conversion to physical monetary",
        "phone number spoofing",
    ],
    "crypto-atm-fraud": [
        "convert to cryptocurrency", "impersonate official",
        "phone number spoofing",
    ],
    "sim-swap": [
        "SIM card swap", "multi-factor authentication",
        "account takeover",
    ],
    "aitm-phishing": [
        "adversary-in-the-middle", "adversary-in-the-browser",
        "steal web session", "phishing",
    ],
    "smishing": [
        "phishing", "phone number spoofing", "fake website",
    ],
    "quishing": [
        "phishing", "fake website", "fake materials",
    ],
}


# Extension (2026-08): fraud types introduced after the April 2026 mapping
# run had no keyword coverage, so signal 3 produced zero technique matches
# and --apply wrote empty mitre_f3 lists. Terms below are grounded in the
# actual F3 technique-name vocabulary (data/f3/F3_Techniques.json).
FRAUD_TYPE_KEYWORDS.update({
    "fraudulent-claim": ["falsify business documents", "fake documents", "dispute legitimate transaction"],
    "disability-fraud": ["falsify business documents", "fake documents"],
    "provider-fraud": ["falsify business documents", "fraudulent merchant account", "invoice"],
    "rdga-infrastructure": ["acquire infrastructure", "domains", "seo poisoning"],
    "traffic-distribution-system": ["acquire infrastructure", "domains", "seo poisoning", "malvertising", "drive-by"],
    "cloaking": ["geolocation spoofing", "device fingerprint spoofing", "seo poisoning"],
    "geo-routing": ["geolocation spoofing"],
    "investment-fraud": ["convert to cryptocurrency", "fake website", "electronic funds transfer", "gather customer information"],
    "state-criminal-convergence": ["acquire infrastructure", "convert to cryptocurrency", "structuring", "supply chain compromise"],
    "crypto-laundering-infrastructure": ["convert to cryptocurrency", "structuring", "peer-to-peer transfer", "transfer of funds"],
    "cmln-operations": ["convert to cryptocurrency", "structuring", "transfer of funds"],
    "money-laundering": ["structuring", "convert to cryptocurrency", "money order", "bank deposit", "transfer of funds"],
    "automated-mule-accounts": ["establish accounts", "fake documents", "device fingerprint spoofing", "test deposit"],
    "bot-driven-account-opening": ["establish accounts", "fake documents", "abuse of public-facing api"],
    "kyc-circumvention": ["fake documents", "device fingerprint spoofing", "geolocation spoofing"],
    "bulletproof-hosting": ["acquire infrastructure", "virtual private network", "stage capabilities"],
    "fraud-enabling-infrastructure": ["acquire infrastructure", "domains", "virtual private network", "stage capabilities"],
    "hosting-provider-complicity": ["acquire infrastructure", "virtual private network"],
    "infrastructure-rotation": ["acquire infrastructure", "domains", "indicator removal"],
    "travel-booking-fraud": ["fradulent purchasing", "fake website", "use virtual cards"],
    "fake-ota": ["fake website", "fraudulent merchant account"],
    "buy-for-you-fraud": ["fradulent purchasing", "use virtual cards", "card testing"],
    "loyalty-point-laundering": ["account manipulation", "transfer of funds"],
    "irsf": ["phone number spoofing", "interactive voice response", "abuse sms"],
    "premium-rate-fraud": ["phone number spoofing", "abuse sms", "interactive voice response"],
    "telecom-revenue-fraud": ["phone number spoofing", "abuse sms", "sim card swap"],
    "wangiri": ["phone number spoofing", "interactive voice"],
    "subscription-fraud": ["establish accounts", "fake documents", "churning"],
    "telecom-billing-fraud": ["abuse sms", "account manipulation", "sim card swap"],
    "premium-sms-fraud": ["abuse sms", "phone number spoofing"],
    "title-fraud": ["falsify business documents", "fake documents", "impersonate account holder", "email spoofing"],
    "deed-theft": ["falsify business documents", "fake documents", "impersonate account holder"],
    "seller-impersonation": ["impersonate account holder", "email spoofing", "fake documents"],
    "appraisal-fraud": ["falsify business documents", "fake documents"],
    "ghost-broking": ["fake website", "fraudulent merchant account", "impersonate official", "fake documents"],
    "ghost-portal": ["fake website", "fraudulent merchant account"],
    "insurance-policy-fraud": ["falsify business documents", "fake documents"],
    "unlicensed-insurance": ["fake website", "impersonate official"],
    "affiliate-fraud": ["malvertising", "seo poisoning", "malicious browser extension"],
    "click-fraud": ["malvertising", "malicious browser extension", "abuse of public-facing api"],
    "ad-fraud": ["malvertising", "seo poisoning"],
    "cookie-stuffing": ["steal web session cookie", "malicious browser extension", "session cookie"],
    "invalid-traffic": ["malvertising", "device fingerprint spoofing"],
})



# ---------------------------------------------------------------------------
# F3 data loading
# ---------------------------------------------------------------------------

def load_f3_tactics(path: Path) -> dict[str, dict]:
    """Load F3 tactics JSON, keyed by tactic ID."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return {t["ID"]: t for t in data}


def load_f3_techniques(path: Path) -> list[dict]:
    """Load F3 techniques JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Frontmatter parsing (reuse FLAME convention)
# ---------------------------------------------------------------------------

FRONTMATTER_PATTERN = re.compile(
    r"```ya?ml\s*\n---\s*\n(.*?)\n---\s*\n```",
    re.DOTALL,
)


def extract_frontmatter_raw(filepath: Path) -> tuple[dict | None, str]:
    """Extract YAML frontmatter dict and the raw YAML string."""
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml is required. Install with: pip install pyyaml",
              file=sys.stderr)
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.search(text)
    if not match:
        return None, ""
    raw_yaml = match.group(1)
    try:
        data = yaml.safe_load(raw_yaml)
    except Exception as e:
        log.error("YAML parse error in %s: %s", filepath, e)
        return None, raw_yaml
    if not isinstance(data, dict):
        return None, raw_yaml
    return data, raw_yaml


# ---------------------------------------------------------------------------
# Mapping logic
# ---------------------------------------------------------------------------

def map_cfpf_to_tactics(cfpf_phases: list[str]) -> set[str]:
    """Signal 1: Map CFPF phases to F3 tactic IDs."""
    result: set[str] = set()
    for phase in cfpf_phases:
        phase_key = phase.strip().upper()
        if phase_key in CFPF_TO_F3_TACTICS:
            result.update(CFPF_TO_F3_TACTICS[phase_key])
    return result


def map_groupib_to_tactics(groupib_stages: list[str]) -> set[str]:
    """Signal 2: Map Group-IB stages to F3 tactic IDs."""
    result: set[str] = set()
    for stage in groupib_stages:
        stage_clean = stage.strip()
        if stage_clean in GROUPIB_TO_F3_TACTIC:
            result.add(GROUPIB_TO_F3_TACTIC[stage_clean])
    return result


def map_fraud_types_to_techniques(
    fraud_types: list[str],
    techniques: list[dict],
) -> list[tuple[str, str, float]]:
    """Signal 3: Match fraud_types keywords against F3 technique names/descriptions.

    Returns list of (technique_id, technique_name, score) tuples,
    sorted by score descending.
    """
    all_terms: list[str] = []
    for ft in fraud_types:
        ft_key = ft.strip().lower()
        if ft_key in FRAUD_TYPE_KEYWORDS:
            all_terms.extend(FRAUD_TYPE_KEYWORDS[ft_key])
        else:
            all_terms.append(ft_key.replace("-", " "))

    if not all_terms:
        return []

    scored: list[tuple[str, str, float]] = []
    for tech in techniques:
        tech_id = tech["ID"]
        tech_name = tech.get("name", "").lower()
        tech_desc = tech.get("description", "").lower()
        searchable = tech_name + " " + tech_desc

        score = 0.0
        matched_terms: set[str] = set()
        for term in all_terms:
            term_lower = term.lower()
            if term_lower in matched_terms:
                continue
            if term_lower in tech_name:
                score += 3.0
                matched_terms.add(term_lower)
            elif term_lower in searchable:
                score += 1.0
                matched_terms.add(term_lower)

        if score > 0:
            scored.append((tech_id, tech["name"], score))

    scored.sort(key=lambda x: x[2], reverse=True)
    return scored


def determine_confidence(
    cfpf_tactics: set[str],
    groupib_tactics: set[str],
    technique_matches: list[tuple[str, str, float]],
) -> str:
    signals_active = 0
    if cfpf_tactics:
        signals_active += 1
    if groupib_tactics:
        signals_active += 1
    if technique_matches:
        signals_active += 1
    if signals_active >= 3:
        return "high"
    elif signals_active >= 2:
        return "medium"
    else:
        return "low"


def map_single_tp(
    meta: dict,
    techniques: list[dict],
) -> dict:
    """Map a single threat path to F3 suggestions."""
    tp_id = meta.get("id", "unknown")
    cfpf_phases = meta.get("cfpf_phases", [])
    groupib_stages = meta.get("groupib_stages", [])
    fraud_types = meta.get("fraud_types", [])

    if isinstance(cfpf_phases, list):
        cfpf_phases = [str(p) for p in cfpf_phases]
    else:
        cfpf_phases = []
    if isinstance(groupib_stages, list):
        groupib_stages = [str(s) for s in groupib_stages]
    else:
        groupib_stages = []
    if isinstance(fraud_types, list):
        fraud_types = [str(f) for f in fraud_types]
    else:
        fraud_types = []

    # Signal 1: CFPF -> F3 tactics
    cfpf_tactics = map_cfpf_to_tactics(cfpf_phases)

    # Signal 2: Group-IB -> F3 tactics
    groupib_tactics = map_groupib_to_tactics(groupib_stages)

    # Signal 3: Fraud type -> F3 techniques
    technique_matches = map_fraud_types_to_techniques(fraud_types, techniques)

    # Filter: prefer parent techniques, cap at 10
    top_techniques: list[tuple[str, str, float]] = []
    seen_parents: set[str] = set()
    for tid, tname, score in technique_matches:
        is_sub = "." in tid
        parent_id = tid.split(".")[0] if is_sub else tid
        if is_sub:
            if parent_id not in seen_parents and score >= 4.0:
                top_techniques.append((tid, tname, score))
                seen_parents.add(parent_id)
        else:
            if parent_id not in seen_parents:
                top_techniques.append((tid, tname, score))
                seen_parents.add(parent_id)
        if len(top_techniques) >= 10:
            break

    confidence = determine_confidence(cfpf_tactics, groupib_tactics, top_techniques)

    return {
        "suggested_f3_techniques": [t[0] for t in top_techniques],
        "confidence": confidence,
        "_detail": {
            "cfpf_tactics": sorted(cfpf_tactics),
            "groupib_tactics": sorted(groupib_tactics),
            "technique_scores": [
                {"id": t[0], "name": t[1], "score": t[2]}
                for t in top_techniques
            ],
        },
    }


# ---------------------------------------------------------------------------
# Apply mode — update YAML frontmatter
# ---------------------------------------------------------------------------

def apply_f3_techniques(filepath: Path, technique_ids: list[str]) -> bool:
    """Update the mitre_f3 field in a threat path's YAML frontmatter."""
    text = filepath.read_text(encoding="utf-8")

    if technique_ids:
        items = ", ".join(f'"{tid}"' for tid in technique_ids)
        replacement = f"mitre_f3: [{items}]"
    else:
        replacement = "mitre_f3: []"

    # Match existing mitre_f3 line (handles [] or multi-line)
    pattern_inline = re.compile(
        r"^(mitre_f3:\s*\[.*?\])(\s*#.*)?$",
        re.MULTILINE,
    )
    pattern_block = re.compile(
        r"^mitre_f3:\s*\n((?:\s+-\s+.*\n)*)",
        re.MULTILINE,
    )

    match_inline = pattern_inline.search(text)
    match_block = pattern_block.search(text)

    if match_inline:
        comment = match_inline.group(2) or ""
        new_text = (
            text[:match_inline.start()]
            + replacement
            + text[match_inline.end():]
        )
    elif match_block:
        new_text = (
            text[:match_block.start()]
            + replacement + "\n"
            + text[match_block.end():]
        )
    else:
        log.warning("Could not find mitre_f3 field in %s", filepath)
        return False

    filepath.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MITRE F3 Auto-Mapper for FLAME Threat Paths",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Root directory of the FLAME repository",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply suggested mappings to frontmatter YAML (default: dry-run)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSON path (default: <root>/data/f3_mapping_suggestions.json)",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Comma-separated TP ids (e.g. TP-0010,TP-0041) to restrict the run to",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --apply: overwrite non-empty existing mappings (default: skip them)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output_path = args.output or (root / "data" / "f3_mapping_suggestions.json")

    log.info("MITRE F3 Auto-Mapper for FLAME Threat Paths")
    log.info("Root: %s", root)
    log.info("Mode: %s", "APPLY" if args.apply else "dry-run")

    # Load F3 data
    tactics_path = root / "data" / "f3" / "F3_Tactics.json"
    techniques_path = root / "data" / "f3" / "F3_Techniques.json"

    if not tactics_path.exists():
        log.error("F3 Tactics JSON not found: %s", tactics_path)
        sys.exit(1)
    if not techniques_path.exists():
        log.error("F3 Techniques JSON not found: %s", techniques_path)
        sys.exit(1)

    tactics = load_f3_tactics(tactics_path)
    techniques = load_f3_techniques(techniques_path)

    log.info("Loaded %d tactics, %d techniques", len(tactics), len(techniques))

    # Find threat path files
    tp_dir = root / "ThreatPaths"
    tp_files = sorted(tp_dir.glob("TP-*.md"))
    log.info("Found %d threat path files", len(tp_files))
    if args.only:
        wanted = {t.strip() for t in args.only.split(",") if t.strip()}
        tp_files = [f for f in tp_files if f.name[:7] in wanted]
        log.info("Restricted to %d file(s) via --only", len(tp_files))


    if not tp_files:
        log.error("No threat path files found in %s", tp_dir)
        sys.exit(1)

    # Process each threat path
    results: dict[str, dict] = {}
    confidence_counts = {"high": 0, "medium": 0, "low": 0}

    for filepath in tp_files:
        meta, raw_yaml = extract_frontmatter_raw(filepath)
        if meta is None:
            log.warning("Skipping %s: no valid frontmatter", filepath.name)
            continue

        tp_id = meta.get("id", filepath.stem)
        mapping = map_single_tp(meta, techniques)
        results[tp_id] = mapping
        confidence_counts[mapping["confidence"]] += 1

        techs_str = ", ".join(mapping["suggested_f3_techniques"][:5])
        log.info(
            "  %s [%s]: %d techniques [%s%s]",
            tp_id,
            mapping["confidence"],
            len(mapping["suggested_f3_techniques"]),
            techs_str,
            "..." if len(mapping["suggested_f3_techniques"]) > 5 else "",
        )

    # Write output JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Wrote mapping suggestions to %s", output_path)

    # Summary
    log.info("---")
    log.info("Mapping summary:")
    log.info("  Total TPs: %d", len(results))
    log.info("  High confidence:   %d", confidence_counts["high"])
    log.info("  Medium confidence: %d", confidence_counts["medium"])
    log.info("  Low confidence:    %d", confidence_counts["low"])

    zero_mappings = sum(
        1 for r in results.values() if not r["suggested_f3_techniques"]
    )
    if zero_mappings:
        log.warning("  TPs with 0 technique suggestions: %d", zero_mappings)

    # Apply mode
    if args.apply:
        log.info("---")
        log.info("Applying F3 mappings to frontmatter...")
        applied = 0
        for filepath in tp_files:
            meta, _ = extract_frontmatter_raw(filepath)
            if meta is None:
                continue
            tp_id = meta.get("id", filepath.stem)
            if tp_id not in results:
                continue
            existing = meta.get("mitre_f3") or []
            if existing and not args.force:
                log.info("  Skipping %s: mitre_f3 already populated (%d ids); use --force to overwrite",
                         tp_id, len(existing))
                continue
            technique_ids = results[tp_id]["suggested_f3_techniques"]
            if apply_f3_techniques(filepath, technique_ids):
                log.info("  Applied to %s: %d techniques", tp_id, len(technique_ids))
                applied += 1
            else:
                log.warning("  FAILED to apply to %s", tp_id)
        log.info("Applied F3 mappings to %d files", applied)

    return 0


if __name__ == "__main__":
    sys.exit(main())
