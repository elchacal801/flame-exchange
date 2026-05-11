#!/usr/bin/env python3
"""Tag all 89 threat paths with short_name frontmatter for matrix chip display."""

import os
import glob

# Curated short names: 2-4 words, unique, max ~22 chars
SHORT_NAMES = {
    "TP-0001": "Treasury ATO",
    "TP-0002": "BEC Wire",
    "TP-0003": "Synth ID Bust-Out",
    "TP-0004": "Payroll Diversion",
    "TP-0005": "Premium Diversion",
    "TP-0006": "Real Estate Wire",
    "TP-0007": "Deepfake Voice Wire",
    "TP-0008": "SIM Swap ATO",
    "TP-0009": "Check Washing",
    "TP-0010": "Disability Fraud",
    "TP-0011": "Romance Mule Pipeline",
    "TP-0012": "APP Tech Support",
    "TP-0013": "Cred Stuff Loyalty",
    "TP-0014": "Insider Fraud",
    "TP-0015": "Employment Fraud",
    "TP-0016": "First-Party Bust-Out",
    "TP-0017": "Pig Butchering",
    "TP-0018": "Deepfake Docs",
    "TP-0019": "Business ID Theft",
    "TP-0020": "Supply Chain Wire",
    "TP-0021": "Healthcare Billing",
    "TP-0022": "Gov Program Fraud",
    "TP-0023": "Mobile Trojan",
    "TP-0024": "A2A Payment Fraud",
    "TP-0025": "GenAI APP Romance",
    "TP-0026": "GenAI APP Investment",
    "TP-0027": "Elder Exploitation",
    "TP-0028": "DME Phantom Billing",
    "TP-0029": "AI Synth ID Forgery",
    "TP-0030": "Triangulation Fraud",
    "TP-0031": "Refund-as-a-Service",
    "TP-0032": "Wallet Drainer",
    "TP-0033": "Ghost Student Aid",
    "TP-0034": "DPRK IT Worker",
    "TP-0035": "Magecart Skimmer",
    "TP-0036": "Purchase Scam",
    "TP-0037": "NFC Relay Fraud",
    "TP-0038": "Card Testing",
    "TP-0039": "Agentic Commerce",
    "TP-0040": "BNPL Stacking",
    "TP-0041": "RDGA Domains",
    "TP-0042": "TDS Chains",
    "TP-0043": "AI Infra Gen",
    "TP-0044": "State-Criminal Infra",
    "TP-0045": "Sanctions Evasion",
    "TP-0046": "Geo-Timed Campaigns",
    "TP-0047": "Trafficking Infra",
    "TP-0048": "BPH Migration",
    "TP-0049": "Crypto Laundering",
    "TP-0050": "Calendar Phishing",
    "TP-0051": "Quishing",
    "TP-0052": "Sextortion Hybrid",
    "TP-0053": "Vehicle Export Fraud",
    "TP-0054": "FaaS Platforms",
    "TP-0055": "Crypto Terror Nexus",
    "TP-0056": "Insurance Claims",
    "TP-0057": "DFaaS Marketplace",
    "TP-0058": "Scam Compounds",
    "TP-0059": "Auto Mule Infra",
    "TP-0060": "Investment TDS",
    "TP-0061": "TAE BPH Infra",
    "TP-0062": "Recovery Fraud",
    "TP-0063": "Counterfeit Networks",
    "TP-0064": "Long-Firm Fraud",
    "TP-0065": "Boiler Room Infra",
    "TP-0066": "Crash-for-Cash",
    "TP-0067": "AiTM Phishing Kit",
    "TP-0068": "Gift Card Fraud",
    "TP-0069": "Smishing PhaaS",
    "TP-0070": "Travel Booking Fraud",
    "TP-0071": "IRSF Revenue Fraud",
    "TP-0072": "Telecom Sub Fraud",
    "TP-0073": "Title/Deed Theft",
    "TP-0074": "Ghost Broking",
    "TP-0075": "Friendly Fraud",
    "TP-0076": "Affiliate Fraud",
    "TP-0077": "AI Claims Fraud",
    "TP-0078": "Stablecoin CEX Launder",
    "TP-0079": "gTLD Subdomain Abuse",
    "TP-0080": "Freeze Evasion",
    "TP-0081": "Vishing Hybrid",
    "TP-0082": "Gold Courier Scam",
    "TP-0083": "Investment Club Scam",
    "TP-0084": "Gov Impersonation APP",
    "TP-0085": "Crypto ATM Fraud",
    "TP-0086": "Crisis Exploitation",
    "TP-0087": "Infostealer Pipeline",
    "TP-0088": "Logistics Spearphish",
    "TP-0089": "TAE Transit Complicity",
}

THREAT_PATHS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ThreatPaths")


def tag_file(filepath, short_name):
    """Insert short_name after primary_phase in YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "short_name:" in content:
        print(f"  SKIP (already tagged): {os.path.basename(filepath)}")
        return False

    lines = content.split("\n")
    insert_idx = None

    for i, line in enumerate(lines):
        if line.strip().startswith("primary_phase:"):
            insert_idx = i
            break

    if insert_idx is None:
        print(f"  ERROR (no primary_phase found): {os.path.basename(filepath)}")
        return None

    new_line = f'short_name: "{short_name}"'
    lines = lines[: insert_idx + 1] + [new_line] + lines[insert_idx + 1 :]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  OK: {os.path.basename(filepath)} -> {short_name}")
    return True


def main():
    # Validate uniqueness
    seen = {}
    for tp_id, name in SHORT_NAMES.items():
        if name in seen:
            print(f"  DUPLICATE short_name '{name}': {seen[name]} and {tp_id}")
            return
        seen[name] = tp_id
    print(f"All {len(SHORT_NAMES)} short_names are unique")

    files = glob.glob(os.path.join(THREAT_PATHS_DIR, "TP-*.md"))
    print(f"Found {len(files)} threat path files")

    tagged = 0
    skipped = 0
    errors = 0

    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        tp_id = basename[:7]

        if tp_id not in SHORT_NAMES:
            print(f"  WARN (no short_name): {basename}")
            errors += 1
            continue

        result = tag_file(filepath, SHORT_NAMES[tp_id])
        if result is True:
            tagged += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1

    print(f"\nDone: {tagged} tagged, {skipped} skipped, {errors} errors")

    # Length stats
    lengths = [len(n) for n in SHORT_NAMES.values()]
    print(f"\nShort name lengths: min={min(lengths)}, max={max(lengths)}, avg={sum(lengths)/len(lengths):.1f}")
    long_names = [(k, v) for k, v in SHORT_NAMES.items() if len(v) > 20]
    if long_names:
        print(f"Names over 20 chars ({len(long_names)}):")
        for k, v in long_names:
            print(f"  {k}: '{v}' ({len(v)} chars)")


if __name__ == "__main__":
    main()
