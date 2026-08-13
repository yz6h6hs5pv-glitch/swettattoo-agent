import calendar
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from month_utils import resolve_month

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_YEAR = datetime.now().year


def run_script(script, input_text=None):
    print("\n" + "=" * 60)
    print(f"ZAPUSZCZAM: {script}")
    print("=" * 60 + "\n")
    result = subprocess.run(
        [sys.executable, script],
        cwd=BASE_DIR,
        input=input_text,
        text=True,
    )
    if result.returncode != 0:
        print("\nOPERACJA ZAKOŃCZYŁA SIĘ BŁĘDEM.")
        return False
    print("\nOPERACJA ZAKOŃCZONA POMYŚLNIE.")
    return True


def month_files():
    return sorted(BASE_DIR.glob("*_dated_content_plan.json"))


def select_dated_plan():
    plans = month_files()
    if not plans:
        print("\nBrak gotowych planów.")
        return None
    print("\nDOSTĘPNE PLANY:\n")
    for i, path in enumerate(plans, 1):
        print(f"{i}. {path.name}")
    try:
        return plans[int(input("\nWybierz plan: ")) - 1]
    except (ValueError, IndexError):
        print("\nNieprawidłowy wybór.")
        return None


def show_plan(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    print("\n" + "=" * 60)
    print(f"PLAN: {path.name}")
    print("=" * 60)
    total = 0
    for week in data.get("weeks", []):
        print(f"\nTYDZIEŃ {week.get('week')}")
        for item in week.get("content", []):
            total += 1
            print(f"{item.get('date', '--.--.----')} | {item.get('type', '-'):8} | {item.get('goal', '-'):15} | {item.get('topic', '-')}")
    print(f"\nŁĄCZNIE: {total}")
    print(f"STATUS: {data.get('status', 'DRAFT')}")
    input("\nNaciśnij Enter, aby kontynuować...")


def show_plans():
    plans = month_files()
    if not plans:
        print("\nDostępne plany: brak.")
        input("\nNaciśnij Enter...")
        return
    print("\nDOSTĘPNE PLANY:\n")
    for i, path in enumerate(plans, 1):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            total = sum(len(w.get("content", [])) for w in data.get("weeks", []))
            print(f"{i}. {path.name} | {data.get('status', 'DRAFT')} | {total} materiałów")
        except Exception as exc:
            print(f"{i}. {path.name} | ERROR: {exc}")
    try:
        path = plans[int(input("\nWybierz plan: ")) - 1]
        show_plan(path)
    except (ValueError, IndexError):
        print("\nNieprawidłowy wybór.")
        input("\nNaciśnij Enter...")


def create_month():
    print("\n" + "=" * 60)
    print("TWORZENIE NOWEGO MIESIĄCA")
    print("=" * 60)
    print("\nPodaj pełną nazwę, skrót albo numer.")
    print("Przykład: September / Sep / 9")

    raw = input("\nMiesiąc: ").strip()
    month, month_number = resolve_month(raw)
    if month is None:
        print("\nNieprawidłowy miesiąc.")
        print("Dozwolone: January-December, Jan-Dec albo 1-12.")
        input("\nNaciśnij Enter...")
        return

    monthly_file = BASE_DIR / f"monthly_plan_{month.lower()}.json"
    weekly_file = BASE_DIR / f"weekly_plan_{month.lower()}.json"

    # The normalized canonical month is passed to the monthly planner.
    # No locale-dependent datetime.strptime('%B') is used here.
    if not run_script("monthly_planner.py", input_text=f"{month}\n"):
        input("\nNaciśnij Enter...")
        return

    if not monthly_file.exists():
        print(f"\nNie znaleziono oczekiwanego pliku: {monthly_file.name}")
        input("\nNaciśnij Enter...")
        return

    try:
        data = json.loads(monthly_file.read_text(encoding="utf-8"))
        year = int(data.get("year", DEFAULT_YEAR))
        data["month"] = month
        data["month_number"] = month_number
        data["year"] = year
        monthly_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"\nNie udało się przygotować planu: {exc}")
        input("\nNaciśnij Enter...")
        return

    create_weekly_plan(monthly_file, weekly_file, year, month_number, month)
    dated_file = create_content_plan(weekly_file, month, year, month_number)

    print("\n" + "=" * 60)
    print("NOWY MIESIĄC GOTOWY")
    print("=" * 60)
    print(f"\nMiesiąc: {month}")
    print(f"Plan miesięczny: {monthly_file.name}")
    print(f"Plan tygodniowy: {weekly_file.name}")
    print(f"Plan content: {dated_file.name}")
    print("\nSTATUS: DRAFT")
    print("Google Calendar: NIE ZMIENIONY")
    input("\nNaciśnij Enter, aby kontynuować...")


