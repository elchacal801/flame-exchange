#!/usr/bin/env python3
"""
FLAME Detection Logic — CI Validation Script

Validates all DL-XXXX rules against the FLAME detection logic specification:
1. sigma_compatible flag is present and accurate
2. Rules marked sigma_compatible: false have queries block (logscale + splunk)
3. All logsource definitions have pipeline mappings
4. All enrichment-required fields are documented in data_sources
5. Framework tags (CFPF + ATT&CK) are present

Exit codes:
  0 = all checks pass
  1 = one or more checks failed
"""

import yaml
import os
import re
import sys
import json

DL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DetectionLogic")
PIPELINE_DIR = os.path.join(DL_DIR, "pipelines")

# Known enrichment fields that MUST be documented if used
ENRICHMENT_FIELDS = {
    "src_ip_type", "src_ip_vpn_provider", "connection_hops",
    "source_ip_threat_intel", "source_ip_category", "source_asn_type",
    "domain_age_days", "script_domain_age_days", "device_trust_level",
    "device_first_seen_days", "device_first_seen",
    "voice_confidence_score", "historical_avg_score",
    "gan_artifact_score", "font_consistency_score", "microprint_validation",
    "spectral_flatness_score", "pitch_variance", "codec_reencoding_detected",
    "breath_sound_detected", "frame_rate_variance", "lip_sync_offset_ms",
    "blink_rate_per_minute", "face_background_lighting_delta",
    "merchant_risk_score", "merchant_dispute_rate_pct", "merchant_age_days",
    "amount_exceeds_3x_user_avg", "category_in_user_history",
    "ani_matches_directory", "callback_number_verified",
    "phone_number_type", "phone_carrier",
    "geo_distance_km", "required_speed_kmh",
    "account_dormancy_days", "account_age_days", "account_balance",
    "post_transaction_balance",
    "beneficiary_country_first_time", "beneficiary_country_in_business_profile",
    "beneficiary_name_match", "beneficiary_relationship_days",
    "beneficiary_bank_relationship",
    "credential_change_hours_ago", "time_since_auth_minutes",
    "time_since_deposit_hours",
    "registration_volume_zscore", "registration_volume_ratio",
    "inter_registration_stddev",
    "domain_cluster_similarity_score", "ns_pattern_similarity_score",
    "intermediate_domain_max_age_days", "intermediate_domain_min_reputation",
    "ip_cidr_overlap", "registrant_divergence", "registration_time_delta",
    "weekday_volume_ratio", "clustering_to_no_kyc_exchanges",
    "avg_processing_time", "outbound_to_exchange_ratio", "cname_density",
    "digital_footprint_score", "email_domain_age_days",
    "chargeback_ratio_pct", "decline_rate", "recurring_transaction_pct",
    "prior_transaction_count", "user_tenure_days",
    "daily_transaction_count", "daily_volume_usd",
    "outbound_amount_pct_of_inbound", "amount_pct_of_rail_limit",
    "payee_relationship", "target_domain_age_days",
    "inbound_source_count", "shared_nameserver_ratio",
    "shared_ns_infrastructure", "nameserver_reuse_cross_attribution",
    "shared_registrar", "privacy_protected_whois",
    "diverse_registrants", "different_asn",
    "new_entity_same_asn", "new_entity_same_ip_range",
    "new_entity_same_transit_provider",
    "previously_sanctioned_ip_range", "previous_ip_range_sanctioned",
    "days_since_ofac_designation", "days_since_sanctioned_entity_shutdown",
    "event_within_sanctions_designation",
    "ip_block_migration", "new_ip_range_different",
    "cloud_provider_ip", "abuse_ratio", "migration_window_days",
    "new_bgp_announcement", "attribution_category",
    "target_is_financial_services", "geopolitical_event_within",
    "l7_dns_query_volume_ratio",
    "cname_chain_depth", "cname_chain_endpoint_count",
    "crypto_payment_indicators", "lexical_nlp_score", "domain_word_count",
    "dga_entropy_score", "registration_to_cert_delta",
    "wallet_cluster", "bulk_registered_domains", "unique_domain_count",
    "domain_registration_delta", "registration_date_within_election",
    "shared_ip_cidr_overlap",
}

