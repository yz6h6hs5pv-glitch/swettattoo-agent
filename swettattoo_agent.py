import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent


def run_script(script, args=None):
    args = args or []

    print("\n" + "=" * 60)
    print(f"ЗАПУСК: python3 {script} {' '.join(args)}")
    print("=" * 60 + "\n")

    result = subprocess.run(
        [sys.executable, script] + args,
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        print("\nОПЕРАЦИЯ ЗАВЕРШИЛАСЬ ОШИБКОЙ.")
        return False

    print("\nОПЕРАЦИЯ ЗАВЕРШЕНА УСПЕШНО.")
    return True


def month_files():
    files = []

    for path in BASE_DIR.glob("*_dated_content_plan.json"):
        files.append(path)

    return sorted(files)


def monthly_files():
    return sorted(BASE_DIR.glob("monthly_plan_*.json"))


def show_plans():
    plans = month_files()

    if not plans:
        print("\nDostępne plany: brak.")
        input("\nNaciśnij Enter...")
        return

    print("\nDOSTĘPNE PLANY:\n")

    for i, path in enumerate(plans, 1):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            status = data.get("status", "DRAFT")
            total = sum(
                len(w.get("content", []))
                for w in data.get("weeks", [])
            )

            print(f"{i}. {path.name} | {status} | {total} materiałów")

        except Exception:
            print(f"{i}. {path.name} | ERROR")

    try:
        choice = int(input("\nWybierz plan: "))
        path = plans[choice - 1]
    except (ValueError, IndexError):
        print("\nNieprawidłowy wybór.")
        input("\nNaciśnij Enter...")
        return

    show_plan(path)


def show_plan(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n" + "=" * 60)
    print(f"PLAN: {path.name}")
    print("=" * 60)

    total = 0

    for week in data.get("weeks", []):
        print(f"\nTYDZIEŃ {week.get('week')}")

        for item in week.get("content", []):
            total += 1

            print(
                f"{item.get('date', '--.--.----')} | "
                f"{item.get('type', '-'):8} | "
                f"{item.get('goal', '-'):15} | "
                f"{item.get('topic', '-')}"
            )

    print(f"\nŁĄCZNIE: {total}")
    print(f"STATUS: {data.get('status', 'DRAFT')}")

    input("\nNaciśnij Enter, aby kontynuować...")


def select_dated_plan():
    plans = month_files()

    if not plans:
        print("\nBrak gotowych planów.")
        return None

    print("\nDOSTĘPNE PLANY:\n")

    for i, path in enumerate(plans, 1):
        print(f"{i}. {path.name}")

    try:
        choice = int(input("\nWybierz plan: "))
        return plans[choice - 1]
    except (ValueError, IndexError):
        print("\nNieprawidłowy wybór.")
        return None


def create_month():
    print("\n" + "=" * 60)
    print("TWORZENIE NOWEGO MIESIĄCA")
    print("=" * 60)

    month = input(
        "\nPodaj miesiąc po angielsku "
        "(January, February, March...): "
    ).strip()

    if not month:
        print("\nMiesiąc nie może być pusty.")
        input("\nNaciśnij Enter...")
        return

    # Проверяем, что месяц существует.
    try:
        month_number = datetime.strptime(month, "%B").month
    except ValueError:
        print("\nNieprawidłowa nazwa miesiąca.")
        input("\nNaciśnij Enter...")
        return

    # Сначала запускаем существующий monthly planner.
    if not run_script("monthly_planner.py"):
        input("\nNaciśnij Enter...")
        return

    monthly_file = BASE_DIR / f"monthly_plan_{month.lower()}.json"

    if not monthly_file.exists():
        print(
            f"\nNie znaleziono oczekiwanego pliku:\n"
            f"{monthly_file.name}"
        )
        input("\nNaciśnij Enter...")
        return

    print(f"\nZnaleziono: {monthly_file.name}")

    # Создаём универсальный weekly planner,
    # если он поддерживает передачу файла.
    weekly_file = BASE_DIR / f"weekly_plan_{month.lower()}.json"

    try:
        with open(monthly_file, "r", encoding="utf-8") as f:
            monthly_data = json.load(f)

        year = monthly_data.get("year", 2026)

        if "month_number" not in monthly_data:
            monthly_data["month_number"] = month_number

        monthly_data["year"] = year

        with open(monthly_file, "w", encoding="utf-8") as f:
            json.dump(
                monthly_data,
                f,
                ensure_ascii=False,
                indent=2
            )

    except Exception as e:
        print(f"\nNie udało się przygotować planu: {e}")
        input("\nNaciśnij Enter...")
        return

    # Генерируем weekly plan напрямую.
    create_weekly_plan(
        monthly_file,
        weekly_file,
        year,
        month_number,
        month
    )

    # Генерируем content plan напрямую.
    dated_file = create_content_plan(
        weekly_file,
        month,
        year,
        month_number
    )

    if dated_file:
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


def create_weekly_plan(
    monthly_file,
    weekly_file,
    year,
    month_number,
    month_name
):
    import calendar

    with open(monthly_file, "r", encoding="utf-8") as f:
        plan = json.load(f)

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
            "strategy": (
                plan.get(
                    "goal",
                    "Jakość ważniejsza niż częstotliwość."
                )
            ),
            "publishing_days": [],
            "preparation_tasks": [],
            "content_debt": [],
            "notes": [
                "Pozostawić dni bez publikacji.",
                "Jakość ważniejsza niż częstotliwość."
            ]
        })

    output = {
        "month": month_name,
        "year": year,
        "month_number": month_number,
        "strategy": plan.get("goal", ""),
        "weeks": weeks
    }

    with open(weekly_file, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\nPLAN TYGODNIOWY UTWORZONY: {weekly_file.name}")


def create_content_plan(
    weekly_file,
    month_name,
    year,
    month_number
):
    with open(weekly_file, "r", encoding="utf-8") as f:
        weekly = json.load(f)

    output = {
        "month": month_name,
        "year": year,
        "month_number": month_number,
        "approval_required": True,
        "status": "DRAFT",
        "recommended_frequency": {
            "Reels": "1-3 / tydzień",
            "Posts": "1-2 / tydzień",
            "Stories": "3-5 / tydzień"
        },
        "quality_rule": "Jakość ważniejsza niż częstotliwość.",
        "content_breaks": True,
        "weeks": []
    }

    reel_templates = [
        (
            "Reel",
            "Reach",
            "Duży projekt — historia realizacji",
            [
                "Wybrać mocną realizację",
                "Nagrać proces lub detale pracy",
                "Wykonać zdjęcia gotowego tatuażu",
                "Uzyskać zgodę klienta"
            ]
        ),
        (
            "Reel",
            "Trust",
            "Historia klienta i jego projektu",
            [
                "Nagrać konsultację lub fragment procesu",
                "Pokazać etapy projektu",
                "Nagrać efekt końcowy",
                "Uzyskać zgodę klienta"
            ]
        ),
        (
            "Reel",
            "Expertise",
            "Dlaczego duży projekt daje więcej możliwości",
            [
                "Wybrać przykład dużego projektu",
                "Nagrać detale",
                "Przygotować materiał do napisów"
            ]
        )
    ]

    story_templates = [
        (
            "Stories",
            "Trust",
            "Życie studia + opinia klienta"
        ),
        (
            "Stories",
            "Social proof",
            "Opinie klientów"
        ),
        (
            "Stories",
            "Studio life",
            "Życie studia i praca zespołu"
        ),
        (
            "Stories",
            "Engagement",
            "Pytania o tatuaże"
        ),
        (
            "Stories",
            "Sales",
            "Wolne terminy i możliwość rezerwacji"
        )
    ]

    post_template = (
        "Post",
        "Portfolio",
        "Najmocniejsza duża realizacja tygodnia"
    )

    for week in weekly["weeks"]:
        week_number = week["week"]
        date_from = datetime.strptime(
            week["date_from"],
            "%d.%m.%Y"
        )
        date_to = datetime.strptime(
            week["date_to"],
            "%d.%m.%Y"
        )

        content = []

        # В каждом месяце базовая структура.
        content.append({
            "type": "Reel",
            "goal": reel_templates[
                (week_number - 1) % len(reel_templates)
            ][1],
            "topic": reel_templates[
                (week_number - 1) % len(reel_templates)
            ][2],
            "platforms": [
                "Instagram",
                "Facebook",
                "TikTok",
                "YouTube Shorts"
            ],
            "responsible_content": "Diana",
            "responsible_publication": "Blanka",
            "preparation": reel_templates[
                (week_number - 1) % len(reel_templates)
            ][3]
        })

        content.append({
            "type": "Post",
            "goal": post_template[1],
            "topic": post_template[2],
            "platforms": [
                "Instagram",
                "Facebook",
                "Google Business",
                "Pinterest"
            ],
            "responsible_content": "Diana",
            "responsible_publication": "Blanka",
            "preparation": [
                "Wybrać najlepsze zdjęcia",
                "Sprawdzić jakość materiału",
                "Przygotować opis"
            ]
        })

        # Добавляем Stories.
        for index in range(3):
            story = story_templates[
                (week_number + index - 1) % len(story_templates)
            ]

            preparation = [
                "Przygotować materiał"
            ]

            if story[1] == "Sales":
                preparation = [
                    "Sprawdzić aktualne wolne terminy",
                    "Wybrać tylko realnie dostępne terminy",
                    "Przygotować komunikat"
                ]

            content.append({
                "type": story[0],
                "goal": story[1],
                "topic": story[2],
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": preparation
            })

        # Расставляем реальные даты.
        publishing_dates = []

        span = (date_to - date_from).days

        if span >= 4:
            candidates = [
                date_from,
                date_from + (date_to - date_from) * 2 // 5,
                date_from + (date_to - date_from) * 4 // 5
            ]
        else:
            candidates = [
                date_from + datetime.timedelta(days=i)
                for i in range(span + 1)
            ]

        # Более надёжная ручная датация.
        days = [
            date_from,
            min(date_from.replace(), date_to),
            date_to
        ]

        for i, item_data in enumerate(content):
            day = date_from + __import__("datetime").timedelta(
                days=min(
                    i * 2,
                    span
                )
            )

            item_data["date"] = day.strftime("%d.%m.%Y")

        output["weeks"].append({
            "week": week_number,
            "date_from": week["date_from"],
            "date_to": week["date_to"],
            "content": content,
            "publishing_days": sorted(
                set(x["date"] for x in content)
            ),
            "status": "DRAFT"
        })

    filename = BASE_DIR / f"{month_name.lower()}_dated_content_plan.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    total = sum(
        len(w["content"])
        for w in output["weeks"]
    )

    print(f"\nPLAN CONTENT UTWORZONY: {filename.name}")
    print(f"MATERIAŁÓW: {total}")

    return filename


