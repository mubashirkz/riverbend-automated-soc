
import os
import requests


OPENCTI_URL = os.getenv("OPENCTI_URL")
OPENCTI_API_KEY = os.getenv("OPENCTI_API_KEY")

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
            mapping[technique_name.lower()] = technique_id

    return mapping


TECHNIQUE_BY_NAME_QUERY = """
query GetTechniqueByName($filters: FilterGroup) {
    attackPatterns(filters: $filters, first: 1) {
        edges {
            node {
                name
                x_mitre_id
            }
        }
    }
}
"""


def get_technique_by_name(technique_name):
    """Fetch a MITRE ATT&CK technique ID by name from OpenCTI."""

    if not technique_name or not technique_name.strip():
        raise ValueError("Technique name cannot be empty.")

    if not OPENCTI_URL or not OPENCTI_API_KEY:
        raise ValueError("OpenCTI URL and API key are required.")

    filters = {
        "mode": "and",
        "filters": [
            {
                "key": "name",
                "values": [technique_name.strip()],
                "operator": "eq",
                "mode": "or"
            }
        ],
        "filterGroups": []
    }

    response = requests.post(
        f"{OPENCTI_URL.rstrip('/')}/graphql",
        json={
            "query": TECHNIQUE_BY_NAME_QUERY,
            "variables": {"filters": filters}
        },
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

    edges = result["data"]["attackPatterns"]["edges"]

    if not edges:
        return None

    return edges[0]["node"].get("x_mitre_id")
