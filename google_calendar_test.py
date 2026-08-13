from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

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


service = get_calendar_service()

start = datetime(2026, 8, 17, 9, 0)
end = start + timedelta(hours=1)

event = {
    "summary": "TEST — Swettattoo Content Plan",
    "description": "To jest wydarzenie testowe utworzone przez agenta Swettattoo.",
    "start": {
        "dateTime": start.isoformat(),
        "timeZone": "Europe/Warsaw",
    },
    "end": {
        "dateTime": end.isoformat(),
        "timeZone": "Europe/Warsaw",
    },
}

created_event = service.events().insert(
    calendarId="u3720236405@gmail.com",
    body=event
).execute()

print("=== SUKCES ===")
print("Utworzono wydarzenie:")
print(created_event.get("summary"))
print(created_event.get("htmlLink"))