import json
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_DIR / "sample-logs" / "sample-events.jsonl"
SIGMA_DIR = PROJECT_DIR / "sigma"


def matches_selection(event, selection):
    for expression, expected in selection.items():
        parts = expression.split("|", 1)
        field = parts[0]
        modifier = parts[1] if len(parts) == 2 else ""

        actual = event.get(field)

        if actual is None:
            return False

        actual_text = str(actual).casefold()
        expected_text = str(expected).casefold()

        if modifier == "endswith":
            matched = actual_text.endswith(expected_text)
        elif modifier == "contains":
            matched = expected_text in actual_text
        else:
            matched = actual_text == expected_text

        if not matched:
            return False

    return True


def matches_rule(event, rule):
    detection = rule["detection"]
    condition = detection["condition"]

    # This project currently uses selection groups joined by "and".
    selections = [
        name.strip()
        for name in condition.split(" and ")
    ]

    return all(
        matches_selection(event, detection[name])
        for name in selections
    )


def main():
    with LOG_FILE.open(encoding="utf-8") as file:
        events = [json.loads(line) for line in file if line.strip()]

    expected_matches = {
        "suspicious_powershell.yml": 1,
        "powershell_network_connection.yml": 1,
    }

    for filename, expected_count in expected_matches.items():
        rule_path = SIGMA_DIR / filename

        with rule_path.open(encoding="utf-8") as file:
            rule = yaml.safe_load(file)

        matches = [
            event for event in events
            if matches_rule(event, rule)
        ]

        print(f"{rule['title']}: {len(matches)} matching event(s)")

        if len(matches) != expected_count:
            raise AssertionError(
                f"{filename}: expected {expected_count} matches, "
                f"got {len(matches)}"
            )

    print("PASS: All sample-log detection tests passed.")


if __name__ == "__main__":
    main()