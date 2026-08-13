import json

FILE = "yearly_strategy.json"


def load_strategy():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    strategy = load_strategy()

    print("\n================================")
    print(" SWETTATTOO — KALENDARZ ROCZNY")
    print("================================\n")

    calendar = strategy.get("annual_calendar", {})

    if not calendar:
        print("Brak annual_calendar w strategii.")
        return

    for month, data in calendar.items():
        print(f"\n### {month}")

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(data)

    print("\n================================")
    print("KONIEC KALENDARZA")
    print("================================")


if __name__ == "__main__":
    main()
