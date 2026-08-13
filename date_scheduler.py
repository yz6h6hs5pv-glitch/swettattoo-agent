import json
from datetime import datetime, timedelta

INPUT_FILE = "august_content_plan.json"
OUTPUT_FILE = "august_dated_content_plan.json"


def load_plan():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_dates(date_from, date_to):
    start = datetime.strptime(date_from, "%d.%m.%Y")
    end = datetime.strptime(date_to, "%d.%m.%Y")

    dates = []
    current = start

    while current <= end:
        dates.append(current)
        current += timedelta(days=1)

    return dates


def choose_days(dates, content):
    reels = [x for x in content if x["type"] == "Reel"]
    posts = [x for x in content if x["type"] == "Post"]
    stories = [x for x in content if x["type"] == "Stories"]

    result = []

    # Publikacje główne rozkładamy możliwie równomiernie.
    main_content = reels + posts

    if main_content:
        positions = []

        if len(main_content) == 1:
            positions = [len(dates) // 2]

        elif len(main_content) == 2:
            positions = [
                len(dates) // 3,
                (len(dates) * 2) // 3
            ]

        else:
            step = len(dates) / len(main_content)

            for i in range(len(main_content)):
                positions.append(int(i * step + step / 2))

        for item, position in zip(main_content, positions):
            position = min(position, len(dates) - 1)

            result.append({
                "date": dates[position].strftime("%d.%m.%Y"),
                "type": item["type"],
                "goal": item["goal"],
                "topic": item["topic"],
                "platforms": item["platforms"],
                "responsible_content": item["responsible_content"],
                "responsible_publication": item["responsible_publication"],
                "preparation": item["preparation"],
                **({"language": item["language"]} if "language" in item else {})
            })

    # Stories dostają osobne dni.
    # Mogą też wypaść w dzień z Reel/Post.
    story_positions = []

    if stories:
        available_positions = list(range(len(dates)))

        if len(stories) >= len(available_positions):
            story_positions = available_positions[:len(stories)]
        else:
            step = len(dates) / len(stories)

            for i in range(len(stories)):
                story_positions.append(
                    min(
                        int(i * step),
                        len(dates) - 1
                    )
                )

    for item, position in zip(stories, story_positions):
        result.append({
            "date": dates[position].strftime("%d.%m.%Y"),
            "type": item["type"],
            "goal": item["goal"],
            "topic": item["topic"],
            "platforms": item["platforms"],
            "responsible_content": item["responsible_content"],
            "responsible_publication": item["responsible_publication"],
            "preparation": item["preparation"],
            **({"language": item["language"]} if "language" in item else {})
        })

    result.sort(
        key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y")
    )

    return result


def main():
    data = load_plan()

    output = {
        "month": data["month"],
        "strategy": data["strategy"],
        "approval_required": True,
        "google_calendar_changed": False,
        "status": "DRAFT",
        "weeks": []
    }

    for week in data["weeks"]:
        dates = get_dates(
            week["date_from"],
            week["date_to"]
        )

        dated_content = choose_days(
            dates,
            week["content"]
        )

        output["weeks"].append({
            "week": week["week"],
            "date_from": week["date_from"],
            "date_to": week["date_to"],
            "content": dated_content,
            "status": "DRAFT"
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    total = sum(
        len(week["content"])
        for week in output["weeks"]
    )

    print("\n" + "=" * 60)
    print("SWETTATTOO — DATE SCHEDULER")
    print("=" * 60)

    print(f"\nPLAN UTWORZONY: {OUTPUT_FILE}")
    print("\nStatus: DRAFT")
    print("Google Calendar: NIE ZMIENIONY")
    print("Akceptacja właściciela: WYMAGANA")

    print("\nLICZBA TYGODNI:", len(output["weeks"]))
    print("LICZBA ZAPLANOWANYCH MATERIAŁÓW:", total)

    print("\nNastępny etap:")
    print("PRZEGLĄD DAT → AKCEPTACJA → GOOGLE CALENDAR")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
