from components._controllers import slider_size

VARIABLE_LABELS = {
    "SALE PRICE": "Sale price (USD)",
    "YEAR BUILT": "Year built",
    "TOTAL UNITS": "Total units",
}


def filter_sales(sales, borough, area_index):
    """Apply the same borough and m² limits to both visualizations."""
    area_limit = slider_size[area_index if area_index is not None else -1]
    filtered = sales.loc[sales["size_m2"] <= area_limit]
    if borough:
        filtered = filtered.loc[filtered["BOROUGH"] == borough]
    return filtered
