import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_monthly_plan():
    files = sorted(Path(".").glob("monthly_plan_*.json"))

    if not files:
        raise FileNotFoundError(
            "Nie znaleziono żadnego pliku monthly_plan_*.json"
        )

    if len(sys.argv) > 1:
        requested = sys.argv[1].lower()
        for file in files:
            if requested in file.stem.lower():
                return file

    return files[-1]


def load_plan(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_week(date_start, date_end, week_number):
    return {
        "week": week_number,
        "date_from": date_start.strftime("%d.%m.%Y"),
        "date_to": date_end.strftime("%d.%m.%Y"),
        "strategy": "",
        "publishing_days": [],
        "preparation_tasks": [],
        "content_debt": [],
        "notes": []
    }


def main():
    plan_path = find_monthly_plan()
    plan = load_plan(plan_path)

    month_name = plan["month"]

    print("\n" + "=" * 60)
    print("SWETTATTOO — WEEKLY CONTENT PLANNER")
    print("=" * 60)

    print(f"\nPLIK: {plan_path.name}")
    print(f"MIESIĄC: {month_name}")
    print(f"CEL: {plan.get('goal', plan.get('main_goal', '-'))}")

    print("\nTEMATY:")
    for topic in plan.get("topics", []):
        print(f"- {topic}")

    print("\nCZĘSTOTLIWOŚĆ:")
    for key, value in plan.get("frequency", {}).items():
        print(f"{key}: {value}")

    print("\nTWORZENIE STRUKTURY TYGODNI...")

    try:
        month_number = datetime.strptime(month_name, "%B").month
    except ValueError:
        raise ValueError(
            f"Nieprawidłowa nazwa miesiąca: {month_name}"
        )

    year = 2026

    first_day = datetime(year, month_number, 1)

    if month_number == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month_number + 1, 1)

    last_day = next_month - timedelta(days=1)

    weeks = []

    current = first_day
    week_number = 1

    while current <= last_day:
        week_start = current
        week_end = min(
            current + timedelta(days=6),
            last_day
        )

        week = create_week(
            week_start,
            week_end,
            week_number
        )

        week["strategy"] = (
            "Jakość ważniejsza niż częstotliwość. "
            "Publikować tylko mocne materiały."
        )

        week["notes"].append(
            "Pozostawić dni bez publikacji."
        )

        week["notes"].append(
            "Reels: priorytet dla dużych projektów, "
            "historii klientów i życia studia."
        )

        week["notes"].append(
            "Posts: głównie mocne realizacje "
            "i portfolio premium."
        )

        week["notes"].append(
            "Stories: studio, klienci, opinie, "
            "proces i spontaniczne sytuacje."
        )

        weeks.append(week)

        current = week_end + timedelta(days=1)
        week_number += 1

    output = {
        "month": month_name,
        "strategy": plan.get(
            "goal",
            plan.get("main_goal", "")
        ),
        "weeks": weeks
    }

    filename = f"weekly_plan_{month_name.lower()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\nPLAN TYGODNIOWY UTWORZONY:")
    print(filename)

    print("\nLICZBA TYGODNI:")
    print(len(weeks))

    print("\nNastępny etap:")
    print("UZUPEŁNIENIE KONKRETNYCH PUBLIKACJI I ZADAŃ")


if __name__ == "__main__":
    main()
