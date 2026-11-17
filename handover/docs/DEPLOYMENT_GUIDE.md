# Riverbend Microfinance Cooperative — SOC Deployment Guide

## 1. Project Overview

This handover package contains the deliverables from the Riverbend Automated SOC project:

- SOC architecture diagram and STRIDE threat model.
- Sigma detection rules and CI validation workflow.
- Python alert enrichment service with MITRE ATT&CK mapping.
- StackStorm SOAR pack for GitHub issue creation and Slack notification.
- Grafana dashboard configuration and weekly PDF reporting.
- Sample security logs, test scripts, and supporting documentation.

The project is a proof of concept using synthetic security events. It is not a production-ready security monitoring environment.

## 2. Prerequisites

Install the following before attempting deployment:

- Docker Desktop with Docker Compose.
- Python 3.12.
- Git.
- A GitHub account for CI and issue integration.
- A Slack workspace if testing notifications.
- Grafana access for dashboard and report generation.

Verify Docker:

    docker --version
    docker compose version

Verify Python:

    python --version

## 3. Package Structure

- `Diagrams/` — architecture diagrams.
- `docs/` — architecture decisions and STRIDE threat model.
- `ci/` — CI workflow reference files.
- `sigma/` — Sigma detection rules.
- `sample-logs/` — synthetic events and test scripts.
- `detections/` — generated detection output.
- `enrichment-service/` — alert enrichment application and tests.
- `stackstorm/` — StackStorm pack and deployment configuration.
- `reports/` — report generator, sample PDFs, and dashboard images.
- `screenshots/` — dashboard evidence.
- `dashboard.json` — Grafana dashboard export.
- `docker-compose.yml` — Elasticsearch, Grafana, and image renderer configuration.


## 4. Deploy the Monitoring Stack

The main Docker Compose file starts Elasticsearch, Grafana, and the Grafana image renderer. It does not start Kibana, StackStorm, or the enrichment service.

### 4.1 Configure environment variables

From the project root, create a local `.env` file. Do not commit this file or include it in the handover ZIP.

Set these required values:

- `GRAFANA_ADMIN_PASSWORD` — a strong Grafana administrator password.
- `RENDERER_AUTH_TOKEN` — a separate long random token for the image renderer.

Do not use example passwords or share these values publicly.

### 4.2 Create the Docker network

    docker network create riverbend-network

If the network already exists, Docker may report that it exists; you can continue.

### 4.3 Start the monitoring services

From the project root, run:

    docker compose -f handover/docker-compose.yml config --quiet
    docker compose -f handover/docker-compose.yml up -d

Check service status:

    docker compose -f handover/docker-compose.yml ps

### 4.4 Access the local services

- Elasticsearch: `http://localhost:9200`
- Grafana: `http://localhost:3000`

Sign in to Grafana using the administrator credentials configured in `.env`.

Import `handover/dashboard.json` into Grafana and configure an Elasticsearch data source that matches the dashboard's expected index and field configuration.

**Security warning:** The supplied Elasticsearch configuration disables Elasticsearch security. Keep this stack on a trusted local environment. Do not expose these ports directly to the public internet.


## 5. Sigma Detection and CI Validation

The project includes two Sigma rules:

- `suspicious_powershell.yml`
- `powershell_network_connection.yml`

Sample Windows security events are provided in `sample-logs/sample-events.jsonl`.

### 5.1 Run local sample tests

From the project root:

    python sample-logs/test_detections.py

Review the generated detection files in `detections/`.

### 5.2 Validate Sigma rules

Install the Sigma CLI and the required Elasticsearch backend plugin according to the Sigma CLI documentation.

The GitHub Actions workflow is located at `.github/workflows/sigma-test.yml`. The handover copy is in `handover/ci/sigma-test.yml`.

In the GitHub repository, open the Actions tab and check the Sigma validation workflow. A successful run should show that the rules pass validation and produce the expected detection output.

### 5.3 Weekly report workflow

The weekly report workflow is `.github/workflows/weekly-soc-report.yml`. The handover copy is in `handover/ci/weekly-soc-report.yml`.

It runs on Sundays at 02:17 UTC and can also be started manually using GitHub Actions.

Configure these GitHub repository Actions secrets:

- `GRAFANA_URL` — the reachable Grafana base URL.
- `GRAFANA_TOKEN` — a Grafana service account token with the required dashboard access.

The workflow installs `requests` and `reportlab`, runs the report generator, and uploads the generated PDF as a workflow artifact.

When deploying this package into another repository, place the workflow YAML files in `.github/workflows/` so GitHub Actions can discover them.


## 6. Alert Enrichment Service

The Python enrichment service maps alert technique names to MITRE ATT&CK technique IDs and writes enriched alerts to Elasticsearch.

### 6.1 Configuration

The service reads these environment variables:

- `OPENCTI_URL` — OpenCTI instance URL.
- `OPENCTI_API_KEY` — OpenCTI API key.
- `ELASTICSEARCH_URL` — Elasticsearch URL; defaults to `http://localhost:9200`.

Keep API keys in environment variables or a secure secrets manager. Never commit them to Git.

### 6.2 Install dependencies

From the project root:

    cd handover/enrichment-service
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

### 6.3 Run unit tests

    python -m pytest tests -v

The tests use mocks and do not require a live OpenCTI connection.

### 6.4 Run the service

The Dockerfile builds the enrichment application:

    docker build -t riverbend-enrichment .

