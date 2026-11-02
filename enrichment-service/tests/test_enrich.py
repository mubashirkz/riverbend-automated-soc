import sys

from pathlib import Path

from unittest.mock import patch, Mock

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import enrich

@patch("enrich.requests.post")
def test_get_technique_by_name(mock_post):
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
    mock_post.return_value = mock_response

    with patch.object(enrich, "OPENCTI_URL", "https://example.com"), \
            patch.object(enrich, "OPENCTI_API_KEY", "test-token"):

        result = enrich.get_technique_by_name("Valid Accounts")

    assert result == "T1078"

    mock_post.assert_called_once()

@patch("enrich.requests.post")
def test_get_technique_by_name_not_found(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "data": {
            "attackPatterns": {
                "edges": []
            }
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    with patch.object(enrich, "OPENCTI_URL", "https://example.com"), \
         patch.object(enrich, "OPENCTI_API_KEY", "test-token"):

        result = enrich.get_technique_by_name("Unknown Technique")

    assert result is None


