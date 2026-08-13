import json
from datetime import datetime, timedelta
from google_calendar_test import get_calendar_service

PLAN_FILE = "august_dated_content_plan.json"

with open(PLAN_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

if data.get("status") != "APPROVED":
    raise ValueError("Plan nie jest zaakceptowany.")

item = data["weeks"][0]["content"][0]

start = datetime.strptime(item["date"], "%d.%m.%Y").replace(hour=9, minute=0)
end = start + timedelta(hours=1)

event = {
    "summary": f"SWETTATTOO TEST | {item['type']} | {item['topic']}",
    "description": (
        f"Cel: {item.get('goal', '-')}\n"
        f"Platformy: {', '.join(item.get('platforms', []))}\n"
        f"Odpowiedzialny: {item.get('responsible_content', '-')}"
    ),
    "start": {
        "dateTime": start.isoformat(),
        "timeZone": "Europe/Warsaw",
    },
    "end": {
        "dateTime": end.isoformat(),
        "timeZone": "Europe/Warsaw",
    },
}

service = get_calendar_service()

created = service.events().insert(
    calendarId="u3720236405@gmail.com",
    body=event
).execute()

print()
print("=== TEST CALENDAR — SUKCES ===")
print("Data:", item["date"])
print("Typ:", item["type"])
print("Temat:", item["topic"])
print("Link:", created.get("htmlLink"))
