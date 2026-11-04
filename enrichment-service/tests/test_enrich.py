
import sys

from pathlib import Path
from unittest.mock import patch, Mock

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import enrich


def test_fetch_attack_patterns():
    mock_response = Mock()

    mock_response.json.return_value = {
        "data": {
            "attackPatterns": {
                "edges": [
                    {
                        "node": {
                            "name": "Valid Accounts",
                            "x_mitre_id": "T1078"
                        }
                    }
                ]
            }
        }
    }

    mock_response.raise_for_status.return_value = None

    with patch("enrich.requests.post", return_value=mock_response) as mock_post:
        with patch.object(enrich, "OPENCTI_URL", "https://example.com"):
            with patch.object(enrich, "OPENCTI_API_KEY", "test-token"):

                result = enrich.fetch_attack_patterns()

    assert result[0]["node"]["name"] == "Valid Accounts"
    assert result[0]["node"]["x_mitre_id"] == "T1078"

    mock_post.assert_called_once()


def test_build_technique_mapping():
    attack_patterns = [
        {
            "node": {
                "name": "Valid Accounts",
                "x_mitre_id": "T1078"
            }
        },
        {
            "node": {
                "name": "Phishing",
                "x_mitre_id": "T1566"
            }
        }
    ]

    result = enrich.build_technique_mapping(attack_patterns)

    assert result["valid accounts"] == "T1078"
    assert result["phishing"] == "T1566"


def test_enrich_alert():
    alert = {
        "alert_id": "ALERT-001",
        "technique_name": "Valid Accounts",
        "severity": "High"
    }

    technique_mapping = {
        "valid accounts": "T1078"
    }

    result = enrich.enrich_alert(alert, technique_mapping)

    assert result["mitre"]["technique_id"] == "T1078"
    assert result["mitre"]["technique_name"] == "Valid Accounts"
    assert result["severity"] == "High"
    assert "mitre" not in alert


def test_enrich_alert_without_technique():
    alert = {
        "alert_id": "ALERT-002",
        "severity": "Medium"
    }

    result = enrich.enrich_alert(alert, {})

    assert result == alert


def test_process_alerts():
    sample_alert = {
        "alert_id": "ALERT-001",
        "technique_name": "Valid Accounts",
        "severity": "High"
    }

    mock_hits = [
        {
            "_id": "alert-001",
            "_source": sample_alert
        }
    ]

    mock_client = Mock()

    mock_client.search.return_value = {
        "hits": {
            "hits": mock_hits
        }
    }

    attack_patterns = [
        {
            "node": {
                "name": "Valid Accounts",
                "x_mitre_id": "T1078"
            }
        }
    ]

    with patch.object(
        enrich,
        "fetch_attack_patterns",
        return_value=attack_patterns
    ):
        with patch.object(
            enrich,
            "create_elasticsearch_client",
            return_value=mock_client
        ):
            result = enrich.process_alerts()

    expected = {
        **sample_alert,
        "mitre": {
            "technique_name": "Valid Accounts",
            "technique_id": "T1078"
        }
    }

    assert result == 1

    mock_client.search.assert_called_once_with(
        index=enrich.SOURCE_INDEX,
        query={"match_all": {}},
        size=1000
    )

    mock_client.index.assert_called_once_with(
        index=enrich.ENRICHED_INDEX,
        id="alert-001",
        document=expected
    )
