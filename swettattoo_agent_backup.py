import json
import subprocess
from pathlib import Path


def run_command(command):
    print()
    print("=" * 60)
    print("ЗАПУСК:", command)
    print("=" * 60)
    print()

    result = subprocess.run(command, shell=True)

    print()

    if result.returncode == 0:
        print("ОПЕРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
    else:
        print("ОПЕРАЦИЯ ЗАВЕРШИЛАСЬ С ОШИБКОЙ")

    input("\nНажмите Enter для продолжения...")


def find_plans():
    plans = []

    for file in Path(".").glob("*_content_plan.json"):
        if "_dated_" not in file.name:
            plans.append(file)

    return sorted(plans)


def find_dated_plans():
    plans = []

    for file in Path(".").glob("*_dated_content_plan.json"):
        plans.append(file)

    return sorted(plans)


def show_plan():
    plans = find_dated_plans()

    if not plans:
        print("\nДатированных планов пока нет.")
        input("\nНажмите Enter...")
        return

    print("\nДОСТУПНЫЕ ПЛАНЫ:\n")

    for i, plan in enumerate(plans, 1):
        print(f"{i}. {plan.name}")

    print()

    choice = input("Выберите план: ").strip()

    if not choice.isdigit():
        print("Неверный выбор.")
        input("\nНажмите Enter...")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(plans):
        print("Неверный выбор.")
        input("\nНажмите Enter...")
        return

    plan = plans[index]

    with open(plan, "r", encoding="utf-8") as f:
        data = json.load(f)

    print()
    print("=" * 60)
    print(f"PLAN: {plan.name}")
    print("=" * 60)

    total = 0

    for week in data.get("weeks", []):
        print()
        print(f"TYDZIEŃ {week.get('week')}")

        for item in week.get("content", []):
            total += 1

            print(
                f"{item.get('date', '-')} | "
                f"{item.get('type', '-'):8} | "
                f"{item.get('goal', '-'):15} | "
                f"{item.get('topic', '-')}"
            )

    print()
    print(f"ŁĄCZNIE: {total}")
    print(f"STATUS: {data.get('status', 'DRAFT')}")

    input("\nНажмите Enter для продолжения...")


def show_status():
    print()
    print("=" * 60)
    print("SWETTATTOO — STATUS")
    print("=" * 60)

    plans = find_dated_plans()

    if not plans:
        print("\nДатированных планов нет.")
        input("\nНажмите Enter...")
        return

    for plan in plans:
        try:
            with open(plan, "r", encoding="utf-8") as f:
                data = json.load(f)

            total = sum(
                len(week.get("content", []))
                for week in data.get("weeks", [])
            )

            print()
            print(f"План: {plan.name}")
            print(f"Статус: {data.get('status', 'DRAFT')}")
            print(f"Материалов: {total}")
            print(
                "Approval required:",
                data.get("approval_required", False)
            )

        except Exception as e:
            print(f"{plan.name}: ERROR — {e}")

    input("\nНажмите Enter для продолжения...")


def menu():
    while True:
        print()
        print("=" * 60)
        print("SWETTATTOO CONTENT AGENT")
        print("=" * 60)
        print()
        print("1. Создать новый месяц")
        print("2. Показать текущий план")
        print("3. Проверить план")
        print("4. Утвердить план")
        print("5. Отправить в Google Calendar")
        print("6. Показать статус")
        print("0. Выход")
        print()

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            run_command("python3 monthly_planner.py")

        elif choice == "2":
            show_plan()

        elif choice == "3":
            run_command("python3 audit_content.py")

        elif choice == "4":
            run_command("python3 approval.py")

        elif choice == "5":
            run_command("python3 calendar_publisher.py")

        elif choice == "6":
            show_status()

        elif choice == "0":
            print("\nВыход.")
            break

        else:
            print("\nНеверный выбор.")
            input("Нажмите Enter...")


if __name__ == "__main__":
    menu()
