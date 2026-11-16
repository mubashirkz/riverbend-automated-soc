import requests

from st2common.runners.base_action import Action


class SendSlackNotificationAction(Action):

    def run(self, alert, issue_url, slack_webhook, dry_run=False):
        """Send or simulate a high-severity SOC notification."""

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

        if dry_run:
            self.logger.info("DRY RUN: Slack notification was not sent.")
            self.logger.info("Mock Slack payload: %s", message)

            return {
                "status": "mocked",
                "issue_url": issue_url,
                "dry_run": True
            }

        if not slack_webhook:
            raise ValueError("Slack webhook is missing.")

        response = requests.post(
            slack_webhook,
            json=message,
            timeout=30
        )

        response.raise_for_status()

        self.logger.info("Slack notification sent successfully.")

        return {
            "status": "sent",
            "issue_url": issue_url,
            "dry_run": False
        }
