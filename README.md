## Project 4: Automated SOC for Riverbend Microfinance Cooperative

**Prepared by:** Mubashir Ahmad  
**Task 1:** Design SOC Architecture and Threat Model  
**Status:** Architecture and threat model documentation prepared

### Project Overview

This project proposes an automated Security Operations Center (SOC) for Riverbend Microfinance Cooperative. Its goal is to improve security monitoring, identify suspicious activity, enrich alerts, automate incident response, and display security metrics.

### Task 1 Deliverables

#### 1. SOC Architecture Diagram

The architecture shows the proposed flow from log sources through collection, storage, security detection, alert enrichment, automated response, and reporting.

- [View Architecture Diagram (PNG)](diagrams/riverbend_soc_architecture.png)
- [Edit Architecture Diagram](diagrams/riverbend_soc_architecture.drawio)

#### 2. Architecture Decision Log

Documents the proposed technology choices, including Elastic Stack versus OpenSearch, cloud versus on-premises hosting, and manual versus automated monitoring.

[View Architecture Decision Log](docs/architecture_decision_log.md)

#### 3. STRIDE Threat Model

Identifies potential spoofing, tampering, repudiation, information disclosure, denial-of-service, and privilege-escalation threats. It includes proposed security controls and MITRE ATT&CK mappings.

[View STRIDE Threat Model](docs/stride_threat_model.md)

### Planned Technology Stack

- Elastic Agent and Elasticsearch
- Elastic Security / Kibana
- Sigma detection rules
- Python alert enrichment
- MITRE ATT&CK mapping
- StackStorm SOAR
- GitHub Issues and Slack notifications
- Grafana dashboards and weekly PDF reporting
- GitHub Actions for detection-rule validation

### Current Scope

Task 1 focuses on architecture design, technology decisions, and threat modeling. Implementation and testing of the automation components will take place in later tasks.

### Security Note

The architecture is a proposed proof of concept. Synthetic logs should be used during development, and production deployment requires appropriate access controls, data protection, and security testing.