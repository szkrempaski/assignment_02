"""
transform.py — the "T" in ETL.

Cleans raw, messy sales rows into usable values and computes the derived
numbers (revenue, per-item summaries, per-day summaries) that the report
programs display. No printing, no input, no file I/O — this module only
ever converts values in and returns values out.
"""

from typing import Any, Optional


def clean_currency(value: Optional[Any]) -> float:
    """Coerce a messy price value into a float, defaulting to 0.0 on failure."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s or s.upper() == "N/A":
        return 0.0

    s = s.replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def clean_quantity(value: Optional[Any]) -> int:
    """Coerce a messy quantity value into an int, defaulting to 0 on failure."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)

    s = str(value).strip()
    if not s:
        return 0
    try:
        return int(s)
    except ValueError:
        return 0


def clean_sales_data(raw_data: list[dict]) -> list[dict]:
    """Clean every raw row and attach a computed total_revenue key."""
    cleaned = []
    for row in raw_data:
        price = clean_currency(row.get("price"))
        qty = clean_quantity(row.get("qty"))

        new_row = dict(row)
        new_row["price"] = price
        new_row["qty"] = qty
        new_row["total_revenue"] = price * qty
        cleaned.append(new_row)
    return cleaned


def calculate_total_revenue(cleaned_data: list[dict]) -> float:
    """Sum total_revenue across every cleaned row."""
    return sum(row["total_revenue"] for row in cleaned_data)


def summarize_by_item(cleaned_data: list[dict]) -> list[dict]:
    """Group cleaned rows by item, summing units and revenue per item."""
    acc: dict[str, dict] = {}
    for row in cleaned_data:
        item = row["item"]
        if item not in acc:
            acc[item] = {"item": item, "units_sold": 0, "revenue": 0.0}
        acc[item]["units_sold"] += row["qty"]
        acc[item]["revenue"] += row["total_revenue"]

    summary = list(acc.values())
    summary.sort(key=lambda e: (-e["revenue"], e["item"]))
    return summary


def summarize_by_day(cleaned_data: list[dict]) -> list[dict]:
    """Group cleaned rows by date, summing units and revenue per day."""
    acc: dict[str, dict] = {}
    for row in cleaned_data:
        date = row["date"]
        if date not in acc:
            acc[date] = {"date": date, "units_sold": 0, "revenue": 0.0}
        acc[date]["units_sold"] += row["qty"]
        acc[date]["revenue"] += row["total_revenue"]

    summary = list(acc.values())
    summary.sort(key=lambda e: e["date"])
    return summary


def find_top_entry(summary: list[dict], field: str) -> dict:
    """Return the entry with the largest value in `field`; {} if empty."""
    if not summary:
        return {}

    top = summary[0]
    for entry in summary[1:]:
        if entry[field] > top[field]:
            top = entry
    return top