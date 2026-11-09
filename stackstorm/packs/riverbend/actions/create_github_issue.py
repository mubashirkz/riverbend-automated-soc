
import requests

from st2common.runners.base_action import Action


class CreateGitHubIssueAction(Action):

    def run(self, alert, github_token):
        """Create a GitHub issue for a high-severity alert."""

        if not github_token:
            raise ValueError("GitHub token is missing.")

        repository = "mubashirkz/riverbend-automated-soc"
        url = f"https://api.github.com/repos/{repository}/issues"

        technique_id = alert.get("mitre", {}).get(
            "technique_id", "Unknown"
        )

        alert_name = alert.get(
            "alert_name", "High-severity security alert"
        )

        title = f"High-severity alert – {technique_id}"

        remediation_steps = [
            "Investigate the source IP and affected account.",
            "Review authentication and PowerShell activity.",
            "Reset affected credentials if compromise is confirmed.",
            "Check for persistence or additional suspicious activity.",
            "Preserve relevant logs and document findings."
        ]

        body = f"""
## Security Alert

**Alert:** {alert_name}

**Severity:** {alert.get('severity')}
**Severity Score:** {alert.get('severity_score')}
**Source IP:** {alert.get('source_ip')}
**MITRE Technique:** {technique_id}
**Technique Name:** {alert.get('mitre', {}).get('technique_name', 'Unknown')}

### Description

{alert.get('description', 'No description available.')}

### Recommended Remediation

""" + "\n".join(
            f"- [ ] {step}" for step in remediation_steps
        )

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        response = requests.post(
            url,
            headers=headers,
            json={
                "title": title,
                "body": body
            },
            timeout=30
        )

        response.raise_for_status()

        issue = response.json()

        self.logger.info(
            "Created GitHub issue number %s",
            issue["number"]
        )

        return {
            "issue_number": issue["number"],
            "issue_url": issue["html_url"]
        }
