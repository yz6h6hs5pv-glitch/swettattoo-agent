"""Centralized month selection and normalization for Swettattoo."""

MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

MONTH_ALIASES = {
    "jan": "January",
    "january": "January",
    "feb": "February",
    "february": "February",
    "mar": "March",
    "march": "March",
    "apr": "April",
    "april": "April",
    "may": "May",
    "jun": "June",
    "june": "June",
    "jul": "July",
    "july": "July",
    "aug": "August",
    "august": "August",
    "sep": "September",
    "sept": "September",
    "september": "September",
    "oct": "October",
    "october": "October",
    "nov": "November",
    "november": "November",
    "dec": "December",
    "december": "December",
}


def resolve_month(value):
    """Return (canonical English name, 1-based month number) or (None, None)."""
    if value is None:
        return None, None

    raw = str(value).strip()
    if not raw:
        return None, None

    if raw.isdigit():
        number = int(raw)
        if 1 <= number <= 12:
            return MONTHS[number - 1], number
        return None, None

    canonical = MONTH_ALIASES.get(raw.casefold())
    if canonical is None:
        return None, None

    return canonical, MONTHS.index(canonical) + 1


def month_filename(month_name, prefix=""):
    canonical, _ = resolve_month(month_name)
    if canonical is None:
        raise ValueError(f"Invalid month: {month_name}")
    return f"{prefix}{canonical.lower()}"
