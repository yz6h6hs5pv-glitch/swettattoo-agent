import json

WEEKLY_PLAN_FILE = "weekly_plan_august.json"
OUTPUT_FILE = "august_content_plan.json"


def load_weekly_plan():
    with open(WEEKLY_PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def item(content_type, goal, topic, platforms, preparation, language=None):
    data = {
        "type": content_type,
        "goal": goal,
        "topic": topic,
        "platforms": platforms,
        "responsible_content": "Diana",
        "responsible_publication": "Blanka",
        "preparation": preparation
    }

    if language:
        data["language"] = language

    return data


def create_weekly_content(week_number):

    common_reels = [
        item(
            "Reel",
            "Reach",
            "Duży projekt — historia realizacji",
            ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
            [
                "Wybrać mocną realizację",
                "Nagrać proces lub detale pracy",
                "Wykonać zdjęcia gotowego tatuażu",
                "Uzyskać zgodę klienta"
            ]
        ),
        item(
            "Reel",
            "Trust",
            "Historia klienta i jego projektu",
            ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
            [
                "Nagrać konsultację lub fragment procesu",
                "Pokazać etapy projektu",
                "Nagrać efekt końcowy",
                "Uzyskać zgodę klienta"
            ]
        ),
        item(
            "Reel",
            "Expertise",
            "Dlaczego duży projekt daje więcej możliwości",
            ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
            [
                "Wybrać przykład dużego projektu",
                "Nagrać detale",
                "Przygotować materiał do napisów"
            ]
        )
    ]

    posts = [
        item(
            "Post",
            "Portfolio",
            "Najmocniejsza duża realizacja tygodnia",
            ["Instagram", "Facebook", "Google Business", "Pinterest"],
            [
                "Wybrać najlepsze zdjęcia",
                "Sprawdzić jakość materiału",
                "Przygotować opis"
            ]
        )
    ]

    stories = [
        item(
            "Stories",
            "Trust",
            "Życie studia + opinia klienta",
            ["Instagram Stories"],
            [
                "Nagrać naturalne ujęcia studia",
                "Wybrać 1–3 opinie Google"
            ]
        ),
        item(
            "Stories",
            "Social proof",
            "Opinie klientów",
            ["Instagram Stories"],
            [
                "Wybrać aktualne opinie Google",
                "Przygotować estetyczne Stories"
            ]
        ),
        item(
            "Stories",
            "Studio life",
            "Życie studia i praca zespołu",
            ["Instagram Stories"],
            [
                "Nagrać spontaniczne materiały",
                "Pokazać atmosferę studia"
            ]
        ),
        item(
            "Stories",
            "Engagement",
            "Pytania o tatuaże",
            ["Instagram Stories"],
            [
                "Przygotować naklejkę pytań",
                "Zebrać odpowiedzi"
            ]
        ),
        item(
            "Stories",
            "Sales",
            "Wolne terminy i możliwość rezerwacji",
            ["Instagram Stories"],
            [
                "Administrator sprawdza aktualne wolne terminy",
                "Wybrać tylko realnie dostępne terminy",
                "Przygotować komunikat bez sztucznej presji"
            ]
        )
    ]

    if week_number == 1:
        return [common_reels[0], posts[0], stories[0], stories[2], stories[4]]

    if week_number == 2:
        return [common_reels[1], common_reels[2], posts[0], stories[1], stories[3], stories[4]]

    if week_number == 3:
        return [
            item(
                "Reel",
                "Desire",
                "Cover-up lub trudna realizacja",
                ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                [
                    "Wybrać mocny przykład",
                    "Nagrać problem → rozwiązanie → efekt",
                    "Wykonać zdjęcia Before / After",
                    "Uzyskać zgodę klienta"
                ]
            ),
            common_reels[0],
            posts[0],
            stories[2],
            stories[1],
            stories[4]
        ]

    if week_number == 4:
        return [
            item(
                "Reel",
                "International",
                "Swettattoo w Szczecinie — klienci zagraniczni",
                ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                [
                    "Wybrać materiał pokazujący studio i Szczecin",
                    "Pokazać atmosferę studia",
                    "Przygotować wersję angielską"
                ],
                "PL + EN"
            ),
            common_reels[1],
            posts[0],
            stories[3],
            stories[0],
            stories[4]
        ]

    if week_number == 5:
        return [
            item(
                "Reel",
                "Reach",
                "Najlepsze momenty miesiąca",
                ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                [
                    "Wybrać najlepsze materiały z sierpnia",
                    "Zmontować dynamiczny materiał",
                    "Dodać polskie napisy"
                ]
            ),
            item(
                "Reel",
                "Trust",
                "Najlepsza historia klienta miesiąca",
                ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                [
                    "Wybrać najlepszą historię miesiąca",
                    "Pokazać proces i efekt",
                    "Uzyskać zgodę klienta"
                ]
            ),
            posts[0],
            stories[2],
            stories[1],
            stories[4]
        ]

    return []


def main():
    data = load_weekly_plan()

    output = {
        "month": data["month"],
        "strategy": data["strategy"],
        "approval_required": True,
        "recommended_frequency": {
            "Reels": "1-3 / tydzień",
            "Posts": "1-2 / tydzień",
            "Stories": "3-5 / tydzień"
        },
        "quality_rule": "Jakość ważniejsza niż częstotliwość.",
        "content_breaks": True,
        "weeks": []
    }

    for week in data["weeks"]:
        content = create_weekly_content(week["week"])

        output["weeks"].append({
            "week": week["week"],
            "date_from": week["date_from"],
            "date_to": week["date_to"],
            "content": content,
            "publishing_days": [],
            "status": "DRAFT"
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total = sum(len(w["content"]) for w in output["weeks"])

    print("\n" + "=" * 60)
    print("SWETTATTOO — CONTENT SCHEDULE")
    print("=" * 60)
    print(f"\nPLAN UTWORZONY: {OUTPUT_FILE}")
    print("\nStatus: DRAFT")
    print("Google Calendar: NIE ZMIENIONY")
    print("Akceptacja właściciela: WYMAGANA")
    print("\nLICZBA TYGODNI:", len(output["weeks"]))
    print("LICZBA ZAPLANOWANYCH MATERIAŁÓW:", total)

    print("\nCZĘSTOTLIWOŚĆ:")
    print("Reels: 1-3 / tydzień")
    print("Posts: 1-2 / tydzień")
    print("Stories: 3-5 / tydzień")

    print("\nZASADA:")
    print("Jakość ważniejsza niż częstotliwość.")
    print("Możliwe są dni bez publikacji.")

    print("\nNastępny etap:")
    print("PRZEGLĄD PLANU → WYBÓR DNI → AKCEPTACJA → GOOGLE CALENDAR")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
