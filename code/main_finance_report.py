"""
main_finance_report.py — Finance department report.

Prints every transaction and the day's total revenue. Reads an optional
seed from the command line so Finance can regenerate the report against a
different dataset without touching this file.
"""

import sys
from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    calculate_total_revenue,
    print_sales_table,
)


def main() -> None:
    # sys.argv[0] is always the script name, so a seed (if given) is
    # sys.argv[1]. Treat a blank argument the same as "no seed" so the
    # debugger's seed prompt can't crash int("").
    seed = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        seed = int(sys.argv[1])

    # Extract: seeded data is reproducible for testing; no seed falls back
    # to the small fixed sample.
    raw_data = get_raw_sales_data(seed) if seed is not None else get_raw_sales_data()

    # Transform: clean the rows, then compute the single number Finance cares
    # about most.
    cleaned_data = clean_sales_data(raw_data)
    total_revenue = calculate_total_revenue(cleaned_data)

    # Load: display.py owns all formatting/printing, so no arithmetic or
    # string formatting happens below this line.
    print("=== FINANCE: Sales Transactions ===")
    print()
    print_sales_table(cleaned_data)
    print()
    print(f"Total Revenue: ${total_revenue:,.2f}")


if __name__ == "__main__":
    main()