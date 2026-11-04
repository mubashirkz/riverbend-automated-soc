# Project 4: Automated SOC for Riverbend Microfinance Cooperative

**Prepared by:** Mubashir Ahmad

## Project Overview

This project proposes and implements an automated Security Operations Center (SOC) for Riverbend Microfinance Cooperative. Its goal is to improve security monitoring, identify suspicious activity, enrich alerts, automate incident response, and display security metrics.

## Task 1: Design SOC Architecture and Threat Model

**Status:** Architecture and threat model documentation prepared.

### Deliverables

1. **SOC Architecture Diagram**
   - [View Architecture Diagram (PNG)](Diagrams/riverbend_soc_architecture.png)
   - [Edit Architecture Diagram](Diagrams/riverbend_soc_architecture.drawio)

2. **Architecture Decision Log**
   - [View Architecture Decision Log](docs/architecture_decision_log.md)

3. **STRIDE Threat Model**
   - [View STRIDE Threat Model](docs/stride_threat_model.md)

The architecture shows the proposed flow from log sources through collection, storage, security detection, alert enrichment, automated response, and reporting.

## Planned Technology Stack

- Elastic Agent and Elasticsearch
- Elastic Security / Kibana
- Sigma detection rules
- Python alert enrichment
- MITRE ATT&CK mapping
- StackStorm SOAR
- GitHub Issues and Slack notifications
- Grafana dashboards and weekly PDF reporting
- GitHub Actions for detection-rule validation

## Task 2: Automated Sigma Rule Testing

![Sigma Rule Testing](https://github.com/mubashirkz/riverbend-automated-soc/actions/workflows/sigma-test.yml/badge.svg)

This project uses GitHub Actions to validate Sigma detection rules, generate Elasticsearch SIEM rule JSON files, validate the generated JSON, and test the rules against sample security logs.

### Run tests locally

Install the dependencies:

```bash
python -m pip install sigma-cli PyYAML
sigma plugin install elasticsearch
```

Validate the Sigma rules:

```bash
sigma check sigma
```

Generate the detection JSON files:

```bash
sigma convert -t lucene -p ecs_windows -f siem_rule -o detections/suspicious_powershell.json sigma/suspicious_powershell.yml

sigma convert -t lucene -p ecs_windows -f siem_rule -o detections/powershell_network_connection.json sigma/powershell_network_connection.yml
```

Run the sample-log detection tests:

```bash
python sample-logs/test_detections.py
```

Sample events are synthetic Sysmon-style JSON Lines records created for testing. They are not collected from a real system.

## Task 3: Alert Enrichment Service

This Python service reads alerts from the `riverbend-alerts` Elasticsearch index, retrieves MITRE ATT&CK technique mappings through the OpenCTI GraphQL API, and writes enriched alerts to `riverbend-alerts-enriched`.

### Features

- Retrieves alerts from Elasticsearch.
- Retrieves ATT&CK technique information through OpenCTI.
- Maps technique names to MITRE ATT&CK IDs.
- Adds a `mitre` object containing the technique name and technique ID.
- Writes enriched alerts to a separate Elasticsearch index.
- Includes pytest unit tests with mocked API responses and Elasticsearch operations.
- Includes a Dockerfile for containerized deployment.
- Includes a local demo that uses a static MITRE mapping.

### Project files

```text
enrichment-service/
├── enrich.py
├── demo_enrichment.py
├── requirements.txt
├── Dockerfile
└── tests/
    └── test_enrich.py
```

### Configuration for production mode

Set these environment variables before running the production service:

- `OPENCTI_URL` — Your OpenCTI instance URL.
- `OPENCTI_API_KEY` — Your OpenCTI API token.
- `ELASTICSEARCH_URL` — Your Elasticsearch URL.

For local execution, use:

```text
ELASTICSEARCH_URL=http://localhost:9200
```

For a container connected to `riverbend-network`, use:

```text
ELASTICSEARCH_URL=http://riverbend-elasticsearch:9200
```

The source index is `riverbend-alerts`, and the output index is `riverbend-alerts-enriched`.

Do not commit real API keys or secrets to GitHub.

### Install dependencies and run unit tests

From the repository root:

```bash
python -m pip install -r enrichment-service/requirements.txt
python -m pytest -v
```

The unit tests mock the OpenCTI HTTP response and Elasticsearch operations. They do not require a live OpenCTI instance.

### Run the local enrichment demo

The demo uses a static mapping:

```python
{
    "Valid Accounts": "T1078"
}
```

It reuses the enrichment logic in `enrich.py` and writes the enriched alert to the real local Elasticsearch instance. It does not require OpenCTI credentials.

Make sure Elasticsearch is running and that the `riverbend-alerts` index contains a sample alert.

From the `enrichment-service` directory, run:

```bash
python demo_enrichment.py
```

Expected output:

```text
Starting MITRE ATT&CK enrichment demo...
Successfully enriched 1 alerts.
Output index: riverbend-alerts-enriched
```

### Build the Docker image

From the `enrichment-service` directory:

```bash
docker build -t riverbend-enrichment-service .
```

### Run the production Docker container

The production container requires valid OpenCTI credentials and an Elasticsearch container accessible through the Docker network.

Create a `.env` file in the repository root:

```text
OPENCTI_URL=https://your-opencti-instance
OPENCTI_API_KEY=your-opencti-api-key
ELASTICSEARCH_URL=http://riverbend-elasticsearch:9200
```

Replace the example OpenCTI values with your actual configuration. Do not commit this file.

From the `enrichment-service` directory, run:

```bash
docker run --rm --network riverbend-network --env-file ../.env riverbend-enrichment-service
```

### Verify enriched alerts

Check the source alerts:

```bash
curl.exe "http://localhost:9200/riverbend-alerts/_search?pretty"
```

Check the enriched alerts:

```bash
curl.exe "http://localhost:9200/riverbend-alerts-enriched/_search?pretty"
```

An enriched alert should contain a `mitre` object similar to:

```json
"mitre": {
  "technique_name": "Valid Accounts",
  "technique_id": "T1078"
}
```

### Testing and demonstration results

- Five pytest unit tests passed.
- Sigma sample-log detection tests passed.
- Docker image built successfully.
- Docker-to-Elasticsearch connectivity was verified.
- The local demo successfully processed a sample alert and wrote the enriched document to Elasticsearch.

**Important:** The local demo uses a static mapping to demonstrate the enrichment and Elasticsearch write process. The production service uses the OpenCTI GraphQL API to retrieve technique mappings.

## Security Note

This project is a proof of concept. Synthetic logs should be used during development. Production deployment requires appropriate access controls, secure API-key handling, data protection, and security testing.