def create_weekly_plan(monthly_file, weekly_file, year, month_number, month_name):
    plan = json.loads(monthly_file.read_text(encoding="utf-8"))
    last_day = calendar.monthrange(year, month_number)[1]
    weeks = []
    for day in range(1, last_day + 1, 7):
        start = datetime(year, month_number, day)
        end_day = min(day + 6, last_day)
        end = datetime(year, month_number, end_day)
        weeks.append({
            "week": len(weeks) + 1,
            "date_from": start.strftime("%d.%m.%Y"),
            "date_to": end.strftime("%d.%m.%Y"),
            "strategy": plan.get("goal", "Jakość ważniejsza niż częstotliwość."),
            "publishing_days": [],
            "preparation_tasks": [],
            "content_debt": [],
            "notes": ["Pozostawić dni bez publikacji.", "Jakość ważniejsza niż częstotliwość."],
        })
    output = {"month": month_name, "year": year, "month_number": month_number, "strategy": plan.get("goal", ""), "weeks": weeks}
    weekly_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nPLAN TYGODNIOWY UTWORZONY: {weekly_file.name}")


def create_content_plan(weekly_file, month_name, year, month_number):
    weekly = json.loads(weekly_file.read_text(encoding="utf-8"))
    output = {
        "month": month_name,
        "year": year,
        "month_number": month_number,
        "approval_required": True,
        "status": "DRAFT",
        "recommended_frequency": {"Reels": "1-3 / tydzień", "Posts": "1-2 / tydzień", "Stories": "3-5 / tydzień"},
        "quality_rule": "Jakość ważniejsza niż częstotliwość.",
        "content_breaks": True,
        "weeks": [],
    }
    reel_templates = [
        ("Reach", "Duży projekt — historia realizacji", ["Wybrać mocną realizację", "Nagrać proces lub detale pracy", "Wykonać zdjęcia gotowego tatuażu", "Uzyskać zgodę klienta"]),
        ("Trust", "Historia klienta i jego projektu", ["Nagrać konsultację lub fragment procesu", "Pokazać etapy projektu", "Nagrać efekt końcowy", "Uzyskać zgodę klienta"]),
        ("Expertise", "Dlaczego duży projekt daje więcej możliwości", ["Wybrać przykład dużego projektu", "Nagrać detale", "Przygotować materiał do napisów"]),
    ]
    story_templates = [
        ("Trust", "Życie studia + opinia klienta"),
        ("Social proof", "Opinie klientów"),
        ("Studio life", "Życie studia i praca zespołu"),
        ("Engagement", "Pytania o tatuaże"),
        ("Sales", "Wolne terminy i możliwość rezerwacji"),
    ]

    for week in weekly["weeks"]:
        week_number = week["week"]
        date_from = datetime.strptime(week["date_from"], "%d.%m.%Y")
        date_to = datetime.strptime(week["date_to"], "%d.%m.%Y")
        span = (date_to - date_from).days
        reel_goal, reel_topic, reel_prep = reel_templates[(week_number - 1) % len(reel_templates)]
        content = [
            {"type": "Reel", "goal": reel_goal, "topic": reel_topic, "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"], "responsible_content": "Diana", "responsible_publication": "Blanka", "preparation": reel_prep},
            {"type": "Post", "goal": "Portfolio", "topic": "Najmocniejsza duża realizacja tygodnia", "platforms": ["Instagram", "Facebook", "Google Business", "Pinterest"], "responsible_content": "Diana", "responsible_publication": "Blanka", "preparation": ["Wybrać najlepsze zdjęcia", "Sprawdzić jakość materiału", "Przygotować opis"]},
        ]
        for index in range(3):
            goal, topic = story_templates[(week_number + index - 1) % len(story_templates)]
            preparation = ["Przygotować materiał"]
            if goal == "Sales":
                preparation = ["Sprawdzić aktualne wolne terminy", "Wybrać tylko realnie dostępne terminy", "Przygotować komunikat"]
            content.append({"type": "Stories", "goal": goal, "topic": topic, "platforms": ["Instagram Stories"], "responsible_content": "Diana", "responsible_publication": "Blanka", "preparation": preparation})
        for index, item in enumerate(content):
            item["date"] = (date_from + timedelta(days=min(index * 2, span))).strftime("%d.%m.%Y")
        output["weeks"].append({"week": week_number, "date_from": week["date_from"], "date_to": week["date_to"], "content": content, "publishing_days": sorted({x["date"] for x in content}), "status": "DRAFT"})

    filename = BASE_DIR / f"{month_name.lower()}_dated_content_plan.json"
    filename.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nPLAN CONTENT UTWORZONY: {filename.name}")
    print(f"MATERIAŁÓW: {sum(len(w['content']) for w in output['weeks'])}")
    return filename