# Non-standard Sigma condition patterns
NON_SIGMA_PATTERNS = [
    r'\|\s*count\s*\(',
    r'\|\s*near\b',
    r'\|\s*where\b',
    r'followed_by\b',
    r'temporal\s*\(',
    r'compare\s*\(',
    r'stddev\s*\(',
    r'geo_distance\s*\(',
    r'\bdc\s*\(',
    r'(?<!\w)count\s*\(',
]


def condition_is_sigma_compatible(condition):
    """Check if a condition string is valid Sigma grammar."""
    for pattern in NON_SIGMA_PATTERNS:
        if re.search(pattern, condition, re.IGNORECASE):
            return False
    return True


def get_fields_from_detection(detection):
    """Extract all field names from detection block."""
    fields = set()
    for key, val in detection.items():
        if key in ('condition', 'timeframe'):
            continue
        if isinstance(val, dict):
            for fk in val.keys():
                base_field = fk.split('|')[0]
                fields.add(base_field)
    return fields


def load_pipeline_logsources(pipeline_path):
    """Extract logsource mappings from a pipeline YAML."""
    with open(pipeline_path) as f:
        data = yaml.safe_load(f)

    logsources = set()
    for transform in data.get('transformations', []):
        for rc in transform.get('rule_conditions', []):
            if rc.get('type') == 'logsource':
                product = rc.get('product', '')
                service = rc.get('service', '')
                logsources.add((product, service))

    return logsources


class ValidationResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []

    def ok(self, msg=""):
        self.passed += 1

    def fail(self, rule_id, msg):
        self.failed += 1
        self.errors.append(f"FAIL [{rule_id}]: {msg}")

    def warn(self, rule_id, msg):
        self.warnings += 1
        self.errors.append(f"WARN [{rule_id}]: {msg}")


