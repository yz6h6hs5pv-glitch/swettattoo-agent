import json
import os
from pathlib import Path
from datetime import datetime, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

PLAN_FILE = "august_dated_content_plan.json"
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
CALENDAR_ID = "u3720236405@gmail.com"

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

TIMEZONE = "Europe/Warsaw"

PUBLISH_TIMES = {
    "Reel": "18:00",
    "Post": "12:00",
    "Stories": "10:00",
}


def get_calendar_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build(
        "calendar",
        "v3",
        credentials=creds
    )


def load_approved_plan():
    path = Path(PLAN_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku: {PLAN_FILE}"
        )

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("status") != "APPROVED":
        raise ValueError(
            "Plan nie jest zaakceptowany. "
            "Google Calendar nie zostanie zmieniony."
        )

    return data


def build_event(item):
    time_string = PUBLISH_TIMES.get(
        item["type"],
        "12:00"
    )

    start = datetime.strptime(
        f"{item['date']} {time_string}",
        "%d.%m.%Y %H:%M"
    )

    end = start + timedelta(minutes=30)

    preparation = "\n".join(
        f"- {x}"
        for x in item.get("preparation", [])
    )

    description = (
        f"SWETTATTOO — PLAN TREŚCI\n\n"
        f"Cel: {item.get('goal', '-')}\n"
        f"Temat: {item.get('topic', '-')}\n"
        f"Typ: {item.get('type', '-')}\n"
        f"Platformy: {', '.join(item.get('platforms', []))}\n\n"
        f"Odpowiedzialny za content: "
        f"{item.get('responsible_content', '-')}\n"
        f"Odpowiedzialny za publikację: "
        f"{item.get('responsible_publication', '-')}\n\n"
        f"PRZYGOTOWANIE:\n"
        f"{preparation}"
    )

    return {
        "summary": (
            f"SWETTATTOO | "
            f"{item['type']} | "
            f"{item['topic']}"
        ),
        "description": description,
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": TIMEZONE,
start_dt = datetime.fromisoformat(start_time)

if start_dt.tzinfo is None:
    from zoneinfo import ZoneInfo
    start_dt = start_dt.replace(tzinfo=ZoneInfo("Europe/Warsaw"))

end_dt = start_dt + timedelta(minutes=30)        }
    }


def event_exists(service, event_data):
    start_time = event_data["start"]["dateTime"]

    start_dt = datetime.fromisoformat(start_time)
    end_dt = start_dt + timedelta(minutes=30)

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    for event in events.get("items", []):
        if event.get("summary") == event_data["summary"]:
            return event

    return None


def publish_events(service, data):
    created = 0
    skipped = 0
    errors = 0
    results = []

    for week in data["weeks"]:
        for item in week["content"]:

            event_data = build_event(item)

            try:
                existing = event_exists(
                    service,
                    event_data
                )

                if existing:
                    print(
                        f"SKIP | {item['date']} | "
                        f"{item['type']} | {item['topic']}"
                    )

                    skipped += 1

                    results.append({
                        "status": "SKIPPED",
                        "item": item,
                        "event_id": existing.get("id")
                    })

                    continue

                created_event = service.events().insert(
                    calendarId=CALENDAR_ID,
                    body=event_data
                ).execute()

                created += 1

                results.append({
                    "status": "CREATED",
                    "item": item,
                    "event_id": created_event.get("id"),
                    "link": created_event.get("htmlLink")
                })

                print(
                    f"CREATED | {item['date']} | "
                    f"{item['type']} | {item['topic']}"
                )

            except Exception as e:
                errors += 1

                print(
                    f"ERROR | {item['date']} | "
                    f"{item['type']} | {e}"
                )

    return created, skipped, errors, results


def save_results(results):
    output_file = "august_calendar_results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )

    return output_file


def main():
    print()
    print("=" * 60)
    print("SWETTATTOO — GOOGLE CALENDAR PUBLISHER")
    print("=" * 60)

    data = load_approved_plan()

    total = sum(
        len(week["content"])
        for week in data["weeks"]
    )

    print()
    print("PLAN: APPROVED")
    print(f"MATERIAŁÓW: {total}")
    print()
    print("Google Calendar będzie aktualizowany.")
    print()

    service = get_calendar_service()

    created, skipped, errors, results = publish_events(
        service,
        data
    )

    result_file = save_results(results)

    print()
    print("=" * 60)
    print("PUBLIKACJA ZAKOŃCZONA")
    print("=" * 60)

    print()
    print(f"ŁĄCZNIE: {total}")
    print(f"UTWORZONO: {created}")
    print(f"POMINIĘTO — JUŻ ISTNIAŁY: {skipped}")
    print(f"BŁĘDY: {errors}")

    print()
    print(f"Wyniki zapisane: {result_file}")

    if errors == 0:
        print()
        print("STATUS: SUCCESS")
    else:
        print()
        print("STATUS: CHECK ERRORS")


if __name__ == "__main__":
    main()
