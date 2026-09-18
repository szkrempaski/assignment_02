"""
main_marketing_report.py — Marketing department report.

Prints per-item sales performance and highlights the top seller by revenue
and by units sold, which are often different products.
"""

import sys
from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    summarize_by_item,
    find_top_entry,
    print_item_table,
)


def main() -> None:
    # Same seed-handling as the Finance report: blank/missing argument
    # means "use the fixed sample data".
    seed = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        seed = int(sys.argv[1])

    raw_data = get_raw_sales_data(seed) if seed is not None else get_raw_sales_data()
    cleaned_data = clean_sales_data(raw_data)

    # Roll up cleaned rows into one entry per item, then find the two
    # different "winners" Marketing cares about.
    item_summary = summarize_by_item(cleaned_data)
    top_by_revenue = find_top_entry(item_summary, "revenue")
    top_by_units = find_top_entry(item_summary, "units_sold")

    print("=== MARKETING: Sales by Item ===")
    print()
    print_item_table(item_summary)
    print()
    # Revenue leader and units leader are printed separately because they're
    # often two different products (cheap-and-frequent vs. expensive-and-rare).
    print(f"Top seller by revenue: {top_by_revenue['item']} (${top_by_revenue['revenue']:,.2f})")
    print(f"Top seller by units:   {top_by_units['item']} ({top_by_units['units_sold']} units)")


if __name__ == "__main__":
    main()