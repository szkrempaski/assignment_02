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

    # Strip formatting characters ("$1,200.00" -> "1200.00") before parsing.
    s = s.replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        # Anything still unparsable ("garbage", etc.) is coerced to 0.0
        # rather than allowed to raise and kill the whole report.
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
        # Handles cases