def check_plan():
    path = select_dated_plan()
    if not path:
        input("\nNaciśnij Enter...")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = []
        dates = []
        required = ["type", "goal", "topic", "platforms", "responsible_content", "responsible_publication", "preparation", "date"]
        for week in data.get("weeks", []):
            for item in week.get("content", []):
                for field in required:
                    if field not in item:
                        errors.append(f"Brak pola {field}: {item.get('topic', '?')}")
                if "date" in item:
                    dates.append(item["date"])
        duplicates = sorted({d for d in dates if dates.count(d) > 1})
        if duplicates:
            errors.append("Powtarzające się daty: " + ", ".join(duplicates))
        if errors:
            print("\nSTATUS: CHECK ERRORS")
            for error in errors:
                print(f"- {error}")
        else:
            print("\nPLAN CHECK: OK")
            print(f"PLAN: {path.name}")
            print(f"MATERIAŁÓW: {sum(len(w.get('content', [])) for w in data.get('weeks', []))}")
            print(f"STATUS: {data.get('status', 'DRAFT')}")
    except Exception as exc:
        print(f"\nCHECK ERROR: {exc}")
    input("\nNaciśnij Enter...")


def approve_plan():
    path = select_dated_plan()
    if not path:
        input("\nNaciśnij Enter...")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["status"] = "APPROVED"
    data["approval_required"] = True
    for week in data.get("weeks", []):
        week["status"] = "APPROVED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nPLAN ZAAKCEPTOWANY — Google Calendar: NIE ZMIENIONY")
    input("\nNaciśnij Enter...")


def publish_calendar():
    path = select_dated_plan()
    if not path:
        input("\nNaciśnij Enter...")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "APPROVED":
        print("\nPlan nie jest APPROVED. Google Calendar nie zostanie zmieniony.")
        input("\nNaciśnij Enter...")
        return
    run_script("calendar_publisher.py")
    input("\nNaciśnij Enter...")


def show_status():
    plans = month_files()
    print("\nSWETTATTOO — STATUS")
    if not plans:
        print("\nBrak planów.")
    for path in plans:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            total = sum(len(w.get("content", [])) for w in data.get("weeks", []))
            print(f"\n{path.name} | {data.get('status', 'DRAFT')} | {total} materiałów")
        except Exception as exc:
            print(f"\n{path.name}: ERROR — {exc}")
    input("\nNaciśnij Enter...")


def main():
    while True:
        print("\n" + "=" * 60)
        print("SWETTATTOO CONTENT AGENT")
        print("=" * 60)
        print("""
1. Создать новый месяц
2. Показать текущий план
3. Проверить план
4. Утвердить план
5. Отправить в Google Calendar
6. Показать статус
0. Выход
""")
        choice = input("Выберите действие: ").strip()
        if choice == "1": create_month()
        elif choice == "2": show_plans()
        elif choice == "3": check_plan()
        elif choice == "4": approve_plan()
        elif choice == "5": publish_calendar()
        elif choice == "6": show_status()
        elif choice == "0": break
        else: print("\nNieprawidłowy wybór.")


if __name__ == "__main__":
    main()