The service needs access to Elasticsearch and OpenCTI. Configure the three environment variables before running it. When Elasticsearch runs in the supplied Docker network, use `http://riverbend-elasticsearch:9200` as its URL from a container on that network.

The source index is `riverbend-alerts`; enriched alerts are written to `riverbend-alerts-enriched`.

The `demo_enrichment.py` file demonstrates enrichment using a local technique mapping. It is a demonstration, not a substitute for a live OpenCTI integration.


## 7. StackStorm SOAR Integration

The Riverbend StackStorm pack is located in `handover/stackstorm/packs/riverbend/`.

It contains:

- A high-severity alert rule and sensor.
- A GitHub issue creation action.
- A Slack notification action.
- An Orquesta workflow that passes the GitHub issue URL to the Slack action.

### 7.1 Authentication setup

The StackStorm Compose configuration is a deployment template. It requires fresh local authentication files before startup.

Read `handover/stackstorm/AUTHENTICATION_SETUP.md` and prepare the required `htpasswd` and `st2-cli.conf` files using the StackStorm deployment documentation.

Do not copy personal authentication files, API keys, encrypted datastore keys, or passwords into the handover package or Git repository.

### 7.2 Configure integration secrets

Store the GitHub token and Slack webhook securely in the StackStorm encrypted datastore. The action metadata expects these keys:

- `github_token`
- `slack_webhook`

Use a GitHub token restricted to the intended test repository and the minimum required permissions. Use a dedicated Slack incoming webhook for the test channel.

Never paste tokens or webhook URLs into source files or commit them to Git.

### 7.3 Register and inspect the pack

After configuring StackStorm and starting its services, register the pack and inspect the workflow:

    st2ctl reload --register-all
    st2 workflow inspect --action riverbend.create_issue_and_notify

The workflow should report no definition errors.

### 7.4 Safe testing

The committed workflow uses `dry_run: true` for both actions. Keep this as the default.

For a controlled live verification, change both workflow task inputs to `dry_run: false`, register the updated pack, and run it with a synthetic alert. Verify that the GitHub issue and Slack notification are correct.

Immediately restore `dry_run: true` and register the pack again after the test.

The test GitHub repository is `mubashirkz/riverbend-soar-test`. Do not use real customer information or production alerts in this demonstration.


## 8. Dashboard and SOC Reporting

The Grafana dashboard export is `handover/dashboard.json`.

It contains four SOC metric panels:

1. Alert Volume
2. Mean Time to Detect (MTTD)
3. Mean Time to Respond (MTTR)
4. False Positive Rate

### 8.1 Import the dashboard

1. Open Grafana.
2. Navigate to Dashboards.
3. Select Import.
4. Upload `handover/dashboard.json`.
5. Select or configure the appropriate Elasticsearch data source.
6. Review the panels and confirm that the expected data is available.

The dashboard and reports use synthetic project data. Metrics should not be interpreted as measurements from a live production SOC.

### 8.2 Generate a PDF report

Install the report generator dependencies:

    python -m pip install requests reportlab

Configure:

- `GRAFANA_URL` — Grafana base URL.
- `GRAFANA_TOKEN` — Grafana service account token.

Run the report generator from the project root:

    python generate_report.py

The generated PDF is saved in the root `reports/` directory. The handover package includes sample reports and dashboard panel images for reference.


## 9. Deployment Limitations

This package is a proof of concept, not a complete production deployment.

- The main Compose file starts Elasticsearch, Grafana, and the image renderer only.
- Kibana is not included in the supplied main Compose file.
- StackStorm uses a separate Compose configuration and requires local authentication setup.
- The enrichment service requires reachable OpenCTI and Elasticsearch instances.
- The Grafana dashboard requires a correctly configured data source.
- The public Render free tier is not suitable for hosting this entire persistent SOC stack reliably. Elasticsearch requires persistent storage, and free services have resource and availability limitations.

Do not claim that the complete stack is publicly deployed unless every component has actually been deployed and verified.

## 10. Security Checklist

Before sharing or deploying the package:

- [ ] Keep `.env` files out of Git and the ZIP.
- [ ] Do not include GitHub tokens, Slack webhook URLs, or API keys.
- [ ] Do not include StackStorm authentication files or datastore encryption keys.
- [ ] Keep StackStorm actions in dry-run mode by default.
- [ ] Use synthetic data for demonstrations.
- [ ] Do not expose Elasticsearch or StackStorm without appropriate authentication and network controls.
- [ ] Replace default credentials and placeholder values before deployment.
- [ ] Restrict integration tokens to the minimum required permissions.
- [ ] Review the package for secrets before publishing it.

## 11. Useful Commands

Run these commands from the project root unless otherwise specified.

Check Git status:

    git status

Validate the main Compose configuration:

    docker compose -f handover/docker-compose.yml config --quiet

Start the monitoring stack:

    docker compose -f handover/docker-compose.yml up -d

Check running containers:

    docker compose -f handover/docker-compose.yml ps

Stop the monitoring stack:

    docker compose -f handover/docker-compose.yml down

Run enrichment unit tests:

    cd handover/enrichment-service
    python -m pytest tests -v

Inspect the StackStorm workflow from a configured StackStorm client:

    st2 workflow inspect --action riverbend.create_issue_and_notify

## 12. Final Handover

The handover package brings together the architecture, detection, enrichment, SOAR, dashboard, and reporting deliverables.

Before final submission:

1. Review the files and deployment instructions.
2. Complete the security scan.
3. Record the demonstration video.
4. Include the video in `handover/demo/`.
5. Create and verify `handover_package.zip`.
6. Update the main project README with the final handover details.

