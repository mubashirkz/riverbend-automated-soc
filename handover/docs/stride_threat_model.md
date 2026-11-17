# STRIDE Threat Model
## Automated SOC for Riverbend Microfinance Cooperative

**Prepared by:** Mubashir Ahmad  
**Date:** 25 October 2026  
**Project:** Automated SOC  
**Task:** 1 – Design SOC Architecture and Threat Model

## 1. Purpose

This document identifies possible security threats affecting Riverbend's proposed SOC logging pipeline. It uses the STRIDE method to explain threats and recommend protections.

The architecture includes log sources, Elastic Agent, Elasticsearch, Elastic Security, a Python enrichment service, StackStorm, GitHub Issues, Slack, and Grafana.

## 2. Threat Model

| STRIDE Category | Component | Possible Threat | Recommended Protection | MITRE ATT&CK Mapping |
|---|---|---|---|---|
| Spoofing | Log sources and Elastic Agent | An attacker sends fake logs or pretends to be a trusted source. | Authenticate log sources and use secure connections. | T1078 – Valid Accounts |
| Tampering | Log collection and Elasticsearch | An attacker modifies or deletes security logs. | Restrict write access and protect logs from unauthorized changes. | T1565.001 – Stored Data Manipulation |
| Repudiation | SOC alerts and response records | A user denies an action because audit evidence is missing. | Keep timestamped audit logs and record response actions. | T1070 – Indicator Removal |
| Information Disclosure | Elasticsearch and Grafana | Unauthorized users access sensitive logs or dashboards. | Apply role-based access control and encryption. | T1552 – Unsecured Credentials |
| Denial of Service | Log pipeline and monitoring services | Excessive events overload the system and delay detection. | Apply resource limits, monitor capacity, and alert on service failures. | T1499 – Endpoint Denial of Service |
| Elevation of Privilege | StackStorm and service accounts | An attacker gains excessive permissions and triggers unauthorized actions. | Use least privilege, protect credentials, and require approval for high-impact actions. | T1068 – Exploitation for Privilege Escalation |

**Note:** These are possible threats and candidate ATT&CK mappings. The mappings describe related attacker behaviors and should be validated against the specific scenario during implementation.

## 3. Main Security Controls

1. Use encrypted connections for log transmission.
2. Restrict access to logs, dashboards, and automation tools.
3. Store credentials securely and rotate them when necessary.
4. Keep audit records of alerts and automated actions.
5. Monitor log ingestion failures and unusual event volumes.
6. Require human approval for high-impact response actions.
7. Test security rules to reduce false positives.

## 4. Conclusion

The STRIDE assessment identifies possible threats to Riverbend's proposed SOC, including fake log sources, log tampering, unauthorized access, service disruption, and excessive permissions.

Authentication, access control, audit logging, encryption, and careful automation can reduce these risks.

This threat model is a starting point and should be reviewed as the SOC is implemented and tested.

## 5. SOC Architecture Components and MITRE ATT&CK Mapping

| SOC Component | Relevant ATT&CK Tactic | Example Technique | Why It Matters |
|---|---|---|---|
| Log Sources | Initial Access | T1190 – Exploit Public-Facing Application | Detect possible attacks against the web portal. |
| Log Collection | Defense Evasion | T1562.001 – Disable or Modify Tools | Detect attempts to interfere with security monitoring tools. |
| Log Storage | Defense Evasion | T1565.001 – Stored Data Manipulation | Identify possible unauthorized changes to stored security data. |
| Detection and Security Monitoring | Credential Access | T1110 – Brute Force | Detect repeated attempts to guess user passwords. |
| Python Alert Enrichment | Discovery | T1087 – Account Discovery | Add context when alerts involve account-discovery activity. |
| StackStorm SOAR | Impact | T1499 – Endpoint Denial of Service | Support investigation and response to possible service-disruption attacks. |
| Grafana Dashboard | Exfiltration | T1041 – Exfiltration Over C2 Channel | Monitor relevant alerts that may indicate data theft. |

**Important:** These are proposed detection and monitoring mappings, not proof that each component directly detects the listed technique. Actual detection depends on available logs, configured rules, and testing.

---

**Prepared by:** Mubashir Ahmad  
**Date:** 25 October 2026