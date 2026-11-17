# StackStorm Authentication Setup

The files htpasswd and st2-cli.conf are intentionally excluded
because they contain environment-specific authentication settings.

Before starting StackStorm:
1. Generate a new htpasswd file for the deployment administrator.
2. Configure st2-cli.conf with the new StackStorm API credentials.
3. Keep both files private and never commit them to Git.
4. Configure GitHub and Slack credentials using the encrypted
   StackStorm datastore.

The supplied docker-compose.yml is a deployment template.
It requires these authentication files before startup.
