import sys
from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    calculate_total_revenue,
    print_sales_table,
)


def main():
    seed = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        seed = int(sys.argv[1])

    raw_data = get_raw_sales_data(seed) if seed is not None else get_raw_sales_data()
    cleaned_data = clean_sales_data(raw_data)
    total_revenue = calculate_total_revenue(cleaned_data)

    print("=== FINANCE: Sales Transactions ===")
    print()
    print_sales_table(cleaned_data)
    print()
    print(f"Total Revenue: ${total_revenue:,.2f}")


if __name__ == "__main__":
    main()