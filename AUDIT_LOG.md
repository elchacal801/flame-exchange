# FLAME Detection Logic Audit Log

**Date**: 2026-03-07
**Rules Audited**: 114
**Sigma Compatible**: 76
**Requires Native Queries**: 38

## Changes Applied

1. **sigma_compatible flag** added to all 114 rules
2. **native_query_required flag** added to 38 rules requiring aggregation/correlation
3. **Condition syntax fixed** on 38 rules — aggregation extracted to queries block, boolean-only condition retained
4. **data_sources block** added to all 114 rules documenting native vs enrichment fields
5. **queries block** (LogScale LQL + Splunk SPL) added to all 38 non-compatible rules
6. **Pipeline YAMLs** created: `pipelines/logscale.yml` and `pipelines/splunk.yml` with 46 logsource mappings each
7. **Framework tags** (CFPF + ATT&CK) added to 14 rules (DL-0101 through DL-0114) that were missing them
8. **CI validation script** (`scripts/validate_rules.py`) passes all 1140 checks

## Per-Rule Audit

| Rule ID | sigma_compatible | Condition Fixed | Enrichment Documented | queries Added | Platforms | FP Improved | Pipeline Mapped | Notes |
|---------|-----------------|-----------------|----------------------|--------------|-----------|-------------|-----------------|-------|
| DL-0001 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0002 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0003 | true | N | Y | N | - | N | Y |  |
| DL-0004 | true | N | Y | N | - | N | Y |  |
| DL-0005 | true | N | Y | N | - | N | Y |  |
| DL-0006 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0007 | true | N | Y | N | - | N | Y |  |
| DL-0008 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0009 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0010 | true | N | Y | N | - | N | Y |  |
| DL-0011 | true | N | Y | N | - | N | Y |  |
| DL-0012 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0013 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0014 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0015 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0016 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0017 | true | N | Y | N | - | N | Y |  |
| DL-0018 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0019 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0020 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0021 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0022 | true | N | Y | N | - | N | Y |  |
| DL-0023 | true | N | Y | N | - | N | Y |  |
| DL-0024 | true | N | Y | N | - | N | Y |  |
| DL-0025 | true | N | Y | N | - | N | Y |  |
| DL-0026 | true | N | Y | N | - | N | Y |  |
| DL-0027 | true | N | Y | N | - | N | Y |  |
| DL-0028 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0029 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0030 | true | N | Y | N | - | N | Y |  |
| DL-0031 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0032 | true | N | Y | N | - | N | Y |  |
| DL-0033 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0034 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0035 | true | N | Y | N | - | N | Y |  |
| DL-0036 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0037 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0038 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0039 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0040 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0041 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0042 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0043 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0044 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0045 | true | N | Y | N | - | N | Y |  |
| DL-0046 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0047 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0048 | true | N | Y | N | - | N | Y |  |
| DL-0049 | true | N | Y | N | - | N | Y |  |
| DL-0050 | true | N | Y | N | - | N | Y |  |
| DL-0051 | true | N | Y | N | - | N | Y |  |
| DL-0052 | true | N | Y | N | - | N | Y |  |
| DL-0053 | true | N | Y | N | - | N | Y |  |
| DL-0054 | true | N | Y | N | - | N | Y |  |
| DL-0055 | true | N | Y | N | - | N | Y |  |
| DL-0056 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0057 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0058 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0059 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0060 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0061 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0062 | true | N | Y | N | - | N | Y |  |
| DL-0063 | true | N | Y | N | - | N | Y |  |
| DL-0064 | true | N | Y | N | - | N | Y |  |
| DL-0065 | true | N | Y | N | - | N | Y |  |
| DL-0066 | true | N | Y | N | - | N | Y |  |
| DL-0067 | true | N | Y | N | - | N | Y |  |
| DL-0068 | true | N | Y | N | - | N | Y |  |
| DL-0069 | true | N | Y | N | - | N | Y |  |
| DL-0070 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0071 | true | N | Y | N | - | N | Y |  |
| DL-0072 | true | N | Y | N | - | N | Y |  |
| DL-0073 | false | Y | Y | Y | logscale, splunk | N | Y |  |
| DL-0074 | true | N | Y | N | - | N | Y |  |
| DL-0075 | true | N | Y | N | - | N | Y |  |
| DL-0076 | true | N | Y | N | - | N | Y |  |
| DL-0077 | true | N | Y | N | - | N | Y |  |
| DL-0078 | true | N | Y | N | - | N | Y |  |
| DL-0079 | true | N | Y | N | - | N | Y |  |
| DL-0080 | true | N | Y | N | - | N | Y |  |
| DL-0081 | true | N | Y | N | - | N | Y |  |
| DL-0082 | true | N | Y | N | - | N | Y |  |
| DL-0083 | true | N | Y | N | - | N | Y |  |
| DL-0084 | true | N | Y | N | - | N | Y |  |
| DL-0085 | true | N | Y | N | - | N | Y |  |
| DL-0086 | true | N | Y | N | - | N | Y |  |
| DL-0087 | true | N | Y | N | - | N | Y |  |
| DL-0088 | true | N | Y | N | - | N | Y |  |
| DL-0089 | true | N | Y | N | - | N | Y |  |
| DL-0090 | true | N | Y | N | - | N | Y |  |
| DL-0091 | true | N | Y | N | - | N | Y |  |
| DL-0092 | true | N | Y | N | - | N | Y |  |
| DL-0093 | true | N | Y | N | - | N | Y |  |
| DL-0094 | true | N | Y | N | - | N | Y |  |
| DL-0095 | true | N | Y | N | - | N | Y |  |
| DL-0096 | true | N | Y | N | - | N | Y |  |
| DL-0097 | true | N | Y | N | - | N | Y |  |
| DL-0098 | true | N | Y | N | - | N | Y |  |
| DL-0099 | true | N | Y | N | - | N | Y |  |
| DL-0100 | true | N | Y | N | - | N | Y |  |
| DL-0101 | true | N | Y | N | - | N | Y |  |
| DL-0102 | true | N | Y | N | - | N | Y |  |
| DL-0103 | true | N | Y | N | - | N | Y |  |
| DL-0104 | true | N | Y | N | - | N | Y |  |
| DL-0105 | true | N | Y | N | - | N | Y |  |
| DL-0106 | true | N | Y | N | - | N | Y |  |
| DL-0107 | true | N | Y | N | - | N | Y |  |
| DL-0108 | true | N | Y | N | - | N | Y |  |
| DL-0109 | true | N | Y | N | - | N | Y |  |
| DL-0110 | true | N | Y | N | - | N | Y |  |
| DL-0111 | true | N | Y | N | - | N | Y |  |
| DL-0112 | true | N | Y | N | - | N | Y |  |
| DL-0113 | true | N | Y | N | - | N | Y |  |
| DL-0114 | true | N | Y | N | - | N | Y |  |
