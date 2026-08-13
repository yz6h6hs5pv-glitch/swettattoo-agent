from month_utils import resolve_month


def select_month():
    raw = input("Month (January-December, Sep, or 1-12): ").strip()
    month, number = resolve_month(raw)
    if month is None:
        print("Invalid month. Use January-December, Jan-Dec, or 1-12.")
        return None
    print(f"Selected: {month} ({number})")
    return month, number


if __name__ == "__main__":
    select_month()
