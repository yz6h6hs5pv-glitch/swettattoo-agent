import asyncio
from pathlib import Path
from datetime import date
from pydantic import BaseModel
from agents import Agent, Runner


# --------------------------------------------------
# 1. Структура одной задачи контент-плана
# --------------------------------------------------

class ContentTask(BaseModel):
    date: str
    responsible: str
    task_type: str
    platform: str
    title: str
    goal: str
    description: str
    hook: str
    cta: str


# --------------------------------------------------
# 2. Структура всего контент-плана
# --------------------------------------------------

class ContentPlan(BaseModel):
    week: str
    strategy: str
    tasks: list[ContentTask]


# --------------------------------------------------
# 3. Текущая дата
# --------------------------------------------------

today = date.today().strftime("%d.%m.%Y")


# --------------------------------------------------
# 4. Загружаем базу знаний
# --------------------------------------------------

knowledge_path = Path(__file__).parent / "swettattoo_knowledge.md"
knowledge = knowledge_path.read_text(encoding="utf-8")


# --------------------------------------------------
# 5. Создаём агента
# --------------------------------------------------

agent = Agent(
    name="Swettattoo Content Manager",

    instructions=f"""
Ты — AI-маркетолог и контент-менеджер Swettattoo.

Сегодняшняя дата: {today}.

Вся работа с контентом и задачами календаря должна
быть на ПОЛЬСКОМ языке.

Исключение:
если сам контент предназначен для немецкой аудитории,
текст публикации может быть на немецком.

Но задача в календаре всегда должна быть на польском языке,
чтобы Diana и Blanka понимали, что необходимо сделать.

================ KNOWLEDGE BASE ================

{knowledge}

============== END KNOWLEDGE BASE ==============

Твои основные принципы:

1. Начинай планирование с бизнес-целей.

2. Каждая задача должна иметь конкретную маркетинговую цель.

3. Не создавай контент только ради количества.

4. Учитывай премиальное позиционирование Swettattoo.

5. Не превращай Instagram в каталог татуировок.

6. Используй баланс:
   - sprzedaż;
   - eksperckość;
   - zaufanie;
   - marka osobista;
   - atmosfera;
   - proces;
   - social proof;
   - edukacja.

7. Учитывай направление Германии.

8. Учитывай сильные стороны Diana и Blanka.

9. Не назначай человеку задачи, которые плохо соответствуют
   его роли.

10. Не придумывай свободные даты мастеров.

11. Не придумывай факты о Swettattoo.

12. Не используй неподтверждённые обещания.

13. Один качественный материал можно адаптировать
   для нескольких платформ.

14. План должен быть реалистичным для выполнения.

15. После создания плана проверь:
   - есть ли продажи;
   - есть ли экспертность;
   - есть доверие;
   - есть немецкое направление;
   - нет ли повторов;
   - соответствует ли план премиальному бренду;
   - реально ли выполнить задачи.

16. Все даты должны относиться к будущей неделе
   относительно сегодняшней даты.

17. Все задачи должны быть на польском языке.

18. Каждая задача должна содержать:
   - дату;
   - ответственного;
   - тип задачи;
   - платформу;
   - название;
   - цель;
   - описание;
   - hook;
   - CTA.

19. task_type используй только из этих значений:

   - "Nagranie"
   - "Zdjęcia"
   - "Montaż"
   - "Tekst"
   - "Publikacja"
   - "Stories"
   - "Google Business"
   - "Pinterest"
   - "LinkedIn"
   - "Planowanie"

20. responsible используй только:
   - "Diana"
   - "Blanka"

21. Если одна публикация требует нескольких действий,
   создавай отдельные задачи.

Пример:

Nagranie → Diana

Montaż → Diana

Tekst → Blanka

Publikacja → Blanka

Не объединяй всё в одну задачу.

Не добавляй ничего в Google Calendar.
Сейчас нужно только создать структурированный план.
""",

    output_type=ContentPlan,
)


# --------------------------------------------------
# 6. Запуск агента
# --------------------------------------------------

async def main():

    result = await Runner.run(
        agent,
        """
Stwórz plan treści Swettattoo na przyszły tydzień.

Plan ma zawierać:

- przygotowanie materiałów;
- nagrania;
- zdjęcia;
- montaż;
- teksty;
- publikacje;
- Stories;
- Google Business;
- Pinterest;
- LinkedIn.

Uwzględnij zarówno zadania przygotowawcze,
jak i same publikacje.

Nie dodawaj niczego do Google Calendar.

Chcę otrzymać wyłącznie uporządkowany plan,
który później będzie można automatycznie
dodać do Google Calendar po mojej akceptacji.
"""
    )

    plan = result.final_output

    print("\n================ PLAN ================\n")

    print(f"Tydzień: {plan.week}")
    print(f"\nStrategia:\n{plan.strategy}\n")

    for i, task in enumerate(plan.tasks, start=1):

        print(f"\n--- ZADANIE {i} ---")
        print(f"Data: {task.date}")
        print(f"Odpowiedzialny: {task.responsible}")
        print(f"Typ: {task.task_type}")
        print(f"Platforma: {task.platform}")
        print(f"Tytuł: {task.title}")
        print(f"Cel: {task.goal}")
        print(f"Opis: {task.description}")
        print(f"Hook: {task.hook}")
        print(f"CTA: {task.cta}")

    import json

    output_path = Path(__file__).parent / "content_plan.json"

    output_path.write_text(
        json.dumps(
            plan.model_dump(),
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"\nPlan zapisany w: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())