def main():
    result = ValidationResult()

    # Load pipeline logsources
    logscale_sources = set()
    splunk_sources = set()

    logscale_path = os.path.join(PIPELINE_DIR, "logscale.yml")
    splunk_path = os.path.join(PIPELINE_DIR, "splunk.yml")

    if os.path.exists(logscale_path):
        logscale_sources = load_pipeline_logsources(logscale_path)
        print(f"[INFO] LogScale pipeline: {len(logscale_sources)} logsource mappings")
    else:
        result.fail("PIPELINE", "logscale.yml not found")

    if os.path.exists(splunk_path):
        splunk_sources = load_pipeline_logsources(splunk_path)
        print(f"[INFO] Splunk pipeline: {len(splunk_sources)} logsource mappings")
    else:
        result.fail("PIPELINE", "splunk.yml not found")

    # Process each rule
    files = sorted([f for f in os.listdir(DL_DIR) if f.endswith('.yml') and f.startswith('DL-')])
    print(f"[INFO] Validating {len(files)} rules...\n")

    for fname in files:
        filepath = os.path.join(DL_DIR, fname)
        rule_id = fname.split('.')[0][:7]

        try:
            with open(filepath) as f:
                data = yaml.safe_load(f.read())
        except Exception as e:
            result.fail(rule_id, f"YAML parse error: {e}")
            continue

        if not isinstance(data, dict):
            result.fail(rule_id, "Not a valid YAML dictionary")
            continue

        # --- Check 1: sigma_compatible flag exists ---
        if 'sigma_compatible' not in data:
            result.fail(rule_id, "Missing sigma_compatible flag")
        else:
            result.ok()

        # --- Check 2: If sigma_compatible: false, must have native_query_required and queries ---
        if data.get('sigma_compatible') == False:
            if not data.get('native_query_required'):
                result.fail(rule_id, "sigma_compatible: false but missing native_query_required: true")
            else:
                result.ok()

            queries = data.get('queries', {})
            if not queries:
                result.fail(rule_id, "sigma_compatible: false but no queries block")
            else:
                if 'logscale' not in queries:
                    result.fail(rule_id, "queries block missing LogScale LQL")
                else:
                    result.ok()

                if 'splunk' not in queries:
                    result.fail(rule_id, "queries block missing Splunk SPL")
                else:
                    result.ok()

        # --- Check 3: sigma_compatible flag accuracy ---
        detection = data.get('detection', {})
        condition = str(detection.get('condition', ''))
        actual_compatible = condition_is_sigma_compatible(condition)

        if data.get('sigma_compatible') == True and not actual_compatible:
            result.fail(rule_id, f"Marked sigma_compatible: true but condition has non-Sigma syntax: {condition[:80]}")
        elif data.get('sigma_compatible') == False and actual_compatible:
            # This is OK — may have been simplified, original had aggregation
            result.ok()
        else:
            result.ok()

        # --- Check 4: Logsource has pipeline mapping ---
        logsource = data.get('logsource', {})
        ls_key = (logsource.get('product', ''), logsource.get('service', ''))

        if ls_key[0] and ls_key[1]:
            if logscale_sources and ls_key not in logscale_sources:
                result.warn(rule_id, f"Logsource ({ls_key[0]}, {ls_key[1]}) not in logscale.yml pipeline")
            else:
                result.ok()

            if splunk_sources and ls_key not in splunk_sources:
                result.warn(rule_id, f"Logsource ({ls_key[0]}, {ls_key[1]}) not in splunk.yml pipeline")
            else:
                result.ok()

        # --- Check 5: Enrichment fields documented ---
        fields = get_fields_from_detection(detection)
        enrichment_fields_used = fields & ENRICHMENT_FIELDS

        if enrichment_fields_used:
            ds = data.get('data_sources', {})
            if not ds:
                result.fail(rule_id, f"Uses enrichment fields {enrichment_fields_used} but no data_sources block")
            else:
                documented_enrichment = set()
                for entry in ds.get('enrichment_required', []):
                    if isinstance(entry, dict):
                        documented_enrichment.add(entry.get('field', ''))

                undocumented = enrichment_fields_used - documented_enrichment
                if undocumented:
                    result.fail(rule_id, f"Enrichment fields not documented in data_sources: {undocumented}")
                else:
                    result.ok()
        else:
            result.ok()

        # --- Check 6: data_sources block exists ---
        if 'data_sources' not in data:
            result.warn(rule_id, "No data_sources block")
        else:
            result.ok()

        # --- Check 7: Framework tagging ---
        tags = data.get('tags', [])
        has_cfpf = any(str(t).startswith('cfpf.') for t in tags)
        has_attack = any(str(t).startswith('attack.t') for t in tags)

        if not has_cfpf:
            result.warn(rule_id, "Missing CFPF framework tag")
        else:
            result.ok()

        if not has_attack:
            result.warn(rule_id, "Missing ATT&CK technique tag")
        else:
            result.ok()

        # --- Check 8: falsepositives exists and is non-empty ---
        fps = data.get('falsepositives', [])
        if not fps:
            result.warn(rule_id, "No falsepositives entries")
        else:
            result.ok()

    # Print report
    print("=" * 60)
    print("FLAME Detection Logic Validation Report")
    print("=" * 60)
    print(f"Rules validated: {len(files)}")
    print(f"Checks passed:  {result.passed}")
    print(f"Checks failed:  {result.failed}")
    print(f"Warnings:       {result.warnings}")
    print()

    if result.errors:
        print("Issues found:")
        for err in result.errors:
            print(f"  {err}")
        print()

    if result.failed > 0:
        print("RESULT: FAILED")
        sys.exit(1)
    elif result.warnings > 0:
        print("RESULT: PASSED with warnings")
        sys.exit(0)
    else:
        print("RESULT: PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
