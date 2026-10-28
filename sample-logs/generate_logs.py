
import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "sample-events.jsonl"


def generate_events():
    timestamp = datetime.now(timezone.utc).isoformat()

    events = [
        {
            "timestamp": timestamp,
            "event_id": 4624,
            "event_type": "login",
            "username": "m.ahmad",
            "source_ip": "192.168.1.25",
            "status": "success",
            "description": "Normal user login"
        },
        {
            "timestamp": timestamp,
            "event_id": 4625,
            "event_type": "login",
            "username": "administrator",
            "source_ip": "203.0.113.45",
            "status": "failed",
            "description": "Failed administrator login"
        },
        {
            "timestamp": timestamp,
            "event_id": 4625,
            "event_type": "login",
            "username": "administrator",
            "source_ip": "203.0.113.45",
            "status": "failed",
            "description": "Repeated failed administrator login"
        },
        {
            "timestamp": timestamp,
            "event_id": 4688,
            "event_type": "process_creation",
            "username": "m.ahmad",
            "source_ip": "192.168.1.25",
            "process": "powershell.exe",
            "command_line": "powershell.exe -EncodedCommand example",
            "description": "Suspicious encoded PowerShell example"
        },
        {
            "timestamp": timestamp,
            "event_id": 4624,
            "event_type": "login",
            "username": "helpdesk",
            "source_ip": "192.168.1.30",
            "status": "success",
            "description": "Normal helpdesk login"
        }
    ]

    return events


def main():
    events = generate_events()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} events: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
