import json
import logging
import os
import urllib.request

from st2reactor.sensor.base import PollingSensor

LOGGER = logging.getLogger(__name__)


class RiverbendAlertSensor(PollingSensor):

    def __init__(self, sensor_service, config, poll_interval):
        super(RiverbendAlertSensor, self).__init__(
            sensor_service=sensor_service,
            config=config,
            poll_interval=poll_interval
        )
        self.elasticsearch_url = os.environ.get(
            "ELASTICSEARCH_URL",
            "http://riverbend-elasticsearch:9200"
        ).rstrip("/")
        self.index = "riverbend-alerts-enriched"
        self.seen_alerts = set()

    def setup(self):
        LOGGER.info("Riverbend alert sensor started")

    def poll(self):
        query = {
            "size": 100,
            "query": {
                "range": {
                    "severity_score": {"gte": 8}
                }
            }
        }

        url = self.elasticsearch_url + "/" + self.index + "/_search"
        request = urllib.request.Request(
            url,
            data=json.dumps(query).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                results = json.loads(response.read().decode("utf-8"))

            for hit in results.get("hits", {}).get("hits", []):
                alert = hit.get("_source", {})
                alert_id = str(alert.get("alert_id", hit.get("_id")))

                if alert_id in self.seen_alerts:
                    continue

                self.seen_alerts.add(alert_id)

                self.sensor_service.dispatch(
                    trigger="riverbend.high_severity_alert",
                    payload=alert,
                    trace_tag=alert_id
                )

                LOGGER.info("Dispatched alert: %s", alert_id)

        except Exception:
            LOGGER.exception("Failed to poll Elasticsearch")

    def cleanup(self):
        LOGGER.info("Riverbend alert sensor stopped")

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
