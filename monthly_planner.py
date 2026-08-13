import json
from datetime import date, timedelta

STRATEGY_FILE = "yearly_strategy.json"


def load_strategy():
    with open(STRATEGY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_month(strategy, month_name):
    calendar = strategy.get("annual_calendar", {})

    if isinstance(calendar, dict):
        for name, data in calendar.items():
            if name.lower() == month_name.lower():
                return name, data

    elif isinstance(calendar, list):
        for item in calendar:
            if isinstance(item, dict):
                name = item.get("month", "")
                if name.lower() == month_name.lower():
                    return name, item

    return None, None


def print_list(items):
    if not items:
        print("- brak")
        return

    for item in items:
        print(f"- {item}")


def get_frequency(month):
    frequency = month.get("recommended_frequency", {})

    return {
        "Reels": frequency.get("Reels", "2-3 per week"),
        "Posts": frequency.get("Posts", "1-2 per week"),
        "Stories": frequency.get("Stories", "3-5 per week"),
    }


def generate_month_structure(month_name, month):
    frequency = get_frequency(month)

    plan = {
        "month": month_name,
        "strength": month.get("strength", ""),
        "goal": month.get("main_goal", ""),
        "topics": month.get("main_topics", []),
        "campaigns": month.get("campaigns", []),
        "sales_priority": month.get("sales_priority", ""),
        "frequency": frequency,
        "principle": month.get(
            "rule",
            "Jakość ważniejsza niż częstotliwość."
        ),
        "content_types": [
            {
                "type": "Reels",
                "target": frequency["Reels"],
                "role": "Reach / Trust / Expertise / Desire / Booking"
            },
            {
                "type": "Posts",
                "target": frequency["Posts"],
                "role": "Portfolio / Quality / Social proof"
            },
            {
                "type": "Stories",
                "target": frequency["Stories"],
                "role": "Relationship / Trust / Sales / Studio life"
            }
        ],
        "rules": [
            "Nie publikować słabego materiału tylko dlatego, że jest zaplanowany.",
            "Pozostawić dni bez publikacji, jeśli nie ma mocnego materiału.",
            "Duże projekty mają pierwszeństwo przed słabszymi materiałami.",
            "Każda dobra praca powinna otrzymać przynajmniej jedno publiczne wykorzystanie.",
            "Stories mogą być publikowane spontanicznie.",
            "Treści sprzedażowe nie powinny wyglądać jak ciągłe promocje.",
            "Głównym językiem komunikacji jest polski."
        ]
    }

    return plan


def print_month(month_name, month):
    print("\n" + "=" * 60)
    print("SWETTATTOO — MONTHLY STRATEGY")
    print("=" * 60)

    print(f"\nMIESIĄC:\n{month_name}")

    print("\nSIŁA MIESIĄCA:")
    print(month.get("strength", "-"))

    print("\nGŁÓWNY CEL:")
    print(month.get("main_goal", "-"))

    print("\nGŁÓWNE TEMATY:")
    print_list(month.get("main_topics", []))

    print("\nKAMPANIE:")
    campaigns = month.get("campaigns", [])
    if campaigns:
        print_list(campaigns)
    else:
        print("- brak głównej kampanii")

    print("\nPRIORYTET SPRZEDAŻOWY:")
    print(month.get("sales_priority", "-"))

    print("\nREKOMENDOWANA CZĘSTOTLIWOŚĆ:")

    frequency = get_frequency(month)

    for key, value in frequency.items():
        print(f"{key}: {value}")

    print("\nZASADA:")
    print(
        month.get(
            "rule",
            "Jakość ważniejsza niż częstotliwość."
        )
    )

    print("\n" + "=" * 60)


def save_monthly_plan(plan):
    filename = f"monthly_plan_{plan['month'].lower()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            plan,
            f,
            ensure_ascii=False,
            indent=2
        )

    return filename


def main():
    strategy = load_strategy()

    month_name = input(
        "\nPodaj miesiąc po angielsku "
        "(January, February, March...): "
    ).strip()

    name, month = find_month(strategy, month_name)

    if month is None:
        print("\nNie znaleziono miesiąca.")
        return

    print_month(name, month)

    print("\nTWORZENIE STRUKTURY PLANU MIESIĘCZNEGO...")

    plan = generate_month_structure(name, month)

    filename = save_monthly_plan(plan)

    print("\nPLAN MIESIĘCZNY UTWORZONY:")
    print(filename)

    print("\nNastępny etap:")
    print("PLAN MIESIĘCZNY → PLAN TYGODNIOWY → ZADANIA → AKCEPTACJA")


if __name__ == "__main__":
    main()