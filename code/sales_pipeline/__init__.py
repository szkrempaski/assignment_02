"""
sales_pipeline — a small ETL package for cleaning and summarizing sales data.

Exposes only the functions a report author needs (Extract, Transform, Load
via display). Internal plumbing (clean_currency, clean_quantity) is
deliberately left out of __all__ since callers only ever need
clean_sales_data, not the row-level coercion it relies on.
"""

from .extract import get_raw_sales_data
from .transform import (
    clean_sales_data,
    calculate_total_revenue,
    summarize_by_item,
    summarize_by_day,
    find_top_entry,
)
from .display import print_sales_table, print_item_table, print_day_table

__all__ = [
    "get_raw_sales_data",
    "clean_sales_data",
    "calculate_total_revenue",
    "summarize_by_item",
    "summarize_by_day",
    "find_top_entry",
    "print_sales_table",
    "print_item_table",
    "print_day_table",
]