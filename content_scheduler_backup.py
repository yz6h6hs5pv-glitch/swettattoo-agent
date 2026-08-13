import json
from pathlib import Path

WEEKLY_PLAN_FILE = "weekly_plan_august.json"
OUTPUT_FILE = "august_content_plan.json"


def load_weekly_plan():
    with open(WEEKLY_PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def create_weekly_content(week):
    week_number = week["week"]

    plans = {
        1: [
            {
                "type": "Reel",
                "goal": "Reach",
                "topic": "Duży projekt — historia realizacji",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać mocną realizację",
                    "Nagrać proces lub detale pracy",
                    "Wykonać zdjęcia gotowego tatuażu",
                    "Uzyskać zgodę klienta"
                ]
            },
            {
                "type": "Post",
                "goal": "Portfolio",
                "topic": "Najmocniejsza duża realizacja tygodnia",
                "platforms": ["Instagram", "Facebook", "Google Business", "Pinterest"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać najlepsze zdjęcia",
                    "Przygotować materiał pionowy i poziomy"
                ]
            },
            {
                "type": "Stories",
                "goal": "Trust",
                "topic": "Życie studia + opinia klienta",
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Nagrać naturalne ujęcia studia",
                    "Wybrać 1–3 opinie Google"
                ]
            }
        ],
        2: [
            {
                "type": "Reel",
                "goal": "Trust",
                "topic": "Historia klienta i jego projektu",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Nagrać konsultację lub fragment procesu",
                    "Pokazać wybrane etapy projektu",
                    "Nagrać efekt końcowy",
                    "Uzyskać zgodę klienta"
                ]
            },
            {
                "type": "Reel",
                "goal": "Expertise",
                "topic": "Dlaczego duży projekt daje więcej możliwości",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać przykład dużego projektu",
                    "Nagrać krótkie ujęcia detali",
                    "Przygotować materiał do napisów"
                ]
            },
            {
                "type": "Stories",
                "goal": "Social proof",
                "topic": "Opinie klientów",
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać aktualne opinie Google",
                    "Przygotować estetyczne Stories"
                ]
            }
        ],
        3: [
            {
                "type": "Reel",
                "goal": "Desire",
                "topic": "Cover-up lub trudna realizacja",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać mocny przykład",
                    "Nagrać problem → rozwiązanie → efekt",
                    "Wykonać zdjęcia Before / After",
                    "Uzyskać zgodę klienta"
                ]
            },
            {
                "type": "Post",
                "goal": "Portfolio",
                "topic": "Duża realizacja",
                "platforms": ["Instagram", "Facebook", "Pinterest", "Google Business"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać zdjęcia",
                    "Sprawdzić jakość materiału"
                ]
            },
            {
                "type": "Stories",
                "goal": "Studio life",
                "topic": "Letnia atmosfera Swettattoo",
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Nagrać spontaniczne materiały",
                    "Pokazać życie zespołu"
                ]
            }
        ],
        4: [
            {
                "type": "Reel",
                "goal": "International",
                "topic": "Swettattoo w Szczecinie — klienci zagraniczni",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "language": "PL + EN",
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać materiał pokazujący studio i Szczecin",
                    "Przygotować krótką wersję angielską",
                    "Pokazać atmosferę studia"
                ]
            },
            {
                "type": "Post",
                "goal": "Portfolio",
                "topic": "Najlepsza realizacja tygodnia",
                "platforms": ["Instagram", "Facebook", "Pinterest", "Google Business"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać najlepsze zdjęcia",
                    "Przygotować opis po polsku"
                ]
            },
            {
                "type": "Stories",
                "goal": "Engagement",
                "topic": "Pytania o tatuaże i Szczecin",
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Przygotować naklejkę pytań",
                    "Zebrać odpowiedzi"
                ]
            }
        ],
        5: [
            {
                "type": "Reel",
                "goal": "Reach",
                "topic": "Najlepsze momenty miesiąca",
                "platforms": ["Instagram", "Facebook", "TikTok", "YouTube Shorts"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać najlepsze materiały z sierpnia",
                    "Zmontować dynamiczny materiał",
                    "Dodać polskie napisy"
                ]
            },
            {
                "type": "Stories",
                "goal": "Trust",
                "topic": "Podsumowanie miesiąca + życie studia",
                "platforms": ["Instagram Stories"],
                "responsible_content": "Diana",
                "responsible_publication": "Blanka",
                "preparation": [
                    "Wybrać najlepsze momenty",
                    "Przygotować krótkie podsumowanie"
                ]
            }
        ]
    }

    return plans.get(week_number, [])


def main():
    data = load_weekly_plan()

    output = {
        "month": data["month"],
        "strategy": data["strategy"],
        "approval_required": True,
        "weeks": []
    }

    for week in data["weeks"]:
        content = create_weekly_content(week)

        output["weeks"].append({
            "week": week["week"],
            "date_from": week["date_from"],
            "date_to": week["date_to"],
            "content": content,
            "publishing_days": [],
            "status": "DRAFT"
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 60)
    print("SWETTATTOO — CONTENT SCHEDULE")
    print("=" * 60)

    print(f"\nPLAN UTWORZONY: {OUTPUT_FILE}")
    print("\nStatus: DRAFT")
    print("Google Calendar: NIE ZMIENIONY")
    print("Akceptacja właściciela: WYMAGANA")

    print("\nLICZBA TYGODNI:", len(output["weeks"]))

    total = sum(
        len(week["content"])
        for week in output["weeks"]
    )

    print("LICZBA ZAPLANOWANYCH MATERIAŁÓW:", total)

    print("\nNastępny etap:")
    print("PRZEGLĄD PLANU → WYBÓR DNI → AKCEPTACJA → GOOGLE CALENDAR")


if __name__ == "__main__":
    main()