def clean_currency(value):
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


def clean_quantity(value):
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


def clean_sales_data(raw_data):
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


def calculate_total_revenue(cleaned_data):
    return sum(row["total_revenue"] for row in cleaned_data)


def summarize_by_item(cleaned_data):
    acc = {}
    for row in cleaned_data:
        item = row["item"]
        if item not in acc:
            acc[item] = {"item": item, "units_sold": 0, "revenue": 0.0}
        acc[item]["units_sold"] += row["qty"]
        acc[item]["revenue"] += row["total_revenue"]
    summary = list(acc.values())
    summary.sort(key=lambda e: (-e["revenue"], e["item"]))
    return summary


def summarize_by_day(cleaned_data):
    acc = {}
    for row in cleaned_data:
        date = row["date"]
        if date not in acc:
            acc[date] = {"date": date, "units_sold": 0, "revenue": 0.0}
        acc[date]["units_sold"] += row["qty"]
        acc[date]["revenue"] += row["total_revenue"]
    summary = list(acc.values())
    summary.sort(key=lambda e: e["date"])
    return summary


def find_top_entry(summary, field):
    if not summary:
        return {}
    top = summary[0]
    for entry in summary[1:]:
        if entry[field] > top[field]:
            top = entry
    return top