
import json
from datetime import datetime, timezone
from pathlib import Path
import uuid

OUTPUT_FILE = Path(__file__).parent / "sample-events.jsonl"


def generate_events():
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )[:-3] + "Z"

    computer = "WORKSTATION-01"
    user = "LAB\\m.ahmad"

    events = [
        {
            "EventID": 1,
            "UtcTime": timestamp,
            "Computer": computer,
            "ProcessGuid": "{" + str(uuid.uuid4()) + "}",
            "ProcessId": 4100,
            "Image": "C:\\Windows\\System32\\notepad.exe",
            "CommandLine": "notepad.exe",
            "User": user,
            "ParentImage": "C:\\Windows\\explorer.exe"
        },
        {
            "EventID": 1,
            "UtcTime": timestamp,
            "Computer": computer,
            "ProcessGuid": "{" + str(uuid.uuid4()) + "}",
            "ProcessId": 4200,
            "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "CommandLine": "powershell.exe -EncodedCommand EXAMPLE",
            "User": user,
            "ParentImage": "C:\\Windows\\System32\\cmd.exe"
        },
        {
            "EventID": 3,
            "UtcTime": timestamp,
            "Computer": computer,
            "ProcessGuid": "{" + str(uuid.uuid4()) + "}",
            "ProcessId": 4200,
            "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "User": user,
            "Protocol": "tcp",
            "Initiated": "true",
            "SourceIp": "192.0.2.10",
            "SourcePort": 51000,
            "DestinationIp": "198.51.100.20",
            "DestinationPort": 443
        }
    ]

    return events


def main():
    events = generate_events()

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} Sysmon-style events: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
