from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cleaned_data.csv"


def load_sales_data(path=DATA_PATH):
    """Load sales once, preserving the original prices and floor areas."""
    sales = pd.read_csv(path, index_col=0)
    sales = sales.loc[sales["YEAR BUILT"] > 0].copy()
    sales["size_m2"] = sales["GROSS SQUARE FEET"] / 10.764
    sales["SALE DATE"] = pd.to_datetime(sales["SALE DATE"], format="%Y-%m-%d")
    return sales
