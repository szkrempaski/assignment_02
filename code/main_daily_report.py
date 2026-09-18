"""
main_daily_report.py — Operations department report.

Prints sales grouped by day so Operations can see when sales happen, not
just what sold. This report is written from scratch: everything it needs
(summarize_by_day, calculate_total_revenue, find_top_entry) already exists
in the package except summarize_by_day itself.
"""

import sys
from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    calculate_total_revenue,
    summarize_by_day,
    find_top_entry,
    print_day_table,
)


def main() -> None:
    seed = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        seed = int(sys.argv[1])

    raw_data = get_raw_sales_data(seed) if seed is not None else get_raw_sales_data()
    cleaned_data = clean_sales_data(raw_data)

    # Group by day (earliest first) instead of by item.
    day_summary = summarize_by_day(cleaned_data)

    # Reuses the same total_revenue calculation Finance uses — grouping by
    # day can't change how much money there was in total, so this number
    # should always match the Finance report's total.
    total_revenue = calculate_total_revenue(cleaned_data)

    # find_top_entry is generic, so it ranks days by field just like it
    # ranked items in the Marketing report.
    top_by_revenue = find_top_entry(day_summary, "revenue")
    top_by_units = find_top_entry(day_summary, "units_sold")

    print("=== OPERATIONS: Sales by Day ===")
    print()
    print_day_table(day_summary)
    print()
    print(f"Total Revenue:          ${total_revenue:,.2f}")
    print(f"Busiest day by revenue: {top_by_revenue['date']} (${top_by_revenue['revenue']:,.2f})")
    print(f"Busiest day by units:   {top_by_units['date']} ({top_by_units['units_sold']} units)")


if __name__ == "__main__":
    main()