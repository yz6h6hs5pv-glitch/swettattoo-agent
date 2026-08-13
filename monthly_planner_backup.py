import json

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


def print_value(value):
    if isinstance(value, list):
        for item in value:
            print(f"- {item}")
    elif isinstance(value, dict):
        for key, item in value.items():
            print(f"{key}: {item}")
    else:
        print(value)


def print_month(month_name, month):
    print("\n" + "=" * 50)
    print("SWETTATTOO — MONTHLY STRATEGY")
    print("=" * 50)

    print(f"\nMIESIĄC:\n{month_name}")

    print("\nSIŁA MIESIĄCA:")
    print_value(month.get("strength", "-"))

    print("\nGŁÓWNY CEL:")
    print_value(month.get("main_goal", "-"))

    print("\nGŁÓWNE TEMATY:")
    print_value(month.get("main_topics", []))

    print("\nKAMPANIE:")
    campaigns = month.get("campaigns", [])
    if campaigns:
        print_value(campaigns)
    else:
        print("- brak głównej kampanii")

    print("\nPRIORYTET SPRZEDAŻOWY:")
    print_value(month.get("sales_priority", "-"))

    print("\nREKOMENDOWANA CZĘSTOTLIWOŚĆ:")
    print_value(month.get("recommended_frequency", "-"))

    print("\nZASADA:")
    print_value(
        month.get(
            "rule",
            "Jakość ważniejsza niż częstotliwość."
        )
    )

    print("\n" + "=" * 50)


def main():
    strategy = load_strategy()

    month_name = input(
        "\nPodaj miesiąc po angielsku "
        "(January, February, March...): "
    ).strip()

    name, month = find_month(strategy, month_name)

    if month is None:
        print("\nNie znaleziono miesiąca.")
        print("Dostępne miesiące:")

        calendar = strategy.get("annual_calendar", {})

        if isinstance(calendar, dict):
            for name in calendar.keys():
                print(f"- {name}")

        elif isinstance(calendar, list):
            for item in calendar:
                if isinstance(item, dict):
                    print(f"- {item.get('month', '?')}")

        return

    print_month(name, month)


if __name__ == "__main__":
    main()