"""
FLAME Fraud Logsource Processing Pipeline for pySigma.

Maps FLAME-specific logsource product values (banking, crypto, ecommerce, telecom,
insurance, healthcare, government) to generic application categories so that pySigma
backends (Splunk, Elasticsearch/Lucene, Microsoft Sentinel/Kusto) can convert them
without encountering unknown-product errors.

NOTE: The exported queries will still require environment-specific tuning.
Field names, index names, and source types must be adjusted to match the
target SIEM deployment.
"""

from sigma.processing.conditions import LogsourceCondition
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline
from sigma.processing.transformations import ChangeLogsourceTransformation

# Map each FLAME domain-specific product to a generic logsource category/product pair.
# Backends treat "application" as a generic category that doesn't require special index
# mappings, which allows conversion to proceed without errors.
FLAME_PRODUCT_MAP: dict[str, dict[str, str]] = {
    "banking": {
        "category": "application",
        "product": "banking_platform",
    },
    "insurance": {
        "category": "application",
        "product": "insurance_platform",
    },
    "ecommerce": {
        "category": "application",
        "product": "ecommerce_platform",
    },
    "crypto": {
        "category": "application",
        "product": "crypto_exchange",
    },
    "healthcare": {
        "category": "application",
        "product": "healthcare_system",
    },
    "government": {
        "category": "application",
        "product": "government_portal",
    },
    "telecom": {
        "category": "application",
        "product": "telecom_platform",
    },
}


def flame_pipeline() -> ProcessingPipeline:
    """Create a processing pipeline that maps FLAME logsource products to generic categories.

    Returns a ``ProcessingPipeline`` whose items rewrite the ``logsource`` block of
    each Sigma rule so that domain-specific FLAME products (``banking``,
    ``ecommerce``, etc.) are translated into the generic ``application`` category
    with a descriptive product name.  This allows standard pySigma backends to
    convert the rules without choking on unknown product values.
    """
    items: list[ProcessingItem] = []
    for flame_product, mapping in FLAME_PRODUCT_MAP.items():
        items.append(
            ProcessingItem(
                identifier=f"flame_{flame_product}_logsource",
                transformation=ChangeLogsourceTransformation(
                    category=mapping["category"],
                    product=mapping["product"],
                ),
                rule_conditions=[
                    LogsourceCondition(product=flame_product),
                ],
            )
        )
    return ProcessingPipeline(
        items=items,
        name="FLAME Fraud Logsource Pipeline",
    )
