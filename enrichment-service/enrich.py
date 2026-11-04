
import os

import requests
from elasticsearch import Elasticsearch


# ==========================================
# 1. Configuration
# ==========================================

OPENCTI_URL = os.getenv("OPENCTI_URL")
OPENCTI_API_KEY = os.getenv("OPENCTI_API_KEY")

ELASTICSEARCH_URL = os.getenv(
    "ELASTICSEARCH_URL",
    "http://localhost:9200"
)

SOURCE_INDEX = "riverbend-alerts"
ENRICHED_INDEX = "riverbend-alerts-enriched"


# ==========================================
# 2. OpenCTI GraphQL Query
# ==========================================

GRAPHQL_QUERY = """
query {
    attackPatterns(first: 1000) {
        edges {
            node {
                name
                x_mitre_id
                externalReferences {
                    edges {
                        node {
                            source_name
                            external_id
                        }
                    }
                }
            }
        }
    }
}
"""


# ==========================================
# 3. OpenCTI Functions
# ==========================================

def fetch_attack_patterns():
    """Retrieve MITRE ATT&CK patterns from OpenCTI."""

    if not OPENCTI_URL or not OPENCTI_API_KEY:
        raise ValueError("OpenCTI URL and API key are required.")

    response = requests.post(
        f"{OPENCTI_URL.rstrip('/')}/graphql",
        json={"query": GRAPHQL_QUERY},
        headers={
            "Authorization": f"Bearer {OPENCTI_API_KEY}",
            "Content-Type": "application/json"
        },
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        raise RuntimeError(f"OpenCTI API error: {result['errors']}")

    return result["data"]["attackPatterns"]["edges"]


def build_technique_mapping(attack_patterns):
    """Build a mapping between technique names and MITRE IDs."""

    mapping = {}

    for item in attack_patterns:
        pattern = item["node"]

        technique_id = pattern.get("x_mitre_id")
        technique_name = pattern.get("name")

        if technique_id and technique_name:
            mapping[technique_name.strip().lower()] = technique_id

    return mapping


# ==========================================
# 4. Alert Enrichment
# ==========================================

def enrich_alert(alert, technique_mapping):
    """Add MITRE ATT&CK information to an alert."""

    technique_name = alert.get("technique_name")

    if not technique_name:
        return alert

    technique_id = technique_mapping.get(
        technique_name.strip().lower()
    )

    enriched_alert = alert.copy()

    enriched_alert["mitre"] = {
        "technique_name": technique_name,
        "technique_id": technique_id
    }

    return enriched_alert


# ==========================================
# 5. Elasticsearch Connection
# ==========================================

def create_elasticsearch_client():
    """Create an Elasticsearch client."""

    return Elasticsearch(ELASTICSEARCH_URL)


# ==========================================
# 6. Elasticsearch Alert Processing
# ==========================================


def process_alerts(technique_mapping=None):
    """Read, enrich, and store alerts in Elasticsearch."""

    # Use the supplied mapping for a demo,
    # otherwise fetch ATT&CK data from OpenCTI.
    if technique_mapping is None:
        attack_patterns = fetch_attack_patterns()
        technique_mapping = build_technique_mapping(
            attack_patterns
        )
    else:
        technique_mapping = {
            name.strip().lower(): technique_id
            for name, technique_id in technique_mapping.items()
        }

    client = create_elasticsearch_client()

    response = client.search(
        index=SOURCE_INDEX,
        query={"match_all": {}},
        size=1000
    )

    alerts = response["hits"]["hits"]
    processed_count = 0

    for hit in alerts:
        alert = hit["_source"]

        enriched_alert = enrich_alert(
            alert,
            technique_mapping
        )

        client.index(
            index=ENRICHED_INDEX,
            id=hit["_id"],
            document=enriched_alert
        )

        processed_count += 1

    return processed_count


# ==========================================
# 7. Service Entry Point
# ==========================================

if __name__ == "__main__":
    count = process_alerts()

    print(f"Successfully processed {count} alerts.")
