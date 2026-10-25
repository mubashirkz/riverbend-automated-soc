# Architecture Decision Log
## Automated SOC for Riverbend Microfinance Cooperative

**Prepared by:** Mubashir Ahmad  
**Date:** 25 October 2026  
**Project:** Automated SOC  
**Task:** 1 – Design SOC Architecture and Threat Model  
**Status:** Proposed Architecture

---

## 1. Project Overview

Riverbend Microfinance Cooperative provides financial services to approximately 40,000 borrowers through a web portal and Android application.

The company needs an automated Security Operations Center (SOC) to monitor security events, detect suspicious activities, and support incident response.

The proposed SOC should be affordable, reliable, secure, and easy for the company's four developers to maintain.

## 2. Decision 1: Elastic Stack vs OpenSearch

### Option A: Elastic Stack

**Advantages:**
- Provides Elasticsearch for storing and searching logs.
- Uses Kibana for visualizing security events.
- Supports security detection and alerting.
- Has extensive documentation and community resources.
- Integrates with other security tools.

**Disadvantages:**
- Some advanced security features require paid licenses.
- Cloud hosting can become expensive as log volume increases.
- Requires careful configuration and maintenance.

### Option B: OpenSearch

**Advantages:**
- Open-source search and analytics platform.
- Includes OpenSearch Dashboards.
- Provides security analytics and alerting capabilities.
- Offers flexibility for self-hosted deployments.
- Has an active open-source community.

**Disadvantages:**
- Requires infrastructure management when self-hosted.
- Some integrations may require additional configuration.
- Our team has less practical experience with OpenSearch.

### Decision

**Selected: Elastic Stack**

Elastic Stack is our preferred solution because it provides log management, security monitoring, and detection capabilities.

It was also used in previous SOC projects, reducing the learning curve.

**Trade-off:** We accept possible licensing and hosting limitations in exchange for familiar tools and established security features.

## 3. Decision 2: On-Premises vs Free Cloud Hosting

### Option A: On-Premises

**Advantages:**
- Greater control over infrastructure.
- Direct control over log storage.
- Can operate without depending entirely on an external cloud provider.

**Disadvantages:**
- Requires servers and maintenance.
- Hardware and electricity increase costs.
- Backups and availability must be managed internally.

### Option B: Free Cloud Hosting

**Advantages:**
- Useful for proof-of-concept testing.
- Reduces initial infrastructure requirements.
- Can provide convenient remote access.
- Simplifies some deployment activities.

**Disadvantages:**
- Free plans may have limited storage and computing resources.
- Services may impose usage limits or expire.
- Sensitive financial information requires appropriate data protection controls.

### Decision

**Selected: Free Cloud Hosting for the Proof of Concept**

We propose using an eligible free-tier or trial cloud environment for testing, subject to verifying its current limits and availability.

Only synthetic security logs will be used during development.

**Trade-off:** Cloud hosting reduces initial setup effort but introduces provider dependencies, resource limits, and potential future costs.

Production deployment will require a separate security, privacy, and cost assessment.

## 4. Decision 3: Manual Monitoring vs Automated SOC

### Option A: Manual Monitoring

**Advantages:**
- Simple initial setup.
- Analysts can investigate alerts individually.
- Human judgment remains part of every response.

**Disadvantages:**
- Requires continuous staff attention.
- Security alerts may be missed.
- Response times can be slower.

### Option B: Automated SOC

**Advantages:**
- Collects and processes logs automatically.
- Detects suspicious events using security rules.
- Enriches alerts with MITRE ATT&CK information.
- Uses SOAR workflows to notify responsible staff.
- Reduces repetitive manual work.

**Disadvantages:**
- Requires additional configuration.
- Incorrect detection rules can generate false positives.
- Automated actions must be carefully controlled.

### Decision

**Selected: Automated SOC with Human Approval for High-Impact Actions**

The proposed architecture will use Sigma detection rules, Python alert enrichment, StackStorm automation, and Grafana dashboards.

High-impact response actions will require human approval.

**Trade-off:** Automation improves monitoring efficiency but increases implementation complexity.

## 5. Proposed Technology Stack

| Component | Selected Technology | Purpose |
|---|---|---|
| Log Collection | Elastic Agent | Collect security logs |
| Log Storage | Elasticsearch | Store and search logs |
| Security Monitoring | Kibana / Elastic Security | Investigate security events |
| Detection Rules | Sigma | Define portable detection logic |
| Alert Enrichment | Python | Add security context and MITRE tags |
| SOAR | StackStorm | Automate response workflows |
| Notifications | Slack | Notify developers about incidents |
| Incident Tracking | GitHub Issues | Record and track incidents |
| Metrics Dashboard | Grafana | Display SOC performance metrics |
| CI/CD | GitHub Actions | Validate and test detection rules |

## 6. Security Considerations

The proposed SOC architecture should include:

- Encryption for log transmission.
- Role-based access control.
- Secure storage of API keys and credentials.
- Monitoring of unauthorized access attempts.
- Protection against log tampering.
- Restricted access to sensitive financial information.
- Audit logs for automated response activities.
- Human approval for high-impact response actions.

## 7. Conclusion

Elastic Stack is the preferred monitoring platform for Riverbend's proposed SOC.

The initial proof of concept will use synthetic logs and a low-cost cloud environment where suitable.

Automation will help Riverbend identify security incidents, improve visibility, and reduce repetitive monitoring work.

These decisions are preliminary and will be reviewed during implementation and testing.

---

**Prepared by:** Mubashir Ahmad  
**Date:** 25 October 2026  
**Document:** Architecture Decision Log – Task 1