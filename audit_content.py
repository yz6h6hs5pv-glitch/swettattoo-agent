import json
from collections import Counter

with open("august_dated_content_plan.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print()
print("=" * 60)
print("SWETTATTOO — AUGUST CONTENT AUDIT")
print("=" * 60)

for week in d["weeks"]:
    counts = Counter(item["type"] for item in week["content"])

    print()
    print(f"TYDZIEŃ {week['week']}")
    print("-" * 50)
    print(f"Reels:  {counts['Reel']}")
    print(f"Posts:  {counts['Post']}")
    print(f"Stories: {counts['Stories']}")

    for item in week["content"]:
        print(
            f"{item['date']} | "
            f"{item['type']:8} | "
            f"{item['goal']:15} | "
            f"{item['topic']}"
        )

print()
print("=" * 60)
print("KONTROLA LIMITÓW")
print("=" * 60)

for week in d["weeks"]:
    counts = Counter(item["type"] for item in week["content"])

    reels = counts["Reel"]
    posts = counts["Post"]
    stories = counts["Stories"]

    print()
    print(
        f"Tydzień {week['week']}: "
        f"Reels {reels}/1-3 | "
        f"Posts {posts}/1-2 | "
        f"Stories {stories}/3-5"
    )

    if not 1 <= reels <= 3:
        print("  UWAGA: Reels poza limitem")

    if not 1 <= posts <= 2:
        print("  UWAGA: Posts poza limitem")

    if not 3 <= stories <= 5:
        print("  UWAGA: Stories poza limitem")

print()
print("=" * 60)
print("AUDIT ZAKOŃCZONY")
print("=" * 60)
