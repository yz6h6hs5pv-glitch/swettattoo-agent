import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CALENDAR_ID = "u3720236405@gmail.com"


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def load_content_plan():
    with open("content_plan.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if "tasks" not in data:
        raise ValueError(
            "Nie znaleziono sekcji 'tasks' w content_plan.json"
        )

    return data["tasks"]


def convert_date(date_string):
    """
    Zamienia DD.MM.YYYY na YYYY-MM-DD.
    """
    date_object = datetime.strptime(date_string, "%d.%m.%Y")
    return date_object.strftime("%Y-%m-%d")


def main():
    print("\n=== SWETTATTOO CONTENT PLAN ===\n")

    plan = load_content_plan()

    print(f"Znaleziono zadań: {len(plan)}\n")

    for i, task in enumerate(plan, start=1):
        print(
            f"{i}. {task['date']} | "
            f"{task['responsible']} | "
            f"{task['task_type']} | "
            f"{task['title']}"
        )

    print("\n--------------------------------")
    print("Czy chcesz dodać ten plan do Google Calendar?")
    print("Wpisz TAK, aby kontynuować.")
    print("--------------------------------\n")

    answer = input("> ")

    if answer.strip().upper() != "TAK":
        print("\nAnulowano.")
        print("Żadne wydarzenie nie zostało dodane.")
        return

    service = get_calendar_service()

    print("\nDodawanie wydarzeń...\n")

    created_count = 0

    for task in plan:

        date = convert_date(task["date"])

        description = (
            f"ODPOWIEDZIALNY:\n"
            f"{task['responsible']}\n\n"

            f"TYP ZADANIA:\n"
            f"{task['task_type']}\n\n"

            f"PLATFORMA:\n"
            f"{task['platform']}\n\n"

            f"CEL:\n"
            f"{task['goal']}\n\n"

            f"CO TRZEBA ZROBIĆ:\n"
            f"{task['description']}\n\n"

            f"HOOK:\n"
            f"{task['hook']}\n\n"

            f"CTA:\n"
            f"{task['cta']}\n\n"

            f"---\n"
            f"Swettattoo Content Plan"
        )

        event = {
            "summary": (
                f"{task['responsible']} — "
                f"{task['title']}"
            ),

            "description": description,

            "start": {
                "date": date,
                "timeZone": "Europe/Warsaw"
            },

            "end": {
                "date": (
                    datetime.strptime(
                        date,
                        "%Y-%m-%d"
                    ) + timedelta(days=1)
                ).strftime("%Y-%m-%d"),
                "timeZone": "Europe/Warsaw"
            }
        }

        service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()

        print(
            f"✓ {task['date']} | "
            f"{task['responsible']} | "
            f"{task['title']}"
        )

        created_count += 1

    print("\n================================")
    print("GOTOWE")
    print("================================")
    print(f"Dodano wydarzeń: {created_count}")
    print("Wydarzenia są całodniowe.")
    print("Kalendarz: Swettattoo")
    print("================================\n")


if __name__ == "__main__":
    main()