import json
from pathlib import Path

PLAN_FILE = "august_dated_content_plan.json"

def main():
    path = Path(PLAN_FILE)

    if not path.exists():
        print(f"Nie znaleziono pliku: {PLAN_FILE}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print()
    print("=" * 60)
    print("SWETTATTOO — CONTENT PLAN APPROVAL")
    print("=" * 60)

    print()
    print(f"Miesiąc: {data.get('month', '-')}")
    print(f"Liczba tygodni: {len(data.get('weeks', []))}")

    total = sum(
        len(week.get("content", []))
        for week in data.get("weeks", [])
    )

    print(f"Liczba materiałów: {total}")
    print(f"Status: {data.get('status', 'DRAFT')}")

    print()
    print("Google Calendar: NIE ZMIENIONY")

    print()
    print("Aby zaakceptować plan, wpisz dokładnie:")
    print("APPROVE")

    print()
    answer = input("Twoja decyzja: ").strip()

    if answer != "APPROVE":
        print()
        print("PLAN NIE ZAAKCEPTOWANY.")
        print("Status pozostaje: DRAFT")
        return

    data["status"] = "APPROVED"
    data["approved_by_owner"] = True

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("=" * 60)
    print("PLAN ZAAKCEPTOWANY")
    print("=" * 60)

    print()
    print("Status: APPROVED")
    print("Google Calendar: NIE ZMIENIONY")
    print()
    print("Następny etap:")
    print("APPROVED → GOOGLE CALENDAR")
    print("=" * 60)


if __name__ == "__main__":
    main()
