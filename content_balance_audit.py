import json
from collections import Counter

with open("august_dated_content_plan.json", "r", encoding="utf-8") as f:
    d = json.load(f)

all_content = [
    item
    for week in d["weeks"]
    for item in week["content"]
]

goals = Counter(item.get("goal", "Unknown") for item in all_content)
types = Counter(item.get("type", "Unknown") for item in all_content)

print()
print("=" * 60)
print("SWETTATTOO — CONTENT BALANCE AUDIT")
print("=" * 60)

print()
print("TYPY PUBLIKACJI")
print("-" * 60)

for key, value in types.items():
    print(f"{key}: {value}")

print()
print("CELE PUBLIKACJI")
print("-" * 60)

for key, value in goals.items():
    print(f"{key}: {value}")

print()
print("TEMATY")
print("-" * 60)

for item in all_content:
    print(f"- {item['topic']}")

print()
print("=" * 60)
print("SPRAWDZENIE SPRZEDAŻY")
print("=" * 60)

sales_items = [
    item for item in all_content
    if item.get("goal") == "Sales"
    or "termin" in item.get("topic", "").lower()
    or "rezerw" in item.get("topic", "").lower()
]

print(f"Materiały sprzedażowe: {len(sales_items)}")

for item in sales_items:
    print(f"- {item['date']} | {item['type']} | {item['topic']}")

print()
print("=" * 60)
print("SPRAWDZENIE INTERNATIONAL")
print("=" * 60)

international = [
    item for item in all_content
    if item.get("goal") == "International"
    or "zagran" in item.get("topic", "").lower()
    or "szczecin" in item.get("topic", "").lower()
    or "niemcy" in item.get("topic", "").lower()
]

print(f"Materiały international: {len(international)}")

for item in international:
    print(f"- {item['date']} | {item['type']} | {item['topic']}")

print()
print("=" * 60)
print("AUDIT ZAKOŃCZONY")
print("=" * 60)
