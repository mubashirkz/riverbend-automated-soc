
from enrich import process_alerts


# Static MITRE ATT&CK mapping for demonstration.
DEMO_TECHNIQUE_MAPPING = {
    "Valid Accounts": "T1078"
}


def main():
    """Run the enrichment service using a static MITRE mapping."""

    print("Starting MITRE ATT&CK enrichment demo...")

    processed_count = process_alerts(
        technique_mapping=DEMO_TECHNIQUE_MAPPING
    )

    print(f"Successfully enriched {processed_count} alerts.")
    print("Output index: riverbend-alerts-enriched")


if __name__ == "__main__":
    main()
