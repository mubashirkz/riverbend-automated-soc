import requests

from st2common.runners.base_action import Action


class SendSlackNotificationAction(Action):

    def run(self, alert, issue_url, slack_webhook):
        """Send a high-severity alert notification to Slack."""

        if not slack_webhook:
            raise ValueError("Slack webhook is missing.")

        alert_name = alert.get(
            "alert_name", "High-severity security alert"
        )

        technique_id = alert.get(
            "mitre", {}
        ).get("technique_id", "Unknown")

        message = {
            "text": (
                ":rotating_light: *HIGH-SEVERITY SOC ALERT*\n"
                f"*Alert:* {alert_name}\n"
                f"*Severity:* {alert.get('severity')}\n"
                f"*Severity Score:* {alert.get('severity_score')}\n"
                f"*Source IP:* {alert.get('source_ip')}\n"
                f"*MITRE Technique:* {technique_id}\n"
                f"*GitHub Issue:* {issue_url}"
            )
        }

        response = requests.post(
            slack_webhook,
            json=message,
            timeout=30
        )

        response.raise_for_status()

        self.logger.info("Slack notification sent successfully.")

        return {
            "status": "sent",
            "issue_url": issue_url
        }