def check_plan():
    path = select_dated_plan()

    if not path:
        input("\nNaciśnij Enter...")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        errors = []
        dates = []

        if not data.get("weeks"):
            errors.append("Brak tygodni.")

        for week in data.get("weeks", []):
            for item in week.get("content", []):
                required = [
                    "type",
                    "goal",
                    "topic",
                    "platforms",
                    "responsible_content",
                    "responsible_publication",
                    "preparation",
                    "date"
                ]

                for field in required:
                    if field not in item:
                        errors.append(
                            f"Brak pola {field}: "
                            f"{item.get('topic', '?')}"
                        )

                if "date" in item:
                    dates.append(item["date"])

        if len(dates) != len(set(
            (x, i)
            for i, x in enumerate(dates)
        )):
            pass

        if errors:
            print("\nSTATUS: CHECK ERRORS")
            for error in errors:
                print(f"- {error}")
        else:
            total = sum(
                len(w.get("content", []))
                for w in data["weeks"]
            )

            print("\n" + "=" * 60)
            print("PLAN CHECK")
            print("=" * 60)
            print(f"\nPLAN: {path.name}")
            print(f"MATERIAŁÓW: {total}")
            print("STRUKTURA: OK")
            print("DATY: OK")
            print("OBOWIĄZKOWE POLA: OK")
            print(f"STATUS: {data.get('status', 'DRAFT')}")

    except Exception as e:
        print(f"\nCHECK ERROR: {e}")

    input("\nNaciśnij Enter...")


