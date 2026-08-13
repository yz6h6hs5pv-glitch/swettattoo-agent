import json
from datetime import datetime


STRATEGY_FILE = "yearly_strategy.json"
PLAN_FILE = "content_plan.json"


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_strategy():
    return load_json(STRATEGY_FILE)


def get_current_plan():
    try:
        return load_json(PLAN_FILE)
    except FileNotFoundError:
        return None


def show_strategy():
    strategy = get_strategy()

    print("\n=== SWETTATTOO CONTENT SYSTEM ===\n")

    if isinstance(strategy, dict):
        print("Strategia została załadowana.")
        print(f"Liczba głównych sekcji: {len(strategy)}")

        for key in strategy.keys():
            print(f"- {key}")

    print("\nSystem jest gotowy do dalszego planowania.")


def main():
    show_strategy()


if __name__ == "__main__":
    main()