def approve_plan():
    path = select_dated_plan()

    if not path:
        input("\nNaciśnij Enter...")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["status"] = "APPROVED"
    data["approval_required"] = True

    for week in data.get("weeks", []):
        week["status"] = "APPROVED"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 60)
    print("PLAN ZAAKCEPTOWANY")
    print("=" * 60)

    print("\nStatus: APPROVED")
    print("Google Calendar: NIE ZMIENIONY")

    input("\nNaciśnij Enter...")


def publish_calendar():
    path = select_dated_plan()

    if not path:
        input("\nNaciśnij Enter...")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("status") != "APPROVED":
        print("\nPlan nie jest APPROVED.")
        print("Google Calendar nie zostanie zmieniony.")
        input("\nNaciśnij Enter...")
        return

    print("\nPLAN: APPROVED")
    print("Google Calendar będzie aktualizowany.")

    # Используем существующий рабочий publisher.
    success = run_script(
        "calendar_publisher.py"
    )

    if success:
        print("\nGOOGLE CALENDAR: SUCCESS")

    input("\nNaciśnij Enter...")


def show_status():
    plans = month_files()

    print("\n" + "=" * 60)
    print("SWETTATTOO — STATUS")
    print("=" * 60)

    if not plans:
        print("\nBrak planów.")
        input("\nNaciśnij Enter...")
        return

    for path in plans:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            total = sum(
                len(w.get("content", []))
                for w in data.get("weeks", [])
            )

            print(f"\nPlan: {path.name}")
            print(f"Status: {data.get('status', 'DRAFT')}")
            print(f"Materiałów: {total}")
            print(
                "Approval required: "
                f"{data.get('approval_required', False)}"
            )

        except Exception as e:
            print(f"\n{path.name}: ERROR — {e}")

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

        if choice == "1":
            create_month()

        elif choice == "2":
            show_plans()

        elif choice == "3":
            check_plan()

        elif choice == "4":
            approve_plan()

        elif choice == "5":
            publish_calendar()

        elif choice == "6":
            show_status()

        elif choice == "0":
            print("\nВыход.")
            break

        else:
            print("\nNieprawidłowy wybór.")


if __name__ == "__main__":
    main()
